from discord.ext import commands
from discord import embeds
import asyncio

token = 'ODE3NzM3NTM2MzEwNDc2ODIx.YEN3bQ.SXXDk7rw87AT_zDMmR1KleTrSy4'

bot=commands.Bot(command_prefix='!')

allowed=True
countdown=0
answered=False
answers={}
channels=['team-1','team-2']
@bot.command(name='start')
@commands.has_role('Test_QM')
async def trial(ctx,arg):
    global allowed
    global countdown
    global answered
    global answers
    answers={}
    allowed=True
    answered = False
    countdown=int(arg)
    message=await ctx.send(countdown)
    print(type(message))
    while countdown>1:
        print(countdown,answered,allowed)
        if answered == True:
            allowed = False
            countdown = int(arg)
            answered = False
            print("Answer received.")
            break
        else:
            await asyncio.sleep(0.9)
            countdown-=1
            await message.edit(content=countdown)
    else:
        await ctx.send('TimeUp')
        allowed = False
        countdown = int(arg)
        answered = False
        
@bot.command(name='ans', help="Write your pounce answer by mentioning !ans and then your answer")
async def answer(ctx):
    global allowed
    global answered
    global answers
    if allowed == True:
        answer=ctx.message.content[5:]
        answers[str(ctx.channel)]=answer
        await ctx.send(f"Seen. Your answer is {answer}")
        answered = True
    else:
        await ctx.message.reply('Pounce closed')

@bot.command(name='fetch', help="To see the pounce answers of each team.")
@commands.has_role('Test_QM')
async def fetch_answers(ctx):
    global answers
    message=''
    for i in answers.keys():
        message=message+i+'        '+answers[i]+'\n'
    if message=='':
        await ctx.send("No team pounced")
    else:
        await ctx.send(message)
    
bot.run(token)
