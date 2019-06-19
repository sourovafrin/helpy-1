from beem.steem import Steem
from beem.account import Account
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.utils import construct_authorperm
from pymongo import MongoClient
from datetime import timedelta
from threading import Thread
from discord_webhook import DiscordWebhook
import requests
import ast
import time
import os

CH = os.environ.get('CH')
SV = os.environ.get('SV')
MD = os.environ.get('MD')
AF = os.environ.get('AF')
WB = os.environ.get('WB')
MU = os.environ.get('MU')

client = MongoClient(MD)
db = client.get_database("wls_db")
record = db.wls_link

#wls = Steem(node='ws://wls.fullnode.nl:8090')
#blockchain = Blockchain(steem_instance=wls, mode='head')
whitelist = ['anritco','samest','karinxxl', 'heyimsnuffles', 'chrisrendon', 'theunion', 'zhanavic69', 'al-desnudo', 'uche-nna', 'samprock', 'marinella', 'joseph1956', 'stackin','thebugiq','zakaria','newenx','ladyfont','azizbd','muh543','chilix','sardart','xawi','rehan12','haejin','tezzmax','caminante','backpackingmonk','termite','peman85','heeyahnuh']
cmnt = ['thebugiq', 'haejin', 'backpackingmonk', 'marinella', 'al-desnudo', 'sardart']
special = ['anritco', 'heyimsnuffles', 'marinella', 'joseph1956', 'thebugiq', 'ladyfont', 'muh543', 'haejin', 'backpackingmonk']

"""
alric = 16
infarno = 5
zinter = 49
lyanna = 27
tyrus = 38
talia = 70
jarlax = 74
seachan = 71
foxwood = 72
kiara = 73
plado = 110
Valnamor = 111
Rennyn = 112
Peakrider = 113
Mancer = 109
Selenia = 56
62: Elven Cutthroat
64: Cocatrice
66: Enchanted Pixie
68: Magi Sphinx
9: Fire Demon
10: Serpent of the Flame
11: Elemental Phoenix
20: Mischievous Mermaid
21: Naga Warrior
22: Frost Giant
32: Swamp Thing
33: Spirit of the Forest
42: Defender of Truth
43: Air Elemental
44: Angel of Light
53: Dark Enchantress
54: Screaming Banshee
55: Lord of Darkness
57: Lightning Dragon
58: Chromatic Dragon
59: Gold Dragon
"""


di = {'16': .6,
       '5': .4,
      '49': .6,
      '27': .6,
      '38': .5,
      '70': .45,
      '32': .4,
      '31': .4,
      '42': .5,
      '71': .45,
      '72': .55,
      '73': .45,
      '74': .4,
      '62': .14,
      '64': .13,
      '66': .13,
      '68': 1.35,
      '9': .38,
      '10': .38,
      '11': 1.5,
      '20': .50,
      '82': 2,
      '22': 1.5,
      '33': 2,
      '98': 2,
      '32': .35,
      '43': .5,
      '44': 1.8,
      '53': .25,
      '54': .25,
      '55': 1.5,
      '57': 1.5,
      '58': 1.5,
      '59': 1.5}


dic = {'16': .7,
        '5': .50,
        '49': .7,
        '27': .56,
        '38': .68}

def check():
    for i in record.find():
        perms = i['link']
        wls = Steem(node='ws://wls.fullnode.nl:8090')
        post = Comment(perms, steem_instance=wls)
        age = post.time_elapsed()
        au = str(post.author)
        if au == 'haejin':
            thresold = timedelta(minutes=22)
        else:
            thresold = timedelta(minutes=29)
        if age > thresold:
            wls = Steem(node='ws://wls.fullnode.nl:8090', keys=[CH, SV])
            if au in special:
                post.clear_cache()
                post.refresh()
                reward = float(post.reward)
                print("Post link: {}".format(perms))
                print("Time elapsed {}".format(age))
                print("Reward before upvote {}".format(reward))
                if reward <= 0.05:
                    wt = 80
                elif reward <= 0.1:
                    wt = 60
                elif reward <= 0.3:
                    wt = 40
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
                    list = (post.get_votes(True))
                    voters = []
                    for i in list:
                        voters.append(i['voter'])
                    if wt == 1:
                        record.delete_one({"link": perms})
                        print("xxxxxxxxxxxxxxxxxxxxxxxxx\nDidn't upvoted\nxxxxxxxxxxxxxxxxxxxxxxxxx")
                    elif 'sourov' in voters:
                        record.delete_one({"link": perms})
                    else:
                        
                        post.upvote(weight=wt, voter='sourov')
                        time.sleep(1)
                        post.upvote(weight=45, voter='mrcheisen')
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
                    wt = 50
                elif reward <= 0.2:
                    wt = 35
                elif reward <= 0.3:
                    wt = 20
                elif reward <= 0.4:
                    wt = 15
                elif reward <= 1:
                    wt = 10
                else:
                    wt = 1
                try:
                    list = (post.get_votes(True))
                    voters = []
                    for i in list:
                        voters.append(i['voter'])
                    if wt == 1:
                        record.delete_one({"link": perms})
                        print("xxxxxxxxxxxxxxxxxxxxxxxxx\nDidn't upvoted\nxxxxxxxxxxxxxxxxxxxxxxxxx")
                    elif 'sourov' in voters:
                        record.delete_one({"link": perms})
                    else:
                        post.upvote(weight=45, voter='mrcheisen')
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


def inn():
    print("start wls")
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
            
def send(market_id, seller, card_price):
    stm = Steem(node="https://steemd.minnowsupportproject.org/", keys=AF)
    acc = Account("svirus",steem_instance=stm)   
    try:
        b = True
        lin = "https://steemmonsters.com/market/status?id=" + market_id
        while b:
            lock = str(requests.get(lin).json()['locked_by'])
            buyer = str(requests.get(lin).json()['purchaser'])
            if lock == 'None':
                webhook = DiscordWebhook(url=WB,content='<@397972596207124480> None. ID: {}'.format(market_id))
            elif lock == 'sourovafrin' and buyer == 'None':
                ra = float(requests.get('https://steemmonsters.com/settings').json()['sbd_price'])
                am = round(card_price / ra, 3)
                webhook = DiscordWebhook(url=WB,content='<@397972596207124480> I bough something. ID: {}'.format(market_id))
                webhook.execute()
                memoo = "sm_market_sale:" + market_id + ":sourovafrin"
                amm = round(am - am * 0.05, 3)
                acc.transfer(seller, amm, 'SBD', memoo)
                time.sleep(2)
                acc = Account("svirus",steem_instance=stm)
                inf = acc.get_balances()
                sbd = float(inf['available'][1])
                sbd = sbd - 1
                acc.transfer('sourovafrin', sbd, 'SBD', "Card is locked by sourovafrin. ID: {}".format(market_id))
                b = False
            else:
                inf = acc.get_balances()
                sbd = float(inf['available'][1])
                sbd = sbd - 1
                acc.transfer('sourovafrin', sbd, 'SBD', "Card is locked by {}. ID {}".format(lock, market_id))
                webhook = DiscordWebhook(url=WB, content='<@397972596207124480> {} bough something'.format(lock))
                webhook.execute()
                b = False
    except Exception as e:
        print("Error in send: {}".format(e))

    

def st():
    car_name_by_id = {"1": "Goblin Shaman",
                      "2": "Giant Roc",
                      "3": "Kobold Miner",
                      "4": "Fire Beetle",
                      "5": "Malric Inferno",
                      "6": "Serpentine Soldier",
                      "7": "Pit Ogre",
                      "8": "Cerberus",
                      "9": "Fire Demon",
                      "10": "Serpent of the Flame",
                      "11": "Elemental Phoenix",
                      "12": "Pirate Captain",
                      "13": "Spineback Turtle",
                      "14": "Crustacean King",
                      "15": "Sabre Shark",
                      "16": "Alric Stormbringer",
                      "17": "Medusa",
                      "18": "Water Elemental",
                      "19": "Frozen Soldier",
                      "20": "Mischievous Mermaid",
                      "21": "Naga Warrior",
                      "22": "Frost Giant",
                      "23": "Flesh Golem",
                      "24": "Goblin Sorcerer",
                      "25": "Rexxie",
                      "26": "Minotaur Warrior",
                      "27": "Lyanna Natura",
                      "28": "Earth Elemental",
                      "29": "Stone Golem",
                      "30": "Stonesplitter Orc",
                      "31": "Magi of the Forest",
                      "32": "Swamp Thing",
                      "33": "Spirit of the Forest",
                      "34": "Divine Healer",
                      "35": "Feral Spirit",
                      "36": "Silvershield Knight",
                      "37": "Silvershield Warrior",
                      "38": "Tyrus Paladium",
                      "39": "Peacebringer",
                      "40": "Silvershield Paladin",
                      "41": "Clay Golem",
                      "42": "Defender of Truth",
                      "43": "Air Elemental",
                      "44": "Angel of Light",
                      "45": "Animated Corpse",
                      "46": "Haunted Spider",
                      "47": "Skeleton Assassin",
                      "48": "Spineback Wolf",
                      "49": "Zintar Mortalis",
                      "50": "Haunted Spirit",
                      "51": "Twisted Jester",
                      "52": "Undead Priest",
                      "53": "Dark Enchantress",
                      "54": "Screaming Banshee",
                      "55": "Lord of Darkness",
                      "56": "Selenia Sky",
                      "57": "Lightning Dragon",
                      "58": "Chromatic Dragon",
                      "59": "Gold Dragon",
                      "60": "Peaceful Giant",
                      "61": "Grumpy Dwarf",
                      "62": "Elven Cutthroat",
                      "63": "Centaur",
                      "64": "Cocatrice",
                      "65": "Cyclops",
                      "66": "Enchanted Pixie",
                      "67": "Raging Impaler",
                      "68": "Magi Sphinx",
                      "69": "Hydra",
                      "70": "Talia Firestorm",
                      "71": "Xia Seachan",
                      "72": "Xander Foxwood",
                      "73": "Kiara Lightbringer",
                      "74": "Jarlax the Undead",
                      "75": "Dragon Whelp",
                      "76": "Royal Dragon Archer",
                      "77": "Shin-Lo",
                      "78": "Neb Seni",
                      "79": "Highland Archer",
                      "80": "Rusty Android",
                      "81": "Hobgoblin",
                      "82": "Lord Arianthus",
                      "83": "Sea Genie",
                      "84": "Divine Sorceress",
                      "85": "Mushroom Seer",
                      "86": "Vampire",
                      "87": "Flame Imp",
                      "88": "Daria Dragonscale",
                      "89": "Sacred Unicorn",
                      "90": "Wood Nymph",
                      "91": "Creeping Ooze",
                      "92": "Phantom Soldier",
                      "93": "Pirate Archer",
                      "94": "Naga Fire Wizard",
                      "95": "Brownie",
                      "96": "Silvershield Archers",
                      "97": "Goblin Mech",
                      "98": "Ruler of the Seas",
                      "99": "Skeletal Warrior",
                      "100": "Imp Bowman",
                      "101": "Crystal Werewolf",
                      "102": "Javelin Thrower",
                      "103": "Sea Monster",
                      "104": "Prismatic Energy",
                      "105": "Undead Minotaur",
                      "106": "Exploding Dwarf",
                      "107": "Manticore",
                      "108": "Black Dragon",
                      "109": "Crypt Mancer",
                      "110": "Plado Emberstorm",
                      "111": "Valnamor",
                      "112": "Prince Rennyn",
                      "113": "The Peakrider",
                      "118": "Armorsmith",
                      "119": "Silvershield Bard",
                      "120": "Goblin Chef",
                      "121": "Minotaur Warlord",
                      "122": "Electric Eels",
                      "123": "Mermaid Healer",
                      "124": "Undead Archer",
                      "125": "Corrupted Pegasus",
                      "126": "Molten Ogre",
                      "127": "Lord of Fire",
                      "128": "Enchanted Defender",
                      "129": "Dwarven Wizard",
                      "130": "Archmage Arius",
                      "114": "Delwyn Dragonscale",
                      "115": "Dragonling Bowman",
                      "116": "Fiendish Harpy",
                      "117": "Red Dragon"
                      }

    
    stm = Steem(node="https://steemd.minnowsupportproject.org/")
    chain = Blockchain(stm, "head")
    print("started sm")
    for detail in chain.stream(['custom_json']):
        try:
            if detail['id'] == 'sm_sell_cards':
                for i in ast.literal_eval(detail['json']):
                    res = requests.get("https://steemmonsters.com/cards/find?ids=" + i['cards'][0]).json()
                    for ii in res:
                        card_id = ii['uid']
                        seller = ii['player']
                        try:
                            market_id = ii['market_id']
                        except Exception as e:
                            break
                        card_number = str(ii['card_detail_id'])
                        is_gold = ii['gold']
                        edit = ii['edition']
                        try:
                            card_price = float(ii['buy_price'])
                        except Exception as e:
                            print("Breaking due to None. Seller: {}".format(seller))
                            break
                        try:
                            if card_number in di:
                                if card_price <= di[card_number]:
                                    time.sleep(4)
                                    t3 = Thread(target=send, args=(market_id, seller, card_price))
                                    t3.start()
                                else:
                                   pass
                        except Exception as e:
                            pass
                        if int(edit) == 0:
                            edition = "Alpha"
                        elif int(edit) == 1:
                            edition = "Beta"
                        elif int(edit) == 2:
                            edition = "Promo"
                        else:
                            edition = "Reward"
                        name = car_name_by_id[str(card_number)]
                        market_detail = requests.get('https://steemmonsters.com/market/for_sale_grouped').json()
                        for each in market_detail:
                            if str(each['card_detail_id']) == card_number and each['gold'] == is_gold and int(each['edition']) == int(edit):
                                second_min = float(each['low_price'])
                        percent = round(100 - (card_price / second_min * 100), 3)
                        per = 10
                        if percent > per:
                            if second_min > 0.06:
                                sbd_price = requests.get("https://steemmonsters.com/purchases/settings").json()['sbd_price']
                                sbd_send = round(card_price / sbd_price, 3)
                                message = """/....

**Card name**: {}
**Card id**: {}
**Price**: **{}**
**Cheaper**: **{}%**
**Second Lowest**: {}
**Seller**: {}
**Edition**: {}
**Gold**: {}
<@397972596207124480>

**Buy instant**: `..transfer {} sbd sm-market sm_market_purchase:{}`
**For admin only:** `..transfer {} sbd svirus sm_market_purchase:{}`
**Verify**: `..verify {}`

..../""".format(name, card_id, card_price, percent, second_min, seller, edition, is_gold, sbd_send, market_id, sbd_send, market_id, market_id)
                                webhook = DiscordWebhook(url=MU, content=message)
                                webhook.execute()
        except Exception as e:
            print("Error found: {}".format(e))


            


if __name__ == '__main__':
    #t1 = Thread(target=inn, args=())
    #t1.start()
    t2= Thread(target=st, args=())
    t2.start()
