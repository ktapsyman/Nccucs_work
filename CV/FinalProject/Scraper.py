import sys
from lxml import html
import requests

BASE_URL = "https://shufa.supfree.net/dity.asp?page="
WORD_DETAIL_BASE_URL = "https://shufa.supfree.net/"
TOTAL_PAGE_NUM = int(sys.argv[1])

def ParseWordTable(DocRoot):
	XPath = "//div[@class='cdiv wenk']/a"
	WordDict = {}
	WordNodes = DocRoot.xpath(XPath)
	print(len(WordNodes))
	for WordNode in WordNodes:
		Text = WordNode.xpath("text()")[0]
		WordDict[Text] = WORD_DETAIL_BASE_URL+WordNode.get("href")
		print(WordDict[Text])
		#print(Text)

	return WordDict

def GetWordImageUrls(DocRoot):
	#TODO
	XPath = "//img"
	ImgNodes = [ImgNode for ImgNode in DocRoot.xpath(XPath) if "草?" in ImgNode.get("alt")]
	return []	

def Main():
	Session = requests.session()
	PageNum = 1
	
	while PageNum <= TOTAL_PAGE_NUM:
		PageUrl = BASE_URL + str(PageNum)
		print(PageUrl)
		WordTablePage = Session.get(PageUrl)
		if 200 != WordTablePage.status_code:
			#TODO
			#Retry
			print(WordTablePage.status_code)
			continue
		HtmlTree = html.fromstring(WordTablePage.content.decode("gbk"))
		for Word in ParseWordTable(HtmlTree):
			#TODO
			continue
		PageNum += 1
	return

Main()
