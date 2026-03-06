class CodeWriter:
    def __init__(self, filepath):
        self.file = open(filepath, "w")
        self.file_name = filepath.split("/")[-1].replace(".asm", "")
        self.label_count = 0

        self.segments = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }


    def writeArithmetic(self, line):
        assembly = [f"// {line}"]

        if line in ["add", "sub", "and", "or"]:
            assembly += [
                "@SP", "AM=M-1", "D=M", "A=A-1"
            ]
            if line == "add":
                assembly += ["M=D+M"]
            if line == "sub":
                assembly += ["M=M-D"]
            if line == "and":
                assembly += ["M=M&D"]
            if line == "or":
                assembly += ["M=M|D"]
        
        elif line in ["not", "neg"]:
            assembly += ["@SP", "A=M-1"]

            if line == "not":
                assembly += ["M=!M"]
            if line == "neg":
                assembly += ["M=-M"]

        elif line in ["eq", "gt", "lt"]:
            label = f"COMP_{self.label_count}"
            self.label_count += 1
            jmp = {"eq" : "JEQ", "gt": "JGT", "lt": "JLT"}[line]
            assembly += ["@SP", 
                         "AM=M-1", 
                         "D=M", 
                         "A=A-1", 
                         "D=M-D",
                         "M=-1",
                         f"@{label}",
                         f"D;{jmp}",
                         "@SP",
                        "A=M-1",
                        "M=0", 
                        f"({label})"]

        self.write(assembly)


    def writePushPop(self, type, seg, idx):
        if type == "push":
            assembly = [f"// {type} {seg} {idx}"]
            
            if seg == "constant":
                assembly += [f"@{idx}", "D=A" ]
            if seg in self.segments:
                assembly += [f"@{self.segments[seg]}", "D=M", f"@{idx}", "A=D+A", "D=M"]
            if seg == "temp":
                assembly += [f"@{5 + int(idx)}", "D=M"]
            if seg == "pointer":
                cmd = "THIS" if idx == "0" else "THAT"
                assembly += [f"@{cmd}", "D=M"]
            if seg == "static":
                assembly += [f"@{self.file_name}.{idx}", "D=M"]

            
            assembly += ["@SP", "A=M", "M=D", "@SP", "M=M+1"]

        if type == "pop":
            assembly = [f"// {type} {seg} {idx}"]
            if seg in self.segments:
                assembly += [f"@{self.segments[seg]}", "D=M", f"@{idx}", "D=D+A", "@R13", "M=D"]
            if seg == "temp":
                assembly += [f"@{5 + int(idx)}", "D=A", "@R13", "M=D"]
            if seg == "pointer":
                cmd = "THIS" if idx == "0" else "THAT"
                assembly += [f"@{cmd}", "D=A", "@R13", "M=D"]
            if seg == "static":
                assembly += [f"@{self.file_name}.{idx}", "D=A", "@R13", "M=D"]

            assembly += ["@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]

        self.write(assembly)



    
    def write(self, instructions):
        self.file.write("\n".join(instructions) + "\n\n")

    def close(self):
        self.file.write("\n(END)\n@END\n0;JMP\n")
        self.file.close()