import roof_util
import unittest

class TestRoofUtil(unittest.TestCase):
    
    def test_roof_low_intensity(self):
        actual = roof_util.roof(
            op_intensity=0.01,
            compute=1e15,
            mem_bw=1e12,
            compute_req=1e10,
        )     
        expected = 1
        self.assertEqual(actual, expected)

    def test_roof_high_intensity(self):
        actual = roof_util.roof(
            op_intensity=100,
            compute=1e15,
            mem_bw=1e12,
            compute_req=1e10,
        )     
        expected = 1e4
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(unittest.main(argv=[''], verbosity=2, exit=False))
