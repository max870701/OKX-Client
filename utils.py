import hmac
import base64
import json
import requests
from datetime import datetime, timezone 

import consts as c

def get_timestamp():
    request_path = f"{c.API_URL}{c.SERVER_TIMESTAMP_URL}"
    response = requests.get(request_path)
    if response.status_code == 200:
        ts = datetime.fromtimestamp(int(response.json()['data'][0]['ts']) / 1000.0, tz=timezone.utc)
        return ts.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    else:
        return ""

def sign(secret_key, timestamp, method, request_path, body=''):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = timestamp + method + request_path + body
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)

def request(api_key, secret_key, passphrase, method, request_path, params=None):
    body = ''
    if method == c.GET:
        if params:
            request_path += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
    else:
        if params:
            body = json.dumps(params)

    url = c.API_URL + request_path
    
    timestamp = get_timestamp()
    sign_str = sign(secret_key, timestamp, method, request_path, body)
    
    headers = {
        c.OK_ACCESS_KEY: api_key,
        c.OK_ACCESS_SIGN: sign_str,
        c.OK_ACCESS_TIMESTAMP: timestamp,
        c.OK_ACCESS_PASSPHRASE: passphrase,
        c.CONTENT_TYPE: c.APPLICATION_JSON
    }
    
    response = requests.request(method, url, headers=headers, data=body)
    return response.json()

def generate_tp_sl_params(tp_price='', tp_trigger_price='', tp_trigger_price_type='',
                          sl_price='', sl_trigger_price='', sl_trigger_price_type=''):
    attachAlgoOrds = {}
    if tp_price:
        attachAlgoOrds['tpOrdPx'] = tp_price
    if tp_trigger_price:
        attachAlgoOrds['tpTriggerPx'] = tp_trigger_price
    if tp_trigger_price_type:
        attachAlgoOrds['tpTriggerPxType'] = tp_trigger_price_type
    if sl_price:
        attachAlgoOrds['slOrdPx'] = sl_price
    if sl_trigger_price:
        attachAlgoOrds['slTriggerPx'] = sl_trigger_price
    if sl_trigger_price_type:
        attachAlgoOrds['slTriggerPxType'] = sl_trigger_price_type
    
    return attachAlgoOrds

def generate_future_tdmode_ccy(leverage_type: str, symbol: str):
    if leverage_type == c.MARGIN_ISOLATED:
        tdMode = c.MARGIN_ISOLATED
        ccy = ""
    elif leverage_type == c.MARGIN_CROSS:
        tdMode = c.MARGIN_CROSS
        ccy = symbol.split("-")[1]
    else:
        raise ValueError(f"Invalid leverage type: {leverage_type}")
    
    return tdMode, ccy

def generate_price(order_type: str, price: str):
    if order_type == c.MARKET:
        return None
    elif order_type == c.LIMIT:
        if not price:
            raise ValueError("Price must be provided for LIMIT orders.")
        return price
    else:
        return price
