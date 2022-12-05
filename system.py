import numpy as np
from collections import deque

class JudgeSystem(object):
    def __init__(self):
        self.qEnter = deque()
        self.qExit = deque()
        self.highPrice = 0.0
        self.lowPrice = 0.0
        self.curLen = 0

    def updateState(self, curPrice):
        self.qEnter.append(curPrice)
        self.qExit.append(curPrice)
        return

    def getBuySignal(self) -> bool:
        if np.random.random() > 0.5:
            return True
        else:
            return False

    def getSellSignal(self) -> bool:
        if np.random.random() > 0.5:
            return True
        else:
            return False

class JudgeSystemOne(JudgeSystem):
    def __init__(self):
        super(JudgeSystemOne, self).__init__()
        self._previousBreakProfitable = False
        self._currentBreakProfitable = False
        self._N = 0.0
        self._buySignal = False
        self._sellSignal = False

    def updateState(self, curPrice):
        self._buySignal = False
        self._sellSignal = False
        if len(self.qEnter) < 20:
            self.qEnter.append(curPrice)
        else:
            ''' TODO 更新N'''
            if curPrice > np.max(self.qEnter):
                self._currentBreakProfitable = True
                if not self._previousBreakProfitable:
                    self._buySignal = True
            if curPrice < np.min(self.qEnter):
                self._currentBreakProfitable = False
            if curPrice >= np.min(self.qEnter) and curPrice <= np.max(self.qEnter):
                self._previousBreakProfitable = self._currentBreakProfitable

            self.qEnter.popleft()
            self.qEnter.append(curPrice)

        if len(self.qExit) < 10:
            self.qExit.append(curPrice)
        else:
            if curPrice < np.min(self.qExit):
                self._sellSignal = True
            self.qExit.popleft()
            self.qExit.append(curPrice)


    def getBuySignal(self) -> bool:
        return self._buySignal

    def getSellSignal(self) -> bool:
        return self._sellSignal


class JudgeSystemTwo(JudgeSystem):
    def __init__(self):
        super(JudgeSystemTwo, self).__init__()
        self._N = 0.0
        self._buySignal = False
        self._sellSignal = False

    def updateState(self, curPrice):
        self._buySignal = False
        self._sellSignal = False
        if len(self.qEnter) < 55:
            self.qEnter.append(curPrice)
        else:
            ''' TODO 更新N'''
            if curPrice > np.max(self.qEnter):
                self._buySignal = True

            self.qEnter.popleft()
            self.qEnter.append(curPrice)

        if len(self.qExit) < 20:
            self.qExit.append(curPrice)
        else:
            if curPrice < np.min(self.qExit):
                self._sellSignal = True
            self.qExit.popleft()
            self.qExit.append(curPrice)

    def getBuySignal(self) -> bool:
        return self._buySignal

    def getSellSignal(self) -> bool:
        return self._sellSignal


class buyPoint(object):
    def __init__(self, price, count, timeStamp, stopLossPoint):
        self.buyPointPrice = price
        self.count = count
        self.timeStamp = timeStamp
        self.stopLossPoint = stopLossPoint

class N(object):
    def __init__(self, total):
        self._N = 0.0
        self.list = []
        self.PDC = 0.0
        self.total = total

    def update(self, open, close, H, L):
        TR = max([H - L, H - self.PDC, self.PDC - L])
        self.PDC = close
        if len(self.list) <= 20:
            self.list.append(TR)
            self._N = np.mean(self.list)
        else:
            self._N = (19 * self._N + TR) / 20
        return self._N

    def getUnit(self):
        return self.total * 0.01 / (self._N * 1)

    def getN(self):
        return self._N
