import os
import math
import time

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

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.fov = 40
        self.viewer_distance = 4

    def render_mesh(self, mesh, angle_x, angle_y, angle_z):
        rotated_vertices = []
        rot_x = MathUtils.get_rotation_x(angle_x)
        rot_y = MathUtils.get_rotation_y(angle_y)
        rot_z = MathUtils.get_rotation_z(angle_z)
        
        for v in mesh.vertices:
            rotated = MathUtils.multiply_matrix_vector(rot_x, v)
            rotated = MathUtils.multiply_matrix_vector(rot_y, rotated)
            rotated = MathUtils.multiply_matrix_vector(rot_z, rotated)
            
            projected = MathUtils.project_3d_to_2d(
                rotated, self.fov, self.viewer_distance, 
                self.screen.width, self.screen.height
            )
            rotated_vertices.append(projected)
            
        for edge in mesh.edges:
            v1_idx, v2_idx = edge
            x0, y0 = rotated_vertices[v1_idx]
            x1, y1 = rotated_vertices[v2_idx]
            self.screen.draw_line(x0, y0, x1, y1, '#')

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    screen = Screen(width=80, height=40)
    cube = Cube()
    renderer = Renderer(screen)
    
    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0
    
    target_fps = 30
    frame_duration = 1.0 / target_fps
    
    try:
        while True:
            start_time = time.time()
            
            screen.clear_buffer()
            renderer.render_mesh(cube, angle_x, angle_y, angle_z)
            screen.draw()
            
            angle_x += 0.05
            angle_y += 0.03
            angle_z += 0.02
            
            elapsed = time.time() - start_time
            sleep_time = frame_duration - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
                
    except KeyboardInterrupt:
        clear_screen()
