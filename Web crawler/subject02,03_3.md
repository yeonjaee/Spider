### Youtube 랭킹 데이터 수집과 시각화

##### 유튜브에서 제공하는 채널 랭킹과 상세 정보를 수집하고 시각화하기

채널 랭킹은 http://youtube-rank.com/board/bbs/board.php?bo_table=youtube에서 확인할 수 있다.



#### 유튜브 랭킹 데이터 수집

---

- 

필요한 라이브러리를 가져온다.

```python
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
```



크롬드라이버를 열고, 유튜브 랭킹 웹페이지에 접속한다.

```python
browser = webdriver.Chrome('./chromedriver.exe')
url = "https://youtube-rank.com/board/bbs/board.php?bo_table=youtube" 
browser.get(url)
```

> ![image-20220113220858902](assets/web crwaling_03/image-20220113220858902.png)

url 변수에 주소를 할당하고 **webdriver.Chrome()** 함수로 크롬드라이버를 호출해서 brower 변수에 할당한다. 그리고 **browser.get()** 함수에 url 변수를 전달해 코드를 실행한다.



이번에는 대상 페이지의 HTML 문서를 가져오는 코드를 작성한다.

```python
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
```

browser 변수에는 현재 실행 중인 브라우저의 정보가 담겨 있는데, HTML 문서를 가져오기 위해서는 browser.page_source 라고 저장하면 된다. 이를 html 변수에 할당한다. 마지막으로 <u>**HTML 문서를 해석하고 데이터를 추출**</u>하기 위해 BS 라이브러리를 이용해 **soup** 변수에 할당한다.

---

- 

이제 페이지에서 [검사]를 활용해 채널 정보가 담긴 태그의 위치를 찾아본다.

> ![image-20220113221818617](assets/web crwaling_03/image-20220113221818617.png)

위의 캡쳐 화면에서 볼 수 있듯이 채널 순위는 tr 태그로 구성돼 있음을 알 수 있다.

```python
channel_list = soup.select('form > table > tbody > tr')
print(len(channel_list))
>>>
100
```
100개가 검출된 것을 보니 코드가 제대로 작동했다. 우선 태그 구조를 살펴 보기 위해 tr 태그에 포함된 태그 중 필요한 정보가 어디에 위치하는지 살펴보자.

```python
channel = channel_list[0]
```

> ![image-20220113224247951](assets/web crwaling_03/image-20220113224247951.png)

위 태그들 중 <p class = "category" ~ [음악/댄스/가수] </p> 태그에서 채널의 **카테고리명**이 표시된 것을 확인할 수 있다.  해당 카테고리명을 추출해보자. 카테고리명에는 **앞뒤에 공백(t)**이 포함되어 있으므로 **strip()** 함수로 제거했다.
```python
category = channel.select('p.category')[0].text.strip()
>>>
[음악/댄스/가수]
```

마찬가지로 <a...> BLACKPINK </a> 태그에 **채널명**이 표시된 것을 알 수 있다. 이 또한 추출한다.
```python
title = channel.select('h1 > a')[0].text.strip()
>>>
BLACKPINK
```

이번에는 구독자 수, View 수, 동영상 수를 추출했다.
```python
subscriber = channel.select('td.subscriber_cnt')[0].text
view = channel.select('td.view_cnt')[0].text
video = channel.select('td.video_cnt')[0].text
>>>
7130만
220억1380만
395개
```
---

- 

이제 top 100의 정보를 추출해보자.

```python
channel_list = soup.select('tbody > tr')
for channel in channel_list:
    title = channel.select('h1 > a')[0].text.strip()
    category = channel.select('p.category')[0].text.strip()
	subscriber = channel.select('td.subscriber_cnt')[0].text
	view = channel.select('td.view_cnt')[0].text
	video = channel.select('td.video_cnt')[0].text
    print(title, category, subscriber, view, video)
```

> ![image-20220113225334349](assets/web crwaling_03/image-20220113225334349.png)

현재 페이지에 표시된 100개 채널에 대한 정보를 확인할 수 있다.

---



#### 다른 페이지의 채널 정보 수집

유튜브 랭킹 화면은 한 페이지에 100개의 항목을 보여주고 맨 아래의 페이지 버튼을 클릭하면 원하는 페이지로 이동이 가능하다. 페이지 2의 url은 `https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page=2` 이다. 페이지 1의 url에다가 `&page=2`가 추가 되었다. 페이지가 변경되면 페이지 번호가 추가된다. 이를 이용해 반복문을 사용해 페이지 1~10의 url 주소를 수집하는 코드를 작성한다.

```python
results = []
for page in range(1,11):
    url = f"https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page={page}" 
    browser.get(url)
    time.sleep(2)		# 2초만큼 멈춘다.
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    channel_list = soup.select('form > table > tbody > tr')
	for channel in channel_list:
    	title = channel.select('h1 > a')[0].text.strip()
    	category = channel.select('p.category')[0].text.strip()
		subscriber = channel.select('td.subscriber_cnt')[0].text
		view = channel.select('td.view_cnt')[0].text
		video = channel.select('td.video_cnt')[0].text
        data = [title, category, subscriber, view, video]
        results.append(data)
```
첫 번 째 for 문에서 페이지를 이동할 때 **html = browser.page_source** 을 실행해 각 페이지의 HTML 문서를 가져오고 BS로 태그를 추출한다. 

**time.sleep()** 함수로 현재 실행되는 코를 지정한 인자만큼 멈춘다. 왜냐하면 화면이 정상적으로 로딩된 후 HTML 문서를 가져와야 하기 때문에 각 반복마다 화면을 이동한 후 대기할 시간을 설정한 것이다.

반복문을 통해 페이지별 url을 생성하고 해당 페이지에서 title,category, ... 이 정보를 가져와 data 변수에 할당하고 results에 append 한다.



```python
df = pd.DataFrame(results)
df.columns = ['title', 'category', 'subscriber', 'view', 'video']
df.to_excel('./files/youtube_rank.xlsx', index = False)
```
그리고 results를 데이터 프레임화 시켜 엑셀 파일로 저장했다.



### 유튜브 랭킹 데이터 시각화하기



엑셀 파일을 불러와 카테고리별 구독자 수와 카테고리별 채널 수를 시각화한다.

```python
import pandas as pd
import matplotlib.pyplot as plt
```

먼저 라이브러리를 추가했다.



```python
df = pd.read_excel('./files/youtube_rank.xlsx')
df.head()
```

![image-20220114094714457](assets/web crwaling_03/image-20220114094714457.png)

엑셀 파일을 읽어 와서 **head()** 함수로 데이터를 확인했다.



```python
df.tail()
```

> ![image-20220114094844688](assets/web crwaling_03/image-20220114094844688.png)



```python
df['subscriber'][0:10]
```

> ![image-20220114094928197](assets/web crwaling_03/image-20220114094928197.png)



```python
df['replaced_subscriber'] = df['subscriber'].str.replace('만', '0000')
df.head()
```

> ![image-20220114100302037](assets/web crwaling_03/image-20220114100302037.png)



```python
df.info()
```

> ![image-20220114100355542](assets/web crwaling_03/image-20220114100355542.png)

**replaced_subscriber**의 데이터 타입이 int가 아닌 것을 확인할 수 있다. **astype()**를 이용해 Series 의 데이터 타입을 변환한다.



```python
df['replaced_subscriber'] = df['replaced_subscriber'].astype('int')
df.info()
```

> ![image-20220114100617579](assets/web crwaling_03/image-20220114100617579.png)

int로 변환됐음을 확인했다.



이제는 **카테고리별 채널 수와 구독자 수**를 파이차트로 시각화하기 위해 category 칼럼에서 개별 카테고리의 개수를 세어야 하고 replaced_subscriber 칼럼에서 카테고리별 구독자 수를 모두 더해야 한다.

```python
pivot_df = df.pivot_table(index = 'category', values = 'replaced_subscriber', aggfunc = ['sum','count'])
pivot_df.head()
```

> ![image-20220114100812130](assets/web crwaling_03/image-20220114100812130.png)



```python
pivot_df.columns = ['subscriber_sum', 'category_count']
pivot_df.head()
```

> ![image-20220114101048866](assets/web crwaling_03/image-20220114101048866.png)

알아보기 쉽게 df 의 컬럼명을 변경했다.



```python
pivot_df = pivot_df.reset_index()
pivot_df.head()
```

> ![image-20220114101120091](assets/web crwaling_03/image-20220114101120091.png)

**reset_index()** 로 인덱스를 초기화 했다.



```python
pivot_df = pivot_df.sort_values(by='subscriber_sum', ascending=False)
pivot_df.head()
```

> ![image-20220114102250778](assets/web crwaling_03/image-20220114102250778.png)

**sort_values()** 함수를 이용해 pivot_df 를 정렬했다. 구독자 수 합계를 기준으로 내림차순으로 정렬했다.



```python
plt.figure(figsize = (30,10))
plt.pie(pivot_df['subscriber_sum'], labels=pivot_df['category'], autopct='%1.1f%%', textprops={'color': 'white'})
plt.show()
```

**figsize**로 x,y 축 사이즈를 각각 30,10으로 설정했다. **label**을 추가했고, **autopct** 로 소수점 한자리까지 나오게 표시했다. 개발툴이 다크모드라 글씨가 안보이는데, **textprops={'color':'white'}**로 글자 색을 변경해주었다.
폰트가 깨져 나오는데, 그래프에서 한글을 표기하기 위한 글꼴을 변경하기 위한 코드는 다음과 같다. 

```python
from matplotlib import font_manager, rc
import platform
if platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname = path).get_name()
    rc('font', family = font_name)
elif platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
else:
    print('Check your OS system')
```

>![image-20220114104345016](assets/web crwaling_03/image-20220114104345016.png)



```python
pivot_df = pivot_df.sort_values(by='category_count', ascending=False)
pivot_df.head()
plt.figure(figsize = (30,10))
plt.pie(pivot_df['category_count'], labels=pivot_df['category'], autopct='%1.1f%%')
plt.show()
```

> ![image-20220114104629822](assets/web crwaling_03/image-20220114104629822.png)

카테고리별 채널 수를 시각화했다.

---



### 결론

**<u>유튜브 랭킹 데이터를 크롤링하여 정보를 수집하여 pandas를 이용해 엑셀에 저장하고, 이를 시각화하였다.</u>**
