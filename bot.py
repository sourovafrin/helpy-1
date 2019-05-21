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
whitelist = ['anritco','samest','karinxxl','stackin','thebugiq','zakaria','tedtv','dangyver','ladyfont','azizbd','muh543','chilix','sardart']
print("Running")
for data in blockchain.stream('comment'):
    time.sleep(1)
    author = data['author']
    perm = data['permlink']
    permlink = construct_authorperm(author, perm)
    post = Comment(permlink, steem_instance=wls)
    if post.is_comment() == True:
        pass
    else:
        if author in whitelist:
            wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'],
                        keys=[CH,SV])
            asyncio.sleep(1)
            time.sleep(1500)
            try:
                post.upvote(weight=10,voter='sourov')
                post_age = post.time_elapsed()
                if author == 'mrcheisen':
                    pass
                else:
                    post.upvote(weight=60,voter='mrcheisen')
                    post.reply("Ahoi, Your post has been upvoted by me and `@sourov`. Keep up the good work ✌",author="mrcheisen")
            except Exception as e:
                print(e)
            print("Upvoted {}\nTime elapsed {}\n\n*************************".format(permlink,post_age))
        else:
            pass
