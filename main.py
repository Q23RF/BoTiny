import os
import discord
from discord.ext import tasks, commands
import random
from keep_alive import keep_alive
from pytube import Playlist

keep_alive()
vids = [
    "ATEEZ(에이티즈) WANTEEZ EP.15 명백한 허위 증언입니다⚖",
    "ATEEZ(에이티즈) - 'HALAZIA' Official MV",
    "Cyberpunk - ATEEZ(에이티즈) [뮤직뱅크/Music Bank] | KBS 230106 방송"
]

fcpl = "https://www.youtube.com/playlist?list=PL0VABZJqw90yVPy8-KB07rJRXTmhSXLj1&jct=MaS1nTcrBKbbHx0qptItZ0ZZkJSnMA"

stpl = "https://www.youtube.com/playlist?list=PL0VABZJqw90z2bSMI1_HPz4BZ007IT2lu&jct=l5Lwa9HRXpR0E3JYwUmjrFw8iSAldg"

mspl = "https://www.youtube.com/playlist?list=OLAK5uy_mhIfeEQekE1BSH2Qzwj-3AU-wTzIiC2Q4"


def get_random_vid(playlist_url):
    p = Playlist(playlist_url)
    urls = p.video_urls
    url = urls[random.randint(0, len(urls) - 1)]
    return url


token = os.environ['token']
bot = commands.Bot(command_prefix='!',
                   activity=discord.Activity(
                       type=discord.ActivityType.watching,
                       name=vids[random.randint(0,
                                                len(vids) - 1)]),
                   status=discord.Status.idle,
                   intents=discord.Intents.all())


@bot.event
async def on_ready():
    daily_stage.start()
    print('logged in as {0.user}'.format(bot))
    discord.opus.load_opus("./libopus.so.0.8.0")


@bot.event
async def on_member_join(member):
    wc_channel = bot.get_channel(1091314075285331999)
    fn = f"annyeong/a{str(random.randint(1, 3))}.jpg"
    await wc_channel.send(
        f"{member.name}！歡迎來到甲板女工會議室，我是甲板機器人啵梯妮。你可以先到公告頻道閱讀伺服器導覽，並為自己設定伺服器暱稱和身分組。",
        file=discord.File(fn))


@bot.command()
async def cmd(ctx):
    gl = "指令:\n!fancam 推薦欸梯子直拍\n!stage 推薦欸梯子舞台\n!song 推薦欸梯子歌曲"
    await ctx.send(gl)
    return


@bot.command()
async def fancam(ctx):
    r = random.randint(0, 1)
    mypl = "https://www.youtube.com/playlist?list=PLtq5j3zzu44kdauHhm79RQbVdT2UHEwQz"
    if r == 0:
        await ctx.send(get_random_vid(fcpl))
    else:
        await ctx.send("愚人節快樂！")
        await ctx.send(get_random_vid(mypl))


@bot.command()
async def stage(ctx):
    await ctx.send(get_random_vid(stpl))
    return


@bot.command()
async def song(ctx):
    await ctx.send(get_random_vid(mspl))
    return


@tasks.loop(hours=24)
async def daily_stage():
    print("sent")
    channel = bot.get_channel(int(1090973582487715880))
    await channel.send("今日舞台：" + get_random_vid(stpl))


try:
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
