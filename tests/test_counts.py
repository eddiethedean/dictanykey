import unittest

from dictanykey.counts import value_counts
from dictanykey.dictanykey import DictAnyKey


class TestValueCounts(unittest.TestCase):
    def test_hashable_values(self):
        values = [4, 1, 1, 4, 5, 1]
        result = value_counts(values)
        expected = DictAnyKey([(1, 3), (4, 2), (5, 1)])
        self.assertEqual(result, expected)

    def test_unhashable_values(self):
        values = [[1], [2], [1], [3], [2], [1]]
        result = value_counts(values)
        expected = DictAnyKey([([1], 3), ([2], 2), ([3], 1)])
        self.assertEqual(result, expected)

    def test_mixed_values(self):
        values = [1, [2], 1, [2], "three", 1]
        result = value_counts(values)
        expected = DictAnyKey([(1, 3), ([2], 2), ("three", 1)])
        self.assertEqual(result, expected)

    def test_empty_values(self):
        values = []
        result = value_counts(values)
        expected = DictAnyKey([])
        self.assertEqual(result, expected)

    def test_single_value(self):
        values = [42]
        result = value_counts(values)
        expected = DictAnyKey([(42, 1)])
        self.assertEqual(result, expected)

    def test_all_same_values(self):
        values = [1, 1, 1, 1]
        result = value_counts(values)
        expected = DictAnyKey([(1, 4)])
        self.assertEqual(result, expected)

    def test_sort_false(self):
        values = [4, 1, 1, 4, 5, 1]
        result = value_counts(values, sort=False)
        # Order should be insertion order
        expected_keys = [4, 1, 5]
        actual_keys = result._get_keys_list()
        self.assertEqual(actual_keys, expected_keys)

    def test_ascending_false(self):
        values = [4, 1, 1, 4, 5, 1]
        result = value_counts(values, ascending=False)
        expected = DictAnyKey([(1, 3), (4, 2), (5, 1)])
        self.assertEqual(result, expected)

    def test_ascending_true(self):
        values = [4, 1, 1, 4, 5, 1]
        result = value_counts(values, ascending=True)
        expected = DictAnyKey([(5, 1), (4, 2), (1, 3)])
        self.assertEqual(result, expected)

    def test_sort_false_ascending_ignored(self):
        values = [4, 1, 1, 4, 5, 1]
        result = value_counts(values, sort=False, ascending=False)
        # When sort=False, ascending should be ignored
        expected_keys = [4, 1, 5]
        actual_keys = result._get_keys_list()
        self.assertEqual(actual_keys, expected_keys)

    def test_string_values(self):
        values = ["apple", "banana", "apple", "cherry", "banana", "apple"]
        result = value_counts(values)
        expected = DictAnyKey([("apple", 3), ("banana", 2), ("cherry", 1)])
        self.assertEqual(result, expected)

    def test_none_values(self):
        values = [None, 1, None, 2, None]
        result = value_counts(values)
        expected = DictAnyKey([(None, 3), (1, 1), (2, 1)])
        self.assertEqual(result, expected)

    def test_dict_values(self):
        values = [{"a": 1}, {"b": 2}, {"a": 1}, {"c": 3}, {"b": 2}]
        result = value_counts(values)
        expected = DictAnyKey([({"a": 1}, 2), ({"b": 2}, 2), ({"c": 3}, 1)])
        self.assertEqual(result, expected)

    def test_tuple_values(self):
        values = [(1, 2), (3, 4), (1, 2), (5, 6), (1, 2)]
        result = value_counts(values)
        expected = DictAnyKey([((1, 2), 3), ((3, 4), 1), ((5, 6), 1)])
        self.assertEqual(result, expected)

    def test_large_dataset(self):
        # Test with a larger dataset to ensure performance
        values = list(range(100)) + list(range(50)) + list(range(25))
        result = value_counts(values)
        self.assertEqual(len(result), 100)  # Should have 100 unique values
        # Check some specific counts
        self.assertEqual(result[0], 3)  # 0 appears 3 times
        self.assertEqual(result[99], 1)  # 99 appears 1 time
        self.assertEqual(result[49], 2)  # 49 appears 2 times

    def test_return_type(self):
        values = [1, 2, 1]
        result = value_counts(values)
        self.assertIsInstance(result, DictAnyKey)

    def test_iterable_input(self):
        # Test with different iterable types
        values = (1, 2, 1, 3, 2)  # tuple
        result = value_counts(values)
        expected = DictAnyKey([(1, 2), (2, 2), (3, 1)])
        self.assertEqual(result, expected)

    def test_generator_input(self):
        # Test with generator
        def value_gen():
            yield 1
            yield 2
            yield 1
            yield 3

        result = value_counts(value_gen())
        expected = DictAnyKey([(1, 2), (2, 1), (3, 1)])
        self.assertEqual(result, expected)
