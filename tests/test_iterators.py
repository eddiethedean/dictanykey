import unittest

from dictanykey.dictanykey import DictAnyKey
from dictanykey.iterators import DictItemIterator, DictKeyIterator, DictValueIterator


class TestDictKeyIterator(unittest.TestCase):
    def test_normal_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictKeyIterator(d)
        keys = list(iterator)
        self.assertEqual(keys, [1, 2, 3])

    def test_mutation_during_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictKeyIterator(d)
        next(iterator)  # Move to first item
        d[4] = "four"  # Mutate the dict
        with self.assertRaises(RuntimeError):
            next(iterator)

    def test_deletion_during_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictKeyIterator(d)
        next(iterator)  # Move to first item
        del d[2]  # Delete an item
        with self.assertRaises(RuntimeError):
            next(iterator)

    def test_empty_dict(self):
        d = DictAnyKey()
        iterator = DictKeyIterator(d)
        keys = list(iterator)
        self.assertEqual(keys, [])

    def test_unhashable_keys(self):
        d = DictAnyKey([([1], "one"), ([2], "two"), ([3], "three")])
        iterator = DictKeyIterator(d)
        keys = list(iterator)
        self.assertEqual(keys, [[1], [2], [3]])

    def test_mixed_keys(self):
        d = DictAnyKey([(1, "one"), ([2], "two"), (3, "three")])
        iterator = DictKeyIterator(d)
        keys = list(iterator)
        self.assertEqual(keys, [1, [2], 3])

    def test_iter_protocol(self):
        d = DictAnyKey([(1, "one"), (2, "two")])
        iterator = DictKeyIterator(d)
        self.assertEqual(iterator, iter(iterator))  # Should return self

    def test_multiple_iterations(self):
        d = DictAnyKey([(1, "one"), (2, "two")])
        iterator1 = DictKeyIterator(d)
        iterator2 = DictKeyIterator(d)
        # Each iterator should be independent
        next(iterator1)
        self.assertEqual(next(iterator2), 1)


class TestDictValueIterator(unittest.TestCase):
    def test_normal_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictValueIterator(d)
        values = list(iterator)
        self.assertEqual(values, ["one", "two", "three"])

    def test_mutation_during_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictValueIterator(d)
        next(iterator)  # Move to first item
        d[4] = "four"  # Mutate the dict
        with self.assertRaises(RuntimeError):
            next(iterator)

    def test_deletion_during_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictValueIterator(d)
        next(iterator)  # Move to first item
        del d[2]  # Delete an item
        with self.assertRaises(RuntimeError):
            next(iterator)

    def test_empty_dict(self):
        d = DictAnyKey()
        iterator = DictValueIterator(d)
        values = list(iterator)
        self.assertEqual(values, [])

    def test_unhashable_keys(self):
        d = DictAnyKey([([1], "one"), ([2], "two"), ([3], "three")])
        iterator = DictValueIterator(d)
        values = list(iterator)
        self.assertEqual(values, ["one", "two", "three"])

    def test_mixed_values(self):
        d = DictAnyKey([(1, [1]), (2, "two"), (3, {3: "three"})])
        iterator = DictValueIterator(d)
        values = list(iterator)
        self.assertEqual(values, [[1], "two", {3: "three"}])

    def test_iter_protocol(self):
        d = DictAnyKey([(1, "one"), (2, "two")])
        iterator = DictValueIterator(d)
        self.assertEqual(iterator, iter(iterator))  # Should return self


class TestDictItemIterator(unittest.TestCase):
    def test_normal_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictItemIterator(d)
        items = list(iterator)
        self.assertEqual(items, [(1, "one"), (2, "two"), (3, "three")])

    def test_mutation_during_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictItemIterator(d)
        next(iterator)  # Move to first item
        d[4] = "four"  # Mutate the dict
        with self.assertRaises(RuntimeError):
            next(iterator)

    def test_deletion_during_iteration(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator = DictItemIterator(d)
        next(iterator)  # Move to first item
        del d[2]  # Delete an item
        with self.assertRaises(RuntimeError):
            next(iterator)

    def test_empty_dict(self):
        d = DictAnyKey()
        iterator = DictItemIterator(d)
        items = list(iterator)
        self.assertEqual(items, [])

    def test_unhashable_keys(self):
        d = DictAnyKey([([1], "one"), ([2], "two"), ([3], "three")])
        iterator = DictItemIterator(d)
        items = list(iterator)
        self.assertEqual(items, [([1], "one"), ([2], "two"), ([3], "three")])

    def test_mixed_keys_values(self):
        d = DictAnyKey([(1, [1]), ([2], "two"), (3, {3: "three"})])
        iterator = DictItemIterator(d)
        items = list(iterator)
        expected = [(1, [1]), ([2], "two"), (3, {3: "three"})]
        self.assertEqual(items, expected)

    def test_iter_protocol(self):
        d = DictAnyKey([(1, "one"), (2, "two")])
        iterator = DictItemIterator(d)
        self.assertEqual(iterator, iter(iterator))  # Should return self

    def test_tuple_unpacking(self):
        d = DictAnyKey([(1, "one"), (2, "two")])
        iterator = DictItemIterator(d)
        key, value = next(iterator)
        self.assertEqual(key, 1)
        self.assertEqual(value, "one")


class TestIteratorEdgeCases(unittest.TestCase):
    def test_iterator_exhaustion(self):
        d = DictAnyKey([(1, "one")])
        iterator = DictKeyIterator(d)
        next(iterator)  # Consume the only item
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_iterator_reset_after_exhaustion(self):
        d = DictAnyKey([(1, "one"), (2, "two")])
        iterator = DictKeyIterator(d)
        list(iterator)  # Exhaust the iterator
        # Creating a new iterator should work
        new_iterator = DictKeyIterator(d)
        keys = list(new_iterator)
        self.assertEqual(keys, [1, 2])

    def test_concurrent_iterators(self):
        d = DictAnyKey([(1, "one"), (2, "two"), (3, "three")])
        iterator1 = DictKeyIterator(d)
        iterator2 = DictKeyIterator(d)

        # Both should start from the beginning
        self.assertEqual(next(iterator1), 1)
        self.assertEqual(next(iterator2), 1)

        # They should be independent
        self.assertEqual(next(iterator1), 2)
        self.assertEqual(next(iterator2), 2)

    def test_iterator_with_dict_modification_between_iterators(self):
        d = DictAnyKey([(1, "one"), (2, "two")])
        iterator1 = DictKeyIterator(d)
        next(iterator1)  # Move to first item

        # Modify dict
        d[3] = "three"

        # Create new iterator - should work fine
        iterator2 = DictKeyIterator(d)
        keys = list(iterator2)
        self.assertEqual(keys, [1, 2, 3])

        # But original iterator should fail on next access
        with self.assertRaises(RuntimeError):
            next(iterator1)

    def test_large_dataset_iteration(self):
        # Test with a larger dataset
        data = [(i, f"value_{i}") for i in range(1000)]
        d = DictAnyKey(data)
        iterator = DictKeyIterator(d)
        keys = list(iterator)
        self.assertEqual(len(keys), 1000)
        self.assertEqual(keys, list(range(1000)))

    def test_iterator_with_complex_keys(self):
        d = DictAnyKey(
            [
                ({"a": 1, "b": 2}, "dict1"),
                ([1, 2, 3], "list1"),
                ((1, 2), "tuple1"),
                ({"a": 1, "b": 2}, "dict1_duplicate"),
            ]
        )
        iterator = DictItemIterator(d)
        items = list(iterator)
        # The duplicate dict key should overwrite the first one, so we get 3 items
        self.assertEqual(len(items), 3)
        # Check that duplicate dict keys are handled correctly (second overwrites first)
        dict_items = [item for item in items if isinstance(item[0], dict)]
        self.assertEqual(len(dict_items), 1)
        self.assertEqual(dict_items[0][1], "dict1_duplicate")
