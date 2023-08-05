# urlopenlib
## 这个库可以用来爬虫，非常实用。现在我开始教大家如何用urlopenlib库。

###导库
```python
import urlopenlib
#导库
```

### 爬虫准备
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
#<__main__.urlopen object at 0x008AC670>
```

### 获取代码
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
code=url.code
print(code)
#类型：BeautifulSoup
#代码很长，就不展示了，可以自己去实践一下
```

### 获取文本内容
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
text=url.text
print(text)
#类型：str
#代码很长，就不展示了，可以自己去实践一下
```

### 获取favicon
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
favicon=url.favicon
print(favicon)
#类型：str
#/favicon.ico
```

### 获取网页标题
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
title=url.title
print(title)
#类型：str
#百度一下，你就知道
```

### 获取网址链接
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
link=url.link
print(link)
#类型：list
#代码很长，就不展示了，可以自己去实践一下
```

### 获取图片链接
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
image=url.image
print(image)
#类型：list
#代码很长，就不展示了，可以自己去实践一下
```

### 获取音频链接
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
audio=url.audio
print(audio)
#类型：list
#[]
```

### 获取视频链接
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
video=url.video
print(video)
#类型：list
#[]
```

### 查找元素（可通过标签和属性来查找）
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
elements=url.getElements(tag="p")
print(elements)
#类型：list
#代码很长，就不展示了，可以自己去实践一下
```

###通过id属性查找元素
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
element=url.getElementById(id="")
print(element)
#类型：list
#以上代码是一个示例
#注：只能查找第一个元素，要想查找更多的元素，可参考getElements。
```

###通过name属性查找元素
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
element=url.getElementByName(name="")
print(element)
#类型：list
#以上代码是一个示例
#注：同getElementById，只能查找第一个元素。
```

###通过标签查找元素
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
element=url.getElementsByTag(tag="")
print(element)
#类型：list
#以上代码是一个示例
```

###通过class属性查找元素
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
element=url.getElementsById(class_="")
print(element)
#类型：list
#以上代码是一个示例
#注：因为参数名为class会触发异常，因此使用class_参数名。
```

###通过style属性（CSS代码）查找元素
```python
import urlopenlib
url=urlopenlib.urlopen("https://www.baidu.com/")
element=url.getElemenstByStyle(style="")
print(element)
#类型：list
#以上代码是一个示例
```