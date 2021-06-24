from discord.ext import commands
import requests
import discord
import asyncio
import time

#change token
token = 'ODE3NzQ3MjMwODM5Nzk5ODA4.YEOAdA.tBU1Hmr9tZkPsBSkFrmCNylpF8o'
bot = commands.Bot(command_prefix='!')

""" allowed = [False,False]
answered = [False,False]
countdown = 0
answers = {}
#manual input of ids
channels = ['team-1', 'team-2']
channel_ids = [817940087206707240, 817940251623555142] """
allowed=[]
answered=[]
text_channel_dict={}
channel_ids=[]
qnset=[]
numteams=0

# Function to get the channel ids of team text channels from the discord server

@bot.command(name='new', help="Initialize the connections to the team channels")
@commands.has_role("QM")
async def get_channel_ids(ctx):
    global text_channel_dict
    global channel_ids
    global answered
    global allowed
    global numteams
    text_channel_dict = {}
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if 'team' in channel.name.lower():
                text_channel_dict[channel.name] = channel.id
    channel_ids = list(text_channel_dict.values())
    # print(channel_ids)
    numteams=len(channel_ids)
    # print(numteams)
    await ctx.send('Connections with teams established')
    answered =[False]*numteams
    allowed=[False]*numteams

# Function to add the .txt file containing questions to be displayed on discord

@bot.command(name="questions",help="To add the .txt file containing qns to be displayed on discord")
@commands.has_role("QM")
async def qnreg(ctx):
    global qnset
    attachment_url = ctx.message.attachments[-1].url
    file_request = requests.get(attachment_url)
    contents=(file_request.text.split("\n"))
    await ctx.send("Qns registered")
    qnset=contents
    # print(qnset)

# Function which the QM would use to send a particular question to every team channel

@bot.command(name="show",help="To send the question to every team channel, !show [question number]")
@commands.has_role('QM')
async def qnshow(ctx,qno):
    for id in channel_ids:
        await bot.get_channel(id).send(qnset[int(qno)-1])

# Function to start buzzer timer
        
@bot.command(name='start',help="Start the timer !start [time(in seconds)]")
@commands.has_role('QM')
async def trial(ctx, arg):
    global allowed
    global countdown
    global answered
    global answers
    global numteams
    answers = {}
    allowed = [True]*numteams
    answered = [False]*numteams
    countdown = int(arg)
    t1 = time.time()
    messages =[]
    for id in channel_ids:
        # print(id)
        messages.append(await bot.get_channel(id).send(min([(countdown//5+1)*5,int(arg)])))         #Time left will decrease by intervals of 5
    
    count=[0]*numteams

    while countdown > 1:
        countdown = int(arg) - (time.time() - t1)
        for i in range(0,numteams):
            if answered[i] == True and count[i]==0:
                allowed[i] = False
                count[i]=1
                
            else:
                for message in messages:
                    await message.edit(content=(int(countdown)//5+1)*5)
                    

    else:
        for message in messages:
            await message.edit(content='TimeUp')
        await ctx.send("Time's Up!")
        allowed = [False]*numteams
        countdown = int(arg)
        answered = [False]*numteams

# Function using which teams can send their answer
        
@bot.command(name='ans', help="Write your pounce answer by mentioning !ans and then your answer")
async def answer(ctx):
    global allowed
    global answered
    global answers
    index=channel_ids.index(ctx.channel.id)
    if allowed[index] == True:
        answer = ctx.message.content[5:]
        answers[str(ctx.channel)] = answer
        await ctx.send(f"Seen. Your answer is {answer}")
        answered[index] = True
        allowed[index] = False
    else:
        await ctx.message.reply('Pounce closed')

# Function using which QM can see the pounce answers of each team

@bot.command(name='fetch', help="To see the pounce answers of each team.")
@commands.has_role('QM')
async def fetch_answers(ctx):
    global answers
    message = ''
    for i in answers.keys():
        message = message + i + '\t\t' + answers[i] + '\n'
    if message == '':
        await ctx.send("No team pounced")
    else:
        await ctx.send(message)

bot.run(token)
