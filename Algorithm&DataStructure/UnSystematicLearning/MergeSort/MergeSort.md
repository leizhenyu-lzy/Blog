# MergeSort 归并排序

## 冗长的版本（自己写的）
```cpp
#include <iostream>
#include <ctime>

using namespace std;

int Merge(int* data, int* sorted, int left, int right);
int MergeSort(int* data, int* sorted, int left, int right);

int main()
{
	clock_t start_time, end_time;
	start_time = clock();

	const int datalen = 10;
	int data[datalen] = { 1,3,0,-2 ,77,65,12,5,89,22 };
	int sorted[datalen] = { 0 };
	MergeSort(data, sorted, 0, datalen - 1);
	//result： -2 0 1 3 5 12 22 65 77 89
	for (int i = 0; i < datalen; i++)
		cout << sorted[i] << "  ";
	cout << endl;

	end_time = clock();
	cout << "程序运行时间：" << ((double)end_time - (double)start_time) / 1000 << endl;

	return 0;
}



int Merge(int* data, int* sorted,const int left,const int right)
{
	int middle = static_cast<int>((left + right) / 2);
	int left_pointer = left;
	int right_pointer = middle + 1;

	//此时left---middle，middle+1---right
	int store_bias = 0;

	while ((left_pointer != middle + 1) && (right_pointer != right + 1))
	{
		if (data[left_pointer] <= data[right_pointer])
		{
			sorted[left + store_bias] = data[left_pointer];
			left_pointer++;
		}
		else //if (data[left_pointer] > data[right_pointer])
		{
			sorted[left + store_bias] = data[right_pointer];
			right_pointer++;
		}
		store_bias++;
	}
	if (left_pointer == middle + 1)//左边存完了
	{
		while (right_pointer != right + 1)
		{
			sorted[left + store_bias] = data[right_pointer];
			right_pointer++;
			store_bias++;
		}
	}
	else //if (right_pointer == right + 1)//右边存完了
	{
		while (left_pointer != middle + 1)
		{
			sorted[left + store_bias] = data[left_pointer];
			left_pointer++;
			store_bias++;
		}
	}

	for (int cnt = left; cnt <= right; cnt++)
		data[cnt] = sorted[cnt];

	return 0;
}

int MergeSort(int* data, int* sorted,const int left,const int right)//left和right是两个边界
{
	int middle = static_cast<int>((left + right) / 2);

	if (left != right)
	{
		MergeSort(data, sorted, left, middle);//左边进行归并排序
		MergeSort(data, sorted, middle + 1, right);//右边进行归并排序
		Merge(data, sorted, left, right);//将左右进行合并
	}
	return 0;
}
```

## 精简版本

## 并行加速
