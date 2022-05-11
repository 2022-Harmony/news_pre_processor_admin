
from module import naver_news_cr, summary_module, save_news_data



if __name__ == '__main__':
    ''' 
        3가지 절차를 통해 네이버 스포츠 뉴스 크롤링, 본문 요약, db 적재를 하는 모듈이다.
        1. module.naver_news_cr.get_news(): 뉴스 데이터 크롤링 해오는 메서드 (뉴스 관련된 모든 정보가 들어간 list 반환)
        2. module.summary_module.apply_summary: 뉴스 제목과 본문 정보 보내주면, 요약된 문장을 리턴
        3. module.save_news_data: 크롤링 및 전처리한 데이터 보내면 doc 형태로 묶어 haromony.news_data.news_data에 저장
    '''
    news_data = naver_news_cr.get_news() # 1. 각 뉴스 관련된 모든 정보들을 리스트 형태로 합쳐 반환
        
    for news in news_data: # 각 뉴스에 접근
        if len(news[3]) > 990:       # naver-cloud-summary api의 가용치가 1000글자여서, 이에대한 처리
            news[3] = news[3][0:990]
        news_summary = summary_module.apply_summary(news[0], news[3])   # 2. 제목과 본문 보내면 요약된 문장 리턴
        save_news_data.put_news(news[0], news_summary, news[2], news[4], news[1], news[5])  #3. 전처리한 데이터 전달, haromony.news_data.news_data에 저장
    
    print('process success')
