import unittest

from .task_3 import create_account, transfer_from_to


class Task3Test(unittest.TestCase):
    """
    Task 3: Accounts
    """
    def test_create_account(self):
        test_accs = {'jane doe': 20, 'test': 25}
        # test for name duplicates in accs
        self.assertEqual(create_account(test_accs, 'test', 25), {'jane doe': 20, 'test': 25})
        # test for negative balance in accs
        self.assertEqual(create_account(test_accs, 'john doe', -10), {'jane doe': 20, 'test': 25})
        # test account creation satisfying all conditions
        self.assertEqual(create_account(test_accs, 'john doe', 50), {'jane doe': 20, 'test': 25, 'john doe': 50})

    def test_transfer_from_to(self):
        transfer_accs = {'jane doe': 20, 'john doe': 50, 'test': 25}
        # test transfer function satisfying all conditions
        self.assertEqual(transfer_from_to(transfer_accs, 'john doe', 'jane doe', 15), {'jane doe': 35, 'john doe': 35,
                                                                                       'test': 25})
        # test account_from not in accs but account_to exist.
        self.assertEqual(transfer_from_to(transfer_accs, 'Bob', 'john doe', 50),
                         {'jane doe': 20, 'john doe': 50, 'test': 25})
        # test account_to not in accs but account_from exist
        self.assertEqual(transfer_from_to(transfer_accs, 'john doe', 'Bob Dylan', 50),
                         {'jane doe': 20, 'john doe': 50, 'test': 25})

        # test value more than the balance
        self.assertEqual(transfer_from_to(transfer_accs, 'john doe', 'jane doe', 60), {'jane doe': 20, 'john doe': 50,
                                                                                       'test': 25})
        # test transfer account value less than 0
        self.assertEqual(transfer_from_to(transfer_accs, 'john doe', 'jane doe', -10), {'jane doe': 20, 'john doe': 50,
                                                                                        'test': 25})


if __name__ == '__main__':
    unittest.main()

