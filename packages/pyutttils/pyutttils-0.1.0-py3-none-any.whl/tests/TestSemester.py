import unittest

from pyutttils.Semester import Semester


class TestSemester(unittest.TestCase):

    def test_semester(self):
        self.assertEqual(Semester("P22").full_name, "Printemps 2022")

    def test_semester_next(self):
        self.assertEqual(Semester("P22").get_next().full_name, "Automne 2022")

    def test_semester_previous(self):
        self.assertEqual(Semester("P22").get_previous().full_name, "Automne 2021")

    def test_semester_add(self):
        self.assertEqual((Semester("P22") + 3).full_name, "Automne 2023")

    def test_semester_add_negative(self):
        self.assertEqual((Semester("P22") + (-3)).full_name, "Automne 2020")

    def test_semester_sub(self):
        self.assertEqual((Semester("P22") - 3).full_name, "Automne 2020")

    def test_semester_sub_semester(self):
        self.assertEqual(Semester("A23") - Semester("P22"), 3)

    def test_semester_sub_semester_negative(self):
        self.assertEqual(Semester("P22") - Semester("A23"), -3)

    def test_semester_sub_semester_negative_same_year(self):
        self.assertEqual(Semester("P22") - Semester("A22"), -1)

    def test_semester_sub_negative(self):
        self.assertEqual((Semester("P22") - (-3)).full_name, "Automne 2023")

    def test_gt(self):
        self.assertTrue(Semester("P22") > Semester("A21"))

    def test_gt_false(self):
        self.assertFalse(Semester("P22") > Semester("A22"))

    def test_gt_false_eq(self):
        self.assertFalse(Semester("P22") > Semester("P22"))

    def test_ge(self):
        self.assertTrue(Semester("P23") >= Semester("P22"))

    def test_ge_eq(self):
        self.assertTrue(Semester("P22") >= Semester("P22"))

    def test_ge_false(self):
        self.assertFalse(Semester("P22") >= Semester("A22"))

    def test_eq(self):
        self.assertTrue(Semester("P22") == Semester("P22"))

    def test_eq_false(self):
        self.assertFalse(Semester("P23") == Semester("P22"))

    def test_lt(self):
        self.assertTrue(Semester("A21") < Semester("P22"))

    def test_lt_false(self):
        self.assertFalse(Semester("A22") < Semester("P22"))

    def test_lt_false_eq(self):
        self.assertFalse(Semester("P22") < Semester("P22"))

    def test_le(self):
        self.assertTrue(Semester("P22") <= Semester("P23"))

    def test_le_eq(self):
        self.assertTrue(Semester("P22") <= Semester("P22"))

    def test_le_false(self):
        self.assertFalse(Semester("A22") <= Semester("P22"))


if __name__ == '__main__':
    unittest.main()
