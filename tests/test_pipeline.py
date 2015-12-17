from unittest import TestCase

from emu.computer.processor import Processor
from emu.utils.compile import compile_code_from_str
from emu.utils.binary import read_instructions


class ProcessorPipelineTestCase(TestCase):

    def setUp(self):
        self.registers_count = 12
        self.memory_size = 1000
        self.processor = Processor(self.registers_count, self.memory_size)

        self.code = """
            mov r2, #11
            mov r3, #10
            add r1, r2, r3
            cmp r1, #15
            add r2, r1, r3, lsl r4
            sub r1, r2, r3
        """
        self.instructions_count = len(self.code.strip().split('\n'))

        self.image = compile_code_from_str(self.code)
        self.processor.load_image(self.image)


    def test_instructions_decoding(self):
        pipeline = self.processor.pipeline
        steps = pipeline.launch()
        self.processor.load_image(self.image)
        self.assertItemsEqual(steps, (step for step in pipeline.itersteps()))

        instructions = read_instructions(self.image)
        for index, step in enumerate(steps):
            self.assertIn('instruction_code', step)
            self.assertEqual(step['instruction_code'], instructions[index])
