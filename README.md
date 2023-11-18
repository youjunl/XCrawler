# XCrawler
A股爬虫项目
- 核心逻辑1:通过财经网址获取全部股票的动态数据，并且经过分析，将日涨，日跌超过x%的股票进行筛选，按照股票的涨跌幅进行排序；通过对股票的大额买入卖出订单进行排序，并预测前10位买入卖出的之后的大概股价，并对买入卖出进行排序；并存储到数据库(DB:Mysql，需要跟进)
- 核心逻辑2:对保留到数据库的数据按照5日，20日进行分析排序，筛选出5，20日上涨，下降的前x位的股票，进行排序，并存储到数据库(DB:Mysql)
- 核心逻辑3:做T，通过股票的涨跌幅，对股票进行T操作
1. 使用技术指标建模交易信号。比如利用布林通道、均线交叉等技术分析指标,建立买入和卖出规则。
2. 加入风险管理作为交易决策依据。比如设置止损价格和动态调整仓位,降低单日风险。
3. 采用复合指标相结合,避免单一依赖某一指标。比如结合MACD、KDJ等多 time frame 的指标信号。
4. 进行回测优化,找出参数组合效果好的交易策略。优化周期、触发点设定等策略变量。
5. 采用平滑移动平均线,避免被短期波动误导。比如用EMA作为买入信号。
6. 重点跟踪行业领跑股票,利用行业势头。同时观察大盘走势变化。
7. 使用量化选股条件排除个股风险,比如营收同比增长、获利能力等。
8. 定期回顾回测结果,调整不好的交易规则。持续优化策略模型。
9. 采取分散投资多个股票池分担风险。

部分参数解释：
- KDJ指标
  - KDJ指标的含义：KDJ是一个动量指标,用于衡量股票近期价格动能的强弱,并判断趋势形成的信号。

  - K值(K)
    1. 衡量最近买势与卖势的相对强度,范围0-100。
    2. K=(C-L14)/(H14-L14)*100
       - C:最近一日收盘价
       - L14:最近14日最低价
       - H14:最近14日最高价

  - D值(D)
    1. K值的简单移动平均,平滑K值的波动。
    2. 当日D = 前一日D值 × (1 - a) + 当日K值 × a (一般a取0.2)

  - J值(J)
    1. 衡量K值与D值距离的平均值,判断K线与D线背离程度。
    2. 当日J = (当日K+前一日K+前一日D)⁄3

  - 指标意义:
    1. K>D表示空头势头较弱或已转弱
    2. K<D表示多头势头较强
    3. K线上穿或下破D线,即K与D背离,可以看作趋势结束或变化的信号

- 布林线指标(Bollinger Bands)
  - 布林线指标是John Bollinger在1986年提出的一种易用且有效的趋势通道指标。是由中轨线和上轨线和下轨线组成。
  
  - 布林线指标意义:
    1. 由一条20日均线和标准差线组成上下界形成的通道。
    2. 标准差线一般取2倍标准差,表示价格波动98%时间范围内的上下波动空间。
    3. 当价格上行突破上轨或下跌破下轨,反映趋势可能将要改变。
    4. 中轨即20日均线,可以观察价格与均线的关系来判断多空趋势。
    5. 通道越窄,表明价格波动趋于平稳;越宽,则波动动较大。
    6. 价格带来回于通道内,反映短期震荡趋势;一直保持在通道内表现强势趋势。
    7. 常用在趋势判断、震荡发现、买入点挖掘、止损点确定等多种交易策略中。
  - 布林线指标计算公式:
    - 上轨:20日均线+2倍标准差
    - 中轨:20日均线
    - 下轨:20日均线-2倍标准差
    - 标准差:标准差可以反映一个数据集的离散程度
      - 标准差公式:Σ(收盘价-MA(N日平均线))2/N [N日所有收盘价-N日平均线 所得差开平方的总和 再除以N 得到的结果开根号]
      eg:则:
      Σ(收盘价-MA)2 = (10-15)2 + (11-15)2 + ...+(28-15)2
      Σ(收盘价-MA)2 / 20 = 和/20
      标准差 = √和/20
