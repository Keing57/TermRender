import os

class Screen:
    def __init__(self, width=80, height=40):
        self.width = width
        self.height = height
        self.framebuffer = [[' ' for _ in range(width)] for _ in range(height)]

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    pass
