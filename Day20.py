import unittest


def parse(blacklist):
    x, y = blacklist.split("-")
    x = int(x)
    y = int(y)
    return x, y


def parse_all(string_ranges):
    return [list(parse(blacklist)) for blacklist in string_ranges]


def get_first_valid_ip(rules):
    if len(rules) == 0:
        return 0
    if len(rules) == 1:
        return rules[0][1] + 1
    else:
        return rules[1][0] - 1


def keep_count(blacklists, maximum):
    count = 0
    minimum = 0
    for blacklist in blacklists:
        if blacklist[0] != minimum:
            count += ((blacklist[0] - 1) - minimum)
        minimum = blacklist[1]

    count += (maximum - blacklists[-1][1])

    return count


def consolidate(blacklists):

    blacklists = sorted(blacklists)
    consolidated = []

    for blacklist in blacklists:
        lower, upper = blacklist
        for item in consolidated:
            if lower <= item[1]+1:
                if item[1] <= upper:
                    item[1] = upper
                break
        else:
            consolidated.append(blacklist)

    return consolidated


class Day20(unittest.TestCase):

    def get_puzzle_input(self):
        return [line.rstrip("\n") for line in open("day20.txt").readlines()]

    def parse(self, string_list):
        return parse_all(string_list)

    def get_first_valid(self, items):
        return get_first_valid_ip(items)

    def get_first_valid_from_string_input(self, strings):
        return self.get_first_valid(self.consolidate(self.parse(strings)))

    def consolidate(self, items):
        return consolidate(items)

    def consolidate_from_strings(self, strings):
        return self.consolidate(self.parse(strings))

    def keep_count(self, items, maximum):
        return keep_count(items, maximum)

    def keep_count_from_strings(self, items, maximum):
        return self.keep_count(self.consolidate_from_strings(items), maximum)

    def test_FirstValidIPIsZeroWithoutAnyRules(self):
        self.assertEqual(self.get_first_valid([]), 0)

    def test_FirstValidIPIsThreeWithRule0_2(self):
        self.assertEqual(self.get_first_valid_from_string_input(["0-2"]), 3)

    def test_FirstValidIPIsTwoWithRule0_1(self):
        self.assertEqual(self.get_first_valid_from_string_input(["0-1"]), 2)

    def test_FirstValidIPIsFourWithRule0_1And2_3(self):
        self.assertEqual(self.get_first_valid_from_string_input(["0-1", "2-3"]), 4)

    def test_Example(self):
        self.assertEqual(self.get_first_valid_from_string_input(["5-8", "0-2", "4-7"]), 3)

    def test_consolidate_ranges_0_2_and_1_3_gives_0_3_(self):
        self.assertEqual([[0, 3]], self.consolidate_from_strings(["0-2", "1-3"]))

    def test_consolidate_ranges_5_8_and_4_7_gives_4_8_(self):
        self.assertEqual([[4, 8]], self.consolidate_from_strings(["4-7", "5-8"]))

    def test_consolidate_ranges_0_1___5_8_and_4_7_gives_4_8_andAnother(self):
        self.assertEqual([[0, 1], [4, 8]], self.consolidate_from_strings(["0-1", "4-7", "5-8"]))

    def test_01_23_can_be_joined(self):
        self.assertEqual([[0, 3]], self.consolidate([[0, 1], [2, 3]]))

    def test_successive_joins_can_be_made(self):
        self.assertEqual([[0, 6]], self.consolidate([[0, 3], [1, 4], [5, 6]]))

    def test_partone(self):
        self.assertEqual(self.get_first_valid_from_string_input(self.get_puzzle_input()), 14975795)

    def testExamplePart2(self):
        self.assertEqual(self.keep_count_from_strings(["5-8", "0-2", "4-7"], 9), 2)

    def testPartTwo(self):
        self.assertEqual(self.keep_count_from_strings(self.get_puzzle_input(), 4294967295), 101)
