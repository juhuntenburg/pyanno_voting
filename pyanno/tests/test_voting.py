import unittest
import numpy as np

from pyanno import voting
from pyanno.voting import MISSING_VALUE as MV


class TestVoting(unittest.TestCase):

    def test_labels_count(self):
        annotations = [
            [1,  2, MV, MV],
            [MV, MV,  3,  3],
            [MV,  1,  3,  1],
            [MV, MV, MV, MV],
        ]
        nclasses = 5
        expected = [0, 3, 1, 3, 0]
        result = voting.labels_count(annotations, nclasses)
        self.assertEqual(result, expected)

    def test_majority_vote(self):
        annotations = [
            [1, 2, 2, MV],
            [2, 2, 2, 2],
            [1, 1, 3, 3],
            [1, 3, 3, 2],
            [MV, 2, 3, 1],
            [MV, MV, MV, 3],
        ]
        expected = [2, 2, 1, 3, 1, 3]
        result = voting.majority_vote(annotations)
        self.assertEqual(expected, result)

    def test_majority_vote_empty_item(self):
        # Bug: majority vote with row of invalid annotations fails
        annotations = np.array(
            [[1, 2, 3],
             [MV, MV, MV],
             [1, 2, 2]]
        )
        expected = [1, MV, 2]
        result = voting.majority_vote(annotations)
        self.assertEqual(expected, result)

    def test_addition(self):
        self.assertEqual(1 + 2, 3)

    def test_float_addition(self):
        self.assertAlmostEqual(1.11 + 2.2, 3.3, 1)

    def test_array_addition(self):
	x = np.array([1, 1])
	y = np.array([2, 2])
	z = np.array([3, 3])
	np.testing.assert_array_equal(x + y, z)	
 
    def test_label_frequency(self):
        result = voting.labels_frequency([[1, 1, 2], [-1, 1, 2]], 4)
        nclasses = 4
        expected = np.array([ 0. , 0.6, 0.4, 0. ])
        np.testing.assert_array_almost_equal(result, expected)

    def test_raise_error_empty(self):
        with self.assertRaises(voting.PyannoValueError):
            voting.labels_count([], 2)
 
    def test_raise_error_empty(self):
        mv = -10
        with self.assertRaises(voting.PyannoValueError):
            voting.labels_count([mv, mv], 2, missing_value=mv)

    def test_labels_count_optional_mv(self):
	mv = 50
        annotations = [
            [1,  2, mv, mv],
            [mv, mv,  3,  3],
            [mv,  1,  3,  1],
            [mv, mv,mv, mv],
        ]
        nclasses = 5
        expected = [0, 3, 1, 3, 0]
        result = voting.labels_count(annotations, nclasses, missing_value=mv)
        self.assertEqual(result, expected)

    def test_majority_vote_optional_mv(self):
        mv = -999
        annotations = [
            [1, 2, 2, mv],
            [2, 2, 2, 2],
            [1, 1, 3, 3],
            [1, 3, 3, 2],
            [mv, 2, 3, 1],
            [mv, mv, mv, 3],
        ]
        expected = [2, 2, 1, 3, 1, 3]
        result = voting.majority_vote(annotations, missing_value=mv)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
