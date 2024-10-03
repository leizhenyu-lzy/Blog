def minSubarray(nums, p: int) -> int:
    sumNums = sum(nums)
    lenNums= len(nums)
    targetRemain = sumNums % p

    if targetRemain == 0:
        return 0

    currentSum = 0
    tempPos = 0
    remainDict = {0: -1}

    minLen = lenNums

    for i in nums:
        currentSum += i
        tempRemain = i % p

        remainDict[tempRemain] = tempPos

        aimKey = (tempRemain + p - targetRemain)%p

        if aimKey in remainDict.keys():
            minLen = min(minLen, tempPos - remainDict[aimKey])

        tempPos += 1  # 更新位置

    return minLen

if __name__ == '__main__':
    print(minSubarray([6,3,5,2], 9))
