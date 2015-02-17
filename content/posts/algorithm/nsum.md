Title: N sum问题求解
Date: 2014-2-16
Modified: 2014-2-16
Category: algorithm
Tags: leetcode, algorithm, java
Slug: nsum
Summary: 对n个数的和为某个特定值问题的分析
Author: bigpotato

##对n个数的和为某个特定值问题的分析
本文对Leetcode上N sum的问题做一个综合分析，总结下解决这类问题的常见方法，具体代码采用java来实现。
###Two sum
>Given an array of integers, find two numbers such that they add up to a specific target number.The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.You may assume that each input would have exactly one solution.
Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2

[**Two sum LeetCode题目地址**](https://oj.leetcode.com/problems/two-sum/)

此题最直接的思路便是利用两个索引index1, index2, index1从数组开始扫描，index2从index1下一个扫描，判断两个索引上的数字和是否为给定的数值，这种方法时间复杂度为\\(O(n^2)\\),空间复杂度为\\(O(1)\\),这么容易想到当然不是最优解，下面介绍两种复杂度比较低的方法。


如果数组是有序数组，那么问题就被大大简化了，选择两个指针index1, index2分别指向数组第一个元素和最后一个元素，判断两个元素的和与给定数值val的大小关系，如果A[index1] + A[index] 等于 val那么找到两个下标返回即可；如果A[index1] + A[index2] < val，说明两个数的和还不够大，把左指针右移；否则两个数和太大，把右指针左移，直到两个指针交错。代码如下：

```java
class TwoSum {
    public int[] twoSum1(int[] numbers, int target)
    {
        int[] result = new int[2];

        int index1 = 0;
        int index2 = numbers.length - 1;

        Arrays.sort(numbers);

        while (index1 < index2) {
            //System.out.println("index1 = " + index1 + " index2 = " + index2);
            if (numbers[index1] + numbers[index2] == target) {
                result[0] = index1 + 1;
                result[1] = index2 + 1;
                break;

            } else if (numbers[index1] + numbers[index2] < target) {
                index1++;
            } else {
                index2--;
            }
        }
        return result;
    }
}
```
但题目描述中并没有说数组有序，上述算法可以用来判断一个数组中是否有两个数的和等于某个特定值，首先进行排序而后查找，排序可以采用快排、归并排序、堆排序等，平均时间复杂度为\\(O(nlogn)\\)，查找的时间复杂度是\\(O(n)\\)，所以说算法整体复杂度是\\(O(nlogn)\\)。


下面介绍一种利用空间换时间的方法，对数组A进行线性扫描，索引为index，目标值为target，只需要判断target - A[index]是否在数组中即可，对于判断某个数是否存在可以用哈希结构来降低时间复杂度，具体代码如下：
```java
public int[] twoSum2(int[] numbers, int target)
    {
        HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
        int[] result = {-1, -1};
        for (int i = 0; i < numbers.length; i++)
            map.put(numbers[i], i);

        for (int i = 0; i < numbers.length; i++) {
            if (map.containsKey(target - numbers[i])
                    && map.get(target - numbers[i]) != i) {
                result[0] = i + 1;
                result[1] = map.get(target - numbers[i]) + 1;
                break;
            }
        }

        return result;
    }
```
这种方法时间复杂度为\\(O(n)\\), 空间复杂度为\\(O(n)\\)。
###Three sum
>Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.

>**Note:**


>* Elements in a triplet (a,b,c) must be in non-descending order. 
>(ie, a ≤ b ≤ c)
>* The solution set must not contain duplicate triplets.



>```
>For example, given array S = {-1 0 1 2 -1 -4},
>A solution set is:
>(-1, 0, 1)
>(-1, -1, 2)
>```


[**Three sum LeetCode题目地址**](https://oj.leetcode.com/problems/3sum/)


这道题要求返回的是三个数的升序组合，不要求下标所以可以利用上一题的两种方法，要求元组(a, b, c)使得a + b + c = 0，对任意一个元素A[i],只要判断数组中是否存在A[j] + A[k] = target - A[i]，这样便可以转换成 **Two sum**问题了。由于题目要求返回的集合无重复且元组顺序非递减，可以先对数组进行排序，而后转换成 **Two sum** 问题。代码如下：
```java
public List<List<Integer>> threeSum(int[] num) {
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        Arrays.sort(num);
        int n = num.length;
        for (int i = 0; i <= n - 3; i++) {
            int j = i + 1;
            int k = n - 1;

            while (j < k) {
                if (num[i] + num[j] + num[k] == 0) {
                    List<Integer> tmp = new ArrayList<Integer>();
                    tmp.add(num[i]);
                    tmp.add(num[j]);
                    tmp.add(num[k]);
                    result.add(tmp);
                    //skip duplicates
                    do {
                        j++;
                    } while (j < k && num[j-1] == num[j]);
                    //skip duplicates
                    do {
                        k--;
                    } while (k > j && num[k] == num[k+1]);

                } else if (num[i] + num[j] + num[k] < 0) {
                    j++;
                } else {
                    k--;
                }
            }
            //skip duplicates
            while (i + 1 <= n - 3 && num[i] == num[i+1])
                i++;
        }

        return result;
    }
```
该算法的时间复杂度为\\(O(n^2)\\), 空间复杂度为\\(O(1)\\)。

###Four sum
>Given an array S of n integers, are there elements a, b, c, and d in S such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.

>**Note:**


>* Elements in a quadruplet (a,b,c,d) must be in non-descending order. (ie, a ≤ b ≤ c ≤ d)
>* The solution set must not contain duplicate triplets.
>For example, given array  S = {1 0 -1 0 -2 2}, and target = 0.


>```
>A solution set is:
>(-1,  0, 0, 1)
>(-2, -1, 1, 2)
>(-2,  0, 0, 2)
>```


[**Four sum LeetCode题目地址**](https://oj.leetcode.com/problems/4sum/)


Four sum的思路和Three sum一致，先选定某个数，就可以把问题转换为 **Three sum**，进而可以转换成 **Two sum**，不再赘述。

###3Sum Closest 
>Given an array S of n integers, find three integers in S such that the sum is closest to a given number, target. Return the sum of the three integers. You may assume that each input would have exactly one solution.


>```
>For example, given array S = {-1 2 1 -4}, and target = 1.
>The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
>```


[**Three sum closest LeetCode题目地址**](https://oj.leetcode.com/problems/3sum-closest/)

这道题和 **Three sum** 思路类似，也是转换成 **Two sum**, 只要在查找过程中更新当前最接近target的三个数的组合即可，最后返回这三个数的和。代码如下：
```java
    public int threeSumClosest(int[] num, int target) {
        Arrays.sort(num);
        int n = num.length;
        int min_diff = num[0] + num[1] + num[2] - target;
        for (int i = 0; i <= n - 3; i++) {
            int j = i + 1;
            int k = n - 1;

            while (j < k) {
                int cur_diff = num[i] + num[j] + num[k] - target;
                if (Math.abs(cur_diff) < Math.abs(min_diff)) {
                    min_diff = cur_diff;
                }

                if (cur_diff == 0) {
                    return target;

                } else if (cur_diff < 0) {
                    j++;
                } else {
                    k--;
                }
            }

        }

        return min_diff + target;
    }
```

###总结
总的来说nsum问题有点类似于递归算法，要想解决nsum，转而去解决(n-1)sum，(n-2)sum，...，2sum。只不过针对具体的题目要求要对数据进行排序、去重等操作。推广开来nsum问题可以在\\(O({m}^{n-1})\\)时间复杂度内完成，m为数组长度。