import unittest


def SSLSupport(input, validation=None):
    if len(input)<3:
        return False
    if input[0] == input[2]:
        if input[1] != input[0]:
            if validation:
                for valid in validation:  # now we check all the validation strings to look for the reverse string
                    if valid[0] == input[1] and valid[1] == input[0]:
                        return True
                return False
            else:
                return True
    return False


def TLSSupport(input, validation=None):
    if len(input) < 4:
        return False
    if input[0] == input[3]:
        if input[1] == input[2]:
            if input[0] != input[1]:
                return True
    else:
        return False


def getValidationStrings(input, function, lengthOfStringToCheck):
    validation = []
    for idx in range(len(input) - (lengthOfStringToCheck - 1)):
        substring = input[idx:idx + lengthOfStringToCheck]
        if function(substring):
            validation.append(substring)
    return validation


def checkSSLInString(input, validation):

    for idx in range(len(input) - 2):
        if SSLSupport(input[idx:idx + 3]):
            reconstructed = input[idx+1]+input[idx]+input[idx+1]  # ABA into BAB
            if reconstructed in validation:
                return True
    return False


def checkTLSInString(input):
    validation = getValidationStrings(input, TLSSupport, 4)
    return len(validation) > 0


def parseInput(input):
    input.rstrip("\n")
    input = input.replace(']', '_')
    input = input.replace('[', '_')
    return input.split("_")


def linePassesPartOne(line):
    subwords = parseInput(line)

    haveFoundTLSInAnAllowedWord = False

    for i in range(0, len(subwords), 2):
        haveFoundTLSInAnAllowedWord |= checkTLSInString(subwords[i])

    for i in range(1, len(subwords), 2):
        if checkTLSInString(subwords[i]):
            return False
    return haveFoundTLSInAnAllowedWord


def linePassesPartTwo(line):
    subwords = parseInput(line)

    validation = []
    for i in range(0, len(subwords), 2):
        validation.extend(getValidationStrings(subwords[i], SSLSupport, 3))

    for i in range(1, len(subwords), 2):
        if checkSSLInString(subwords[i], validation):
            return True
    return False


class Day7(unittest.TestCase):
    def test_AAAAFails(self):
        self.assertFalse(TLSSupport("AAAA"))

    def test_ABBAPasses(self):
        self.assertTrue(TLSSupport("ABBA"))

    def test_ABCDFails(self):
        self.assertFalse(TLSSupport("ABCD"))

    def test_BDDBPasses(self):
        self.assertTrue(TLSSupport("BDDB"))

    def test_IOXXOJPasses(self):
        self.assertTrue(checkTLSInString("IOXXOJ"))

    def test_ABBCDDEFails(self):
        self.assertFalse(checkTLSInString("ABBCDDE"))

    def test_ABCDDCPasses(self):
        self.assertTrue(checkTLSInString("ABCDDC"))

    def test_canSeperateInput(self):
        input = "abba[mnop]qrst"
        self.assertEqual(parseInput(input), ["abba", "mnop", "qrst"])

    def test_aWholeSequenceCanPass(self):
        test = "abba[mnop]qrst\n"
        self.assertTrue(linePassesPartOne(test))

    def test_wholeSequenceFailsBecauseOfMiddleRepetition(self):
        self.assertFalse(linePassesPartOne("abcd[bddb]xyyx"))

    def test_wholeSequenceFailsBecauseOfAAAA(self):
        self.assertFalse(linePassesPartOne("aaaa[qwer]tyui"))

    def test_longerSequencePasses(self):
        self.assertTrue(linePassesPartOne("ioxxoj[asdfgh]zxcvbn"))

    def test_multipleHypernetSequence(self):
        test = "rnqfzoisbqxbdlkgfh[lwlybvcsiupwnsyiljz]kmbgyaptjcsvwcltrdx[ntrpwgkrfeljpye]jxjdlgtntpljxaojufe"
        self.assertEqual(parseInput(test),
                         ["rnqfzoisbqxbdlkgfh", "lwlybvcsiupwnsyiljz", "kmbgyaptjcsvwcltrdx", "ntrpwgkrfeljpye",
                          "jxjdlgtntpljxaojufe"])

    def test_multipleHypernetSequencePasses(self):
        test = "abba[pass]word[pass]beef"
        self.assertTrue(linePassesPartOne(test))

    def test_multipleHypernetSequenceFailsBecauseOfRepetitionInHypernet(self):
        test = "abba[pass]word[abba]beef"
        self.assertFalse(linePassesPartOne(test))

    def test_multipleHypernetSequenceFailsBecauseOfNoRepetition(self):
        test = "fail[pass]word[abba]beef"
        self.assertFalse(linePassesPartOne(test))

    def testPartOne(self):
        count = 0
        for line in open("day7.txt").readlines():
            count += linePassesPartOne(line)
        self.assertEqual(count, 105)

    def test_SSL_SupportInSupernet(self):
        self.assertTrue(SSLSupport("ABA"))

    def test_SSL_SupportInHypernet(self):
        self.assertTrue(checkSSLInString("BAB", ["ABA"]))

    def test_SSL_NoSupportInHypernet(self):
        self.assertFalse(checkSSLInString("ABA", ["ABA"]))

    def test_validationreturnsABA(self):
        self.assertEqual(getValidationStrings("ABADC", SSLSupport, 3), ["ABA"])

    def test_validationreturnsABAandBAB(self):
        self.assertEqual(getValidationStrings("ABABC", SSLSupport, 3), ["ABA", "BAB"])

    def test_validationreturnsNothing(self):
        self.assertEqual(getValidationStrings("ABCDE", SSLSupport, 3), [])

    def test_ExampleOne(self):
        test = "aba[bab]xyz"
        self.assertTrue(linePassesPartTwo(test))

    def test_exampleTwo(self):
        test = "xyx[xyx]xyx"
        self.assertFalse(linePassesPartTwo(test))

    def test_exampleThree(self):
        test = "aaa[kek]eke"
        self.assertFalse(SSLSupport("AAA"))
        self.assertTrue(linePassesPartTwo(test))

    def test_exampleFour(self):
        test = "zazbz[bzb]cdb"
        self.assertTrue(linePassesPartTwo(test))

    def test_multipleHyperNetProblemPartTwo(self):
        test = "abba[pass]word[pass]beef"
        self.assertFalse(linePassesPartTwo(test))

    def test_multipleHyperNetProblemPartTwo_a(self):
        test = "aaba[pass]word[pbab]beef"
        self.assertTrue(linePassesPartTwo(test))

    def testPartTwo(self):
        count = 0
        for line in open("day7.txt").readlines():
            count += linePassesPartTwo(line)
        self.assertEqual(count, 258)
