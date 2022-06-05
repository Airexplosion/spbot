from aiocqhttp import CQHttp, Event
import random
from pprint import pprint

bot = CQHttp()

# 全局变量mag rem 为俄罗斯轮盘赌功能服务
global _mag, _rem
_mag = [1, 2, 3, 4, 5, 6]
_rem = 5

# 前缀匹配和完全匹配指令的注册字典
only_commands = {}
start_commands = {}


# 命令处理函数装饰器 完全匹配
def only_command(name):
    def decorator(func):
        only_commands[name] = func
        return func

    return decorator


# 命令处理函数装饰器 前缀匹配
def start_command(name):
    def decorator(func):
        start_commands[name] = func
        return func

    return decorator


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
@only_command('俄罗斯轮盘赌')
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
@start_command('俄罗斯轮盘赌')
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
@only_command('美国轮盘赌')
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
@only_command('/占卜')
async def zhan(event: Event, *args):
    await bot.send(event, "占你妈个头，滚！")
    return


# 群聊消息处理
@bot.on_message('group', 'private')
async def _(event: Event):
    msg: str = event['message']
    sp = msg.split(maxsplit=1)
    if not sp:
        return
    cmd, *args = sp
    arg = ''.join(args)
    only_handler = only_commands.get(cmd)
    start_handler = start_commands.get(cmd)
    if only_handler and not arg:  # 判断是否有后续指令
        return await only_handler(event)
    elif start_handler:  # 判断是否在前端匹配的注册库内
        return await start_handler(event, arg)
    else:
        return


# 好友邀请同意
@bot.on_request('group', 'friend')
async def handle_request(event):
    return {'approve': True}


@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
async def handle_group_increase(event):
    await bot.send(event, '欢迎新人～')  # 发送欢迎新人


# 暂时这样！
bot.run(host='127.0.0.1', port=8080)  # M6
