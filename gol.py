import random
import pyglet

class GameOfLife:

    def __init__(self, window_height = 60, window_width = 60, cell_size = 20):
        self.cell_size = cell_size
        self.grid_height = int(window_height / self.cell_size)
        self.grid_width = int(window_width / self.cell_size)
        self.grid_length = self.grid_height * self.grid_width
        self.cells = []
        self.cells = self.rnd_cells()
    
    def rnd_cells(self):
        for cell_index in range(self.grid_length):
            if random.random() < 0.25:
                self.cells.append(1)
            else:
                self.cells.append(0)
        return self.cells
    
    def clear_cells(self):
        self.cells = [0 for cell_index in range(self.grid_length)]

    def get_nearby_indices(self, cell_index):
        # consider 1 base instead of 0
        cell_index += 1
        
        # check boundaries
        if cell_index < 1 or cell_index > self.grid_length:
            return False
        
        # filling nearby indices (column)
        tmp_indices1 = [cell_index]
        if cell_index % self.grid_height == 1:
            tmp_indices1.append(cell_index + 1)
        elif cell_index % self.grid_height == 0:
            tmp_indices1.append(cell_index - 1)
        else:
            tmp_indices1.append(cell_index - 1)
            tmp_indices1.append(cell_index + 1)

        # filling nearby indices (row)
        tmp_indices2 = [-self.grid_height, 0, self.grid_height]

        tmp_indices3 = [i1 + i2 for i1 in tmp_indices1 for i2 in tmp_indices2]

        nearby_indices = []
        for i3 in tmp_indices3:
            if i3 > 0 and i3 <= self.grid_length and i3 != cell_index:
                nearby_indices.append(i3 - 1) # converting to 0 base
        return nearby_indices

    def get_cell_value(self, cell_index, nearby_indices):
        current_cell_value = self.cells[cell_index]
        nearby_values = sum([self.cells[i] for i in nearby_indices])
        if current_cell_value == 1:
            if nearby_values in [2,3]:
                return 1
        else:
            if nearby_values == 3:
                return 1
        return 0

    def next_cells(self):
        new_cells = []
        for cell_index in range(self.grid_length):
            nearby_indices = self.get_nearby_indices(cell_index)
            new_cells.append(self.get_cell_value(cell_index, nearby_indices))
        self.cells = new_cells

    def draw(self):
        col = -1
        batch = pyglet.graphics.Batch()
        for cell_index in range(self.grid_length):
            row = cell_index % self.grid_height
            if row == 0:
                col += 1
            # row += 1 # converting to 1 base
            if self.cells[cell_index] == 1:
                # top down and left to right, due to get_nearby_indices function
                cell_coords = (
                    col * self.cell_size, 
                    (self.grid_height * self.cell_size) - (row * self.cell_size) - self.cell_size,

                    col * self.cell_size,
                    (self.grid_height * self.cell_size) - (row * self.cell_size),

                    (col * self.cell_size) + self.cell_size,
                    (self.grid_height * self.cell_size) - (row * self.cell_size) - self.cell_size,
                    
                    (col * self.cell_size) + self.cell_size,
                    (self.grid_height * self.cell_size) - (row * self.cell_size)
                )
                cell_colors = (255, 255, 0) * int(len(cell_coords)/2)
                # pyglet.graphics.draw_indexed(4,
                #     pyglet.gl.GL_TRIANGLES, [0, 1, 2, 1, 2, 3], ('v2i', cell_coords), ('c3B', cell_colors))
                batch.add_indexed(4,
                    pyglet.gl.GL_TRIANGLES, None, [0, 1, 2, 1, 2, 3], ('v2i', cell_coords), ('c3B', cell_colors))
        return batch

    def get_coord_index(self, x, y):
        row = int(x / self.cell_size) # 1 based
        col = self.grid_height - (int(y / self.cell_size)) - 1 # 0 based
        cell_index = (row * self.grid_height) + col
        return cell_index
        
    def change_cell_value(self, x, y, buttons):
        cell_index = self.get_coord_index(x, y)
        if buttons == 1:
            self.cells[cell_index] = 1
        elif buttons == 4:
            self.cells[cell_index] = 0