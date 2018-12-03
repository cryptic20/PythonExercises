import unittest

from .task_4 import swap_case


class Task4Test(unittest.TestCase):
    """
    Task 4: Swap case
    """

    def test_swap_case(self):
        # test for none input
        self.assertEqual(swap_case(None), None)
        # test for empty string. Assuming it will return an empty string as well.
        self.assertEqual(swap_case(''), '')
        # test for numbers in string. Assuming the code will ignore numbers in the string input.
        self.assertEqual(swap_case('The 2nd dog has a BONE'), 'tHE 2ND DOG HAS A bone')
        # test for special characters. Assuming they will also get ignored in the string input.
        self.assertEqual(swap_case('$$The dog has a bone!'), '$$tHE DOG HAS A bone!')
        # test for all conditions satisfied.
        self.assertEqual(swap_case('The dog has a BONE'), 'tHE DOG HAS A bone')


if __name__ == '__main__':
    unittest.main()