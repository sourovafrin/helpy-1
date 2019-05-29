from beem.steem import Steem
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


def inn():
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
}


stm = Steem()
chain = Blockchain(stm,"head")
print("started steem as well")
for detail in chain.stream(['custom_json']):
    if detail['id'] == 'sm_sell_cards':
        for i in ast.literal_eval(detail['json']):
            for ii in requests.get("https://steemmonsters.com/cards/find?ids=" + i['cards'][0]).json():
                card_id = ii['uid']
                seller = ii['player']
                market_id = ii['market_id']
                card_number = ii['card_detail_id']
                is_gold = ii['gold']
                edit =  ii['edition']
                if int(edit) == 0:
                    edition = "Alpha"
                elif int(edit) == 1:
                    edition = "Beta"
                elif int(edit) == 2:
                    edition = "Promo"
                else:
                    edition = "Reward"
                card_price = float(ii['buy_price'])
                name = car_name_by_id[str(card_number)]
                cooldown = "False" if ii['last_used_block'] == 'null' else "True"
                market_detail = requests.get('https://steemmonsters.com/market/for_sale_by_card?card_detail_id={}&gold={}&edition={}'.format(card_number, is_gold, edit)).json()
                price_dict = []
                for each in market_detail:
                    if each != market_id:
                        price_dict.append(each['buy_price'])
                second_min = float(min(price_dict))
                percent = round(100 - (card_price / second_min * 100), 3)
                if second_min > card_price:
                    if card_price < 0.5:
                        per = 25
                    elif card_price < 2:
                        per = 20
                    else:
                        per = 15
                else:
                    break
                if percent > per:
                    sbd_price = requests.get("https://steemmonsters.com/purchases/settings").json()['sbd_price']
                    sbd_send = round(card_price/sbd_price, 3)
                    message = """.
                    
**Card name**: {}
**Card id**: {}
**Price**: **{}**
**Second Lowest**: {}
**Cheaper**: **{}%**
**Seller**: {}
**Edition**: {}
**Gold**: {}
**Cooldown**: {}
                    
**Buy instant**: `..transfer {} sbd sm-market sm_market_purchase:{}:sourovafrin`

. 
                    """.format(name, card_id, card_price, second_min, percent, seller, edition, is_gold, cooldown, sbd_send, market_id)
                    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/583245496546623489/AIQUHD2eRwtlR9ntw3Mpl8qbn3q85EQU3qQBIoHFBaZrbVK_iM772FAUspQ6oxk3FyP_',content=message)
                    webhook.execute()


            


if __name__ == '__main__':
    t1 = Thread(target=inn, args=())
    t1.start()
    t2= Thread(target=st, args=())
    t2.start()
