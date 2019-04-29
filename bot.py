from beem.steem import Steem
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.utils import construct_authorperm
import time
import asyncio
import os

SV=os.environ.get('SV')
CH=os.environ.get('CH')

wls = Steem(node=['https://wls.kennybll.com', 'https://wls.kidw.space/', 'wss://wls.kidw.space/'])
wlss = Steem(node=['https://wls.kennybll.com', 'https://wls.kidw.space/', 'wss://wls.kidw.space/'])
blockchain = Blockchain(steem_instance=wls, mode='head')
whitelist = ['anritco', 'gabeboy','samest','djlethalskillz','adsactly','karinxxl','stackin','milkbox.esp']
print("Running")
for data in blockchain.stream('comment'):
    time.sleep(1)
    author = data['author']
    perm = data['permlink']
    permlink = construct_authorperm(author, perm)
    post = Comment(permlink, steem_instance=wls)
    postt = Comment(permlink, steem_instance=wlss)
    if post.is_comment() == True:
        pass
    else:
        if author in whitelist:
            wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'],
                        keys=[SV])
            wlss = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'],
                        keys=[CH])
            asyncio.sleep(1)
            time.sleep(1500)
            try:
                post.upvote(weight=50,voter='sourov')
                time.sleep(1)
                postt.upvote(weight=90,voter='mrcheisen')
                post_age = post.time_elapsed()
            except Exception as e:
                print(e)
            print("Upvoted {}\nTime elapsed {}\n\n*************************".format(permlink,post_age))
        else:
            pass
