from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

def get_page_html(url, time=0):
    '''
    param: 
    '''
    # 옵션 생성
    options = webdriver.ChromeOptions()
    options.add_argument("headless") # 창 숨기는 옵션 추가
    driver = webdriver.Chrome('./chromedriver', options = options)  # 드라이버를 실행합니다.
    driver.get(url)
    sleep(time)  # 요청받은 시간 만큼 대기
    
    req = driver.page_source  # html 정보를 가져옵니다.
    driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

    return req

def get_news():
    '''
    네이버 뉴스에서 제목과 내용 가져와서, app.py의 news_get라우터 함수에 리턴
    :param: None
    :return:
        - title: 기사 제목
        - img_src: 기사 이미지 주소
        - detail_sentence: 기사 외부 설명 글
        - detail_uri: 기사 url
        - sentence: 기사 본문 전체 내용
        - detail_time: 기사 작성 시간
    '''
    
    
    ## 크롤링 세팅 ##
    req = get_page_html('https://sports.news.naver.com/ranking/index', 2)
    soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.
    news = soup.select('#_newsList > ul > li')
    news_box = []
    error_image = 'https://user-images.githubusercontent.com/68278903/167756503-6c7fd836-65e3-42f5-a4a2-289bc7472e94.jpg'

    ## 크롤링 작업 ##
    for target in news:
        # target 요소 찾기 #
        title = target.select_one('div.text > a').text
        sentence = target.select_one('div.text > p').text
        # img_src = target.select_one('a > img').attrs['src']
        detail_uri = target.select_one('div.text > a').attrs['href']
        
            # 각 뉴스 세부 내용 크롤링: 위에서 수집한 detail_uri 타고 2중 스크래핑 #
        req = get_page_html(f'https://sports.news.naver.com/{detail_uri}', 2)
        detail_soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.
        detail_time = detail_soup.select_one('#content > div > div.content > div > div.news_headline > div > span:nth-child(1)').text
        detail_sentence = detail_soup.select_one('#newsEndContents').text.split('기사제공')[0].replace('\n', '').replace('\t', '')

        try:
            img_src = detail_soup.select_one('#newsEndContents > span:nth-child(1) > img')['src']
        except:
            img_src = detail_soup.select_one('#newsEndContents > span:nth-child(1) > img')['src']
            
        if img_src == None:
            print(f'cant scrapy img: https://sports.news.naver.com/{detail_uri}')
            img_src = error_image
        # print(img_src)
        news_box.append([title, sentence, img_src, detail_sentence, f'https://sports.news.naver.com/{detail_uri}', detail_time.split('기사입력 ')[1]])
        img_src = None

    return news_box