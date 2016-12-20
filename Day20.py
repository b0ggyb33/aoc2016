import unittest


def parse(range):
    x, y = range.split("-")
    x = int(x)
    y = int(y)
    return x,y


def parseAll(string_ranges):
    return [list(parse(range)) for range in string_ranges]


def getFirstValidIP(rules):
    rules = consolidate(rules)
    if len(rules)==0:
        return 0
    if len(rules)==1:
        return rules[0][1]+1
    else:
        return rules[1][0]-1


def keepCount(ranges, maximum):
    count = 0
    minimum = 0
    for range in ranges:
        if range[0] != minimum:
            count += ((range[0] - 1) - minimum)
        minimum = range[1]
    count += (maximum - ranges[-1][1])

    return count


def consolidate(ranges):

    ranges = sorted(ranges, key=lambda range: range[0])
    consolidated = []

    for range in ranges:
        x,y = range
        matched=False
        for item in consolidated:
            if x <= item[1]+1:
                matched = True
                if item[1] <= y:
                    item[1] = y

        if not matched:
            consolidated.append(range)

    return consolidated

class Day20(unittest.TestCase):

    def test_FirstValidIPIsZeroWithoutAnyRules(self):
        self.assertEqual(getFirstValidIP([]),0)

    def test_FirstValidIPIsThreeWithRule0_2(self):
        self.assertEqual(getFirstValidIP(parseAll(["0-2"])), 3)

    def test_FirstValidIPIsTwoWithule0_1(self):
        self.assertEqual(getFirstValidIP(parseAll(["0-1"])), 2)

    def test_FirstValidIPIsFourWithRule0_1And2_3(self):
        self.assertEqual(getFirstValidIP(parseAll(["0-1", "2-3"])), 4)

    def test_Example(self):
        self.assertEqual(getFirstValidIP(parseAll(["5-8", "0-2", "4-7"])), 3)

    def test_consolidate_ranges_0_2_and_1_3_gives_0_3_(self):
        self.assertEqual([[0,3]],consolidate(parseAll(["0-2","1-3"])))

    def test_consolidate_ranges_5_8_and_4_7_gives_4_8_(self):
        self.assertEqual([[4, 8]], consolidate(parseAll(["4-7", "5-8"])))

    def test_consolidate_ranges_0_1___5_8_and_4_7_gives_4_8_andAnother(self):
        self.assertEqual([[0,1],[4, 8]], consolidate(parseAll(["0-1", "4-7", "5-8"])))

    def test_01_23_canbejoined(self):
        self.assertEqual([[0, 3]], consolidate([[0, 1], [2, 3]]))

    def test_recursive(self):
        self.assertEqual([[0, 6]], consolidate([[0, 3], [1, 4], [5, 6]]))

    def test_partone(self):
        puzzle_input = [line.rstrip("\n") for line in open("day20.txt").readlines()]
        puzzle_input = parseAll(puzzle_input)
        self.assertEqual(getFirstValidIP(puzzle_input), 14975795)

    def testExamplePart2(self):
        blacklist = parseAll(["5-8", "0-2", "4-7"])
        blacklist = consolidate(blacklist)
        self.assertEqual(keepCount(blacklist, 9), 2)

    def testPartTwo(self):
        puzzle_input = [line.rstrip("\n") for line in open("day20.txt").readlines()]
        puzzle_input = parseAll(puzzle_input)
        puzzle_input = consolidate(puzzle_input)
        self.assertEqual(keepCount(puzzle_input, 4294967295), 101)
