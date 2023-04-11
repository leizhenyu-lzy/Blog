# 引用同一文件夹下的内容

from func import hello as hello2
import func as func2

if __name__ == "__main__":
    hello2()  # hello from subDir2
    func2.hello()  # hello from subDir2
  
  