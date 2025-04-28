'''
    get data from amazon product page

    queries generated from chatgpt
'''


class Rule:
    def __init__(self, field, qstr, single=True):
        self.field = field
        self.qstr = qstr
        self.single = single


def amazon_scraper(sb):
    rules = [
        Rule("title", '#productTitle'),
        Rule("price", '#corePriceDisplay_desktop_feature_div .aok-offscreen'),
        Rule("stars", '#acrPopover .a-icon-alt'),
        Rule("bought_past_month", '#social-proofing-faceout-title-tk_bought')
    ]

    data = dict()
    for rule in rules:
        try:
            if rule.single:
                tag = sb.cdp.select(rule.qstr)
            else:
                tag = sb.cdp.select_all(rule.qstr)

            data[rule.field] = tag.text

        except Exception as error:
            print(f"Couldn't get data for: {rule.field}")
            pass

    # print(str(data))
    return data
