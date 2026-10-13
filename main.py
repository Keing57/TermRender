import os

class Screen:
    def __init__(self, width=80, height=40):
        self.width = width
        self.height = height
        self.framebuffer = [[' ' for _ in range(width)] for _ in range(height)]

    def draw(self):
        clear_screen()
        frame = '\n'.join([''.join(row) for row in self.framebuffer])
        print(frame, end='')
        
    def set_pixel(self, x, y, char):
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.framebuffer[y][x] = char

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    pass
