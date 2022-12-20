import copy
import math
import random

import backend.parser as parser


class Algorithm:
    """
    Base algorithm class
    """

    def __init__(self, Graph, workers_data: dict) -> None:
        self.Graph = Graph
        self.workers_data = workers_data
        self.wokrers_list = parser.preper_woreks(workers_data=workers_data)
        self.wn = len(workers_data)
        self.order = self.Graph.TOP_ORDER()
        self.preproces()

    def preproces(self):
        self.permutation = [[] for _ in range(self.wn + 1)]
        self.Z = []
        for _ in range(self.wn + 1):
            self.Z.append(0)

    def generate_permutation(self):
        iteracje = 1
        print("graph order: ", self.order)
        for e in self.order:
            if e == 0:
                continue

            USE_WORKERS = []
            ID_WORKERS = []

            for i in self.Graph.Res[e]:
                for k in range(1, self.wn + 1):
                    if i.id in self.wokrers_list[k - 1]:

                        if k not in USE_WORKERS:
                            ID_WORKERS.append(k)
                for _ in range(1, i.number + 1):
                    USE_WORKERS.append(ID_WORKERS.pop(0))
            iteracje += 1
            for m in USE_WORKERS:
                self.permutation[m].append(e)
        print(self.permutation)


def easy_asign(workers, Graph):
    a = []
    a.append([])
    for op in range(1, Graph.n + 1):
        USE_WORKERS = []
        FUNCTION_ID = []
        for r in Graph.Res[op]:
            r_id = r.id
            r_number = r.number
            ID_WORKERS = []
            for k in range(1, len(workers)):
                if r_id in workers[k - 1]:
                    if k not in USE_WORKERS:
                        ID_WORKERS.append(k)
            for _ in range(1, r_number + 1):
                if len(ID_WORKERS) == 0:
                    break
                USE_WORKERS.append(ID_WORKERS.pop(0))
                FUNCTION_ID.append(r_id)
        a.append({"USE_WORKERS": USE_WORKERS, "FUNCTION_ID": FUNCTION_ID})
    return a


def c_max(m, workers, Graph, a, pi):
    Z = [0 for _ in range(m + 1)]
    C = [0 for _ in range(Graph.n + 1)]
    for i in range(1, Graph.n + 1):
        op = pi[i]
        z = 0
        for j in a[op]["USE_WORKERS"]:
            z = max([z, Z[j]])
        for arc in Graph.Pred[op]:
            z = max([z, C[arc.nd] + arc.weight])

        z = z + Graph.p[op]
        C[op] = z
        for j in a[op]["USE_WORKERS"]:
            Z[j] = z
    return C


def c_max2(m, workers, Graph, a, pi):
    Z = [0 for _ in range(m + 1)]
    C = [0 for _ in range(Graph.n + 1)]  # momenty zakonczenia
    for i in range(1, Graph.n + 1):
        op = pi[i]
        z = 0
        for j in a[op]["USE_WORKERS"]:
            z = max([z, Z[j]])

        for nx in range(len(a[op]["USE_WORKERS"])):
            ky = a[op]["USE_WORKERS"][nx]
            fun_w = a[op]["FUNCTION_ID"][nx]
            if z == Z[ky]:
                for k in range(1, m + 1):
                    if k in a[op]["USE_WORKERS"]:
                        continue
                    if Z[k] >= z:
                        continue
                    if fun_w in workers[k - 1]:
                        a[op]["USE_WORKERS"][nx] = k
                        break
                    continue
        z = 0
        for j in a[op]["USE_WORKERS"]:
            z = max([z, Z[j]])
        for arc in Graph.Pred[op]:
            z = max([z, C[arc.nd] + arc.weight])
        z = z + Graph.p[op]
        C[op] = z
        for j in a[op]["USE_WORKERS"]:
            Z[j] = z
    return C, max(C)


def move_elem(l, oldindex, newindex):  # noqa
    l.insert(newindex, l.pop(oldindex))


def IS_TOP(pi, Graph):
    ps = [0 for _ in range(Graph.n + 1)]
    for i in range(1, Graph.n + 1):
        ps[pi[i]] = i
    # print("ps: ",ps)
    for nd in range(1, Graph.n + 1):
        for a in Graph.Succ[nd]:
            if ps[nd] > ps[a.nd]:
                return False
    return True


def insert_nbr(Graph, workers_list, ord):
    best_C, best_max_C = 0, 0
    a0 = easy_asign(Graph=Graph, workers=workers_list)

    C0, max_C0 = c_max2(
        m=len(workers_list), workers=workers_list, Graph=Graph, a=a0, pi=ord
    )

    best_C = C0
    best_max_C = max_C0
    best_ord = copy.deepcopy(ord)
    # print(best_ord)

    for i in range(1, len(ord)):
        for j in range(i + 1, len(ord)):
            move_elem(l=ord, oldindex=i, newindex=j)
            if IS_TOP(pi=ord, Graph=Graph) is False:
                move_elem(l=ord, oldindex=j, newindex=i)
                break
            else:
                a1 = 0
                C1, max_C1 = 0, 0

                a1 = easy_asign(Graph=Graph, workers=workers_list)

                C1, max_C1 = c_max2(
                    m=len(workers_list), workers=workers_list, Graph=Graph, a=a1, pi=ord
                )

                if best_max_C > max_C1:
                    best_max_C = max_C1
                    best_C = C1
                    best_ord = copy.deepcopy(ord)

                move_elem(l=ord, oldindex=j, newindex=i)
        for j in range(i - 1, 1, -1):
            move_elem(l=ord, oldindex=i, newindex=j)
            if IS_TOP(pi=ord, Graph=Graph) is False:
                move_elem(l=ord, oldindex=j, newindex=i)
                break
            else:
                a1 = 0
                C1, max_C1 = 0, 0

                a1 = easy_asign(Graph=Graph, workers=workers_list)

                C1, max_C1 = c_max2(
                    m=len(workers_list), workers=workers_list, Graph=Graph, a=a1, pi=ord
                )

                if best_max_C > max_C1:
                    best_max_C = max_C1
                    best_C = C1
                    best_ord = copy.deepcopy(ord)

                move_elem(l=ord, oldindex=j, newindex=i)
    return best_C, best_max_C, best_ord


def insert_rand(Graph, workers_list, ord):
    best_C, best_max_C = 0, 0
    a0 = easy_asign(Graph=Graph, workers=workers_list)

    C0, max_C0 = c_max2(
        m=len(workers_list), workers=workers_list, Graph=Graph, a=a0, pi=ord
    )

    best_C = C0
    best_max_C = 1000_000
    best_max_C = max_C0

    best_ord = copy.deepcopy(ord)
    i = random.randint(1, len(ord) - 1)
    for j in range(i + 1, len(ord)):
        move_elem(l=ord, oldindex=i, newindex=j)
        if IS_TOP(pi=ord, Graph=Graph) is False:
            move_elem(l=ord, oldindex=j, newindex=i)
            break
        else:
            a1 = 0
            C1, max_C1 = 0, 0

            a1 = easy_asign(Graph=Graph, workers=workers_list)

            C1, max_C1 = c_max2(
                m=len(workers_list), workers=workers_list, Graph=Graph, a=a1, pi=ord
            )

            if best_max_C > max_C1:
                best_max_C = max_C1
                best_C = C1
                best_ord = copy.deepcopy(ord)

            move_elem(l=ord, oldindex=j, newindex=i)
    for j in range(i - 1, 1, -1):
        move_elem(l=ord, oldindex=i, newindex=j)
        if IS_TOP(pi=ord, Graph=Graph) == False:  # noqa
            move_elem(l=ord, oldindex=j, newindex=i)
            # print("2")
            break
        else:
            a1 = 0
            C1, max_C1 = 0, 0

            a1 = easy_asign(Graph=Graph, workers=workers_list)

            C1, max_C1 = c_max2(
                m=len(workers_list), workers=workers_list, Graph=Graph, a=a1, pi=ord
            )

            if best_max_C > max_C1:
                best_max_C = max_C1
                best_C = C1
                best_ord = copy.deepcopy(ord)

            move_elem(l=ord, oldindex=j, newindex=i)
    return best_C, best_max_C, best_ord


def ds(ord, Graph, workers_list):
    best_ord = copy.deepcopy(ord)
    NX = 1000_000
    while True:
        best_C, best_max_C, best_ord = insert_nbr(
            Graph=Graph, workers_list=workers_list, ord=best_ord
        )
        if best_max_C < NX:
            NX = best_max_C
        else:
            break
    return best_C, best_max_C, best_ord


def random_serge(ord, Graph, workers_list):
    best_ord = copy.deepcopy(ord)
    NX = 1000_000
    for i in range(1000):
        best_C, best_max_C, best_ord = insert_rand(
            Graph=Graph, workers_list=workers_list, ord=best_ord
        )
        if best_max_C < NX:
            NX = best_max_C
    return best_C, best_max_C, best_ord


def symulowane_wyzazanie(pi, Graph, workers_list):
    t0 = 1000
    tk = 0.1
    lam = 0.995
    t = t0
    n = Graph.n
    m = len(workers_list)
    a0 = easy_asign(Graph=Graph, workers=workers_list)

    C0_best, Cmax_best = c_max2(m=m, workers=workers_list, Graph=Graph, a=a0, pi=pi)

    best_pi = []
    best_pi = copy.deepcopy(pi)
    while t > tk:
        l1 = random.randint(1, n)
        l2 = random.randint(1, n)
        C_tmp0, max_tmp0 = c_max2(m=m, workers=workers_list, Graph=Graph, a=a0, pi=pi)
        move_elem(l=pi, oldindex=l1, newindex=l2)
        if IS_TOP(pi=pi, Graph=Graph) is False:
            move_elem(l=pi, oldindex=l2, newindex=l1)
            continue
        else:
            C_tmp, max_tmp = c_max2(m=m, workers=workers_list, Graph=Graph, a=a0, pi=pi)
            if max_tmp < Cmax_best:
                C0_best = C_tmp
                Cmax_best = max_tmp
                # print("pom: ",Cmax_best)
                best_pi = copy.deepcopy(pi)
            if max_tmp > max_tmp0:
                delta = max_tmp - max_tmp0
                P = math.exp(-delta / t)
                Z = random.random()
                # if Z <= P:
                #     i = 0
                # else:
                #     move_elem(l=pi, oldindex=l2, newindex=l1)
                if Z > P:
                    move_elem(l=pi, oldindex=l2, newindex=l1)
        t = lam * t
    best_order = copy.deepcopy(best_pi)
    # print("end")
    return C0_best, Cmax_best, best_order, Graph
