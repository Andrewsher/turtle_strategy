import pandas as pd
from system import JudgeSystemOne, JudgeSystemTwo, buyPoint, N

def main():
    path = 'BrentOilPrices.csv'
    initCash = 100000
    countUpperBound = 4

    cash = initCash
    buyList1 = []
    buyList2 = []

    sys1 = JudgeSystemOne()
    sys2 = JudgeSystemTwo()
    n = N(cash)

    df = pd.read_csv(path)
    prices = df['Price'].values
    dates = df['Date'].values
    for i in range(len(prices) - 200, len(prices)):
        ''' 扫描止损点 '''
        for buyPointNode in buyList1:
            if prices[i] <= buyPointNode.stopLossPoint:
                cash += prices[i] * buyPointNode.count
                cash -= prices[i] * buyPointNode.count * 0.001
                print(f"止损：卖出{buyPointNode.count}单位原油，单价{prices[i]}，总计{buyPointNode.count * prices[i]}。成本价{buyPointNode.buyPointPrice}，收益{buyPointNode.count * (prices[i] - buyPointNode.buyPointPrice)}，剩余现金{cash}")
                buyList1.remove(buyPointNode)

        for buyPointNode in buyList2:
            if prices[i] <= buyPointNode.stopLossPoint:
                cash += prices[i] * buyPointNode.count
                cash -= prices[i] * buyPointNode.count * 0.001
                print(
                    f"止损：卖出{buyPointNode.count}单位原油，单价{prices[i]}，总计{buyPointNode.count * prices[i]}。成本价{buyPointNode.buyPointPrice}，收益{buyPointNode.count * (prices[i] - buyPointNode.buyPointPrice)}，剩余现金{cash}")
                buyList2.remove(buyPointNode)

        ''' 更新N '''
        n.update(prices[i],prices[i],prices[i],prices[i])

        sys1.updateState(prices[i])
        if sys1.getBuySignal() and len(buyList1) + len(buyList2) < countUpperBound and cash - prices[i] * n.getUnit() > 0:
            for buyPointNode in buyList1:
                buyPointNode.stopLossPoint += n.getN()
            buyList1.append(buyPoint(prices[i], int(n.getUnit()), dates[i], stopLossPoint=prices[i]-2*n.getN()))
            cash -= prices[i] * n.getUnit()
            cash -= prices[i] * n.getUnit() * 0.001
            print(f"系统1：在{dates[i]}买入{int(n.getUnit())}1单位的原油，单价{prices[i]}，花费{prices[i] * n.getUnit()}，剩余现金{cash}")
        if sys1.getSellSignal():
            for buyPointNode in buyList1:
                cash += buyPointNode.count * prices[i]
                cash -= buyPointNode.count * prices[i] * 0.001
                print(f"系统1:在{dates[i]}卖出{buyPointNode.count}单位的原油，单价{prices[i]}，总计{prices[i] * buyPointNode.count}。成本价{buyPointNode.buyPointPrice}，该笔交易收益{buyPointNode.count * (prices[i] - buyPointNode.buyPointPrice)}，剩余现金{cash}")
            buyList1.clear()

        sys2.updateState(prices[i])
        if sys2.getBuySignal() and not sys1.getBuySignal() and len(buyList1) + len(buyList2) < countUpperBound and cash - prices[i] * n.getUnit() > 0:
            for buyPointNode in buyList2:
                buyPointNode.stopLossPoint += n.getN()
            buyList2.append(buyPoint(prices[i], int(n.getUnit()), dates[i], stopLossPoint=prices[i] - 2 * n.getN()))
            cash -= prices[i] * n.getUnit()
            cash -= prices[i] * n.getUnit() * 0.001
            print(f"系统2：在{dates[i]}买入{int(n.getUnit())}单位的原油，单价{prices[i]}，花费{prices[i] * n.getUnit()}，剩余现金{cash}")
        if sys2.getSellSignal():
            for buyPointNode in buyList2:
                cash += buyPointNode.count * prices[i]
                cash -= buyPointNode.count * prices[i] * 0.001
                print(f"系统1:在{dates[i]}卖出{buyPointNode.count}单位的原油，单价{prices[i]}，总计{prices[i] * buyPointNode.count}。成本价{buyPointNode.buyPointPrice}，该笔交易收益{buyPointNode.count * (prices[i] - buyPointNode.buyPointPrice)}，剩余现金{cash}")
            buyList2.clear()

    print(f"剩余现金：{cash}")
    count = 0
    for buyPointNode in buyList1:
        count += buyPointNode.count
    for buyPointNode in buyList2:
        count += buyPointNode.count
    print(f"持有原油：{count}单位，单价{prices[-1]}，总价值{count * prices[-1]}")
    print(f"总身家：{cash + count * prices[-1]}")
    print(f"收益率：{(cash + count * prices[-1]) / initCash * 100 - 100}%")

main()
