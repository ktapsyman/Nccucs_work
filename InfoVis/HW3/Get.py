from lxml import html
import requests

Session = requests.session()
HtmlStr = Session.get("https://byronhu.wordpress.com/2013/09/09/%E5%8F%B0%E7%81%A3%E7%B8%A3%E5%B8%82%E7%B6%93%E7%B7%AF%E5%BA%A6/")
HtmlTree = html.fromstring(HtmlStr.content)
XPath = '//*[@id="post-2374"]/div[1]/table/tbody/tr'
print("{")
for Node in HtmlTree.xpath(XPath):
	ChildPath = "td"
	Tds = Node.xpath(ChildPath)
	NameNode = Tds[0].xpath("p/text()")
	LngNode = Tds[1].xpath("p/text()")
	LatNode = Tds[2].xpath("p/text()")
	print("	\"" + NameNode[0] + "\":[" + LngNode[0] + ", " + LatNode[0] +"],\\")
print("}")
