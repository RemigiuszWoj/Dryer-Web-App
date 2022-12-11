import csv


class fileCsv:
    "csv file modifi class"

    def __init__(self, path: str) -> None:
        self.path = path
        self.read()

    def read(self) -> None:
        self.rows = []
        self.header = []
        with open(self.path, "r") as file:
            csvreader = csv.reader(file)
            self.header = next(csvreader)
            for row in csvreader:
                self.rows.append(row)

    def modifi(self, data: list, position="end") -> None:
        with open(self.path, "a") as file:
            if position == "end":
                for row in data:
                    for x in row:
                        file.write(str(x) + "; ")
                    file.write("\n")

    def write(self, data: list, position="end") -> None:
        with open(self.path, "") as file:
            if position == "end":
                for row in data:
                    for x in row:
                        file.write(str(x) + "; ")
                    file.write("\n")

    def write_difrent(self, data: list, path: str, position="end") -> None:
        with open(path, "") as file:
            if position == "end":
                for row in data:
                    for x in row:
                        file.write(str(x) + "; ")
                    file.write("\n")


class preprocesData(fileCsv):
    def split_header(self) -> None:
        header = self.header[0].split(";")
        header.pop()
        self.header = header

    def split_rows(self) -> None:
        split_rows = []
        rows = self.rows
        for row in rows:
            tmp = row[0].split(";")
            tmp.pop()
            split_rows.append(tmp)
        self.rows = split_rows

    def transpose(self) -> None:
        self.rows = [list(i) for i in zip(*self.rows)]

    def list_to_dict(self) -> None:
        self.file_to_dict = {
            self.header[i]: self.rows[i] for i in range(len(self.header))
        }

    def preper_file(self) -> None:
        self.split_header()
        self.split_rows()
        self.transpose()
        self.list_to_dict()
