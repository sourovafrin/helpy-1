from beem.steem import Steem
from beem.blockchain import Blockchain
from beem.account import Account
from beem.comment import Comment
from beem.utils import construct_authorperm
import asyncio
import os

SV=os.environ.get('SV')

wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'])
blockchain = Blockchain(steem_instance=wls,mode='head')
ignore_list= ['holger80']

print("Running")
for data in blockchain.stream('vote'):
    print(data)
    asyncio.sleep(1)
    if data['voter'] == 'holger80':
        author = data['author']
        permlink = data['permlink']
        vote_percent = round(int(data['weight']) * 0.8,2)
        if author in ignore_list:
            pass
        if vote_percent == 0:
            pass
        else:
            wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'],
                        keys=[SV])
            main_perm = construct_authorperm(author,permlink)
            account = Account('sourov')
            post = Comment(main_perm,steem_instance=wls)
            try:
                post.upvote(weight=vote_percent, voter='sourov')
                post_age = post.time_elapsed()
            except Exception as e:
                print(e)
            print("Upvoted {}\nVoting weight {}\nTime elapsed {}\n\n*************************".format(main_perm,vote_percent,post_age))
