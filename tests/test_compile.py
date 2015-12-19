from __future__ import absolute_import
from unittest import TestCase
from tempfile import NamedTemporaryFile

from emu.utils.compile import compile_code_from_str
from emu.utils.compile import compile_code_from_file
from emu.utils.binary import read_image
from emu.utils.binary import read_instructions
from emu.utils.binary import read_instructions_from_file


class CompileCodeTestCase(TestCase):

    def setUp(self):
        self.code = """
            mov r2, #11
            mov r3, #10
            add r1, r2, r3
            cmp r1, #15
        """
        self.instructions_count = len(self.code.strip().split('\n'))

    def test_compile_code_from_file(self):
        with NamedTemporaryFile(mode='w+') as source:
            source.write(self.code)
            source.seek(0)
            exitcode = compile_code_from_file(source.name)
            instructions = read_instructions_from_file(source.name + '.bin')
            self.assertEqual(len(instructions), self.instructions_count)

        self.assertRaises(IOError, compile_code_from_file, 'some_file')

    def test_compile_code_from_str(self):
        image = compile_code_from_str(self.code)
        instructions = read_instructions(image)
        self.assertEqual(len(instructions), self.instructions_count)
