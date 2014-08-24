Title: C++并行编程1
Date: 2014-8-19 00:20
Modified: 2014-8-19 00:20
Category: bigdata
Tags: C++
Slug: c-concurrency-in-action-1
Author: jacksu
Summary:在C++11中的标准库中引入了线程库，这样就可以方便我们并行编程。什么时候需要并行编程呢？什么时候又不需要呢？并用线程库实现hello world。

##what is concurrency
我们可以一边看电视，一边唱歌。人并行非常容易理解，但是计算机呢？是不是我们一边编辑着word文档，一边听着歌，这样计算机就是在并行吗？不一定欧，如果你计算机是单核，就一定不是并行了，而是把你的任务分成你根本感觉不到的任务片，近似在并行执行，其实是在串行执行。如果是双核，也不一定，有可能一个核上同时执行两个任务，也有可能是并行欧，不同核执行不同的任务。

并行执行有两种实现方法：
多进程：启动比较复杂并且比较慢，操作系统需要额外的资源来管理进程，但是容易写比线程安全的代码。

多线程：线程之间更容易通信，启动和通信也比进程开销小。

##why use concurrency

> * 拆分任务
> * 合理利用性能

通常有三种并行的方法：
###task parallelism

把一个任务拆分成不同部分，并行执行

###data parallelism
把数据分成不同部分，线程在不同数据上执行相同操作。

###embarrassingly parallel
算法变为并行执行算法

##why not use concurrency

> * 执行任务容易完成，但是线程启动也需要开销
> * 启动线程太多，容易消耗完内存和地址空间（特别是32位机器），容易消耗完系统资源，比如每个链接建立一个线程，还有切换开销。

##hello world

需要在C++11环境下编译。

```
	#include <iostream>
  	#include <thread>
  
  	void hello()
  	{
  	     std::cout<<"hello world"<<std::endl;
  	}
 
 	int main()
 	{
 	    std::thread t(hello);
 	    t.join();
 	    return 0;
 	}
 ```
