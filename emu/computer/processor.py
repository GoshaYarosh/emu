from emu.utils.binary import encode_instruction
from memory.registers import RegistersManager
from memory.random_access import RandomAccessMemoryManager
from decoders.instruction import InstructionDecoder


class Pipeline(object):

    def __init__(self, processor):
        self.decoder = InstructionDecoder()
        self.processor = processor

    def retrieve_instruction(self):
        memory = self.processor.memory
        pointer = self.processor.registers['pc']
        instruction_bytes = memory.read_bytes(pointer, 4)
        instruction_code = encode_instruction(instruction_bytes)
        return instruction_code

    def decode_instruction(self, code):
        handler = self._decoder.decode(self, processor, code)
        return handler

    def handle_instruction(self, instruction_handler):
        instruction_handler.handle(processor)

    def itersteps(self):
        try:
            image_size = len(self.processor.memory.image)
            while self.processor.registers['pc'] < image_size:
                instructon_code = self.retrieve_instruction()
                instruction_handler = None#self.decode_instruction(instructon_code)
                #self.handle_instruction(instruction_handler)
                self.processor.registers['pc'] += 4
                yield {
                    'instruction_code': instructon_code,
                    'instruction_handler': instruction_handler
                }
        except IndexError as e:
            print e
        except ValueError as e:
            print e

    def launch(self):
        return [step for step in self.itersteps()]


class Processor(object):

    def __init__(self, registers_count, memory_size):
        self.pipeline = Pipeline(self)
        self.registers = RegistersManager(registers_count)
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
