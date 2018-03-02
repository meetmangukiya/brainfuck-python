import argparse
import io
import sys

class Stack:
    def __init__(self):
        self._stack = []

    def push(self, element):
        self._stack.insert(0, element)

    def pop(self):
        return self._stack.pop()

    def is_empty(self):
        return len(self._stack) == 0

class Brainfuck:
    KEYWORDS = [
        '>',
        '<',
        '+',
        '-',
        '.',
        ',',
        '[',
        ']',
    ]

    def __init__(self, fstream, istream=None):
        self._cells = [0]
        self._current_cell = 0
        self._fstream = fstream
        self._istream = istream

    def _convert_block(self, block):
        """
        Converts a list of tokens forming a block to a list of executable
        tokens.

        A list of tokens is an *executable block of instructions*.

        '[--[++]]' ==> ['-', '-', ['+', '+']]
        """
        block = list(block)

        # remove the braces
        if len(block) == 0:
            return

        block.pop()
        del block[0]

        while '[' in block:
            stack = Stack()

            end = start = block.index('[')
            stack.push('[')
            while not stack.is_empty():
                end += 1
                if block[end] == '[':
                    stack.push('[')
                elif block[end] == ']':
                    stack.pop()
            end += 1
            block[start:end] = [self._convert_block(block[start:end])]

        return block

    def run(self):
        """
        Execute the program. Instructions are read from
        ``self._fstream`` and input is taken from ``self._istream``.
        """
        while not self._eostream():
            curr = self._fstream.read(1)

            if curr == '[':
                instructions = ['[']
                stack = Stack()
                stack.push('[')
                while not stack.is_empty():
                    char = self._fstream.read(1)
                    instructions.append(char)
                    if char == ']':
                        stack.pop()
                    elif char == '[':
                        stack.push('[')
                instructions = self._convert_block(instructions)
                curr = instructions

            self._take_action(curr)

    def _eostream(self):
        """
        Returns if the stream ended, i.e. if all instructions were read and
        executed.
        """
        if self._fstream.read(1) != '':
            self._fstream.seek(self._fstream.tell() - 1)
            return False
        else:
            return True

    def _take_action(self, char):
        if char in self.KEYWORDS:
            if char == '>':
                self._move_right()
            elif char == '<':
                self._move_left()
            elif char == '+':
                self._increment()
            elif char == '-':
                self._decrement()
            elif char == '.':
                self._print()
            elif char == ',':
                char = input('-> ')[0]
                self._write(char)
        elif isinstance(char, list):
            self._execute_block(char)
        else:
            pass

    def _move_right(self):
        """
        Move the current cell pointer to right.
        """
        self._current_cell += 1
        if self._current_cell == len(self._cells):
            self._cells.append(0)

    def _move_left(self):
        """
        Move the current cell pointer to left.
        """
        self._current_cell -= 1
        assert self._current_cell >= 0, "Segmentation Fault"

    def _increment(self):
        """
        Increment the current cell value by 1. If it is 255, then on increment
        it becomes 0.
        """
        if self._cells[self._current_cell] == 255:
            self._cells[self._current_cell] = -1
        self._cells[self._current_cell] += 1

    def _decrement(self):
        """
        Decrement the current cell value by 1. If it is 0, then on decrement it
        becomes 255.
        """
        if self._cells[self._current_cell] == 0:
            self._cells[self._current_cell] = 256
        self._cells[self._current_cell] -= 1

    def _print(self):
        """
        Print the ascii character of the current cell value.
        """
        print(self._read(), end='')

    def _read(self):
        """
        Read current cell value and return the ascii character corresponding to
        it.
        """
        return chr(self._cells[self._current_cell])

    def _write(self, char):
        """
        Write the ascii value of the ``char`` to the current cell.
        """
        self._cells[self._current_cell] = ord(char)

    def _execute_block(self, block):
        """
        Execute the block of instructions. A block of instructions is a
        ``list``.
        """
        execute = True
        while execute:
            for instruction in block:
                self._take_action(instruction)
            execute = self._cells[self._current_cell] != 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', action='store',
                        help='brainfuck file to execute')
    args = parser.parse_args()
    if args.file:
        print('executing file', args.file)
        stream = open(args.file)
        Brainfuck(stream).run()
    else:
        print("Didn't run anything. Use --file option. Use --help for more "
              "information")
