def makeFancyString(s: str):
    acc = s[0]
    len = 1
    result = acc
    for cur in s[1:]:
        if cur == acc:
            len += 1
        else:
            len = 1
            acc = cur

        if len<3:
            result+=cur

    return str(result)

if __name__ == '__main__':
    print(makeFancyString("leeetcode"))
