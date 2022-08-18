import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
from pymongo import MongoClient


def stock_an(stock_list, number):
    stock = []
    for tmp in stock_list:
        stock.append(tmp[0:6] + tmp[7:])

    stock_number = len(stock)
    m = 0
    p = []
    sum = 0
    for i in number:
        sum = sum + float(i)
    for i in number:
        p.append(float(i) / sum)
    StockReturns = pd.DataFrame()
    length = 0
    client = MongoClient(host='localhost')
    db = client.Stocks
    x = 0
    while m < stock_number:
        tmp = db['%s' % (stock[m])]
        gap = []
        time = []
        for x in tmp.find({}, {"gap": 1, "tradeCode": 1, "_id": 0}):
            gap.append(x['gap'])
            time.append(x['tradeCode'])
        if length < len(time):
            StockReturns['date'] = time
            length = len(time)
        StockReturns[stock[m]] = gap
        m = m + 1
    StockReturns['date'] = pd.to_datetime(StockReturns['date'], format='%Y%m%d')
    StockReturns = StockReturns.dropna()
    StockReturns = StockReturns[StockReturns['date'] > '2019-1-1']
    StockReturns = StockReturns.set_index('date')

    numstocks = stock_number

    portfolio_weights = np.array(p)
    stock_return = StockReturns.copy()
    WeightedReturns = stock_return.mul(portfolio_weights, axis=1)
    StockReturns['Portfolio'] = WeightedReturns.sum(axis=1)
    StockReturns.Portfolio.plot()
    plt.savefig('组合收益.jpg')
    correlation_matrix = stock_return.corr()

    import seaborn as sns

    # 创建热图
    sns.heatmap(correlation_matrix,
                annot=True,
                cmap="YlGnBu",
                linewidths=0.3,
                annot_kws={"size": 8})

    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.savefig('static/热图.jpg')

    cov_mat = stock_return.cov()

    # 年化协方差矩阵
    cov_mat_annual = cov_mat * 252
    # 设置模拟的次数
    number = 10000
    # 设置空的numpy数组，用于存储每次模拟得到的权重、收益率和标准差
    random_p = np.empty((number, stock_number + 2))
    # 设置随机数种子，这里是为了结果可重复
    np.random.seed(123)

    # 循环模拟10000次随机的投资组合
    for i in range(number):
        random9 = np.random.random(stock_number)
        random_weight = random9 / np.sum(random9)
        mean_return = stock_return.mul(random_weight, axis=1).sum(axis=1).mean()
        annual_return = (1 + mean_return) ** 252 - 1
        random_volatility = np.sqrt(np.dot(random_weight.T,
                                           np.dot(cov_mat_annual, random_weight)))
        random_p[i][:stock_number] = random_weight
        random_p[i][stock_number] = annual_return
        random_p[i][stock_number + 1] = random_volatility

    # 将numpy数组转化成DataFrame数据框
    RandomPortfolios = pd.DataFrame(random_p)
    # 设置数据框RandomPortfolios每一列的名称
    RandomPortfolios.columns = [ticker + "_weight" for ticker in stock] \
                               + ['Returns', 'Volatility']

    # 找到标准差最小数据的索引值
    min_index = RandomPortfolios.Volatility.idxmin()

    # 在收益-风险散点图中突出风险最小的点
    RandomPortfolios.plot('Volatility', 'Returns', kind='scatter', alpha=0.3)
    x = RandomPortfolios.loc[min_index, 'Volatility']
    y = RandomPortfolios.loc[min_index, 'Returns']
    plt.scatter(x, y, color='red')
    plt.savefig('static/风险最小.jpg')
    GMV_weights = np.array(RandomPortfolios.iloc[min_index, 0:numstocks])
    StockReturns['Portfolio_GMV'] = stock_return.mul(GMV_weights, axis=1).sum(axis=1)
    risk_free = 0

    # 计算每项资产的夏普比率
    RandomPortfolios['Sharpe'] = (RandomPortfolios.Returns - risk_free) \
                                 / RandomPortfolios.Volatility

    # 绘制收益-标准差的散点图，并用颜色描绘夏普比率
    plt.scatter(RandomPortfolios.Volatility, RandomPortfolios.Returns,
                c=RandomPortfolios.Sharpe)
    plt.colorbar(label='Sharpe Ratio')
    plt.savefig('static/夏普比率.jpg')
    plt.clf()
    max_index = RandomPortfolios.Sharpe.idxmax()
    MSR_weights = np.array(RandomPortfolios.iloc[max_index, 0:numstocks])
    StockReturns['Portfolio_MSR'] = stock_return.mul(MSR_weights, axis=1).sum(axis=1)

    for name in ['Portfolio', 'Portfolio_GMV', 'Portfolio_MSR']:
        CumulativeReturns = StockReturns[name].cumsum()
        CumulativeReturns.plot(label=name)
    plt.legend()
    plt.savefig('static/累计收益.jpg')

    return {'your_weight': portfolio_weights, 'least_risk_weight': GMV_weights, 'highest_profit_weight': MSR_weights}
if __name__ == '__main__':
    stock=['000001.SZ','000002.SZ']
    number=[25,25]
    print(stock_an(stock,number))