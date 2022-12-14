import csv
import backend.parser as parser
import backend.preproces_data as preproces_data
import backend.algorithm as algorithm

from api.models import Worker, Order


def manin() -> None:
    print("siema")

    NB = [2]
    # sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    sequence = [0, 1, 2]

    dyer_number = 0

    # C_best_sw, best_Cmax_sw, best_ord_sw, Graph = make_harmonogram(sequence=sequence, NB=NB, dyer_number=dyer_number)

    # initial_db()


# def make_harmonogram(sequence, NB, dyer_number):
    workers = Worker.objects.all()
    workers_data = parser.PARS_WORKERS(data_set=workers)
    wokrers_list = parser.preper_woreks(workers_data=workers_data)

    orders_list = Order.objects.all()
    G_list = preproces_data.generate_full_graph_list(orders_list=orders_list)
    G = preproces_data.create_G(G_list=G_list,
                                sequence=sequence,
                                nb=NB[dyer_number])
    ord = G.TOP_ORDER()
    C_best_sw, best_Cmax_sw, best_ord_sw = algorithm.ds(ord=ord,
                                                        Graph=G,
                                                        workers_list=wokrers_list)
    print(C_best_sw, best_Cmax_sw, best_ord_sw)


def initial_db():
    initial_workers()
    # initial_orders()


def initial_workers(path: str = "backend/workers.csv") -> None:
    with open(path) as file:
        workers_reader = csv.reader(file)
        next(workers_reader)
        Worker.objects.all().delete()

        for row in workers_reader:
            row = row[0].split(";")
            worker = Worker(
                lp=row[0],
                name=row[1],
                surname=row[2],
                utility_1=row[3],
                utility_2=row[4],
                utility_3=row[5])
            worker.save()
