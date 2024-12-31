from kivy.uix.button import Button
from kivy.graphics import Rotate, Color, Rectangle

class CharlesButton(Button):
    def __init__(self, **kwargs):
        super(CharlesButton, self).__init__(**kwargs)
        self.angle = 2
        self.background_angle = 0
        
    def rotate_button(self,*args):
        self.background_angle += self.angle
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1,1,1,1)
            Rotate(angle=self.background_angle, origin=self.center)
            Rectangle(pos=self.pos, size=self.size)
