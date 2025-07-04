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
        },
        "wildcard": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
        },
        "allocated": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
        },
        "fulfilled": {
            "AP": 0,
            "SP": 0,
            "DP": 0,
            "BA": 0,
            "BC": 0,
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
                if row == "fixed":
                    self.matrix["fulfilled"][item] += self.matrix[row][item]
                elif row == "allocated":
                    self.matrix["fulfilled"][item] += self.matrix[row][item]
        self.as_string

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
                self.matrix[a][b] = val
            else:
                self.message(f"Sorry, don't know what to do with [b={b}]")
        else:
            self.message(f"Sorry, don't know what to do with [a={a}]")
        self.as_string

    def get(self, a, b):
        return int(self.matrix[a][b])

    def toSummary(self):
        str = ""
        str += f"<li><tt>Attributes..... {self.get("fixed", "AP"):3d} | {self.get("wildcard", "AP"):3d} | {self.get("allocated", "AP"):3d} | {self.get("fulfilled", "AP"):3d}</tt></li>"
        str += f"<li><tt>Skills......... {self.get("fixed", "SP"):3d} | {self.get("wildcard", "SP"):3d} | {self.get("allocated", "SP"):3d} | {self.get("fulfilled", "SP"):3d}</tt></li>"
        str += f"<li><tt>Degrees........ {self.get("fixed", "DP"):3d} | {self.get("wildcard", "DP"):3d} | {self.get("allocated", "DP"):3d} | {self.get("fulfilled", "DP"):3d}</tt></li>"
        str += f"<li><tt>B/C............ {self.get("fixed", "BC"):3d} | {self.get("wildcard", "BC"):3d} | {self.get("allocated", "BC"):3d} | {self.get("fulfilled", "BC"):3d}</tt></li>"
        str += f"<li><tt>B/A............ {self.get("fixed", "BA"):3d} | {self.get("wildcard", "BA"):3d} | {self.get("allocated", "BA"):3d} | {self.get("fulfilled", "BA"):3d}</tt></li>"
        return str
