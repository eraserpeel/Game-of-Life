
import random as rnd
import numpy

class GameOfLife: 
    def __init__(self, grid_width, grid_height, percent_fill):
        self.grid_width =grid_width
        self.grid_height = grid_height
        self.percent_fill = percent_fill
        self.cells = []
        self.generate_cells()

    def generate_cells(self):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                if rnd.random() < self.percent_fill:
                    self.cells[row].append(1)
                else:
                    self.cells[row].append(0)


    def run_rules(self):
        temp = []
        for row in range(0, self.grid_height):
            temp.append([])
            for col in range(0, self.grid_width):
                cell_sum = sum([self.get_cell_value(row - 1, col),
                                self.get_cell_value(row - 1, col - 1),
                                self.get_cell_value(row,     col - 1),
                                self.get_cell_value(row + 1, col - 1),
                                self.get_cell_value(row + 1, col),
                                self.get_cell_value(row + 1, col + 1),
                                self.get_cell_value(row,     col + 1),
                                self.get_cell_value(row - 1, col + 1)])

                if self.cells[row][col] == 0 and cell_sum == 3: 
                    temp[row].append(1)
                elif self.cells[row][col] == 1 and (cell_sum == 3 or cell_sum == 2):
                    temp[row].append(1)
                else: 
                    temp[row].append(0)

        self.cells = temp

    def get_as_tuple(self):
        return tuple(tuple(elem) for elem in self.cells)

    def get_living_count(self):
        count = 0
        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                if self.cells[row][col] == 1:
                    count = count + 1
        return count



    def get_cell_value(self, row, col):
        if row >= 0 and row < self.grid_height and col >= 0 and col < self.grid_width:
           return self.cells[row][col]
        return 0


  


    # def __init__(self, grid_width, grid_height, percent_fill):
    #     self.grid_width = grid_width
    #     self.grid_height = grid_height
    #     self.percent_fill = percent_fill
    #     self.cells = numpy.zeros(shape=(self.grid_width, self.grid_height))
        
    #     # self.cells = numpy.array([[ 0. , 1. , 1. , 1. , 1.],
    #     #                   [ 0. , 1. , 1. , 1. , 1.],
    #     #                   [ 1. , 0. , 0. , 1. , 1.],
    #     #                   [ 1. , 0. , 1. , 1. , 1.],
    #     #                   [ 0. , 0. , 1. , 1. , 1.]])
    #     #self.generate_cells()
    #     self.generate_cells()

    # def generate_cells(self):
    #     for row in range(0, self.grid_height):
    #         for col in range(0, self.grid_width):
    #             if rnd.random() < self.percent_fill:
    #                 self.cells[row][col] = 1
    #             else:
    #                 self.cells[row][col] = 0

    # def run_rules(self):
    #     temp_cells = numpy.zeros(shape=(self.grid_width, self.grid_height))
    #     for row in range(0, self.grid_height):
    #         for col in range(0, self.grid_width):
    #             cell_sum = sum([self.get_cell_value(row - 1, col),
    #                             self.get_cell_value(row - 1, col - 1),
    #                             self.get_cell_value(row,     col - 1),
    #                             self.get_cell_value(row + 1, col - 1),
    #                             self.get_cell_value(row + 1, col),
    #                             self.get_cell_value(row + 1, col + 1),
    #                             self.get_cell_value(row,     col + 1),
    #                             self.get_cell_value(row - 1, col + 1)])
    #             if self.cells[row][col] == 0.0 and cell_sum == 3: 
    #                 temp_cells[row][col] = 1
    #             elif self.cells[row][col] == 1.0 and (cell_sum == 3 or cell_sum == 2):
    #                 temp_cells[row][col] = 1

    #     self.cells = temp_cells


    # def get_cell_value(self, row, col):
    #     if row >= 0 and row < self.grid_height and col >= 0 and col < self.grid_width:
    #        return self.cells[row][col]
    #     return 0

    # def get_as_string(self):
    #     return self.cells.tostring()
