BASE_URL = "https://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?"


class CourseSLN:
    def __init__(self, sln, quarter, year):
        self.sln = sln
        self.quarter = quarter
        self.year = year

        self.url = f"{BASE_URL}QTRYR={self.quarter}+{self.year}&SLN={self.sln}"
