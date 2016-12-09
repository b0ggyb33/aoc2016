import unittest
import collections
import string


def prepareInput(string):
    room, checksum = string.split("[")
    checksum = checksum.rstrip("]\n")
    room = room.split("-")
    sector_id = room[-1]
    return "".join(room[:-1]), checksum, sector_id


def getMostCommon(string):
    counter = collections.Counter(string)
    most_common = counter.most_common()
    groupByNumber = collections.defaultdict(list)
    output = ""

    for letter, count in most_common:
        groupByNumber[count].append(letter)
    for item in sorted(groupByNumber.keys(), reverse=True):
        #  each item is a list
        for letter in sorted(groupByNumber[item]):
            if len(output) < 5:
                output += letter
    return output


def sumRoom(room, checksum, sector_id):
    if checksum == getMostCommon(room):
        return int(sector_id)
    else:
        return 0


def shift(letter, places):
    idx = string.ascii_lowercase.find(letter)
    if idx == -1:
        return " "
    idx += places
    idx %= 26  # remove any full rotations
    return string.ascii_lowercase[idx]


def shiftword(word, places):
    output = ""
    for letter in word:
        output += shift(letter, places)
    return output


class Day4(unittest.TestCase):
    def test_CanParseInput(self):
        room, checksum, _ = prepareInput("aaaaa-bbb-z-y-x-123[abxyz]")
        self.assertEqual(room, "aaaaabbbzyx")
        self.assertEqual(checksum, "abxyz")

    def test_aaReturnsmaximumInA(self):
        most_common = getMostCommon("aa")
        self.assertEqual(most_common, "a")

    def testCheckSumofaaIsJustA(self):
        check = ""
        for letter in getMostCommon("aa"):
            check += letter
        self.assertEqual(check, "a")

    def testExamples(self):
        test = "aaaaa-bbb-z-y-x-123[abxyz]"
        room, checksum, _ = prepareInput(test)

        self.assertEqual(getMostCommon(room), checksum)

    def testExamples2(self):
        room, checksum, _ = prepareInput("a-b-c-d-e-f-g-h-987[abcde]")
        self.assertEqual(getMostCommon(room), checksum)

    def testExample3(self):
        room, checksum, _ = prepareInput("not-a-real-room-404[oarel]")
        self.assertEqual(getMostCommon(room), checksum)

    def testExample4(self):
        room, checksum, _ = prepareInput("totally-real-room-200[decoy]")
        self.assertFalse(getMostCommon(room) == checksum)

    def testFullExample(self):
        input = ["aaaaa-bbb-z-y-x-123[abxyz]",
                 "a-b-c-d-e-f-g-h-987[abcde]",
                 "not-a-real-room-404[oarel]",
                 "totally-real-room-200[decoy]"]

        sum = 0
        for item in input:
            room, checksum, sector_id = prepareInput(item)
            sum += sumRoom(room, checksum, sector_id)

        self.assertEqual(1514, sum)

    def testPartOne(self):
        sum = 0
        for item in open("day4.txt").readlines():
            room, checksum, sector_id = prepareInput(item)
            sum += sumRoom(room, checksum, sector_id)

        self.assertEqual(173787, sum)

    def test_cipher(self):
        self.assertEqual(shift("q", 343), "v")
        output = shiftword("qzmt-zixmtkozy-ivhz", 343)
        self.assertEqual(output, "very encrypted name")

    def testPartTwo(self):
        for item in open("day4.txt").readlines():
            room, checksum, sector_id = prepareInput(item)
            valid = sumRoom(room, checksum, sector_id) > 0
            if valid:
                if "northpole" in shiftword(room, int(sector_id)):
                    print sector_id

