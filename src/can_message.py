

class CanMessage:
    def __init__(self, buffer, command):
        string = buffer.decode()
        if command == 'T':
            id = string[:8]
            dlc = string[8]
            msg = [[string[i:i+2] for i in range(9, len(string), 2)]]
        elif command == 't':
            id = string[:3]
            dlc = int(string[3])
            msg = [[string[i:i+2] for i in range(4, len(string), 2)]]
        self.dlc = dlc
        self.id = id
        self.msg = msg

    def print_msg(self):
        print(self.id+'\t' + self.dlc + '\t', end='')
        [print(byte, end=' ') for byte in self.msg]
        print()
