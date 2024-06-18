# Common Function

def checkSortStatus(testList, sortedList) -> bool:
    """
    [INPUT]

    testList : 待排序的数组 \n
    sortedList : 排序好的数组 \n
    ---
    [OUTPUT]

    bool : 检查结果(checkResult)
    """
    if sorted(testList) == sortedList:
        return True
    else:
        return False


import random

def generateRandomList(lenList=10, randMin=-5, randMax=6, printFlag=False) -> list:
    """
    [INPUT]

    lenList=10 : 待生成随机数组长度 \n
    randMin=-5, randMax=6 : 数字的上限&下限 [Min, Max) 会自动调整上下限关系\n
    printFlag=False : 是否打印标志位 \n
    ---
    [OUTPUT]

    randomList : 随机生成的(int数组)
    """
    if randMin > randMax:
        randMin, randMax = randMax, randMin
    elif randMin ==  randMax:
        randMax = randMin + int(lenList * 0.8)

    randomList = [random.randint(randMin, randMax) for _ in range(lenList)]
    if printFlag:
        print(f"randomList(lenList:{lenList}, randMin:{randMin}, randMax:{randMax}) : \n{randomList}")

    return randomList


def quickSortDoublePtr(outerList):
    """
    双指针实现方式
    左边
    右边


    边界问题

    """
    sortedList = outerList.copy()
    lenList = len(sortedList)

    if lenList <= 1:
        return sortedList

    leftPtr = 0
    rightPtr = lenList - 1

    pivotVal = sortedList[leftPtr]  # pivotVal 会被当做皮球来回踢

    while True:
        for rPos in range(rightPtr, leftPtr-1, -1):
            if sortedList[rPos] < pivotVal:
                sortedList[leftPtr] = sortedList[rPos]
                sortedList[rPos] = pivotVal
                leftPtr += 1
                rightPtr = rPos
                break

        if leftPtr == rightPtr:
            break

        for lPos in range(leftPtr, rightPtr+1, 1):
            if sortedList[lPos] >= pivotVal:
                sortedList[rightPtr] = sortedList[lPos]
                sortedList[lPos] = pivotVal
                rightPtr -= 1
                leftPtr = lPos
                break

        if leftPtr == rightPtr:
            break

    sortedList[0:leftPtr] = quickSortDoublePtr(sortedList[0:leftPtr])
    sortedList[rightPtr+1:lenList] = quickSortDoublePtr(sortedList[rightPtr+1:lenList])

    print(sortedList)

    return sortedList


testList = [1,2]
sortedList = quickSortDoublePtr(testList)
print(checkSortStatus(testList, sortedList))