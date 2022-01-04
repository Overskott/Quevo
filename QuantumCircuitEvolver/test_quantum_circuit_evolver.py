from unittest import TestCase
from quantum_circuit_evolver import *


class TestCircuitString(TestCase):

    def test_check_duplicate_qubit_assignment(self):
        assert True

    def test_generate_gate_string(self):

        assert True

    def test_mutate_gate_string(self):
        assert True

    def test_set_gate_string(self):

        assert True

    def test_get_gates_string(self):
        test_circuit_string = CircuitString()
        assert test_circuit_string.get_gates_string() == []

        int_list = [1, 2, 3]
        test_circuit_string.set_gate_string(int_list)
        assert test_circuit_string.get_gates_string() == int_list

    def test_clear_string(self):
        test_circuit_string = CircuitString()

        assert test_circuit_string.set_gate_string([]) in None

        test_circuit_string.set_gate_string([1, 2, 3])
        assert test_circuit_string.clear_string() is None
