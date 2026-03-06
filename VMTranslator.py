#!/bin/bash
import os
import sys

from Parser import Parser
from CodeWriter import CodeWriter





def getpath():
    if len(sys.argv) < 2:
        print("Usage: python.py VMTranslator.py <filepath>")
        return None, None
    
    path = sys.argv[1]
    vm_files = []

    if os.path.isfile(path) and path.endswith(".vm"):
        
        output_path = path.replace(".vm", ".asm")
        return [path], output_path
    elif os.path.isdir(path):

        for file in os.listdir(path):
            if file.endswith(".vm"):
                vm_files.append(os.path.join(path, file))

        folder_name = os.path.basename(os.path.normpath(path))
        output_path = os.path.join(path, f"{folder_name}.asm")
        return vm_files, output_path
    else:
        print("invalid path")
        return None, None
    

vm_files, output_path = getpath()

if vm_files:
    print(vm_files,output_path)

my_parser = Parser(vm_files[0])
code_writer = CodeWriter(output_path) 

while my_parser.hasMoreLines():
    type = my_parser.commandType()
    if type == "C_ARITHMETIC":
        op = my_parser.arg1()
        code_writer.writeArithmetic(op)
    elif type == "C_PUSH" or type == "C_POP":
        cmd = "push" if type == "C_PUSH" else "pop"
        seg = my_parser.arg1()
        index = my_parser.arg2()
        code_writer.writePushPop(cmd, seg, index)
    my_parser.advance()

code_writer.close()    

   
    
          

