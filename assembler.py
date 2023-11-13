TYPE_MAP = {
    'lb': 'i',
    'lh': 'i',
    'lw': 'i',
    'lbu': 'i',
    'lhu': 'i',
    'addi': 'i',
    'slli': 'i',
    'slti': 'i',
    'sltiu': 'i',
    'xori': 'i',
    'srli': 'i',
    'srai': 'i',
    'ori': 'i',
    'andi': 'i',
    'jalr': 'i',
    'add': 'r',
    'sub': 'r',
    'sll': 'r',
    'slt': 'r',
    'sltu': 'r',
    'xor': 'r',
    'srl': 'r',
    'sra': 'r',
    'or': 'r',
    'and': 'r',
    'mul': 'r',
    'mulh': 'r',
    'mulhsu': 'r',
    'mulhu': 'r',
    'div': 'r',
    'divu': 'r',
    'rem': 'r',
    'remu': 'r',
    'sb': 's',
    'sh': 's',
    'sw': 's',
    'beq': 'sb',
    'bne': 'sb',
    'blt': 'sb',
    'bge': 'sb',
    'bltu': 'sb',
    'bgeu': 'sb',
    'auipc': 'u',
    'lui': 'u',
    'jal': 'uj',
}


I_OPCODE_MAP = {
    'lb': ('000', '0000011'),
    'lh': ('001', '0000011'),
    'lw': ('010', '0000011'),
    'lbu': ('100', '0000011'),
    'lhu': ('101', '0000011'),
    'addi': ('000', '0010011'),
    'slli': ('001', '0010011'),
    'slti': ('010', '0010011'),
    'sltiu': ('011', '0010011'),
    'xori': ('100', '0010011'),
    'srli': ('101', '0010011'),
    'srai': ('101', '0010011'),
    'ori': ('110', '0010011'),
    'andi': ('111', '0010011'),
    'jalr': ('000', '1100111'),
}


R_OPCODES = {
    'add': ('000', '0000000'),
    'sub': ('000', '0100000'),
    'sll': ('001', '0000000'),
    'slt': ('010', '0000000'),
    'sltu': ('011', '0000000'),
    'xor': ('100', '0000000'),
    'srl': ('101', '0000000'),
    'sra': ('101', '0100000'),
    'or': ('110', '0000000'),
    'and': ('111', '0000000'),
    'mul': ('000', '0000001'),
    'mulh': ('001', '0000001'),
    'mulhsu': ('010', '0000001'),
    'mulhu': ('011', '0000001'),
    'div': ('100', '0000001'),
    'divu': ('101', '0000001'),
    'rem': ('110', '0000001'),
    'remu': ('111', '0000001'),
}


S_FUNCT3 = {
    'sb': "000",
    'sh': '001',
    'sw': '010',
}


SB_FUNCT3 = {
    'beq': '000',
    'bne': '001',
    'blt': '100',
    'bge': '101',
    'bltu': '110',
    'bgeu': '111',
}


U_OPCODES = {
    'auipc': '0010111',
    'lui': '0110111',
}


def assemble_codes(codes):
    addr = 0
    instructions = []

    for code in codes:
        if code == '\n':
            continue
        instruction, addr = add_instruction(code, addr)
        instructions.append(instruction)
        addr += 4

    instructions.append(':00000001FF')

    return instructions


def add_instruction(code: str, addr: int):
    tokens = code.strip().split(' ')
    hex_str = ''
    offset = 0
    if ':' in tokens[0]:
        addr = tokens[0][0:-1]
        addr = int(addr, 16)
        ins_type = TYPE_MAP[tokens[1]]
        offset = 1
    elif tokens[0] == 'break':
        test = f'04{hex(addr)[2:].zfill(4)}00{73001000}'.upper()
        return (':' + test + checksum(test) + '\n', addr)
    else:
        ins_type = TYPE_MAP[tokens[0]]

    for i in range(1 + offset, len(tokens)):
        tokens[i] = tokens[i].replace('x', '')

    if ins_type == 'i':
        immediate = format(int(tokens[3 + offset]) & 0xFFF, '012b')
        rs1 = str(bin(int(tokens[2 + offset])))[2:].zfill(5)
        rd = str(bin(int(tokens[1 + offset])))[2:].zfill(5)

        instruction_code = tokens[0 + offset]
        code = I_OPCODE_MAP[instruction_code]
        bin_str = immediate + rs1 + code[0] + rd + code[1]
        hex_str = hex(int(bin_str, 2))[2:].zfill(8)

    elif ins_type == 'r':
        instruction_code = tokens[0 + offset]
        rd = str(bin(int(tokens[1 + offset])))[2:].zfill(5)
        rs1 = str(bin(int(tokens[2 + offset])))[2:].zfill(5)
        rs2 = str(bin(int(tokens[3 + offset])))[2:].zfill(5)
        code = R_OPCODES[instruction_code]
        bin_str = code[1] + rs2 + rs1 + code[0] + rd + '0110011'
        hex_str = hex(int(bin_str, 2))[2:].zfill(8)

    elif ins_type == 's':
        funct3 = S_FUNCT3[tokens[0 + offset]]
        rs1 = str(bin(int(tokens[1 + offset])))[2:].zfill(5)
        rs2 = str(bin(int(tokens[2 + offset])))[2:].zfill(5)
        immediate = str(bin(int(tokens[3 + offset])))[2:].zfill(12)

        bin_str = immediate[:7] + rs2 + rs1 + funct3 + immediate[7:] + '0100011'
        hex_str = hex(int(bin_str, 2))[2:].zfill(8)

    elif ins_type == 'sb':
        funct3 = SB_FUNCT3[tokens[0 + offset]]
        rs1 = str(bin(int(tokens[1 + offset])))[2:].zfill(5)
        rs2 = str(bin(int(tokens[2 + offset])))[2:].zfill(5)
        immediate = to_signed_binary(int(tokens[3 + offset]) // 2)

        bin_str = immediate[0] + immediate[2:8] + rs2 + rs1 + funct3 + immediate[8:] + immediate[1] + '1100011'
        hex_str = hex(int(bin_str, 2))[2:].zfill(8)

    elif ins_type == 'u':
        opcode = U_OPCODES[tokens[0 + offset]]
        rd = str(bin(int(tokens[1 + offset])))[2:].zfill(5)
        immediate = str(bin(int(tokens[2 + offset])))[2:].zfill(20)

        bin_str = immediate + rd + opcode
        hex_str = hex(int(bin_str, 2))[2:].zfill(8)

    elif ins_type == 'uj':
        rd = str(bin(int(tokens[1 + offset])))[2:].zfill(5)
        immediate = str(bin(int(tokens[2 + offset])))[2:].zfill(20)
        result = [immediate[0], immediate[1:9], immediate[9:19], immediate[19]]
        bin_str = result[0] + result[2] + result[3] + result[1] + rd + '1101111'

        hex_str = hex(int(bin_str, 2))[2:].zfill(8)

    chunks = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]
    reversed_chunks = chunks[::-1]
    result_string = ''.join(reversed_chunks)

    test = f'04{hex(addr)[2:].zfill(4)}00{result_string}'.upper()

    return(':' + test + checksum(test) + '\n', addr)


def checksum(data):
    byte_data = bytes.fromhex(data)
    total = sum(byte_data)

    curr_checksum = ((~total) + 1) & 0xFF
    checksum_hex = format(curr_checksum, '02X')
    return checksum_hex


def to_signed_binary(value, width=12):
    value &= (1 << width) - 1
    binary_str = bin(value)[2:]

    binary_str = binary_str.zfill(width)

    return binary_str

