def countConsistentStrings(allowed: str, words) -> int:

    cnt = 0
    flag = False
    allowedSet = set(allowed)
    for word in words:
        word = list(set(word))
        for c in word:
            if not (c in allowedSet):
                flag = False
                break
        if flag is True:
            cnt+=1

    return cnt

if __name__ == '__main__':
    countConsistentStrings("ab", ["ad","bd","aaab","baa","badab"])
