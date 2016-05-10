from argparse import ArgumentParser
from emu.cpu.processor import Processor
from emu.decoders.instruction import InstructionDecoder
from emu.utils.binary import read_image

message = """
Hello. I'm a arm emu. Glad to see you
Press:
  's' to handle next instruction
  'c' to run it to end
  'r' to print all register values
  'f' to print processor state
  'clear' to clear output
  'exit' to exit from emu
------------------------------------
"""


class Emu(object):

    def print_registers(self):
        for name, register in self.processor.registers:
            print "{}: {:}".format(name, register.get_value())
        print

    def print_flags(self):
        print "negative({}): {}".format('n', self.processor.state.get_flag('n'))
        print "carried({}): {}".format('c', self.processor.state.get_flag('c'))
        print "zero({}): {}".format('z', self.processor.state.get_flag('z'))
        print "overflowed({}): {}".format('v', self.processor.state.get_flag('v'))
        print

    def wait_for_press(self, callback):
        if self.force_run:
            callback()
        else:
            some_key = raw_input(':')
            if some_key == 's':
                callback()
            if some_key == 'c':
                self.force_run = True
                callback()
            if some_key == 'r':
                self.print_registers()
                self.wait_for_press(callback)
            if some_key == 'f':
                self.print_flags()
                self.wait_for_press(callback)
            if some_key == 'clear':
                for i in xrange(100):
                    print
                self.wait_for_press(callback)
            if some_key == 'exit':
                exit(0)

    def __init__(self):
        self.force_run = False
        parser = ArgumentParser()
        parser.add_argument('-b', '--binary')
        args = parser.parse_args()

        self.processor = Processor(registers_count=12, memory_size=1000)
        if args.binary:
            self.image = read_image(args.binary)
            self.processor.load_image(self.image)

            print message
            self.make_steps()

    def make_step(self, step):
        handler = step['instruction_handler']
        code = step['instruction_code']

        instruction_addr = self.processor.registers['pc']
        instr_str = InstructionDecoder(self.processor).to_str(code)

        name = handler.get_name()
        if name in ['tst', 'teq', 'cmp', 'cmn']:
            print "<0x{:08x}>: {:30} (changes: {} {} {} {})".format(
                instruction_addr,
                instr_str,
                "{} <= {}".format('n', self.processor.state.get_flag('n')),
                "{} <= {}".format('c', self.processor.state.get_flag('c')),
                "{} <= {}".format('z', self.processor.state.get_flag('z')),
                "{} <= {}".format('v', self.processor.state.get_flag('v')),
            )
        else:
            dst_reg_name = handler.get_dst_reg_name()
            dst_reg_value = self.processor.registers[dst_reg_name]
            print "<0x{:08x}>: {:30} (changes: {} <= 0x{:x})".format(
                instruction_addr,
                instr_str,
                dst_reg_name,
                dst_reg_value
            )
        print

    def make_steps(self):
        for step in self.processor.pipeline.itersteps():
            self.wait_for_press(lambda: self.make_step(step))

        self.print_registers()
        self.print_flags()


if __name__ == '__main__':
    Emu()
