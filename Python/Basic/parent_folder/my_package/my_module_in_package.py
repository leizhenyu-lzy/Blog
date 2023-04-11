import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),".."))
print(os.path.abspath(sys.path[-1]))

from my_module import func as ff

ff()


def func():
    print("my module in package")


