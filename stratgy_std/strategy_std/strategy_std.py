# -*- coding: utf-8 -*-
"""
@author: Zed
@file: strategy_std.py
@time: 2024/1/5 10:32
@describe:回测系统标准接口
"""
from typing import Union
import numpy as np
from easydict import EasyDict

class Asset:
    def __init__(self, total, free, locked):
        self._total = total
        self._free = free
        self._locked = locked

    def set_total(self, total):
        self._total = total

    def set_free(self, free):
        self._free = free

    def set_locked(self, locked):
        self._locked = locked

    @property
    def total(self):
        return self._total

    @property
    def free(self):
        return self._free

    @property
    def locked(self):
        return self._locked

    @property
    def data(self):
        return {'total': self._total, 'free': self._free, 'locked': self._locked}

    def __str__(self):
        return str({'total': self._total, 'free': self._free, 'locked': self._locked})

    def __getitem__(self, item):
        return self.data[item]


class PositionUnite:
    def __init__(self, symbol, avg_price, quantity, direction, value, ret_rate, ret_value, init_asset,
                 create_time):
        self._symbol = symbol
        self._avg_price = avg_price
        self._quantity = quantity
        self._direction = direction
        self._value = value
        self._ret_value = ret_value
        self._ret_rate = ret_rate
        self._init_asset = init_asset
        self._create_time = create_time
        self._update_time = create_time

    @property
    def symbol(self):
        return self._symbol

    @property
    def avg_price(self):
        return self._avg_price

    @property
    def quantity(self):
        return self._quantity

    @property
    def direction(self):
        return self._direction

    @property
    def value(self):
        return self._value

    @property
    def ret_value(self):
        return self._ret_value

    @property
    def ret_rate(self):
        return self._ret_rate

    @property
    def init_asset(self):
        return self._init_asset

    @property
    def create_time(self):
        return self._create_time

    @property
    def update_time(self):
        return self._update_time

    @property
    def data(self):
        return {'symbol': self._symbol, 'avg_price': self._avg_price,
                'quantity': self._quantity, 'value': self._value, 'direction': self._direction,
                'ret_value': self.ret_value, 'ret_rate': self._ret_rate, 'init_asset': self._init_asset,
                'create_time': self._create_time,
                'update_time': self._update_time}

    def __getitem__(self, item):
        return self.data.get(item, {})

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


class Position:
    def __init__(self):
        self._position = {}
        self._symbol = None
        self._symbols = []

    @property
    def ret_rate(self):
        return self._position[self.symbol].ret_rate

    @property
    def ret_value(self):
        return self._position[self.symbol].ret_value

    @property
    def avg_price(self):
        return self._position[self.symbol].avg_price

    @property
    def symbol(self):
        return self._symbol

    @property
    def quantity(self):
        return self._position[self.symbol].quantity

    @property
    def direction(self):
        return self._position[self.symbol].direction

    @property
    def value(self):
        return self._position[self.symbol].value

    @property
    def init_asset(self):
        return self._position[self.symbol].init_asset

    @property
    def create_time(self):
        return self._position[self.symbol].create_time

    @property
    def update_time(self):
        return self._position[self.symbol].update_time

    @property
    def data(self):
        return self._position[self.symbol].data

    @property
    def symbols(self):
        return self._symbols

    @property
    def datas(self):
        return self._position

    def get(self, symbol, replace_obj={}):
        return self._position.get(symbol, replace_obj)

    def __bool__(self):
        return True if self._position else False

    def __setitem__(self, key, value):
        if not value:
            del self._position[key]
        self._position.update({key: value})
        self._symbol = key
        self._symbols.append(key)

    def __contains__(self, item):
        return True if item in self._symbol else False

    def __getitem__(self, item):
        return self._position.get(item, {})

    def __str__(self):
        return str(self._position)

    def __repr__(self):
        return self._position

    def __delitem__(self, key):
        del self._position[key]
        self._symbols.remove(key)

    def delete(self):
        self._position = {}
        self._symbol = None

    @property
    def position(self):
        return self._position


class Order:
    def __init__(self, order_id, symbol, avg_price, direction, quantity, filled, fee, value, create_time, date=None,
                 time=None, tag=''):
        self.order_id = order_id
        self.symbol = symbol
        self.avg_price = avg_price
        self.direction = direction
        self.quantity = quantity
        self.filled = filled
        self.fee = fee
        self.create_time = create_time
        self.value = value
        self.date = date
        self.time = time
        self.tag = tag
        self.data = {'order_id': order_id, 'symbol': symbol, 'avg_price': avg_price,
                     'quantity': quantity, 'value': value, 'direction': direction,
                     'filled': filled, 'fee': fee, 'create_time': create_time, 'date': date, 'time': time,
                     'tag': tag}

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return str(self.data)


class Error:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return str({'code': self.code, 'msg': self.msg})


class Kline:
    def __init__(self, symbol, open, high, low, close, volume, amount, timestamp, dtype='kline_1m'):
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.amount = amount
        self.timestamp = timestamp
        self.dtype = dtype

    @property
    def data(self):
        return {'symbol': self.symbol,
                'open': self.open,
                'high': self.high,
                'low': self.low,
                'close': self.close,
                'volume': self.volume,
                'amount': self.amount,
                'timestamp': self.timestamp,
                'dtype': self.dtype
                }

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


class StrategyStd:
    def __init__(self, *args, **kwargs):
        self.g = EasyDict()

    def add_task(self, func, interval, *args, **kwargs):
        pass

    def liquid_callback(self, success, error):
        pass

    def init(self):
        pass

    def sys_start(self):
        pass

    def sys_finish(self):
        pass

    def trade_start(self):
        pass

    def trade_finish(self):
        # print('trade_finish')
        pass

    def set_lever(self, lever=2):
        pass

    def set_slip(self, slip=0.002):
        pass

    def subscribe_market(self, symbol_dict=None):
        pass

    def subscribe_his(self, symbol_dict=None):
        pass

    def run(self, *args, **kwargs):
        pass

    def create_order(self, symbol, price, quantity=10, direction='OPEN_LONG', order_type='market', tag='') -> Union[
        tuple[None, Error], tuple[Order, None]]:
        #
        pass

    def user_create_order(self, symbol, direction, rate, tag='') -> Union[
        tuple[None, Error], tuple[Order, None]]:
        pass

    def liquid_total(self, symbol, tag='') -> Union[
        tuple[None, Error], tuple[Order, None]]:
        pass

    def liquid_part(self, symbol, rate, tag='') -> Union[
        tuple[None, Error], tuple[Order, None]]:
        pass

    def get_asset(self) -> Asset:
        """
        获取最新资产
        :return:
        """
        pass

    def get_position(self) -> Position:
        """
        获取最新仓位
        :return:
        """
        pass

    def update_asset(self):
        """
        获取最新资产
        :return:
        """
        pass

    def update_position(self):
        """
        获取最新仓位
        :return:
        """
        pass

    @property
    def asset(self) -> dict:
        """
        获取当前资产（不保证最新）
        :return:
        """
        return {}

    @property
    def position(self) -> dict:
        """
        获取当前仓位（不保证最新）
        :return:
        """
        return {}

    def get_market(self, symbol, freq):
        pass

    def get_live_1s(self, symbol, col, length=0, freq=None) -> list:
        pass

    def get_live_array_1s(self, symbol, col, length=0, freq=None) -> np.ndarray:
        pass

    def get_live_1m(self, symbol, col, length=0, freq=None) -> list:
        pass

    def get_live_array_1m(self, symbol, col, length=0, freq=None) -> np.ndarray:
        pass

    def get_live_data_len(self, symbol, freq=None) -> int:
        pass

    def callback_kline_1m(self, kline: Kline):
        pass

    def callback_kline_1h(self, kline: Kline):
        pass

    def subscribe_live_kline(self, live_freq='1s', freq=5):
        """
        订阅动态k线：3m,5m,10m,15m,30m,...任意频率的实时未到期k线，精度为分钟或者秒
        live_freq:颗粒度：'1m'/'1s'
        length:频率长度:'3m','5m',...
        :return:
        """
        pass

    def callback_kline_1s(self, kline: Kline):
        pass

    @property
    def datetime(self) -> str:
        return '1'
