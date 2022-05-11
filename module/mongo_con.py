from pymongo import MongoClient
API_KEY = '니꺼 넣어'


def conn_mongo_news():
    '''
    news_data 컬렉션에 대한 커넥터 반환 함수
    param:
        - None
    return
        - client.news_data(db)
    '''
    try:
        client = MongoClient(API_KEY)
        db = client.news_data
    except:
        client = MongoClient(API_KEY)
        db = client.news_data
    
    return db