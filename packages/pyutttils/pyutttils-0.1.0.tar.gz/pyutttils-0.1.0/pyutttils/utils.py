from datetime import date
from pyutttils.Semester import Semester


def get_current_semester() -> Semester:
    today = date.today()
    if today.month >= 2 or today.month <= 8:  # Printemps
        return Semester("P" + str(today.year))
    else:  # Automne
        if today.month == 1:
            return Semester("A" + str(today.year - 1))
        return Semester("A" + str(today.year))
