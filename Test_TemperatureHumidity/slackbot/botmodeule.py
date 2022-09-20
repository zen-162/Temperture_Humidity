from slackbot.bot import respond_to
from slackbot.bot import listen_to

# 「respond_to」はメンションする(@でダーゲットを指定すること)と応答する
@respond_to('こんにちは')
def greeting_1(message):
    # Slackに応答を返す
    message.reply('こんにちは！')

# 「listen_to」はメンションがなくても応答する
@listen_to('コンニチハ')
def greeting_2(message):
    message.reply('コンニチハ')
