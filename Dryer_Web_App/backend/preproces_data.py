import backend.parser as parser
import backend.graph as graph


def load_orders(orders_list: list) -> list:
    orders = parser.PARS_ORDERS(orders_list=orders_list)
    orders = parser.preper_orders(orders)
    return orders


def make_orders_list(orders) -> list:
    orders_list = []
    for i in range(0, len(orders)):
        orders_list.append(orders[i]["MODEL"])
    return orders_list

# def generate_full_graph():
    # orders = load_orders()
    # orders_list = make_orders_list(orders=orders)

    # GP = graph.CGraph(np=0)
    # job = 1
    # for model in orders_list:
    #     G = parser.PARSOWANIE_DANYCH(
    #         path =model, nr_job = job)
    #     GP.mergeGraf(G1=G)
    #     job += 1
    # return GP


def generate_full_graph_list(orders_list: list):
    G_list = []
    orders = load_orders(orders_list=orders_list)
    orders_list = make_orders_list(orders=orders)

    job = 1
    for model in orders_list:
        G = parser.PARSOWANIE_DANYCH(path=model, nr_job=job)
        G_list.append(G)
        job += 1
    return G_list

# def test_graph():
#     GP = graph.CGraph(np=0)
#     G = parser.PARSOWANIE_DANYCH(path ="dryer_35_t.csv", nr_job = 1)
#     G1 = parser.PARSOWANIE_DANYCH(path ="dryer_20_t.csv", nr_job = 2)
#     GP.mergeGraf(G1=G)
#     GP.mergeGraf(G1=G1)
#     return GP

# def get_job():
#     G_list = []
#     G = parser.PARSOWANIE_DANYCH(path ="dryer_35_t.csv", nr_job = 1)
#     G_list.append(G)
#     G1 = parser.PARSOWANIE_DANYCH(path ="dryer_20_t.csv", nr_job = 2)
#     G_list.append(G1)
#     G2 = parser.PARSOWANIE_DANYCH(path ="dryer_20_t.csv", nr_job = 3)
#     G_list.append(G2)
#     return G_list


def create_G(G_list, sequence, nb):
    GP = graph.CGraph(np=0)
    for i in range(1, nb+1):
        GP.mergeGraf(G1=G_list[sequence[i]-1])
    return GP
