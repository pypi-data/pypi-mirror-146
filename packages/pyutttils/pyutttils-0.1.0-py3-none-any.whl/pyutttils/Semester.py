class Semester:

    def __init__(self, identifier: str):
        """
        Créée un semestre à partir d'une chaine de caractère ("P22, "P2022", "Automne 2022").
        Si l'année est au format court ("22"), alors l'année réelle sera 2022.

        :param str identifier: "P22", "P2022", "Automne 2022"
        """
        self.short_season = identifier[0]
        if self.short_season == "A":
            self.full_season = "Automne"
        if self.short_season == "P":
            self.full_season = "Printemps"

        if len(identifier) == 3:  # "P22"
            self.short_year = int(identifier[1:3])
            self.full_year = 2000 + self.short_year
        elif len(identifier) == 5:  # "P2022"
            self.full_year = int(identifier[1:])
            self.short_year = int(identifier[3:])
        else:  # "Printemps 2022"
            self.full_year = int(identifier.split(" ")[1])
            self.short_year = int(identifier.split(" ")[1][2:])
        self.long_code = self.short_season + str(self.full_year)
        self.full_name = self.full_season + " " + str(self.full_year)

    def __str__(self):
        return self.full_name

    def __sub__(self, other):
        if isinstance(other, Semester):
            semesters = 2 * (self.full_year - other.full_year)
            if semesters >= 0 and self.short_season != other.short_season:
                if self.short_season == "P" and other.short_season == "A":
                    semesters -= 1
                else:
                    semesters += 1
            elif semesters < 0:
                semesters = (other - self) * -1
            return semesters
        elif isinstance(other, int):
            if other < 0:
                return self.__add__(other * -1)
            semester = self
            for i in range(other):
                semester = semester.get_previous()
            return semester
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Semester):
            return self.full_name == other.full_name
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Semester):
            return self - other > 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Semester):
            return self - other < 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Semester):
            return not self.__gt__(other)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Semester):
            return not self.__lt__(other)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, int):
            if other < 0:
                return self.__sub__(other * -1)
            semester = self
            for i in range(other):
                semester = semester.get_next()
            return semester
        return NotImplemented

    def get_next(self):
        if self.short_season == "A":
            return Semester("P" + str(self.full_year + 1))
        else:
            return Semester("A" + str(self.full_year))

    def get_previous(self):
        if self.short_season == "A":
            return Semester("P" + str(self.full_year))
        else:
            return Semester("A" + str(self.full_year - 1))
