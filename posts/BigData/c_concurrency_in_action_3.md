Title: C++并行编程3
Date: 2014-8-24 09:20
Modified: 2014-8-24 09:20
Category: bigdata
Tags: C++
Slug: c-concurrency-in-action-3
Author: jacksu
Summary:基于C++11，介绍std::thread是如何传递参数的，是如何转换所有权的，以及如何确定线程数和获得线程标识符。

##传参数给线程

线程参数默认是传值，copy进内存。下面看看几种错误的用法。

```
void f(int i,std::string const& s);void oops(int some_param){	char buffer[1024];
	sprintf(buffer, "%i",some_param);
	std::thread t(f,3,buffer);
	t.detach();}
```
会隐式把buffer转化为string，但是子线程先copy buffer，运行了才隐式转，有可能还没有转化，主线程就退出了，那么行为就未定义。那么我们可以修改为：

```
std::thread t(f,3,std::string(buffer));
```
别忘了线程默认是传值。

```
void update_data_for_widget(widget_id w,widget_data& data);void oops_again(widget_id w){    widget_data data;    std::thread t(update_data_for_widget,w,data);    display_status();    t.join();    process_widget_data(data);}
```
data是不会更新的，这样传给process_widget_data的还是原始值。应该这样使用：
```
std::thread t(update_data_for_widget,w,std::ref(data));```
如果想传给一个类中函数，可以这样：
```
class X{public:    void do_lengthy_work();};X my_x;std::thread t(&X::do_lengthy_work,&my_x);```
##所有权转换
thread是movable的，但不是copyable的，和ifstream等类似。（movable做一下简单解释，就是调用std:move()后，原来的对象为空）。如果我们想实现子线程等待，而不是有父线程join（`其实是没有父子关系的，完全是平等的，只是把最开始的线程习惯称为父线程`）。
```
1 void some_function();2 void some_other_function();3 std::thread t1(some_function);4 std::thread t2=std::move(t1);5 t1=std::thread(some_other_function);6 std::thread t3;7 t3=std::move(t2);8 t1=std::move(t3);```
第4行后，t2执行some_function，t1没有执行的线程。5行后，t1执行some_other_function，但是第5行没有显式调用std::move，是因为t1是临时变量，moving是原子的（`std::move()也是原子的`）。第7行后，t3执行some_function。第8行后，t1执行std::terminate，然后执行some_function。
线程的moving特性，是线程可以作为函数返回值或函数参数。如下：
```
std::thread f(){    void some_function();    return std::thread(some_function);}std::thread g(){    void some_other_function(int);    std::thread t(some_other_function,42);    return t;}```
```
void f(std::thread t);void g(){    void some_function();    f(std::thread(some_function));    std::thread t(some_function);    f(std::move(t));}```
前面的thread_guard可以用下面的方法实现。
```class thread_guard
{
    std::thread t;
public:
    explicit thread_guard(std::thread t_):
        t(std::move(t_)
    {}
    ~thread_guard()
    {
        if(t.joinable())
        {
            t.join();
        }
    }
    thread_guard(thread_guard const&)=delete;
    thread_guard& operator=(thread_guard const&)=delete;
};
```
```
thread_guard g(my_thread);      
do_something_in_current_thread();
```
##选择运行时的线程数
std::thread::hardware_ concurrency()这个函数可能是0，也可能是计算机核数。指示真正并行执行的线程数。

```
//
//  choosing_the_num_of_thread.cpp
//  cpp_concurrency
//
//  Created by jack on 14-8-24.
//  Copyright (c) 2014年 jack. All rights reserved.
//

#include <thread>
#include <numeric>
#include <algorithm>
#include <functional>
#include <vector>
#include <iostream>

template<typename Iterator,typename T>
struct accumulate_block
{
    void operator()(Iterator first,Iterator last,T& result)
    {
        result=std::accumulate(first,last,result);
    }
};

template<typename Iterator,typename T>
T parallel_accumulate(Iterator first,Iterator last,T init)
{
    unsigned long const length=std::distance(first,last);
    
    if(!length)
        return init;
    
    unsigned long const min_per_thread=25;
    //最大线程数
    unsigned long const max_threads=
    (length+min_per_thread-1)/min_per_thread;
    
    //确定计算机核数
    unsigned long const hardware_threads=
    std::thread::hardware_concurrency();
    
    //如果hardware_concurrency返回为0，我们取为2，不想运行太多的线程，
    //线程太多需要上下文切换，不能发挥更好的性能，太少就成为单线程了。线程数
    //不希望多于核数，不然也有上下文切换。
    unsigned long const num_threads=
    std::min(hardware_threads!=0?hardware_threads:2,max_threads);
    std::cout<<"hardware_threads:"<<hardware_threads<<" num_threads:"<<num_threads<<std::endl;
    
    //每个线程处理的长度
    unsigned long const block_size=length/num_threads;
    
    std::vector<T> results(num_threads);
    //还有个父线程
    std::vector<std::thread>  threads(num_threads-1);
    
    Iterator block_start=first;
    for(unsigned long i=0;i<(num_threads-1);++i)
    {
        Iterator block_end=block_start;
        std::advance(block_end,block_size);
        threads[i]=std::thread(accumulate_block<Iterator,T>(),
                               block_start,block_end,std::ref(results[i]));
        block_start=block_end;
    }
    accumulate_block<Iterator,T>()(block_start,last,results[num_threads-1]);
    
    //等待每个线程结束
    std::for_each(threads.begin(),threads.end(),
                  std::mem_fn(&std::thread::join));
    //把每个线程计算结果合起来
    return std::accumulate(results.begin(),results.end(),init);
}

int main()
{
    std::vector<int> vi;
    for(int i=0;i<50;++i)
    {
        vi.push_back(10);
    }
    int sum=parallel_accumulate<std::vector<int>::iterator,int>(vi.begin(),vi.end(),5);
    std::cout<<"sum="<<sum<<std::endl;
}

```

##线程标识符
std::thread::id 是可copy和比较的。可以通过std::this_thread::get_id()获得。