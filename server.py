from RyhBotPythonSDK import Message, Server
import BotConfig
import check_Knapsack
import KnapsackManage
import json

Message.Token = ''
Send = Message.Send()

@Server.Message.BotSettings
def Settings(data):
    gId = data['groupId']
    gName = data['groupName']
    settingJson = data['settingJson']
    settingJson = json.loads(settingJson)
    uId = settingJson['pakavv']['value']
    BotConfig.AddConfig(
        gId, gName, uId
    )

def use(data):
    chatId = data['chat']['chatId']
    chatType = data['chat']['chatType']
    if chatType == 'group':
        senderId = data['sender']['senderId']
        senderNickname = data['sender']['senderNickname']
        useName = data['message']['content']['text']
        things = KnapsackManage.Read(senderId)
        thingList = things.keys()
        if useName in thingList:
            groupId = things[useName]['group']
            if chatId == groupId:
                Configs = BotConfig.Read()
                Owner = Configs[chatId]['uId']
                gName = Configs[chatId]['gName']
                rep = f'''
用户 {senderNickname}({senderId}) 使用了你在 {gName}({chatId}) 中给予的物品 {useName}
请尽快审理
'''
                Send.Markdown(Owner, 'user', rep)
                KnapsackManage.delete(useName, senderId)
                Send.Markdown(chatId, chatType, '已向群主提交审核')

def view(data):
    chatId = data['chat']['chatId']
    chatType = data['chat']['chatType']
    senderId = data['sender']['senderId']
    things = KnapsackManage.Read(senderId)
    rep = '### 账户中没有物品'
    if things != {}:
        rep = ''
        thingList = things.keys()
        for thinName in thingList:
            rep += f'''
- {thinName}
  - {things[thinName]['who']}({things[thinName]['id']}) 在 {things[thinName]['giveTime']} 给予你了这个物品
  - 该物品可在 群({things[thinName]['group']}) 中使用
  - {things[thinName]['time']} 有效期
'''
    Send.Markdown(chatId, chatType, rep)

def give(data):
    chatId = data['chat']['chatId']
    chatType = data['chat']['chatType']
    senderId = data['sender']['senderId']
    senderNickname = data['sender']['senderNickname']
    req_form = {
        'uId':data['message']['content']['formJson']['xfxghv']['value'],
        'thing':data['message']['content']['formJson']['wzzdwt']['value'],
        'time':data['message']['content']['formJson']['chwbjw']['value'],
        'group':chatId
    }
    if senderId != req_form['uId']:
        check_Knapsack.check(req_form['uId'])
        KnapsackManage.add(req_form, senderId, senderNickname)
        Send.Text(
            chatId, chatType, '已加入对方账户'
        )

@Server.Message.Command
def Handle(data):
    commandName = data['message']['commandName']
    if data['sender']['senderUserLevel'] != 'owner':
        check_Knapsack.check(data['sender']['senderId'])
        if commandName == "使用":
            use(data)
        if commandName == "查看":
            view(data)
    if data['sender']['senderUserLevel'] == 'owner':
        if commandName == "给予":
            give(data)

Server.Start(
    'localhost', 5000, True
)