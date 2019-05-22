from beem.steem import Steem
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.utils import construct_authorperm
import time
import asyncio
import os

CH=os.environ.get('CH')
SV=os.environ.get('SV')

wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'])
blockchain = Blockchain(steem_instance=wls, mode='head')
whitelist = ['anritco','samest','karinxxl','stackin','thebugiq','zakaria','tedtv','dangyver','ladyfont','azizbd','muh543','chilix','sardart','xawi','rehan12','haejin']
cmnt = ['thebugiq','haejin']
print("Running")
for data in blockchain.stream('comment'):
    author = data['author']
    perm = data['permlink']
    permlink = construct_authorperm(author, perm)
    post = Comment(permlink, steem_instance=wls)
    if post.is_comment() == True:
        pass
    else:
        if author in whitelist:
            wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'], keys=[CH,SV])
            asyncio.sleep(1)
            if author == 'haejin':
                time.sleep(1400)
            else:
                time.sleep(1790)
            reward = float(post.reward)
            if reward == 0:
                wt = 100
            elif reward <= 0.1:
                wt = 90
            elif reward <= 0.2:
                wt = 70
            elif reward <= 0.3:
                wt = 30
            elif reward <= 0.4:
                wt = 15
            else:
                wt =10
            try:
                post.upvote(weight=wt,voter='sourov')
                post_age = post.time_elapsed()
                post.upvote(weight=60,voter='mrcheisen')
                if author not in cmnt:
                    post.reply("Ahoi, Your post has been upvoted by me and `@sourov`. Keep up the good work ✌\nReply `@sourov stop` in case you don't want comment anymore.",author="mrcheisen")
            except Exception as e:
                print(e)
            print("Upvoted {}\nTime elapsed {}\n\n*************************".format(permlink,post_age))
        else:
            pass
