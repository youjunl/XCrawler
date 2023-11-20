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

部分参数解释:

- SMA(MA)(简单平均数)
  - 普通移动平均线(Moving Average):表示求x在n周期内的简单移动平均
  - 计算方法:n个时间单位移动平均线= (第1个时间单位价格+第2时间单位价格+…+第n时间单位价格)/n
  - 5日均线(5 SMA):是指股票在最近5个交易日(不包括当日)内每日收盘价格的平均值。反映近期价格动向。
  - 10日均线(10 SMA):是指股票在最近10个交易日(不包括当日)内每日收盘价格的平均值。较5日均线则反应的周期稍长。
  - 20日均线(20 SMA):是指股票在最近20个交易日(不包括当日)内每日收盘价格的平均值。相对5日和10日均线,20日均线反映了价格动向的中期趋势。
  - 这三条均线使用不同交易日计算平均价格,周期从短到长。
    - 5日判断近期短中长线价格走势
    - 10日金叉与死叉形成买卖信号
    - 20日价格与不同周期均线的交叉位点形成支持 Resistance 轴。

- EMA(指数移动平均线 EXPMA指标)
  - 通俗说法,EMA则需要给每个时间单位的最高最低等价位数值做一个权重处理，然后再平均,对于越近期的收盘价给予更高的权重，也就是说越靠近当天的收盘价对EMA产生的影响力越大，而越远离当天的收盘价则呈现指数式递减。指数平滑移动平均线的初始值计算方法与简单移动平均相同，也就是将n日间的收盘价的合计除以n算出。然后从第2日起，以前一日的EMA+平滑化常数α×（当日收盘价-前日EMA）算出。此外，平滑化常数为α＝2÷（n+1）。使用此平滑化常数计算，比重就会呈现指数函数性的衰减。相对于SMA来说，EMA走势更为平滑，反映较为灵敏，能更即时反应出近期股价涨跌的波动与转折。但也容易在震荡环境下被主力洗筹的假象给洗出去
  - 指数移动平均线指标(Exponential Moving Average):表示求x在n周期内的平滑移动平均。(指数加权)
  - 计算方法:
    当前周期单位指数平均值 = 平滑系数 * (当前周期单位指数值 - 上一个周期单位指数平均值) + 上一个周期单位指数平均值；
    平滑系数= 2 / (周期单位+1)
    得到：EMA(N) = [ (N-1) * EMA(N-1) + 2 * X(当前周期单位的收盘价)] / (N+1)

- WMA(加权移动平均线)
  - 加权移动平均线指标(Weighted Moving Average):表示求x在n周期内的加权移动平均。在计算平均价格时，对于越近期的收盘价给予越高的权重，而较后期的收盘价则占有较小权重。不过与EMA之间的差异在于，WMA使用的加权乘数是以「线性递减」的方式，与EMA的加权乘数呈现不固定式递减的方式不同。在市场上，WMA这条均线比较少人在使用，绝大多数人还是使用较简单理解的SMA作为主要观察的均线。
  - 计算方法:WMA(N) = [N*第N天收盘价 + (N-1)*第N-1天收盘价 + … + 1*第1天收盘价] / (N+N-1+N-2+....+1)加权乘数总和

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

  - 布林线指标意义:
    1. 由一条20日均线和标准差线组成上下界形成的通道。
    2. 标准差线一般取2倍标准差,表示价格波动98%时间范围内的上下波动空间。
    3. 当价格上行突破上轨或下跌破下轨,反映趋势可能将要改变。
    4. 中轨即20日均线,可以观察价格与均线的关系来判断多空趋势。
    5. 通道越窄,表明价格波动趋于平稳;越宽,则波动动较大。
    6. 价格带来回于通道内,反映短期震荡趋势;一直保持在通道内表现强势趋势。
    7. 常用在趋势判断、震荡发现、买入点挖掘、止损点确定等多种交易策略中。
  - 布林线指标应用:
    - 喇叭口研判:https://www.zhihu.com/question/384284854
      1. 开口型:开口型喇叭口预示着一方力量逐渐强大而一方力量逐步衰竭，价格将处于短期单向行情中，方向则一般由盘整时所处的位置决定，例如高位盘整开口一般意味着暴跌，低位盘整则一般意味着暴涨.
      开口型喇叭口形态的形成必须具备两个条件。
      其一，长时间的横盘整理，整理时间越长、上下轨之间的距离越小则未来波动的幅度越大；
      其二，布林线开口时要有明显的大的成交量出现。
      开口喇叭口形态的确立是以K线向上突破上轨线、价格带量向上突破中长期均线为准
      2. 收口型:经历上涨后收口型喇叭口预示着空头力量逐渐强大而多头力量开始衰竭，价格将处于短期大幅下跌的行情之中。经历下跌后的收口型喇叭口则相反。收口型喇叭口形态的形成虽然对成交量没有要求。
      收口型喇叭具备一个条件，即价格经过前期大幅的短线拉升，拉升的幅度越大、上下轨之间的距离越大则未来下跌幅度越大。上涨后收口型喇叭口形态的确立是以价格的上轨线开始掉头向下、价格向下跌破短期均线为准。
      3. 紧口型:紧口型喇叭口预示着多空双方的力量逐步处于平衡，价格将处于长期横盘整理的行情中
      紧口型喇叭口形态的形成条件和确认标准比较宽松，只要价格经过较长时间的大幅波动后，成交极度萎缩，上下轨之间的距离越来越小的时候就可认定紧口型喇叭初步形成。当紧口型喇叭口出现后，投资者既可以观望等待，也可以少量建仓。BOLL线还可以配合判断M头和W底，以W底为例，主要是看左底和右底在布林线中处于何种相对位置上。一般来说，W底的左底会触及下轨线甚至跌破下轨线，但右底却大多是收在布林线下轨线之内，跌破下轨线的时候较少。当价格第一次下跌时，价格跌破布林线下轨线，但随后的反弹却比较强劲，价格不仅越过了布林线的中轨，且能上摸至上轨线；当价格第二次下跌时，没有跌破布林线的下轨线，而是与下轨线有一小段距离，受到下轨线的有力支撑，并再次出现了强劲反弹。从二次下探过程中，我们看到，价格的每次下探是逐步与布林线下轨线拉开距离的，这表明布林线显示市场人气在逐渐地增强，在酝酿着转机。

- RSI指标(相对强弱指数)(动能策略)

  - 指数含义:衡量价格上涨或者下跌动能的技术指标
  - 计算公式:RSI＝[上升平均数÷(上升平均数＋下跌平均数)]×100
    - 上升平均数:N日价格的上涨平均数
    - 下跌平均数:N日价格的下跌平均数
  - 应用:RSI最基本的用法是在指标自下而上突破30点时寻找买入，或者在指标自上而下跌破70时卖出。 该策略是押注市场行情会在强弱间切换，当趋势过强时去捕捉向下的转折点，而当趋势太弱时定位向上的突破机会

- MACD策略(Moving Average Convergence Divergence 移动平均线收敛与发散策略)
  - MACD指标含义:通过计算较长时间和较短时间指数移动平均线的差异,来衡量股票近期价格动能的强弱。
  - MACD指标计算公式:MACD＝(ema12- ema26) / (ema12 + ema26) * 200 + ema12 其中ema12为12日指数移动平均线,ema26为26日指数移动平均线
  
- 均线策略
- 可转债策略
- 资金流策略
- WR(动量策略)
  - 策略含义:WR指标是衡量市场动量的技术指标。WR指标由Williams %R指标和动量指标(MOM)构成。
    1. 该指标能及早发现行情的转向信号，对突发事件反应灵敏，是短线操作应用指标。在使用过程中，最好能结合强弱指数，动向指数等较为平衡的技术指标一起研制，由此可对行情趋势得出较准确的判断。
    2. 超买、超卖和买卖信号非常清楚，能使投资者了解；发出的超卖信号不等于可以买进，而是告知投资者在此价位不要盲目追卖。反之，发出的超买信号也不等于可以卖出，而是警告投资者不要盲目在此价位追买。
    3. 改变W%R曲线的取样天数可以滤除短线频繁的交叉点买卖信号。
    4. 在使用该指标时，会出现超买之后又超买，超卖之后又超卖现象，常使投资者左右为难，不知如何是好。
  - 计算公式: (N周期内最高价-当前价)/(N周期内最高价-N周期内最低价)*100 其中N一般为4或14。
    取值范围为0-100:
    WR值越大,当前价格距离周期最高价越近,表明动能较强;
    WR值越小,当前价格距离周期最低价越近,表明动能较弱。
  - 判断条件
    1、当威廉指标在20——0区间内时，是指标提示的超买区，表明市场处于超买状态，可考虑卖出。威廉指标20线，一般看做卖出线。
    2、当威廉指标进入80——100区间内时，是指标提示的超卖区，表明市场处于超卖状态，可考虑买入。威廉指标80线，一般看做买入线。
    3、当威廉指标在20——80区间内时，表明市场上多空双方处于相持阶段，价格处于横盘整理，可考虑观望。
  - 总结:威廉指标可以运用于行情的各个周期的研究判断，大体而言，威廉指标可分为5分钟、15分钟、30分钟、60分钟、日、周、月、年等各种周期，
WR连续几次撞顶（底），局部形成双重或多重顶（底），是卖出（买进）的信号。这样的信号更为可靠

- DMI(动能策略)
  - 策略含义:DMI指标又叫动向指标或趋向指标,其全称叫“Directional Movement Index,简称DMI”,也是由美国技术分析大师威尔斯．威尔德（Wells Wilder）所创造的,是一种中长期股市技术分析方法。
    1. 上升方向线+DI(又称PDI), +DI为黄色线
    2. 下降方向线- DI (又称 MDI), -DI为红色线
    3. 趋向平均值ADX，主要用于对趋势的判断, ADX为蓝色线
    4. ADXR，对ADX 的评估数值，也是对市场的评估指标, ADXR为绿色线
  - 策略原理:DMI指标是通过分析股价在涨跌过程中买卖双方力量均衡点的变化情况,即多空双方的力量的变化受价格波动的影响而发生由均衡到失衡的循环过程,从而提供对趋势判断依据的一种。
　　DMI指标的基本原理是在于寻找股价涨跌过程中,股价藉以创新高价或新低价的功能,研判多空力量,进而寻求买卖双方的均衡点及股价在双方互动下波动的循环过程。在大多数指标中,绝大部分都是以每一日的收盘价的走势及涨跌幅的累计数来计算出不同的分析数据,其不足之处在于忽略了每一日的高低之间的波动幅度。比如某个股票的两日收盘价可能是一样的,但其中一天上下波动的幅度不大,而另一天股价的震幅却在10%以上,那么这两日的行情走势的分析意义决然不同,这点在其他大多数指标中很难表现出来。而DMI指标则是把每日的高低波动的幅度因素计算在内,从而更加准确的反应行情的走势及更好的预测行情未来的发展变化。
  - 计算正向动量指标DI+: DI+ = (当日高点 - 上一日高点)/当日移动范围 × 100
  - 计算负向动量指标DI-: DI- = (当日低点 - 上一日低点)/当日移动范围 × 100
  - 移动范围: 每日最高价 - 每日最低价 移动范围是用来标准化DI+和DI-的值,消除因价格范围不同而引起的指标计算误差
  - 计算动向指标DM: DM+ = DI+的N日简单移动平均  DM- = DI-的N日简单移动平均
  - 计算动向趋势线DX: DX = abs(DM+)/ (abs(DM+)+abs(DM-)) * 100
  - 计算动向移动平均指数DMI: DMI = N日EMA(DX)
  - 计算公式:
  - 参考逻辑:
    1. 多空指标包括(+DI多方、-DI空方 +DM多动向、-DM空动向)
       - +DI在-DI上方,股票行情以上涨为主
       - +DI在-DI下方，股票行情以下跌为主
       - 在股票价格上涨行情中，当+DI向上交叉-DI，是买进信号，相反,当+DI向下交叉-DI，是卖出信号。
       - -DI从20以下上升到50以上,股票价格很有可能会有一波中级下跌行情。
       - +DI从20以下上升到50以上,股票价格很有可能会有一波中级上涨行情。
       - +DI和-DI以20为基准线上下波动时，该股票多空双方拉锯战,股票价格以箱体整理为主。
       - 当ADX脱离20－30之间上行，不论当时的行情是上涨或下跌，都预示股价将在一段时间维持原先的走势。
       - 当ADX位于＋DI与－DI下方，特别是在20之下时，表示股价已经陷入泥沼，应远离观望
       - 当绿色的ADXR曲线低于20时，所有指标都将失去作用，应果断离市。
       - 在一般的行情中，ADX的值高于50以上时，突然改变原来的上升态势调头向下，无论股价正在上涨还是下跌都代表行情即将发生反转。此后ADX往往会持续下降到20左右才会走平。但在极强的上涨行情中ADX在50以上发生向下转折，仅仅下降到40－60之间，随即再度回头上升，在此期间，股价并未下跌而是走出横盘整理的态势。随着ADX再度回升股价向上猛涨，这种现象称为"半空中转折"。也是大行情即将来临的征兆。但在实际操作中仍遵循ADX高于50以上发生向下转折，即抛出持股离场观望，在确认"半空中转折"成立后再跟进的原则
       - 当＋DI与-DI相交之后，ADX会随后与ADXR交叉，此时如果行情上涨，将是最后一次买入机会；如果行情下跌，将是最后一次卖出机会。如图所示，白色的+DI上穿黄色的-DI之后不久，紫色的ADX就上穿绿色的ADXR，随即股价开始大幅上扬。
    2. DMI数值 reflects当前趋势的强弱,通常:
       - DMI>50表示趋势明确
       - 两条DM交叉时可能发生趋势转向