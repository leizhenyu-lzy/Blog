def numIslands(grid) -> int:
    rows = len(grid)
    cols = len(grid[0])

    mat = [[0]*cols for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            mat[i][j] = ord(grid[i][j]) - ord("0")

    maxNum = rows * cols + 10

    dirs = [[-1, 0],
            [ 1, 0],
            [ 0,-1],
            [ 0, 1]]
    lenDir = 4

    tempList = []
    maxIslandIdx = 1
    islandDict = {}

    for i in range(rows):
        for j in range(cols):
            if mat[i][j] == 0:
                continue
            connect = maxIslandIdx + 1
            multiConnectList = []
            for dir in dirs:
                nexti = i + dir[0]
                nextj = j + dir[1]
                if nexti<0 or nexti>=rows:
                    continue
                if nextj<0 or nextj>=cols:
                    continue
                nextNum = mat[nexti][nextj]
                if mat[nexti][nextj] > 1:
                    connect = min(connect, nextNum)
                    multiConnectList.append(nextNum)
            mat[i][j] = connect
            if connect == maxIslandIdx + 1:
                maxIslandIdx += 1
            if connect in islandDict.keys():
                islandDict[connect].append([i,j])
            else:
                islandDict[connect] = [[i,j]]

            if len(multiConnectList) > 1:
                minConnect = min(multiConnectList)
                for tempConnect in multiConnectList:
                    if tempConnect != minConnect:
                        changeList = islandDict[tempConnect]
                        for r,c in changeList:
                            mat[r][c] = minConnect
                        islandDict[minConnect].extend(changeList)
                        islandDict.pop(tempConnect)

    return len(islandDict.keys())


if __name__ == '__main__':
    print(numIslands([["1","1","1"],["0","1","0"],["1","1","1"]]))
