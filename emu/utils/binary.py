def read_image(binary_file_name):
    with open(binary_file_name, 'r+') as binary:
        content = binary.read()
        return bytearray(content)

def read_instructions(binary_image):
    instructions = [
        encode_instruction(binary_image[i:i+4])
        for i in xrange(0, len(binary_image), 4)
    ]
    return instructions


def read_instructions_from_file(binary_file_name):
    image = read_image(binary_file_name)
    return read_instructions(image)

def encode_instruction(instruction_bytes):
    return int(str(instruction_bytes).encode('hex'), 16)
