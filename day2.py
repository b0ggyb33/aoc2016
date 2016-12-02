import unittest
import numpy as np

def move(keypad, start, direction):

    where = np.where(keypad==str(start))
    where_asarray = np.asarray(where)
    coordinates = where_asarray.T[0]
    functions = {'U':[-1,0], 'L': [0,-1], 'R':[0,1], 'D':[1,0]}

    new = coordinates + functions[direction]
    new = keypad[new[0],new[1]]
    if new in ['A','B','C','D'] or int(new)>0:
        return new
    else:
        return str(start)
    

def parseSequence(keypad, seq):
    start = 5
    result = []
    for item in seq:
        for char in item:
            start = move(keypad, start, char)
        result.append(str(start))
    return "".join(result)


class Day2(unittest.TestCase):
    
    def setUp(self):
        self.keypad1 = np.array(((0, 0, 0, 0, 0),
                                 (0, '1', '2', '3', 0),
                                 (0, '4', '5', '6', 0),
                                 (0, '7', '8', '9', 0),
                                 (0, 0, 0, 0, 0)))

        self.keypad2 = np.array(((0, 0, 0, 0, 0, 0, 0),
                                 (0, 0, 0, 1, 0, 0, 0),
                                 (0, 0, 2, 3, 4, 0, 0),
                                 (0, 5, 6, 7, 8, 9, 0),
                                 (0, 0, 'A', 'B', 'C', 0, 0),
                                 (0, 0, 0, 'D', 0, 0, 0),
                                 (0, 0, 0, 0, 0, 0, 0)))
    
    def test_UFrom5Gives2(self):
        self.assertEqual(move(self.keypad1, 5, 'U'), '2')

    def test_LFrom5Gives4(self):
        self.assertEqual(move(self.keypad1, 5, 'L'), '4')

    def test_RFrom5Gives6(self):
        self.assertEqual(move(self.keypad1, 5, 'R'), '6')

    def test_DFrom5Gives8(self):
        self.assertEqual(move(self.keypad1, 5, 'D'), '8')

    def test_UFrom2Gives2(self):
        self.assertEqual(move(self.keypad1, 2,'U'), '2')

    def testLFrom4Gives4(self):
        self.assertEqual(move(self.keypad1, 4,'L'), '4')

    def testRFrom6Gives6(self):
        self.assertEqual(move(self.keypad1, 6, 'R'), '6')

    def test_DFrom8Gives8(self):
        self.assertEqual(move(self.keypad1, 8, 'D'), '8')

    def test_example(self):
        seq = ["ULL", "RRDDD", "LURDL", "UUUUD"]
        result = parseSequence(self.keypad1, seq)
        self.assertEqual("1985", result)

    def testPartOne(self):
        file = open("day2.txt")
        seq= [line.rstrip("\n") for line in file.readlines()]
        result = parseSequence(self.keypad1, seq)
        self.assertEqual('73597', result)

    def testPartTwo(self):
        file = open("day2.txt")
        seq = [line.rstrip("\n") for line in file.readlines()]
        result = parseSequence(self.keypad2, seq)
        self.assertEqual('A47DA', result)
