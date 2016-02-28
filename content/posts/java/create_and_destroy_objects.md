Title: Effective Java笔记 -- Creating and Destroying Objects
Date: 2015-5-1
Modified: 2015-5-1
Category: java
Tags: java, factory, singleton, objects
Slug: create_and_destroy_objects
Summary: effective java 笔记
Author: bigpotato

##Effective Java笔记 -- Creating and Destroying Objects

Effective Java 在这一章中讲解了对象创建和销毁方面的知识，包括什么时候怎样创建对象，什么时候如何避免创建对象，怎样确保对象被及时销毁，以及在对象销毁前怎么做好清理工作。下面分条款一一介绍。

###一、优先使用静态工厂方法而不是构造函数###

通常我们向外部提供一个类的公有构造函数，使得外部类能够得到一个类的实例，我们也可以提供一个**静态工厂方法**，即一个能够返回类的实例的静态方法。静态工厂方法既有优势又有劣势。

优点如下：

1. 通过静态工厂方法的名字能够准确表达返回对象类型
2. 静态工厂方法不必在每次调用时都创建对象
3. 静态工厂方法能够返回该类的子类型
4. 静态工厂方法可以避免冗长的类型列表，例如：

```java
	Map<String, List<String>> m = 
		new HashMap<String, List<String>>();
```

参数类型越复杂，类型列表越长，通过静态工厂方法，可以通过编译器的类型推断来帮助编写简洁的代码.

```java
	public static <K, V> HashMap<K, V> newInstance() {
		return new HashMap<K, V>();
	}
```
利用工厂方法可以把上面的实例化过长改成如下：

```java
	Map<String, List<String>> m = HashMap.newInstance();

```
当然静态工厂方法也有缺点：

1. 如果一个类只有静态工厂方法，没有public 或者 protected 类型的构造函数的话，这个类是不能被继承的。
2. 目前静态工厂方法还能和其它静态方法做一个很好的区分，不如构造函数那样在Java 的API doc中一眼就能看到。

###二、当有很多构造参数时可以考虑builder方法###

静态工厂方法和构造函数有一个共同的缺点：当可选的构造参数很多时它们的扩展性并不是很好。这里作者举了一个营养成分表标签的例子，在这些标签有一些可选项，例如：食用量，脂肪、卡路里含量等。我们可以通过下面的类来表示营养成分表。

```java
	public class NutritionFacts {
		private final int servingSize;
		private final int servings;
		private final int calories;
		private final int fat;
		private final int sodium;
		private final int carbohydrate;
		
		public NutritionFacts(int servingSize, int servings) {   		this(servingSize, servings, 0);	}
			public NutritionFacts(int servingSize, int servings,        int calories) {    	this(servingSize, servings, calories, 0);	}
			public NutritionFacts(int servingSize, int servings,        int calories, int fat) {   		this(servingSize, servings, calories, fat, 0);	}
			public NutritionFacts(int servingSize, int servings,        int calories, int fat, int sodium) {    	this(servingSize, servings, calories, fat, sodium, 0);	}
		public NutritionFacts(int servingSize, int servings,int calories, int fat, int sodium, int carbohydrate) {    	this.servingSize  = servingSize;		this.servings = servings;		this.calories = calories;		this.fat = fat;		this.sodium = sodium;		this.carbohydrate = carbohydrate;	}
}
```
这里的构造函数采用了一种可伸缩的模式，即提供了一个包含所有必备参数的构造函数，其它构造函数调用这个构造函数。但是当构造函数的参数列表很长时很难准确记住各个参数的位置，不得不去翻看api文档。一种解决方法是采用JavaBeans的模式，即把属性设置为私有，然后提供公有的setter和getter，但这种方式会把类型的初始化分割到多个调用中去，破坏了类初始化的原子性。采用builder模式能够很好地解决上面的问题，通过给静态工厂方法或者构造函数传入适当的参数来初始化类的实例，然后通过得到的builder初始化其它属性。

```java
public class NutritionFacts {
	private final int servingSize;
	private final int servings;
	private final int calories;
	private final int fat;
	private final int sodium;
	private final int carbohydrate;
	
	public static class Builder {
		// Required parameters;
		private final int servingSize;
		private final int servings;
		
		// Optional parameters
		private int calories = 0;
		private int fact = 0;
		private int carbohydrate = 0;
		private int sodium = 0;
		
		public Builder(int servingSize, int servings) {
			this.servingSize = servingSize;
			this.servings = servings;
		}
		
		public Builder calories(int val) {
			calories = val;
			return this;
		}
		
		public Builder fat(int val) {
			fat = val;
			return this;
		}
		
		public Builder carbohydrate(int val) {
			carbohydrate = val;
			return this;
		}
		
		public Builder sodium(int val) {
			sodium = val;
			return this;
		}
		
		public NutritionFacts build() {
			return new NutritionFacts(this);
		}
	}
	
	private NutritionFacts(Builder builder) {
		servingSize = builder.servingSize;
		servings = builder.servings;
		calories = builder.calories;
		fat = builder.fat;
		sodium = builder.sodium;
		carbohydrate = builder.carbohydrate;
	}
}
```

现在调用就可以变成下面这样：

```java
NutritionFacts cocaCola = new NutritionFacts.Builder(240,
	8).calories(100).sodium(35).carbohydrate(27).build();

```

我们可以把Builder抽象成一个接口，这样任何采用Builder pattern的类里德Builder类只要实现这个接口就可以了。

```java
public interface Builder<T> {
	public T build();
}

```

###三、通过私有构造函数或者枚举类型来实现单例

在JDK1.5之前有两种实现单例的方式，通过把类的构造函数设置为私有，通过一个公有的成员向外暴露类唯一的实例。一种是通过一个共有的实例变量：

```java
public class Elvis {
	public static final Elvis INSTANCE = new Elvis();
	private Elvis() {...}
	
	public void leaveTheBuilding() {...}
}
```

在这个例子中类的私有构造函数只会被调用一次，并且由于类中没有public或者protected修饰的构造函数，当类被继承时构造函数也只会被调用一次。
另一宗方法就是提供一个共有的静态工厂方法：

```java
public class Elvis {
	private static final Elvis INSTANCE = new Elvis();
	private Elvis() {...}
	public static Elvis getInstance() {return INSTANCE;}
	
	public void leaveTheBuilding() {...}
}
```

当这两种方法是饿汉式的，所以单例会在类加载后就被初始化。在JDK1.5中可以通过枚举类型来实现单例模式。

```java
public enum Elvis {
	INSTANCE;
	
	public void leaveTheBuilding() {...}
	
}
```

这种方法相当于第一种方法，但更为简洁，并且默认是线程安全的，还能够防止反序列化重新创建新德对象。是实现单例模式最好的方法。

###通过私有构造函数禁止类的实例化



















