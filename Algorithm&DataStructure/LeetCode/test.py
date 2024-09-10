# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

def spiralMatrix(m: int, n: int, head):

    if head is None:
        return [[-1]*n]*m


    lenList = 0
    # spiralMat = [[None]*n]*m
    spiralMat = [[None for _ in range(n)] for _ in range(m)]

    dirs = [[ 0, 1],
            [ 1, 0],
            [ 0, -1],
            [ -1, 0]]

    dirPtr = 0

    dirBounds = [   [-1, n],
                    [-1, m],
                    [-1, n],
                    [-1, m]]

    dirBoundCoords = [  1,
                        0,
                        1,
                        0]

    # nodePtr = head

    pos = [0, 0]

    curNum = -1

    for i in range(m * n):
        if i < len(head):
            curNum = head[i]
            # nodePtr = nodePtr.next
        else:
            curNum = -1

        curDir = dirs[dirPtr]
        curBound = dirBounds[dirPtr]
        curBoundCoord = dirBoundCoords[dirPtr]

        spiralMat[pos[0]][pos[1]] = curNum
        nextPos = [a + b for a, b in zip(pos, curDir)]

        if (curBound[0]<nextPos[curBoundCoord]<curBound[1]):
            if (spiralMat[nextPos[0]][nextPos[1]] is None):
                pass  # 不用换方向
            else:  # 需要换方向
                dirPtr = (dirPtr + 1) % 4
        else:  # 需要换方向
            dirPtr = (dirPtr + 1) % 4

        pos = [a + b for a, b in zip(pos, dirs[dirPtr])]  # update pos

    return spiralMat

if __name__ == '__main__':
    m=3
    n=5
    head = [3,0,2,6,8,1,7,9,4,2,5,5,0]

    result = spiralMatrix(m,n,head)
    print(result)