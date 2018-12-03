import unittest


from .task_1 import quick_sort


class Task1Test(unittest.TestCase):
    """
    Task 1: Quicksort
    """

    def test_quick_sort(self):
        # testing sort function
        self.assertEqual(quick_sort([5, 3, 2, 4, 1]), [1, 2, 3, 4, 5])
        # test for empty array
        self.assertEqual(quick_sort([]), [])
        # test for none input
        self.assertEqual(quick_sort(None), None)


if __name__ == '__main__':
    unittest.main()