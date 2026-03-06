# a vm-to-hack translator
There's three modules.
=> VMTranslator.py; which is the driver. kind of like the main. inside of here you see the roadmap of all that happens.
=> Parser.py; this module takes the input vm file and helps us walk through each line etc
=> CodeWriter.py; this is the engine. this module takes a line of vm and translates it to asm code accordingly. whether its a arithmetic operation, or a push or pop operation. 
