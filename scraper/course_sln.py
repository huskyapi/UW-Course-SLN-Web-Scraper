BASE_URL = "https://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?"


class CourseSLN:
    def __init__(self, quarter, year, sln):
        self.sln = sln
        self.quarter = f"{quarter[:3].upper()}"
        self.year = year

        self.url = f"{BASE_URL}QTRYR={self.quarter}+{self.year}&SLN={self.sln}"
