# -*- coding: utf-8 -*-
import talib
from strategy_std import StrategyStd, Kline


class Strategy(StrategyStd):
    def __init__(self, params=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_asset_position(self):
        self.update_position()
        self.update_asset()

    def init(self):

        self.g.position_time = 0  # 初始化开仓时间
        self.set_slip(0.001)  # 滑点千分之一
        self.set_lever(2)  # 2倍杠杆
        self.add_task(self.update_asset_position, 3 * 1000) # 每隔3s执行一次定时任务（可以添加多个定时任务）

    def callback_kline_1s(self, kline: Kline):

        # 如果距离上次开仓时间超过30s
        if (kline.timestamp - self.g.position_time) > 1000 * 30:

            # 获取频率为5分钟的该标的的收盘价21条，数据类型为np.ndarray
            close_prices = self.get_live_array_1s(kline.symbol, 'close', 21, 5)


            # 使用TA-Lib计算短期和长期移动平均线
            short_ma = talib.SMA(close_prices, timeperiod=5)
            long_ma = talib.SMA(close_prices, timeperiod=20)

            # 如果当前没有持仓该标的，且出现金叉信号
            if kline.symbol not in self.position and short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]:
                # 金叉信号，买入
                success, error = self.user_create_order(kline.symbol, direction='OPEN_LONG', rate=0.5, tag='金叉买入')
                if success:
                    self.g.position_time = kline.timestamp
                    print(f"[{self.datetime}] 发出金叉买入信号:", kline.symbol)
                else:
                    print(f"[{self.datetime}] 金叉买入信号执行失败:", error)
            # 如果当前持有该标的仓位，且出现死叉信号
            elif kline.symbol in self.position and short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]:
                # 死叉信号，卖出
                success, error = self.liquid_total(kline.symbol, tag='死叉卖出')
                if success:

                    print(f"[{self.datetime}] 发出死叉卖出信号:", kline.symbol, self.position)
                    print('asset:', self.asset)
                else:
                    print(f"[{self.datetime}] 死叉卖出信号执行失败:", error)


if __name__ == '__main__':
    st = Strategy()

    st.subscribe_his({'kline_1m': (['btcusdt', 'ethusdt'], 300),
                      'kline_1h': (['btcusdt', 'ethusdt'], 300),
                      })

    st.subscribe_live_kline(live_freq='1s', freq=5)
    st.subscribe_live_kline(live_freq='1s', freq=20)
    st.subscribe_market({'kline_1m': [['btcusdt', 'ethusdt'], st.callback_kline_1m],
                         'kline_1h': [['btcusdt', 'ethusdt'], st.callback_kline_1h],
                         'close_1s': [['btcusdt', 'ethusdt'], st.callback_kline_1s],
                         })

    st.run(start='20231001', end='20231107', single_mode=True)
