# 导入函数库
from jqdata import *

# 均线
MA_WIN_1 = 10
MA_WIN_2 = 60


#  设置仓位管理系统。


# 初始化函数，设定基准等等
def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    # log.set_level('order', 'error')

    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱

    # 定时运行函数
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    run_daily(market_open, time='every_bar', reference_security='000300.XSHG')
    # run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')
    # 股票池 - 上证50
    # g.stock_pool = get_index_stocks("000016.XSHG", date=context.current_dt)
    g.stock_pool = '510300.XSHG'
    g.init_cash = context.portfolio.starting_cash  # 启动资金
    g.down_cross_signaled = []


# 开盘前运行函数  ，定义股票池
def before_market_open(context):
    look_ahead_n = max(MA_WIN_1, MA_WIN_2) + 1
    g.up_cross_signaled = set()
    g.down_cross_signaled = set()

    df = attribute_history(g.stock_pool, look_ahead_n, "1d", ["close"], skip_paused=True)  # 该函数返回结果不包括当天数据
    if len(df) != look_ahead_n:
        continue
    close = df["close"]
    ma_short = close.rolling(MA_WIN_1).mean()  # 短时均线
    ma_long = close.rolling(MA_WIN_2).mean()  # 长时均线
    uc_flags = (ma_short.shift(1) <= ma_long.shift(1)) & (ma_short > ma_long)  # 上穿标志
    dc_flags = (ma_short.shift(1) >= ma_long.shift(1)) & (ma_short < ma_long)  # 下穿标志
    # 股票列表
    if uc_flags.iloc[-1]:
        g.up_cross_signaled.add(g.stock_pool)
    # if dc_flags.iloc[-1]:
    #     g.down_cross_signaled.add(g.stock_pool)


# 开盘时运行函数，定义交易规则
def market_open(context):
    cur_dt = context.current_dt.date()  # 当前日期
    # p = context.portfolio  # 资金账户
    current_data = get_current_data()
    # open_price = current_data[code].day_open
    each_cash = g.init_cash * 0.3   # 每只股票分配的资金
    each_cash1 = g.init_cash * 0.6

    amount = context.portfolio.positions[g.stock_pool].total_amount
    cost = context.portfolio.positions[g.stock_pool].avg_cos
    p = get_current_data()[g.stock_pool].last_price

    # 买入均线金叉信号的持仓股 /1/3仓位
    for code in g.up_cross_signaled:
        if current_data[code].paused:
            continue
        order_value(code, each_cash)

    if amount > 0 and p >= cost * 1.1:
        order_value(g.stock_pool, each_cash1)  # 加仓，全部卖出
        if amount > 0 and p >= cost * 1.25:
            order_target(g.stock_pool, 0)  # 止盈一部分，全部卖出
    if amount > 0 and p <= cost * 0.9:
        order_target(g.stock_pool, 0)  # 止损，全部卖出



#
# 收盘后运行函数
# def after_market_close(context):





    # p = context.portfolio
    # pos_level = p.positions_value / p.total_value
    # record(pos_level=pos_level)
