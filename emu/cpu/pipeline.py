from emu.utils.binary import encode_instruction
from emu.decoders.instruction import InstructionDecoder


class Pipeline(object):

    def __init__(self, processor):
        self.decoder = InstructionDecoder(processor)
        self.processor = processor

    def retrieve_instruction(self):
        memory = self.processor.memory
        pointer = self.processor.registers['pc']
        instruction_bytes = memory.read_bytes(pointer, 4)
        instruction_code = encode_instruction(instruction_bytes)
        return instruction_code

    def decode_instruction(self, code):
        return self.decoder.decode(code)

    def handle_instruction(self, instruction_handler):
        instruction_handler.handle()

    def itersteps(self):
        try:
            image_size = self.processor.memory.get_image_len()
            while self.processor.registers['pc'] < image_size:
                instructon_code = self.retrieve_instruction()
                instruction_handler = self.decode_instruction(instructon_code)
                self.handle_instruction(instruction_handler)
                self.processor.registers['pc'] += 4
                yield {
                    'instruction_code': instructon_code,
                    'instruction_handler': instruction_handler,
                }
        except IndexError as e:
            print e
        except ValueError as e:
            print e

    def launch(self):
        return [step for step in self.itersteps()]
