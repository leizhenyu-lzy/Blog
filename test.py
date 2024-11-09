def maxArea(height) -> int:

    lines = len(height)
    lPtr = 0
    rPtr = lines - 1
    maxWater = 0

    while lPtr<rPtr:
        curWater = min(height[lPtr], height[rPtr])*(rPtr - lPtr)
        maxWater = max(maxWater, curWater)
        if height[lPtr] > height[rPtr]:
            rPtr -= 1
        else:
            lPtr += 1

    return maxWater


if __name__ == '__main__':
    print(maxArea([1,8,6,2,5,4,8,3,7]))