from beem.steem import Steem
from beem.blockchain import Blockchain
from dhooks import Webhook, Embed
from beem.steemconnect import SteemConnect
import requests
import json
import os
import base64
from util import get_bcx, get_level, thumbnail_generator

WB = os.environ.get('WB')
MU = os.environ.get('MU')
AU = os.environ.get('AU')
MLU = os.environ.get('MLU')
UN = os.environ.get('UN')

ahook = Webhook(url=AU)
bhook = Webhook(url=MU)
mhook = Webhook(url=MLU)
ghook = Webhook(url=WB)
uhook = Webhook(url=UN)

card_dict = {'1': "Goblin Shaman",
'2': "Giant Roc",
'3': "Kobold Miner",
'4': "Fire Beetle",
'5': "Malric Inferno",
'6': "Serpentine Soldier",
'7': "Pit Ogre",
'8': "Cerberus",
'9': "Fire Demon",
'10': "Serpent of the Flame",
'11': "Elemental Phoenix",
'12': "Pirate Captain",
'13': "Spineback Turtle",
'14': "Crustacean King",
'15': "Sabre Shark",
'16': "Alric Stormbringer",
'17': "Medusa",
'18': "Water Elemental",
'19': "Frozen Soldier",
'20': "Mischievous Mermaid",
'21': "Naga Warrior",
'22': "Frost Giant",
'23': "Flesh Golem",
'24': "Goblin Sorcerer",
'25': "Rexxie",
'26': "Minotaur Warrior",
'27': "Lyanna Natura",
'28': "Earth Elemental",
'29': "Stone Golem",
'30': "Stonesplitter Orc",
'31': "Magi of the Forest",
'32': "Swamp Thing",
'33': "Spirit of the Forest",
'34': "Divine Healer",
'35': "Feral Spirit",
'36': "Silvershield Knight",
'37': "Silvershield Warrior",
'38': "Tyrus Paladium",
'39': "Peacebringer",
'40': "Silvershield Paladin",
'41': "Clay Golem",
'42': "Defender of Truth",
'43': "Air Elemental",
'44': "Angel of Light",
'45': "Animated Corpse",
'46': "Haunted Spider",
'47': "Skeleton Assassin",
'48': "Spineback Wolf",
'49': "Zintar Mortalis",
'50': "Haunted Spirit",
'51': "Twisted Jester",
'52': "Undead Priest",
'53': "Dark Enchantress",
'54': "Screaming Banshee",
'55': "Lord of Darkness",
'56': "Selenia Sky",
'57': "Lightning Dragon",
'58': "Chromatic Dragon",
'59': "Gold Dragon",
'60': "Peaceful Giant",
'61': "Grumpy Dwarf",
'62': "Elven Cutthroat",
'63': "Centaur",
'64': "Cocatrice",
'65': "Cyclops",
'66': "Enchanted Pixie",
'67': "Raging Impaler",
'68': "Magi Sphinx",
'69': "Hydra",
'70': "Talia Firestorm",
'71': "Xia Seachan",
'72': "Xander Foxwood",
'73': "Kiara Lightbringer",
'74': "Jarlax the Undead",
'75': "Dragon Whelp",
'76': "Royal Dragon Archer",
'77': "Shin-Lo",
'78': "Neb Seni",
'79': "Highland Archer",
'80': "Rusty Android",
'81': "Hobgoblin",
'82': "Lord Arianthus",
'83': "Sea Genie",
'84': "Divine Sorceress",
'85': "Mushroom Seer",
'86': "Vampire",
'87': "Flame Imp",
'88': "Daria Dragonscale",
'89': "Sacred Unicorn",
'90': "Wood Nymph",
'91': "Creeping Ooze",
'92': "Phantom Soldier",
'93': "Pirate Archer",
'94': "Naga Fire Wizard",
'95': "Brownie",
'96': "Silvershield Archers",
'97': "Goblin Mech",
'98': "Ruler of the Seas",
'99': "Skeletal Warrior",
'100': "Imp Bowman",
'101': "Crystal Werewolf",
'102': "Javelin Thrower",
'103': "Sea Monster",
'104': "Prismatic Energy",
'105': "Undead Minotaur",
'106': "Exploding Dwarf",
'107': "Manticore",
'108': "Black Dragon",
'109': "Crypt Mancer",
'110': "Plado Emberstorm",
'111': "Valnamor",
'112': "Prince Rennyn",
'113': "The Peakrider",
'114': "Delwyn Dragonscale",
'115': "Dragonling Bowman",
'116': "Fiendish Harpy",
'117': "Red Dragon",
'118': "Armorsmith",
'119': "Silvershield Bard",
'120': "Goblin Chef",
'121': "Minotaur Warlord",
'122': "Electric Eels",
'123': "Mermaid Healer",
'124': "Undead Archer",
'125': "Corrupted Pegasus",
'126': "Molten Ogre",
'127': "Lord of Fire",
'128': "Enchanted Defender",
'129': "Dwarven Wizard",
'130': "Archmage Arius",
'131': "Furious Chicken",
'132': "Fallen Specter",
'133': "Beetle Queen",
'134': "Naga Windmaster",
'135': "Maggots",
'136': "Cursed Slimeball",
'137': "Giant Scorpion",
'138': "Undead Badger",
'139': "Dark Astronomer",
'140': "Bone Golem",
'141': "Death Elemental",
'142': "Soulstorm",
'143': "Darkest Mage",
'144': "Dark Ha'on",
'145': "Contessa L'ament",
'146': "Cave Slug",
'147': "Crystal Jaguar",
'148': "Lone Boatman",
'149': "Herbalist",
'150': "Truthspeaker",
'151': "Luminous Eagle",
'152': "Shieldbearer",
'153': "Light Elemental",
'154': "Thunderbird",
'155': "High Priest Darius",
'156': "Mother Khala",
'157': "Kobold Bruiser",
'158': "Serpentine Spy",
'159': "Magma Troll",
'160': "Goblin Fireballer",
'161': "Fire Elemental",
'162': "Living Lava",
'163': "Spark Pixies",
'164': "Ferexia General",
'165': "Pyromaniac",
'166': "Magnor",
'167': "Pyre",
'168': "Feasting Seaweed",
'169': "Albatross",
'170': "Tortisian Fighter",
'171': "Sniping Narwhal",
'172': "Ice Pixie",
'173': "Giant Squid",
'174': "Serpent of Eld",
'175': "Coral Wraith",
'176': "Azmare Harpoonist",
'177': "Phantom of the Abyss",
'178': "Bortus",
'179': "Goblin Thief",
'180': "Failed Summoner",
'181': "Biceratops",
'182': "Orc Sergeant",
'183': "Khmer Princess",
'184': "Unicorn Mustang",
'185': "Child of the Forest",
'186': "Mitica Headhunter",
'187': "Sporcerer",
'188': "Kron the Undying",
'189': "Wizard of Eastwood",
'190': "Elven Defender",
'191': "Horny Toad",
'192': "Mantoid",
'193': "Parasitic Growth",
'194': "Elven Mystic",
'195': "Goblin Chariot",
'196': "Tower Griffin",
'197': "War Chaang",
'198': "Tortisian Chief",
'199': "Cornealus",
'200': "Camila Sungazer",
'201': "The Vigilator",
'202': "Scale Doctor",
'203': "Dragon Jumper",
'204': "Gloridax Magus",
'205': "Prince Julian",
'206': "Boogeyman",
'207': "Spirit Miner",
'208': "Battle Orca",}

def send_message(market_id, second_min, edition, name, is_gold, card_uid, seller, bcx, level, card_price, percent):
    if second_min > 0.05:
        if edition == 0:
            edition_txt = "Alpha"
        elif edition == 1:
            edition_txt = "Beta"
        elif edition == 2:
            edition_txt = "Promo"
        elif edition == 3:
            edition_txt = "Reward"
        else:
            edition_txt = "Untamed"
        price_info_json = requests.get("https://steemmonsters.com/settings").json()
        sbd_price = price_info_json['sbd_price'] - 0.02
        steem_price = price_info_json['steem_price'] - 0.01
        dec_price = price_info_json['dec_price']
        dec_send = round(card_price / dec_price, 3)
        sbd_send = round(card_price / sbd_price, 3)
        stmc_sbd = str(sbd_send) + " SBD"
        steem_send = round(card_price / steem_price, 3)
        stmc_steem = str(steem_send) + " STEEM"
        dec = """["custom_json",{"required_auths":["__signer"],"required_posting_auths":[],"id":"sm_market_purchase","json":"{\\"items\\":[\\"@\\"],\\"purchaser\\":\\"__signer\\",\\"market\\":\\"svirus\\"}"}]"""
        dec = dec.split("@")
        dec = dec[0] + market_id + dec[1]
        encoded_dec = base64.b64encode(bytes(dec, "utf-8"))
        string = encoded_dec.decode("utf-8")
        final_dec = f"https://beta.steemconnect.com/sign/op/{string.replace('=', '.')}?authority=active"
        memo = "sm_market_purchase:{}".format(market_id)
        stmconnect = SteemConnect()
        steem_link = stmconnect.create_hot_sign_url("transfer", {"to": "svirus", "amount": stmc_steem, "memo": memo})
        sbd_link = stmconnect.create_hot_sign_url("transfer", {"to": "svirus", "amount": stmc_sbd, "memo": memo})
        thumbnail_link = thumbnail_generator(edition, name, is_gold)
        embed = Embed(color=15105817, timestamp='now')
        if bcx == 1:
            embed.set_thumbnail(thumbnail_link)
            embed.set_author(f"{name}\n{card_uid} by @{seller}")
            embed.set_title(f"Edition: **{edition_txt}**, Gold: **{is_gold}**, Bcx: **{bcx}**, Level: **{level}**\nPrice: {card_price}$, Cheaper: {percent}%, Second Lowest: {second_min}")
            embed.add_field(name=f"**---------------------------**",
                            value=f"Command to purchase:\n**STEEM**: `..transfer {steem_send} steem svirus {memo}`\n**SBD**: `..transfer {sbd_send} sbd svirus {memo}`\n\nSteemconnect link to purchase:\n**STEEM**: [{steem_send} STEEM]({steem_link})\n**SBD**: [{sbd_send} SBD]({sbd_link})\n**DEC**: [{dec_send} DEC]({final_dec})\n\n**Verify**: `..verify {market_id}`")
        else:
            one_card_price = round(card_price / bcx, 3)
            embed.set_author(f"{name}\n{card_uid} by @{seller}")
            embed.set_title(f"Edition: **{edition_txt}**, Gold: **{is_gold}**, Bcx: **{bcx}**, Level: **{level}**\nPrice: {card_price}$, Per bcx price: {one_card_price}$, Cheaper by single bcx: {percent}%, Second Lowest by single bcx: {second_min}")
            embed.add_field(name=f"**---------------------------**",
                            value=f"Command to purchase:\n**STEEM**: `..transfer {steem_send} steem svirus {memo}`\n**SBD**: `..transfer {sbd_send} sbd svirus {memo}`\n\nSteemconnect link to purchase:\n**STEEM**: [{steem_send} STEEM]({steem_link})\n**SBD**: [{sbd_send} SBD]({sbd_link})\n**DEC**: [{dec_send} DEC]({final_dec})\n\n**Verify**: `..verify {market_id}`")
        try:
            if bcx > 1:
                mhook.send(embed=embed)
                mhook.close()
            elif is_gold is True:
                ghook.send(embed=embed)
                ghook.close()
            elif edition == 0:
                ahook.send(embed=embed)
                ahook.close()
            elif edition == 4:
                uhook.send(embed=embed)
                uhook.close()
            else:
                bhook.send(embed=embed)
                bhook.close()
        except:
            pass


def process(json_data, user_perm_posting, user_perm_active):
    for card in json_data:
        try:
            card_uid = card['cards'][0]
        except:
            card_uid = card
        response_json = requests.get(f"https://steemmonsters.com/cards/find?ids={card_uid}").json()[0]
        seller = response_json['player']
        if seller == user_perm_posting or seller == user_perm_active:
            market_id = response_json['market_id']
            if market_id is not None:
                card_price = float(response_json['buy_price'])
                card_detail_id = str(response_json['card_detail_id'])
                is_gold = bool(response_json['gold'])
                edition = int(response_json['edition'])
                rarity = int(response_json['details']['rarity'])
                name = card_dict[card_detail_id]
                bcx = int(get_bcx(response_json))
                level = get_level(edition, rarity, bcx, is_gold)
                market_group_sale = requests.get('https://steemmonsters.com/market/for_sale_grouped').json()

                for info in market_group_sale:
                    if str(info['card_detail_id']) == card_detail_id and info['gold'] == is_gold and int(
                            info['edition']) == int(edition):
                        next_price = float(info['low_price'])
                percent = round(100 - (card_price / next_price * 100), 2)
                if percent > 10:
                    send_message(market_id, next_price, edition, name, is_gold, card_uid, seller, bcx, level, card_price, percent)

def stream():
    stm = Steem(node=["https://api.steemit.com", "https://steemd.minnowsupportproject.org", "https://anyx.io"])
    chain = Blockchain(stm, "head")
    for tx in chain.stream(['custom_json']):
        if tx['id'] == 'sm_sell_cards':
            user_perm_posting = ""
            user_perm_active = ""
            try:
                user_perm_posting = tx['required_posting_auths'][0]
                user_perm_active = tx['required_auths'][0]
            except:
                pass
            json_data = json.loads(tx['json'])
            process(json_data, user_perm_posting, user_perm_active)

        elif tx['id'] == 'sm_update_price':
            market_id_list = json.loads(tx['json'])['ids']
            card_uid_dict = []
            for market_id in market_id_list:
                response_json = requests.get(f"https://steemmonsters.com/market/status?id={market_id}").json()
                try:
                    card_uid = response_json['cards'][0]['uid']
                    card_uid_dict.append(card_uid)
                except KeyError:
                    pass
            user_perm_posting = ""
            user_perm_active = ""
            try:
                user_perm_posting = tx['required_posting_auths'][0]
                user_perm_active = tx['required_auths'][0]
            except:
                pass
            process(card_uid_dict, user_perm_posting, user_perm_active)

if __name__ == '__main__':
    print("process started")
    stream()
