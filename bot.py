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
whitelist = ['anritco','samest','karinxxl', 'heyimsnuffles', 'chrisrendon', 'theunion', 'zhanavic69', 'al-desnudo', 'uche-nna', 'samprock', 'marinella', 'joseph1956', 'stackin','thebugiq','zakaria','tedtv','newenx','ladyfont','azizbd','muh543','chilix','sardart','xawi','rehan12','haejin','tezzmax','caminante','backpackingmonk','termite','peman85','heeyahnuh']
cmnt = ['thebugiq', 'haejin', 'backpackingmonk', 'marinella', 'al-desnudo']
print("Running")


def check():
    for i in record.find():
        perms = i['link']
        wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'])
        post = Comment(perms, steem_instance=wls)
        age = post.time_elapsed()
        au = str(post.author)
        if au == 'haejin':
            thresold = timedelta(minutes=24)
        else:
            thresold = timedelta(minutes=29)
        if age > thresold:
            wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'], keys=[CH, SV])
            post.clear_cache()
            post.refresh()
            reward = float(post.reward)
            print("Post link: {}".format(perms))
            print("Time elapsed {}".format(age))
            print("Reward before upvote {}".format(reward))
            if reward <= 0.1:
                wt = 100
            elif reward <= 0.2:
                wt = 75
            elif reward <= 0.3:
                wt = 50
            elif reward <= 0.4:
                wt = 30
            elif reward <= 1:
                wt = 20
            elif reward <= 1.5:
                wt = 15
            elif reward <= 2:
                wt = 10
            else:
                wt = 1
            try:
                if wt == 1:
                    record.delete_one({"link": perms})
                    print("xxxxxxxxxxxxxxxxxxxxxxxxx\nDidn't upvoted\nxxxxxxxxxxxxxxxxxxxxxxxxx")
                else:
                    post.upvote(weight=80, voter='mrcheisen')
                    time.sleep(1)
                    post.upvote(weight=wt, voter='sourov')
                    if post.author not in cmnt:
                        post.reply("Ahoi, Your post has been upvoted by me and `@sourov`. Keep up the good work ✌\nReply `@sourov stop` in case you don't want comment anymore.", author="mrcheisen")
                    print("Upvoted\n\n*************************")
                    record.delete_one({"link": perms})
            except Exception as e:
                e = str(e)
                print("Following error :{}".format(e))
                if e == 'You have already voted in a similar way.':
                    record.delete_one({"link": perms})
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
        print("A new post has been found and thrown into database.\nAuthor: {}".format(author))
        link = {"link": permlink}
        record.insert_one(link)
