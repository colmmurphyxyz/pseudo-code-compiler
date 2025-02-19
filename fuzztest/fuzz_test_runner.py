from typing import Callable
import unittest

class FuzzTestRunner(unittest.TestCase):
    def __init__(self, num_trials: int, input_generator: Callable, algorithms: tuple[Callable, Callable], output_comparator: Callable | None = None, inplace_output_key: Callable | None = None):
        self.input_generator = input_generator
        self.pc_function, self.py_function = algorithms
        self.num_trials = num_trials
        self.output_comparator = output_comparator
        self.inplace_output_key = inplace_output_key
        super().__init__()

    def _get_error_mesage(self, pc_inputs, py_inputs, pc_output, py_output):
        return f"Test Case Failed.\nPC Inputs: {pc_inputs}\nPy Inputs: {py_inputs}\nPC Output: {pc_output}\nPy Output: {py_output}"

    def run_trials(self):
        for _ in range(self.num_trials):
            pc_inputs, py_inputs = self.input_generator()
            pc_output = self.pc_function(*pc_inputs)
            py_output = self.py_function(*py_inputs)
            if self.inplace_output_key:
                lhs = self.inplace_output_key(pc_inputs)
                rhs = self.inplace_output_key(py_inputs)
                is_equal = self.output_comparator(lhs, rhs) if self.output_comparator else lhs == rhs
            else:
                is_equal = self.output_comparator(pc_output, py_output) if self.output_comparator else pc_output == py_output
            self.assertTrue(is_equal, msg=self._get_error_mesage(pc_inputs, py_inputs, pc_output, py_output))
