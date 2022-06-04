from aiocqhttp import CQHttp, Event
import random
from pprint import pprint

bot = CQHttp()  # M1

global mag, rem
mag = [1, 2, 3, 4, 5, 6]
rem = 5


async def _contrast(event: Event):    # 权限判断函数
    bot_role = (await bot.get_group_member_info(group_id=event["group_id"], user_id=event["self_id"]))["role"]
    user_role = (await bot.get_group_member_info(group_id=event["group_id"], user_id=event["user_id"]))["role"]
    role = False
    if bot_role == 'member':
        role = False
    elif bot_role == 'admin' and user_role == 'owner':
        role = False
    elif bot_role == 'admin' and user_role == 'admin':
        role = False
    elif bot_role == 'admin' and user_role == 'member':
        role = True
    elif bot_role == 'owner':
        role = True
    return role


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
            if await _contrast(event):
                ban = random.randint(60, 300)
                await bot.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=int(ban))
                await bot.send(event, "你已知道，这是必死之局。砰，你死了。距离下次复活还有：" + str(int(ban / 60)) + "分")
                await bot.send(event, "已重新装填子弹。")
                mag = [1, 2, 3, 4, 5, 6]
                rem = 5
            elif not await _contrast(event):
                await bot.send(event, "你已知道，这是必死之局。砰，你死了。呃，好像打不穿你的防弹衣呢……")
                await bot.send(event, "已重新装填子弹。")
                mag = [1, 2, 3, 4, 5, 6]
                rem = 5
        elif re == 6:
            if await _contrast(event):
                ban = random.randint(60, 300)
                await bot.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=int(ban))
                await bot.send(event, "砰，你死了。距离下次复活还有：" + str(int(ban / 60)) + "分")
                await bot.send(event, "已重新装填子弹。")
                mag = [1, 2, 3, 4, 5, 6]
                rem = 5
            elif not await _contrast(event):
                await bot.send(event, "砰，你死了。呃，好像打不穿你的防弹衣呢……")
                await bot.send(event, "已重新装填子弹。")
                mag = [1, 2, 3, 4, 5, 6]
                rem = 5
        elif re != 6:
            del mag[int(bul)]
            await bot.send(event, "“咔嚓” 哈，是空的。侥幸逃过一劫呢，哼。剩余弹仓：" + str(len(mag)))
    elif msg == '俄罗斯轮盘死':
        await bot.send(event, "砰，你死了。")
    elif msg == '/占卜':
        await bot.send(event, "占你妈个头，滚！")


@bot.on_request('group', 'friend')
def handle_request(event):
    return {'approve': True}


@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
def handle_group_increase(event):
    bot.send(event, '欢迎新人～')  # 发送欢迎新人


# 暂时这样！
bot.run(host='127.0.0.1', port=8080)  # M6
