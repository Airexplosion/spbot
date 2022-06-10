from pprint import pprint

from aiocqhttp import CQHttp, Event
import random

bot = CQHttp()

# 全局变量mag rem 为俄罗斯轮盘赌功能服务
global _mag, _rem
_mag = [1, 2, 3, 4, 5, 6]
_rem = 5

# 前缀匹配和完全匹配指令的注册字典
on_commands = {}


# 命令处理函数装饰器
def on_command(name):
    def decorator(func):
        on_commands[name] = func
        return func

    return decorator


#  判断是群聊消息还是私聊消息group_or_private函数
def group_or_private(event: Event):
    place = False
    if event["message_type"] == "private":
        place = 1
    elif event["message_type"] == "group":
        place = 2
    return place


#  获取群内成员昵称group_card
async def group_card(event: Event):
    card = (await bot.get_group_member_info(group_id=event["group_id"], user_id=event["user_id"]))["card"]
    return card


# 机器人群聊权限判断函数_contrast 如果是非群聊 直接返回False
async def _contrast(event: Event):
    role = False
    if event["message_type"] == 'group':
        bot_role = (await bot.get_group_member_info(group_id=event["group_id"], user_id=event["self_id"]))["role"]
        user_role = (await bot.get_group_member_info(group_id=event["group_id"], user_id=event["user_id"]))["role"]
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
    else:
        pass
    return role


# 俄罗斯轮盘赌 单发
@on_command('俄罗斯轮盘赌')
async def r_only_gun(event: Event, *args):
    global _mag, _rem
    bul = random.randint(0, _rem)
    _rem = int(_rem) - 1
    re = _mag[int(bul)]
    if _rem == -1:
        if await _contrast(event):
            ban = random.randint(60, 300)
            await bot.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=int(ban))
            await bot.send(event, "你已知道，这是必死之局。砰，你死了。距离下次复活还有：" + str(int(ban / 60)) + "分")
            await bot.send(event, "已重新装填子弹。")
            _mag = [1, 2, 3, 4, 5, 6]
            _rem = 5
        elif not await _contrast(event):
            await bot.send(event, "你已知道，这是必死之局。砰，你死了。呃，好像打不穿你的头盖骨呢……")
            await bot.send(event, "已重新装填子弹。")
            _mag = [1, 2, 3, 4, 5, 6]
            _rem = 5
    elif re == 6:
        if await _contrast(event):
            ban = random.randint(60, 300)
            await bot.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=int(ban))
            await bot.send(event, "砰，你死了。距离下次复活还有：" + str(int(ban / 60)) + "分")
            await bot.send(event, "已重新装填子弹。")
            mag = [1, 2, 3, 4, 5, 6]
            rem = 5
        elif not await _contrast(event):
            await bot.send(event, "砰，你死了。呃，好像打不穿你的头盖骨呢……")
            await bot.send(event, "已重新装填子弹。")
            _mag = [1, 2, 3, 4, 5, 6]
            _rem = 5
    elif re != 6:
        del _mag[int(bul)]
        await bot.send(event, "“咔嚓” 哈，是空的。侥幸逃过一劫呢，哼。剩余弹仓：" + str(len(_mag)))
    return


# 俄罗斯轮盘赌 多发
@on_command('俄罗斯轮盘赌')
async def r_more_gun(event: Event, *args):
    try:
        a = int(args[0])
    except ValueError:
        return await bot.send(event, '你到底要开几枪？或者我直接毙了你？')
    for i in range(0, a):
        global _mag, _rem
        bul = random.randint(0, _rem)
        _rem = int(_rem) - 1
        re = _mag[int(bul)]
        if _rem == -1:
            if await _contrast(event):
                ban = random.randint(60, 300)
                await bot.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=int(ban))
                await bot.send(event, "你已知道，这是必死之局。砰，你死了。距离下次复活还有：" + str(int(ban / 60)) + "分")
                await bot.send(event, "已重新装填子弹。")
                _mag = [1, 2, 3, 4, 5, 6]
                _rem = 5
                break
            elif not await _contrast(event):
                await bot.send(event, "你已知道，这是必死之局。砰，你死了。呃，好像打不穿你的头盖骨呢……")
                await bot.send(event, "已重新装填子弹。")
                _mag = [1, 2, 3, 4, 5, 6]
                _rem = 5
                break
        elif re == 6:
            if await _contrast(event):
                ban = random.randint(60, 300)
                await bot.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=int(ban))
                await bot.send(event, "砰，你死了。距离下次复活还有：" + str(int(ban / 60)) + "分")
                await bot.send(event, "已重新装填子弹。")
                _mag = [1, 2, 3, 4, 5, 6]
                _rem = 5
                break
            elif not await _contrast(event):
                await bot.send(event, "砰，你死了。呃，好像打不穿你的头盖骨呢……")
                await bot.send(event, "已重新装填子弹。")
                _mag = [1, 2, 3, 4, 5, 6]
                _rem = 5
                break
        elif re != 6:
            del _mag[int(bul)]
            await bot.send(event, "“咔嚓” 哈，是空的。侥幸逃过一劫呢，哼。剩余弹仓：" + str(len(_mag)))
    return


# 美国轮盘赌
@on_command('美国轮盘赌')
async def a_gun(event: Event, *args):
    if await _contrast(event):
        ban = random.randint(60, 300)
        await bot.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=int(ban))
        await bot.send(event, "啊，怎么是半自动手枪……砰，你死了。距离下次复活还有：" + str(int(ban / 60)) + "分")
        await bot.send(event, "已重新装填子弹。")
    elif not await _contrast(event):
        await bot.send(event, "啊，怎么是半自动手枪……砰，你死了。呃，好像打不穿你的头盖骨呢……")
        await bot.send(event, "已重新装填子弹。")
    return


# 占卜
@on_command('/占卜')
async def zhan(event: Event, *args):
    await bot.send(event, "占你妈个头，滚！")
    return


# rd骰点
@on_command('.rd')
async def _(event: Event, *args):
    if group_or_private(event) == 1:
        await bot.send(event, '你的本次骰点值为：D100=' + str(random.randint(1, 100)))
    elif group_or_private(event) == 2:
        await bot.send(event, str(await group_card(event))  + '掷骰：D100=' + str(random.randint(1, 100)))
    else:
        await bot.send(event, str(args))


# 消息处理
@bot.on_message('group', 'private')
async def _(event: Event):
    msg: str = event['message']
    sp = msg.split(maxsplit=1)
    if not sp:
        return
    cmd, *args = sp
    arg = ''.join(args)
    only_handler = on_commands.get(cmd)
    if only_handler and not arg:
        return await only_handler(event)
    else:
        return


# 好友邀请同意
@bot.on_request('group', 'friend')
async def handle_request(event: Event):
    return {'approve': True}


@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
async def handle_group_increase(event: Event):
    await bot.send(event, '欢迎新人～')  # 发送欢迎新人


# 暂时这样！
bot.run(host='127.0.0.1', port=8080)  # M6
