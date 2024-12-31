from kivy.uix.button import Button
from kivy.graphics import Rotate, Color, Rectangle

class CharlesButton(Button):
    def __init__(self, **kwargs):
        super(CharlesButton, self).__init__(**kwargs)
        self.angle = 2
        self.background_angle = 0
        self.bind(size=self.update_canvas, pos=self.update_canvas)  # Ensure canvas updates when size/position changes

    def rotate_button(self, *args):
        self.background_angle += self.angle
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()  # Clear the previous drawing
        with self.canvas.before:
            # Set the color for the button (white in this case)
            Color(1, 1, 1, 1)
            # Apply the rotation to the button based on the center of the button
            Rotate(angle=self.background_angle, origin=self.center)
            # Redraw the background (the button's rectangle)
            Rectangle(pos=self.pos, size=self.size)
