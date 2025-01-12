import unittest

# FILLER CODE


def is_primzahl(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5 + 1)):
        if n % i == 0:
            return False
    return True


class PrimzahlTestCase(unittest.TestCase):
    def test_primzahl(self):
        primzahl = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for i in primzahl:
            self.assertTrue(is_primzahl(i), f"{i} ist keine Primzahl")

    def test_keine_primzahl(self):
        keine_primzahl = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
        for i in keine_primzahl:
            self.assertFalse(is_primzahl(i), f"{i} ist eine Primzahl")


def is_palindrom(s: str) -> bool:
    return s == s[::-1]


class PalindromTestCase(unittest.TestCase):
    def test_palindrom(self):
        palindrom = ["anna", "otto", "rentner", "lagerregal"]
        for i in palindrom:
            self.assertTrue(is_palindrom(i), f"{i} ist kein Palindrom")

    def test_kein_palindrom(self):
        kein_palindrom = ["test", "hallo", "welt", "python"]
        for i in kein_palindrom:
            self.assertFalse(is_palindrom(i), f"{i} ist ein Palindrom")
