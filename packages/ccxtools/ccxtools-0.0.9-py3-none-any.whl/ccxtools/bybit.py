from decimal import Decimal
import ccxt
from ccxtools.exchange import Exchange


class Bybit(Exchange):

    def __init__(self, who, config):
        self.ccxt_inst = ccxt.bybit({
            'apiKey': config(f'BYBIT_API_KEY{who}'),
            'secret': config(f'BYBIT_SECRET_KEY{who}')
        })
        self.max_trading_qtys = self.get_max_trading_qtys()

    def get_balance(self, market, ticker):
        return self.ccxt_inst.fetch_balance()[ticker]['total']

    def get_max_trading_qtys(self):
        markets = self.ccxt_inst.fetch_markets()

        result = {}
        for market in markets:
            if not market['linear']:
                continue

            ticker = market['base']
            result[ticker] = Decimal(market['info']['lot_size_filter']['max_trading_qty'])

        return result

    def get_risk_limit(self, market, ticker):
        if market == 'USDT':
            return self.ccxt_inst.public_linear_get_risk_limit({
                'symbol': f'{ticker}USDT'
            })

    def set_risk_limit(self, market, ticker, side, risk_id):
        if market == 'USDT':
            return self.ccxt_inst.private_linear_post_position_set_risk({
                'symbol': f'{ticker}USDT',
                'side': side,
                'risk_id': risk_id
            })
