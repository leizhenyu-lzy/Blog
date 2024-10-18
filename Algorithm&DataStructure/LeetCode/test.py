def smallestRange(nums):
    lenNums = len(nums)
    events = []
    for numList in nums:
        events.append((numList[0], 1))  # 1表示入
        for num in list(set(numList[1:-1])):  # 通过set保证
            events.append((num, -1))  # -1 表示出
            events.append((num, 1))  # 1 表示入
        events.append((numList[-1]+1, -1))  # 结束时的出，需要延迟减


    events.sort(key = lambda x:(x[0], x[1]))  # 要先出后入
    # lenEvents = len(events)

    # formerPos = events[0][0]
    # eventIdx = 0
    cnt = 0
    possiblePosList = []

    for pos, motion in events:
        cnt += motion
        if cnt == lenNums:
            possiblePosList.append(pos)

    minGap = 3 * 10**5  # 根据 数据 constrains
    l, r = None, None

    for idx in range(len(possiblePosList)-1):
        tempL = possiblePosList(idx)
        tempR = possiblePosList(idx+1)
        tempGap = tempR - tempR
        if tempGap < minGap:
            minGap = tempGap
            l, r  = tempL, tempR

    return [l, r]



if __name__ == '__main__':
    result = smallestRange([[1,2,3],[1,2,3],[1,2,3]])
    print(result)

