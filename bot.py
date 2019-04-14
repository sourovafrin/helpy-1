from discord.ext import commands
from beem.account import Account
from beem.comment import Comment
from beem import Steem
import asyncio
import os

SV=os.environ.get('SV')
client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    channel = client.get_channel('566855351018848271')
    print("running")
    await client.send_message(channel,"I am on with prefix `?`\n*Ayasha is beautiful, so why i though of helping her here*")


stm = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'],keys=[SV])
sourov = Account("sourov", steem_instance=stm)
acc = Account("mrcheisen", steem_instance=stm)

last_com = "<Comment @mrcheisen/re-black-man-homeless-heart-part-1-20190413t213522942z>"

def glo(met):
    global last_com
    last_com=met

@client.command()
async def start():
    while True:
        stm = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'], keys=[SV])
        comments = []
        vp = sourov.get_voting_power()
        if vp >=99.5:
            for perm in acc.comment_history():
                if str(perm) == last_com:
                    break
                else:
                    comments.append(perm)

            comments.reverse()
            if len(comments) == 2:
                await client.say("<@404376297624567810> I have only 1 more comment left to upvote. You better write some comment")
            if len(comments) == 1:
                await client.say("<@404376297624567810> I don't see any comment to upvote. Please, do hurry and comment.\nOtherwise, vp will go waste")
            if len(comments)==0:
                await client.say("<@404376297624567810> Vp is going waste. I will cut rewards from you :rage:")
            else:
                for comment in comments:
                    comm=Comment(comment,steem_instance=stm)
                    comm.upvote(100,"sourov")
                    glo(str(comment))
                    await client.say("Successfully upvoted `{}`".format(comm))
                    break
        else:
            wait_time=(99.51-vp)*4300
            msg=wait_time/60
            await client.say("Next upvote in `{}` minutes".format(msg))
            await asyncio.sleep(wait_time)

@start.error
async def on_command_error(error,ctx):
    if isinstance(error, Exception, ):
        await client.say(error)
        
        
@client.command()
async def vp():
    vp = sourov.get_voting_power()
    await client.say(vp)

client.run(os.environ.get('TOKEN'))
