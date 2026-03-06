class Parser:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            self.clean_lines = [line.strip() for line in f if line.split("//")[0].strip()]
        self.curr = 0

    def hasMoreLines(self):
        if self.curr < len(self.clean_lines):
            return True
        
    def advance(self):
        if self.hasMoreLines():
            self.curr += 1

    def curr_command(self):
        return self.clean_lines[self.curr]
        
    def commandType(self):
        cmd = self.curr_command().split()[0]
        types = {
            "push": "C_PUSH",
            "pop": "C_POP"
        }

        return types.get(cmd, "C_ARITHMETIC")
 
    def arg1(self):
        parts = self.curr_command().split()

        if self.commandType() == "C_ARITHMETIC":
            return parts[0]
        return parts[1]

    def arg2(self):
        parts = self.curr_command().split()
        return parts[2]
    

    

