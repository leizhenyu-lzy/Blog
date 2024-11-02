# NeetCode

[NeetCode - Website](https://neetcode.io/)

[NeetCode - YouTube](https://www.youtube.com/@NeetCode/playlists)


## Table of Contents


# Leetcode BLIND-75 Solutions

[Leetcode BLIND-75 Solutions](https://www.youtube.com/playlist?list=PLot-Xpze53ldVwtstag2TL4HQhAnC8ATf)

## 01 - Two Sum

[0001. Two Sum](https://leetcode.com/problems/two-sum/description/)
1. hash : `dict (val:index)`

Python 中的 `set` 是一种无序的、可变的集合类型，底层主要是使用 哈希表(`hash table`) 来实现
1. 创建
    ```python
    s1 = set()
    s2 = {1, 2, 3, 4}
    s3 = set([1, 2, 2, 3, 4])  # # 从列表创建集合，自动去重
    s4 = s2.copy()  # 复制集合
    s5 = {3, 4, 5, 6}
    ```
2. 添加
    ```python
    s2.add(5)
    ```
3. 删除
    ```python
    s2.remove(3)  # 如果要删除一个不存在的元素，会引发 KeyError
    s2.discard(10)  # 不会有错误，即使10不在集合中
    s2.clear()  # 清空合集
    ```
4. 集合运算
    ```python
    # 并集
    union = s2 | s5  # {1, 2, 4, 5, 3, 6}
    union = s2.union(s5)  # 另一种写法
    # 交集
    intersection = s2 & s5  # {4, 5}
    intersection = s2.intersection(s5)
    # 差集
    difference = s2 - s5  # {1, 2}
    difference = s2.difference(s5)
    # 对称差集（在 s2 或 s5 中但不在两者中）
    symmetric_difference = s2 ^ s5  # {1, 2, 3, 6}
    symmetric_difference = s2.symmetric_difference(s5)
    ```
5. 集合关系
    ```python
    # 两个集合相等时，它们既是彼此的子集，也是彼此的超集
    is_subset = {1, 2}.issubset(s2)  # 子集，检查一个集合是否是另一个集合的子集
    is_superset = s2.issuperset({1, 2})  # 超集
    not_intersection = s2.isdisjoint(s5)  # 判断两个集合是否没有重叠的元素
    ```


Python 中的 `dict` 是通过 哈希表 `hash table` 的数据结构实现的，使得字典能够快速地进行插入、查找和删除操作
1. 创建
    ```python
    d1 = {}  # 创建一个空字典
    d2 = {'name': 'Alice', 'age': 25, 'city': 'New York'}  # 创建一个有元素的字典
    d3 = dict([('name', 'Bob'), ('age', 30)])  # 从列表创建字典  # 结果为 {'name': 'Bob', 'age': 30}
    ```
2. 添加 : `d2['job'] = 'Engineer'`
3. 修改 : `d2['age'] = 26`
4. 访问 : `name = d2['name']`
5. 删除
    ```python
    # 尝试删除不存在的键，会抛出 KeyError
    age = d2.pop('age')  # 删除字典中指定的键，并返回该键对应的值
    del d2['city']  # 没有返回值，直接执行删除操作
    d2.clear()  # 清空字典
    ```
6. 合并
    ```python
    d5 = {'name': 'Alice'}
    d6 = {'age': 25, 'city': 'Los Angeles'}

    # 使用 update() 合并字典
    d5.update(d6)  # d5 现在是 {'name': 'Alice', 'age': 25, 'city': 'Los Angeles'}
    # 使用解包操作符（Python 3.5 及以上）
    d7 = {**d5, **d6}  # 结果为 {'name': 'Alice', 'age': 25, 'city': 'Los Angeles'}

    # P.S. * 来解包一个可迭代对象，** 来解包一个字典
    ```
7. 字典推导式 : `squared = {x: x**2 for x in range(5)}`
8. 检查键 : `exists = 'name' in d4`
9. 字典方法 : `keys()`, `values()`, `items()  # 返回字典中的所有键值对`



## 02 - Best Time to Buy and Sell Stock

[121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/)
1. 方法1 : 前序最小 + 后序最大
2. 方法2 : 滑动窗口(双指针)，当右指针的值小于左指针的值，左指针滑动到右指针位置



## 03 - Contains Duplicate

[217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/description/)
1. 方法1 : sorting + adjacent search
   1. Time : `O(n logn)`
   2. Space : `O(1)`
2. 方法2 : hashSet - Python `set`。 比较 `list` & `set` 长度 或者 一位位添加并检查
   1. Time : `O(n)`
   2. Space : `O(n)`



## 04 -


## 05 -

## 06 -


## 07 -


## 08 -

## 09 -

## 10 -
## 11 -
## 12 -
## 13 -
## 14 -
## 15 -

## 06 -


## 07 -


## 08 -

## 09 -

## 10 -
## 11 -
## 12 -
## 13 -
## 14 -
## 15 -

## 16 -


## 17 -


## 18 -

## 19 -

## 20 -
## 21 -
## 22 -
## 23 -
## 24 -
## 25 -

## 26 -


## 27 -


## 28 -

## 29 -

## 30 -
## 31 -
## 32 -
## 33 -
## 34 -
## 35 -


[Algorithms & Data Structures for Beginners]()

Python 中的 `dict` 和 `set` 都使用 哈希表 `hash table` 作为底层数据结构

在处理键值对和唯一元素时都能提供高效的插入、查找和删除操作

[Advanced Algorithms]()

[System Design for Beginners]()

[System Design Interview]()

[Python for Beginners]()

[Python for Coding Interviews]()

[Python OOP]()

[Object Oriented Design Interview]()

[Design Patterns]()

[SQL for Beginners]()

[Full Stack Development]()

[Relational Database]()




