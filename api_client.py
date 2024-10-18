import consts as c
import utils

class OkxClient:
    def __init__(self, api_key: str, secret_key: str, passphrase: str):
        super().__init__(api_key, secret_key)
        self._passphrase = passphrase

    def _request(self, method, request_path, params=None):
        return utils.request(self._api_key, self._secret_key, self._passphrase, method, request_path, params)

    """
    Account Info
    """
    def get_account_config(self):
        return self._request(c.GET, c.ACCOUNT_CONFIG)

    def get_account_info(self):
        return self._request(c.GET, c.ACCOUNT_INFO)

    def get_position_info(self):
        return self._request(c.GET, c.POSITION_INFO)

    def get_position_history(self):
        return self._request(c.GET, c.POSITIONS_HISTORY)
    
    def get_position_risk(self):
        return self._request(c.GET, c.POSITION_RISK)
    
    def get_leverage_info(self, symbol: str, mgnMode: str):
        params = {
            "instId": symbol,
            "mgnMode": mgnMode
        }
        return self._request(c.GET, c.GET_LEVERAGE, params)
    
    def set_position_mode(self, posMode: str):
        params = {
            "posMode": posMode
        }
        return self._request(c.POST, c.POSITION_MODE, params)
    
    def set_leverage(self, instId: str, lever: str, mgnMode: str):
        params = {
            "instId": instId,
            "lever": lever,
            "mgnMode": mgnMode,
        }
        return self._request(c.POST, c.SET_LEVERAGE, params)

    """
    Trade
    """
    def place_order(self, instId, tdMode, side, ordType, sz, ccy='', clOrdId='', tag='', posSide='', px='',
                    reduceOnly='', tgtCcy='', tpTriggerPx='', tpOrdPx='', slTriggerPx='', slOrdPx='',
                    tpTriggerPxType='', slTriggerPxType='', stpMode='', attachAlgoOrds=None):
        params = {'instId': instId, 'tdMode': tdMode, 'side': side, 'ordType': ordType, 'sz': sz, 'ccy': ccy,
                  'clOrdId': clOrdId, 'tag': tag, 'posSide': posSide, 'px': px, 'reduceOnly': reduceOnly,
                  'tgtCcy': tgtCcy, 'tpTriggerPx': tpTriggerPx, 'tpOrdPx': tpOrdPx, 'slTriggerPx': slTriggerPx,
                  'slOrdPx': slOrdPx, 'tpTriggerPxType': tpTriggerPxType, 'slTriggerPxType': slTriggerPxType,
                  'stpMode': stpMode, 'attachAlgoOrds': attachAlgoOrds}
        return self._request(c.POST, c.PLACE_ORDER, params)

    def cancel_order(self, symbol: str, order_id: str = ''):
        params = {
            'instId': symbol,
            'ordId': order_id
        }
        return self._request(c.POST, c.CANCEL_ORDER, params)

    def place_future_order(
            self, leverage_type: str, symbol: str, quantity: str, side: str, order_type: str, price: str = '', tp_price: str = '',
            tp_trigger_price: str = '', tp_trigger_price_type: str = '', sl_price: str = '', sl_trigger_price: str = '', sl_trigger_price_type: str = ''
        ):
        
        attachAlgoOrds = utils.generate_tp_sl_params(
            tp_price, tp_trigger_price, tp_trigger_price_type,
            sl_price, sl_trigger_price, sl_trigger_price_type
        )

        tdMode, ccy = utils.generate_future_tdmode_ccy(leverage_type, symbol)

        price = utils.generate_price(order_type, price)
        
        return self.place_order(
            instId=symbol,
            tdMode=tdMode,
            side=side,
            ordType=order_type,
            sz=quantity,
            ccy=ccy,
            px=price,
            attachAlgoOrds=attachAlgoOrds
        )

    def place_spot_order(
            self, symbol: str, quantity: str, side: str, order_type: str, price: str = '', tp_price: str = '', tp_trigger_price: str = '',
            tp_trigger_price_type: str = '', sl_price: str = '', sl_trigger_price: str = '', sl_trigger_price_type: str = ''
        ):

        attachAlgoOrds = utils.generate_tp_sl_params(
            tp_price, tp_trigger_price, tp_trigger_price_type,
            sl_price, sl_trigger_price, sl_trigger_price_type
        )

        price = utils.generate_price(order_type, price)

        return self.place_order(
            instId=symbol,
            tdMode=c.NO_MARGIN_CASH,
            side=side,
            ordType=order_type,
            sz=quantity,
            px=price,
            attachAlgoOrds=attachAlgoOrds
        )