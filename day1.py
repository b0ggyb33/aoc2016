import unittest
import numpy as np


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parseString(stringUnderTest):
    if 'L' in stringUnderTest:
        rotate = -90
        number = int(stringUnderTest.lstrip("L"))
        return rotate, number
    else:
        rotate = 90
        number = int(stringUnderTest.lstrip("R"))
        return rotate, number


def changeDirection(initialDirection, rotation):
    directions = ['N', 'E', 'S', 'W']
    idx = directions.index(initialDirection)
    if rotation > 0:
        return directions[(idx + 1) % 4]
    else:
        return directions[idx - 1]


def move(position, direction, amount):
    if direction == "N":
        return (position[0] + amount, position[1])
    elif direction == "S":
        return (position[0] - amount, position[1])
    elif direction == "E":
        return (position[0], position[1] + amount)
    else:
        return (position[0], position[1] - amount)


class Day1(unittest.TestCase):
    def setUp(self):
        self.stringUnderTest = "R2, L5, L4, L5, R4, R1, L4, R5, R3, R1, L1, L1, R4, L4, L1, R4, L4, R4, L3, R5, R4, R1, R3, L1, L1, R1, L2, R5, L4, L3, R1, L2, L2, R192, L3, R5, R48, R5, L2, R76, R4, R2, R1, L1, L5, L1, R185, L5, L1, R5, L4, R1, R3, L4, L3, R1, L5, R4, L4, R4, R5, L3, L1, L2, L4, L3, L4, R2, R2, L3, L5, R2, R5, L1, R1, L3, L5, L3, R4, L4, R3, L1, R5, L3, R2, R4, R2, L1, R3, L1, L3, L5, R4, R5, R2, R2, L5, L3, L1, L1, L5, L2, L3, R3, R3, L3, L4, L5, R2, L1, R1, R3, R4, L2, R1, L1, R3, R3, L4, L2, R5, R5, L1, R4, L5, L5, R1, L5, R4, R2, L1, L4, R1, L1, L1, L5, R3, R4, L2, R1, R2, R1, R1, R3, L5, R1, R4"

    def test_manhattanDistanceBetweenNeighboursIsOne(self):
        self.assertEqual(manhattan((0, 0), (0, 1)), 1)

    def test_L1GivesDistanceOfOne(self):
        rotation, distance = parseString("L1")
        self.assertEqual(distance, 1)
        self.assertEqual(rotation, -90)

    def test_R1Returns_0_1_(self):
        rotation, distance = parseString("R1")
        self.assertEqual(distance, 1)
        self.assertEqual(rotation, 90)

    def test_R2Returns_0_2_(self):
        rotation, distance = parseString("R2")
        self.assertEqual(distance, 2)
        self.assertEqual(rotation, 90)

    def test_givenN90ReturnE(self):
        self.assertEqual(changeDirection("N", 90), 'E')

    def test_givenN_90ReturnW(self):
        self.assertEqual(changeDirection("N", -90), 'W')

    def test_givenE90ReturnS(self):
        self.assertEqual(changeDirection("E", 90), 'S')

    def test_givenE_90ReturnN(self):
        self.assertEqual(changeDirection("E", -90), 'N')

    def test_givenW90ReturnN(self):
        self.assertEqual(changeDirection("W", 90), 'N')

    def test_moveOneNorth(self):
        self.assertEqual(move((0, 0), 'N', 1), (1, 0))

    def test_moveOneSouth(self):
        self.assertEqual(move((0, 0), 'S', 1), (-1, 0))

    def test_moveOneEast(self):
        self.assertEqual(move((0, 0), 'E', 1), (0, 1))

    def test_moveOneWest(self):
        self.assertEqual(move((0, 0), 'W', 1), (0, -1))

    def test_moveNorthFrom1_1(self):
        self.assertEqual(move((1, 1), 'N', 1), (2, 1))

    def test_moveWest2From1_1(self):
        self.assertEqual(move((1, 1), 'W', 2), (1, -1))

    def test_one(self):

        direction = 'N'
        position = 0, 0

        for item in self.stringUnderTest.split(", "):
            rotation, distance = parseString(item)
            direction = changeDirection(direction, rotation)
            position = move(position, direction, distance)
        self.assertEqual(239, manhattan((0, 0), position))

    def test_two(self):
        direction = 'N'
        position = 0, 0
        locations = []
        stop = False
        for item in self.stringUnderTest.split(", "):
            rotation, distance = parseString(item)
            direction = changeDirection(direction, rotation)

            while not stop and distance > 0:
                position = move(position, direction, 1)
                distance -= 1

                if position in locations:
                    print(manhattan((0, 0), position))
                    stop = True
                else:
                    locations.append(position)
            if stop:
                break

        self.assertEqual(141, manhattan((0, 0), position))
