# LeetCode Book

[Book - 算法通关手册 LeetCode](https://algo.itcharge.cn/)

[Github Repository - 算法通关手册 LeetCode](https://github.com/itcharge/LeetCode-Py)

## Table of Contents

- [LeetCode Book](#leetcode-book)
  - [Table of Contents](#table-of-contents)
- [00 序言](#00-序言)
- [01 数组](#01-数组)
- [02 链表](#02-链表)
- [03 堆栈](#03-堆栈)
- [04 队列](#04-队列)
- [05 哈希表](#05-哈希表)
- [06 字符串](#06-字符串)
- [07 树](#07-树)
- [08 图](#08-图)
- [09 基础算法](#09-基础算法)
- [10 动态规划](#10-动态规划)
- [11 补充内容](#11-补充内容)
- [12 LeetCode 题解](#12-leetcode-题解)
  - [0000 - 0999](#0000---0999)
  - [1000 - 1999](#1000---1999)
  - [2000 - 2999](#2000---2999)

---

# 00 序言




---

# 01 数组

---

# 02 链表

---

# 03 堆栈

---

# 04 队列

---

# 05 哈希表

---

# 06 字符串

---

# 07 树

---

# 08 图

---

# 09 基础算法

---

# 10 动态规划

---

# 11 补充内容

---

# 12 LeetCode 题解

## 0000 - 0999

[438]

## 1000 - 1999

[1310 - XOR Queries of a SubArray](https://leetcode.com/problems/xor-queries-of-a-subarray/description) - `XOR` **a^0=a, a^a=0**， 提前建立数组

[1371 - Find the Longest Substring Containing Vowels in Even Counts](https://leetcode.com/problems/find-the-longest-substring-containing-vowels-in-even-counts/description) - TODO

[1684 - Count the Number of Consistent Strings](https://leetcode.com/problems/count-the-number-of-consistent-strings/description) - `ord([char])`返回单个字符Unicode，`chr(int)`返回Unicode对应字符

## 2000 - 2999

[2028 - Find Missing Observations](https://leetcode.com/problems/find-missing-observations/description/) - 先求平均数(向下取整)，然后把剩余差值一个个 +1 分配

[2220 - Minimum Bit Flips to Convert Number](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/description) - XOR-Operator(^) + BitwiseAnd(&) + RightShiftOperator(>>)

[2326 - Spiral Matrix IV](https://leetcode.com/problems/spiral-matrix-iv/description) - 上下左右 4 ptr - [YouTube 题解](https://www.youtube.com/watch?v=sOV1nRhmsMQ)

[2419 - Longest SubArray With Maximum Bitwise AND](https://leetcode.com/problems/longest-subarray-with-maximum-bitwise-and/description) - 位与 Bitwise AND，两个数按位与，只有两数相同时，结果才能等于最大值，否则都将小于两个数之间的最大值

[2807 - Insert Greatest Common Divisors in Linked List](https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/description) - [Euclidean Algorithm 辗转相除法](https://en.wikipedia.org/wiki/Euclidean_algorithm) 求最大公约数(Greatest Common)

```python
# 带余数除法 (x, y) = (a y + b , y)  -> (b, y) 找最大公约数 -> (y, b) 具体实现如下
while y != 0:
    x, y = y, x % y
return x
```


---


