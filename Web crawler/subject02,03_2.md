### 여러 음원 서비스의 순위 수집/정리하기

---

- 앞서 멜론 HOT 100을 크롤링했던 코드를 **xlsx 파일**로 저장하고자 한다.

```python
# 예제 3-1 멜론 사이트 접속하기 
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('./chromedriver.exe')
url = 'http://www.melon.com/chart/index.htm'
driver.get(url)     

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
```
> ![image-20220113094508152](assets/web crawling_02/image-20220113094508152.png)



- 이제 반복문을 이용해 곡과 가수명을 song_data 리스트에 저장해보자.

```python
song_data = []
rank = 1		# 순위

songs = soup.select('table > tbody > tr')
for song in songs:                                        
    title = song.select('div.rank01 > span > a')[0].text
    singer = song.select('div.rank02 > a')[0].text
    song_data.append(['Melon', rank, title, singer])
    rank = rank + 1
```


- for 문을 통해 데이터를 순서대로 **song**에 할당한다. 각 곡에서 추출한 정보를 **['Melon', rank, title, singer]**형식으로 **song_data**에 할당한다. 이렇게 저장되는 데이터를 엑셀로 저장하기 위해 데이터 프레임을 만들어 보자.

```python
import pandas as pd
columns = ['사이트', '순위', '타이틀', '가수']
pd_data = pd.DataFrame(song_data, columns = columns)
pd_data.head()
```
> ![image-20220113095055429](assets/web crawling_02/image-20220113095055429.png)

```python
pd_data.to_excel('./files/melon.xlsx', index=False)
```
이렇게 해서 정보를 수집하고 엑셀 파일로 저장했다.



#### 벅스 크롤링

- 이번에는 벅스 사이트의 정보를 크롤링해보자. 먼저 벅스 웹 사이트에 접속한다.

```python
# 예제 3-5 벅스 사이트 접속하기 
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('./chromedriver.exe')
url  = 'https://music.bugs.co.kr/chart'
driver.get(url)     

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
```
> ![image-20220113101714068](assets/web crawling_02/image-20220113101714068.png)



- 마찬가지로 곡 정보가 저장된 html을 찾아보자

![image-20220113101900396](assets/web crawling_02/image-20220113101900396.png)

이 부분인것 같다.

```python
songs = soup.select('table.list.trackList.byChart > tbody > tr')
print(len(songs))
>>>100
```
table 명을 입력할 때 `table.byChart`같이 간략화 시켜도 일단은 작동한다. 그래도 풀네임으로 쓰는 것이 좋을 것 같다. **1위 곡의 정보**를 살펴보자.

```python
print(songs[0])
```
```tex
<tr albumid="20444436" artistid="80347259" multiartist="N" mvid="605415" rowtype="track" trackid="32438762">
<input name="_isStream" type="hidden" value="32438762"/>
<input name="_isDown" type="hidden" value="32438762"/>
<td class="check"><input buyminquality="T" disc_id="1" name="check" title="Blessed-Cursed" type="checkbox" value="32438762"/></td>
<td>
<div class="ranking">
<strong>1</strong>
<p class="change none"><em>0</em><span>변동없음</span></p>
</div>
</td>
<td>
<a class="thumbnail" href="https://music.bugs.co.kr/album/20444436?wl_ref=list_tr_07_chart" onclick="
">
<span class="mask"></span>
<img alt="DIMENSION : ANSWER 대표이미지" onerror="bugs.utils.imgError(this);" src="https://image.bugsm.co.kr/album/images/50/204444/20444436.jpg?version=20220111004230.0"/>
</a>
</td>
<td>
<a class="trackInfo" href="https://music.bugs.co.kr/track/32438762?wl_ref=list_tr_08_chart" onclick="
">곡정보</a>
</td>
<th scope="row">
<p adult_yn="N" class="title">
<a adultcheckval="1" aria-label="새창" href="javascript:;" onclick="bugs.wiselog.area('list_tr_09_chart');bugs.music.listen('32438762',true);
" title="Blessed-Cursed">Blessed-Cursed</a>
<a artist_disp_nm="ENHYPEN" artist_id="80347259" class="btnActions" href="javascript:;" layer_type="CHART" layerpositiontarget="td" onclick="bugs.wiselog.area('list_tr_17_chart');
bugs.layermenu.trackMoreAction(this,'32438762','0','20444436','bugs.music.listenRadioFromSeed(\'32438762\',\'track\');','N', 'Y', '_chart');
" track_title="Blessed-Cursed">기타 기능</a>
</td>
</tr>
```

>  ![image-20220113102757080](assets/web crawling_02/image-20220113102757080.png)

**title**은 *p 클래스 title 안의 a href*에 저장되어 있고, **artis**t는 *p 클래스 artist 안의 a href*에 저장되어 있다.

- 이를 코드로 작성하고 결과를 출력해보자.

```python
title = soup.select('p.title > a')[0].text
artist = soup.select('p.artist > a')[0].text
>>>
Blessed-Cursed
'ENHYPEN'
```


- 이제 100위 모든 노래의 순위 정보를 가져오자

```python
songs = soup.select('table.list.trackList.byChart > tbody > tr')
for song in songs:
    title = song.select('p.title > a')[0].text
	artist = song.select('p.artist > a')[0].text
    print(title, artist, sep = ' by ')
```
> ![image-20220113103728674](assets/web crawling_02/image-20220113103728674.png)

실행 결과를 보면 제대로 추출됐는지 알 수 있다.

- 이제 이 결과를 엑셀에 저장해보자.

```python
song_data = []
rank = 1
songs = soup.select('table.byChart > tbody > tr')
for song in songs:
    title = song.select('p.title > a')[0].text
    singer = song.select('p.artist > a')[0].text
    song_data.append(['Bugs', rank, title, singer])
    rank = rank + 1

columns = ['사이트', '순위', '타이틀', '가수']
pd_data = pd.DataFrame(song_data, columns = columns)
pd_data.to_excel('./files/bugs.xlsx', index=False)
```


#### 지니 크롤링

지니 사이트도 마찬가지로 정보를 크롤링하여 엑셀 파일로 저장하였다.

```python
from selenium import webdriver 
from bs4 import BeautifulSoup 
import pandas as pd

driver = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.genie.co.kr/chart/top200'
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

song_data = []
rank = 1
songs = soup.select('tbody > tr') 
for song in songs:
    title = song.select('a.title')[0].text
    singer = song.select('a.artist')[0].text 
    song_data.append(['Genie', rank, title, singer]) 
    rank = rank + 1

columns = ['사이트', '순위', '타이틀', '가수']
pd_data = pd.DataFrame(song_data, columns = columns) 
pd_data.to_excel('./files/genie.xlsx', index=False)
```


#### 멜론, 벅스, 지니 크롤링 엑셀 파일 통합하기

이제 모든 사이트의 인기 차트 곡 정보를 수집했고, 각 엑셀 파일에 저장했다. 이 엑셀 파일들을 하나로 합쳐보자.

```python
import pandas as pd
excel_names = ['./files/melon.xlsx','./files/bugs.xlsx','./files/genie.xlsx']
appended_data = pd.DataFrame()
for name in excel_names:
    pd_data = pd.read_excel(name)
    appended_data = appended_data.append(pd_data)
```
**pandas**를 불러오고, 지금까지 멜론,벅스,지니의 크롤링 결과가 담긴 엑셀 파일의 이름을 **excel_names**에 차례대로 입력한다. 그런 다음 **pd.DataFrame()**을 실행해 빈 데이터 프레임을 만들어 **appended_data**에 넣는다. 다음으로 반복문을 통해 엑셀 파일을 대상으로 순서대로 **read_excel** 함수를 실행해 내용을 읽고 appended_data 변수에 추가한다.



크롤링 결과 확인

```python
<class 'pandas.core.frame.DataFrame'>
Int64Index: 250 entries, 0 to 49
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   사이트     250 non-null    object
 1   순위      250 non-null    int64 
 2   타이틀     250 non-null    object
 3   가수      250 non-null    object
dtypes: int64(1), object(4)
memory usage: 11.7+ KB
```
250개의 정보가 들어가 있으니 제대로 작동한 것을 확인할 수 있다. 이를 엑셀 파일로 저장한다.

```python
appended_data.to_excel('./files/total.xlsx', index=False)
```
