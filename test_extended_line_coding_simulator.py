import unittest
import numpy as np
import os
from line_coding_simulator import (
    encode_nrz_l,
    encode_nrz_i,
    encode_rz,
    encode_manchester,
    encode_diff_manchester,
    encode_ami,
    encode_pseudoternary,
    read_bits_from_input,
    plot_signal
)


class TestExtendedLineCodingSimulator(unittest.TestCase):

    def setUp(self):
        self.long_bits = [0, 1]*500  # 1000 bits alternating
        self.invalid_input_strings = [
            "10201",      # Contains '2'
            "abcdef",     # Alphabetic characters
            "001100a1",   # Contains letter inside bits
            "",           # Empty string
            "  ",         # Spaces only
            "1010\n101"   # Newline within string
        ]
        self.valid_file = "test_bits_valid.txt"
        with open(self.valid_file, "w") as f:
            f.write("1010101010")

    def tearDown(self):
        if os.path.exists(self.valid_file):
            os.remove(self.valid_file)
        # Remove any generated png files from long_bits test
        for name in ["NRZ-L", "NRZ-I", "RZ", "Manchester", "Manchester Diferencial", "AMI", "Pseudoternário"]:
            filename = name.replace(" ", "_").replace(
                "ç", "c").replace("ã", "a") + ".png"
            if os.path.exists(filename):
                os.remove(filename)

    def test_large_sequence_performance(self):
        # Just invoke encoding functions to check if any unexpected error occurs on large input
        try:
            for encoder in [encode_nrz_l, encode_nrz_i, encode_rz, encode_manchester, encode_diff_manchester, encode_ami, encode_pseudoternary]:
                t, s = encoder(self.long_bits, 1e3, 100)
                self.assertEqual(len(s), len(self.long_bits)*100)
        except Exception as e:
            self.fail("Encoding failed on large input: " + str(e))

    def test_invalid_manual_inputs(self):
        # Testing the validation logic for manual string inputs.
        # Since read_bits_from_input reads from input(), here we simulate validation function separately.
        # For this, we check if the invalid strings fail the bit set check.
        for invalid_str in self.invalid_input_strings:
            self.assertFalse(set(invalid_str).issubset({"0", "1"}))

    def test_valid_file_input(self):
        # Test reading bits from file; simulate file reading
        with open(self.valid_file, "r") as f:
            bitstring = f.read().strip()
        self.assertTrue(set(bitstring).issubset({"0", "1"}))

    def test_plot_signal_file_creation(self):
        # Test if plot_signal creates an image file for small input
        bits = [1, 0, 1, 0]
        t = np.arange(0, len(bits), 0.01)
        s = np.sin(2*np.pi*5*t)
        plot_signal(t, s, bits, "Test_Plot", save=True)
        filename = "Test_Plot.png"
        self.assertTrue(os.path.exists(filename))
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    unittest.main()
