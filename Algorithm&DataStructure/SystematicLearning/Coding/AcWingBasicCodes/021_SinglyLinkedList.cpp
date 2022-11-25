#include <iostream>

using namespace std;

const int N = 1e5;
int vals[N], nexts[N], headPtr=-1,savePtr = 0;  // head 和 save只是标识，不存节点
// head = -1表示空

void init()
{
    for (int i = 0; i < N; i++)
        nexts[i] = -1;
}

void orderHead(int x)
{
	vals[savePtr] = x;
	nexts[savePtr] = headPtr;
	headPtr = savePtr;
	savePtr++;
    //cout << savePtr << endl;
}

// 由于采用数组模拟，所以第k个数的数组下标为k-1，所以其后的数的数组下标为k

void orderDelete(int k)  // 删除下标为k的数
{
    if (k == 0)
    {
        headPtr = nexts[headPtr];
    }
    else
    {
        nexts[k-1] = nexts[nexts[k-1]];
    }
    //cout << savePtr << endl;
}

void orderInsert(int k, int x)  // 插在k的位置
{
	vals[savePtr] = x;
	nexts[savePtr] = nexts[k-1];
	nexts[k-1] = savePtr;
	savePtr++;
    //cout << savePtr << endl;
}

void dispLinkedList()
{
    for (int i = headPtr; i != -1; i = nexts[i])
    {
        cout << vals[i] << " ";
    }
    cout << endl;
}

int main()
{
    init();

    int orderNums = 0;
    char orderType = 0;
    int k = 0, x = 0;  // 位置&值，k从1开始，不是从0开始
    cin >> orderNums;
    for (int i = 0; i < orderNums; i++)
    {
        cin >> orderType;
        if (orderType == 'H')
        {
            cin >> x;
            orderHead(x);
        }
        else if (orderType == 'D')
        {
            cin >> k;
            orderDelete(k);
        }
        else if (orderType == 'I')
        {
            cin >> k >> x;
            orderInsert(k, x);
        }
    }
    dispLinkedList();
    return 0;
}

