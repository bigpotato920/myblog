Title: fastjson序列化java对象
Date: 2016-2-16
Modified: 2016-2-16
Category: java
Tags: java, json
Slug: java_serialization
Summary: 利用fastjson对java对象进行序列化
Author: bigpotato

###fastjson和mybatis中驼峰命名和下划线分隔命名的转换

>最近在看外卖搜狗搜索项目的代码时发现，在给搜狗方返回的数据采用的是json格式，其中key的命名采用的是下划线分隔，为了方便Java类中属性命名就直接采用了下划线分隔的方式，对这种命名方式很不习惯，所以就搜索了相关资料找到解决办法。由此又想到了平时数据库中列命名多采用下划线分隔，在用mybatis进行查询时对返回结果需要人工转换成驼峰命名，才能给model正常赋值，查找资料后也有相应的解决方法。


* fastjson序列化中驼峰命名和下划线命名的转换

Java中把对象序列化成json有相应的类库可以使用，[Jackson](http://wiki.fasterxml.com/JacksonInFiveMinutes)，[fastjson](https://github.com/alibaba/fastjson)等，在序列化的时候需要对格式进行各种各样的定制，下面总结了利用fastjson序列化对象时格式定制的方法。Java语言规范的命名是采用驼峰式命名，在json中有些人习惯下划线分隔的命名方式，所以在把Java对象序列化成json格式的时候就存在命名方式转换的问题，查找fastjson资料时发现fastjson提供一个`JSONField`的注解来完成序列化时各种格式的定制。

1. 指定字段名
2. 配置序列化和反序列化的顺序
3. 格式化日期
4. 某个字段是否序列化、反序列化

下面通过具体代码介绍`JSonField`注解的使用方法

指定字段名

```java
public class Event {

    @JSONField(name="start_time")
    private int startTime;
    @JSONField(name="end_time")
    private int endTime;

    public Event(int startTime, int endTime) {
        this.startTime = startTime;
        this.endTime = endTime;
    }

    public int getStartTime() {
        return startTime;
    }

    public void setStartTime(int startTime) {
        this.startTime = startTime;
    }

    public int getEndTime() {
        return endTime;
    }

    public void setEndTime(int endTime) {
        this.endTime = endTime;
    }
}
```

在`Event`类中对连个属性`startTime`,`endTime`指定了`JSONField`注解，在序列化时相应的key就变成了`start_time`和`end_time`，进而完成了两个命名方式的转换。再也不会在Java类中生成蛋疼的`getStart_time()`这种命名方式的方法了。

配置序列化和反序列化的顺序
在用fastjson对Java对象进行序列化的时候，生成的json的key是按照字母顺序的，可以通过ordinal来指定序列化的顺序

```java
public static class VO {
    @JSONField(ordinal = 3)
    private int f0;

    @JSONField(ordinal = 2)
    private int f1;

    @JSONField(ordinal = 1)
    private int f2;
}
```

格式化日期

```java
 public class A {
      // 配置date序列化和反序列使用yyyyMMdd日期格式
      @JSONField(format="yyyyMMdd")
      public Date date;
 }
```

某个字段是否序列化、反序列化

```java
 public class A {
      @JSONField(serialize=false)
      public Date date;
 }

 public class A {
      @JSONField(deserialize=false)
      public Date date;
 }
```

* mybatis中驼峰命名和下划线命名的转换

在数据库创建的时候习惯把列用下划线分隔的方式来命名，而Java中model类的命名是采用驼峰式，在进行select操作时不能直接给model类赋值。

Java类

```java
package com.springapp.domain;

/**
 * Created by hjy on 6/28/15.
 */
public class Account {
    private long id;
    private String name;
    private String password;
    private int createTime;

    public Account() {
        this.createTime = (int)System.currentTimeMillis() / 1000;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public int getCreateTime() {
        return createTime;
    }

    public void setCreateTime(int createTime) {
        this.createTime = createTime;
    }

    @Override
    public String toString() {
        return "Account{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", password='" + password + '\'' +
                ", createTime=" + createTime +
                '}';
    }
}

```

数据库建表语句

```sql
CREATE TABLE `account` (
  `id` bigint(64) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

AccountDao

```java
@Component
public interface AccountDao {
    public static final String TABLENAME = "account";
    public static final String VIEW = "id, name, password, create_time As createTime";

    @Select("select " + VIEW + " from " + TABLENAME + " where id = #{id}")
    public Account selectById(long id);

    @Insert("insert into " + TABLENAME + "(name, password) values(#{name}, #{password}, #{createTime})")
    @Options(useGeneratedKeys = true, keyColumn = "id", keyProperty = "id", useCache = false, flushCache = true)
    public long createAccount(Account account);
}
```

注意到Account类中的`createTime`和sql中的`create_time`命名方式不一样，在做select操作时为了返回正确的Account对象，一种做法是做一个名字的转换，像AccountDao定义的`VIEW`字符串变量那样。另一种做法就是启用mybatis的`mapUnderscoreToCamelCase`的属性设置，来自动完成两种命名方式的转换。具体做法如下。

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <settings>
        <setting name="mapUnderscoreToCamelCase" value="true" />
    </settings>
</configuration>
```
然后指定配置文件的位置

```xml
  <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="springUnitTest"/>
        <property name="configLocation" value="classpath:mybatis-config.xml"></property>
	</bean>
```
