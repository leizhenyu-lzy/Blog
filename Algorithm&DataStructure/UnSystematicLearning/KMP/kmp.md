# KMP

## 00 传送门

[印度老哥讲KMP](https://www.bilibili.com/video/BV18k4y1m7Ar)

[轻松掌握KMP 细致讲解](https://www.bilibili.com/video/BV1iJ411a7Kb)

## 01 KMP简介

Knuth-Morris-Pratt

前缀表 prefix table

寻找最大前缀

## 02 最大前后缀表生成

前缀不包含最后一个字母

后缀不包含第一个字母

所以一个字母的最大前后缀为0

## 03  用最大前缀表去比较


## 代码实现

```cpp
#include <iostream>
#include <cstring>

using namespace std;

int naive_method(const char* const main, const char* const sub)//朴素方法
{
	int position = 0;//匹配到的位置

	int len_main = strlen(main);
	int	len_sub = strlen(sub);

	if (len_sub > len_main)//子串不能长于主串
		return -1;

	for (int start = 0; start <= len_main - len_sub; start++)
	{
		//strncmp//返回值 < 0，str1 < str2//返回值 > 0，str1 > str2//返回值 = 0，str1 = str2
		if (strncmp(main + position, sub, len_sub) != 0)//等于零说明匹配上，非零则表示有大小区别
			position++;
		else
			break;
	}

	if (position >= len_main - len_sub + 1)//没找到的判断，position理论上最大就是len_main-len_sub
		position = -1;

	return position;
}

int KMP(const char* const main, const char* const sub)//KMP
{
	int len_main = strlen(main);
	int	len_sub = strlen(sub);

	if (len_sub > len_main)//子串不能长于主串
		return -1;

	//prefix
	int* prefix = new int[len_sub];//动态申请前后缀数组

	for (int cnt = 0; cnt < len_sub; cnt++)
		prefix[cnt] = 0;//对prefix数组进行初始化

	int sub_former = 1, sub_latter = 0;//former在前（右）
	while (sub_former < len_sub)//如果子串为一个字符，不用做任何操作，蕴含于while条件中
	{
		if (sub[sub_former] == sub[sub_latter])//本位匹配成功
			prefix[sub_former++] = ++sub_latter;
		else
			if (sub_latter > 0)//虽然本位匹配失败，但是可能有更小的串可以匹配成功
				sub_latter = prefix[sub_latter - 1];
			else
				prefix[sub_former++] = 0;//也可以直接sub_former++因为本身已经初始化过了
	}

	//KMP match
	int pointer_main = 0;//指向主串的位置
	int pointer_sub = 0;//指向字串的位置
	int foundflag = 0;//标志是否找到

	while (pointer_main < len_main)//pointer_main有机会和len_main-1相同
	{
		if (main[pointer_main] == sub[pointer_sub])
		{
			pointer_sub++;
			pointer_main++;
			if (pointer_sub == len_sub)//说明全部匹配完成
			{
				foundflag = 1;
				break;
			}
		}
		else
		{
			if (pointer_sub == 0)//不存在公共前后缀
				pointer_main++;//从主串后一位开始比较
			else//存在前后缀，下次匹配可以节省
				pointer_sub = prefix[pointer_sub-1];
		}
	}
	delete[] prefix;//释放申请的前后缀数组空间

	if (foundflag != 1)
		return -1;
	else
		return pointer_main-pointer_sub;//两个指向位置的插值为字符的头位置
}

int main()
{
	char mainstr[] = "aaaaceaabcd";
	char deststr[] = "123";

	int pos_by_trad = naive_method(mainstr, deststr);
	int pos_by_KMP = KMP(mainstr, deststr);
	cout << "pos_by_trad: " << pos_by_trad << endl;
	cout << "pos_by_KMP : " << pos_by_KMP << endl;

	return 0;
}


```


