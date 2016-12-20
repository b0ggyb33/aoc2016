import unittest
from collections import deque

runLongTests = True


def getNextElf(elves, current_elf):
    elfKeys = list(elves.keys())
    idx = elfKeys.index(current_elf)
    return elfKeys[(idx + 1) % len(elves)]


def getElfWithPresents(n):
    elves = {}
    for i in range(1, n, 2):
        elves[i] = 2
    elves[n] = 1

    current_elf = n

    unique_elf = uniqueElf(elves)

    while unique_elf is None:
        passOnAPresent(elves, current_elf)
        unique_elf = uniqueElf(elves)
        current_elf = getNextElf(elves, current_elf)
    return unique_elf


def passOnAPresent(elves, idx):
    nextElf = getNextElf(elves, idx)
    elves[idx] += elves[nextElf]
    del elves[nextElf]


def uniqueElf(elves):
    if len(elves) == 1:
        return list(elves.keys())[0]
    else:
        return None


def getAnswerQuick(n):
    elves = deque()
    for i in range(1, n + 1):
        elves.append(i)
    while len(elves) > 1:
        x = elves.popleft()
        _ = elves.popleft()
        elves.append(x)
    return elves[0]


def getAnswerQuick2(n):
    elves = [deque(), deque()]

    midpoint = int((n + 1) / 2)
    for i in range(1, midpoint + 1):
        elves[0].append(i)
    for i in range(midpoint + 1, n + 1):
        elves[1].append(i)

    while len(elves[0]) > 1:
        if len(elves[0]) > len(elves[1]):
            popFrom = 0
        else:
            popFrom = 1
        x = elves[0].popleft()
        _ = elves[popFrom].pop()
        elves[1].appendleft(x)
        y = elves[1].pop()
        elves[0].append(y)

    return elves[0][0]

class Day19(unittest.TestCase):

    def setUp(self):
        self.puzzle_input = 3014387

    def test_WithTwoElves_FirstElfGetsAllPresents(self):
        self.assertEqual(1, getAnswerQuick(2))

    def test_WithThreeElves_ThirdElfGetsAllPresents(self):


        self.assertEqual(3, getElfWithPresents(3))

    def test_WithFourElves_ThirdElfGetsAllPresents(self):


        self.assertEqual(3, getElfWithPresents(4))

    def test_testWithThreeElves_FirstElfTakesPresentsFromSecond(self):

        elves = {0: 1, 1: 1, 2: 1}
        index=0
        passOnAPresent(elves, index)
        self.assertEqual(elves[0], 2)

    def test_testWithThreeElves_SecondElfTakesPresentsFromThird(self):

        elves = {0: 1, 1: 1, 2: 1}
        index = 1
        passOnAPresent(elves, index)
        self.assertEqual(elves[1], 2)

    def test_withThreeElves_ElfThreeIsSatNextToElfFive(self):
        elves = {0: 2, 3: 2, 5: 1}
        current_elf = 3
        self.assertEqual(getNextElf(elves,current_elf), 5)

    def test_WithThreeElvesGetNextElfIsNext(self):
        elves = {1:1, 2:1, 3:1}
        self.assertEqual(getNextElf(elves,3), 1)

    def test_withThreeElves_ThirdElfTakesPresentFromFirst(self):
        elves = {0: 2, 1: 1, 2: 1}
        index = 2
        passOnAPresent(elves,index)
        self.assertEqual(elves[2], 3)

    def test_WithThreeElves_CanFindUniqueElfWithPresents(self):
        elves = {1: 3}
        self.assertEqual(uniqueElf(elves), 1)

    def test_WithThreeElves_CantFindUniqueElfWithPresents(self):
        elves = {0: 1, 1: 2, 2: 1}
        self.assertEqual(uniqueElf(elves), None)

    def test_withFiveElves_ThirdElfTakesAllPresents(self):
        self.assertEqual(getAnswerQuick(5),3)

    def test_partOne(self):
        self.assertEqual(getAnswerQuick(self.puzzle_input), 1834471)

    def test_ExampleTwo(self):
        self.assertEqual(getAnswerQuick2(5), 2)

    @unittest.skipIf(not runLongTests, "skipping long test")
    def test_partTwo(self):
        answer = getAnswerQuick2(self.puzzle_input)
        self.assertNotEquals(answer,1507195)
        self.assertEqual(answer, 1420064)

    def test_CorrectList(self):
        queueA = deque()
        queueB = deque()
        n=9
        midpoint=int((n+1)/2)
        for i in range(1,midpoint+1):
            queueA.append(i)
        for i in range(n,midpoint,-1):
            queueB.append(i)
        self.assertEqual(queueA, deque([1,2,3,4,5]))
        self.assertEqual(queueB, deque([9,8,7,6]))





