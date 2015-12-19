from unittest import TestCase

from emu.cpu.processor import Processor
from emu.utils.compile import compile_code_from_str
from emu.utils.binary import read_instructions


class ProcessorPipelineTestCase(TestCase):

    def setUp(self):
        self.registers_count = 12
        self.memory_size = 1000
        self.processor = Processor(self.registers_count, self.memory_size)

        self.code = """
                mov r1, #2
                mov r2, #3
                add r3, r1, r2
                mov r3, r3, lsl 1
                b pipa
                mov r3, #123
            pipa:
        """
        self.instructions_count = len(self.code.strip().split('\n'))

        self.image = compile_code_from_str(self.code)
        self.processor.load_image(self.image)


    def test_instructions_decoding(self):
        pipeline = self.processor.pipeline
        steps = pipeline.launch()
        self.processor.load_image(self.image)

        instructions = read_instructions(self.image)
        for index, step in enumerate(steps):
            self.assertIn('instruction_code', step)
            self.assertEqual(step['instruction_code'], instructions[index])

    def test_run_simple_code(self):
        pipeline = self.processor.pipeline
        steps = pipeline.launch()
        self.assertEqual(self.processor.registers['r3'], 10)
