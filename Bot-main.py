from aiocqhttp import CQHttp, Event
import random
from pprint import pprint
bot = CQHttp()  # M1

global mag, rem
mag = [1, 2, 3, 4, 5, 6]
rem = 5


@bot.on_message('private', 'group')  # M2
async def _(event: Event):  # M3
    global rem, mag
    msg = event['message']
    if msg.startswith('.'):
        tmsg = event['message'][1:]
        await bot.send(event, '你发了：' + tmsg)  # M4
    elif msg == '俄罗斯轮盘赌':
        bul = random.randint(0, rem)
        rem = int(rem) - 1
        re = mag[int(bul)]
        if rem == -1:
            await bot.send(event, "你已知道，这是必死之局。")
            # ban = random.randint(60, 300)
            # await bot.set_group_ban(int(ban))
            # await bot.send(event, "砰，你死了。距离下次复活还有：" + str(int(ban)) + "分")
            await bot.send(event, "砰，你死了。")
            await bot.send(event, "已重新装填子弹。")
            mag = [1, 2, 3, 4, 5, 6]
            rem = 5
        elif re == 6:
            # ban = random.randint(60, 300)
            # await bot.set_group_ban(int(ban))
            # await bot.send(event, "砰，你死了。距离下次复活还有：" + str(int(ban)) + "分")
            await bot.send(event, "砰，你死了。")
            await bot.send(event, "已重新装填子弹。")
            mag = [1, 2, 3, 4, 5, 6]
            rem = 5
        elif re != 6:
            del mag[int(bul)]
            await bot.send(event, "“咔嚓”")
            await bot.send(event, "哈，是空的。")
            await bot.send(event, "侥幸逃过一劫呢，哼。剩余弹仓：" + str(len(mag)))
    elif msg == '/占卜':
        await bot.send(event, "占你妈个头，滚！")


#暂时这样！
bot.run(host='127.0.0.1', port=8080)  # M6
