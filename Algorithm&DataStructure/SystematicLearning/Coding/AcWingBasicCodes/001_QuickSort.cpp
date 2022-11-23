# include <iostream>

using namespace std;

void quickSort(int array[],int left, int right)
{
    int pointerL = left-1, pointerR = right+1;  // 提前偏移，方便do-while
    if(left>=right)  // left&right相等时，表明子数组只有一个元素，无需排序
        return;

    int sepNum = array[left];  // 用于划分的值，使用左值，可以使用其他值
    // cout<<pointerL<<" "<<pointerR<<endl;
    while(pointerL<pointerR)
    {
        // 使用do-while，否则左右指针遇到两个相同值会死循环
        // 等于的也得换位置，否则不能保证划分值在正确位置（虽然会导致相同值交换）
        // 此外，快速排序保证的左边小于等于，右边大于等于
        do pointerL++;while(array[pointerL]<sepNum);
        do pointerR--;while(array[pointerR]>sepNum);
        if(pointerL<pointerR)
        {
            swap(array[pointerL], array[pointerR]);
        }
    }
    quickSort(array,left,pointerL-1);
    quickSort(array,pointerL,right);
}

int main()
{
    const unsigned long N = 1e6;
    int* array = new(nothrow) int[N];   // int array[N] = {};好像再g++中申请不了
    int n = 0;

    cout<<"enter n:"<<endl;
    cin>>n;
    for(int i=0;i<n;i++)
    {
        cin>>array[i];
    }
    
    quickSort(array,0,n-1);

    for(int i=0;i<n;i++)
    {
        cout<<array[i]<<" ";
    }

    return 0;
}
