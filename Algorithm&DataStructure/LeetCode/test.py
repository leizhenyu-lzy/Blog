def areSentencesSimilar(sentence1: str, sentence2: str) -> bool:

    if len(sentence1) > len(sentence2):
        sentence1, sentence2 = sentence2, sentence1


    s1List = sentence1.split()
    s1ListLen = len(s1List)
    s2List = sentence2.split()
    s2ListLen = len(s2List)

    if s1ListLen > s2ListLen:
        return False

    if s1ListLen == 1:  # 单个单词 不能被夹在中间
        if s1List[0] == s2List[0] or s1List[0] == s2List[-1]:
            return True
        else:
            return False

    for word in s1List:
        if word not in s2List:
            return False

    # check insert front
    if s1List == s2List[s2ListLen - s1ListLen:s2ListLen]:
        print("insert front")
        return True


    # check insert end
    if s1List == s2List[0:s1ListLen]:
        print("insert end")
        return True


    # check insert middle
    wordPtr = 0
    for word in s1List:
        if word == s2List[wordPtr]:
            wordPtr += 1
        else:
            break

    if s1List[wordPtr:s1ListLen] == s2List[s2ListLen-s1ListLen+wordPtr:s2ListLen]:
        return True


if __name__ == '__main__':
    # print(areSentencesSimilar("eTUny i b R UFKQJ EZx JBJ Q xXz", "eTUny i R EZx JBJ xXz"))
    s = "abc"
    print(id(s))
    s[2] = 'd'
    print(s)
    s[2] = 'd'

