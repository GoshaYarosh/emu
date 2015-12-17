from unittest import TestCase
from random import randint

from emu.computer.processor import Processor
from emu.utils.compile import compile_code_from_str


class ProcessorTestCase(TestCase):

    def setUp(self):
        self.memory_size = 100
        self.registers_count = 12
        self.code = """
            mov r2, #11
            mov r3, #10
            add r1, r2, r3
            cmp r1, #15
            add r2, r1, r3, lsl r4
            sub r1, r2, r3
        """
        self.instructions_count = len(self.code.strip().split('\n'))

    def test_create_processor(self):
        processor = Processor(self.registers_count, self.memory_size)
        self.assertIn('pc', processor.registers._registers)
        self.assertIn('sp', processor.registers._registers)
        self.assertEqual(processor.memory.size(), self.memory_size)
        self.assertEqual(processor.registers.count(), self.registers_count + 2)

    def test_access_registers(self):
        processor = Processor(self.registers_count, self.memory_size)
        registers = processor.registers
        registers['r1'] = 123
        registers['r2'] = 1256
        self.assertEqual(registers['r1'], 123)
        self.assertEqual(registers['r2'], 1256)
        self.assertRaises(ValueError, registers.__setitem__, 'r3', 10 ** 10)

    def test_access_memory(self):
        processor = Processor(self.registers_count, self.memory_size)
        memory = processor.memory
        self.assertEqual(memory.size(), self.memory_size)

        memory_copy = [0] * self.memory_size
        for address in xrange(self.memory_size):
            value = randint(0, 255)
            memory_copy[address] = value
            memory.write_byte(address, value)
            self.assertEqual(memory.read_byte(address), value)
        self.assertItemsEqual(memory, memory_copy)

        for address in xrange(self.memory_size):
            value = randint(257, 10 ** 100)
            self.assertRaises(ValueError, memory.write_byte, address, value)

        for address in xrange(100):
            count = randint(0, self.memory_size / 2)
            start = randint(0, self.memory_size - count - 1)
            bytes_from_memory = memory.read_bytes(start, count)
            bytes_from_list = memory_copy[start:start + count]
            self.assertItemsEqual(bytes_from_memory, bytes_from_list)

    def test_load_image(self):
        processor = Processor(self.registers_count, self.memory_size)
        image = compile_code_from_str(self.code)

        processor.load_image(image)
        for memory_value, image_value in zip(processor.memory, image):
            self.assertEqual(memory_value, image_value)
