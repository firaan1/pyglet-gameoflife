import pyglet
from gol import GameOfLife

class Window(pyglet.window.Window):

    def __init__(self):
        super().__init__(1600, 800)
        self.gol = GameOfLife(window_height = self.get_size()[1], window_width = self.get_size()[0], cell_size = 10)
        self.pause = False
        self.fps = 12
        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)
    
    def on_draw(self):
        self.clear()
        # self.gol.draw()
        batch = self.gol.draw()
        batch.draw()
    
    def update(self, dt):
        if not self.pause:
            self.gol.next_cells()
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons and self.pause:
            self.gol.change_cell_value(x, y, buttons)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.pause:
            self.gol.change_cell_value(x, y, buttons)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.pause = False if self.pause else True
        if symbol == pyglet.window.key.N and self.pause:
            self.gol.next_cells()
        if symbol == pyglet.window.key.C:
            self.gol.clear_cells()
            self.pause = True
        if symbol == pyglet.window.key.R:
            self.gol.rnd_cells()
            self.pause = True
        
if __name__ == '__main__':
    window = Window()
    pyglet.app.run()