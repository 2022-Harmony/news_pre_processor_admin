#!/usr/bin/env python3
#-*- codig: utf-8 -*-
import sys
import requests
import json


def apply_summary(title, content):
    '''
        param:
            - title: 기사 제목 정보, 네이버측 클로바 모델에 인풋 값으로 title이 필요해 인자로 받음
            - content: 기사 본문 내용, 네이버 클로바 모델의 인풋 값으로 contnet가 필요해 인자로 받음
        return:
            -  response.text.split(':\"')[1][:-2]: 본문 내용 요약 정보 리턴
    '''
    # api 관련 세팅 #
    client_id = "니거 넣으삼"
    client_secret = "니거 넣으삼"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    language = "ko" # Language of document (ko, ja )
    model = "news" # Model used for summaries (general, news)
    tone = "2" # Converts the tone of the summarized result. (0, 1, 2, 3)
    summaryCount = "5" # This is the number of sentences for the summarized document.
    url= "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"
    data = {   ## 정리 내용 data에 모두 담아줌 line: 45의 requests에 담아 보내줌 ##
        "document": {
        "title": title,
        "content" : content
        },
        "option": {
        "language": language,
        "model": model,
        "tone": tone,
        "summaryCount" : summaryCount
        }
    }
    # print(json.dumps(data, indent=4, sort_keys=True)) # data에 올바르게 data가 적재되었는지 테스트
    
    
    # 위 세팅한 정보를 url 경로(line:29)로 post 요청
    response = requests.post(url, data=json.dumps(data), headers=headers)
    rescode = response.status_code

    # 요약 성공 여부에 따른 분기 처리
    if(rescode == 200): 
        return response.text.split(':\"')[1][:-2].replace('\\n', '  ').replace('\\\"', '') # 성공시 요약 정보 리턴, (깔끔한 데이터를 위해 약간의 전처리)
    else:
        print("Error : " + response.text)