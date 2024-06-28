import datetime
import json

def Read(uId:str) -> dict:
    with open(f'./Knapsack/{uId}.json', 'r', encoding='utf-8') as json_f:
        json_content = json.loads(json_f.read())
    return json_content

def Write(uId:str, content:dict):
    with open(f'./Knapsack/{uId}.json', "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def add(req_form:dict, senderId:str, senderNickname:str):
    Write(
        req_form['uId'], 
        {
            **Read(req_form['uId']), 
            **{
                req_form['thing']:{
                    'who':senderNickname,
                    'id':senderId,
                    'time':req_form['time'],
                    'giveTime':str(datetime.datetime.now()),
                    'group':req_form['group']
                }
            }
        }
    )

def delete(thinName:str, senderId:str):
    things = Read(senderId)
    del things[thinName]
    Write(senderId, things)