from pyglet.gl import *
import random as rnd
 
class GameOfLife:
    def __init__(self, 
                grid_width, 
                grid_height, 
                cell_size, 
                initial_coverage):
        self.grid_width = int(grid_width / cell_size)
        self.grid_height = int(grid_height / cell_size)
        self.cell_size = cell_size
        self.initial_coverage = initial_coverage
        self.cells = []
        self.vertices = []
        self.generate_cells()

    def generate_cells(self):
        for x in range(0, self.grid_width):
            self.cells.append([])
            for y in range(0, self.grid_height):
                if(rnd.random() < self.initial_coverage):
                    self.cells[x].append(1)
                else:
                    self.cells[x].append(0)
     
    def run_rules(self):
        temp = [] 
        for x in range(0, self.grid_width):
            temp.append([])
            for y in range(0, self.grid_height):
                s = sum([self.get_cell_value(x - 1, y    ),  
                         self.get_cell_value(x - 1, y - 1), 
                         self.get_cell_value(x    , y - 1),  
                         self.get_cell_value(x + 1, y - 1),  
                         self.get_cell_value(x + 1, y    ),  
                         self.get_cell_value(x + 1, y + 1),  
                         self.get_cell_value(x    , y + 1),  
                         self.get_cell_value(x - 1, y + 1)])
               
                if(self.cells[x][y] == 0 and s == 3):
                    temp[x].append(1)
                elif(self.cells[x][y] == 1 and (s == 2 or s == 3)):
                    temp[x].append(1)
                else:
                    temp[x].append(0)
        self.cells = temp

    def get_cell_value(self, x, y):
        if(x >= 0 and x < self.grid_width and
           y >= 0 and y < self.grid_height):
            return self.cells[x][y]
        return 0
        

    def build_vertex_list(self):
        self.vertices = []
        for x in range(0, self.grid_width):
            for y in range(0, self.grid_height):
                if(self.cells[x][y] == 1):
                    self.vertices.extend(
                        [x * self.cell_size, 
                         y * self.cell_size, 
                         x * self.cell_size, 
                         y * self.cell_size + self.cell_size, 
                         x * self.cell_size + self.cell_size, 
                         y * self.cell_size + self.cell_size,
                         x * self.cell_size + self.cell_size,
                         y * self.cell_size])
                
    
    def draw(self):
        self.build_vertex_list()
        vlist = pyglet.graphics.vertex_list(len(self.vertices)//2, ('v2f', self.vertices))
        glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        glColor3f(1,0,0)
        vlist.draw(GL_QUADS)
 

