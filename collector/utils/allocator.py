class Allocator:
    """
        matrix example:
        to_allocate = wildcard + fixed
        fulfilled = allocated + fixed

    """
    matrix = {
        "fixed": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
            "OP": 0,
            "LP": 0,
        },
        "wildcard": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
            "OP": 0,
            "LP": 0,
        },
        "allocated": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
            "OP": 0,
            "LP": 0,
        },
        "experience": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
            "OP": 0,
            "LP": 0,
        },
        "total": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
            "OP": 0,
            "LP": 0,
        },
    }
    defstring = ""
    seprow = ";"
    sepelem = "."
    sepkeyval = "="

    def __init__(self):
        self.as_string

    def restore(self, str=''):
        self.defstring = str
        self.as_matrix

    def check(self):
        for row, values in self.matrix.items():
            for item, value in values.items():
                if row == "total":
                    self.matrix[row][item] = 0
        for row, values in self.matrix.items():
            for item, value in values.items():
                if row != "total":
                    if row in ["wildcard", "fixed"]:
                        self.matrix["total"][item] += self.matrix[row][item]
        self.as_string
        # print(self.defstring)

    @property
    def fulfilled(self):
        res = {"AP": 0, "DP": 0, "SP": 0, "BA": 0, "BC": 0}
        for row, values in self.matrix.items():
            for item, value in values.items():
                if row == "wildcard":
                    res[item] += int(self.matrix[row][item])
                elif row == "allocated":
                    res[item] -= int(self.matrix[row][item])
        return res["AP"] == 0 and res["SP"] == 0 and res["DP"] == 0 and res["BA"] == 0 and res["BC"] == 0

    def message(self, str):
        print(str)

    @property
    def as_string(self):
        elems = []
        for row, values in self.matrix.items():
            for item, value in values.items():
                if value != 0:
                    elems.append(f"{row}{self.sepelem}{item}{self.sepkeyval}{value}")
        self.defstring = self.seprow.join(elems)
        return self.defstring

    @property
    def as_matrix(self):
        for row, values in self.matrix.items():
            for item in values.keys():
                self.matrix[row][item] = 0
        if self.defstring != "":
            for elem in self.defstring.split(self.seprow):
                keyval = elem.split(self.sepkeyval)
                val = int(keyval[1])
                keyparts = keyval[0].split(self.sepelem)
                self.matrix[keyparts[0]][keyparts[1]] = val
        else:
            print("Nothing to do with empty defstring!")
        return self.matrix

    def set(self, val, a, b):
        if a in self.matrix.keys():
            if b in self.matrix[a].keys():
                self.matrix[a][b] = int(val)
            else:
                self.message(f"Sorry, don't know what to do with [b={b}]")
        else:
            self.message(f"Sorry, don't know what to do with [a={a}]")
        self.as_string

    def stack(self, val, a, b):
        if a in self.matrix.keys():
            if b in self.matrix[a].keys():
                self.matrix[a][b] = int(self.matrix[a][b]) + val
            else:
                self.message(f"Sorry, don't know what to do with [b={b}]")
        else:
            self.message(f"Sorry, don't know what to do with [a={a}]")
        self.as_string

    def stacks(self, vals=[], a=""):
        if len(vals) == 5:
            if a in self.matrix.keys():
                self.matrix[a]["AP"] = int(self.matrix[a]["AP"]) + vals[0]
                self.matrix[a]["SP"] = int(self.matrix[a]["SP"]) + vals[1]
                self.matrix[a]["DP"] = int(self.matrix[a]["DP"]) + vals[2]
                self.matrix[a]["BA"] = int(self.matrix[a]["BA"]) + vals[3]
                self.matrix[a]["BC"] = int(self.matrix[a]["BC"]) + vals[4]
            else:
                self.message(f"Sorry, don't know what to do with [a={a}]")
        else:
            self.message(f"Not enough values to proceed: {vals}")
        self.as_string

    def prune_row(self, a):
        if a in self.matrix.keys():
            for b in self.matrix[a].keys():
                self.matrix[a][b] = 0

    def prune_all(self):
        self.prune_row("fixed")
        self.prune_row("wildcards")
        self.prune_row("allocated")
        self.prune_row("experience")
        self.prune_row("total")

    def get(self, a, b) -> int:
        return int(self.matrix[a][b])

    def gets(self, a, b):
        return str(self.get(a, b))

    def toSummary(self):
        str = f"<tt>...............  FIX |  WIL |  ALL |  EXP  | TOT </tt><br/>"
        str += f"<tt>Attributes..... {self.get("fixed", "AP"): 4d} | {self.get("wildcard", "AP"): 4d} | {self.get("allocated", "AP"): 4d} | {self.get("experience", "AP"): 4d} | {self.get("total", "AP"): 4d}</tt><br/>"
        str += f"<tt>Skills......... {self.get("fixed", "SP"): 4d} | {self.get("wildcard", "SP"): 4d} | {self.get("allocated", "SP"): 4d} | {self.get("experience", "SP"): 4d} | {self.get("total", "SP"): 4d}</tt><br/>"
        str += f"<tt>Degrees........ {self.get("fixed", "DP"): 4d} | {self.get("wildcard", "DP"): 4d} | {self.get("allocated", "DP"): 4d} | {self.get("experience", "DP"): 4d} | {self.get("total", "DP"): 4d}</tt><br/>"
        str += f"<tt>B/A............ {self.get("fixed", "BA"): 4d} | {self.get("wildcard", "BA"): 4d} | {self.get("allocated", "BA"): 4d} | {self.get("experience", "BA"): 4d} | {self.get("total", "BA"): 4d}</tt><br/>"
        str += f"<tt>B/C............ {self.get("fixed", "BC"): 4d} | {self.get("wildcard", "BC"): 4d} | {self.get("allocated", "BC"): 4d} | {self.get("experience", "BC"): 4d} | {self.get("total", "BC"): 4d}</tt><br/>"
        str = str.replace(" ", "&nbsp;")
        return str
