class urlopen():
    def __init__(self, url):
        # 开始爬虫
        import requests, bs4
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        response.encoding = "UTF-8"
        soup = bs4.BeautifulSoup(response.text, "lxml")

        # 获取代码
        CODE = soup

        # 获取文本内容
        TEXT = soup.body.text

        # 获取favicon
        try:
            FAVICON = soup.find("link", rel="icon")["href"]
        except:
            FAVICON = None

        # 获取网页标题
        try:
            TITLE = soup.find("title").text
        except:
            TITLE = None

        # 获取网址链接
        LINK = []
        for link in soup.find_all("a"):
            try:
                LINK.append(link["href"])
            except:
                pass

        # 获取图片链接
        IMAGE = []
        for image in soup.find_all("img"):
            try:
                IMAGE.append(image["src"])
            except:
                pass

        # 获取音频链接
        AUDIO = []
        for audio in soup.find_all("audio"):
            try:
                AUDIO.append(audio["src"])
            except:
                pass

        # 获取视频链接
        VIDEO = []
        for video in soup.find_all("video"):
            try:
                VIDEO.append(audio["src"])
            except:
                pass

        # 整理数据
        self.code = CODE
        self.text = TEXT
        self.favicon = FAVICON
        self.title = TITLE
        self.link = LINK
        self.image = IMAGE
        self.audio = AUDIO
        self.video = VIDEO

    def getElements(self, tag=None, **attribute):
        if "class_" in attribute:
            className = attribute["class_"]
            del attribute["class_"]
            attribute["class"] = className
            del className
        return self.code.find_all(name=tag, attrs=attribute)

    def getElementById(self, id):
        return self.code.find(id=id)

    def getElementByName(self, name):
        return self.code.find(name=None, attrs={"name": name})

    def getElementsByTag(self, tag):
        return self.code.find_all(tag)

    def getElementsByClass(self, class_):
        return self.code.find_all(class_=class_)

    def getElementsByStyle(self, style):
        return self.code.find_all(style=style)