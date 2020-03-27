"""CPU functionality."""

import sys



class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8 
        self.pc = 0 # Program Counter
        self.SP = 0xF4 # Stack Pointer, register[SP]
        self.FL = 0 #? flag
        
        self.branchtable = {
            #funcs indexed by opcode val
            HLT = 0b00000001
            LDI = 0b10000010
            PRN = 0b01000111
            MUL = 0b10100010 
            PUSH = 0b01000101
            POP = 0b01000110
            CALL = 0b01010000
            RET  = 0b00010001
            ADD  = 0b10100000
            CMP = 0b10100111
            JMP = 0b01010100
            JEQ = 0b01010101
            JNE = 0b01010110
        }
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

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
        # if/elif = O(n) || branchtable = O(1)
        # read address in pc, store result in IR (Instruction Register)
        running = True
        while running is True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1) #address = register[pc + 1]
            operand_b = self.ram_read(self.pc + 2)

            # fetch instruction val from RAM
            # use val to look up, call func in branch table
            IR = OP1
            self.branchtable[IR](operand_a)

            IR = OP2
            self.branchtable[IR](operand_b)
                # pop val from stack and store in PC
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3

            else:
                running = False
                print(f'Unknown command: {command}')
                sys.exit(1)


    def handle_HLT(self):
        running = False
        # self.pc += 1

    def handle_PRN(self):
        # prints num value in rgstr
        print(self.reg[operand_a])
        self.pc += 2

    def handle_LDI(self):
        # load immediate, store val in reg
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_MUL(self):
        # self.alu(MUL, operand_a, operand_b)
        self.reg[operand_a] *= self.reg[operand_b]
        self.pc += 3

    def handle_PUSH(self):
        # Copy val from address to given reg
        # decrement SP
        self.SP -= 1
        self.ram[self.SP] = self.reg[operand_a]
        self.pc += 2

    def handle_POP(self):
        # copy val from address
        # increment SP
        self.reg[operand_a] = self.ram[self.SP]
        self.SP += 1
        self.pc += 2

    def handle_CALL(self):
        # decrement SP
        self.SP -= 1
        self.ram[self.SP] = self.pc + 2
        # store the instruction
        self.pc = self.reg[operand_a]

    def handle_RET(self):
        # pop val from stack and return 
        self.pc = self.ram[self.SP]
        self.SP += 1

    def handle_ADD(self):
        # pop val from stack and store in PC
        self.reg[operand_a] += self.reg[operand_b]
        self.pc += 3

    def handle_CMP(self, op, reg_a, reg_b):
        #handled by alu
        reg_a = self.reg[operand_a]
        reg_b = self.reg[operand_b]

        if reg_a == reg_b:
            # set flag to equal
            self.FL = 'E'
            self.E = 1
            self.L = 0
            self.G = 0
        if reg_a < reg_b:
            # set flag to L
            self.FL = 'L'
            self.E = 0
            self.L = 1
            self.G = 0
        if reg_a > reg_b:
            # set flag to G
            self.FL = 'G'
            self.E = 0
            self.L = 0
            self.G = 1

    def handle_JMP(self):
        # jump to address stored in given reg
        # set PC to this address
        self.pc = register[self.SP]

    def handle_JEQ(self):
        #if flag = Equal, jump to address stored in given reg
        if self.E == 1:
            self.JMP()
        else:
            continue

    def handle_JNE(self):
        # if flag is not Equal, jump to address in given reg
        if self.E = 0:
            self.JMP()
        else:
            continue

        # pop val from stack and store in PC
        self.reg[operand_a] += self.reg[operand_b]
        self.pc += 3