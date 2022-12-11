import csv

from api.models import Worker


def manin() -> None:
    print("siema")
    initial_db()


def initial_db():
    initial_workers()


def initial_workers(path: str = "backend/workers.csv"):
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)

        Worker.objects.all().delete()

        for row in reader:
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
