# 导入聚宽函数库
import jqdata


# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 定义一个全局变量, 保存要操作的股票
    # 510300.XSHG 泸深300 ETF
    g.security = '510300.XSHG'
    # g.security = '002223.XSHE'
    # g.security = get_index_stocks('000300.XSHG')    # 沪深300
    # 设定沪深300作为基准
    # set_benchmark('002223.XSHE')
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)

    run_daily(handle_data, time='09:30')
    # run_daily(trade_data, time='14:50')


# def run_data(context):


# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context,data):
    tobuy = []
    # for stock in g.security
    security = g.security
    # 获取股票的收盘价
    close_data = attribute_history(security, 60, '1d', ['close'])
    close_data2 = attribute_history(security, 10, '1d', ['close'])
    # 取得过去21天的平均价格
    MA60 = close_data['close'].mean()
    MA20 = close_data2['close'].mean()
    # 取得上一时间点价格
    current_price = close_data['close'][-1]

    cash = context.portfolio.available_cash

    cash03 = cash / 3


    if (MA20 > MA60) and (cash > 0):
        order_value(security, cash03)
        log.info("Buying %s" % (security))
    # 如果上一时间点价格低于21天平均价, 则空仓卖出
    elif (MA60 > MA20) and context.portfolio.positions[security].closeable_amount > 0:
        # 卖出所有股票,使这只股票的最终持有量为0
        order_target(security, 0)
        # 记录这次卖出
        log.info("Selling %s" % (security))
    # 画出上一时间点价格
    # record(stock_price=current_price)


# def trade_data(context):
#     amount = context.portfolio.positions[g.security].total_amount
    cost = context.portfolio.positions[g.security].avg_cos
#     p = get_current_data()[g.security].last_price
#
#     if amount > 0 and p >= cost * 1.1:
#         order_value(g.stock_pool, each_cash1)  # 加仓，全部卖出
#         if amount > 0 and p >= cost * 1.25:
#             order_target(g.security, 0)  # 止盈一部分，全部卖出
#     if amount > 0 and p <= cost * 0.9:
#         order_target(g.security, 0)  # 止损，全部卖出
