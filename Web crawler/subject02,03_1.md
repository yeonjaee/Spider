## 웹 크롤링 기초

**웹 크롤링은 웹 페이지에 있는 정보를 가지고 오는 것**을 의미한다. 참고로 특정 웹페이지에서 짧은 시간동안 과도한 데이터를 수집하는 행위는 해당 서버에 무리를 주거나, 공격으로 인식될 가능성이 있으므로 주의를 요한다.

이 내용에선 **selenium** 라이브러리의 webdriver를 활용해 웹 브라우저를 조작하고, BeautifulSoup 라이브러리를 활용해 웹 페이지 상의 HTML 데이터에서 필요한 정보를 가져오는 방법을 사용한다.



**1.1 selenium과 웹 브라우저 설치**

selenium의 webdriver는 크롬이나 인터넷 익스플로러 등에서 사이트 접속, 버튼 클릭, 글자 입력과 같이 웹 브라우저에서 사람이 할 수 있는 일들을 코드를 통해 제어할 수 있는 라이브러리다.

**`! pip install selenium`**으로 설치 후 **`from selenium import webdriver`**로 불러온다.

```python
from selenium import webdriver
webdriver.__version__
# 버전 확인
```

브라우저는 크롬 드라이버가 설치된 크롬이 적절하므로 크롬을 다운로드 해준다. 크롬 드라이버는 selenium를 통해 파이썬에서 브라우저를 제어할 수 있게 해준다. 다만 크롬이 설치되어 있다 하더라도, 크롬드라이버는 별도의 파일이 필요하니 다운로드해야한다. [크롬 드라이버 다운](https://chromedriver.chromium.org/home) 을 클릭하여 현재 버전이 96이므로 96 버젼 크롬 드라이버를 다운 받고,  파일이 위치한 경로를 기억한다.

---

**1.2 크롬 드라이버 활용하기**

크롬 드라이버 실행

```python
from selenium import webdriver
driver = webdriver.Chrome('./chromedriver.exe')
```

>  <img src="assets/web crawling/image-20220112141616677.png" alt="image-20220112141616677" style="zoom:25%;" /> 
>
> 위 코드를 실행하면 selenium을 정상적으로 불러오고 크롬드라이버의 경로가 올바르게 입력된 경우 크롬 브라우저가 열린다.

---

**1.3 웹 페이지 접속**

**driver.get(URL)** 명령을 통해 특정 웹 페이지에 접속할 수 있다.

```python
url = 'https://www.naver.com/'
driver.get(url)
```

---

**1.4 웹 페이지(HTML) 다운로드**

selenium을 이용하면 웹 브라우저에 표시되는 웹 페이지 정보를 다운로드할 수 있다. 크롬 같은 브라우저는 웹 페이지에 접속하면 HTML 정보를 가져와 읽고 해석해서 화면에 표현하는 역할을 한다. 이를 위해 먼저 웹 페이지의 HTML을 다운로드하는 것이 필요하다. **driver.page_source** 명령을 통해 웹 페이지의 HTML 정보를 가져올 수 있다.

```python
html = driver.page_source
```

---

**1.5 HTML의 기본 구조와 기본 태그**

https://wikidocs.net/85437 해당 링크의 설명을 참고하자

---

**1.6 크롬 브라우저에서 웹 페이지의 HTML 살펴보기**

[설정] -[도구 더보기]-[개발자 도구]를 클릭하면 해당 웹 페이지의 정보를 볼 수 있다. 마찬가지로 웹 페이지의 해당 영역을 우클릭 후 [검사]를 클릭하면 정보를 볼 수 있다.

---

**1.7 BeautifulSoup을 이용한 정보 찾기**

하지만 실제 웹 페이지는 HTML의 규모가 비교적 크기 때문에 간단한 웹 페이지의 HTML로 필요한 정보를 찾는 방법이 필요하다. 웹 브라우저에서 특정 사이트에 접속한 뒤 `driver.page_source`를 이용해 내려받은 HTML은 여러 문자들이 연결된 문자열 데이터이므로, 이를 읽고 정보를 쉽게 찾을 수 있도록 **BeautifulSoup** 라이브러리를 활용한다.

**`! pip install bs4`** 먼저 라이브러리 bs4를 설치하고, **`from bs4 import BeautifulSoup`** 로 불러온다.

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
```

`BeautifulSoup(html, 'html.parser')` 명령을 통해 **html 변수에 들어 있는 문자열 정보를 HTML 형식에 맞게 해석해서 원하는 정보를 찾을 수 있도록 준비**한다.

```
예제 실습용 HTML

<html>
    <head>
    </head>
    <body>
        <h1> 우리동네시장</h1>
            <div class = 'sale'>
                <p id='fruits1' class='fruits'>
                    <span class = 'name'> 바나나 </span>
                    <span class = 'price'> 3000원 </span>
                    <span class = 'inventory'> 500개 </span>
                    <span class = 'store'> 가나다상회 </span>
                    <a href = 'http://bit.ly/forPlaywithData' > 홈페이지 </a>
                </p>
            </div>
            <div class = 'prepare'>
                <p id='fruits2' class='fruits'>
                    <span class ='name'> 파인애플 </span>
                </p>
            </div>
    </body>
</html>
```



- 1.7.1 정보 찾기 - **태그 속성 활용**

  BeautifulSoup 명령어인 **select('조건')**을 이용하면 HTML 내에서 입력한 조건을 만족하는 태그를 모두 선택할 수 있다. 조건 부분에 태그명이나 속성값을 지정하거나 태그 간의 구조를 지정할 수도 있고, 두 방법을 모두 활용할 수도 있다.

  ```python
  tags_span = soup.select('span')
  ```

  태그명 외에도 태그의 속성 중 **id 값**이나 **class 명**을 이용해 태그를 찾을 수 있다. select('조건')에 **샵(#) 기호 뒤에 id 값**을 넣거나 **점(.)뒤에 class 명**을 넣는 방식으로 사용한다.

  ```python
  ids_fruits1 = soup.select('#fruits1')
  class_price = soup.select('.price')
  tags_span_class_price = soup.select('span.price') # 태그명이 span이면서 클래스가 price 인 태그
  ```

  **id 값**은 특정 대상을 지정하기 위해 사용되므로 HTML 내에서 한 번만 사용 가능하다. 따라서 **id 값**을 잘 활용한다면 특정 태그를 쉽게 찾을 수 있다.



- 1.7.2 정보 찾기 - **상위 구조 활용**

  태그의 속성만으로 찾기가 어려울 경우 어떠한 부모 태그 아래에 있는지를 알아내 찾아낼 수 있다. 한 단계 아래를 의미할 때는 **'>'** 기호를 사용하고, 여러 단계(한 단계도 포함) 아래를 의미할 때는 **띄어쓰기(' ')**를 사용한다.

  ```python
  tags_name = soup.select('span.name')
  print(tags_name)
  >>>
  [<span class="name"> 바나나 </span>, <span class="name"> 파인애플 </span>]
  ```

  태그명이 'span' 이면서 class 명이 'name' 인 태그를 모두 찾아서 tags_name 변수에 저장하였다. 여기서 바나나를 찾기위해 바나나가 속한 부모 태그 정보를 추가해본다.

  ```python
  tags_banana1 = soup.select('#fruits1 > span.name')
  print(tags_banana1)
  >>>
  [<span class="name"> 바나나 </span>]
  ```

  부모 태그 정보를 추가함으로써 바나나만 출력되는 것을 확인할 수 있다. 아래의 코드도 같은 값을 출력한다.

  ```python
  tags_banana2 = soup.select('div.sale > #fruits1 > span.name')
  tags_banana3 = soup.select('div.sale span.name')
  print(tags_banana2)
  print(tags_banana3)
  >>>
  [<span class="name"> 바나나 </span>]
  [<span class="name"> 바나나 </span>]
  ```



- 1.7.3 정보 찾기 - **선택한 태그에서 정보 가져오기**

  인덱스 번호나 반복문을 활용해 원하는 태그를 선택한 다음에 화면에 보이는 글 부분을 가져오거나**(.text)** 태그 내 속성의 값을 가져올 수 있다(**['속성명']**). 일반적으로 브라우저에 표시되는 정보를 수집하는 일이 많기에 .text 명령을 자주 활용하지만, 화면에 보이지 않는 URL 주소를 수집하기 위해서는 **['href']** 명령도 필요하다. (하이퍼링크는 모두 <a href='URL 주소')형식으로 작성돼 있다.

  ```python
  content = tag.text   # 태그에서 화면에 보이는 텍스트 부분만 가져오기
  attribute = tag['속성명']  # 태그 내 속성값 가져오기
  ```

  ```python
  tags = soup.select('a')		# 태그명이 a인 태그를 모두 선택
  tag = tags[0]				# 인덱스 번호 0번인 원소를 선택하여 변수에 저장
  content = tag.text
  print(content)
  >>>
  '''홈페이지'''
  
  link = tag['href']			# 태그에서 href 속성에 저장된 값을 변수에 저장
  print(link)
  >>>
  '''http://bit.ly/forPlaywithData'''
  ```

---

**1.8 멜론 노래 순위 정보 크롤링**

```python
## 크롬드라이버 실행
from selenium import webdriver
driver = webdriver.Chrome('./chromedriver.exe')
```

```python
## 멜론 인기차트 웹페이지 접속
url = 'http://www.melon.com/chart/index.htm'
driver.get(url)
```

```python
# HTML 다운로드 및 BeautifulSoup으로 읽기
from bs4 import BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
```

- 이제 **soup** 변수의 HTML 속에서 노래 정보를 포함하는 태그를 찾아본다. 앞서 설명한 것처럼 크롬 브라우저의 **[개발자 도구]**를 활용한다. 노래 한 곡의 정보를 가지는 태그를 찾아보자.

> ![제목 없음](assets/web crawling/제목 없음.png)

table 태그 밑의 tbody의 밑의 tr 태그 하나에 노래 한 곡의 정보가 담긴 것으로 추측할 수 있다. 더 자세히 알아보자

```python
songs = soup.select('table > tbody > tr')  
print(len(songs))
print(songs[0])
```

```tex
>>>
100
<tr class="lst50" data-song-no="34061322" id="lst50">
<td><div class="wrap t_right"><input class="input_check" name="input_check" title="사랑은 늘 도망가 곡 선택" type="checkbox" value="34061322"/></div></td>
<td><div class="wrap t_center"><span class="rank">1</span><span class="none">위</span></div></td>
<!-- 차트순위 추가 -->
<td><div class="wrap">
<span class="rank_wrap" title="순위 동일">
<span class="bullet_icons rank_static"><span class="none">순위 동일</span></span>
<span class="none">0</span>
</span>
</div></td>
<td><div class="wrap">
<a class="image_typeAll" href="javascript:melon.link.goAlbumDetail('10735654');" title="신사와 아가씨 OST Part.2">
<img alt="신사와 아가씨 OST Part.2 - 페이지 이동" height="60" onerror="WEBPOCIMG.defaultAlbumImg(this);" src="https://cdnimg.melon.co.kr/cm2/album/images/107/35/654/10735654_20211008114339_500.jpg/melon/resize/120/quality/80/optimize" width="60"/>
<span class="bg_album_frame"></span>
</a>
</div></td>
<td><div class="wrap">
<a class="btn button_icons type03 song_info" href="javascript:melon.link.goSongDetail('34061322');" title="사랑은 늘 도망가 곡정보"><span class="none">곡정보</span></a>
</div></td>
<td><div class="wrap">
<div class="wrap_song_info">
<div class="ellipsis rank01"><span>
<a href="javascript:melon.play.playSong('1000002721',34061322);" title="사랑은 늘 도망가 재생">사랑은 늘 도망가</a>
</span></div><br/>
<div class="ellipsis rank02">
<a href="javascript:melon.link.goArtistDetail('994944');" title="임영웅 - 페이지 이동">임영웅</a><span class="checkEllipsis" style="display: none;"><a href="javascript:melon.link.goArtistDetail('994944');" title="임영웅 - 페이지 이동">임영웅</a></span>
</div>
</div>
</div></td>
<td><div class="wrap">
<div class="wrap_song_info">
<div class="ellipsis rank03">
<a href="javascript:melon.link.goAlbumDetail('10735654');" title="신사와 아가씨 OST Part.2 - 페이지 이동">신사와 아가씨 OST Part.2</a>
</div>
</div>
</div></td>
<td><div class="wrap">
<button class="button_etc like" data-song-menuid="1000002721" data-song-no="34061322" title="사랑은 늘 도망가 좋아요" type="button"><span class="odd_span">좋아요</span>
<span class="cnt">
<span class="none">총건수</span>
108,815</span></button>
</div></td>
<td><div class="wrap t_center">
<button class="button_icons play" onclick="melon.play.playSong('1000002721',34061322);" title="듣기" type="button"><span class="none">듣기</span></button>
</div></td>
<td><div class="wrap t_center">
<button class="button_icons scrap" onclick="melon.play.addPlayList('34061322');" title="담기" type="button"><span class="none">담기</span></button>
</div></td>
<td><div class="wrap t_center">
<button class="button_icons download" onclick="melon.buy.goBuyProduct('frm', '34061322', '3C0001', '','0', '1000002721');" title="다운로드" type="button"><span class="none">다운로드</span></button>
</div></td>
<td><div class="wrap t_center">
<button class="button_icons video" onclick="melon.link.goMvDetail('1000002721', '34061322','song');" title="뮤직비디오" type="button"><span class="none">뮤직비디오</span></button>
</div></td>
</tr>
## 위 html 정보가 한 개의 곡에 대한 모든 정보다. 이런게 100개 있는 것이다.
..... 중략
```

**`songs = soup.select('table > tbody > tr')  `**을 통해 곡 정보가 포함된 tr 태그를 모두 찾았다. 그리고

**`len()`**을 이용해 해당 원소가 몇 개인지 알아냈다. 100 이라는 출력 값은 1위부터 100위까지의 곡 수와 일치한다.



- 1위곡을 지정해보자

```python
song_1st = songs[0]
```

- 1위곡의 제목을 찾아보자.

1위 곡의 태그를 **song_1st** 변수로 지정했다.

> ![image-20220112165037340](assets/web crawling/image-20220112165037340.png)

**곡 제목**은 태그명이 **a** 이면서 **href**와 **title**을 속성으로 가지는 태그에 정보가 들어있다. 해당 태그를 선택해본다.

```python
title = song_1st.select('div.ellipsis.rank01 > span > a')
```

- **해당 태그에서 `(.text)` 를 사용하여 텍스트 부분만 출력해보자.**

```python
title = song_1st.select('div.ellipsis.rank01 > span > a')[0].text
### "ellipsis rank01" 중간의 띄어쓰기는 `.`으로 대체한다.

print(title)
>>>
사랑은 늘 도망가
```

.select()의 경우 조건에  해당하는 데이터를 모두 선택하기 때문에 **인덱스 번호[0]**을 활용해 조건에 해당하는 태그 중 첫 번째 태그를 선택했고, **.text**를 통해 해당 태그의 텍스트 부분을 선택했다.

- 1위곡의 가수를 찾아보자.

  >![image-20220112165404490](assets/web crawling/image-20220112165404490.png)

```python
singer = song_1st.select('div.ellipsis.rank02 > a')[0].text
print(singer)
>>>
임영웅
```

위와 같이 가수 이름이 출력되는 것을 확인할 수 있다.



- 이번에는 **100곡의 노래**에서 노래 제목과 가수 정보를 추출해보자.

```python
for song in songs:                                        
    title = song.select('div.ellipsis.rank01 > span > a')[0].text
    singer = song.select ('div.ellipsis.rank02 > a')[0].text
    print(title, singer, sep = ' .by ')
```

```tex
사랑은 늘 도망가 .by 임영웅
취중고백 .by 김민석 (멜로망스)
회전목마 (Feat. Zion.T, 원슈타인) (Prod. Slom) .by sokodomo
Counting Stars (Feat. Beenzino) .by BE'O (비오)
ELEVEN .by IVE (아이브)
리무진 (Feat. MINO) (Prod. GRAY) .by BE'O (비오)
겨울잠 .by 아이유
Dreams Come True .by aespa
눈이 오잖아(Feat.헤이즈) .by 이무진
만남은 쉽고 이별은 어려워 (Feat. Leellamarz) (Prod. TOIL) .by 베이식 (Basick)
다정히 내 이름을 부르면 .by 경서예지
strawberry moon .by 아이유
Step Back .by GOT the beat
신호등 .by 이무진
Savage .by aespa
드라마 .by 아이유
STAY .by The Kid LAROI
이제 나만 믿어요 .by 임영웅
Next Level .by aespa
불협화음 (Feat. AKMU) (Prod. GRAY) .by Mudd the student
Christmas Tree .by V
흰눈 .by 먼데이 키즈 (Monday Kiz)
우리가 헤어져야 했던 이유 .by 비비 (BIBI)
그대라는 사치 .by 임영웅
쉬어 (Feat. MINO) (Prod. GRAY) .by 아넌딜라이트(Anandelight)
네가 없는 밤 (Feat. ASH ISLAND) (Prod. GRAY) .by BE'O (비오)
다시 사랑한다면 (김필 Ver.) .by 임영웅
너를 생각해 .by 주시크 (Joosiq)
별빛 같은 나의 사랑아 .by 임영웅
Butter .by 방탄소년단
OHAYO MY NIGHT .by 디핵 (D-Hack)
Wake Up (Prod. 코드 쿤스트) .by 개코
잊었니 .by 임영웅
언덕나무 .by 이승윤
서랍 .by 10CM
HERO .by 임영웅
Permission to Dance .by 방탄소년단
문득 .by BE'O (비오)
바라만 본다 .by MSG워너비(M.O.M)
끝사랑 .by 임영웅
이별후회 .by 김나영
My Universe .by Coldplay
낙하 (with 아이유) .by AKMU (악뮤)
Dynamite .by 방탄소년단
Bk Love .by 임영웅
Celebrity .by 아이유
정거장 .by 아이유
Weekend .by 태연 (TAEYEON)
그게 더 편할 것 같아 (N번째 연애 X 멜로망스) .by 멜로망스
헤픈 우연 .by 헤이즈 (Heize)
라일락 .by 아이유
Bad Habits .by Ed Sheeran
밤하늘의 별을(2020) .by 경서
Still I Love You .by 토요태
고백 .by 멜로망스
안녕 우린 헤어져야만 해 .by 전상근
찰나가 영원이 될 때 (The Eternal Moment) .by 마크툽 (MAKTUB)
어떻게 이별까지 사랑하겠어, 널 사랑하는 거지 .by AKMU (악뮤)
사랑이 아니었다고 말하지 마요 .by 이예준
러브레터 .by 아이유
사이렌 Remix (Feat. UNEDUCATED KID, Paul Blanco) .by 호미들
모든 날, 모든 순간 (Every day, Every Moment) .by 폴킴
롤린 (Rollin') .by 브레이브걸스
추억은 만남보다 이별에 남아 .by 정동하
내 손을 잡아 .by 아이유
Off My Face .by Justin Bieber
Dun Dun Dance .by 오마이걸 (OH MY GIRL)
밝게 빛나는 별이 되어 비춰줄게 .by 송이한
시간을 거슬러 (낮에 뜨는 달 X 케이윌) .by 케이윌
Blueming .by 아이유
오늘도 빛나는 너에게 (To You My Light) (Feat.이라온) .by 마크툽 (MAKTUB)
MBTI (Feat. 쿠기 & 로꼬) (Prod. GRAY) .by BE'O (비오)
계단말고 엘리베이터 .by 임영웅
비가 오는 날엔 (2021) .by 헤이즈 (Heize)
봄날 .by 방탄소년단
작은 것들을 위한 시 (Boy With Luv) (Feat. Halsey) .by 방탄소년단
너 .by 아이유
좋아좋아 .by 조정석
Queendom .by Red Velvet (레드벨벳)
그날에 나는 맘이 편했을까 .by 이예준
Savage Love (Laxed - Siren Beat) (BTS Remix) .by Jawsh 685
취기를 빌려 (취향저격 그녀 X 산들) .by 산들
DUMB DUMB .by 전소미
여름비 .by 샘김 (Sam Kim)
Snowman .by Sia
멜로디 .by ASH ISLAND
너의 모든 순간 .by 성시경
나 그댈위해 시 한편을 쓰겠어 .by 케이시 (Kassy)
Life Goes On .by 방탄소년단
비와 당신 .by 이무진
탕!♡ .by MINO (송민호)
ASAP .by STAYC(스테이씨)
매일 크리스마스 (Everyday Christmas) .by 다비치
호우주의 (Feat. 개코, 넉살 (Nucksal)) (Prod. 코드 쿤스트) .by 조광일
아직도 좋아해 .by 양요섭
죽을 만큼 아파서 (Feat. JAMIE (제이미)) .by MC몽
깐부 (Feat. 염따, ASH ISLAND) (Prod. TOIL) .by 쿤타
Peaches (Feat. Daniel Caesar & Giveon) .by Justin Bieber
밤새 서로 미루다 .by 존박
Santa Tell Me .by Ariana Grande
```

반복문을 통해 songs에 들어있는 모든 곡의 제목과 가수 정보를 추출했으며 분리자를 넣어주었다.

---



**1.9 selenium을 활용한 크롤링**

앞서 공부한 내용은 **BeautifulSoap**를 활용한 정보 수집 방식이었다. 사실 selenium은 BS를 활용하지 않고도 필요한 정보를 찾아오는 명령어가 존재한다. 바로 **`driver.find_elements_by_css_selector('조건')`**으로 원하는 조건에 해당하는 태그를 모두 찾을 수 있으며, 여기서 조건에는 **BS의 select**와 동일하게 태그명, 클래스명, id 값, 부모 태그 등의 구조 정보를 지정할 수 있다. 참고로 이러한 태그의 구조 정보를 CSS Selector 라고 한다.

```python
driver = webdriver.Chrome('../chromedriver.exe') 
url = 'http://www.melon.com/chart/index.htm'
driver.get(url)          
                                
songs = driver.find_elements_by_css_selector('table>tbody>tr')
for song in songs:                                        
    title = song.find_elements_by_css_selector('div.ellipsis.rank01 > span > a')[0].text
    singer = song.find_elements_by_css_selector('div.ellipsis.rank02 > a')[0].text  
    print(title, singer, sep = ' .by ')
```

