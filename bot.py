from beem.steem import Steem
from beem.blockchain import Blockchain
from dhooks import Webhook, Embed
from beem.steemconnect import SteemConnect
import requests
import json
import os
import base64
import traceback
import asyncio
import time
from util import get_bcx, get_level, thumbnail_generator

WB = os.environ.get('WB')
MU = os.environ.get('MU')
AU = os.environ.get('AU')
MLU = os.environ.get('MLU')
UN = os.environ.get('UN')
FO = os.environ.get('FO')

ahook = Webhook(url=AU)
bhook = Webhook(url=MU)
mhook = Webhook(url=MLU)
ghook = Webhook(url=WB)
uhook = Webhook(url=UN)
fhook = Webhook(url=FO)


def send_message(card_detail_id, market_id, second_min, edition, is_gold, card_uid, seller, bcx, level, card_price, percent):
    if second_min > 0.05:
        r = requests.get("https://steemmonsters.com/cards/get_details").json()
        for i in r:
            if i['id'] == int(card_detail_id):
                name = i['name']
                break
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
            embed.set_title(f"Edition: {edition_txt}, Gold: {is_gold}, Bcx: {bcx}, Level: {level}\nPrice: {card_price}$, Cheaper: {percent}%, Second Lowest: {second_min}")
            embed.add_field(name=".", value=f"Commands:\n**STEEM**: `..transfer {steem_send} steem svirus {memo}`\n**SBD**: `..transfer {sbd_send} sbd svirus {memo}`\n\nSteemconnect:\n[{steem_send} STEEM]({steem_link})\n[{sbd_send} SBD]({sbd_link})\n[{dec_send} DEC]({final_dec})\n\n**Verify**: `..verify {market_id}`")
        else:
            one_card_price = round(card_price / bcx, 3)
            embed.set_thumbnail(thumbnail_link)
            embed.set_author(f"{name}\n{card_uid} by @{seller}")
            embed.set_title(f"Edition: {edition_txt}, Gold: {is_gold}, Bcx: {bcx}, Level: {level}\nPrice: {card_price}$, Per bcx: {one_card_price}$, Cheaper: {percent}%, Second Lowest: {second_min}")
            embed.add_field(name=".", value=f"Commands:\n**STEEM**: `..transfer {steem_send} steem svirus {memo}`\n**SBD**: `..transfer {sbd_send} sbd svirus {memo}`\n\nSteemconnect:\n[{steem_send} STEEM]({steem_link})\n[{sbd_send} SBD]({sbd_link})\n[{dec_send} DEC]({final_dec})\n\n**Verify**: `..verify {market_id}`")
        try:
            if percent > 40:
                fhook.send(embed=embed)
                fhook.close()
            elif bcx > 1:
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
            print(traceback.format_exc())


async def process(json_data, user_perm_posting, user_perm_active):
    await asyncio.sleep(17)
    try:
        for card in json_data:
            try:
                card_uid = card['cards'][0]
            except:
                card_uid = card
            response_json = requests.get(f"https://steemmonsters.com/cards/find?ids={card_uid}").json()[0]
            seller = response_json['player']
            if seller == user_perm_posting or seller == user_perm_active:
                for i in range(5):
                    try:
                        market_id = response_json['market_id']
                        purchaser = requests.get(f"https://steemmonsters.com/market/status?id={market_id}").json()['purchaser']
                        break
                    except:
                        response_json = requests.get(f"https://steemmonsters.com/cards/find?ids={card_uid}").json()[0]
                        time.sleep(1)
                if market_id is not None and purchaser is None:
                    card_price = float(response_json['buy_price'])
                    card_detail_id = str(response_json['card_detail_id'])
                    is_gold = bool(response_json['gold'])
                    edition = int(response_json['edition'])
                    rarity = int(response_json['details']['rarity'])
                    bcx = int(get_bcx(response_json))
                    level = get_level(edition, rarity, bcx, is_gold)
                    market_group_sale = requests.get('https://steemmonsters.com/market/for_sale_grouped').json()
                    for info in market_group_sale:
                        if str(info['card_detail_id']) == card_detail_id and bool(info['gold']) == is_gold and int(info['edition']) == int(edition):
                            next_price = float(info['low_price'])
                            if bcx > 1:
                                one_card_price = round(card_price / bcx, 3)
                                percent = round(100 - (one_card_price / next_price * 100), 2)
                            else:
                                percent = round(100 - (card_price / next_price * 100), 2)
                            if percent > 10:
                                send_message(card_detail_id, market_id, next_price, edition, is_gold, card_uid, seller, bcx, level, card_price, percent)
    except:
        print(traceback.format_exc())


async def stream():
    try:
        stm = Steem(node=["https://api.steemit.com", "https://steemd.minnowsupportproject.org", "https://anyx.io"])
        chain = Blockchain(stm, "head")
        for tx in chain.stream(['custom_json']):
            if tx['id'] == 'sm_sell_cards':
                user_perm_posting = ""
                user_perm_active = ""
                try:
                    user_perm_posting = tx['required_posting_auths'][0]
                except:
                    pass
                try:
                    user_perm_active = tx['required_auths'][0]
                except:
                    pass
                json_data = json.loads(tx['json'])
                loop.create_task(process(json_data, user_perm_posting, user_perm_active))
            elif tx['id'] == 'sm_update_price':
                market_id_list = json.loads(tx['json'])['ids']
                card_uid_dict = []
                for market_id in market_id_list:
                    time.sleep(2)
                    try:
                        response_json = requests.get(f"https://steemmonsters.com/market/status?id={market_id}").json()
                        card_uid = response_json['cards'][0]['uid']
                        card_uid_dict.append(card_uid)
                    except:
                        pass
                user_perm_posting = ""
                user_perm_active = ""
                try:
                    user_perm_posting = tx['required_posting_auths'][0]
                except:
                    pass
                try:
                    user_perm_active = tx['required_auths'][0]
                except:
                    pass
                loop.create_task(process(card_uid_dict, user_perm_posting, user_perm_active))
            await asyncio.sleep(0)
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    print("process started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream())
