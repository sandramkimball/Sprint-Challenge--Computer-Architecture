"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010 
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
LD   = 0b10000011
ST   = 0b10000100
PRA  = 0b01001000
ADD  = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


# - [ ] Add the `CMP` instruction and `equal` flag to your LS-8.
# - [ ] Add the `JMP` instruction.
# - [ ] Add the `JEQ` and `JNE` instructions.

class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8 
        self.pc = 0 # Program Counter
        self.SP = 0xF4 # Stack Pointer, register[SP]

    def load(self): 
        """Load a program into memory."""
        address = 0
        program = sys.argv[1]

        if len(sys.argv) != 2:
            print(f'usage: file.py {program}')
            sys.exit(1)
    
        try: 
            with open(program) as f:
                count = 0
                for line in f:
                    count += 1
                    # ignore comments
                    comment_split = line.split('#')
                    # strip out whitespace
                    num = comment.split[0].strip()
                    # ignore blank lines
                    try:
                        val = int(num, 2)
                    except ValyeError:
                        continue

                    self.ram[address] = val
                    address += 1
                    print(f'{x:08b}: {x:d}')

        except FileNotFoundError:
            print('File not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(MAR):
        return self.ram[MAR]
        # self.pc += 2

    def ram_write(MAR, MDR): 
        self.ram[MAR] = MDR
        # self.pc += 3

    def run(self):
        # if/elif = O(n) || O(1)
        # read address in pc, store result in IR (Instruction Register)
        running = True
        while running is True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1) #address = register[pc + 1]
            operand_b = self.ram_read(self.pc + 2)

            # HLT
            if IR == 0b00000001: 
                running = False
                # self.pc += 1

            # LDI
            elif IR == 0b10000010: 
                # load immediate, store val in reg
                self.reg[operand_a] = operand_b
                self.pc += 3

            # PRN
            elif IR == 0b01000111:
                # prints num value in rgstr
                print(self.reg[operand_a])
                self.pc += 2
 
            # MUL
            elif IR == 0b10100010:
                # self.alu(MUL, operand_a, operand_b)
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            # PUSH
            elif IR == 0b01000101:
                # Copy val from address to given reg
                # decrement SP
                self.SP -= 1
                self.ram[self.SP] = self.reg[operand_a]
                self.pc += 2

            # POP
            elif IR == 0b01000110:
                # copy val from address
                # increment SP
                self.reg[operand_a] = self.ram[self.SP]
                self.SP += 1
                self.pc += 2

            # CALL
            elif IR == 0b01010000:
                # decrement SP
                self.SP -= 1
                self.ram[self.SP] = self.pc + 2
                # store the instruction
                self.pc = self.reg[operand_a]

            # RET
            elif IR == 0b00010001:
                # pop val from stack and return 
                self.pc = self.ram[self.SP]
                self.SP += 1

            # ADD
            elif IR == 0b10100000:
                # pop val from stack and store in PC
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3

            else:
                running = False
                print(f'Unknown command: {command}')
                sys.exit(1)


def HLT(self):
    running = False
    # self.pc += 1

def PRN(self):
    # prints num value in rgstr
    print(self.reg[operand_a])
    self.pc += 2

def LDI(self):
    # load immediate, store val in reg
    self.reg[operand_a] = operand_b
    self.pc += 3

def MUL(self):
    # self.alu(MUL, operand_a, operand_b)
    self.reg[operand_a] *= self.reg[operand_b]
    self.pc += 3

def PUSH(self):
    # Copy val from address to given reg
    # decrement SP
    self.SP -= 1
    self.ram[self.SP] = self.reg[operand_a]
    self.pc += 2

def POP(self):
    # copy val from address
    # increment SP
    self.reg[operand_a] = self.ram[self.SP]
    self.SP += 1
    self.pc += 2

def CALL(self):
    # decrement SP
    self.SP -= 1
    self.ram[self.SP] = self.pc + 2
    # store the instruction
    self.pc = self.reg[operand_a]

def RET(self):
    # pop val from stack and return 
    self.pc = self.ram[self.SP]
    self.SP += 1

def ADD(self):

def CMP(self):
    #handled by alu
    if register_a = register_b:
        # set flag to equal
        'E' = 1
        'L' = 0
        'G' = 0
    if register_a < register_b:
        # set flag to L
        'E' = 0
        'L' = 1
        'G' = 0
    if register_a > register_b:
        # set flag to G
        'E' = 0
        'L' = 0
        'G' = 1

def JMP(self):
    # jump to address stored in given reg
    # set PC to this address
    self.pc = register[self.SP]

def JEQ(self):
    #if flag = Equal, jump to address stored in given reg
    if 'E' = 1:
        self.JMP()
    else:
        continue

def JNE(self):
    # if flag is not Equal, jump to address in given reg
    if 'E' = 0:
        self.JMP()
    else:
        continue

    # pop val from stack and store in PC
    self.reg[operand_a] += self.reg[operand_b]
    self.pc += 3