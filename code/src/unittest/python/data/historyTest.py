import sys
sys.path.append("src/main/python")
from model.project import History
from model.project import Operation
from .testOperation import TestOperation

import unittest

class HistoryTest(unittest.TestCase):

    def test_add_operation(self):
        start_data = [0,1,2,3,4,5,6,7,8,9]
        end_data = [1,2,3,4,5,6,7,8,9,10]
        test_data = [0,1,2,3,4,5,6,7,8,9]
        history = History()
        operation1 = TestOperation(test_data)
        operation2 = TestOperation(test_data)
        self.assertEqual(history.get_num_operations(), 0)
        history.do_operation(operation1)
        self.assertEqual(test_data, end_data)
        self.assertEqual(history.get_num_operations(), 1)
        history.do_operation(operation2)
        self.assertEqual(history.get_num_operations(), 2)

    def test_undo_operation(self):
        start_data = [0,1,2,3,4,5,6,7,8,9]
        end_data = [1,2,3,4,5,6,7,8,9,10]
        end_data2 = [2,3,4,5,6,7,8,9,10,11]
        test_data = [0,1,2,3,4,5,6,7,8,9]
        history = History()
        operation1 = TestOperation(test_data)
        operation2 = TestOperation(test_data)
        self.assertEqual(history.get_num_operations(), 0)
        history.do_operation(operation1)
        self.assertEqual(test_data, end_data)
        self.assertEqual(history.get_num_operations(), 1)
        history.do_operation(operation2)
        self.assertEqual(test_data, end_data2)
        self.assertEqual(history.get_num_operations(), 2)
        history.undo_last_operation()
        self.assertEqual(test_data, end_data)
        self.assertEqual(history.get_num_operations(), 1)
        history.undo_last_operation()
        self.assertEqual(test_data, start_data)
        self.assertEqual(history.get_num_operations(), 0)

    def test_undo_empty_history(self):
        test_data = []
        history = History()
        self.assertRaises(Exception, history.undo_last_operation)
        operation1 = TestOperation(test_data)
        history.do_operation(operation1)
        history.undo_last_operation()
        self.assertRaises(Exception, history.undo_last_operation)


    def test_redo_operation(self):
        start_data = [0,1,2,3,4,5,6,7,8,9]
        end_data = [1,2,3,4,5,6,7,8,9,10]
        end_data2 = [2,3,4,5,6,7,8,9,10,11]
        test_data = [0,1,2,3,4,5,6,7,8,9]
        history = History()
        operation1 = TestOperation(test_data)
        operation2 = TestOperation(test_data)
        history.do_operation(operation1)
        history.do_operation(operation2)
        self.assertEqual(test_data, end_data2)
        history.undo_last_operation()
        self.assertEqual(test_data, end_data)
        self.assertEqual(history.get_num_undone_operations(), 1)
        history.redo_last_operation()
        self.assertEqual(history.get_num_undone_operations(), 0)
        self.assertEqual(test_data, end_data2)
        history.undo_last_operation()
        history.undo_last_operation()
        self.assertEqual(history.get_num_undone_operations(), 2)
        self.assertEqual(test_data, start_data)
        history.redo_last_operation()
        self.assertEqual(history.get_num_undone_operations(), 1)
        self.assertEqual(test_data, end_data)

    def test_redo_empty_history(self):
        test_data = []
        history = History()
        self.assertRaises(Exception, history.redo_last_operation)
        operation1 = TestOperation(test_data)
        history.do_operation(operation1)
        history.undo_last_operation()
        history.redo_last_operation()
        self.assertRaises(Exception, history.redo_last_operation)