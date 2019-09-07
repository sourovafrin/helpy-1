from beem.steem import Steem
from beem.blockchain import Blockchain
from datetime import timedelta
from dhooks import Webhook, Embed
from beem.steemconnect import SteemConnect
import requests
import json
import time
import os
import asyncio

CH = os.environ.get('CH')
SV = os.environ.get('SV')
MD = os.environ.get('MD')
AF = os.environ.get('AF')
WB = os.environ.get('WB')
MU = os.environ.get('MU')
AU = os.environ.get('AU')
MLU = os.environ.get('MLU')


ahook = Webhook(url= AU)
bhook = Webhook(url= MU)
mhook = Webhook(url= MLU)
ghook = Webhook(url= WB)


def get_level(edition, rarity, bcx, gold):
    if edition == 1 or edition == 2 or edition == 3:
        if rarity == 1:
            if gold is False:
                if bcx < 3:
                    return 1
                elif bcx < 5:
                    return 2
                elif bcx < 12:
                    return 3
                elif bcx < 25:
                    return 4
                elif bcx < 52:
                    return 5
                elif bcx < 105:
                    return 6
                elif bcx < 172:
                    return 7
                elif bcx < 305:
                    return 8
                elif bcx < 505:
                    return 9
                else:
                    return 10
            else:
                if bcx < 2:
                    return 4
                elif bcx < 4:
                    return 5
                elif bcx < 8:
                    return 6
                elif bcx < 13:
                    return 7
                elif bcx < 23:
                    return 8
                elif bcx < 38:
                    return 9
                else:
                    return 10
        elif rarity == 2:
            if gold is False:
                if bcx < 3:
                    return 1
                if bcx < 5:
                    return 2
                if bcx < 11:
                    return 3
                if bcx < 21:
                    return 4
                if bcx < 35:
                    return 5
                if bcx < 61:
                    return 6
                if bcx < 115:
                    return 7
                else:
                    return 8
            else:
                if bcx < 2:
                    return 3
                if bcx < 4:
                    return 4
                if bcx < 7:
                    return 5
                if bcx < 12:
                    return 6
                if bcx < 22:
                    return 7
                else:
                    return 8
        elif rarity == 3:
            if gold is False:
                if bcx < 3:
                    return 1
                if bcx < 6:
                    return 2
                if bcx < 11:
                    return 3
                if bcx < 23:
                    return 4
                if bcx < 46:
                    return 5
                else:
                    return 6
            else:
                if bcx < 3:
                    return 3
                if bcx < 5:
                    return 4
                if bcx < 10:
                    return 5
                else:
                    return 6
        elif rarity == 4:
            if gold is False:
                if bcx < 3:
                    return 1
                if bcx < 5:
                    return 2
                if bcx < 11:
                    return 3
                else:
                    return 4
            else:
                if bcx < 2:
                    return 2
                if bcx < 4:
                    return 3
                else:
                    return 4
    elif edition == 0:
        if rarity == 1:
            if gold is False:
                if bcx < 2:
                    return 1
                elif bcx < 4:
                    return 2
                elif bcx < 9:
                    return 3
                elif bcx < 19:
                    return 4
                elif bcx < 39:
                    return 5
                elif bcx < 79:
                    return 6
                elif bcx < 129:
                    return 7
                elif bcx < 229:
                    return 8
                elif bcx < 379:
                    return 9
                else:
                    return 10
            else:
                if bcx < 2:
                    return 4
                elif bcx < 4:
                    return 5
                elif bcx < 7:
                    return 6
                elif bcx < 11:
                    return 7
                elif bcx < 19:
                    return 8
                elif bcx < 31:
                    return 9
                else:
                    return 10
        if rarity == 2:
            if gold is False:
                if bcx < 2:
                    return 1
                if bcx < 4:
                    return 2
                if bcx < 8:
                    return 3
                if bcx < 16:
                    return 4
                if bcx < 26:
                    return 5
                if bcx < 46:
                    return 6
                if bcx < 86:
                    return 7
                else:
                    return 8
            else:
                if bcx < 2:
                    return 3
                if bcx < 3:
                    return 4
                if bcx < 5:
                    return 5
                if bcx < 9:
                    return 6
                if bcx < 17:
                    return 7
                else:
                    return 8
        elif rarity == 3:
            if gold is False:
                if bcx < 2:
                    return 1
                if bcx < 4:
                    return 2
                if bcx < 8:
                    return 3
                if bcx < 16:
                    return 4
                if bcx < 32:
                    return 5
                else:
                    return 6
            else:
                if bcx < 2:
                    return 3
                if bcx < 4:
                    return 4
                if bcx < 8:
                    return 5
                else:
                    return 6
        elif rarity == 4:
            if gold is False:
                if bcx < 2:
                    return 1
                if bcx < 4:
                    return 2
                if bcx < 8:
                    return 3
                else:
                    return 4
            else:
                if bcx < 2:
                    return 2
                if bcx < 3:
                    return 3
                else:
                    return 4


def get_bcx(details):
    bcx_dict = {0: {1: 20, 2: 100, 3: 250, 4: 1000}, 1: {1: 15, 2: 75, 3: 175, 4: 750}}
    gold_bcx_dict = {0: {1: 250, 2: 500, 3: 1000, 4: 2500}, 1: {1: 200, 2: 400, 3: 800, 4: 2000}}
    if details['gold']:
        if details['edition'] == 1 or details['edition'] == 3:
            return details['xp'] / gold_bcx_dict[1][details['details']['rarity']]
        if details['edition'] == 0:
            return details['xp'] / gold_bcx_dict[0][details['details']['rarity']]
        if details['edition'] == 2 and details['card_detail_id'] > 100:
            return details['xp'] / gold_bcx_dict[1][details['details']['rarity']]
        if details['edition'] == 2 and details['card_detail_id'] < 100:
            return details['xp'] / gold_bcx_dict[0][details['details']['rarity']]
    if details['edition'] == 1 or details['edition'] == 3:
        return details['xp'] / bcx_dict[1][details['details']['rarity']] + 1
    if details['edition'] == 0:
        return details['xp'] / bcx_dict[0][details['details']['rarity']] + 1
    if details['edition'] == 2 and details['card_detail_id'] > 100:
        return details['xp'] / bcx_dict[1][details['details']['rarity']] + 1
    if details['edition'] == 2 and details['card_detail_id'] < 100:
        return details['xp'] / bcx_dict[0][details['details']['rarity']] + 1


def thumbnail_generator(edition, name, is_gold):
    try:
        name_parts = name.split(" ")
        lent = len(name_parts)
        if edition == "Beta" or edition == "Reward":
            check = 0
            link = "https://s3.amazonaws.com/steemmonsters/cards_beta/"
            for i in name_parts:
                check += 1
                link += i
                if check == lent:
                    if is_gold is True:
                        link += "_gold.png"
                    else:
                        link += ".png"
                else:
                    link += "%20"
            return link
        else:
            check = 0
            link = "https://s3.amazonaws.com/steemmonsters/cards_v2.2/"
            for i in name_parts:
                check += 1
                link += i
                if check == lent:
                    if is_gold is True:
                        link += "_gold.png"
                    else:
                        link += ".png"
                else:
                    link += "%20"
            return link
    except Exception as e:
        print("Error in thumbnail generation: {}.\nCard edition: {} and Card name: {}".format(e, edition, name))


async def wait(market_id, second_min, edition, name, is_gold, card_id, seller, bcx, level, card_price, percent, edit):
    await asyncio.sleep(13)
    linkk = "https://steemmonsters.com/market/status?id=" + market_id
    ress = requests.get(linkk).json()
    buyer = ress['purchaser']
    print("Purchaser: {}".format(buyer))
    if second_min > 0.06 and buyer is None:
        if bcx == 1:
            price_resp = requests.get("https://steemmonsters.com/purchases/settings").json()
            sbd_price = price_resp['sbd_price']
            steem_price = price_resp['steem_price']
            sbd_send = round(card_price / sbd_price, 3)
            stmc_sbd = str(sbd_send) + " SBD"
            steem_send = round(card_price / steem_price, 3)
            stmc_steem = str(steem_send) + " STEEM"
            memo = "sm_market_purchase:{}".format(market_id)
            stmconnect = SteemConnect()
            steem_link = stmconnect.create_hot_sign_url("transfer", {"to": "svirus",
                                                                     "amount": stmc_steem,
                                                                     "memo": memo})
            sbd_link = stmconnect.create_hot_sign_url("transfer",
                                                      {"to": "svirus", "amount": stmc_sbd,
                                                       "memo": memo})
            thumbnail_link = thumbnail_generator(edition, name, is_gold)
            embed = Embed(color=15105817)
            embed.add_field(name="**{}\n{} by @{}**".format(name, card_id, seller),
                            value="Edition: **{}**,  Gold: **{}**, Bcx: **{}**, Level: **{}**\nPrice: **{}$**,  Cheaper: **{}%**,  Second Lowest: {}$".format(
                                edition, is_gold, bcx, level, card_price, percent,
                                second_min))
            embed.set_thumbnail(thumbnail_link)
            embed.add_field(name="**Commands to buy(3% cashback)**",
                            value="**STEEM**: `..transfer {} steem svirus {}`\n\n**SBD**: `..transfer {} sbd svirus {}`".format(
                                steem_send, memo, sbd_send, memo))
            embed.add_field(name="**Steemconnect link to buy(3% cashback)**",
                            value="**STEEM**: {}\n\n**SBD**: {}".format(steem_link,
                                                                        sbd_link))
            embed.add_field(name="**Verification**",
                            value="**Verify**: `..verify {}`".format(market_id))
        else:
            price_resp = requests.get("https://steemmonsters.com/purchases/settings").json()
            sbd_price = price_resp['sbd_price'] - 0.02
            steem_price = price_resp['steem_price'] - 0.01
            sbd_send = round(card_price / sbd_price, 3)
            stmc_sbd = str(sbd_send) + " SBD"
            steem_send = round(card_price / steem_price, 3)
            stmc_steem = str(steem_send) + " STEEM"
            memo = "sm_market_purchase:{}".format(market_id)
            stmconnect = SteemConnect()
            steem_link = stmconnect.create_hot_sign_url("transfer",
                                                        {"to": "svirus", "amount": stmc_steem,
                                                         "memo": memo})
            sbd_link = stmconnect.create_hot_sign_url("transfer",
                                                      {"to": "svirus", "amount": stmc_sbd,
                                                       "memo": memo})
            thumbnail_link = thumbnail_generator(edition, name, is_gold)
            embed = Embed(color=15105817)
            embed.add_field(name="**{}\n{} by @{}**".format(name, card_id, seller),
                            value="Edition: **{}**,  Gold: **{}**, Bcx: **{}**, Level: **{}**\nPrice: **{}$**, Per bcx price: **{}$**, Second lowest by single bcx: **{}$**\nCheaper by single bcx: **{}%**".format(
                                edition, is_gold, bcx, level, card_price, one_card_price,
                                second_mi, one_percent))
            embed.set_thumbnail(thumbnail_link)
            embed.add_field(name="**Commands to buy(3% cashback)**",
                            value="**STEEM**: `..transfer {} steem svirus {}`\n\n**SBD**: `..transfer {} sbd svirus {}`".format(
                                steem_send, memo, sbd_send, memo))
            embed.add_field(name="**Steemconnect link to buy(3% cashback)**",
                            value="**STEEM**: {}\n\n**SBD**: {}".format(steem_link, sbd_link))
            embed.add_field(name="**Verification**",
                            value="**Verify**: `..verify {}`".format(market_id))
        if is_gold == True:
            ghook.send(embed=embed)
            ghook.close()
        elif bcx > 1:
            mhook.send(embed=embed)
            mhook.close()
        elif edit == 0:
            ahook.send(embed=embed)
            ahook.close()
        else:
            bhook.send(embed=embed)
            bhook.close()


async def st():
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

    stm = Steem(node=[ "https://api.steemit.com", "https://steemd.minnowsupportproject.org", "https://anyx.io"])
    chain = Blockchain(stm, "head")
    print("started sm")
    for detail in chain.stream(['custom_json']):
        if detail['id'] == 'sm_sell_cards':
            trans = ""
            transactor = ""
            try:
                transactor = detail['required_posting_auths'][0]
                trans = detail['required_auths'][0]
            except:
                pass
            listtt = json.loads(detail['json'])
            await asyncio.sleep(5)
            for i in listtt:
                cardddd = i['cards'][0]
                linkk = "https://steemmonsters.com/cards/find?ids=" + cardddd
                res = requests.get(linkk).json()
                res = res[0]
                seller = res['player']
                success = 0
                if seller == transactor:
                    success = 1
                elif seller == trans:
                    success = 1
                if success == 1:
                    card_id = res['uid']
                    market_id = res['market_id']
                    if market_id is not None:
                        card_price = float(res['buy_price'])
                        card_number = str(res['card_detail_id'])
                        is_gold = bool(res['gold'])
                        edit = int(res['edition'])
                        rarity = int(res['details']['rarity'])
                        name = car_name_by_id[str(card_number)]
                        if edit == 0:
                            edition = "Alpha"
                        elif edit == 1:
                            edition = "Beta"
                        elif edit == 2:
                            edition = "Promo"
                        else:
                            edition = "Reward"
                        bcx = int(get_bcx(res))
                        level = get_level(edit, rarity, bcx, is_gold)
                        market_detail = requests.get('https://steemmonsters.com/market/for_sale_grouped').json()
                        if bcx == 1:
                            for each in market_detail:
                                if str(each['card_detail_id']) == card_number and each['gold'] == is_gold and int(each['edition']) == int(edit):
                                    second_min = float(each['low_price'])
                            percent = round(100 - (card_price / second_min * 100), 2)
                            if percent > 10:
                                loop.create_task(wait(market_id, second_min, edition, name, is_gold, card_id, seller, bcx, level, card_price, percent, edit))
                        else:
                            for each in market_detail:
                                if str(each['card_detail_id']) == card_number and each['gold'] == is_gold and int(each['edition']) == int(edit):
                                    second_mi = float(each['low_price'])
                            one_card_price = round(card_price / bcx, 3)
                            one_percent = round(100 - (one_card_price / second_mi * 100), 2)
                            if one_percent > 10:
                                loop.create_task(wait(market_id, second_mi, edition, name, is_gold, card_id, seller, bcx, level, card_price, one_percent, edit))
        elif detail['id'] == "sm_update_price":
            info = json.loads(detail['json'])
            ids = info['ids']
            cards = []
            for market_id in ids:
                link = "https://steemmonsters.com/market/status?id=" + market_id
                res = requests.get(link).json()
                try:
                    card_uid = str(res['cards'][0]['uid'])
                    cards.append(card_uid)
                except KeyError:
                    pass
            trans = ""
            transactor = ""
            try:
                transactor = detail['required_posting_auths'][0]
                trans = detail['required_auths'][0]
            except:
                pass
            await asyncio.sleep(5)
            for i in cards:
                cardddd = i
                linkk = "https://steemmonsters.com/cards/find?ids=" + cardddd
                res = requests.get(linkk).json()
                res = res[0]
                seller = res['player']
                success = 0
                if seller == transactor:
                    success = 1
                elif seller == trans:
                    success = 1
                if success == 1:
                    card_id = res['uid']
                    market_id = res['market_id']
                    if market_id is not None:
                        card_price = float(res['buy_price'])
                        card_number = str(res['card_detail_id'])
                        is_gold = bool(res['gold'])
                        edit = int(res['edition'])
                        rarity = int(res['details']['rarity'])
                        name = car_name_by_id[str(card_number)]
                        if edit == 0:
                            edition = "Alpha"
                        elif edit == 1:
                            edition = "Beta"
                        elif edit == 2:
                            edition = "Promo"
                        else:
                            edition = "Reward"
                        bcx = int(get_bcx(res))
                        level = get_level(edit, rarity, bcx, is_gold)
                        market_detail = requests.get('https://steemmonsters.com/market/for_sale_grouped').json()
                        if bcx == 1:
                            for each in market_detail:
                                if str(each['card_detail_id']) == card_number and each['gold'] == is_gold and int(
                                        each['edition']) == int(edit):
                                    second_min = float(each['low_price'])
                            percent = round(100 - (card_price / second_min * 100), 2)
                            if percent > 10:
                                loop.create_task(wait(market_id, second_min, edition, name, is_gold, card_id, seller, bcx, level,card_price, percent, edit))
                        else:
                            for each in market_detail:
                                if str(each['card_detail_id']) == card_number and each['gold'] == is_gold and int(
                                        each['edition']) == int(edit):
                                    second_mi = float(each['low_price'])
                            one_card_price = round(card_price / bcx, 3)
                            one_percent = round(100 - (one_card_price / second_mi * 100), 2)
                            if one_percent > 10:
                                loop.create_task(wait(market_id, second_mi, edition, name, is_gold, card_id, seller, bcx, level,card_price, one_percent, edit))

        await asyncio.sleep(0)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(st())
