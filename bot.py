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


@client.command()
async def start(memo):
    last_com = memo
    runn = True
    while runn:
        stm = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'], keys=[SV])
        comments = []
        vp = sourov.get_voting_power()
        if vp >=99.7:
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
            if len(comments) == 0:
                await client.say("<@404376297624567810> Vp is going waste. I will cut rewards from you :rage:\nBy the way when you comment, start the bot again by this command: `?start`. Stopping......")
                runn = False
            else:
                for comment in comments:
                    comm=Comment(comment,steem_instance=stm)
                    comm.upvote(100,"sourov")
                    await client.say("Successfully upvoted `{}`".format(comm))
                    last_com = comm
                    await asyncio.sleep(5)
                    break
        else:
            wait_time=(99.71-vp)*4300
            msg=wait_time/60
            hr=msg/60
            await client.say("Next upvote in `{}` minutes or `{}` hours".format(msg,hr))
            await asyncio.sleep(wait_time)


        
        
@client.command()
async def vp():
    vp = sourov.get_voting_power()
    await client.say(vp)

client.run(os.environ.get('TOKEN'))
