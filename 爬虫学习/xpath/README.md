xpath解析:
XPath（XML Path Language）是一种用于在XML文档中导航和选择节点的语言。
它也可以用于HTML文档，因为HTML是XML的一个子集。
XPath通过路径表达式来选择节点或节点集。
节点：XML或HTML文档中的元素、属性、文本内容等。
路径表达式：用于定位节点的语法，例如 /html/body/div。
常用路径表达式：
//：选取文档中的所有节点，包括元素、属性、文本等。
/：从根节点选取。
.：选取当前节点。
..：选取当前节点的父节点。
@：选取属性。
[]：用于条件筛选。

xpath使用
/1. 导入lxml库
from lxml import etree

#注意编码格式,否则可能出现中文乱码
/2. 获取网页源码
html_text = requests.get('https://www.example.com').text

/3. 创建etree对象,解析HTML文档  
tree = etree.HTML(html_text)

/4. 使用xpath()方法查找元素 
#查找指定div标签的全部p标签（前提是有多个p标签）默认从1开始即第一个标签
result = tree.xpath('//div[@class="content"]/p')
获取文本内容
for i in result:
    print(i.xpath('text()'))
or
result = tree.xpath('//div[@class="content"]/p/text()')
for i in result:
    print(i)

#查找指定div标签的第一个p标签
result = tree.xpath('//div[@class="content"]/p[1]')
获取文本内容
print(result.xpath('text()'))

/5. 使用.get()方法获取元素的属性值
result = tree.xpath('//div[@class="content"]/p/text()')[0].get('class')
print("class:",result)