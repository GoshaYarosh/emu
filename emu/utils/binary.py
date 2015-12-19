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
    return int(str(instruction_bytes)[::-1].encode('hex'), 16)


def pretty(instruction_code):
    bits = str("{:032b}".format(instruction_code))[::-1]
    print "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(
        bits[28:32][::-1],
        bits[25:28][::-1],
        bits[21:25][::-1],
        bits[20:21][::-1],
        bits[16:20][::-1],
        bits[12:16][::-1],
        bits[8:12][::-1],
        bits[7:8][::-1],
        bits[5:7][::-1],
        bits[4:5][::-1],
        bits[0:4][::-1],
    )
    print
