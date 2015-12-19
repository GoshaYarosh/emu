from emu.cpu.pipeline import Pipeline
from emu.cpu.registers import RegistersManager
from emu.cpu.state import StateManager
from emu.decoders.instruction import InstructionDecoder
from emu.memory.ram import RandomAccessMemoryManager
from emu.utils.binary import encode_instruction


class Processor(object):

    def __init__(self, registers_count, memory_size):
        self.pipeline = Pipeline(self)
        self.registers = RegistersManager(registers_count)
        self.state = StateManager()
        self.memory = RandomAccessMemoryManager(memory_size)

    def load_image(self, binary_image, offset=0):
        self.registers['pc'] = offset
        try:
            self.memory.load_image(binary_image)
        except ValueError as e:
            print e
        except TypeError as e:
            print e

    def run_image(self):
        self.pipeline.launch()
