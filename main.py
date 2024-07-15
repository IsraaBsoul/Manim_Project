
import tkinter as tk
from tkinter import colorchooser, Toplevel, messagebox, ttk
# import webcolors

# from PIL import Image, ImageTk
# import os


# Global variables
selected_shape = None
drawing = False
shape_id = None
start_x = None
start_y = None
shape_color = 'black'
shape_width = None
shape_height = None
shape_fill = 'white'
current_shape = None
edit_mode = False
current_page = 1
# Declare global variables for UI elements
shape_window = None
width_scale = None
height_scale = None
# Global variable for animation selection
selected_animation = None
selected_type = None
speed_value = None
start_time_value = None
from manim import *


# Stacks to manage undo and redo actions
undo_stack = []
redo_stack = []

all_of_drawings = []
sorted_drawings = []


# def get_color_name(hex_color):
#     try:
#         # Try to get the exact color name
#         color_name = webcolors.hex_to_name(hex_color)
#     except ValueError:
#         # If exact color name is not found, get the closest color name
#         color_name = closest_color_name(hex_color)
#     return color_name


# def closest_color_name(hex_color):
#     # Convert hex to RGB
#     # rgb_color = webcolors.hex_to_rgb(hex_color)
#
#     # Find the closest color name
#     min_colors = {}
#     for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
#         r_c, g_c, b_c = webcolors.hex_to_rgb(key)
#         rd = (r_c - rgb_color.red) ** 2
#         gd = (g_c - rgb_color.green) ** 2
#         bd = (b_c - rgb_color.blue) ** 2
#         min_colors[(rd + gd + bd)] = name
#     return min_colors[min(min_colors.keys())]

def update_object_menu():
    object_menu.delete(0, tk.END)  # Clear previous options
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            shape_name = f"{shape['type'].capitalize()} ({shape['id']})"
            object_menu.add_command(label=shape_name, command=lambda s=shape: select_object(s))

def show_add_button():
    global sorted_drawings
    # print(all_of_drawings[0].get('type'))
    # Filter out drawings that have animations and ensure 'details' key exists
    drawings_with_animations = [d for d in all_of_drawings if d.get('animation')]

    sorted_drawings = sorted(drawings_with_animations, key=lambda x: int(x['start_time']))

    print(sorted_drawings)

    window = tk.Tk()
    window.title("Sorted Drawings with Animations")

    # Create a treeview widget to display the data
    tree = ttk.Treeview(window, columns=('Shape', 'Animation', 'Type', 'Start Time'), show='headings')

    # Define the columns
    tree.heading('Shape', text='Shape')
    tree.heading('Animation', text='Animation')
    tree.heading('Type', text='Type')
    tree.heading('Start Time', text='Start Time')

    # Insert data into the treeview
    for draws in sorted_drawings:
        tree.insert('', tk.END,
                    values=(draws['type'], draws['animation'], draws['typeAnimation'], draws['start_time']))

    # Pack the treeview widget
    tree.pack(expand=True, fill='both')



def open_settings_window(shape):
    global speed_value, start_time_value  # Declare them as global to store the values

    # Create a new window
    settings_window = tk.Toplevel()
    settings_window.title("Object Settings")

    # Speed label and entry
    speed_label = tk.Label(settings_window, text="Speed:")
    speed_label.pack(padx=10, pady=5, anchor=tk.W)

    speed_entry = tk.Entry(settings_window)
    speed_entry.pack(padx=10, pady=5)

    # Start Time label and entry
    start_time_label = tk.Label(settings_window, text="Start Time:")
    start_time_label.pack(padx=10, pady=5, anchor=tk.W)

    start_time_entry = tk.Entry(settings_window)
    start_time_entry.pack(padx=10, pady=5)


    def close_window():
        global speed_value, start_time_value
        # Retrieve the entered values
        speed_value = float(speed_entry.get())
        start_time_value = float(start_time_entry.get())
        update_all_of_drawings(shape['id'], speed=speed_value)
        update_all_of_drawings(shape['id'], start_time=start_time_value)
        settings_window.destroy()

    # Button to close the window
    close_button = tk.Button(settings_window, text="Close", command=close_window)
    close_button.pack(pady=10)




def select_object(shape):
    global selected_shape
    selected_shape = shape
    print("**************************")
    print("in select_object:")
    print("the selected animation:")
    print(selected_animation)
    print("in select_object:")
    print("the selected type:")
    print(selected_type)
    print("**************************")

    object_button.config(text=f"Object: {shape['type'].capitalize()} ({shape['id']})")
    update_all_of_drawings(shape['id'], animation=selected_animation, typeAnimation=selected_type)

    print(all_of_drawings)

    # Enable Entry widgets for object properties
    # width_entry.config(state=tk.NORMAL)
    # height_entry.config(state=tk.NORMAL)
    # border_color_entry.config(state=tk.NORMAL)
    # fill_color_entry.config(state=tk.NORMAL)
    # x_coord_entry.config(state=tk.NORMAL)
    # y_coord_entry.config(state=tk.NORMAL)

    # Clear any existing text
    # width_entry.delete(0, tk.END)
    # height_entry.delete(0, tk.END)
    # border_color_entry.delete(0, tk.END)
    # fill_color_entry.delete(0, tk.END)
    # x_coord_entry.delete(0, tk.END)
    # y_coord_entry.delete(0, tk.END)

    # Insert the shape properties into the entry fields
    # width_entry.insert(0, shape.get('width', ''))
    # height_entry.insert(0, '5')  # You may need to calculate height if it's relevant
    # border_color_entry.insert(0, shape.get('color', ''))
    # fill_color_entry.insert(0, shape.get('fill', ''))
    # x_coord_entry.insert(0, shape.get('coords', [])[0])  # x-coordinate
    # y_coord_entry.insert(0, shape.get('coords', [])[1])  # y-coordinate
    # Enable other related functionalities if necessary
    open_settings_window(shape)


def select_shape(shape):
    global selected_shape, shape_window
    selected_shape = shape
    if shape_window:
        shape_window.destroy()  # Close the shape selection window


def open_shape_window():
    global shape_window
    shape_window = Toplevel(root)
    shape_window.title("Shapes")

    circle_button = tk.Button(shape_window, text="Circle", command=lambda: select_shape("circle"))
    circle_button.pack(side=tk.TOP, padx=5, pady=5)

    square_button = tk.Button(shape_window, text="Square", command=lambda: select_shape("square"))
    square_button.pack(side=tk.TOP, padx=5, pady=5)

    triangle_button = tk.Button(shape_window, text="Triangle", command=lambda: select_shape("triangle"))
    triangle_button.pack(side=tk.TOP, padx=5, pady=5)

    line_button = tk.Button(shape_window, text="Line", command=lambda: select_shape("line"))
    line_button.pack(side=tk.TOP, padx=5, pady=5)

    curve_button = tk.Button(shape_window, text="Curve", command=lambda: select_shape("curve"))
    curve_button.pack(side=tk.TOP, padx=5, pady=5)


def start_draw(event):
    global drawing, start_x, start_y, shape_id
    drawing = True
    start_x = event.x
    start_y = event.y

def draw_shape(event):
    global drawing, shape_id, start_x, start_y, shape_color, shape_width, object_text

    if drawing and selected_shape:
        if shape_id:
            canvas.delete(shape_id)
        if selected_shape == "circle":
            radius = ((event.x - start_x)**2 + (event.y - start_y)**2)**0.5
            shape_id = canvas.create_oval(start_x-radius, start_y-radius, start_x+radius, start_y+radius, outline=shape_color, fill=shape_fill, width=shape_width)
        elif selected_shape == "square":
            shape_id = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=shape_color, fill=shape_fill, width=shape_width)
        elif selected_shape == "triangle":
            x1, y1 = start_x, start_y
            x2, y2 = event.x, start_y
            x3, y3 = (start_x + event.x) / 2, event.y
            shape_id = canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=shape_color, fill=shape_fill, width=shape_width)
        elif selected_shape == "line":
            shape_id = canvas.create_line(start_x, start_y, event.x, event.y, fill=shape_color, width=shape_width)
        elif selected_shape == "curve":
            control_x = (start_x + event.x) / 2
            control_y = (start_y + event.y) / 2 - 50
            shape_id = canvas.create_line(start_x, start_y, control_x, control_y, event.x, event.y, smooth=True, fill=shape_color, width=shape_width)

        # Set object_text to indicate the selected shape
        # object_text.set(f"You chose {selected_shape.capitalize()}")
def save_shape_properties():
    global all_of_drawings, current_page
    if shape_id:
        shape_properties = {
            'id': shape_id,
            'type': selected_shape,
            'color': shape_color,
            'fill': shape_fill,
            'width': shape_width,
            'height': shape_height,
            'coords': canvas.coords(shape_id),  # Save the coordinates
            'page': current_page,  # Assign current page number
            'animation': selected_animation,  # Save the animation
            'typeAnimation': selected_type,
            'speed': speed_value,  # Save the speed
            'start_time': start_time_value  # Save the start time
        }
        all_of_drawings.append(shape_properties)




def end_draw(event):
    global drawing, shape_id, object_text
    drawing = False
    if shape_id:
        canvas.tag_bind(shape_id, '<ButtonPress-1>', on_shape_click)
        if edit_mode:
            canvas.tag_bind(shape_id, '<B1-Motion>', resize_shape)
        else:
            canvas.tag_bind(shape_id, '<B1-Motion>', drag_shape)
        undo_stack.append(shape_id)
        save_shape_properties()

    shape_id = None
    redo_stack.clear()

    # Update object_text to default message
    update_object_menu()  # Refresh object menu after drawing a shape


def on_shape_click(event):
    global current_shape, start_x, start_y
    current_shape = canvas.find_closest(event.x, event.y)[0]
    start_x = event.x
    start_y = event.y

    # Update the object_button text and color based on the clicked shape
    for shape in all_of_drawings:
        if shape['id'] == current_shape:
            object_button.config(text=f"You chose {shape['type'].capitalize()}", fg=shape['color'])
            break




def resize_shape(event):
    global start_x, start_y
    if current_shape:
        dx = event.x - start_x
        dy = event.y - start_y
        coords = canvas.coords(current_shape)
        if len(coords) == 4:  # Rectangle or oval
            x1, y1, x2, y2 = coords
            canvas.coords(current_shape, x1, y1, x2 + dx, y2 + dy)
            update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))
        elif len(coords) == 6:  # Triangle
            x1, y1, x2, y2, x3, y3 = coords
            canvas.coords(current_shape, x1, y1, x2 + dx, y2, (x1 + x2 + dx) / 2, y3 + dy)
            update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))
        elif len(coords) == 2:  # Line
            x1, y1 = coords
            x2, y2 = canvas.coords(current_shape)[2], canvas.coords(current_shape)[3]
            canvas.coords(current_shape, x1, y1, x2 + dx, y2 + dy)
            update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))
        start_x = event.x
        start_y = event.y

def drag_shape(event):
    global start_x, start_y
    if current_shape:
        dx = event.x - start_x
        dy = event.y - start_y
        canvas.move(current_shape, dx, dy)
        update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))
        start_x = event.x
        start_y = event.y

def change_color():
    global shape_color
    color = colorchooser.askcolor()[1]
    if color:
        shape_color = color

        if current_shape:
            canvas.itemconfig(current_shape, outline=shape_color)
            update_all_of_drawings(current_shape, color=shape_color)

def change_fill_color():
    global shape_fill
    color = colorchooser.askcolor()[1]
    if color:
        shape_fill = color

        if current_shape:
            canvas.itemconfig(current_shape, fill=shape_fill)
            update_all_of_drawings(current_shape, fill=shape_fill)

def undo():
    if undo_stack:
        shape_id = undo_stack.pop()
        canvas.itemconfigure(shape_id, state='hidden')
        redo_stack.append(shape_id)

def redo():
    if redo_stack:
        shape_id = redo_stack.pop()
        canvas.itemconfigure(shape_id, state='normal')
        undo_stack.append(shape_id)


def change_width(value):
    global shape_width
    shape_width = int(value)
    if current_shape:
        canvas.itemconfig(current_shape, width=shape_width)
        update_all_of_drawings(current_shape, width=shape_width)

def change_height(value):
    if current_shape:
        canvas_height = canvas.winfo_height()
        new_height = canvas_height * (int(value) / 100)
        coords = canvas.coords(current_shape)

        if len(coords) == 4:  # Rectangle or oval
            x1, y1, x2, y2 = coords
            canvas.coords(current_shape, x1, y1, x2, y1 + new_height)
            update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))
        elif len(coords) == 6:  # Triangle
            x1, y1, x2, y2, x3, y3 = coords
            y3 = y1 + new_height
            canvas.coords(current_shape, x1, y1, x2, y2, (x1 + x2) / 2, y3)
            update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))


def rotate_shape(value):
    if current_shape:
        angle = int(value)
        coords = canvas.coords(current_shape)
        if len(coords) == 4:  # Rectangle or oval
            x1, y1, x2, y2 = coords
            canvas.coords(current_shape, x1, y1, x2, y2)
            # Rotation logic for rectangle or oval (needs additional implementation)
        elif len(coords) == 6:  # Triangle
            x1, y1, x2, y2, x3, y3 = coords
            # Rotation logic for triangle (needs additional implementation)


def update_all_of_drawings(shape_id, **kwargs):
    global all_of_drawings
    for shape in all_of_drawings:
        if shape['id'] == shape_id:
            for key, value in kwargs.items():
                shape[key] = value
            shape['coords'] = canvas.coords(shape_id)  # Update coordinates
            shape['page'] = current_page  # Ensure correct page assignment



def next_page():
    global current_page
    if current_page < max(shape['page'] for shape in all_of_drawings):
        current_page += 1
        update_canvas()
    else:
        messagebox.showinfo("End of Pages", "This is the last page :(")
    page_label.config(text=f"Page: {current_page}")


def previous_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        update_canvas()
    else:
        messagebox.showinfo("Start of Pages", "This is the first page :(")
    page_label.config(text=f"Page: {current_page}")


def update_all_of_drawings_after_page_change():
    global all_of_drawings
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            draw_saved_shape(shape)

def add_page():
    global current_page
    current_page += 1
    update_canvas()
    page_label.config(text=f"Page: {current_page}")
    reassign_page_numbers()
    update_all_of_drawings_after_page_change()

def delete_page():
    global current_page, all_of_drawings
    if len(set(shape['page'] for shape in all_of_drawings)) > 1:  # Ensure at least one page remains
        all_of_drawings = [shape for shape in all_of_drawings if shape['page'] != current_page]
        reassign_page_numbers()
        if current_page > len(set(shape['page'] for shape in all_of_drawings)):
            current_page -= 1
        update_canvas()
        page_label.config(text=f"Page: {current_page}")
        update_all_of_drawings_after_page_change()




def update_canvas():
    global canvas, current_page
    canvas.delete("all")  # Clear the canvas
    # Redraw shapes for the current page
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            draw_saved_shape(shape)
    page_label.config(text=f"Page: {current_page}")


def draw_saved_shape(shape):
    if shape['type'] == "circle":
        canvas.create_oval(shape['coords'], outline=shape['color'], fill=shape['fill'], width=shape['width'])
    elif shape['type'] == "square":
        canvas.create_rectangle(shape['coords'], outline=shape['color'], fill=shape['fill'], width=shape['width'])
    elif shape['type'] == "triangle":
        canvas.create_polygon(shape['coords'], outline=shape['color'], fill=shape['fill'], width=shape['width'])
    elif shape['type'] == "line":
        canvas.create_line(shape['coords'], fill=shape['color'], width=shape['width'])
    elif shape['type'] == "curve":
        canvas.create_line(shape['coords'], smooth=True, fill=shape['color'], width=shape['width'])

def reassign_page_numbers():
    global all_of_drawings
    page_mapping = {}
    new_page = 1
    for shape in all_of_drawings:
        old_page = shape['page']
        if old_page not in page_mapping:
            page_mapping[old_page] = new_page
            new_page += 1
        shape['page'] = page_mapping[old_page]


def open_width_scale():
    global width_scale
    width_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Width (%)", command=change_width)
    width_scale.pack(side=tk.LEFT, padx=5, pady=5)


def open_height_scale():
    global height_scale
    height_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Height (%)", command=change_height)
    height_scale.pack(side=tk.LEFT, padx=5, pady=5)


def finish_editing():
    global edit_mode, width_scale, height_scale
    edit_mode = False
    if width_scale:
        width_scale.pack_forget()  # Remove width scale from view
    if height_scale:
        height_scale.pack_forget()  # Remove height scale from view


def open_rotate_scale():
    rotate_scale = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label='Rotate', command=rotate_shape)
    rotate_scale.pack(side=tk.LEFT, padx=5, pady=5)


def open_type_menu():
    type_menu.post(type_button.winfo_rootx(), type_button.winfo_rooty() + type_button.winfo_height())


def open_animation_menu():
    global selected_animation
    print("in open_animation_menu:")
    print("the selected_animation:")
    print(selected_animation)
    #######it prints None#########

    animation_menu = tk.Menu(root, tearoff=0)

    # Add commands for each animation option
    for option in animation_options:
        animation_menu.add_command(label=option, command=lambda opt=option: update_animation_button(opt))

    # Display the menu near the "Animations" button
    animation_menu.post(animation_button.winfo_rootx(),
                        animation_button.winfo_rooty() + animation_button.winfo_height())


# Function to update animation button text
def update_animation_button(option):
    global selected_animation


    selected_animation = option

    print("in update_animation_button:")
    print("the selected_animation:")
    print(selected_animation)
    #######it prints the animation#########

    animation_button.config(text=f"Animation: {selected_animation}")

    # Enable the Type button and update its options based on selected animation
    type_button.config(state=tk.NORMAL)
    update_type_options(selected_animation)



def update_type_options(animation):
    print("in update_type_options:")
    print("the selected_animation:")
    print(selected_animation)
    #######it prints the animation#########

    type_menu.delete(0, tk.END)  # Clear previous options

    if animation == "Fade":
        type_options = ["FadeIn", "FadeOut"]
    elif animation == "Transform":
        type_options = ["Rotate", "Scale", "TransformToAnObject"]
    elif animation == "Creation":
        type_options = ["Create", "Uncreate", "Grow"]
    elif animation == "Write":
        type_options = ["Write", "ShowPassingFlash", "WriteOnce"]
    else:
        type_options = []  # Default empty options if no specific animation selected

    # Add commands for each type option
    for option in type_options:
        type_menu.add_command(label=option, command=lambda opt=option: update_type_button(opt))


def update_type_button(option):

    global selected_type
    selected_type = option
    print("in update_type_button:")
    print("the selected_animation:")
    print(selected_animation)
    #######it prints the animation#########
    print("in update_type_button:")
    print("the selected_type:")
    print(selected_type)
    #######it prints the animation#########
    type_button.config(text=f"Type: {option}")
    object_button.config(state=tk.NORMAL)  # Enable the object button


def open_object_menu():
    print("in open_object_menu:")
    print("the selected_animation:")
    print(selected_animation)
    #######it prints the animation#########
    print("in open_object_menu:")
    print("the selected_type:")
    print(selected_type)
    #######it prints the animation#########


    object_menu.post(object_button.winfo_rootx(), object_button.winfo_rooty() + object_button.winfo_height())
    # select_object(shape)
    # Enable Entry widgets for object properties

    # width_entry.config(state=tk.NORMAL)
    # height_entry.config(state=tk.NORMAL)
    # border_color_entry.config(state=tk.NORMAL)
    # fill_color_entry.config(state=tk.NORMAL)
    # x_coord_entry.config(state=tk.NORMAL)
    # y_coord_entry.config(state=tk.NORMAL)
    #
    # width_entry.insert(0, "Sample Text")
    # height_entry.insert(0, "Sample Text")
    # border_color_entry.insert(0, "Sample Text")
    # fill_color_entry.insert(0, "Sample Text")
    # x_coord_entry.insert(0, "Sample Text")
    # y_coord_entry.insert(0, "Sample Text")


# def create_animation():


def create_animation():
    global sorted_drawings
    Shape_Var =[]

    # Extract the 'type' from each dictionary in sorted_drawings
    Shape_Var = [drawing['type'] for drawing in sorted_drawings]
    # print("jkjkjkjkj")
    # print(Shape_Var)  # Output: ['triangle', 'circle']
    Shape_colore_fill = [drawing['fill'] for drawing in sorted_drawings]

    Shape_colore_Bor = [drawing['color'] for drawing in sorted_drawings]
    Shape_colore_Width = [drawing['width'] for drawing in sorted_drawings]
    Shape_speed = [drawing['speed'] for drawing in sorted_drawings]
    Shape_start_time = [drawing['start_time'] for drawing in sorted_drawings]
    Shape_anime = [drawing['typeAnimation'] for drawing in sorted_drawings]
    Shape_coords = [drawing['coords'] for drawing in sorted_drawings]
    # print(Shape_colore_Bor)

    class ShapeAnimation(Scene):
        def construct(self):
            shapes = []
            i = 0
            # Create shapes based on Shape_Var
            for shape_type in Shape_Var:
                if shape_type == "circle":
                    # x1, y1, x2, y2 = Shape_coords[i]
                    # center_x = (x1 + x2) / 2
                    # center_y = (y1 + y2) / 2
                    # radius = (x2 - x1) / 2
                    shape = Circle(color=Shape_colore_fill[i], fill_opacity=0.5)
                    # shape.set_stroke(color=Shape_colore_Bor[i], width=Shape_colore_Width[i])
                    shape.set_stroke(color=Shape_colore_Bor[i], width=4)
                    # shape.set_center(center_x, center_y)
                    # shape.set_radius(radius)
                    i = i + 1
                elif shape_type == "triangle":
                    shape = Triangle(color=Shape_colore_fill[i], fill_opacity=0.5)
                    # shape.set_stroke(color=Shape_colore_Bor[i], width=Shape_colore_Width[i])
                    shape.set_stroke(color=Shape_colore_Bor[i], width=4)
                    # x1, y1, x2, y2, x3, y3 = Shape_coords[i]
                    # shape.set_vertices(x1, y1, x2, y2, x3, y3)
                    i = i + 1
                elif shape_type == "square":
                    # coords = Shape_coords[i]
                    # center_x = (x1 + x2) / 2
                    # center_y = (y1 + y2) / 2

                    shape = Square(color=Shape_colore_fill[i], fill_opacity=0.5)
                    # shape.set_stroke(color=Shape_colore_Bor[i], width=Shape_colore_Width[i])
                    shape.set_stroke(color=Shape_colore_Bor[i], width=4)

                    i = i + 1
                elif shape_type == "line":
                    shape = Line(color=Shape_colore_fill[i], fill_opacity=0.5)
                    # shape.set_stroke(color=Shape_colore_Bor[i], width=Shape_colore_Width[i])
                    shape.set_stroke(color=Shape_colore_Bor[i], width=4)
                    # x1, y1, x2, y2 = Shape_coords[i]
                    # shape.set_points(x1, y1, x2, y2)
                    i = i + 1
                # elif shape_type == "curve":
                #     # x1, y1, x2, y2 = Shape_coords[i]
                #     # start_point = np.array([x1, y1, 0])
                #     # end_point = np.array([x2, y2, 0])
                #
                #     shape = CurvedArrow(start_point, end_point, color=Shape_colore_fill[i], fill_opacity=0.5)
                #     # shape.set_stroke(color=Shape_colore_Bor[i], width=Shape_colore_Width[i])
                #     shape.set_stroke(color=Shape_colore_Bor[i], width=4)
                #     i = i + 1

                # Add more elif conditions for other shape types like square, line, curve

                shapes.append(shape)

            i=0
            # Animation sequence for each shape
            for shape in shapes:
                # self.play(Create(shape))
                # self.play(Transform(shape, shape.copy().scale(2)))
                # self.play(FadeOut(shape))
                # Calculate start_time for the shape
                wait_time = Shape_start_time[i] - Shape_start_time[0] if i > 0 else Shape_start_time[i]
                # print("wait_time:")
                # print(wait_time)
                # print("speed:")
                # print(Shape_speed[i])
                # Animation sequence for each shape
                self.wait(wait_time)
                if Shape_anime[i] == "Create":
                    self.play(Create(shape), run_time=Shape_speed[i])
                elif Shape_anime[i] == "Uncreate":
                    self.play(Uncreate(shape), run_time=Shape_speed[i])
                elif Shape_anime[i] == "Grow":
                    self.play(GrowFromCenter(shape), run_time=Shape_speed[i])
                elif Shape_anime[i] == "FadeIn":
                    self.play(FadeIn(shape), run_time=Shape_speed[i])
                elif Shape_anime[i] == "FadeOut":
                    self.play(FadeOut(shape), run_time=Shape_speed[i])
                i=i+1


    if __name__ == "__main__":
        # Configure Manim to open the file after rendering
        config.video_dir = "./"
        config.open_file = True

        # Render the scene
        scene = ShapeAnimation()
        scene.render()


# Create the main window
root = tk.Tk()
root.title("Manim")
root.configure(bg='white')

# Create frame for buttons
button_frame = tk.Frame(root, bg='lightgray')
button_frame.pack(side=tk.LEFT, fill=tk.Y)


# Create a dropdown menu for shapes
shape_menu = tk.Menu(button_frame, tearoff=0)
shape_menu.add_command(label="Circle", command=lambda: select_shape("circle"))
shape_menu.add_command(label="Square", command=lambda: select_shape("square"))
shape_menu.add_command(label="Triangle", command=lambda: select_shape("triangle"))
shape_menu.add_command(label="Line", command=lambda: select_shape("line"))
shape_menu.add_command(label="Curve", command=lambda: select_shape("curve"))

shape_button = tk.Button(button_frame, text="Shapes", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
shape_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
shape_button.config(command=lambda: shape_menu.post(shape_button.winfo_rootx(), shape_button.winfo_rooty() + shape_button.winfo_height()))


undo_button = tk.Button(button_frame, text="Undo", command=undo, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
undo_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10

redo_button = tk.Button(button_frame, text="Redo", command=redo, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
redo_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10


# Create a dropdown menu for edit options
edit_menu = tk.Menu(button_frame, tearoff=0)
edit_menu.add_command(label="Change Color", command=change_color)
edit_menu.add_command(label="Change Fill Color", command=change_fill_color)
edit_menu.add_command(label="Width", command=open_width_scale)
edit_menu.add_command(label="Height", command=open_height_scale)
edit_menu.add_command(label="Rotate", command=open_rotate_scale)
edit_menu.add_command(label="Finish", command=finish_editing)

# Modify the edit button to show the menu
edit_button = tk.Button(button_frame, text="Edit", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
edit_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
edit_button.config(command=lambda: edit_menu.post(edit_button.winfo_rootx(), edit_button.winfo_rooty() + edit_button.winfo_height()))



prev_page_button = tk.Button(button_frame, text="Previous Page", command=previous_page, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
next_page_button = tk.Button(button_frame, text="Next Page", command=next_page, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
add_page_button = tk.Button(button_frame, text="Add Page", command=add_page, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
delete_page_button = tk.Button(button_frame, text="Delete Page", command=delete_page, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')

prev_page_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
next_page_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
add_page_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
delete_page_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10

###################################FOR MANIM ANIMATION####################
# Create a frame on the right side
right_button_frame = tk.Frame(root, bg='lightgray', relief=tk.FLAT, bd=0)
right_button_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Add an "Animations" button next to the Canvas on the right side
animation_button = tk.Button(right_button_frame, text="Animations", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
animation_button.pack(side=tk.TOP, padx=5, pady=10)

# Define animation options
animation_options = ["Creation", "Fade", "Transform", "Write"]

# Create Type button (initially disabled)
type_button = tk.Button(right_button_frame, text="Type", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray', state=tk.DISABLED)
type_button.pack(side=tk.TOP, padx=5, pady=10)

# Create menu for Type button
type_menu = tk.Menu(root, tearoff=0)

# Object button and menu
object_button = tk.Button(right_button_frame, text="Choose Object", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray', state=tk.DISABLED)
object_button.pack(side=tk.TOP, padx=5, pady=10)

object_menu = tk.Menu(root, tearoff=0)


##################################################
##################################################
##################################################
##################################################

animation_button.config(command=open_animation_menu)
type_button.config(command=open_type_menu)
object_button.config(command=open_object_menu)

# Create Labels for object properties
# width_label = tk.Label(right_button_frame, text="Width:")
# height_label = tk.Label(right_button_frame, text="Height:")
# border_color_label = tk.Label(right_button_frame, text="Border Color:")
# fill_color_label = tk.Label(right_button_frame, text="Fill Color:")
# x_coord_label = tk.Label(right_button_frame, text="X Coordinate:")
# y_coord_label = tk.Label(right_button_frame, text="Y Coordinate:")

# Create Entry widgets for object properties
# width_entry = tk.Entry(right_button_frame, width=10, state=tk.DISABLED)
# height_entry = tk.Entry(right_button_frame, width=10, state=tk.DISABLED)
# border_color_entry = tk.Entry(right_button_frame, width=10, state=tk.DISABLED)
# fill_color_entry = tk.Entry(right_button_frame, width=10, state=tk.DISABLED)
# x_coord_entry = tk.Entry(right_button_frame, width=10, state=tk.DISABLED)
# y_coord_entry = tk.Entry(right_button_frame, width=10, state=tk.DISABLED)

# Pack the labels and entry widgets
# width_label.pack(side=tk.TOP, padx=5, pady=2)
# width_entry.pack(side=tk.TOP, padx=5, pady=2)
# height_label.pack(side=tk.TOP, padx=5, pady=2)
# height_entry.pack(side=tk.TOP, padx=5, pady=2)
# border_color_label.pack(side=tk.TOP, padx=5, pady=2)
# border_color_entry.pack(side=tk.TOP, padx=5, pady=2)
# fill_color_label.pack(side=tk.TOP, padx=5, pady=2)
# fill_color_entry.pack(side=tk.TOP, padx=5, pady=2)
# x_coord_label.pack(side=tk.TOP, padx=5, pady=2)
# x_coord_entry.pack(side=tk.TOP, padx=5, pady=2)
# y_coord_label.pack(side=tk.TOP, padx=5, pady=2)
# y_coord_entry.pack(side=tk.TOP, padx=5, pady=2)



add_button = tk.Button(right_button_frame, text="Add", command=show_add_button, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
add_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10

add_button.config(command= show_add_button)


video_button = tk.Button(right_button_frame, text="Preview", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
video_button.pack(side=tk.TOP, padx=5, pady=80)
video_button.config(command=create_animation)
############################################
# Create canvas for drawing shapes
canvas = tk.Canvas(root, width=800, height=600, bg='white', borderwidth=2, relief=tk.SUNKEN)
canvas.pack(fill=tk.BOTH, expand=True)

# Create a label to display the current page number
page_label = tk.Label(root, text=f"{current_page}", bg='lightgray', font=("Arial", 14))
page_label.pack(side=tk.BOTTOM, fill=tk.X)


# Optionally add a grid or guides
# for i in range(0, 800, 20):
#     canvas.create_line(i, 0, i, 600, fill="lightgray", tags="grid")
# for i in range(0, 600, 20):
#     canvas.create_line(0, i, 800, i, fill="lightgray", tags="grid")
#
# # Consider using a different cursor when drawing shapes
# canvas.config(cursor="dot")

# Bind events to canvas
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<B1-Motion>", draw_shape)
canvas.bind("<ButtonRelease-1>", end_draw)

# Start the main loop
root.mainloop()