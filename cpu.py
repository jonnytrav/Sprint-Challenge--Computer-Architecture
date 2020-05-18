"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 7
        self.pc = 0
        self.MAR = None
        self.MDR = None
        self.FL = 0

    def load(self, load_file):
        """Load a program into memory."""

        address = 0

        # sys.argv is a list of all args
        load_file = load_file
        print("load_file => ", load_file)

        with open(load_file) as f:
            for line in f:
                # add to memory
                i = line.split("#")
                num = i[0].strip()
                if num == "":
                    continue

                self.ram[address] = int(num, 2)
                print("current address => ", address)
                print("value in the RAM => ", self.ram[address])

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.reg[self.sp] = 0xf4
        running = True
        while running == True:
            command = self.ram[self.pc]
            # print(command)
            reg1 = self.ram[self.pc + 1]
            reg2 = self.ram[self.pc + 2]
            # LDI - load and store in register
            if command == 0b10000010:
                self.reg[reg1] = reg2
                self.pc += 3
            # PRN
            elif command == 0b01000111:
                print(self.reg[reg1])
                self.pc += 2
            # MULTIPLY
            elif command == 0b10100010:
                # reg1 = self.ram[self.pc + 1]
                # reg2 = self.ram[self.pc + 2]
                self.reg[reg1] = self.reg[reg1] * self.reg[reg2]
                self.pc += 3
            # HALT
            elif command == 0b00000001:
                running = False
            # PUSH - takes in register as operand
            elif command == 0b01000101:
                self.reg[self.sp] -= 1
                reg1 = self.ram[self.pc + 1]
                val = self.reg[reg1]
                self.ram[self.reg[self.sp]] = val

                self.pc += 2
            # POP
            elif command == 0b01000110:
                sp_value = self.ram[self.reg[self.sp]]
                self.reg[reg1] = sp_value

                self.reg[self.sp] += 1
                self.pc += 2
            # CALL
            elif command == 0b01010000:
                ret_address = self.pc + 2
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = ret_address

                sub_address = self.reg[reg1]
                self.pc = sub_address
                # print("In the CALL block")
                # print("PC =>", self.pc)
                # print("SP =>", self.reg[self.sp])
            # RET
            elif command == 0b00010001:
                return_address = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

                self.pc = return_address
                # print("In the RET block")
            # ADD
            elif command == 0b10100000:
                self.alu("ADD", reg1, reg2)
                self.pc += 3
                # print("In the add block!")
                # print("Result of adding =>", self.reg[0])
            # CMP
            elif command == 0b10100111:
                val1 = self.reg[reg1]
                val2 = self.reg[reg2]

                if val1 == val2:
                    self.FL = 0b00000001
                elif val1 > val2:
                    self.FL = 0b00000010
                elif val1 < val2:
                    self.FL = 0b00000100

                self.pc += 3
            # JMP
            elif command == 0b01010100:
                self.pc = self.reg[reg1]
            # JEQ
            elif command == 0b01010101:
                if self.FL == 0b00000001:
                    self.pc = self.reg[reg1]
                else:
                    self.pc += 2
            # JNE
            elif command == 0b01010110:
                if self.FL != 0b00000001:
                    self.pc = self.reg[reg1]
                else:
                    self.pc += 2

            # IF NOT RECOGNIZED
            else:
                sys.exit(1)
