import requests
import json
import datetime,pytz

with open('config.json') as json_file:
    token = json.load(json_file)['LINE_NOTIFY_TOKEN']

def time_now():
    tz = pytz.timezone('Asia/Bangkok')
    return str(datetime.datetime.now(tz))[:17]

def get_price():
    symbol = {'bitcoin':'BTC','binancecoin':'BNB','ethereum':'ETH','alpha-finance':'ALPHA','pancakeswap-token':'CAKE','cardano':'ADA','solana':'SOL','fantom':'FTM','avalanche-2':'AVAX','matic-network':'MATIC','vechain':'VET'}
    currency = 'usd'
    t = requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+'%2C'.join(symbol.keys())+'&vs_currencies='+currency).text
    t = json.loads(t)
    return '\n'.join(sorted([ symbol[str(k)]+ ' : ' + str(v['usd'])  for k,v in t.items()]))

def send_notify(text):
    msg_out = '\n'+ time_now()+'🚀 \n' + text
    url = 'https://notify-api.line.me/api/notify'
    headers = {
                'content-type':
                'application/x-www-form-urlencoded',
                'Authorization':'Bearer '+ token
            }
    r = requests.post(url, headers=headers , data = {'message': msg_out})
    print(r.text)

def crypto_alert(request):
    try:
        send_notify(get_price())
        return (json.dumps({'status':"/ok"}),200)
    except Exception as e:
        err = "Error: {}".format(e)
        res={'status',err}
        //send_notify(err)
        return (json.dumps(res),400)

//crypto_alert()


