import discord
import asyncio
from discord.ext import commands
from NumBall import *

config = open("config.txt", 'r')

for string in config.readlines():
    exec(string)

digit = int(digit)
diff = int(diff)

bot = commands.Bot(command_prefix='', description='')
game = Computer(digit, diff)

def DiscordUI(digit, diff, token):
    try:
        bot.run(token)
    except:
        print('토큰이 잘못 입력됬거나 네트워크에 연결되지 않았습니다.')
        exit()

@bot.event
async def on_message(message):
    text = message.content.split(' ')
    if text[0] == 'start' and game.state == 'start':
        embed = discord.Embed(title='NumBall Bot', desription="")
        embed.add_field(name='게임을 시작합니다', value='-'*30, inline=False)
        embed.add_field(name='당신의 숫자를 입력하세요', value='-'*30, inline=False)
        await bot.send_message(message.channel, embed=embed)
        game.state = 'setplayernum'
    elif text[0] == 'set':
        if game.state == 'setplayernum' and game.isRight(text[1]):
            game.setPlayerNum(text[1])
            game.setComputerNum()
            embed = discord.Embed(title='NumBall Bot', desription="")
            embed.add_field(name='숫자를 정했습니다', value='-'*30, inline=False)
            embed.add_field(name='컴퓨터가 숫자를 정했습니다', value='-'*30, inline=False)
            embed.add_field(name='공격할 수를 입력해주세요', value='-'*30, inline=False)
            await bot.send_message(message.channel, embed=embed)
            game.state = 'attack'
        elif game.state == 'setplayernum':
            embed = discord.Embed(title='NumBall Bot', desription="")
            embed.add_field(name='입력 형식에 맞지 않게 입력하셨습니다', value='-'*30, inline=False)
            await bot.send_message(message.channel, embed=embed)
    elif text[0] == 'guess':
        if game.state == 'attack' and game.isRight(text[1]):
            attackNum, s, b = game.Attack(text[1])
            embed = discord.Embed(title='NumBall Bot', desription="")
            embed.add_field(name='%s로 공격한 결과 strike: %d, ball: %d'%(attackNum, s, b), value='-'*30, inline=False)
            if game.winner == None:
                attackNum, s, b = game.Defend()
                embed.add_field(name='컴퓨터가 공격합니다', value='-'*30, inline=False)
                embed.add_field(name='%s로 공격한 결과 strike: %d, ball: %d'%(attackNum, s, b), value='-'*30, inline=False)
            if not game.winner == None:
                embed.add_field(name='%s가 승리하였습니다!'%getWinner(), value='-'*30, inline=False)
                game.state = 'end'
            await bot.send_message(message.channel, embed=embed)
            game.state = 'attack'
        elif game.state == 'attack':
            embed = discord.Embed(title='NumBall Bot', desription="")
            embed.add_field(name='입력 형식에 맞지 않게 입력하셨습니다', value='-'*30, inline=False)
            await bot.send_message(message.channel, embed=embed)
            
