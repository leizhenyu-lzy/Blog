# include <iostream>

using namespace std;

// 经典交替移动占位
void quickSortClassic(int array[],int left, int right)
{
    if(left>=right)
        return;
    int sepNum = array[left];
    int pL=left, pR = right;
    while(pL<pR)  // pL一开始指向left，方便把pR的数换过来。左边小于等于，右边大于。
    {
        if(array[pR]<=sepNum && pL<pR)
        {
            array[pL]=array[pR];
            pL++;
        }
        else
            return;
        if(array[pL]>sepNum && pL<pR)
        {
            array[pR]=array[pL];
            pR--;
        }
        else
            return;
    }
    cout<<"pL==pR?"<<(pL==pR)<<endl;
    array[pL]=sepNum;
    // 中间值不用排了
    if(pL-1>left)
        quickSortClassic(array,left,pL-1);
    if(pR+1<right)
        quickSortClassic(array,pR+1,right);
}


// 模板
void quickSort(int array[],int left, int right)
{
    if(left>=right)  // left&right相等时，表明子数组只有一个元素，无需排序
        return;

    int pointerL = left-1, pointerR = right+1;  // 提前偏移，方便do-while
    int sepNum = array[(left+right)>>1];  // 用于划分的值，可以是其他值，位运算右移一位相当于÷2
    // cout<<pointerL<<" "<<pointerR<<endl;
    while(pointerL<pointerR)
    {
        // 使用do-while，否则左右指针遇到两个相同值会死循环
        // 等于的也得换位置，否则不能保证划分值在正确位置（虽然会导致相同值交换）
        // 注意，快速排序保证的左边小于等于，右边大于等于，就算交换相同值仍满足
        do pointerL++;while(array[pointerL]<sepNum);
        do pointerR--;while(array[pointerR]>sepNum);
        if(pointerL<pointerR)
        {
            swap(array[pointerL], array[pointerR]);
        }
    }
    // pointerR会不断向左推进，直到找到小于sepNum的数，并标记
    // 不能用pointerL向右推进，用pointerL或者pointerL-1都不行
    // ①pointerL反例：假设abc，L指向a，R指向c，ac需要交换，下一次循环LR会同时指向b，
    // 使用pointerL，b如果大于sepNum，L也会停在哪里，应该使用L-1，而对于pointerR，会继续向左移动
    // ②pointerL-1反例：假设选取的sepNum，正好是最小值或最大值，则出错（选最小值会越界，选最大值会错分）
    // sepNum取最小值，R不会越界，一路走到最左；sepNum取最大值，R也会指着小于等于sepNum的值
    quickSort(array,left,pointerR);
    quickSort(array,pointerR+1,right);
}

int main()
{
    const unsigned long N = 1e5;
    int array[N] = {};
    int n = 0;

    cin>>n;
    for(int i=0;i<n;i++)
        cin>>array[i];
    
    quickSortClassic(array,0,n-1);

    for(int i=0;i<n;i++)
        cout<<array[i]<<" ";

    return 0;
}


