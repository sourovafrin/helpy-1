def get_level(edition, rarity, bcx, gold):
    if edition == 1 or edition == 2 or edition == 3 or edition == 4:
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
    if details['edition'] == 4:
        return details['xp']
    elif details['gold']:
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
    name = name.title()
    if is_gold is True:
        is_gold == 1
    else:
        is_gold == 0
    try:
        name_parts = name.split(" ")
        lent = len(name_parts)
        if edition == 1 or edition == 3:
            check = 0
            link = "https://s3.amazonaws.com/steemmonsters/cards_beta/"
            for i in name_parts:
                check += 1
                link += i
                if check == lent:
                    if is_gold == 1:
                        link += "_gold.png"
                    else:
                        link += ".png"
                else:
                    link += "%20"
            return link
        elif edition == 0 or edition == 2:
            check = 0
            link = "https://s3.amazonaws.com/steemmonsters/cards_v2.2/"
            for i in name_parts:
                check += 1
                link += i
                if check == lent:
                    if is_gold == 1:
                        link += "_gold.png"
                    else:
                        link += ".png"
                else:
                    link += "%20"
            return link
        else:
            check = 0
            link = "https://s3.amazonaws.com/steemmonsters/cards_untamed/"
            for i in name_parts:
                check += 1
                link += i
                if check == lent:
                    if is_gold == 1:
                        link += "_gold.png"
                    else:
                        link += ".png"
                else:
                    link += "%20"
            return link
    except Exception as e:
        print("Error in thumbnail generation: {}.\nCard edition: {} and Card name: {}".format(e,edition,name))


def get_table(iterable, header):
    max_len = [len(x) for x in header]
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        for index, col in enumerate(row):
            if max_len[index] < len(str(col)):
                max_len[index] = len(str(col))
    output = ('-' * (sum(max_len) + 1)) + '\n'
    output += '|' + ''.join([h + ' ' * (l - len(h)) + '|' for h, l in zip(header, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        output += '|' + ''.join([str(c) + ' ' * (l - len(str(c))) + '|' for c, l in zip(row, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    return output
