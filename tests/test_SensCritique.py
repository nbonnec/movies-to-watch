import source.SensCritique
import unittest


class TestSensCritiqueMethods(unittest.TestCase):

    def test_get_count(self) -> None:
        self.assertEqual(source.SensCritique.get_page_count(), 9)


if __name__ == '__main__':
    unittest.main()
