import csv
from math import floor

import backend.algorithm as algorithm
import backend.parser as parser
import backend.preproces_data as preproces_data
import matplotlib.pyplot as plt
from api.models import Order, Worker


def make_harmonogram(sequence, NB, dyer_number):
    workers = Worker.objects.all()
    workers_data = parser.PARS_WORKERS(data_set=workers)
    wokrers_list = parser.preper_woreks(workers_data=workers_data)

    orders_list = Order.objects.all()
    G_list = preproces_data.generate_full_graph_list(orders_list=orders_list)
    G = preproces_data.create_G(G_list=G_list, sequence=sequence, nb=NB[dyer_number])
    ord = G.TOP_ORDER()
    C_best_sw, best_Cmax_sw, best_ord_sw = algorithm.ds(
        ord=ord, Graph=G, workers_list=wokrers_list
    )

    return C_best_sw, best_Cmax_sw, best_ord_sw, G


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
                utility_3=row[5],
            )
            worker.save()


def save_to_table(
    Kolejnosc,
    Rozpoczecie,
    Zakonczenie,
    Czas_trwania,
    Graph,
    Pracownicy,
    path="harmonogra_tabela.csv",
):

    my_data_file = open(path, "+w")
    my_data_file.write("LP;Operacja;Rozpocecie;Zakonczenie,Pracownicy;" + "\n")
    for i in range(1, len(Kolejnosc)):
        Workers = str(Pracownicy[i]).replace("[", "").replace("]", "")
        # print(f"{i};{Kolejnosc[i]};{Rozpoczecie[i]};{Zakonczenie[i]};{Workers};")
        my_data_file.write(
            f"{i};{Kolejnosc[i]};{Rozpoczecie[i]};{Zakonczenie[i]};{Workers};\n"  # noqa
        )
    my_data_file.close()


def print_harmonogram(sequence, NB, dyer_number, COLORS):
    save = True

    workers = Worker.objects.all()
    workers_data = parser.PARS_WORKERS(data_set=workers)
    wokrers_list = parser.preper_woreks(workers_data=workers_data)

    C_best_sw, best_Cmax_sw, best_ord_sw, Graph = make_harmonogram(
        sequence=sequence, NB=NB, dyer_number=dyer_number
    )

    m = len(wokrers_list)
    a0 = algorithm.easy_asign(Graph=Graph, workers=wokrers_list)
    C0_best, Cmax_best = algorithm.c_max2(
        m=m, workers=wokrers_list, Graph=Graph, a=a0, pi=best_ord_sw
    )

    Zakonczenia = C0_best
    Czas_trwania = Graph.p
    Rozpoczecie = [Zakonczenia[i] - Czas_trwania[i] for i in range(len(Zakonczenia))]

    Pracownicy = [a0[i]["USE_WORKERS"] for i in range(1, len(a0))]
    Pracownicy.insert(0, [])

    if save:
        save_to_table(
            Kolejnosc=best_ord_sw,
            Rozpoczecie=Rozpoczecie,
            Zakonczenie=Zakonczenia,
            Czas_trwania=Czas_trwania,
            Pracownicy=Pracownicy,
            Graph=Graph,
        )

    fig, ax = plt.subplots()

    for i in range(1, len(Rozpoczecie) - 1):
        for j in Pracownicy[i]:
            ax.hlines(j, Rozpoczecie[i], Zakonczenia[i], colors=COLORS[Graph.job[i]])
    ax.set_title("Harmonogram Czasu Pracy")
    ax.set_ylabel("Pracownik")
    ax.set_xlabel("Czas [h]")
    plt.show()


def initial_db():
    initial_workers()
    # initial_orders()


def number_of_job_to_order(jobs: list) -> list:
    output = []
    for job in jobs:
        if job == 0:
            output.append(0)
        else:
            tmp = job / 28
            if tmp % 1 == 0:
                tmp = floor(tmp)
            else:
                tmp = floor(tmp) + 1
            output.append(tmp)
    return output


def job_time_merger(job: list, time: list) -> list:
    merged = []
    for i in range(len(job)):
        merged.append((job[i], time[i]))
    return merged


def manin() -> None:
    print("siema")

    NB = [1, 2, 3, 4, 5, 6, 7, 8]

    sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # sequence = [0, 1, 2]

    orders_list = Order.objects.all()
    dyer_number = len(orders_list) - 1

    C_best_sw, best_Cmax_sw, best_ord_sw, Graph = make_harmonogram(
        sequence=sequence, NB=NB, dyer_number=dyer_number
    )

    dryer_number = number_of_job_to_order(best_ord_sw)

    # print(dryer_number)
    job_time = job_time_merger(job=dryer_number, time=C_best_sw)
    print(job_time)
