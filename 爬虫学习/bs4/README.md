BS4解析

对html文档进行解析,提取数据
BeautifulSoup 是 Python 库,它可以从 HTML 或 XML 文件中提取数据。
它是一个可以从复杂的文档中提取信息的库。

#禁用安全请求警告
requests.packages.urllib3.disable_warnings() 

/1. 导入BeautifulSoup库   
from bs4 import BeautifulSoup

/2. 打开网页文件并获取源码
/3. 创建BeautifulSoup对象,传入网页源码和解析器
soup = BeautifulSoup(html_doc, 'html.parser')  #告诉BeautifulSoup解析器使用html.parser解析器
html_doc:网页源码
'html.parser':解析器,这里使用的是html.parser

/4. 使用find()或find_all()方法查找元素

find()函数说明：
1. 根据标签名查找元素
p_tag = soup.find('p') 查找第一个<p>标签
print(p_tag) #返回该标签的所有内容
#<p class="intro">Beautiful Soup is a Python library for parsing HTML and XML documents.</p>
2. 根据属性查找元素
p_description = soup.find('p', class_='description')
print(p_description)
#<p class="description">It creates a parse tree for parsing HTML and XML documents.</p>
3. 根据文本查找元素
p_intro = soup.find(string="Beautiful Soup is a Python library for parsing HTML and XML documents.")
print(p_intro)
#Beautiful Soup is a Python library for parsing HTML and XML documents.
4. 多个条件组合查找元素
p_combined = soup.find('p', class_='description', string="It creates a parse tree for parsing HTML and XML documents.")
print(p_combined)
#<p class="description">It creates a parse tree for parsing HTML and XML documents.</p>

find_all()函数说明：
1.获取所有的<a>标签
links = soup.find_all('a') #返回的是一个列表
2.获取所有包含指定文本的<a>标签
links = soup.find_all('a', string='Python') #返回的是一个列表
3.获取所有class为s的<a>标签
links = soup.find_all('a', class_='s') #返回的是一个列表
or
links = soup.find_all('a', attrs={'class': 's'}) 

/5. 使用.get()方法获取标签在元素的属性值
#获取<a>标签的href属性值
c=link in links.get("href")
#http://example.com/elsie"

/6. 使用get_text() 方法用于从 HTML 标签中提取文本内容
text=soup.find('p', class_='intro').get_text()
print(text) 
#"Beautiful Soup is a Python library for parsing HTML and XML documents."