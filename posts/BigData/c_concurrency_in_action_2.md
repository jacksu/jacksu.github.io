Title: C++并行编程2
Date: 2014-8-23 23:20
Modified: 2014-8-23 00:20
Category: 大数据
Tags: C++
Slug: c-concurrency-in-action-2
Author: jacksu
Summary:基于C++11线程的基本管理，包括如何启动一个线程，如何等待一个线程结束，如何处理一个异常以及如何让一个线程后台运行。

##启动线程
查看线程构造函数，接受一个返回值为void的函数。如下：

```
void do_some_work();std::thread my_thread(do_some_work);
```
也可以接受一个重新定义操作符的类，如下：

```
class background_task{public:    void operator()() const    {        do_something();        do_something_else();    }};background_task f;std::thread my_thread(f);
```
但是下面这样使用是错误的，还以为是一个函数：

```std::thread my_thread(background_task());
```
可以这样使用：

```std::thread my_thread((background_task());std::thread my_thread{background_task()};
```
一个完全启动的例子为：

```
#include <thread>

void do_something(int& i)
{
    ++i;
}

struct func
{
    int& i;

    func(int& i_):i(i_){}

    void operator()()
    {
        for(unsigned j=0;j<1000000;++j)
        {
            do_something(i);
        }
    }
};


void oops()
{
    int some_local_state=0;
    func my_func(some_local_state);
    std::thread my_thread(my_func);
    my_thread.detach();
}

int main()
{
    oops();
}
```
只要线程构造时，传入了可执行代码，那么就开始执行，但是调用了detach，这样主线程就不会等待子线程，子线程共享了变量some_local_state，这样就导致非法访问。因此就需要等待子线程。

##等待线程

my_thread.detach()应该修改为my_thread.join();join()只能调用一次，如果调用过，那么joinable()就return false。

##异常处理

如果主线程还在做一些事情，那么就有可能异常退出，这样还是没有等待子线程，我们就要进行异常处理。有两种方法：

```
try
{
    do_something_in_current_thread();
}
catch(...)
{
	if(my_thread.joinable())
	{
    	my_thread.join();
    }
    throw;
}

```
或者

```
class thread_guard
{
    std::thread& t;
public:
    explicit thread_guard(std::thread& t_):
        t(t_)
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

##后台运行线程

就是调用detach().应用场景是，比如word编辑，建立一个新的文档就启动一个线程，两个文档之间不需要等待，这样就会后台运行线程。