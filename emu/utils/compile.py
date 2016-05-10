from os import remove
from subprocess import call
from os.path import splitext, abspath, dirname
from tempfile import NamedTemporaryFile

from emu.utils.binary import read_image


def compile_code_from_str(asm_code):
    source_file_name = '.arm/temp.asm'
    with open('.arm/temp.asm', 'w+') as source:
        source.write(asm_code)
        source.seek(0)
    compile_code_from_file(source_file_name)
    binary_file_name = splitext(source_file_name)[0] + '.bin'
    image = read_image(binary_file_name)
    remove(binary_file_name)
    remove(source_file_name)
    return image


def compile_code_from_file(source_file_name):
    with NamedTemporaryFile('w+') as out:
        fasm_path = dirname(abspath(__file__)) + '/fasmarm'
        command = "{0} {1}".format(fasm_path, source_file_name)
        exitcode = call(command, stdout=out, stderr=out, shell=True)
        if exitcode:
            out.seek(0)
            raise IOError('Compilation error {}'.format(out.read()))
