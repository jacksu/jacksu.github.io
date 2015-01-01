Title: Scala快速入门－基本数据结构
Date: 2015-1-1 13:20
Modified: 2015-1-1 13:46
Category: bigdata
Tags: spark
Slug: scala-datastruct
Author: jacksu
Summary:2014年apache开源软件最火的应该是spark，没有之一。为了更好的掌握spark，scala应该是必须学习的。为了一周左右快速入门scala，对scala有个基本认识，不可能像学校那样拿着书系统学习，只能通过官网tutorial以及高手的总结（后面的参考资料）。现把scala的基本知识总结了一下，分享给大家。

##模式匹配
使用用模式匹配实现斐波那契
```
def fibonacci(in: Any): Int = in match {
    case 0 => 0
    case 1 => 1
    case n: Int if(n > 1)=> fibonacci(n - 1) + fibonacci(n - 2)
    case _ => 0
}

println(fibonacci(3))
```
##元组tuple
元组可以保存不同类型的值，不能通过名称获取字段，而是使用位置下标来读取对象；而且这个下标基于1，而不是基于0。
```
val hostPort = ("localhost", 80)
println("host:%s,port:%s".format(hostPort._1,hostPort._2))
```
执行结果：
```
host:localhost,port:80
```
##选项 Option
Option 是一个表示有可能包含值的容器。
Option基本的接口是这样的：
```
trait Option[T] {
  def isDefined: Boolean
  def get: T
  def getOrElse(t: T): T
}
```
##映射 Map
Option本身是泛型的，并且有两个子类： Some[T] 或 None
Map.get 使用 Option 作为其返回值，表示这个方法也许不会返回你请求的值。
```
val map = Map(1 -> "one", 2 -> "two")
println(map.get(2))
println(map.get(3))
```
执行结果：
```
Some(two)
None
```
##函数组合子（Functional Combinators）
###map
map对列表中的每个元素应用一个函数，返回应用后的元素所组成的列表。
```
    val numbers = List(1, 2, 3)
    val double = numbers.map((i: Int) => i * 2)
    val squared = numbers.map((i: Int) => BigInt(i).pow(3))
    println("%s".format(numbers))
    println(double)
    println(squared)
    //传入一个部分应用函数
    def timesTwo(i: Int): Int = i * 2
    val doubleFunction = numbers.map(timesTwo _)
    println(doubleFunction)
```
执行结果：
```
List(1, 2, 3)
List(2, 4, 6)
List(1, 8, 27)
List(2, 4, 6)
```
###foreach
foreach很像map，但没有返回值。foreach仅用于有副作用[side-effects]的函数
```
    //foreach返回值为Unit即void
    val foreachResult = numbers.foreach { (i: Int) => i * 2 }
    println(foreachResult)
```
执行结果：
```
()
```
###filter
filter移除任何对传入函数计算结果为false的元素
```
    val filterResult = numbers.filter { (i: Int) => i % 2 == 0 }
    println(filterResult)
```
执行结果：
```
List(2)
```
###zip
zip将两个列表的内容聚合到一个对偶列表中，**多余的元素删除**
```
    val zipResult = numbers.zip(List('a', 'b', 'c', 'd'))
    println(zipResult)
```
执行结果：
```
List((1,a), (2,b), (3,c))
```
###partition
partition将使用给定的谓词函数分割列表。
```
    val partitionResult = numbers.partition { _ % 2 == 0 }
    println("partition result:%s".format(partitionResult))
```
执行结果：
```
partition result:(List(2),List(1, 3))
```
###find
find返回集合中第一个匹配谓词函数的元素
```
    var findResult = numbers.find(_ == 1)
    println("find result:%s".format(findResult))
    findResult = numbers.find(_ > 3)
    println("find result:%s".format(findResult))
```
执行结果：
```
find result:Some(1)
find result:None
```
###drop&dropWhile
drop删除前i个元素,dropWhile删除直到不满足谓词函数的元素
```
    var dropResult = numbers.drop(2)
    println("drop result:%s".format(dropResult))
    dropResult = numbers.dropWhile(_ % 2 != 0)
    println("dropWhile result:%s".format(dropResult))
```
执行结果：
```
drop result:List(3)
dropWhile result:List(2, 3)
```
###foldLeft&foldRight
0为初始值（记住numbers是List[Int]类型），m作为一个累加器,foldRight与foldLeft运行过程相反
```
    var foldLeftResult = numbers.foldLeft(0) {
      (m: Int, n: Int) => println("m:" + m + " n:" + n); m + n
    }
    println("foldLeft result:%s".format(foldLeftResult))
    var foldRightResult = numbers.foldRight(0) {
      (m: Int, n: Int) => println("m:" + m + " n:" + n); m + n
    }
    println("foldRight result:%s".format(foldRightResult))
```
执行结果：
```
m:0 n:1
m:1 n:2
m:3 n:3
foldLeft result:6
m:3 n:0
m:2 n:3
m:1 n:5
foldRight result:6
```
###flatten
flatten将嵌套结构扁平化为一个层次的集合
```
    var flattenResult = List(List(1, 2, 3), List(4, 5, 6)).flatten
    println("flatten result:%s".format(flattenResult))
```
执行结果：
```
flatten result:List(1, 2, 3, 4, 5, 6)
```
###flatMap
flatMap是一种常用的组合子，结合映射[mapping]和扁平化[flattening]。 flatMap需要一个处理嵌套列表的函数，然后将结果串连起来。flatMap是map和flatten的组合。
```
    val nestedNumbers = List(List(1, 2), List(3, 4))
    var flatMapResult = nestedNumbers.flatMap(x => x.map(_ * 2))
    println("flatMap result:%s".format(flatMapResult))
    flatMapResult = nestedNumbers.map(x => x.map(_ * 2)).flatten
    println("flatMap result:%s".format(flatMapResult))
```
执行结果：
```
flatMap result:List(2, 4, 6, 8)
flatMap result:List(2, 4, 6, 8)
```
##广告
点击[Spark](http://jq.qq.com/?_wv=1027&k=g2JG15)加入群[Spark](http://jq.qq.com/?_wv=1027&k=g2JG15)，分享更多[Spark](http://jq.qq.com/?_wv=1027&k=g2JG15)相关信息

