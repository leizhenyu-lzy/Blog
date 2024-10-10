def maxWidthRamp(nums) -> int:
    lenNums = len(nums)
    maxRight = [-1]*lenNums
    maxDict = {}

    maxRight[-1] = nums[-1]
    tempMax = maxRight[-1]
    maxDict[nums[-1]] = lenNums - 1

    for ptr in range(lenNums-2,-1,-1):
        tempNum = nums[ptr]
        if tempNum > tempMax:
            maxDict[tempNum] = ptr
            tempMax = tempNum

        maxRight[ptr] = tempMax

    maxWidth=0

    for ptr in range(lenNums-1):
        nextPtr = ptr + 1
        tempNum = nums[ptr]
        if tempNum > maxRight[nextPtr]:
            continue


        while True:
            nextPtr = maxDict[maxRight[nextPtr]]
            maxWidth = max(maxWidth, nextPtr - ptr)

            nextPtr += 1
            if nextPtr == lenNums:
                break

    return maxWidth



if __name__ == '__main__':
    maxWidthRamp([6,0,8,2,1,5])

