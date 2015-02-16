Title: thinking in java 中interface讲解笔记
Date: 2014-2-16
Modified: 2014-2-16
Category: java
Tags: java, interface
Slug: java_interface
Summary: thinking in java 中对interface的讲解笔记
Author: bigpotato

##Thinking in java 中interface讲解笔记
>Interfaces and abstract classes provide more structured way to separate interface from implementation.

在Java中提供了两种抽象类和接口机制给用户来抽象实现。
###抽象类
抽象类要用 **abstract** 关键字修饰，类中可以存在抽象方法，这种方法只有声明，没有具体实现，如：
```java
abstract void f();
```
你可以创建某个类A来继承抽象类，如果想创建A类的对象，在A类中必须实现所有抽象类中的抽象方法，否则类A也是一个抽象类，不能被实例化。抽象类的好处是可以给用户显示地提供对类的抽象，迫使用户去实现抽象方法，并在编译期进行检查。

###接口
接口对抽象的限制更加严格，在接口中所有方法都是抽象方法，都只有一个声明，没有实现，实现接口的类必须实现接口中的所有方法。
>An Interface says,"All classes that implement this particular interfae will look like this."Thus any code that use a particular interface knows what methods might be called for that interface, and that's all.So the interface is used to establish a "protocol" between classes.

接口和抽象类另一个不同点是类只能继承一个抽象类，但却可以实现多个接口，这点可以提供类似c++中多重继承的功能使得某个类可以转换成不同的父类型的类，但在语义上又更加合理。创建接口的时候用 **interface**关键字修饰，如果接口名字和所在文件同名，可以在inteface前加 **public** 修饰，如果不加public关键字修饰，那么接口是包访问权限，只能被同层包中其它类引用。接口中方法默认是用 **public
** 修饰的，所以在实现接口中的方法时一定要把方法声明为 **public**, 否则方法的默认访问权限是包访问权限，在Java中不允许在实现的时候降低了方法的访问权限。除了方法还可以有域，它们默认是被 **static** 和 **final** 修饰。

###通过继承扩展接口
在Java中接口通过继承的方式来扩展现有的接口，如代码所示：
```java
// Extending an interface with inheritance.
interface Monster {
    void menace();
}
interface DangerousMonster extends Monster {
    void destroy();
}
interface Lethal {
    void kill();
}
interface Vampire extends DangerousMonster, Lethal {
    void drinkBlood();
}
```
并且这中接口继承允许继承 **多个** 现有接口。
在扩展接口的时候，多个接口中可能存在同名函数，完全相同的函数不会出现问题，但是当函数签名相同但返回值不同时就会造成命名冲突。

```java
interface I1 {void f();}
interface I2 {int f();}
interface I3 extends I1, I2 {}

```

当接口I3要扩展I1和I2时两个函数f()完全相同造成命名冲突。这点在Java的编程规范中有说明：
>Two methods have the same signature if they have the same name and argument types.

###类转换成接口
>A common use for interfaces is the aftermentioned Strategy design pattern. You write a method that performs certain operations, and that method takes an interface that you also specify. You’re basically saying, "You can use my method with any object you like, as long as your object conforms to my interface." This makes your method more flexible, general and reusable.

即我们可以向任何实现了特定接口的类传递消息，或者说我们可以把任意实现了特定接口的对象传递给某个方法。
###接口变量初始化
接口中的变量默认为static final修饰，必须进行显示初始化。
###类和接的选择
>An appropriate guideline is to prefer classes to interfaces. Start with classes, and if it becomes clear that interfaces are necessary, then refactor. Interfaces are a great tool, but they can easily be overused.