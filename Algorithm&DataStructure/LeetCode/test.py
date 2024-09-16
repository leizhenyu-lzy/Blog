def findMinDifference(timePoints) -> int:
    # a day has 60 * 24 min
    timeList = [0] * (60*24)
    for timeStr in timePoints:
        hh = int(timeStr[0:2])
        mm = int(timeStr[3:5])

        totalTime = hh*60+mm

        timeList[totalTime] += 1
        if timeList[totalTime] == 2:
            return 0

    lptr = 0
    rptr = 1

    minGap = 24 * 60
    minTime = None
    maxTime = None

    print(sum(timeList))

    while rptr < 60*24:
        if timeList[lptr] == 0:
            lptr += 1
            rptr = lptr + 1
            continue

        if timeList[lptr] and minTime is None:
            minTime = lptr
            continue

        if timeList[lptr] == 1 and timeList[rptr] == 0:
            rptr += 1
            continue

        if timeList[lptr] == 1 and timeList[rptr] == 1:
            tempGap = rptr - lptr
            if tempGap < minGap:
                minGap = tempGap
            lptr = rptr
            maxTime = rptr
            rptr += 1
            continue

    # 还需比较 最大的时间 到第二天 最小的时间
    crossDayGap = 24 * 60 + minTime - maxTime

    if crossDayGap < minGap:
        minGap = crossDayGap

    return minGap


if __name__ == '__main__':
    timePoints = ["00:00","23:59"]
    result = findMinDifference(timePoints)
    print(result)
