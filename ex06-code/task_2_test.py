import unittest

from .task_2 import list_duplicates


class Task2Test(unittest.TestCase):
    """
    Task 2: List duplicates
    """
    def test_list_duplicates(self):
        # test function
        self.assertEqual(list_duplicates([1, 2, 1, 2, 3, 4, 5, 6, 7, 4]), [(1, (0, 2)), (2, (1, 3)), (4, (5, 9))])
        # test for empty array input
        self.assertEqual(list_duplicates([]), [])
        # test for none input
        self.assertEqual(list_duplicates(None), None)


if __name__ == '__main__':
    unittest.main()
