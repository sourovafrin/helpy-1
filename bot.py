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
cmnt = ['thebugiq', 'haejin', 'backpackingmonk', 'marinella', 'al-desnudo', 'sardart']
special = ['anritco', 'heyimsnuffles', 'marinella', 'joseph1956', 'thebugiq', 'ladyfont', 'muh543', 'haejin', 'backpackingmonk']
print("Running")


def check():
    for i in record.find():
        perms = i['link']
        wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'])
        post = Comment(perms, steem_instance=wls)
        age = post.time_elapsed()
        au = str(post.author)
        if au == 'haejin':
            thresold = timedelta(minutes=23)
        else:
            thresold = timedelta(minutes=29)
        if age > thresold:
            wls = Steem(node=['wss://wls.kidw.space/', 'https://wls.kidw.space/', 'https://wls.kennybll.com'], keys=[CH, SV])
            if au in special:
                post.clear_cache()
                post.refresh()
                reward = float(post.reward)
                print("Post link: {}".format(perms))
                print("Time elapsed {}".format(age))
                print("Reward before upvote {}".format(reward))
                if reward <= 0.05:
                    wt = 90
                elif reward <= 0.1:
                    wt = 80
                elif reward <= 0.3:
                    wt = 60
                elif reward <= 0.4:
                    wt = 40
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
                        post.upvote(weight=wt, voter='sourov')
                        time.sleep(1)
                        post.upvote(weight=50, voter='mrcheisen')
                        if post.author not in cmnt:
                            post.reply("Ahoi, Your post has been upvoted by me and `@sourov`. Keep up the good work ✌\nReply `@sourov stop` in case you don't want comment anymore.", author="mrcheisen")
                        print("Upvoted\n\n*************************")
                        record.delete_one({"link": perms})
                except Exception as e:
                    e = str(e)
                    print("Following error :{}".format(e))
                    if e == 'You have already voted in a similar way.':
                        record.delete_one({"link": perms})
                    elif e == 'You may only comment once every 20 seconds.':
                        time.sleep(18)
                        post.reply("Ahoi, Your post has been upvoted by me and `@sourov`. Keep up the good work ✌\nReply `@sourov stop` in case you don't want comment anymore.", author="mrcheisen")
            else:
                post.clear_cache()
                post.refresh()
                reward = float(post.reward)
                print("Post link: {}".format(perms))
                print("Time elapsed {}".format(age))
                print("Reward before upvote {}".format(reward))
                if reward <= 0.1:
                    wt = 60
                elif reward <= 0.2:
                    wt = 50
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
                        print("xxxxxxxxxxxxxxxxxxxxxxxxx\nDidn't upvoted\nxxxxxxxxxxxxxxxxxxxxxxxxx")
                    else:
                        post.upvote(weight=70, voter='mrcheisen')
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
                    elif e == 'You may only comment once every 20 seconds.':
                        time.sleep(18)
                        post.reply("Ahoi, Your post has been upvoted by me and `@sourov`. Keep up the good work ✌\nReply `@sourov stop` in case you don't want comment anymore.", author="mrcheisen")
        else:
            break


def in():
    for data in blockchain.stream('comment'):
        if int(record.count_documents({})) > 0:
            Thread(target=check, args=()).start()
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


if __name__ == '__main__':
    t1 = Thread(target=in, args=())
    t1.start()
