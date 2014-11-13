Title: C++并行编程4
Date: 2014-8-25 23:20
Modified: 2014-8-25 23:20
Category: bigdata
Tags: C++
Slug: c-concurrency-in-action-4
Author: jacksu
Summary:基于C++11，并行线程编程的最大好处，就是可以数据共享，但最大的坏处也是数据共享，如果使用不当，最容易产生bug。本节介绍如何安全的共享数据，避免潜在的问题。
##共享数据的问题
所有问题都是由*共享数据更新*导致的，如果数据是只读的话，一个线程的读取，是不会影响其他线程的读取的。

###invariants
为了更好的理解代码，引入了invariants的概念。比如一个列表的元素个数，这个invariants，经常在更新列表中多于一个元素时打破。再如双向列表，删除一个元素，执行完`node->prev->next=node->next;`后，如果有另外一个线程读取，从左到右，那么就跳过该node，如果从右到左，还可以读到该node，那么就破坏了invariants，执行完`node->next->prev=node->prev`,才正常。
###race conditions
假设你买一张电影票去看电影，售票员有很多，同时在买票。你得到的座位必须看是否有人先比你预定。这就出现了race condition。race condition就是最后的结果依赖多个线程的执行顺序。race condition导致invariant破坏了，通常是有问题的，比如上面提到的双向列表中节点的删除。
###Avoiding problematic race conditions
避免race conditions导致的问题，通常有三种做法：

* > protection mechanism
* > lock-free programming
* > software transactional memory

##mutexes保护数据共享
不要传输一个指针或应用到锁可以保护的范围外，即不要作为函数返回值，不要存储在外部可见的空间中，不要作为用户函数的参数。如下面就是不安全的。

```
#include <mutex>

class some_data
{
    int a;
    std::string b;
public:
    void do_something()
    {}
};

class data_wrapper
{
private:
    some_data data;
    std::mutex m;
public:
    template<typename Function>
    void process_data(Function func)
    {
        std::lock_guard<std::mutex> l(m);
        func(data);
    }
};

some_data* unprotected;

void malicious_function(some_data& protected_data)
{
    unprotected=&protected_data;
}

data_wrapper x;

void foo()
{
    x.process_data(malicious_function);
    unprotected->do_something();
}

int main()
{
    foo();
}
```

消除接口中race conditions的方法，可供选择的有三种：

* > 传输引用
* > 拷贝构造函数和move构造函数可以throw异常
* > 返回指针指向poped项

根据上面的方法构造线程安全的stack。如下：

```
//
//  thread_safe_stack.cpp
//  cpp_concurrency
//
//  Created by jack on 14-8-31.
//  Copyright (c) 2014年 jack. All rights reserved.
//

#include "thread_safe_stack.h"
#include <exception>
#include <stack>
#include <mutex>
#include <memory>

struct empty_stack: std::exception
{
    const char* what() const throw()
    {
        return "empty stack";
    }
    
};

template<typename T>
class threadsafe_stack
{
private:
    std::stack<T> data;
    mutable std::mutex m;
public:
    threadsafe_stack(){}
    threadsafe_stack(const threadsafe_stack& other)
    {
        std::lock_guard<std::mutex> lock(other.m);
        data=other.data;
    }
    threadsafe_stack& operator=(const threadsafe_stack&) = delete;
    
    void push(T new_value)
    {
        std::lock_guard<std::mutex> lock(m);
        data.push(new_value);
    }
    std::shared_ptr<T> pop()
    {
        std::lock_guard<std::mutex> lock(m);
        if(data.empty()) throw empty_stack();
        std::shared_ptr<T> const res(std::make_shared<T>(data.top()));
        data.pop();
        return res;
    }
    void pop(T& value)
    {
        std::lock_guard<std::mutex> lock(m);
        if(data.empty()) throw empty_stack();
        value=data.top();
        data.pop();
    }
    bool empty() const
    {
        std::lock_guard<std::mutex> lock(m);
        return data.empty();
    }
};

int main()
{
    threadsafe_stack<int> si;
    si.push(5);
    std::shared_ptr<int> first=si.pop();
    std::cout<<*first<<std::endl;
    try {
        int x;
        si.pop(x);
    } catch (empty_stack e) {
        std::cout<<e.what()<<std::endl;
    }
    
}
```
###死锁
避免死锁的方法：

* > 如果拥有了一个锁，就尽量不要再请求另外一个锁
* > 调用用户的程序时，不要使用锁，你不知道用户的程序是否包含锁
* > 以一定的顺序调用锁，比如使用lock和lock_guard的结合
* > 使用hierarchy锁，只在运行时才可以检测

```
//
//  hierarchy_lock.cpp
//  cpp_concurrency
//
//  Created by jack on 14-8-31.
//  Copyright (c) 2014年 jack. All rights reserved.
//


/**
 *  hierarchical的不足就是，在运行时才可以检测
 */

#include "hierarchy_lock.h"
#include <mutex>
#include <stdexcept>
#include <thread>


class hierarchical_mutex
{
    std::mutex internal_mutex;
    unsigned long const hierarchy_value;
    unsigned long previous_hierarchy_value;
    static _Thread_local unsigned long this_thread_hierarchy_value;
    
    void check_for_hierarchy_violation()
    {
        if(this_thread_hierarchy_value <= hierarchy_value)
        {
            throw std::logic_error("mutex hierarchy violated");
        }
    }
    void update_hierarchy_value()
    {
        previous_hierarchy_value=this_thread_hierarchy_value;
        this_thread_hierarchy_value=hierarchy_value;
        std::cout<<"thread hierarchy value: "<<this_thread_hierarchy_value<<std::endl;
    }
public:
    explicit hierarchical_mutex(unsigned long value):
    hierarchy_value(value),
    previous_hierarchy_value(0)
    {}
    void lock()
    {
        //不需要catch，这样死锁就直接退出，这儿只是为了提示错误
        try{
            check_for_hierarchy_violation();
        }catch(std::logic_error e) {
            std::cout<<e.what()<<std::endl;
            return;
        }
        internal_mutex.lock();
        update_hierarchy_value();
    }
    void unlock()
    {
        this_thread_hierarchy_value=previous_hierarchy_value;
        internal_mutex.unlock();
    }
    bool try_lock()
    {
        
        check_for_hierarchy_violation();
        if(!internal_mutex.try_lock())
            return false;
        update_hierarchy_value();
        return true;
    }
};
_Thread_local unsigned long
hierarchical_mutex::this_thread_hierarchy_value(ULONG_MAX);

hierarchical_mutex high_level_mutex(10000);
hierarchical_mutex low_level_mutex(5000);

hierarchical_mutex other_mutex(100);

int do_low_level_stuff()
{
    return 42;
}


int low_level_func()
{
    std::lock_guard<hierarchical_mutex> lk(low_level_mutex);
    return do_low_level_stuff();
}

void high_level_stuff(int some_param)
{}


void high_level_func()
{
    std::lock_guard<hierarchical_mutex> lk(high_level_mutex);
    high_level_stuff(low_level_func());
}

void thread_a()
{
    high_level_func();
}

void do_other_stuff()
{}


void other_stuff()
{
    high_level_func();
    do_other_stuff();
}

void thread_b()
{
    std::lock_guard<hierarchical_mutex> lk(other_mutex);
    other_stuff();
}

int main()
{
    std::thread a(thread_a);
    if (a.joinable()) {
          a.join();
    }
    
    std::thread b(thread_b);
    if (b.joinable()) {
        b.join();
    }
    
}
``` 

