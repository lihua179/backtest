# 回测系统文档 0.0.2
```commandline
pip install strategy_std-0.0.2-py3-none-any.whl
```
[v-0.0.2]  
```commandline
[update]
    1.添加多周期k线订阅
      st.subscribe_live_kline(live_freq='1s', freq=5) #这里订阅频率为5m的动态k线数据
      st.subscribe_live_kline(live_freq='1s', freq=10) #这里订阅频率为10m的动态k线数据
      
      
      def callback_kline_1s(self, kline: Kline):
      
          close_prices = self.get_live_1s(kline.symbol, col='close',  length=21,freq=5)#这里获取频率为5m的动态k线21根
          close_prices1 = self.get_live_1s(kline.symbol, 'close', 21) #这里获取频率为10m的动态k线21根，没有输入频率参数则默认为最后一次订阅的频率
    
    2.提供双均线策略demo
```
[v-0.0.1] 

```commandline
[append]
文档内容:
0.快速上手
1.程序架构以及策略关键函数
    订阅历史数据
    订阅动态数据(实时数据)
    订阅自定义动态k线
    系统开始函数
        设定手续费和滑点
        设定定时任务
    交易日开始函数
    行情回调函数    
    强制爆仓回调函数
    获取仓位
    获取资产
    交易日结束函数
    系统结束函数
2.数据结构
    K线
    资产
    仓位
    订单
    历史数据
3.进阶
    配合talib进行指标计算
    完整的双均线demo
```

### 0.快速上手
```commandline
# -*- coding: utf-8 -*-
from strategy_std import StrategyStd, Kline, Close, DIRECTION_RATE

class Strategy(StrategyStd):
    def __init__(self, params=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def loop_fun(self):
        self.update_position()
        self.update_asset()
        # print('每隔3s打印一次')
        # print(self.position)
        # print(self.asset)

    def init(self):
        """
        策略初始化函数
        :return:
        """
        self.set_lever(2)  # 设置杠杆为2倍
        self.add_task(self.loop_fun, 3 * 1000)  # 定时任务，3s循环一次
        pass

    def callback_kline_1h(self, kline: Kline):
        #
        # 每小时调用一次
        # print('kline_1h:', kline)
        pass

    def liquid_callback(self, success, error):
        print('强制爆仓：', success, error)
        print(self.position)
        print(self.asset)

    def callback_kline_1m(self, kline: Kline):
        pass

    def trade_start(self):
        pass
        # print('交易日开始')
        # print(self.position)
        # print(self.asset)
        # {'ETHUSDT': {'symbol': 'ETHUSDT', 'avg_price': 1892.72, 'quantity': 51.25, 'value': 96681.5875, 'direction': 'SHORT', 'ret_value': 320.3125, 'ret_rate': 0.006604252081660256, 'init_asset': 97001.9, 'create_time': 1699393743055.1887, 'update_time': 1699394703035.1887}, 'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 35381.4, 'quantity': 2.74, 'value': 96945.03600000001, 'direction': 'SHORT', 'ret_value': 0, 'ret_rate': 0, 'init_asset': 96945.03600000001, 'create_time': 1699394711015.7095, 'update_time': 1699394711015.7095}}
        # {'total': 146205.12320789794, 'free': 48814.397671897954, 'locked': 97293.7805}

    def trade_finish(self):
        pass
        # print('交易日结束')
        # print(self.position)
        # print(self.asset)

    def callback_kline_1s(self, kline: Kline):
        # 如果该标的不存在当前仓位，则开空
        if kline.symbol not in self.position:
            success, error = self.user_create_order(kline.symbol, direction='OPEN_SHORT', rate=0.5,
                                                    tag=f'标的{kline.symbol}不存在当前仓位，开空')  # 输入标的名，开仓方向，资金使用比例，tag为备注信息
            print(success, error)  # 返回订单结果
            print(self.position)
            print(self.asset)
#                 {'order_id': 638, 'symbol': 'ETHUSDT', 'avg_price': 1882.52, 'quantity': 51.73, 'value': 97382.75959999999, 'direction': 'OPEN_SHORT', 'filled': 51.73, 'fee': 97.38275959999999, 'create_time': 1699395068037.1887, 'date': '2023-11-08', 'time': '06:11:08', 'tag': '标的ETHUSDT不存在当前仓位，开空'} None
#                 {'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 35381.4, 'quantity': 2.74, 'value': 96876.53600000001, 'direction': 'SHORT', 'ret_value': 68.5, 'ret_rate': 0.0014131718925763253, 'init_asset': 96945.03600000001, 'create_time': 1699394711015.7095, 'update_time': 1699395063021.7095}, 'ETHUSDT': {'symbol': 'ETHUSDT', 'avg_price': 1882.52, 'quantity': 51.73, 'value': 97382.75959999999, 'direction': 'SHORT', 'ret_value': 0, 'ret_rate': 0, 'init_asset': 97382.75959999999, 'create_time': 1699395068037.1887, 'update_time': 1699395068037.1887}}
#                 {'total': 146306.23509689796, 'free': 48976.454537297956, 'locked': 97232.3978}
        #否则，如果持仓收益率>0.0或者<-0.01则平仓
        else:
         
            if self.position[kline.symbol].ret_rate < -0.01:
                success, error = self.liquid_total(kline.symbol, tag=f'触发止损，平仓（{kline.symbol}），打印此时资产和仓位：, position:{self.position}, asset:{self.asset}')
                print(success, error)
                print(self.position)
                print(self.asset)
            elif self.position[kline.symbol].ret_rate > 0.01:
                success, error = self.liquid_total(kline.symbol, tag=f'触发止盈，平仓（{kline.symbol}），打印此时资产和仓位：, position:{self.position}, asset:{self.asset}')
                print(success, error)
                print(self.position)
                print(self.asset)
#                 {'order_id': 637, 'symbol': 'ETHUSDT', 'avg_price': 1882.06, 'quantity': 51.25, 'value': 96455.575, 'direction': 'CLOSE_SHORT', 'filled': 51.25, 'fee': 96.455575, 'create_time': 1699395067001.1887, 'date': '2023-11-08', 'time': '06:11:07', 'tag': "触发止盈，平仓（ETHUSDT），打印此时资产和仓位：, position:{'ETHUSDT': {'symbol': 'ETHUSDT', 'avg_price': 1892.72, 'quantity': 51.25, 'value': 96455.575, 'direction': 'SHORT', 'ret_value': 546.3250000000041, 'ret_rate': 0.01126421235047982, 'init_asset': 97001.9, 'create_time': 1699393743055.1887, 'update_time': 1699395067001.1887}, 'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 35381.4, 'quantity': 2.74, 'value': 96876.53600000001, 'direction': 'SHORT', 'ret_value': 68.5, 'ret_rate': 0.0014131718925763253, 'init_asset': 96945.03600000001, 'create_time': 1699394711015.7095, 'update_time': 1699395063021.7095}}, asset:{'total': 146402.69067189796, 'free': 48814.397671897954, 'locked': 97588.293}"} None
#                 {'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 35381.4, 'quantity': 2.74, 'value': 96876.53600000001, 'direction': 'SHORT', 'ret_value': 68.5, 'ret_rate': 0.0014131718925763253, 'init_asset': 96945.03600000001, 'create_time': 1699394711015.7095, 'update_time': 1699395063021.7095}}
#                 {'total': 146306.23509689796, 'free': 97765.21709689795, 'locked': 48541.018000000004}




if __name__ == '__main__':
    st = Strategy()

    st.subscribe_his({'kline_1m': (['btcusdt', 'ethusdt'], 30),
                      'kline_1h': (['btcusdt', 'ethusdt'], 30),
                      })
    st.subscribe_live_kline(live_freq='1s', freq=5)
    st.subscribe_market({'kline_1m': [['btcusdt', 'ethusdt'], st.callback_kline_1m],
                         'kline_1h': [['btcusdt', 'ethusdt'], st.callback_kline_1h],
                         'close_1s': [['btcusdt', 'ethusdt'], st.callback_kline_1s],
                         })

    st.run(start='20231001', end='20231107', single_mode=True)


```
### 二.关键函数以及调用
###### 注意：以下函数以def 开头,如：def callback_kline_1s均为用户需要实现的函数，非主动调用，而是被动触发

1.程序架构以及策略关键函数

- 订阅历史数据
```commandline
st.subscribe_his({'kline_1m': (['btcusdt', 'ethusdt'], 300),
                  'kline_1h': (['btcusdt', 'ethusdt'], 30),
                  }) #这里订阅了btcusdt和ethusdt1分钟k线300根，1小时k线数据30根
```

- 订阅动态数据(实时数据)
```commandline
st.subscribe_live_kline(live_freq='1s', freq=5) #这里订阅了频率为5m的k线，且颗粒度为秒级  
st.subscribe_live_kline(live_freq='1s', freq=10) #这里订阅了频率为10m的k线，且颗粒度为秒级
支持多频率订阅
```

- 订阅自定义动态k线
```commandline
st.subscribe_live_kline(live_freq='1s', freq=5) #这里订阅了频率为5m的k线，且颗粒度为秒级
```

- 订阅回测行情
```commandline

st.subscribe_market({'kline_1m': [['btcusdt', 'ethusdt'], st.callback_kline_1m],
                     'kline_1h': [['btcusdt', 'ethusdt'], st.callback_kline_1h],
                     'close_1s': [['btcusdt', 'ethusdt'], st.callback_kline_1s],
                     })#这里对'btcusdt', 'ethusdt'订阅了分钟级，小时级，秒级行情，
                       #st.callback_kline_1m为接收1m行情数据的回调函数，其他同理
 
```
- 行情回调函数    
  事件驱动，主要用于实现策略逻辑
```commandline
def callback_kline_1s(self, kline: Kline):
    ...你的策略逻辑在此实现
 
```

- self.g
```commandline
  self.g是框架内可以存储当前状态的对象g,本体是一个字典，
  但经过处理后可以通过调用属性的方式来获取属性值
  使用demo:
  
  
    def init(self):
        self.g.create_position_time = 0  # 初始化开仓时间
        # self.g.order_id = []  # 初始化订单列表
        
    def callback_kline_1s(self, kline: Kline):
      # 如果当前时间与持仓时间超过30秒，则执行下单操作
        if (kline.timestamp - self.g.position_time) > 1000 * 30:
            self.g.create_position_time=kline.timestamp
            success, error = self.user_create_order(kline.symbol, direction='OPEN_LONG', rate=0.5, tag='金叉买入')
            if success:
                #如果成功的话，则刷新开仓时间
                self.g.create_position_time = kline.timestamp
                # self.g.order_id.append(success.order_id)
```
- 策略初始化函数
```commandline
def loop_fun(self):
    #自定义定时任务：更新资产和仓位
    self.update_position()
    self.update_asset()
    
#这里在初始函数可以设定手续费和滑点
def init(self):

    self.set_lever(2)  # 设置杠杆为2倍
    self.set_slip(0.001)  # 设置滑点为千一
    self.add_task(self.loop_fun, 3 * 1000)  # 定时任务，3s循环一次
 
```
- 交易日开始函数（trade_start） ,交易日结束函数（trade_finish）
  每个交易日开始前,结束后需要做的工作，如打印当前的资产和仓位，
- 系统开始函数  （sys_start）， 系统结束函数  （sys_finish）
```commandline
def trade_start(self):
    position=self.get_position()
    asset=self.get_asset()
    log.info(position)
    log.info(asset)
    
def trade_finish(self):
    pass
    
def sys_start(self):
    #只执行一次，在策略启动前开始
    pass
def sys_finish(self):
    #只执行一次，在策略结束后开始
    pass
 
```

    
  
- 获取动态k线数据
  
```commandline

data = self.get_live_1s(kline.symbol, 'close', 30) 
print(data)
#data:[27528.1,..., 27561.4, 27578.5, 27579.0, 27600.9, 27612.1, 27619.0],最后一个为未到期最新数据
 
data = self.get_live_array_1s(kline.symbol, 'close', 30) #用于将列表自动转为np.ndarray数据类型，便于后续用于talib计算
print(data)
#data:[27528.1,..., 27561.4, 27578.5, 27579.0, 27600.9, 27612.1, 27619.0],最后一个为未到期最新数据
  
 
```  
#### 2.交易相关

- 获取仓位/获取资产
  
```commandline
position=self.get_position()
#position:{'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 35381.4, 'quantity': 2.74, 'value': 96876.53600000001, 'direction': 'SHORT', 'ret_value': 68.5, 'ret_rate': 0.0014131718925763253, 'init_asset': 96945.03600000001, 'create_time': 1699394711015.7095, 'update_time': 1699395063021.7095}}
asset=self.get_asset()  
#asset:{'total': 146306.23509689796, 'free': 97765.21709689795, 'locked': 48541.018000000004}
 
```  

- 创建订单
  
```commandline

create_order(symbol,  #交易标的，如：BTCUSDT
                price=0,  #下单价格 
                quantity=10,  #下单数量 
                direction='OPEN_LONG', #下单方向:开多，开空，平多，平空['OPEN_LONG','OPEN_SHORT','CLOSE_LONG','CLOSE_SHORT']
                order_type='market', #订单类型'market','limit'
                tag='',      #订单备注 
                ) -> [Order, Error] # 订单结果，错误结果
                
                
``` 

- 用户快速创建订单  
  根据用户的可用资金下单（常用）
```commandline

user_create_order(self,
                      symbol,
                      direction, 
                      rate,  #可用资金比率
                      tag='')  
                      
success, error = self.user_create_order('BTCUSDT', direction='OPEN_SHORT', rate=0.5,)  # 这里使用一半的可用资金开空仓
print(success, error)  # 返回订单结果  
                
``` 

- 用户全部平仓 

```commandline

liquid_total(self, symbol, tag='')
      
           
``` 
- 用户部分平仓 
  rate为平仓比例，0-1之间
```commandline

liquid_part(self, symbol, rate, tag='')
   
                
``` 

- 强制爆仓回调函数  
  -返回结果为订单结果success,error
```commandline
def liquid_callback(self, success, error):
    log.info('强制爆仓：', success, error) 
 
```  



#### 3.数据类型

###### 行情K线 资产 仓位 订单 历史数据  

- 行情K线  

```commandline
class Kline:
    def __init__(self, symbol, open,  high, low,close, volume, amount, timestamp,dtype='kline_1m'):
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
``` 

- 仓位 

```commandline
数据结构
position={'ETHUSDT': {'symbol': 'ETHUSDT', #标的
'avg_price': 1892.72,  #成交均价
'quantity': 51.25,  #数量
'value': 96681.5875, #持仓价值
'direction': 'SHORT',  #方向
'ret_value': 320.3125, #收益值
'ret_rate': 0.006604252081660256, #收益率
'init_asset': 97001.9,  #初始资产
'create_time': 1699393743055.1887, #创建时间
'update_time': 1699394703035.1887}, #更新时间

'BTCUSDT': {'symbol': 'BTCUSDT', 
'avg_price': 35381.4, 'quantity': 2.74,
'value': 96945.03600000001, 
'direction': 'SHORT', 'ret_value': 0,
'ret_rate': 0, 'init_asset': 96945.03600000001,
'create_time': 1699394711015.7095, 
'update_time': 1699394711015.7095}}


相关函数
self.position #获取当前全部仓位，字典类型，非更新
self.get_position() #通过http请求，获取当前最新仓位数据
self.update_position() #通过最新行情自行计算当前仓位最新数据
#回测模式下，self.get_position()与self.up_position() 完全相同，都是内部计算

使用方式：
在每个回调函数下都进行self.update_position()
如：
  def callback_kline_1m(self, kline:Kline):
      self.update_position()
    
或者通过定时任务self.update_position()
如：
    def loop_fun(self):
    #自定义定时任务：更新资产和仓位
    self.update_position()
    self.update_asset()
    
  #这里在初始函数可以设定手续费和滑点
  def init(self):
      self.add_task(self.loop_fun, 3 * 1000)  # 定时任务，3s循环一次
``` 


- 资产

```commandline
asset={'total': 146306.23509689796, #总资产
'free': 97765.21709689795,  #可用资产
'locked': 48541.018000000004} #锁定资产

相关函数
self.asset #获取当前全部资产，字典类型，非更新
self.get_asset() #通过http请求，获取当前最新资产数据
self.update_asset() #通过最新行情自行计算当前资产最新数据

使用方式同position
``` 


- 订单

```commandline
success, error = self.user_create_order(kline.symbol, 
                                        direction='OPEN_SHORT',
                                        rate=0.5,
                                        tag=f'标的{kline.symbol}不存在当前仓位，开空')
如果成功，则：                                                    
success={'order_id': 638, #订单id
'symbol': 'ETHUSDT', #标的 
'avg_price': 1882.52,  #成交均价
'quantity': 51.73,  #数量
'value': 97382.75959999999, #价值
'direction': 'OPEN_SHORT', #方向 
'filled': 51.73,  #成交数量
'fee': 97.38275959999999, #手续费 
'create_time': 1699395068037.1887, #创建时间
'date': '2023-11-08', #日期
'time': '06:11:08',  #时间
'tag': '标的ETHUSDT不存在当前仓位，开空'} #订单备注

如果创建订单失败，则： 
error=class Error:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return str({'code': self.code, 'msg': self.msg})


相关函数
self.asset #获取当前全部资产，字典类型，非更新
self.get_asset() #通过http请求，获取当前最新资产数据
self.update_asset() #通过最新行情自行计算当前资产最新数据

使用方式同position
``` 

- 历史数据

```commandline
数据结构：

{'BTCUSDT':{'open':[11,11.1,11.2,11.05,...],
'high':[12,13.1,13.2,14.05,...],
'low':[10,10.1,10.2,10.05,...],
'close':[11.6,11.2,11.4,11.15,...],
'volume':[11231,1145.1,13241.2,17581.05,...],
'amount':[12131,111.1,4511.2,1671.05,...],
'timestampt':[111891956.48,119519651969.1,151134851.2,1131425143.05,...],
}}


使用方式:
秒级
res=self.get_live_1s(symbol='BTCUSDT',  col='close',length=10) #获取动态k线序列
res:[11,11.1,11.2,11.05,...] #其中，最后一条为未到期

分钟级
res=self.get_live_1m(symbol='BTCUSDT',  col='close',length=10) #获取动态k线序列
res:[11,11.1,11.2,11.05,...] #最后一条为1分钟到期，n分钟未到期

分钟级
res=get_market(symbol='BTCUSDT', freq='1m') #获取1分钟btcusdt到期历史数据
res:{'open':[11,11.1,11.2,11.05,...],
'high':[12,13.1,13.2,14.05,...],
'low':[10,10.1,10.2,10.05,...],
'close':[11.6,11.2,11.4,11.15,...],
'volume':[11231,1145.1,13241.2,17581.05,...],
'amount':[12131,111.1,4511.2,1671.05,...],
'timestampt':[111891956.48,119519651969.1,151134851.2,1131425143.05,...],
}

```

### 3.进阶
- 配合talib进行指标计算

```commandline
[计算macd指标]
def callback_kline_1s(self, kline: Kline):
    close_prices = self.get_live_array_1s(kline.symbol, 'close', 50)
    macd, signal, hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    print(macd[-1],signal[-1],hist[-1])
    
    #res:19.598217015940463 20.050940318076997 -0.45272330213653333
```

```commandline
[计算布林带]
def callback_kline_1s(self, kline: Kline):
    close_prices = self.get_live_array_1s(kline.symbol, 'close', 50)
    upper_band, middle_band, lower_band = talib.BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    # 打印结果
    print("Upper Band:", upper_band[-1])
    print("Middle Band:", middle_band[-1])
    print("Lower Band:", lower_band[-1])
    
    #res:Upper Band: 27610.106519481247
        Middle Band: 27530.274999999994
        Lower Band: 27450.44348051874
```

- 完整的双均线demo
```commandline
#在下列代码中，我们使用callback_kline_1s函数来接收1秒频率的K线数据，
#并计算短期（5根bar）和长期（20根bar）的移动平均线。
#其中，计算移动平均线的每根bar颗粒度为5分钟
#然后，我们根据短期和长期均线的交叉情况判断金叉和死叉信号，并执行相应的买入和卖出操作。

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
        self.add_task(self.update_asset_position, 3 * 1000)  # 每隔3s执行一次定时任务（可以添加多个定时任务）

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
```
```commandline
运行双均线策略程序, 截取部分打印信息：
[2023-10-03 09:30:00] 发出金叉买入信号: ETHUSDT
[2023-10-03 09:35:00] 发出金叉买入信号: BTCUSDT
[2023-10-03 11:04:04] 发出死叉卖出信号: ETHUSDT {'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 27493.0, 'quantity': 18.15, 'value': 499860.07499999995, 'direction': 'LONG', 'ret_value': 862.1249999999999, 'ret_rate': 0.0034554250172771253, 'init_asset': 498997.94999999995, 'create_time': 1696296900129.6465, 'update_time': 1696302242024.6465}}
asset: {'total': 998933.860618, 'free': 748572.7606180001, 'locked': 250361.09999999998}
[2023-10-03 11:45:00] 发出金叉买入信号: ETHUSDT
[2023-10-03 12:10:00] 发出死叉卖出信号: BTCUSDT {'ETHUSDT': {'symbol': 'ETHUSDT', 'avg_price': 1666.95, 'quantity': 447.27, 'value': 744995.2755, 'direction': 'LONG', 'ret_value': -581.4509999999797, 'ret_rate': -0.0015597348450762825, 'init_asset': 745576.7265, 'create_time': 1696304700735.3489, 'update_time': 1696306200000.6135}}
asset: {'total': 997618.2928015001, 'free': 625411.3805515, 'locked': 372206.91225}
[2023-10-03 12:27:12] 发出死叉卖出信号: ETHUSDT {}
asset: {'total': 996140.624539, 'free': 996140.624539, 'locked': 0.0}
[2023-10-03 12:55:00] 发出金叉买入信号: ETHUSDT
[2023-10-03 12:58:12] 发出金叉买入信号: BTCUSDT
[2023-10-03 13:29:33] 发出死叉卖出信号: ETHUSDT {'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 27630.0, 'quantity': 17.99, 'value': 496252.35099999997, 'direction': 'LONG', 'ret_value': -811.3489999999738, 'ret_rate': -0.003264567499095081, 'init_asset': 497063.69999999995, 'create_time': 1696309092010.6465, 'update_time': 1696310972084.3489}}
asset: {'total': 992776.516666, 'free': 745056.0156660001, 'locked': 247720.50099999993}
[2023-10-03 13:31:03] 发出金叉买入信号: ETHUSDT
[2023-10-03 13:59:50] 发出死叉卖出信号: BTCUSDT {'ETHUSDT': {'symbol': 'ETHUSDT', 'avg_price': 1665.44, 'quantity': 445.57, 'value': 741891.8728, 'direction': 'LONG', 'ret_value': -178.2280000000405, 'ret_rate': -0.0004803535402057005, 'init_asset': 742070.1008, 'create_time': 1696311063033.3489, 'update_time': 1696312790137.6465}}
asset: {'total': 990858.5561301999, 'free': 620001.7337302, 'locked': 370856.82239999995}
[2023-10-03 14:05:00] 发出死叉卖出信号: ETHUSDT {}
asset: {'total': 989684.8935602999, 'free': 989684.8935602999, 'locked': 0.0}
[2023-10-03 14:30:00] 发出金叉买入信号: BTCUSDT
[2023-10-03 14:39:18] 发出金叉买入信号: ETHUSDT
[2023-10-03 15:20:00] 发出死叉卖出信号: ETHUSDT {'BTCUSDT': {'symbol': 'BTCUSDT', 'avg_price': 27585.9, 'quantity': 35.73, 'value': 985168.9979999999, 'direction': 'LONG', 'ret_value': -475.20900000010397, 'ret_rate': -0.0009642607274008033, 'init_asset': 985644.2069999999, 'create_time': 1696314600022.6465, 'update_time': 1696317600000.6135}}
asset: {'total': 986168.3986742999, 'free': 493821.50417429995, 'locked': 492346.89449999994}
[2023-10-03 15:20:27] 发出死叉卖出信号: BTCUSDT {}
asset: {'total': 984951.2562242998, 'free': 984951.2562242998, 'locked': 0.0}
...
```

```commandline
可视化结果
order.jpg:订单流可视化
performance.jpg:策略性能表现
```
![示例图片](https://github.com/lihua179/strategy_std/blob/main/order.jpg)
![示例图片](https://github.com/lihua179/strategy_std/blob/main/performance.jpg)
![示例图片](https://github.com/lihua179/strategy_std/blob/main/research.jpg)









