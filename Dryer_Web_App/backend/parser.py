import data_csv
import graph

TRANSLATE_TABLE = {"K": 1, "E": 2, "U": 3, "W": 4, "S": 5, "C": 6, "-": 99}

MODEL_TABLE = {
    "dryer_20_t": "dryer_20_t.csv",
    "dryer_35_t": "dryer_35_t.csv",
    "dryer_50_t": "dryer_50_t.csv",
}


def chat_to_int(umiejetnosc: str) -> int:
    return TRANSLATE_TABLE[umiejetnosc]


def PARSOWANIE_DANYCH(path: str = "dryer_50_t.csv", nr_job=0):

    file = data_csv.preprocesData(path=path)
    file.preper_file()

    G = graph.CGraph(len(file.file_to_dict["lp"]))

    for i in range(G.n):
        G.job[i + 1] = nr_job

    for i in range(G.n):
        G.p[i + 1] = int(file.file_to_dict["Czas wykonania"][i])

    stringSeparators = [" and "]
    for i in range(1, G.n + 1, 1):
        sp = file.file_to_dict["Wymaga zakonczenia"][i - 1].split(*stringSeparators)

        for s in sp:
            spx = s.split("(")
            nd = int(spx[0])

            if nd == 0:
                continue
            weight = int(eval(spx[1].replace(")", "")))
            a = graph.CArc(nd=i, weight=weight)
            G.Succ[nd].append(a)
            b = graph.CArc(nd=nd, weight=weight)
            G.Pred[i].append(b)

        sp = file.file_to_dict["Pracownicy"][i - 1].split(" ")

        for s in sp:
            if s == "":
                continue
            spx = s.split("x")
            nbr = int(spx[0])
            id = str(spx[1])
            id = chat_to_int(id)

            r = graph.CRes(id=id, number=nbr)
            G.Res[i].append(r)
    return G


def type_to_csv(model: str) -> int:
    return MODEL_TABLE[model]


def PARS_WORKERS(path: str = "workers.csv"):
    file = data_csv.preprocesData(path=path)
    file.preper_file()
    data_set = file.file_to_dict
    workers = []
    for i in range(0, len(data_set["LP"])):
        workers.append(
            {
                "LP": i + 1,
                "IMIE": data_set["IMIE"][i],
                "NAZWISKO": data_set["NAZWISKO"][i],
                "UMIEJETNOSC_1": data_set["UMIEJETNOSC_1"][i],
                "UMIEJETNOSC_2": data_set["UMIEJETNOSC_2"][i],
                "UMIEJETNOSC_3": data_set["UMIEJETNOSC_3"][i],
            }
        )

    for i in range(0, len(data_set["LP"])):
        workers[i]["UMIEJETNOSC_1"] = chat_to_int(workers[i]["UMIEJETNOSC_1"])
        workers[i]["UMIEJETNOSC_2"] = chat_to_int(workers[i]["UMIEJETNOSC_2"])
        workers[i]["UMIEJETNOSC_3"] = chat_to_int(workers[i]["UMIEJETNOSC_3"])
    return workers


def PARS_ORDERS(path: str = "orders.csv"):
    file = data_csv.preprocesData(path=path)
    file.preper_file()
    data_set = file.file_to_dict
    orders = []
    for i in range(0, len(data_set["LP"])):
        orders.append(
            {
                "LP": i + 1,
                "NAZWA_FIRMY": data_set["NAZWA_FIRMY"][i],
                "MODEL": data_set["MODEL"][i],
            }
        )
    return orders


def preper_orders(orders):
    for i in range(0, len(orders)):
        orders[i]["MODEL"] = type_to_csv(orders[i]["MODEL"])
        # print(orders)
    return orders


def preper_woreks(workers_data: dict) -> list:
    wokrers_list = []
    for i in range(0, len(workers_data)):
        tmp = []
        if workers_data[i]["UMIEJETNOSC_1"] != 99:
            tmp.append(workers_data[i]["UMIEJETNOSC_1"])
        if workers_data[i]["UMIEJETNOSC_2"] != 99:
            tmp.append(workers_data[i]["UMIEJETNOSC_2"])
        if workers_data[i]["UMIEJETNOSC_3"] != 99:
            tmp.append(workers_data[i]["UMIEJETNOSC_3"])
        wokrers_list.append(tmp)
    return wokrers_list
