import unittest


def do_copy(registers, arguments):
    if arguments[0] in registers:
        registers[arguments[1]] = registers[arguments[0]]
    else:
        registers[arguments[1]] = int(arguments[0])
    return 0


def do_inc(registers, arguments):
    registers[arguments[0]] += 1
    return 0


def do_dec(registers, arguments):
    registers[arguments[0]] -= 1
    return 0


def do_jump(registers, arguments):
    if arguments[0] in registers:
        value = registers[arguments[0]]
    else:
        value = int(arguments[0])
    if value != 0:
        return int(arguments[1])
    else:
        return 0


def perform_instruction(instruction, registers):
    commands = {"cpy": do_copy, "inc": do_inc, "dec": do_dec, "jnz": do_jump}
    arguments = instruction.split(" ")
    command, arguments = arguments[0], arguments[1:]
    return commands[command](registers, arguments)


def perform_instructions(instructions, registers):
    idx = 0
    while idx < len(instructions):
        instruction = instructions[idx]
        jump = perform_instruction(instruction, registers)
        if jump == 0:
            idx += 1
        else:
            idx += jump


class Day12(unittest.TestCase):
    def setUp(self):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}

    def test_CansetATo1(self):
        instr = "cpy 1 a"
        perform_instruction(instr, self.registers)

        self.assertEqual(self.registers['a'], 1)

    def test_canSetATo2(self):
        instr = "cpy 2 a"
        perform_instruction(instr, self.registers)

        self.assertEqual(self.registers['a'], 2)

    def test_canSetBTo2(self):
        instr = "cpy 2 b"
        perform_instruction(instr, self.registers)

        self.assertEqual(self.registers['b'], 2)

    def test_CanCopyAIntoB(self):
        instr = "cpy 2 a"
        perform_instruction(instr, self.registers)
        instr = "cpy a b"
        perform_instruction(instr, self.registers)

        self.assertEqual(self.registers['b'], 2)

    def test_canIncrementA(self):
        instr = "inc a"
        perform_instruction(instr, self.registers)
        self.assertEqual(self.registers['a'], 1)

    def test_canIncrementB(self):
        instr = "inc b"
        perform_instruction(instr, self.registers)
        self.assertEqual(self.registers['b'], 1)

    def test_canDecrementA(self):
        instr = "dec a"
        perform_instruction(instr, self.registers)
        self.assertEqual(self.registers['a'], -1)

    def test_noJumpWhenAisZero(self):
        instr = "jnz a 2"
        jumps = perform_instruction(instr, self.registers)
        self.assertEqual(jumps, 0)

    def test_JumpWhenAisOne(self):
        self.registers['a'] = 1
        instr = "jnz a 2"
        jumps = perform_instruction(instr, self.registers)
        self.assertEqual(jumps, 2)

    def test_JumpBackwardWhenAisOneAndInstructionsSaysNegative(self):
        self.registers['a'] = 1
        instr = "jnz a -1"
        jumps = perform_instruction(instr, self.registers)
        self.assertEqual(jumps, -1)

    def test_example(self):
        instructions = ["cpy 41 a",
                        "inc a",
                        "inc a",
                        "dec a",
                        "jnz a 2",
                        "dec a"]

        perform_instructions(instructions, self.registers)

        self.assertEqual(self.registers['a'], 42)

    def test_partOne(self):
        instructions = [line.rstrip("\n") for line in open("day12.txt").readlines()]
        perform_instructions(instructions, self.registers)
        self.assertEqual(self.registers['a'], 318117)

    def test_partTwo(self):
        self.registers['c'] = 1
        instructions = [line.rstrip("\n") for line in open("day12.txt").readlines()]
        perform_instructions(instructions, self.registers)
        self.assertEqual(self.registers['a'], 9227771)
