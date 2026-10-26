import os
import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

class MathUtils:
    @staticmethod
    def multiply_matrix_vector(matrix, vec):
        x = matrix[0][0] * vec.x + matrix[0][1] * vec.y + matrix[0][2] * vec.z
        y = matrix[1][0] * vec.x + matrix[1][1] * vec.y + matrix[1][2] * vec.z
        z = matrix[2][0] * vec.x + matrix[2][1] * vec.y + matrix[2][2] * vec.z
        return Vector3(x, y, z)

    @staticmethod
    def get_rotation_x(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return [
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ]

    @staticmethod
    def get_rotation_y(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return [
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ]

    @staticmethod
    def get_rotation_z(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return [
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ]

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
