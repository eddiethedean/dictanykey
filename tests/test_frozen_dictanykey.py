import unittest

from dictanykey.frozen_dictanykey import FrozenDictAnyKey as TestClass


class TestInit(unittest.TestCase):
    def test_hashable_keys(self):
        d = TestClass([(1, "one"), (2, "two"), (3, "three")])
        self.assertListEqual([1, 2, 3], d._get_keys_list())
        self.assertListEqual(["one", "two", "three"], d._get_values_list())

    def test_unhashable_keys(self):
        d = TestClass([([1], "one"), ([2], "two"), ([1, 2], "one two")])
        self.assertListEqual([[1], [2], [1, 2]], d._get_keys_list())
        self.assertListEqual(["one", "two", "one two"], d._get_values_list())

    def test_mixed_keys(self):
        d = TestClass([(1, "one"), ([2], "two"), (3, "three")])
        self.assertListEqual([1, [2], 3], d._get_keys_list())
        self.assertListEqual(["one", "two", "three"], d._get_values_list())

    def test_empty(self):
        d = TestClass()
        self.assertEqual(len(d), 0)
        self.assertListEqual([], d._get_keys_list())
        self.assertListEqual([], d._get_values_list())

    def test_dict_input(self):
        d = TestClass({1: "one", 2: "two"})
        self.assertListEqual([1, 2], d._get_keys_list())
        self.assertListEqual(["one", "two"], d._get_values_list())


class TestLen(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, "one"), (2, "two"), (3, "three")])
        self.assertEqual(len(d), 3)

    def test_unhashable(self):
        d = TestClass([([1], "one"), ([2], "two"), ([1, 2], "one two")])
        self.assertEqual(len(d), 3)

    def test_mix(self):
        d = TestClass([(1, "one"), ([2], "two"), (3, "three")])
        self.assertEqual(len(d), 3)

    def test_empty(self):
        d = TestClass()
        self.assertEqual(len(d), 0)


class TestIter(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, "one"), (2, "two"), (3, "three")])
        iterator = iter(d)
        zero = next(iterator)
        self.assertEqual(zero, 1)
        one = next(iterator)
        self.assertEqual(one, 2)
        two = next(iterator)
        self.assertEqual(two, 3)
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_unhashable(self):
        d = TestClass([([1], "one"), ([2], "two"), ([1, 2], "one two")])
        iterator = iter(d)
        zero = next(iterator)
        self.assertEqual(zero, [1])
        one = next(iterator)
        self.assertEqual(one, [2])
        two = next(iterator)
        self.assertEqual(two, [1, 2])
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_empty(self):
        d = TestClass()
        iterator = iter(d)
        with self.assertRaises(StopIteration):
            next(iterator)


class TestContains(unittest.TestCase):
    d = TestClass([(1, "one"), (2, "two"), ([1, 2], "one two")])

    def test_hashable(self):
        one_in = 1 in TestContains.d
        three_in = 3 in TestContains.d
        self.assertTrue(one_in)
        self.assertFalse(three_in)

    def test_unhashable(self):
        one_two_in = [1, 2] in TestContains.d
        one_one_in = [1, 1] in TestContains.d
        self.assertTrue(one_two_in)
        self.assertFalse(one_one_in)

    def test_dict_key(self):
        d = TestClass([({1: "one", 2: "two"}, 12)])
        two_one_in = {2: "two", 1: "one"} in d
        two_three_in = {2: "two", 3: "three"} in d
        self.assertTrue(two_one_in)
        self.assertFalse(two_three_in)


class TestGetItem(unittest.TestCase):
    d = TestClass(
        [(1, "one"), (2, "two"), ([1, 2], "one two"), ({1: "ONE", 2: "TWO"}, "ONE TWO")]
    )

    def test_hashable(self):
        value = TestGetItem.d[1]
        self.assertEqual(value, "one")

    def test_unhashable(self):
        value = TestGetItem.d[[1, 2]]
        self.assertEqual(value, "one two")

    def test_dict_key(self):
        value = TestGetItem.d[{2: "TWO", 1: "ONE"}]
        self.assertEqual(value, "ONE TWO")

    def test_key_error(self):
        with self.assertRaises(KeyError):
            TestGetItem.d[3]
        with self.assertRaises(KeyError):
            TestGetItem.d[{1: "ONE"}]


class TestKeysMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, "one"), (2, "two"), (3, "three")])
        self.assertListEqual([1, 2, 3], d._get_keys_list())

    def test_unhashable(self):
        d = TestClass([([1, 1], "one"), ([2, 8], "two"), ([3, 9], "three")])
        self.assertListEqual([[1, 1], [2, 8], [3, 9]], d._get_keys_list())

    def test_mix(self):
        d = TestClass([(1, "one"), ([2, 2], "two two"), (2, "two")])
        self.assertListEqual([1, [2, 2], 2], d._get_keys_list())

    def test_empty(self):
        d = TestClass([])
        self.assertListEqual([], d._get_keys_list())


class TestValuesMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, "one"), (2, "two"), (3, "three")])
        self.assertListEqual(["one", "two", "three"], d._get_values_list())

    def test_unhashable(self):
        d = TestClass([([1, 1], "one"), ([2, 8], "two"), ([3, 9], "three")])
        self.assertListEqual(["one", "two", "three"], d._get_values_list())

    def test_mix(self):
        d = TestClass([(1, "one"), ([2, 2], "two two"), (2, "two")])
        self.assertListEqual(["one", "two two", "two"], d._get_values_list())

    def test_empty(self):
        d = TestClass([])
        self.assertListEqual([], d._get_values_list())


class TestItemsMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, "one"), (2, "two"), (3, "three")])
        self.assertListEqual(
            [(1, "one"), (2, "two"), (3, "three")], d._get_items_list()
        )

    def test_unhashable(self):
        d = TestClass([([1, 1], "one"), ([2, 8], "two"), ([3, 9], "three")])
        self.assertListEqual(
            [([1, 1], "one"), ([2, 8], "two"), ([3, 9], "three")], d._get_items_list()
        )

    def test_mix(self):
        d = TestClass([(1, "one"), ([2, 2], "two two"), (2, "two")])
        self.assertListEqual(
            [(1, "one"), ([2, 2], "two two"), (2, "two")], d._get_items_list()
        )

    def test_empty(self):
        d = TestClass([])
        self.assertListEqual([], d._get_items_list())


class TestGetMethod(unittest.TestCase):
    d = TestClass(
        [(1, "one"), (2, "two"), ([1, 2], "one two"), ({1: "ONE", 2: "TWO"}, "ONE TWO")]
    )

    def test_hashable(self):
        value = TestGetMethod.d.get(1)
        self.assertEqual(value, "one")

    def test_unhashable(self):
        value = TestGetMethod.d.get([1, 2])
        self.assertEqual(value, "one two")

    def test_dict_key(self):
        value = TestGetMethod.d.get({2: "TWO", 1: "ONE"})
        self.assertEqual(value, "ONE TWO")

    def test_default(self):
        value = TestGetMethod.d.get(3, default="NaN")
        self.assertEqual(value, "NaN")
        value = TestGetMethod.d.get({1: "ONE"}, "Missing")
        self.assertEqual(value, "Missing")


class TestCopyMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, "one"), (2, "two"), (3, "three")])
        c = d.copy()
        self.assertTrue(d == c)

    def test_unhashable(self):
        d = TestClass([([1, 1], "one"), ([2, 8], "two"), ([3, 9], "three")])
        c = d.copy()
        self.assertTrue(d == c)

    def test_mix(self):
        d = TestClass([(1, "one"), ([2, 2], "two two"), (2, "two")])
        c = d.copy()
        self.assertTrue(d == c)


class TestHashMethod(unittest.TestCase):
    def test_hashable_keys(self):
        d1 = TestClass([(1, "one"), (2, "two")])
        d2 = TestClass([(1, "one"), (2, "two")])
        self.assertEqual(hash(d1), hash(d2))

    def test_different_order_same_hash(self):
        d1 = TestClass([(1, "one"), (2, "two")])
        d2 = TestClass([(2, "two"), (1, "one")])
        # Order should not affect hash for frozen dict
        self.assertEqual(hash(d1), hash(d2))

    def test_different_values_different_hash(self):
        d1 = TestClass([(1, "one"), (2, "two")])
        d2 = TestClass([(1, "ONE"), (2, "two")])
        self.assertNotEqual(hash(d1), hash(d2))

    def test_unhashable_keys(self):
        d1 = TestClass([([1], "one"), ([2], "two")])
        d2 = TestClass([([1], "one"), ([2], "two")])
        # FrozenDictAnyKey with unhashable keys cannot be hashed
        with self.assertRaises(TypeError):
            hash(d1)
        with self.assertRaises(TypeError):
            hash(d2)

    def test_mixed_keys(self):
        d1 = TestClass([(1, "one"), ([2], "two")])
        d2 = TestClass([(1, "one"), ([2], "two")])
        # FrozenDictAnyKey with mixed keys cannot be hashed due to unhashable keys
        with self.assertRaises(TypeError):
            hash(d1)
        with self.assertRaises(TypeError):
            hash(d2)

    def test_empty(self):
        d1 = TestClass()
        d2 = TestClass()
        self.assertEqual(hash(d1), hash(d2))


class TestImmutableOperations(unittest.TestCase):
    def test_setitem_raises_error(self):
        d = TestClass([(1, "one"), (2, "two")])
        with self.assertRaises(TypeError):
            d[3] = "three"

    def test_delitem_raises_error(self):
        d = TestClass([(1, "one"), (2, "two")])
        with self.assertRaises(TypeError):
            del d[1]

    def test_clear_raises_error(self):
        d = TestClass([(1, "one"), (2, "two")])
        with self.assertRaises(AttributeError):
            d.clear()

    def test_pop_raises_error(self):
        d = TestClass([(1, "one"), (2, "two")])
        with self.assertRaises(AttributeError):
            d.pop(1)

    def test_popitem_raises_error(self):
        d = TestClass([(1, "one"), (2, "two")])
        with self.assertRaises(AttributeError):
            d.popitem()

    def test_setdefault_raises_error(self):
        d = TestClass([(1, "one"), (2, "two")])
        with self.assertRaises(AttributeError):
            d.setdefault(3, "three")

    def test_update_raises_error(self):
        d = TestClass([(1, "one"), (2, "two")])
        with self.assertRaises(TypeError):
            d.update({3: "three"})


class TestEqMethod(unittest.TestCase):
    def test_equal_dicts(self):
        d1 = TestClass([(1, "one"), (2, "two"), ([1, 2], "one two")])
        d2 = TestClass([(1, "one"), (2, "two"), ([1, 2], "one two")])
        self.assertTrue(d1 == d2)

    def test_different_order(self):
        d1 = TestClass([(1, "one"), (2, "two")])
        d2 = TestClass([(2, "two"), (1, "one")])
        self.assertTrue(d1 == d2)  # Order should not matter for dict equality

    def test_different_values(self):
        d1 = TestClass([(1, "one"), (2, "two")])
        d2 = TestClass([(1, "ONE"), (2, "two")])
        self.assertFalse(d1 == d2)

    def test_regular_dict(self):
        d1 = TestClass([(1, "one"), (2, "two")])
        d2 = {1: "one", 2: "two"}
        self.assertTrue(d1 == d2)


class TestReprStrMethod(unittest.TestCase):
    def test_repr_hashable(self):
        d = TestClass([(1, "one"), (2, "two")])
        expected = "FrozenDictAnyKey([(1, 'one'), (2, 'two')])"
        self.assertEqual(repr(d), expected)

    def test_repr_unhashable(self):
        d = TestClass([([1], "one"), ([2], "two")])
        expected = "FrozenDictAnyKey([([1], 'one'), ([2], 'two')])"
        self.assertEqual(repr(d), expected)

    def test_str_hashable(self):
        d = TestClass([(1, "one"), (2, "two")])
        expected = "{1: 'one', 2: 'two'}"
        self.assertEqual(str(d), expected)

    def test_str_unhashable(self):
        d = TestClass([([1], "one"), ([2], "two")])
        expected = "{[1]: 'one', [2]: 'two'}"
        self.assertEqual(str(d), expected)
