# https://www.bilibili.com/video/BV1TD4y147VG/
import xml.etree.ElementTree as et
from xml.dom.minidom import Document


# 读入xml
xmlTree = et.ElementTree(file="multiObject.xml")
print(type(xmlTree))  # <class 'xml.etree.ElementTree.ElementTree'>

# 获取根节点
root = xmlTree.getroot()
print(type(root))  # <class 'xml.etree.ElementTree.Element'>
print(root)  # <Element 'annotation' at 0x000002509CDD17C0>

# 标签名和属性
print(root.tag)  # annotation
print(root.attrib)  # {}

# 循环访问元素
countObj = 0
print("循环访问元素")
for element in root:
    print(element.tag,element.attrib,element.text)
    if element.tag == "object":
        countObj = countObj+1
    for ele in element:
        print(ele.tag, ele.attrib,ele.text)
print("countObj : ", countObj)


# 索引方式访问元素
print("索引方式访问元素")

print(root[2][1].text)  # PASCAL VOC2007  对应annotation->source->annotation

print(root.findall("object"))
#[<Element 'object' at 0x0000029EF1D43B30>, <Element 'object' at 0x0000029EF1D43E50>, 
# <Element 'object' at 0x0000029EF1D451D0>, <Element 'object' at 0x0000029EF1D454F0>]

print(root.findall("object")[1][0].text)  # aeroplane
print(root.findall("object")[0].findtext("name"))  # aeroplane, 函数填入的不是要查找的字符串而是名称





# 初始化Document
doc = Document()
# 创建元素
root = doc.createElement("root")
doc.appendChild(root)
child = doc.createElement("child")
root.appendChild(child)

# 添加文本
root.setAttribute("attr1","123")
root.setAttribute("attr2","456")
text1 = doc.createTextNode("1")
root.appendChild(text1)

text2 = doc.createTextNode("2")
code = doc.createElement("code")
code.appendChild(text2)
root.appendChild(code)
# 生成xml

# 写入文件
with open('writeXML.xml',"w+") as f:
    f.write(doc.toprettyxml(encoding="UTF-8").decode("UTF-8"))
    f.close()

print(doc.toxml())