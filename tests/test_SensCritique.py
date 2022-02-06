import source.SensCritique
import unittest


class TestSensCritiqueMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.sc = source.SensCritique.SensCritique(page='../resources/html/page-1.html')

    def test_get_count(self) -> None:
        self.assertEqual(self.sc.get_page_count(), 9)


if __name__ == '__main__':
    unittest.main()
