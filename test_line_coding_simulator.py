import unittest
import os
import numpy as np
from line_coding_simulator import (
    encode_nrz_l,
    encode_nrz_i,
    encode_rz,
    encode_manchester,
    encode_diff_manchester,
    encode_ami,
    encode_pseudoternary,
    count_transitions,
    calculate_dc_component,
    estimate_bandwidth
)


class TestLineCodingSimulator(unittest.TestCase):

    def setUp(self):
        self.bits_simple = [0, 1, 0, 1]
        self.bits_all_zero = [0] * 5
        self.bits_all_one = [1] * 5
        self.Rb = 1e3
        self.sps = 10

    def test_encode_nrz_l_basic(self):
        t, s = encode_nrz_l(self.bits_simple, self.Rb, self.sps)
        expected_signal = np.array(
            [[-1]*10, [1]*10, [-1]*10, [1]*10]).flatten()
        np.testing.assert_array_equal(s, expected_signal)

    def test_encode_nrz_i_edges(self):
        # Test with all zeros, output should remain constant level
        t, s = encode_nrz_i(self.bits_all_zero, self.Rb, self.sps)
        self.assertTrue(np.all(s == 1))
        # Test with all ones, output should alternate
        t, s = encode_nrz_i(self.bits_all_one, self.Rb, self.sps)
        # Should alternate between +1 and -1 for each bit
        levels = [s[i*self.sps] for i in range(len(self.bits_all_one))]
        for i in range(1, len(levels)):
            self.assertEqual(levels[i], -levels[i-1])

    def test_encode_rz(self):
        t, s = encode_rz(self.bits_simple, self.Rb, self.sps)
        half_sps = self.sps//2
        self.assertTrue(np.all(s[0:half_sps] == 0))  # First bit 0, all zero
        # 2nd bit is 1 level first half
        self.assertTrue(np.all(s[self.sps:self.sps+half_sps] == 1))

    def test_encode_manchester(self):
        t, s = encode_manchester(self.bits_simple, self.Rb, self.sps)
        half_sps = self.sps//2
        # 0's first half high, second half low
        self.assertTrue(np.all(s[0:half_sps] == 1))
        self.assertTrue(np.all(s[half_sps:self.sps] == -1))

    def test_encode_diff_manchester_transition(self):
        t, s = encode_diff_manchester(self.bits_simple, self.Rb, self.sps)
        # Check initial transition for 0 bit
        first_bit_level = s[0]
        second_bit_start_level = s[self.sps]
        self.assertNotEqual(first_bit_level, second_bit_start_level)

    def test_encode_ami_alternation(self):
        t, s = encode_ami(self.bits_simple, self.Rb, self.sps)
        levels = [s[i*self.sps]
                  for i in range(len(self.bits_simple)) if self.bits_simple[i] == 1]
        for i in range(1, len(levels)):
            self.assertEqual(levels[i], -levels[i-1])

    def test_encode_pseudoternary_alternation(self):
        t, s = encode_pseudoternary(self.bits_simple, self.Rb, self.sps)
        Zero_indices = [i for i, b in enumerate(self.bits_simple) if b == 0]
        levels = [s[i*self.sps] for i in Zero_indices]
        for i in range(1, len(levels)):
            self.assertEqual(levels[i], -levels[i-1])

    def test_count_transitions(self):
        signal = np.array([0, 0, 1, 1, 0, 0])
        transitions = count_transitions(signal)
        self.assertEqual(transitions, 2)

    def test_calculate_dc_component(self):
        signal = np.array([1, -1, 1, -1])
        dc = calculate_dc_component(signal)
        self.assertAlmostEqual(dc, 0)

    def test_estimate_bandwidth(self):
        self.assertEqual(estimate_bandwidth(5, 1), "alta")
        self.assertEqual(estimate_bandwidth(1, 10), "baixa")
        self.assertEqual(estimate_bandwidth(4, 3), "média")

    def test_invalid_bits_input(self):
        # Not a direct function but can check robustness by simulating inputs in main code if extended
        pass


if __name__ == '__main__':
    unittest.main()
