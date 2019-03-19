class Message:
    def __init__(self, command, data=None):
        self.command = command
        self.data = data

    def __repr__(self):
        return (f'command: {self.command}\n' +
                f'data: {self.data}')

if __name__ == '__main__':
    print(Message('test', [1, 2, 3]))
