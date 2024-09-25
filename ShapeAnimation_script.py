target_shapes = []

animations_arr = []

animations_arr = []

animations_arr = []

from manim import *


class ShapeAnimation(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        shapes = []

        target_shape = Polygon([3.345029239766082, -0.9531914893617022, 0], [4.374269005847953, -0.9531914893617022, 0], [3.859649122807017, 1.6170212765957448, 0], color='#eb0214', fill_opacity=1)

        target_shape.set_fill(color='#eb0214', opacity=1)

        target_shape.set_stroke(color='BLACK')

        target_shapes.append(target_shape)

        shape = Ellipse(width=0.8291812124517752, height=3.3097446269329938, color='WHITE')

        shape.set_fill(color='WHITE', opacity=1)

        shape.set_stroke(color='#004000')

        shape.move_to([3.005847953216374, 0.0851063829787234, 0])

        shapes.append(shape)

        shape = Text('This is circle ∞', font_size=12, color='#3c0504')

        shape.move_to([-4.514619883040935, 2.570212765957447, 0])

        shapes.append(shape)

        shape = Text('Now we will transform', font_size=12, color='#ff0080')

        shape.move_to([-4.514619883040935, 2.570212765957447, 0])

        shapes.append(shape)

        shape = Rectangle(width=1.1695906432748537, height=1.8893617021276596, color='WHITE')

        shape.set_fill(color='WHITE', opacity=1)

        shape.set_stroke(color='#008080')

        shape.move_to([-3.3684210526315788, 0.4340425531914894, 0])

        shapes.append(shape)

        self.wait(1)

        animations_arr.append(Create(shapes[0], run_time=3))

        animations_arr.append(FadeIn(shapes[1], run_time=3))

        self.play(*animations_arr)

        self.wait(1)

        animations_arr.append(Uncreate(shapes[0], run_time=2))

        animations_arr.append(FadeOut(shapes[1], run_time=2))

        self.play(*animations_arr)

        self.wait(5)

        animations_arr.append(Create(shapes[2], run_time=3))

        animations_arr.append(Transform(shapes[3],target_shapes[0], run_time=3))

        self.play(*animations_arr)
