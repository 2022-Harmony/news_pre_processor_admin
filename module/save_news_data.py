from module.mongo_con import conn_mongo_news

db = conn_mongo_news()


def put_news(title, summary, image_url, news_url, explain, write_time):
    '''
    param:
        - title: 본문 제목                  [FROM naver_news_cr.py]
        - summary: 본문 요약 정보           [FROM summary_module.py]
        - image_url: 기사 이미지 url 주소   [FROM naver_news_cr.py]
        - news_url: 뉴스의 본래 url 주소    [FROM naver_news_cr.py]
        - explain: 뉴스에 대한 간략한 소개   [FROM naver_news_cr.py]
        - write_time: 작성 시간             [FROM naver_news_cr.py]
    return:
        - db 적재 성공 여부 [True || False]
    '''
    
    post_count = db.news_data.estimated_document_count()    # news_data 문서 개수 가져와 count로 사용
    if post_count == 0:                                     # 컬렉션에 문서가 있을 때와 없을 때 분기 처리
        max_value = 1
    else:
        max_value = db.news_data.find_one(sort=[("post_id", -1)])['post_id'] + 1  # 가장 큰 post_id에서 하나를 더 해줌
    
    doc = {
        'post_id': max_value,
        'title': title,
        'summary': summary,
        'image_url': image_url,
        'news_url': news_url,
        'explain': explain,
        'write_time': write_time
    }
    
    try: #DB 삽입 성공 여부에 따른 분기 반환 [True || False]
        db.news_data.insert_one(doc)
        return True
    except:
        return False