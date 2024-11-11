def coinChange(coins, amount: int) -> int:
    history = [-1]*(amount+1)
    history[0] = 0

    for i in range(1, amount+1):
        tempMin = None
        for coin in coins:
            if i-coin<0:
                continue
            if history[i-coin] == -1:
                continue

            if tempMin is None:
                tempMin = history[i-coin] + 1
            else:
                tempMin = min(tempMin, history[i-coin] + 1)
        history[i] = tempMin

    return history[amount]


if __name__ == '__main__':
    print(coinChange([1,2,5], 11))