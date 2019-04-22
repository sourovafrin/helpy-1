from beem.steem import Steem
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.utils import construct_authorperm
import time
import asyncio
import os

SV=os.environ.get('SV')

wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'])
blockchain = Blockchain(steem_instance=wls, mode='head')
whitelist = ['anritco', 'gabeboy','samest','djlethalskillz','adsactly','karinxxl','stackin',]
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
                        keys=[SV])
            asyncio.sleep(1)
            time.sleep(1500)
            try:
                post.upvote(weight=50,voter='sourov')
                post_age = post.time_elapsed()
            except Exception as e:
                print(e)
            print("Upvoted {}\nTime elapsed {}\n\n*************************".format(permlink,post_age))
        else:
            pass
