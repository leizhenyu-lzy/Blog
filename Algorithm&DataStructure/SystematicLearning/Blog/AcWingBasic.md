# AcWing算法基础课

[toc]

# Portals

[AcWing 算法基础课](https://www.acwing.com/activity/content/11/)
[AcWing 算法提高课](https://www.acwing.com/activity/content/16/)
[AcWing LeetCode究极班](https://www.acwing.com/activity/content/31/)


# 第一 算法基础（一） 快排+归并+二分

[常用代码模板1——基础算法](https://www.acwing.com/blog/content/277/)
[AcWing视频课](https://www.acwing.com/video/10/)

![](Pics/AcWingBasicPics/acwingBasic001.png)

## 快速排序（分治）

步骤：
1. 确定分界值（左值，右值，中间位置的值，随机位置的值）
2. （==重点==）重新划分区间，小于等于在左边，大于等于在右边
   1. 笨（占用额外空间）：暴力开两个数组
   2. 优美（不占用额外空间）：两个指针指两边分别向内移动，两个指针都找到两个不应该在该区间的数，交换...直至相遇
3. **递归**处理左&右




# 第二章 数据结构（一）

[AcWing视频课](https://www.acwing.com/video/15/)
[常用代码模板2——数据结构](https://www.acwing.com/blog/content/404/)

## 链表与邻接表（数组模拟）
数组模拟
1. 单链表，其中邻接表用的最多（用于存储图和树）
2. 双链表，优化某些问题

**单链表**
node(val, next)
head->null
head->node1->node2->null

数组模拟：①val[N] ②next[N]，存储下一个节点的下标，null用-1表示

**双链表**

## 栈与队列（数组模拟）

**栈** 先进后出

**队列** 先进先出


## KMP



