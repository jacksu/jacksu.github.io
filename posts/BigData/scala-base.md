Title: Scala快速入门－基础
Date: 2015-1-1 11:20
Modified: 2015-1-1 11:20
Category: bigdata
Tags: spark
Slug: scala-base
Author: jacksu
Summary:2014年apache开源软件最火的应该是spark，没有之一。为了更好的掌握spark，scala应该是必须学习的。为了一周左右快速入门scala，对scala有个基本认识，不可能像学校那样拿着书系统学习，只能通过官网tutorial以及高手的总结（后面的参考资料）。现把scala的基本知识总结了一下，分享给大家。

##HelloWorld
从HelloWorld开始，使用scala IDE编辑器。
> * 新建scala project
> * 新建scala object
> * 编写HelloWorld
> * run as scala application
```
object HelloWorld {
  
  def main(args: Array[String]){
    println("Hello world")
  }
}
```
##表达式和值
scala中，几乎所有的元素都是表达式，以val定义常量，var定义变量
##函数
可以使用def来定义一个函数。函数体是一个表达式。
使用Block表达式的时候，默认最后一行的返回是返回值，如果不是递归函数，无需显式指定。
函数还可以像值一样，赋值给var或val。因此**函数也可以作为参数传给另一个函数**。
```
//定义函数，函数参数要指定类型签名
def square(a: Int) = a * a
def squareWithBlock(a: Int) = {
    a * a
}
//定义匿名函数，匿名函数由参数列表，箭头连接符和函数体组成
val squareVal = (a: Int) => a * a

def addOne(f: Int => Int, arg: Int) = f(arg) + 1

println("square(2):" + square(2))
println("squareWithBlock(2):" + squareWithBlock(2))
println("squareVal(2):" + squareVal(2))
println("addOne(squareVal,2):" + addOne(squareVal, 2))
```
执行结果：
```
square(2):4
squareWithBlock(2):4
squareVal(2):4
addOne(squareVal,2):5
```
`def log(msg: ＝> String)`按名称传递，参数只有在实际使用时才计算
##类
使用`class`定义类，使用`new`生成类，**构造函数不是特殊的方法，他们是除了类的方法定义之外的代码**。
```
class Calculator(brand: String) {
  /**
   * A constructor.
   */
  val color: String = if (brand == "TI") {
    "blue"
  } else if (brand == "HP") {
    "black"
  } else {
    "white"
  }

  // An instance method.
  def add(m: Int, n: Int): Int = m + n
}
val calc = new Calculator("HP")
calc.color
```
##特质（trait）
特质类似于java中interface，但trait则可以定义方法体，通过`with`关键字，一个类可以扩展多个特质：
`在scala中重写一个方法是需要指定override关键词的。如果重写一个方法时，没有加上override关键词，那么scala编译会无法通过。`
```
trait Friendly {
  def greet() = "Hi"
}

class Dog extends Friendly {
  override def greet() = "Woof"
}

class HungryDog extends Dog {
  override def greet() = "I'd like to eat my own dog food"
}

trait ExclamatoryGreeter extends Friendly {
  override def greet() = super.greet() + "!"
}

var pet: Friendly = new Dog
println(pet.greet())

pet = new HungryDog
println(pet.greet())

pet = new Dog with ExclamatoryGreeter
println(pet.greet())

pet = new HungryDog with ExclamatoryGreeter
println(pet.greet())
```
result:
Woof
I'd like to eat my own dog food
Woof!
I'd like to eat my own dog food!

##类型
泛型，可以到用`方括号`语法引入的类型参数
##object
scala中没有静态方法和属性，全部由singleton object（单例对象）来替代

##参考文献
http://zh.scala-tour.com/#/welcome
http://twitter.github.io/scala_school/zh_cn/index.html
[first step to scala](http://www.artima.com/scalazine/articles/steps.html)
[A Tour of Scala](http://www.scala-lang.org/old/node/104.html)

##广告
点击[Spark](http://jq.qq.com/?_wv=1027&k=g2JG15)加入群[Spark](http://jq.qq.com/?_wv=1027&k=g2JG15)，分享更多[Spark](http://jq.qq.com/?_wv=1027&k=g2JG15)相关信息