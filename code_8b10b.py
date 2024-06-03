#!/usr/bin/python3

from enum import Enum
from encoder import *

class Disparity(Enum):
    Neg = 0
    Pos = 1

def encode_byte(byte, current_disp = 0, control_byte = 0):
    data_5b = byte & 0x1F
    data_3b = (byte >> 5) & 0x7

    code_5b = encoder_data_5b6b[data_5b]
    code_3b = encoder_data_3b4b[data_3b]

    code = 0
    next_rd = current_disp
    if code_5b['even'] == 1:
        code |= (code_5b[0] << 4)
    else:
        code |= (code_5b[current_disp] << 4)
        next_rd = not current_disp
    
    if code_3b['even'] == 1:
        code |= (code_3b[0])
    else:
        code |= (code_3b[next_rd])
        next_rd = not next_rd
 
    return code, next_rd

def encode_data(data, disparity=0, verbose=0):
    encoded_data = []
    for byte in data:
        code, next_rd = encode_byte(byte, disparity)
        encoded_data.append(code)
        disparity = next_rd

        if verbose:
            print(f"0x{byte:02x}: 0x{code:03x}")

    return encoded_data


