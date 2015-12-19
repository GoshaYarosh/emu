from unittest import TestCase

from emu.cpu.processor import Processor
from emu.decoders.base import Decoder
from emu.decoders.shift import ShiftDecoder
from emu.handlers.shift import asr, ror, lsl, lsr
from emu.utils.compile import compile_code_from_str
from emu.utils.binary import read_instructions
from emu.utils.binary import pretty, encode_instruction


class ShiftDecoderTestCase(TestCase):

    def setUp(self):
        self.code = """
            add r1, r2, r3, asr r4
            add r1, r2, r3, asr #4

            and r1, r2, r3, ror #3
            and r1, r2, r3, lsl #3
            and r1, r2 ,r3, lsr r4
        """
        self.image = compile_code_from_str(self.code)
        self.instructions = read_instructions(self.image)

        self.processor = Processor(registers_count=12, memory_size=1000)
        self.processor.registers['r3'] = 42
        self.processor.registers['r4'] = 2

        self.decoder = ShiftDecoder(self.processor)

    def test_shift_decoder(self):
        code = self.instructions[0]
        self.assertEqual(self.decoder.get_shifted_value(code), 42)
        self.assertEqual(self.decoder.get_shift_amount(code), 2)
        self.assertEqual(self.decoder.decode(code).get_shift_name(), 'asr')

        code = self.instructions[1]
        self.assertEqual(self.decoder.get_shifted_value(code), 42)
        self.assertEqual(self.decoder.get_shift_amount(code), 4)
        self.assertEqual(self.decoder.decode(code).get_shift_code(), 0b10)
        self.assertEqual(self.decoder.decode(code).get_shift_name(), 'asr')

        code = self.instructions[2]
        self.assertEqual(self.decoder.decode(code).get_shift_code(), 0b11)
        self.assertEqual(self.decoder.decode(code).get_shift_name(), 'ror')

        code = self.instructions[3]
        self.assertEqual(self.decoder.decode(code).get_shift_code(), 0b00)
        self.assertEqual(self.decoder.decode(code).get_shift_name(), 'lsl')

        code = self.instructions[4]
        self.assertEqual(self.decoder.decode(code).get_shift_code(), 0b01)
        self.assertEqual(self.decoder.decode(code).get_shift_name(), 'lsr')


class ShiftHandlerTestCase(ShiftDecoderTestCase):

    def setUp(self):
        super(ShiftHandlerTestCase, self).setUp()

    def test_arithmetic_right_shift(self):
        self.assertEqual(0b11 << 30, asr(2 ** 31, 1))
        self.assertEqual(0b01 << 29, asr(2 ** 30, 1))
        self.assertEqual(2 ** 32 - 1, asr(2 ** 31, 42))

    def test_rotate_right_shift(self):
        self.assertEqual(2 ** 31 + 1, ror(0b11, 1))
        self.assertEqual(0b1, ror(0b10, 1))
        self.assertEqual(2 ** 32 - 1, ror(2 ** 32 - 1, 42))

    def test_logical_left_shift(self):
        self.assertEqual(0b100, lsl(0b1, 2))
        self.assertEqual(2 ** 31, lsl(0b1, 31))
        self.assertEqual(0, lsl(0b1, 42))

    def test_logical_right_shift(self):
        self.assertEqual(0b100, lsr(0b10000, 2))
        self.assertEqual(1, lsr(2 ** 32 - 1, 31))
        self.assertEqual(0b111, lsr(0b111000, 3))

    def test_shift_handler(self):
        handlers = [
            self.decoder.decode(instruction)
            for instruction in self.instructions
        ]
        self.assertEqual(handlers[0].handle(), asr(42, 2))
        self.assertEqual(handlers[1].handle(), asr(42, 4))
        self.assertEqual(handlers[2].handle(), ror(42, 3))
        self.assertEqual(handlers[3].handle(), lsl(42, 3))
        self.assertEqual(handlers[4].handle(), lsr(42, 2))
