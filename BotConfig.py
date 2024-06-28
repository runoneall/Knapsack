import json

def Read() -> dict:
    with open('./Config/BotConfig.json', 'r', encoding='utf-8') as json_f:
        json_content = json.loads(json_f.read())
    return json_content

def Write(content):
    with open("./Config/BotConfig.json", "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def AddConfig(gId:str, gName:str, uId:str):
    ConfigDict = {
        gId: {
            'gName': gName,
            'uId': uId
        }
    }
    Write({**Read(), **ConfigDict})