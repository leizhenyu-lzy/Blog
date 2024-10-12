def minGroups(intervals) -> int:
    events = []
    for l, r in intervals:
        events.append((l, 1))
        events.append((r+1, -1))

    events.sort(key=lambda x:(x[0], +x[1]))

    print(events)

    currentIntervals = 0
    maxIntervals = 0

    for event in events:
        currentIntervals += event[1]
        maxIntervals = max(maxIntervals, currentIntervals)

    return maxIntervals



if __name__ == '__main__':
    print(minGroups([[5,10],[6,8],[1,4],[2,3]]))

