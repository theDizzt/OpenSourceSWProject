import discord
import asyncio
import os
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='!',help_command=None)
chipdir = "./saved"

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    print("Discord bot ID is "+str(bot.user.id))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!help 카지노 일'))

@bot.command(aliases=["Hello","hello!","Hello!","hi","Hi","hi!","Hi!"])
async def hello(ctx):
    
    await ctx.channel.send("Hello!")

@bot.command()
async def embed(ctx):
    embed=discord.Embed(title="Embed", description="Embed 내용.", color=0x00aaaa)
    embed.set_author(name="작성자의 이름")
    embed.add_field(name="이것은 field1입니다.", value="이것은 field1 값입니다.", inline=False)
    embed.add_field(name="이것은 field2입니다.", value="이것은 field2 값입니다.", inline=False)
    embed.add_field(name="이것은 field3입니다.", value="이것은 field3 값입니다.", inline=False)
    embed.add_field(name="이것은 field4입니다.", value="이것은 field4 값입니다.", inline=False)
    embed.set_footer(text="이것은 footer의 값입니다.")
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["help"])
async def Help(ctx):
    embed=discord.Embed(title="명령어 목록", description="모든 명령어는 !(명령어) 형태", color=0x00aaaa)
    embed.set_author(name="카지노 봇")
    embed.add_field(name="!help", value="명령어 목록을 알려줍니다", inline=False)
    embed.add_field(name="!addChip (숫자)", value="(숫자)만큼 칩을 추가합니다. 값이 없으면 100개", inline=False)
    embed.add_field(name="!가위바위보 (숫자)", value="테스트용 게임. 칩을 걸고 가위바위보를 합니다. 기본값은 1개", inline=False)
    embed.add_field(name="!myChip", value="플레이어의 칩 수를 보여줍니다.", inline=False)
    embed.set_footer(text="footer는 아직 어떻게 쓸지 모른다.")
    await ctx.channel.send(embed=embed)

def chipchange(ctx,want):
    if not os.path.isdir(chipdir):
        os.mkdir(chipdir)
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)
    try:
        with open(player+".txt","r") as playerchip:
            chip=int(playerchip.read())
            print(chip)
        with open(player+".txt","w") as playerchip:
            chip = chip+want
            print(chip)
            playerchip.write(str(chip))
    except FileNotFoundError:
        with open(player+".txt","w") as playerchip:
            playerchip.write("100")

@bot.command(aliases=["mychip"])
async def myChip(ctx):
    chipchange(ctx,0)
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)
    with open(player+".txt","r") as playerchip:
        await ctx.channel.send(ctx.author.name+"씨의 칩은 "+playerchip.read()+"개")

@bot.command(aliases=["addchip"])
async def addChip(ctx,wants=100):
    chipchange(ctx,wants)
    senderid=ctx.author.id
    player = chipdir+"/player"+str(senderid)
    with open(player+".txt","r") as playerchip:
        await ctx.channel.send(ctx.author.name+"씨의 칩은 "+playerchip.read()+"개")



@bot.command(aliases=["가위바위보","rps"])
async def RockPaperSissors(ctx,wants=1):
    rps = ["가위","바위","보"]
    embed = discord.Embed(title="가위바위보",description=ctx.author.name+"님\n가위, 바위, 보 중 하나를 5초 안에 내주세요!", color=0x00aaaa)
    senderid=ctx.author.id
    channel = ctx.channel
    msg1 =await ctx.channel.send(embed=embed)
    def checksame(newtext):
        return newtext.author == ctx.author and newtext.channel == channel
    try:
        msg2 = await bot.wait_for('message', timeout=5.0, check=checksame)
    except asyncio.TimeoutError:
        await msg1.delete()
        embed = discord.Embed(title="가위바위보",description="5초가 다 지났어요!", color=0x00aaaa)
        await ctx.channel.send(embed=embed)
        return
    else:
        await msg1.delete()
        bot_rps = str(random.choice(rps))
        user_rps  = str(msg2.content)
        answer = ""
        if bot_rps == user_rps:
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "비겼습니다.\n"
            wants=0
        elif (bot_rps == "가위" and user_rps == "바위") or (bot_rps == "보" and user_rps == "가위") or (bot_rps == "!바위" and user_rps == "!보"):
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "승리하셨습니다. 칩 "+str(wants)+"개를 획득하셨습니다.\n"
            
        elif (bot_rps == "바위" and user_rps == "가위") or (bot_rps == "가위" and user_rps == "보") or (bot_rps == "!보" and user_rps == "!바위"):
            answer = "딜러인 저는 " + bot_rps + "를 냈고, "+ctx.author.name+"씨는 " + user_rps + "를 내셨습니다.\n" + "패배하셨습니다. 칩 "+str(wants)+"개를 잃으셨습니다.\n"
            wants=-wants
        else:
            embed = discord.Embed(title="가위바위보",description="가위, 바위, 보 중에서만 내셔야 합니다.", color=0x00aaaa)
            await ctx.channel.send(embed=embed)
            return
        senderid=ctx.author.id
        player = chipdir+"/player"+str(senderid)
        with open(player+".txt","r") as playerchip:
            chipchange(ctx,wants)
            answer = answer + "\n"+ctx.author.name+"씨의 칩은 "+playerchip.read()+"개"
        embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
        await ctx.channel.send(embed=embed)
        return

bot.run('my token')
