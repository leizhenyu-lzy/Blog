import cv2
import numpy as np

def largestNumber(nums) -> str:

    strNums = [str(num) for num in nums]

    maxNum = max(nums)
    maxLength = len(str(maxNum))

    sortedStrNums = sorted(strNums, key=lambda numStr: numStr.ljust(maxLength, numStr[-1]))

    result = ""

    for i in reversed(sortedStrNums):
        result = result+i

    return result


if __name__ == '__main__':
    result = largestNumber(nums = [34323,3432])
    print(result)
