from unittest import TestCase

from emu.cpu.processor import Processor
from emu.decoders.instruction import InstructionDecoder
from emu.handlers.shift import asr, ror, lsr, lsl
from emu.handlers.instruction import InstructionHandler
from emu.utils.compile import compile_code_from_str
from emu.utils.binary import read_instructions


class InstructionDecoderTestCase(TestCase):

    def setUp(self):
        self.code = """
            add r1, r2, r3, asr r4
            add r5, r2, #220
            sub r8, r3, #65536

            subs r1, r2, r3
            adds r1, r2, r3

            cmp r2, r3
            tst r2, r3

            cmp r2, r3
            moveq r1, #100
            movhi r1, #150
        """
        self.image = compile_code_from_str(self.code)
        self.instructions = read_instructions(self.image)

        self.processor = Processor(registers_count=12, memory_size=1000)
        self.processor.registers['r2'] = 220
        self.processor.registers['r3'] = 150
        self.processor.registers['r4'] = 2

        self.decoder = InstructionDecoder(self.processor)

    def test_operands_decoding(self):
        code = self.instructions[0]
        self.assertEqual(self.decoder.get_destination_register_number(code), 1)
        self.assertEqual(self.decoder.get_source_operand_value(code), 220)
        self.assertEqual(self.decoder.get_shifter_operand_value(code), asr(150, 2))

        code = self.instructions[1]
        self.assertEqual(self.decoder.get_destination_register_number(code), 5)
        self.assertEqual(self.decoder.get_source_operand_value(code), 220)
        self.assertEqual(self.decoder.get_shifter_operand_value(code), 220)

        code = self.instructions[2]
        self.assertEqual(self.decoder.get_destination_register_number(code), 8)
        self.assertEqual(self.decoder.get_source_operand_value(code), 150)
        self.assertEqual(self.decoder.get_shifter_operand_value(code), 65536)

    def test_instruction_decoding(self):
        handlers = [
            self.decoder.decode(code)
            for code in self.instructions
        ]

        handlers[0].handle()
        self.assertEqual(handlers[0].get_name(), 'add')
        self.assertEqual(handlers[0].get_code(), 0b0100)
        self.assertEqual(self.processor.registers['r1'], 220 + asr(150, 2))

        handlers[1].handle()
        self.assertEqual(handlers[1].get_name(), 'add')
        self.assertEqual(handlers[1].get_code(), 0b0100)
        self.assertEqual(self.processor.registers['r5'], 220 + 220)

        handlers[2].handle()
        self.assertEqual(handlers[2].get_name(), 'sub')
        self.assertEqual(handlers[2].get_code(), 0b0010)
        self.assertEqual(self.processor.registers['r8'], 150 - 65536 + 2 ** 32)

    def test_state_changing(self):
        self.processor.registers['r2'] = 2 ** 31
        self.processor.registers['r3'] = 2 ** 31
        self.decoder.decode(self.instructions[4]).handle()
        self.assertEqual(self.processor.registers['r1'], 0)
        self.assertTrue(self.processor.state.get_flag('c'))
        self.assertTrue(self.processor.state.get_flag('z'))
        self.assertFalse(self.processor.state.get_flag('n'))
        self.assertTrue(self.processor.state.get_flag('v'))

        self.processor.registers['r1'] = 42
        self.processor.registers['r2'] = 150
        self.processor.registers['r3'] = 200
        self.decoder.decode(self.instructions[5]).handle()
        self.assertEqual(self.processor.registers['r1'], 42)
        self.assertTrue(self.processor.state.get_flag('c'))
        self.assertFalse(self.processor.state.get_flag('z'))
        self.assertTrue(self.processor.state.get_flag('n'))
        self.assertTrue(self.processor.state.get_flag('v'))

        self.processor.registers['r1'] = 42
        self.processor.registers['r2'] = 0
        self.processor.registers['r3'] = 2 ** 30
        self.decoder.decode(self.instructions[6]).handle()
        self.assertEqual(self.processor.registers['r1'], 42)
        self.assertFalse(self.processor.state.get_flag('c'))
        self.assertTrue(self.processor.state.get_flag('z'))
        self.assertFalse(self.processor.state.get_flag('n'))
        self.assertFalse(self.processor.state.get_flag('v'))

    def test_conditions(self):
        handler = self.decoder.decode(self.instructions[4])
        self.assertEqual(handler._condition_handler.get_name(), 'al')

        self.processor.registers['r1'] = 120
        self.processor.registers['r2'] = 0
        self.processor.registers['r3'] = 0
        self.decoder.decode(self.instructions[7]).handle()
        self.assertTrue(self.processor.state.get_flag('z'))
        self.decoder.decode(self.instructions[8]).handle()
        self.assertEqual(self.processor.registers['r1'], 100)
        self.decoder.decode(self.instructions[9]).handle()
        self.assertEqual(self.processor.registers['r1'], 100)

        self.processor.registers['r1'] = 120
        self.processor.registers['r2'] = 20
        self.processor.registers['r3'] = 50
        self.decoder.decode(self.instructions[7]).handle()
        self.assertFalse(self.processor.state.get_flag('z'))
        self.assertTrue(self.processor.state.get_flag('c'))
        self.decoder.decode(self.instructions[8]).handle()
        self.assertEqual(self.processor.registers['r1'], 120)
        self.decoder.decode(self.instructions[9]).handle()
        self.assertEqual(self.processor.registers['r1'], 150)
