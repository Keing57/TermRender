import os
import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

class Mesh:
    def __init__(self, vertices=None, edges=None):
        self.vertices = vertices if vertices is not None else []
        self.edges = edges if edges is not None else []

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

    @staticmethod
    def project_3d_to_2d(vector, fov, viewer_distance, screen_width, screen_height):
        z_dist = vector.z + viewer_distance
        if z_dist == 0:
            z_dist = 0.0001
            
        x = int((vector.x * fov) / z_dist + screen_width / 2)
        y = int((vector.y * fov) / z_dist + screen_height / 2)
        return (x, y)

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

    def draw_line(self, x0, y0, x1, y1, char):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.set_pixel(x0, y0, char)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    pass
