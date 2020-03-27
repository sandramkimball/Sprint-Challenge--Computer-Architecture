"""CPU functionality."""

import sys


class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8 
        self.pc = 0 # Program Counter
        self.IR = None
        self.SP = 0xF4 # Stack Pointer, register[SP]
        self.FL = 0 # flag
        self.branchtable = {} # funcs indexed by opcode val
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        self.branchtable[0b00000001] = self.handle_HLT
        self.branchtable[0b10000010] = self.handle_LDI
        self.branchtable[0b01000111] = self.handle_PRN
        self.branchtable[0b10100111] = self.handle_CMP
        self.branchtable[0b01010100] = self.handle_JMP
        self.branchtable[0b01010101] = self.handle_JEQ
        self.branchtable[0b01010110] = self.handle_JNE

    def load(self): 
        """Load a program into memory."""
        address = 0
        program = sys.argv[1]

        if len(sys.argv) != 2:
            print(f'usage: file.py {program}')
            sys.exit(1)
    
        try: 
            with open(program, 'rb') as f:
                for line in f:
                    print(line)
        
                    # ignore comments
                    comment = line.split('#')
                    # strip out whitespace
                    num = comment[0].strip()
                    print(num)
                    
                    if num == "":
                        continue #skips blanks

                    try:
                        val = int(num, 2)
                        print('val', val)

                    except ValueError:
                        continue

                    self.ram[address] = val
                    address += 1

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

        elif op == 'CMP':
            #if equal, set E = 1
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001

            #set L = 1
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100

            #set G = 1
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010

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

    def ram_read(self, address):
        return self.ram[address]
        # self.pc += 2

    def ram_write(self, address, val): 
        self.ram[address] = val
        # self.pc += 3

    def handle_HLT(self):
        running = False
        self.pc = 0

    def handle_PRN(self):
        # prints num value in rgstr
        numVal = self.ram_read(self.ram[self.pc] + 1)
        print(self.reg[numVal])
        self.pc += 2

    def handle_LDI(self):
        # load immediate, store val in reg
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_CMP(self):
        #handled by alu
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc +2)
        self.alu('CMP', reg_a, reg_b)
        self.pc += 3

    def handle_JMP(self):
        # jump to address stored in given reg
        # set PC to this address
        address = self.ram_read(self.pc + 1)
        self.pc = reg[address]

    def handle_JEQ(self):
        #if flag == Equal, jump to address stored in given reg
        address = self.ram_read(self.pc + 1)
        if self.FL == 0b00000001:
            self.pc = self.reg[address]
        else:
            self.pc += 2

    def handle_JNE(self):
        # if flag is not Equal, jump to address in given reg
        address = self.ram_read(self.pc + 1)
        if self.FL != 0b00000001:
            self.pc = self.reg[address]
        else:
            self.pc += 2

    def run(self):
        # branchtable = O(1)
        # read address in pc, store result in IR (Instruction Register)
        running = True
        while running is True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1) #address = register[pc + 1]
            operand_b = self.ram_read(self.pc + 2)

            # fetch instruction val from RAM
            IR = self.ram_read(self.pc)

            # use val to look up, call func in branch table
            try:
                self.branchtable[IR]()

            except KeyError:
                print(f'Error! Unknown command: {IR}')
                sys.exit(1)

test = CPU()
test.load()
test.run()