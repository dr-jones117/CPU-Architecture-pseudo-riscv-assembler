import sys
from assembler import assemble_codes
import os

out_file_name = 'object.obj'

def print_usage_statement():
    print("Usage: python3 riscvasm.py [code-file-name].txt [object-file-name].obj")
    return


def load_file(file_name):
    try:
        with open(file_name) as file:
            program_content = file.readlines()
            return program_content
    except FileNotFoundError:
        print(f'Couldn\'t open the file \'{file_name}\'')
        return None


def check_and_load_program():
    if len(sys.argv) > 3  or len(sys.argv) < 2:
        print_usage_statement()
        sys.exit(1)
    if len(sys.argv) == 3:
        global out_file_name
        out_file_name = sys.argv[2]
        return load_file(sys.argv[1])
    else:
        return load_file(sys.argv[1])


def main():
    codes = check_and_load_program()
    assembled_codes = assemble_codes(codes)
    out_directory = os.path.dirname(out_file_name)

    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
        os.chmod(out_directory, 0o777)
    with open(out_file_name, 'w') as file:
        file.writelines(assembled_codes)


if __name__ == '__main__':
    main()
