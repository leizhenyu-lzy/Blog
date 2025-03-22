#include <iostream>
#include <vector>
#include <list>

using namespace std;

int main()
{
	list<int> myList = { 1,2,3 };
	list<int> myList2 = { 11,22,33 };
	myList.splice(myList.begin(), myList2, ++myList2.begin(), ++++myList2.begin());

	return 0;
}
