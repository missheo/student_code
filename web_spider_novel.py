import requests
from bs4 import BeautifulSoup
import os


class get_html:
    def __init__(self, url):
        self.url = url
        self.kv = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}

    def get(self):
        try:
            txt = requests.get(self.url, headers=self.kv)
            txt.raise_for_status()
            txt.encoding = txt.apparent_encoding
            return txt
        except:
            return None

class seek:
    def __init__(self, url, html,bool = False):
        self.url = url
        self.bool = bool
        self.html = html
        self.soup = BeautifulSoup(self.html.text, "html.parser")
        self.txt = ''
        self.next_link = ''
        self.biaoti = self.soup.title.text


    def seek_next_link(self):
        if self.bool is True:
            self.biaoti = self.biaoti.split("_")
            self.biaoti = self.biaoti[0] + '  ' + self.biaoti[1]

        if self.bool is False:
            self.biaoti = self.biaoti.split("_")
            self.biaoti = self.biaoti[1]

        for div3 in self.soup.find_all('a',  attrs={"id": "j_chapterNext"}):
            self.next_link = 'https:' + div3['href']

        if self.next_link == '':
            for div4 in self.soup.find_all('a'):
                if div4['href'][0:6] == "//read":
                    self.next_link = 'https:' + div4['href']
                    break
        return self.next_link,self.biaoti

    def seek_txt(self):
        for div1 in self.soup.find_all('div', attrs={"class": "read-content j_readContent"}):
            self.txt = div1.get_text().split('\n')
        return self.txt


class write_document:
    def __init__(self):
        pass
    
    
    def write_txt(self, text, title, name):
        with open("{}.txt".format(name), "a", encoding="utf-8") as f:
            f.write(title)
            f.write('\n')
            for index, txt in enumerate(text):
                if index == 1:
                    txt = txt.replace("\u3000\u3000", "\n\u3000\u3000")
                    f.write(txt)
            f.write('\n\n')
            f.close()


if __name__ == "__main__":
    # url = 'https://book.qidian.com/info/1015938738#Catalog'
    url = input("请输入网址：")
    index = 0
    while url[0:32] != 'https://read.qidian.com/lastpage':
        if index == 0:
            html = get_html(url).get()
            url, name = seek(url,html,True).seek_next_link()
            print('{:-^90}'.format(name))
            index += 1
        else:
            html = get_html(url).get()
            url, title = seek(url,html).seek_next_link()
            txt = seek(url,html).seek_txt()
            write_document().write_txt(txt,title,name)
            print("{}  {}   下载完成".format(title,url,end=""))
    print('{:-^90}'.format('结束'))
