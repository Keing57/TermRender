import os
import math
import time

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

class Mesh:
    def __init__(self, vertices=None, edges=None):
        self.vertices = vertices if vertices is not None else []
        self.edges = edges if edges is not None else []
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0
        self.rotation_speed_x = 0.05
        self.rotation_speed_y = 0.03
        self.rotation_speed_z = 0.02
        self.position = Vector3(0, 0, 0)
        self.color = Colors.WHITE
        
    def update(self):
        self.angle_x += self.rotation_speed_x
        self.angle_y += self.rotation_speed_y
        self.angle_z += self.rotation_speed_z

class Cube(Mesh):
    def __init__(self):
        super().__init__()
        self.vertices = [
            Vector3(-1, -1, -1),
            Vector3( 1, -1, -1),
            Vector3( 1,  1, -1),
            Vector3(-1,  1, -1),
            Vector3(-1, -1,  1),
            Vector3( 1, -1,  1),
            Vector3( 1,  1,  1),
            Vector3(-1,  1,  1)
        ]
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

class Pyramid(Mesh):
    def __init__(self):
        super().__init__()
        self.vertices = [
            Vector3( 0, -1,  0),
            Vector3(-1,  1, -1),
            Vector3( 1,  1, -1),
            Vector3( 1,  1,  1),
            Vector3(-1,  1,  1)
        ]
        self.edges = [
            (1, 2), (2, 3), (3, 4), (4, 1),
            (0, 1), (0, 2), (0, 3), (0, 4)
        ]

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

    def clear_buffer(self):
        self.framebuffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def draw(self):
        clear_screen()
        frame = '\n'.join([''.join(row) for row in self.framebuffer])
        print(frame, end='')
        
    def set_pixel(self, x, y, char):
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.framebuffer[y][x] = char

    def draw_line(self, x0, y0, x1, y1, char, color=''):
        colored_char = f"{color}{char}{Colors.RESET}" if color else char
        
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.set_pixel(x0, y0, colored_char)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.fov = 40
        self.viewer_distance = 5

    def render_mesh(self, mesh):
        rotated_vertices = []
        rot_x = MathUtils.get_rotation_x(mesh.angle_x)
        rot_y = MathUtils.get_rotation_y(mesh.angle_y)
        rot_z = MathUtils.get_rotation_z(mesh.angle_z)
        
        for v in mesh.vertices:
            rotated = MathUtils.multiply_matrix_vector(rot_x, v)
            rotated = MathUtils.multiply_matrix_vector(rot_y, rotated)
            rotated = MathUtils.multiply_matrix_vector(rot_z, rotated)
            
            translated = rotated + mesh.position
            
            projected = MathUtils.project_3d_to_2d(
                translated, self.fov, self.viewer_distance, 
                self.screen.width, self.screen.height
            )
            rotated_vertices.append(projected)
            
        for edge in mesh.edges:
            v1_idx, v2_idx = edge
            x0, y0 = rotated_vertices[v1_idx]
            x1, y1 = rotated_vertices[v2_idx]
            self.screen.draw_line(x0, y0, x1, y1, '#', color=mesh.color)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    if os.name == 'nt':
        os.system('')
        
    screen = Screen(width=80, height=40)
    
    cube = Cube()
    cube.color = Colors.CYAN
    cube.position = Vector3(-1.5, 0, 0)
    
    pyramid = Pyramid()
    pyramid.color = Colors.GREEN
    pyramid.position = Vector3(1.5, 0, 0)
    
    meshes = [cube, pyramid]
    renderer = Renderer(screen)
    
    target_fps = 30
    frame_duration = 1.0 / target_fps
    
    try:
        while True:
            start_time = time.time()
            
            screen.clear_buffer()
            for m in meshes:
                m.update()
                renderer.render_mesh(m)
                
            screen.draw()
            
            elapsed = time.time() - start_time
            sleep_time = frame_duration - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
                
    except KeyboardInterrupt:
        clear_screen()
