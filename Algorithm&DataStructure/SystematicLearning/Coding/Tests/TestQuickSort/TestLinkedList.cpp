#include <iostream>

using namespace std;

const int N = 1e5;
int vals[N], L[N], R[N], headPtr = -1, tailPtr = -1, savePtr = 0;  // head 和 save只是标识，不存节点
// head = -1表示空

void init()
{
    for (int i = 0; i < N; i++)
    {
        L[i] = -1, R[i] = -1;
    }
}

void orderL(int x)
{
    vals[savePtr] = x;
    R[savePtr] = headPtr;
    if(headPtr != -1)
        L[headPtr] = savePtr;
    headPtr = savePtr;
    if (tailPtr == -1)
        tailPtr = headPtr;
    savePtr++;
}

void orderR(int x)
{
    vals[savePtr] = x;
    L[savePtr] = tailPtr;
    if (tailPtr != -1)
        R[tailPtr] = savePtr;
    tailPtr = savePtr;
    if (headPtr == -1)
        headPtr = tailPtr;
    savePtr++;
}

void orderD(int k)  // 将第 k 个插入的数删除，删除数组下标为 k-1 的数
{
    if (headPtr == tailPtr)  // 是唯一的数
    {
        headPtr = -1, tailPtr = -1;
    }
    else if(k-1 == headPtr)  // 第一个数，且不是最后一个数
    {
        L[R[headPtr]] = -1;  // 跳过
        headPtr = R[headPtr];  // 重定位头指针
    }
    else if(k-1 == tailPtr)  // 最后一个数，且不是第一个数
    {
        R[L[tailPtr]] = -1;  // 跳过
        tailPtr = L[tailPtr];  // 重定位尾指针
    }
    else  // 中间的数
    {
        R[L[k - 1]] = R[k - 1];
        L[R[k - 1]] = L[k - 1];
    }
}

void orderIL(int k, int x)  // 在第 k 个插入的数（数组下标 k-1）左侧插入一个数，
{
    if (headPtr == k - 1)  // 插在头部
    {
        orderL(x);
    }
    else  // 保证了不会是第一个数也不会是最后一个数
    {
        vals[savePtr] = x;
        // 先将新节点连接好
        L[savePtr] = L[k-1];
        R[savePtr] = k - 1;
        // 再断开旧节点
        R[L[k - 1]] = savePtr;
        L[k - 1] = savePtr;

        savePtr++;
    }
}

void orderIR(int k, int x)  // 在第 k 个插入的数（数组下标 k-1）右侧插入一个数
{
    if (tailPtr == k - 1)  // 插在尾部
    {
        orderR(x);
    }
    else  // 保证了不会是第一个数也不会是最后一个数
    {
        vals[savePtr] = x;
        // 先将新节点连接好
        L[savePtr] = k - 1;
        R[savePtr] = R[k - 1];
        // 再断开旧节点
        L[R[k - 1]] = savePtr;
        R[k - 1] = savePtr;

        savePtr++;
    }
}


void dispLinkedList()
{
    for (int i = headPtr; i != -1; i = R[i])
    {
        cout << vals[i] << " ";
    }
    cout << endl;
}

int main()
{
    init();

    int orderNums = 0;
    int k = 0, x = 0;  // 位置&值，k从1开始，不是从0开始
    cin >> orderNums;
    for (int i = 0; i < orderNums; i++)
    {
        char orderType[3] = "";
        cin >> orderType;
        if (strcmp(orderType, "L")==0)  // 在链表的最左端插入数 x
        {
            cin >> x;
            orderL(x);
        }
        else if (strcmp(orderType, "R") == 0)  // 在链表的最右端插入数 x
        {
            cin >> x;
            orderR(x);
        }
        else if (strcmp(orderType, "D") == 0)  // 将第 k 个插入的数删除(数组下标为k-1的数删去)
        {
            cin >> k;
            orderD(k);
        }
        else if (strcmp(orderType, "IL") == 0)  // 在第 k 个插入的数左侧插入一个数
        {
            cin >> k >> x;
            orderIL(k, x);

        }
        else if (strcmp(orderType, "IR") == 0)  // 在第 k 个插入的数右侧插入一个数
        {
            cin >> k >> x;
            orderIR(k, x);
        }
    }
    dispLinkedList();
    return 0;
}

