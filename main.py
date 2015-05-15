import pyglet
#from pyglet.gl import *
from game_of_life import GameOfLife


class Window(pyglet.window.Window):

    def __init__(self):
        super(Window, self).__init__(600, 600)
        self.game_of_life = GameOfLife(600, 600, 10, 0.2)
        pyglet.clock.schedule_interval(self.update, 1.0 / 24.0)   

    def on_draw(self):
        self.clear()
        self.game_of_life.draw()
        self.game_of_life.run_rules()

    
    def update(self, dt):
        pass

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()



