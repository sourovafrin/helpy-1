from beem.steem import Steem
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.utils import construct_authorperm
from pymongo import MongoClient
from datetime import timedelta
import time
import os

CH = os.environ.get('CH')
SV = os.environ.get('SV')
MD = os.environ.get('MD')

client = MongoClient(MD)
db = client.get_database("wls_db")
record = db.wls_link

wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'])
blockchain = Blockchain(steem_instance=wls, mode='head')
whitelist = ['anritco','samest','karinxxl','stackin','thebugiq','zakaria','tedtv','newenx','ladyfont','azizbd','muh543','chilix','sardart','xawi','rehan12','haejin','tezzmax','arepadigital','caminante','bmbk','exe8422','backpackingmonk','termite','peman85','heeyahnuh']
cmnt = ['thebugiq','haejin']
thresold = timedelta(minutes=29)
print("Running")


def check():
    for i in record.find():
        perms = i['link']
        wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'])
        post = Comment(perms, steem_instance=wls)
        age = post.time_elapsed()
        if age > thresold:
            wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'], keys=[CH, SV])
            post.clear_cache()
            post.refresh()
            reward = float(post.reward)
            print("Post link: {}".format(perms))
            print("Reward before upvote {}".format(reward))
            if reward <= 0.1:
                wt = 90
            elif reward <= 0.2:
                wt = 70
            elif reward <= 0.3:
                wt = 30
            elif reward <= 0.4:
                wt = 15
            elif reward <= 1:
                wt = 10
            else:
                wt = 1
            try:
                if wt == 1:
                    record.delete_one({"link": perms})
                else:
                    post.upvote(weight=60, voter='mrcheisen')
                    time.sleep(1)
                    post.upvote(weight=wt, voter='sourov')
                    if author not in cmnt:
                        post.reply("Ahoi, Your post has been upvoted by me and `@sourov`. Keep up the good work ✌\nReply `@sourov stop` in case you don't want comment anymore.", author="mrcheisen")
                        
                    print("Upvoted\nTime elapsed {}\n\n*************************".format(age))
                    record.delete_one({"link": perms})
            except Exception as e:
                print(e)
        else:
            break


for data in blockchain.stream('comment'):
    if int(record.count_documents({})) > 0:
        check()
    else:
        time.sleep(1)
    author = data['author']
    perm = data['permlink']
    permlink = construct_authorperm(author, perm)
    post = Comment(permlink, steem_instance=wls)

    if post.is_comment() == False and author in whitelist:
        link = {"link": permlink}
        record.insert_one(link)
