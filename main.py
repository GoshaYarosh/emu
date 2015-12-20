from argparse import ArgumentParser
from emu.cpu.processor import Processor
from emu.decoders.instruction import InstructionDecoder
from emu.utils.binary import read_image


message = """
Hello. I'm a arm emu. Glad to see you
Press:
  's' to handle next instruction
  'c' to run it to end
------------------------------------
"""

class Emu(object):

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

	def __init__(self):
		self.force_run = False
		parser = ArgumentParser()
		parser.add_argument('-f', '--file')
		args = parser.parse_args()

		self.processor = Processor(registers_count=12, memory_size=1000)
		self.image = read_image(args.file)
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
				instr_str ,
				"{} <= {}".format('n', self.processor.state.get_flag('n')),
				"{} <= {}".format('c', self.processor.state.get_flag('c')),
				"{} <= {}".format('z', self.processor.state.get_flag('z')),
				"{} <= {}".format('v', self.processor.state.get_flag('v')),
			)
		else:
			dst_reg_name = handler.get_dst_reg_name()
			dst_reg_value = self.processor.registers[dst_reg_name]
			print "<0x{:08x}>: {:30} (changes: {} <= {})".format(
				instruction_addr, 
				instr_str, 
				dst_reg_name, 
				dst_reg_value
			) 
		print

	def make_steps(self):
		for step in self.processor.pipeline.itersteps():
			self.wait_for_press(lambda: self.make_step(step))


if __name__ == '__main__':
	Emu()