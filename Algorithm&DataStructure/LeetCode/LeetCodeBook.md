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
  - [3000 - 3999](#3000---3999)
- [Appendix - 专题训练](#appendix---专题训练)

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

[169. Majority Element](https://leetcode.com/problems/majority-element/description/) - Moore 投票法，用数字相抵，最差情况是 majority 和 其他所有数相抵

[179. Largest Number](https://leetcode.com/problems/largest-number/description) - [YouTube 讲解](https://www.youtube.com/watch?v=WDx6Y4i4xJ8)
1. **自定义比较函数** : 普通函数 返回 `+1/0/-1`，`+1`表示第一个元素应该排在第二个元素之后，`-1`表示第一个元素应该排在第二个元素之前，`0`表示两个元素相等，顺序无所谓
2. **自定义排序** : `sorted(strNums, key=cmp_to_key(compare))`，`cmp_to_key` 是一个工具，将 比较函数 转换为 `Python 3` 中 `sorted()` 函数使用的 `键函数` - TODO(cmp_to_key 需要两个值，但是其他情况 只需要对原数进行一个映射，不需要两个数)
3. `sorted()` 函数 使用的是 **TimSort 排序算法** - TODO

[200. Number of Islands](https://leetcode.com/problems/number-of-islands/description/) - TODO 自己的写法对的，但是需要研究 DFS，BFS

[241. Different Ways to Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses/description) - [NeetCode](https://www.youtube.com/watch?v=cykVFFm5D3s) - [算法通关手册(LeetCode)](https://algo.itcharge.cn/Solutions/0200-0299/different-ways-to-add-parentheses/) - 分治算法 & 递归 - TODO

[539. Minimum Time Difference](https://leetcode.com/problems/minimum-time-difference/description) - BucketSort

[567. Permutation in String](https://leetcode.com/problems/permutation-in-string/description) - Fixed Length Sliding Window

[884. Uncommon Words from Two Sentences](https://leetcode.com/problems/uncommon-words-from-two-sentences/description) - `str.split(" ")` - `dict.items()` - List1 & List2 don't matter

[962. Maximum Width Ramp](https://leetcode.com/problems/maximum-width-ramp/description) - Preprocessing(**从后往前构建最大值List**) & 提速核心(**长度更短的不用看**，不需要从相邻位置开始扩展)



## 1000 - 1999

[1310. XOR Queries of a SubArray](https://leetcode.com/problems/xor-queries-of-a-subarray/description) - `XOR` **a^0=a, a^a=0**， 提前建立数组

[1331. Rank Transform of an Array](https://leetcode.com/problems/rank-transform-of-an-array/description) - TODO : Tim Sort

[1371. Find the Longest Substring Containing Vowels in Even Counts](https://leetcode.com/problems/find-the-longest-substring-containing-vowels-in-even-counts/description) - TODO

[1497. Check If Array Pairs Are Divisible by k](https://leetcode.com/problems/check-if-array-pairs-are-divisible-by-k/description) - 根据 余数 不同 进行分类/计数，判断 对应数量是否 match

[1590. Make Sum Divisible by P](https://leetcode.com/problems/make-sum-divisible-by-p/description) - TODO : 前缀余数列表

[1684. Count the Number of Consistent Strings](https://leetcode.com/problems/count-the-number-of-consistent-strings/description) - `ord([char])`返回单个字符Unicode，`chr(int)`返回Unicode对应字符

[1813. Sentence Similarity III](https://leetcode.com/problems/sentence-similarity-iii/description) - Deque / 2 Pointers

[1963. Minimum Number of Swaps to Make the String Balanced](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/description) - Stack to eliminate paired brackets

[1971. Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/description) - TODD : BFS & DFS




## 2000 - 2999

[2028. Find Missing Observations](https://leetcode.com/problems/find-missing-observations/description/) - 先求平均数(向下取整)，然后把剩余差值一个个 +1 分配

[2220. Minimum Bit Flips to Convert Number](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/description) - XOR-Operator(^) + BitwiseAnd(&) + RightShiftOperator(>>)

[2326. Spiral Matrix IV](https://leetcode.com/problems/spiral-matrix-iv/description) - 上下左右 4 ptr - [YouTube 题解](https://www.youtube.com/watch?v=sOV1nRhmsMQ)

[2419. Longest SubArray With Maximum Bitwise AND](https://leetcode.com/problems/longest-subarray-with-maximum-bitwise-and/description) - 位与 Bitwise AND，两个数按位与，只有两数相同时，结果才能等于最大值，否则都将小于两个数之间的最大值

[2490. Circular Sentence](https://leetcode.com/problems/circular-sentence/description) - Easy 题

[2491. Divide Players Into Teams of Equal Skill](https://leetcode.com/problems/divide-players-into-teams-of-equal-skill/description) - 记录 频次

[2696. Minimum String Length After Removing Substrings](https://leetcode.com/problems/minimum-string-length-after-removing-substrings/description) - Stack

[2807. Insert Greatest Common Divisors in Linked List](https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/description) - [Euclidean Algorithm 辗转相除法](https://en.wikipedia.org/wiki/Euclidean_algorithm) 求最大公约数(Greatest Common)

```python
# 带余数除法 (x, y) = (a y + b , y)  -> (b, y) 找最大公约数 -> (y, b) 具体实现如下
while y != 0:
    x, y = y, x % y
return x
```

## 3000 - 3999

[3394. Check if Grid can be Cut into Sections](https://leetcode.com/problems/check-if-grid-can-be-cut-into-sections/description) - 思路 : 合并区间(有 overlap 也 合并)


---

# Appendix - 专题训练

[Graph](https://leetcode.com/explore/featured/card/graph/)


[Dynamic Programming](https://leetcode.com/explore/featured/card/dynamic-programming/)




