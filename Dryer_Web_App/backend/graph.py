from collections import deque
from copy import deepcopy


class CArc:
    """
    CArc class;
    :param: nd;
    :param: weight;
    """

    def __init__(self, nd: int = 0, weight: int = 0) -> None:
        self.nd = nd
        self.weight = weight


class CRes:
    """
    CRes class;
    :param: id;
    :param: number;
    """

    def __init__(self, id: int = 0, number: int = 0) -> None:
        self.id = id
        self.number = number


class CGraph:
    """
    CGraph class;
    :param: n;
    :param: Succ;
    :param: Pred;
    :param: Res;
    """

    def __init__(self, np: int = 0) -> None:

        self.n = np
        self.Succ = list()
        self.Pred = list()
        self.Res = list()
        self.p = list()
        self.job = list()

        for _ in range(self.n + 1):
            self.Succ.append([])

        for _ in range(self.n + 1):
            self.Pred.append([])

        for _ in range(self.n + 1):
            self.Res.append([])

        for _ in range(self.n + 1):
            self.p.append(0)

        for _ in range(self.n + 1):
            self.job.append(0)

    def TOP_ORDER(self) -> list:
        LP = [None] * (self.n + 1)
        for i in range(1, self.n + 1, 1):
            LP[i] = len(self.Pred[i])

        Q = deque()
        for i in range(1, self.n + 1, 1):
            if LP[i] == 0:
                Q.appendleft(i)

        ORD = []
        ORD.append(0)
        while len(Q) > 0:
            nd = Q.pop()
            ORD.append(nd)
            for arc in self.Succ[nd]:
                LP[arc.nd] = LP[arc.nd] - 1
                if LP[arc.nd] == 0:
                    Q.appendleft(arc.nd)
        return ORD

    def mergeGraf(self, G1) -> None:
        for i in range(1, len(G1.p)):
            self.p.append(G1.p[i])
            self.job.append(G1.job[i])
            self.Res.append(G1.Res[i])

        for i in range(1, len(G1.Succ)):
            pom = []
            pom = deepcopy(G1.Succ[i])
            for j in range(0, len(pom)):
                pom[j].nd = pom[j].nd + self.n
            self.Succ.append(pom)

        for i in range(1, len(G1.Pred)):
            pom = []
            pom = deepcopy(G1.Pred[i])
            for j in range(0, len(pom)):
                pom[j].nd = pom[j].nd + self.n
            self.Pred.append(pom)
        self.n += G1.n
