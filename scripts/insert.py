#!/usr/bin/env python3

import os
import subprocess
import sys
import shutil
import binascii
import textwrap
import sys
import argparse
import _io

if sys.version_info < (3, 4):
        print('Python 3.4 or later is required.')
        sys.exit(1)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--offset', metavar='offset',
                    help='offset to insert at', default=0x800000)
parser.add_argument('--input', metavar='file', 
                    help='input filename', default='BPRE0.gba')
parser.add_argument('--output', metavar='file', 
                    help='output filename', default='test.gba')
args = parser.parse_args()

def get_text_section():
        # Dump sections
        with open("build/rom.sym", "r") as symfile:
            lines = symfile.readlines()
        
        # Find text section
        text = filter(lambda x: x.strip().endswith('.text'), lines)
        section = list(text)[0]
        
        # Get the offset
        offset = int(section.split(' ')[0], 16)
        
        return offset

def symbols(subtract=0):
        with open("build/rom_1.sym", "r") as symfile:
            lines = symfile.readlines()
        
        name = ''
        
        ret = {}
        for line in lines:
                parts = line.strip().split()
                
                if (len(parts) < 3):
                        continue
                        
                if (parts[1].lower() != 't'):
                        continue
                        
                offset = int(parts[0], 16)
                ret[parts[2]] = offset - subtract
                
        return ret

def insert(rom):
        where = int(args.offset, 16)
        rom.seek(where)
        print("Where is: " + str(where) + str(type(where)))
        with open('build/output.bin', 'rb') as binary:
                data = binary.read()
        rom.write(data)
        print("data is: " + str(type(data)))
        return where
                       
def hook(rom, space, hook_at, register=0):
        # Align 2
        if hook_at & 1:
            hook_at -= 1
            
        rom.seek(hook_at)
        
        register &= 7
        
        if hook_at % 4:
            data = bytes([0x01, 0x48 | register, 0x00 | (register << 3), 0x47, 0x0, 0x0])
        else:
            data = bytes([0x00, 0x48 | register, 0x00 | (register << 3), 0x47])
            
        space += 0x08000001
        data += (space.to_bytes(4, 'little'))
        rom.write(bytes(data))
		
def rom_write(new_ptr, address):
        rom.seek(int(address, 0))
        array = bytearray()
        array.append(int("0x" + hex(new_ptr)[7:], 0))
        array.append(int("0x" + hex(new_ptr)[5:7], 0))
        array.append(int("0x" + hex(new_ptr)[3:5], 0))
        array.append(int(hex(new_ptr)[:3], 0))
        rom.write(array)

def TryProcessFileInclusion(line: str, definesDict: dict) -> bool:
    if line.startswith('#include "'):
        try:
            path = line.split('"')[1].strip()
            with open(path, 'r') as file:
                for line in file:
                    if line.startswith('#define '):
                        try:
                            lineList = line.strip().split()
                            title = lineList[1]

                            if len(lineList) == 2 or lineList[2].startswith('//') or lineList[2].startswith('/*'):
                                define = True
                            else:
                                define = lineList[2]

                            definesDict[title] = define
                        except IndexError:
                            print('Error reading define on line"' + line.strip() + '" in file "' + path + '".')

        except Exception as e:
            print('Error including file on line "' + line.strip() + '".')
            print(e)

        return True  # Inclusion line; don't read otherwise

    return False

def TryProcessConditionalCompilation(line: str, definesDict: dict, conditionals: [(str, bool)]) -> bool:
    line = line.strip()
    upperLine = line.upper()
    numWordsOnLine = len(line.split())

    if upperLine.startswith('#IFDEF ') and numWordsOnLine > 1:
        condition = line.strip().split()[1]
        conditionals.insert(0, (condition, True))  # Insert at front
        return True
    elif upperLine.startswith('#IFNDEF ') and numWordsOnLine > 1:
        condition = line.strip().split()[1]
        conditionals.insert(0, (condition, False))  # Insert at front
        return True
    elif upperLine == '#ELSE':
        if len(conditionals) >= 1:  # At least one statement was pushed before
            condition = conditionals.pop(0)
            if condition[1] is True:
                conditionals.insert(0, (condition[0], False))  # Invert old statement
            else:
                conditionals.insert(0, (condition[0], True))  # Invert old statement
            return True
    elif upperLine == '#ENDIF':
        conditionals.pop(0)  # Remove first element (last pushed)
        return True
    else:
        for condition in conditionals:
            definedType = condition[1]
            condition = condition[0]

            if definedType is True:  # From #ifdef
                if condition not in definesDict:
                    return True  # If something isn't defined then skip the line
            else:  # From #ifndef
                if condition in definesDict:
                    return True  # If something is defined then skip the line

    return False

def Repoint(rom: _io.BufferedReader, space: int, repointAt: int, slideFactor=0):
    rom.seek(repointAt)

    space += (0x08000000 + slideFactor)
    data = (space.to_bytes(4, 'little'))
    rom.write(bytes(data))

def ReplaceBytes(rom: _io.BufferedReader, offset: int, data: str):
    ar = offset
    words = data.split()
    for i in range(0, len(words)):
        rom.seek(ar)
        intByte = int(words[i], 16)
        rom.write(bytes(intByte.to_bytes(1, 'big')))
        ar += 1

shutil.copyfile(args.input, args.output)
with open(args.output, 'rb+') as rom:
        offset = get_text_section()
        table = symbols(offset)
        where = insert(rom)
        # Adjust symbol table
        for entry in table:
                table[entry] += where

        # Read hooks from a file
        with open('hooks', 'r') as hooklist:
                for line in hooklist:
                        if line.strip().startswith('#'): continue
                        
                        symbol, address, register = line.split()
                        offset = int(address, 16) - 0x08000000
                        try:
                                code = table[symbol]
                        except KeyError:
                                print('Symbol missing:', symbol)
                                continue

                        hook(rom, code, offset, int(register))

        if os.path.isfile("bytereplacement"):
            with open("bytereplacement", 'r') as replacelist:
                definesDict = {}
                conditionals = []
                for line in replacelist:
                    if TryProcessFileInclusion(line, definesDict):
                        continue
                    if TryProcessConditionalCompilation(line, definesDict, conditionals):
                        continue
                    if line.strip().startswith('#') or line.strip() == '':
                        continue
 
                    offset = int(line[:8], 16) - 0x08000000
                    try:
                        ReplaceBytes(rom, offset, line[9:].strip())
                    except ValueError: #Try loading from the defines dict if unrecognizable character
                        newNumber = definesDict[line[9:].strip()]
                        try:
                            newNumber = int(newNumber)
                        except ValueError:
                            newNumber = int(newNumber, 16)

                        newNumber = str(hex(newNumber)).split('0x')[1]
                        ReplaceBytes(rom, offset, newNumber) 
        if os.path.isfile("routinepointers"):
            with open("routinepointers", 'r') as pointerlist:
                definesDict = {}
                conditionals = []
                for line in pointerlist:
                    if TryProcessFileInclusion(line, definesDict):
                        continue
                    if TryProcessConditionalCompilation(line, definesDict, conditionals):
                        continue
                    if line.strip().startswith('#') or line.strip() == '':
                        continue

                    symbol, address = line.split()
                    offset = int(address, 16) - 0x08000000
                    try:
                        code = table[symbol]
                    except KeyError:
                        print('Symbol missing:', symbol)
                        continue

                    Repoint(rom, code, offset, 1)
