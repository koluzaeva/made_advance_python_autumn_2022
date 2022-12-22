'''Tests for Stats class'''

import unittest
import time
from stat_classes import Stats


class TestMyClass(unittest.TestCase):
    """Tests"""

    def test_stat(self):
        '''tests for stat collect'''

        def foo():
            time.sleep(0.5)
            return 5

        with Stats.timer("foo"):  # 0.5
            res = foo()  # 5
        Stats.timer("foo").add()  # 0.3
        Stats.count("foo").add()
        Stats.avg("foo").add(res)

        Stats.count("foo").add()
        Stats.avg("foo").add(res)

        Stats.count("new_func").add()
        Stats.avg("new_func").add(0.7)

        Stats.count("no_used")  # не попадет в результат collect

        metrics = Stats.collect()

        self.assertEqual(round(metrics['foo.timer'], 1), 0.5, "Wrong value")
        self.assertEqual(metrics['foo.avg'], 5.0, "Wrong value")
        self.assertEqual(metrics['foo.avg'], 5.0, "Wrong value")
        self.assertEqual(metrics['new_func.avg'], 0.7, "Wrong value")
        self.assertEqual(metrics['foo.count'], 2, "Wrong value")
        self.assertEqual(metrics['new_func.count'], 1, "Wrong value")

        metrics = Stats.collect()
        self.assertEqual(metrics, {}, "Wrong value")


if __name__ == '__main__':
    unittest.main()
