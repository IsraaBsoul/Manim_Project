target_shapes = []

animations_arr = []

from manim import *


class ShapeAnimation(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        shapes = []

        target_shape = Polygon([1.2163742690058479, -0.2723404255319149, 0], [4.187134502923977, -0.2723404255319149, 0], [2.7017543859649122, 1.6170212765957448, 0], color='#ff8080', fill_opacity=1)

        target_shape.set_fill(color='#ff8080', opacity=1)

        target_shape.set_stroke(color='BLACK')

        target_shapes.append(target_shape)

        shape = Ellipse(width=1.7455933789374862, height=4.402112628928978, color='WHITE')

        shape.set_fill(color='WHITE', opacity=1)

        shape.set_stroke(color='#004000')

        shape.move_to([2.7719298245614032, 0.7574468085106383, 0])

        shapes.append(shape)

        shape = Text('create circle ∞', font_size=12, color='#7d0d82')

        shape.move_to([-3.0409356725146197, 2.5531914893617023, 0])

        shapes.append(shape)

        shape = Text('transforming', font_size=12, color='#d70428')

        shape.move_to([-0.1871345029239766, 2.9617021276595743, 0])

        shapes.append(shape)

        shape = Rectangle(width=1.7543859649122806, height=3.5914893617021275, color='WHITE')

        shape.set_fill(color='WHITE', opacity=1)

        shape.set_stroke(color='#ff8000')

        shape.move_to([-5.111111111111111, 0.0425531914893617, 0])

        shapes.append(shape)

        self.wait(1)

        animations_arr.clear()

        animations_arr.append(Create(shapes[0], run_time=2))

        animations_arr.append(FadeIn(shapes[1], run_time=2))

        self.play(*animations_arr)

        self.wait(1)

        animations_arr.clear()

        animations_arr.append(Uncreate(shapes[0], run_time=2))

        animations_arr.append(FadeOut(shapes[1], run_time=2))

        self.play(*animations_arr)

        self.wait(2)

        animations_arr.clear()

        animations_arr.append(Create(shapes[2], run_time=2))

        self.play(*animations_arr)

        self.wait(2)

        animations_arr.clear()

        animations_arr.append(Transform(shapes[3],target_shapes[0], run_time=2))

        self.play(*animations_arr)

        self.wait(4)

        animations_arr.clear()

        animations_arr.append(Uncreate(shapes[2], run_time=2))

        self.play(*animations_arr)
