
import tkinter as tk
from tkinter import colorchooser, Toplevel, messagebox, ttk,font
from tkinter import PhotoImage, Menu
from tkinter import Canvas, Entry, Toplevel, Label, OptionMenu, StringVar
from manim import *
import math

from svgelements import QuadraticBezier


selected_shape = None
shape_id = None
start_x = 0
start_y = 0
shape_color = 'black'
shape_width = None
shape_height = None
shape_fill = 'white'
current_shape = None
current_page = 1
max_page = 1

resizing = False
drawing = False
edit_mode = False
shape_window = None
add_shape_mode = False
drawing_mode = False   #####I DIDNT USE IT IN THE SHAPES ####

selected_target_shape=None
selected_animation = None
end_selected_animation = None
# selected_type = None
speed_value = 0
end_speed=0
start_time_value = 0
end_time_value = 0

selected_text = None
start_x_text, start_y_text = None, None
text_mode = False
text_rectangle = None
text_entry = None
text_entry_id = None
selected_text_id = None
adding_text = False
selected_color = None
canvas_id=None
# List to keep track of text items and their properties
text_items = []
# Default properties
default_font_family = "Arial"
default_font_size = 16
default_color = "black"
default_bold = False
default_italic = False
default_underline = False

undo_stack = []
redo_stack = []

all_of_drawings = []
sorted_drawings = []

page_with_time = [(1, None)]

########################################DRAWING SECTION##############################
################################################ Text functions: #########################################
def start_drag(event, canvas_id):
    global start_x_text, start_y_text, selected_text
    start_x_text, start_y_text = event.x, event.y

    # Set the selected text to the one clicked
    selected_text = (canvas_id, event.widget)


def drag_text(event, canvas_id):
    global start_x_text, start_y_text

    # Calculate the movement
    dx, dy = event.x - start_x_text, event.y - start_y_text

    # Move the text entry
    canvas.move(canvas_id, dx, dy)

    # Update start position
    start_x_text, start_y_text = event.x, event.y


def end_drag(event, canvas_id):
    pass  # Optional: Add any final actions needed when dragging ends

def add_text():
    global selected_text, selected_color, text_items
    print("llllllll")
    print(text_items)

    # Create a new text entry on the canvas
    text_entry = tk.Text(canvas, wrap=tk.WORD, height=2, width=20)
    canvas_id = canvas.create_window(300, 150, window=text_entry, anchor='center')
    text_entry.focus_set()  # Set focus to the text entry
    selected_text = (canvas_id, text_entry)

    # Initialize properties for the new text entry with default values
    text_properties = {
        'id': canvas_id,
        'font': (default_font_family, default_font_size),
        'color': default_color,  # Default color is black
        'size': default_font_size,
        'text': "",
        'bold': default_bold,
        'italic': default_italic,
        'underline': default_underline,
    }
    text_items.append(text_properties)

    # Set default font and color
    text_entry.config(font=(default_font_family, default_font_size), foreground=default_color)

    # Update the text field when the user modifies the text
    def update_text_field(event):
        text_properties['text'] = text_entry.get("1.0", tk.END).strip()

    text_entry.bind("<KeyRelease>", update_text_field)

    # Bind events for dragging the text entry
    text_entry.bind("<ButtonPress-1>", lambda event: start_drag(event, canvas_id))
    text_entry.bind("<B1-Motion>", lambda event: drag_text(event, canvas_id))
    text_entry.bind("<ButtonRelease-1>", lambda event: end_drag(event, canvas_id))

def edit_text():
    global selected_text, selected_color
    if selected_text:
        canvas_id, text_entry = selected_text

        # Retrieve the text properties for the selected text
        text_properties = next(item for item in text_items if item["id"] == canvas_id)
        current_text = text_entry.get("1.0", tk.END).strip()
        text_properties['text'] = current_text  # Update text property with the current text
        current_font = text_properties["font"]
        current_color = text_properties["color"]
        is_bold = text_properties["bold"]
        is_italic = text_properties["italic"]
        is_underline = text_properties["underline"]

        # Set selected color to the text's current color
        selected_color = current_color

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Text Properties")

        font_label = tk.Label(edit_window, text="Font Family:")
        font_label.grid(row=0, column=0, padx=10, pady=5)

        font_family = font.Font(font=current_font).actual()['family']
        font_var = tk.StringVar(value=font_family)
        font_combo = tk.OptionMenu(edit_window, font_var, *font.families())
        font_combo.grid(row=0, column=1, padx=10, pady=5)

        size_label = tk.Label(edit_window, text="Font Size:")
        size_label.grid(row=1, column=0, padx=10, pady=5)

        font_size = text_properties["size"]
        size_var = tk.IntVar(value=font_size)
        size_spinbox = tk.Spinbox(edit_window, from_=8, to=72, textvariable=size_var)
        size_spinbox.grid(row=1, column=1, padx=10, pady=5)

        def update_text_properties(*args):
            # Construct the font tuple based on the selected options
            styles = []
            if bold_var.get():
                styles.append('bold')
            if italic_var.get():
                styles.append('italic')
            if underline_var.get():
                styles.append('underline')

            if styles:
                new_font = (font_var.get(), size_var.get(), ' '.join(styles))
            else:
                new_font = (font_var.get(), size_var.get())

            text_properties['font'] = new_font
            text_properties['size'] = size_var.get()
            text_properties['color'] = selected_color if selected_color else current_color
            text_entry.config(font=new_font, foreground=text_properties["color"])

        # Update the text properties immediately when changes are made
        font_var.trace("w", update_text_properties)  # Listen for changes in font family
        size_var.trace("w", update_text_properties)  # Listen for changes in font size

        def choose_color():
            global selected_color
            color = colorchooser.askcolor(initialcolor=current_color)[1]
            if color:
                selected_color = color
                text_properties['color'] = color
                text_entry.config(foreground=color)

        color_button = tk.Button(edit_window, text="Color", command=choose_color)
        color_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        bold_var = tk.BooleanVar(value=is_bold)
        bold_check = tk.Checkbutton(edit_window, text="Bold", variable=bold_var)
        bold_check.grid(row=3, column=0, padx=10, pady=5)

        italic_var = tk.BooleanVar(value=is_italic)
        italic_check = tk.Checkbutton(edit_window, text="Italic", variable=italic_var)
        italic_check.grid(row=3, column=1, padx=10, pady=5)

        underline_var = tk.BooleanVar(value=is_underline)
        underline_check = tk.Checkbutton(edit_window, text="Underline", variable=underline_var)
        underline_check.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        def toggle_font_style():
            text_properties['bold'] = bold_var.get()
            text_properties['italic'] = italic_var.get()
            text_properties['underline'] = underline_var.get()
            styles = []
            if text_properties['bold']:
                styles.append("bold")
            if text_properties['italic']:
                styles.append("italic")
            if text_properties['underline']:
                styles.append("underline")
            new_font = (font_var.get(), size_var.get(), ' '.join(styles) if styles else '')
            text_properties['font'] = new_font
            text_entry.config(font=new_font)

        bold_var.trace("w", lambda *args: toggle_font_style())
        italic_var.trace("w", lambda *args: toggle_font_style())
        underline_var.trace("w", lambda *args: toggle_font_style())

        # Ensure text_properties['text'] is updated with any changes made by the user
        text_entry.bind("<KeyRelease>", update_text_properties)

###############################################################################################################
###############################################################################################################
#%%%%%%%%%%%%%%%%%%% shape functions ^^^^^^^^^
def canvas_clicked(event):
    global current_shape, resizing,selected_text
    if selected_text:
        canvas_id, text_entry = selected_text
        text_entry.destroy()
        canvas.itemconfig(canvas_id, text=text_entry.get("1.0", tk.END))
        selected_text = None

    if resizing:
        return  # Don't select shapes if resizing is active

    # Get the mouse click coordinates
    x, y = event.x, event.y

    # Get all items (shapes) on the canvas
    items = canvas.find_all()

    # Check if any item contains the click coordinates
    for item in items:
        # Check if the mouse click is inside the item
        if canvas.type(item) in ['rectangle', 'oval', 'polygon', 'line']:
            coords = canvas.coords(item)
            if canvas.type(item) == 'rectangle':
                x1, y1, x2, y2 = coords
                if x1 <= x <= x2 and y1 <= y <= y2:
                    current_shape = item
                    break
            elif canvas.type(item) == 'oval':
                x1, y1, x2, y2 = coords
                if (x - (x1 + x2) / 2)**2 + (y - (y1 + y2) / 2)**2 <= ((x2 - x1) / 2)**2:
                    current_shape = item
                    break
            elif canvas.type(item) == 'polygon':
                # For triangles or any polygon
                if canvas.find_enclosed(x, y, x, y) == (item,):
                    current_shape = item
                    break


            elif canvas.type(item) == 'line':
                if len(coords)==4:
                    x1, y1, x2, y2 = coords
                    # Check if the click is near the line
                    distance = abs((y2 - y1)*x - (x2 - x1)*y + x2*y1 - y2*x1) / ((y2 - y1)**2 + (x2 - x1)**2)**0.5
                    if distance < 5:  # Tolerance for line selection
                        current_shape = item
                        break
                else:
                    ##CURVE
                    x1, y1, x2, y2, x3, y3 = coords
                    # Assuming you have a method to check proximity to the curve
                    if is_near_curve(x, y, x1, y1, x2, y2, x3, y3):
                        current_shape = item
                        break



    # If no shape is found, clear current_shape
    if current_shape is None:
        current_shape = None



def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def point_to_bezier(px, py, x1, y1, x2, y2, x3, y3, num_samples=100):
    min_dist = float('inf')
    for i in range(num_samples + 1):
        t = i / num_samples
        # Calculate the point on the Bézier curve for parameter t
        bx = (1 - t)**2 * x1 + 2 * (1 - t) * t * x2 + t**2 * x3
        by = (1 - t)**2 * y1 + 2 * (1 - t) * t * y2 + t**2 * y3
        # Calculate the distance from the point to this point on the curve
        dist = distance(px, py, bx, by)
        # Keep track of the minimum distance found
        if dist < min_dist:
            min_dist = dist
    return min_dist

def is_near_curve(px, py, x1, y1, x2, y2, x3, y3, tolerance=5):
    min_distance = point_to_bezier(px, py, x1, y1, x2, y2, x3, y3)
    return min_distance < tolerance

def select_shape(shape):
    # print("ppppppppppp")
    # print(shape)
    global selected_shape,add_shape_mode
    selected_shape = shape

    add_shape_mode = True
    ####ISRAA###
    if shape_window:
        shape_window.destroy()  # Close the shape selection window


##in the plus ##
# def enable_add_mode():
#     global add_shape_mode, shape_window
#     if selected_shape:
#         add_shape_mode = True
#         shape_window.destroy()  # Close the shape selection window
#     else:
#         messagebox.showerror("Error", "Please choose a shape!")

def open_shape_window():
    global shape_window, drawing
    drawing = True
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

    # add_button = tk.Button(shape_window, text="Add", command=enable_add_mode)
    # add_button.pack(side=tk.TOP, padx=5, pady=5)

    # cancel_button = tk.Button(shape_window, text="Cancel", command=shape_window.destroy)
    # cancel_button.pack(side=tk.TOP, padx=5, pady=5)

def start_draw(event):
    global drawing, start_x, start_y, shape_id, selected_shape, resizing, shape_width
    if add_shape_mode and selected_shape:
        drawing = True
        if not resizing:
            start_x = event.x
            start_y = event.y

def draw_shape(event):
    global drawing, shape_id, start_x, start_y, add_shape_mode, selected_shape, current_shape, resizing, shape_width
    if drawing and selected_shape and not resizing:
        if shape_id:
            canvas.delete(shape_id)
        if start_x is None:
            start_x = event.x
        if start_y is None:
            start_y = event.y
        shape_color = 'black'
        shape_fill = 'white'

        if selected_shape == "circle":
            radius = ((event.x - start_x) ** 2 + (event.y - start_y) ** 2) ** 0.5
            shape_id = canvas.create_oval(start_x - radius, start_y - radius, start_x + radius, start_y + radius, outline=shape_color, fill=shape_fill)
        elif selected_shape == "square":
            shape_id = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=shape_color, fill=shape_fill)
        elif selected_shape == "triangle":
            x1, y1 = start_x, start_y
            x2, y2 = event.x, start_y
            x3, y3 = (start_x + event.x) / 2, event.y
            shape_id = canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=shape_color, fill=shape_fill)
        elif selected_shape == "line":
            shape_id = canvas.create_line(start_x, start_y, event.x, event.y, fill=shape_color)
        elif selected_shape == "curve":
            control_x = (start_x + event.x) / 2
            control_y = (start_y + event.y) / 2 - 50
            shape_id = canvas.create_line(start_x, start_y, control_x, control_y, event.x, event.y, smooth=True, fill=shape_color)

        current_shape = shape_id
        canvas.delete("yellow_dot")
        draw_yellow_dots(canvas, current_shape)

def end_draw(event):
    global drawing, shape_id, add_shape_mode, current_shape, edit_mode, shape_width, shape_height
    if drawing:
        drawing = False
        if shape_id:
            canvas.tag_bind(current_shape, '<ButtonPress-1>', on_shape_click)
            undo_stack.append(shape_id)
            current_shape = shape_id
            save_shape_properties()  # Save the shape with the current page info
            update_width_height()
        shape_id = None
        redo_stack.clear()
        update_object_menu()

        open_target_object_menu()
        add_shape_mode = False
        drawing = False

def update_width_height():
    global shape_height,shape_width,current_shape,all_of_drawings
    # print(shap)
    # print("in update_width_height")
    # print(shape_width)
    # print(shape_height)
    shape_height = None
    shape_width = None
    # print("in update_width_height")
    # print(shape_width)
    # print(shape_height)
    # coords = canvas.coords(current_shape)

    shapee =get_sshape(current_shape)
    if shapee is not None:
        coords = shapee['coords']
        # print("p[][][][][][opopjdkhdhjhj")
        # print(coords)
        # print(shapee)
        # print("00000000")
        # print(shapee['type'])
        if shapee['type'] == "circle":
            # Circle: Calculate diameter as width and height
            x1, y1, x2, y2 = coords
            shape_width = abs(x2 - x1)
            shape_height = abs(y2 - y1)
        elif shapee['type'] in ["square", "rectangle"]:
            # print(coords)
            # Rectangle or Square
            x1, y1, x2, y2 = coords
            shape_width = abs(x2 - x1)
            shape_height = abs(y2 - y1)
        elif shapee['type'] == "triangle":
            # Triangle: Calculate bounding box width and height
            x1, y1, x2, y2, x3, y3 = coords
            shape_width = max(x1, x2, x3) - min(x1, x2, x3)
            shape_height = max(y1, y2, y3) - min(y1, y2, y3)
        elif shapee['type'] == "line":
            # Line: Width and height are just the difference in coordinates
            x1, y1, x2, y2 = coords
            shape_width = abs(x2 - x1)
            shape_height = abs(y2 - y1)
        elif shapee['type'] == "curve":
            # Curve: Approximate width and height based on the coordinates
            x1, y1, x2, y2, cx, cy = coords
            shape_width = abs(max(x1, x2, cx) - min(x1, x2, cx))
            shape_height = abs(max(y1, y2, cy) - min(y1, y2, cy))

        # print(shape_width)
        # print(shape_height)
        # print("in update_width_height")
        # print(shape_width)
        # print(shape_height)
        update_all_of_drawings(shapee['id'], height=shape_height)
        update_all_of_drawings(shapee['id'], width=shape_width)
        #####the hieght and width untill here are correct
        # print(all_of_drawings)
        shape_width = None
        shape_height = None
    # print(all_of_drawings)
def draw_yellow_dots(canvas, shape_id):
    coords = canvas.coords(shape_id)

    if canvas.type(shape_id) in ["rectangle", "oval"]:
        x1, y1, x2, y2 = coords
        if canvas.type(shape_id) == "rectangle":
            dot_coords = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        else:  # For oval
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            rx = (x2 - x1) / 2
            ry = (y2 - y1) / 2
            dot_coords = [
                (cx, cy - ry),  # Top
                (cx, cy + ry),  # Bottom
                (cx - rx, cy),  # Left
                (cx + rx, cy)  # Right
            ]
    elif canvas.type(shape_id) == "polygon":  # Triangle
        x1, y1, x2, y2, x3, y3 = coords
        dot_coords = [(x1, y1), (x2, y2), (x3, y3)]
    elif canvas.type(shape_id) == "line":
        if len(coords)==4:
            x1, y1, x2, y2 = coords
            dot_coords = [(x1, y1), (x2, y2)]
        elif len(coords)==6:
            x1, y1, x2, y2, x3, y3 = coords
            dot_coords = [(x1, y1), (x3, y3)]

    else:
        return

    for x, y in dot_coords:
        dot = canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='yellow', tags=("yellow_dot", "resize_handle"))
        canvas.tag_bind(dot, '<ButtonPress-1>', on_dot_click)
        canvas.tag_bind(dot, '<B1-Motion>', resize_shape)

def on_dot_click(event):
    global start_x, start_y, resizing
    # print("on_dot_click")
    resizing = True
    start_x = event.x
    start_y = event.y


def on_shape_click(event):
    global current_shape, start_x, start_y, resizing,shape_width,all_of_drawings
    # print(shape_width)
    # print("on_shape_click(on_shape_click(")
    # print(all_of_drawings)
    # print(resizing)
    if not resizing:
        current_shape = canvas.find_closest(event.x, event.y)[0]
        start_x = event.x
        start_y = event.y

        # Remove previous yellow dots if any
        canvas.delete("yellow_dot")

        # Draw yellow dots around the clicked shape
        draw_yellow_dots(canvas, current_shape)

        # Identify the shape in all_of_drawings
        for shape in all_of_drawings:
            if shape['id'] == current_shape and shape['page'] == current_page:
                # Call select_object with the identified shape
                select_object(shape)
                break  # Stop once the shape is found

        # Bind drag event to the shape
        canvas.tag_bind(current_shape, '<B1-Motion>', drag_shape)
    resizing = False


def start_resizing(event):
    global start_x, start_y, resizing, current_shape,shape_width
    # print(shape_width)
    if current_shape:
        start_x = event.x
        start_y = event.y
        resizing = True


def resize_shape(event):
    global start_x, start_y, resizing, current_shape,shape_width,shape_height,all_of_drawings
    # print("in resize")
    # print(shape_width)
    # print(shape_height)
    # print(all_of_drawings)
    if current_shape:
        dx = event.x - start_x
        dy = event.y - start_y
        coords = canvas.coords(current_shape)
        if len(coords) == 4:  # Rectangle or oval
            x1, y1, x2, y2 = coords
            canvas.coords(current_shape, x1, y1, x2 + dx, y2 + dy)
        elif len(coords) == 6:  # Triangle
            if canvas.type(current_shape) == "polygon":
                x1, y1, x2, y2, x3, y3 = coords
                canvas.coords(current_shape, x1, y1, x2 + dx, y2, (x1 + x2 + dx) / 2, y3 + dy)

            else:
                x1, y1, cx, cy, x2, y2 = coords
                # Adjust control points
                new_cx = cx + dx
                new_cy = cy + dy
                new_x2 = x2 + dx
                new_y2 = y2 + dy
                canvas.coords(current_shape, x1, y1, new_cx, new_cy, new_x2, new_y2)

        elif len(coords) == 2:  # Line
            x1, y1 = coords
            x2, y2 = canvas.coords(current_shape)[2], canvas.coords(current_shape)[3]
            canvas.coords(current_shape, x1, y1, x2 + dx, y2 + dy)

        update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))

        # Delete old yellow dots
        canvas.delete("yellow_dot")

        # Draw new yellow dots around the resized shape
        draw_yellow_dots(canvas, current_shape)
        start_x = event.x
        start_y = event.y
        update_width_height()
        # print("in resize")
        # print(shape_width)
        # print(shape_height)
        # save_shape_properties()

def stop_resizing(event):
    global resizing,shape_width
    # print(shape_width)
    resizing = False


def drag_shape(event):
    global current_shape, start_x, start_y,all_of_drawings
    # print("in drag")
    # print(all_of_drawings)
    # Calculate the movement
    dx, dy = event.x - start_x, event.y - start_y

    # Move the shape
    canvas.move(current_shape, dx, dy)

    # Delete old yellow dots
    canvas.delete("yellow_dot")

    # Draw new yellow dots around the dragged shape
    draw_yellow_dots(canvas, current_shape)

    # Update start position
    start_x, start_y = event.x, event.y

def get_sshape(c_shape):
    for s in all_of_drawings:
        if s['id'] == c_shape:
            return s
    return None  # Explicitly return None if shape not found

def change_color():
    global shape_color, edit_mode, current_shape

    # print("poopoopoopoo")
    # print(all_of_drawings)
    shape=get_sshape(current_shape)
    # print(shape['type'])
    # print(len(shape['coords']))

    if shape['type'] == "line":
        messagebox.showwarning("Warning", "There is no border for line")

    elif shape['type'] == "curve":
        messagebox.showwarning("Warning", "There is no border for Curve")
    else:
        edit_mode = True
        color = colorchooser.askcolor()[1]
        if color:
            shape_color = color

            if current_shape:
                canvas.itemconfig(current_shape, outline=shape_color)
                update_all_of_drawings(current_shape, color=shape_color)

            shape_color = 'black'



def change_fill_color():
    global shape_fill,edit_mode,current_shape

    edit_mode = True
    color = colorchooser.askcolor()[1]
    if color:
        shape_fill = color

        if current_shape:
            canvas.itemconfig(current_shape, fill=shape_fill)
            update_all_of_drawings(current_shape, fill=shape_fill)

        shape_fill='white'

# def undo():
#     if undo_stack:
#         shape_id = undo_stack.pop()
#         canvas.itemconfigure(shape_id, state='hidden')
#         redo_stack.append(shape_id)
#
# def redo():
#     if redo_stack:
#         shape_id = redo_stack.pop()
#         canvas.itemconfigure(shape_id, state='normal')
#         undo_stack.append(shape_id)





def update_all_of_drawings(shape_id, **kwargs):
    # print("in update_all_of_drawings")
    # print(shape_width)
    # print(shape_height)
    global all_of_drawings
    for shape in all_of_drawings:
        if shape['id'] == shape_id:
            for key, value in kwargs.items():
                shape[key] = value
            # shape['coords'] = canvas.coords(shape_id)  # Update coordinates
            # shape['page'] = current_page  # Ensure correct page assignment
            # shape['width'] = shape_width
            # shape['height'] = shape_height

def save_shape_properties():
    global all_of_drawings, current_page,shape_width,shape_height,shape_id,selected_shape,shape_color,shape_fill,selected_animation,speed_value,start_time_value,end_selected_animation,end_time_value,end_speed

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
            'end_animation':end_selected_animation,
            'speed': speed_value,  # Save the speed
            'start_time': start_time_value,  # Save the start time
            'end_time':end_time_value,
            'end_speed':end_speed,
            'target_shape': selected_target_shape
        }
        all_of_drawings.append(shape_properties)

def clear_current_page():
    global all_of_drawings
    # Remove all shapes associated with the current page
    all_of_drawings = [shape for shape in all_of_drawings if shape['page'] != current_page]
    canvas.delete("all")  # Clear the canvas
    update_object_menu()  # Update the object menu if you have one
    open_target_object_menu()
def delete_shape():
    global all_of_drawings, current_shape
    if current_shape:
        # Remove the shape from the canvas
        canvas.delete(current_shape)

        # Remove the yellow dots associated with the current shape
        canvas.delete("yellow_dot")

        # Remove the shape from the list of drawings
        all_of_drawings = [shape for shape in all_of_drawings if shape['id'] != current_shape]

        # Clear the current shape
        current_shape = None

        # Update the object menu if you have one
        update_object_menu()
        open_target_object_menu()
# #####     PAGES     #####

def clear_canvas():
    """Clear the canvas."""
    canvas.delete("all")


def load_shapes():
    """Load shapes for the current page."""
    clear_canvas()
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            canvas.create_rectangle(shape['coords'], outline='black')  # Adjust this for different shapes


def navigate_page(direction):
    global current_page, max_page
    save_shape_properties()  # Save current shapes before changing page
    current_page += direction
    if current_page < 1:
        current_page = 1
    elif current_page > max_page:
        max_page += 1
    update_page_label()
    load_shapes()  # Load shapes for the new page

def add_page():
    global max_page, current_page
    max_page += 1
    current_page = max_page
    load_shapes_for_current_page()
    update_page_label()
def delete_page():
    global current_page, max_page, all_of_drawings

    # Remove all shapes associated with the current page
    all_of_drawings = [shape for shape in all_of_drawings if shape['page'] != current_page]

    # Adjust page count
    if current_page == max_page:
        max_page -= 1
        current_page -= 1
    else:
        # Update the page number of shapes on higher pages
        for shape in all_of_drawings:
            if shape['page'] > current_page:
                shape['page'] -= 1
        max_page -= 1

    # If there are no pages left, reset
    if max_page < 1:
        max_page = 1
        current_page = 1

    load_shapes_for_current_page()
    update_page_label()

def next_page():
    global current_page, max_page
    if current_page < max_page:
        current_page += 1
        load_shapes_for_current_page()
    else:
        messagebox.showinfo("End of Pages", "This is the last page :(")

    update_page_label()

def previous_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        load_shapes_for_current_page()

    else:
        messagebox.showinfo("Start of Pages", "This is the first page :(")

    update_page_label()

def update_page_label():
    page_label.config(text=f"Page: {current_page}")

def load_shapes_for_current_page():
    canvas.delete("all")  # Clear the canvas
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            if shape['type'] == "circle":
                shape['id'] = canvas.create_oval(*shape['coords'], outline=shape['color'], fill=shape['fill'])
            elif shape['type'] == "square":
                shape['id'] = canvas.create_rectangle(*shape['coords'], outline=shape['color'], fill=shape['fill'])
            elif shape['type'] == "triangle":
                shape['id'] = canvas.create_polygon(*shape['coords'], outline=shape['color'], fill=shape['fill'])
            elif shape['type'] == "line":
                shape['id'] = canvas.create_line(*shape['coords'], fill=shape['color'])
            elif shape['type'] == "curve":
                shape['id'] = canvas.create_line(*shape['coords'], smooth=True, fill=shape['color'])

            # Bind the shape to make it draggable
            canvas.tag_bind(shape['id'], '<ButtonPress-1>', on_shape_click)

#####################################Drawing section###########################
#####################################Animation section###########################

def update_object_menu():
    object_menu.delete(0, tk.END)  # Clear previous options
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            shape_name = f"{shape['type'].capitalize()}"
            object_menu.add_command(label=shape_name, command=lambda s=shape: select_object(s))

def show_add_button():
    global sorted_drawings,all_of_drawings
    # print("in add show")
    # print(all_of_drawings)
    # print(all_of_drawings[0].get('type'))
    # Filter out drawings that have animations and ensure 'details' key exists
    drawings_with_animations = [d for d in all_of_drawings if d.get('animation')]
    # print("in add show")
    # print(drawings_with_animations)
    sorted_drawings = sorted(drawings_with_animations, key=lambda x: int(x['start_time']))

    # print(sorted_drawings)

    window = tk.Tk()
    window.title("Drawings Per Page")

    # Create a treeview widget to display the data
    tree = ttk.Treeview(window, columns=('Shape', 'Start Animation', 'Start Time', 'Start Speed','End Animation', 'End Time', 'End Speed'), show='headings')

    # Define the columns
    tree.heading('Shape', text='Shape')
    tree.heading('Start Animation', text='Start Animation')
    tree.heading('Start Time', text='Start Time')
    tree.heading('Start Speed', text='Start Speed')
    tree.heading('End Animation', text='End Animation')
    tree.heading('End Time', text='End Time')
    tree.heading('End Speed', text='End Speed')

    # Insert data into the treeview
    for draws in sorted_drawings:
        # print("pppp")
        # print(draws['page'])
        # print(current_page)
        if (draws['page']== (current_page)):
            tree.insert('', tk.END,
                        values=(draws['type'], draws['animation'], draws['start_time'], draws['speed'],draws['end_animation'],draws['end_time'], draws['end_speed']))

    # Pack the treeview widget
    tree.pack(expand=True, fill='both')

def increment_time_obj():
    global selected_shape,all_of_drawings
    print(increment_time_obj)
    print(all_of_drawings)
    if selected_shape['start_time'] is None:
        selected_shape['start_time'] = 0
    time_entry_obj.delete(0, tk.END)
    time_entry_obj.insert(0, str(selected_shape['start_time']))

    time = int(selected_shape['start_time'])
    time = time + 1
    # print(selected_shape['id'])
    update_all_of_drawings(selected_shape['id'], start_time=time)
    time_entry_obj.delete(0, tk.END)
    time_entry_obj.insert(0, str(time))
    # print(all_of_drawings)
    # plus_button_time_obj_end.config(state=tk.NORMAL)
    # minus_button_time_obj_end.config(state=tk.NORMAL)
    #
    # time_label_obj_end_entry.delete(0, tk.END)
    # time_label_obj_end_entry.insert(0, str(selected_shape['start_time']))
    if selected_shape['start_time'] is not None:
        selected_shape['end_time'] = selected_shape['start_time']

    elif selected_shape['start_time'] != 0:
        selected_shape['end_time'] = selected_shape['start_time']

    else:
        selected_shape['end_time'] = 0

    end_time_entry_obj.delete(0, tk.END)
    end_time_entry_obj.insert(0, str(selected_shape['end_time']))

def increment_time_obj_end():
    global selected_shape,end_time_value

    # if selected_shape['start_time'] is not None:
    #     selected_shape['end_time'] = selected_shape['start_time']
    #
    # elif selected_shape['start_time'] is not 0:
    #     selected_shape['end_time'] = selected_shape['start_time']
    #
    # else:
    #     selected_shape['end_time'] =0
    #
    # end_time_entry_obj.delete(0, tk.END)
    # end_time_entry_obj.insert(0, str(selected_shape['end_time']))

    time = int(selected_shape['end_time'])
    time = time + 1

    # print(selected_shape['id'])
    update_all_of_drawings(selected_shape['id'], end_time=time)
    end_time_entry_obj.delete(0, tk.END)
    end_time_entry_obj.insert(0, str(time))
    print(all_of_drawings)
def decrement_time_obj():
    global selected_shape,all_of_drawings
    print("decrement_time_obj")
    print(all_of_drawings)
    if selected_shape['start_time'] is None:
        selected_shape['start_time'] = 0
    time_entry_obj.delete(0, tk.END)
    time_entry_obj.insert(0, str(selected_shape['start_time']))

    time = int(selected_shape['start_time'])

    if time > 0:
        time = time - 1
        # print(selected_shape['id'])
        update_all_of_drawings(selected_shape['id'], start_time=time)
        time_entry_obj.delete(0, tk.END)
        time_entry_obj.insert(0, str(time))
        # print(all_of_drawings)
    else:
        messagebox.showwarning("Warning", "You can't have negative values!")

    if selected_shape['start_time'] is not None:
        selected_shape['end_time'] = selected_shape['start_time']

    elif selected_shape['start_time'] != 0:
        selected_shape['end_time'] = selected_shape['start_time']

    else:
        selected_shape['end_time'] = 0

    end_time_entry_obj.delete(0, tk.END)
    end_time_entry_obj.insert(0, str(selected_shape['end_time']))

def decrement_time_obj_end():
    global selected_shape,end_time_value

    if selected_shape['end_time'] is None:
        selected_shape['end_time'] = selected_shape['start_time']
    end_time_entry_obj.delete(0, tk.END)
    end_time_entry_obj.insert(0, str(selected_shape['end_time']))

    time = int(selected_shape['end_time'])
    strat=int(selected_shape['start_time'])
    if time > strat:
        time = time - 1
        # end_time_value=time
        # print(selected_shape['id'])
        update_all_of_drawings(selected_shape['id'], end_time=time)
        end_time_entry_obj.delete(0, tk.END)
        end_time_entry_obj.insert(0, str(time))
        print(all_of_drawings)
    else:
        messagebox.showwarning("Warning", "End time can't be less than Start time")
######speed####
def increment_speed_obj():
    global selected_shape

    if selected_shape['speed'] is None:
        selected_shape['speed']=0
    speed_entry_obj.delete(0, tk.END)
    speed_entry_obj.insert(0,str(selected_shape['speed']))


    speed=int(selected_shape['speed'])
    speed=speed+1
    # print(selected_shape['id'])
    update_all_of_drawings(selected_shape['id'], speed=speed)
    speed_entry_obj.delete(0, tk.END)
    speed_entry_obj.insert(0, str(speed))
    # print(all_of_drawings)
    if selected_shape['speed'] is not None:
        selected_shape['end_speed'] = selected_shape['speed']

    elif selected_shape['speed'] != 0:
        selected_shape['end_speed'] = selected_shape['speed']

    else:
        selected_shape['end_speed'] = 0

    end_speed_entry_obj.delete(0, tk.END)
    end_speed_entry_obj.insert(0, str(selected_shape['end_speed']))

def decrement_speed_obj_end():
    global selected_shape

    if selected_shape['end_speed'] is None:
        selected_shape['end_speed'] = 0
    end_speed_entry_obj.delete(0, tk.END)
    end_speed_entry_obj.insert(0, str(selected_shape['end_speed']))

    speed = int(selected_shape['end_speed'])

    if speed > 0:
        speed = speed - 1
        # print(selected_shape['id'])
        update_all_of_drawings(selected_shape['id'], end_speed=speed)
        end_speed_entry_obj.delete(0, tk.END)
        end_speed_entry_obj.insert(0, str(speed))
        # print(all_of_drawings)
    else:
        messagebox.showwarning("Warning", "You can't have negative values!")


def increment_speed_obj_end():
    global selected_shape,all_of_drawings

    if selected_shape['end_speed'] is None:
        selected_shape['end_speed'] = 0
    end_speed_entry_obj.delete(0, tk.END)
    end_speed_entry_obj.insert(0, str(selected_shape['end_speed']))

    speed = int(selected_shape['end_speed'])
    speed = speed + 1
    # print(selected_shape['id'])
    update_all_of_drawings(selected_shape['id'], end_speed=speed)
    end_speed_entry_obj.delete(0, tk.END)
    end_speed_entry_obj.insert(0, str(speed))
    print("beforee the add")
    print(all_of_drawings)
def decrement_speed_obj():
    global selected_shape

    if selected_shape['speed'] is None:
        selected_shape['speed']=0
    speed_entry_obj.delete(0, tk.END)
    speed_entry_obj.insert(0,str(selected_shape['speed']))

    speed=int(selected_shape['speed'])

    if speed > 0:
        speed = speed - 1
        # print(selected_shape['id'])
        update_all_of_drawings(selected_shape['id'], speed=speed)
        speed_entry_obj.delete(0, tk.END)
        speed_entry_obj.insert(0, str(speed))
        # print(all_of_drawings)
    else:
        messagebox.showwarning("Warning", "You can't have negative values!")

    if selected_shape['speed'] is not None:
        selected_shape['end_speed'] = selected_shape['speed']

    elif selected_shape['speed'] != 0:
        selected_shape['end_speed'] = selected_shape['speed']

    else:
        selected_shape['end_speed'] = 0

    end_speed_entry_obj.delete(0, tk.END)
    end_speed_entry_obj.insert(0, str(selected_shape['end_speed']))

def select_object(shape):
    global selected_shape, speed_value,end_speed,time_value,end_time_value
    selected_shape = shape

    object_button.config(text=f"Object: {shape['type'].capitalize()}", fg="white")
    # update_all_of_drawings(shape['id'], animation=selected_animation, typeAnimation=selected_type)
    canvas.delete("yellow_dot")
    draw_yellow_dots(canvas, shape['id'])
    print("in select obj")
    print(all_of_drawings)
    # print(all_of_drawings)

    # Initialize speed_value for the selected shape
    # speed_value = shape.get('speed', 0)  # Use 0 as the default value if 'speed' is not present
    # speed_entry.delete(0, tk.END)
    # speed_entry.insert(0, str(speed_value))




    # Assuming shape['speed'] is stored as a string with leading zeros
    speed_value = int(shape['speed'])  # Convert to integer to remove leading zeros
    time_value = int(shape['start_time'])  # Convert to integer to remove leading zeros
    end_time_value = int(shape['end_time'])
    end_speed = int(shape['end_speed'])
    # Clear the entry fields and insert the new values
    speed_entry_obj.delete(0, tk.END)
    speed_entry_obj.insert(0, str(speed_value))

    time_entry_obj.delete(0, tk.END)
    time_entry_obj.insert(0, str(time_value))

    end_speed_entry_obj.delete(0, tk.END)
    end_speed_entry_obj.insert(0, str(speed_value))

    end_time_entry_obj.delete(0, tk.END)
    end_time_entry_obj.insert(0, str(time_value))

    anim=selected_shape['animation']
    type_button.config(text=f"animation: {anim}")
    update_all_of_drawings(selected_shape['id'], animation=anim)

    end_anim = selected_shape['end_animation']
    end_type_button.config(text=f"animation: {end_anim}")
    update_all_of_drawings(selected_shape['id'], end_animation=end_anim)
# def open_type_menu():
#     type_menu.post(type_button.winfo_rootx(), type_button.winfo_rooty() + type_button.winfo_height())


def open_type_menu():
    global selected_animation
    print("in open_type_menu")
    print(all_of_drawings)
    print(selected_animation)
    animation_menu = tk.Menu(root, tearoff=0)

    # Add commands for each animation option
    for option in animation_options:
        animation_menu.add_command(label=option, command=lambda opt=option: update_animation_button(opt))

    # Display the menu near the "Animations" button
    animation_menu.post(type_button.winfo_rootx(),
                        type_button.winfo_rooty() + type_button.winfo_height())

# Function to update animation button text
def update_animation_button(option):
    global selected_animation,selected_shape
    selected_animation = option
    print(" i am in update_animation_button")
    print(selected_animation)
    update_all_of_drawings(selected_shape['id'], animation=selected_animation)
    type_button.config(text=f"animation: {selected_animation}")
    plus_button_speed_obj.config(state=tk.NORMAL)
    minus_button_speed_obj.config(state=tk.NORMAL)

    plus_button_time_obj.config(state=tk.NORMAL)
    minus_button_time_obj.config(state=tk.NORMAL)

    # Enable the Type button and update its options based on selected animation
    # type_button.config(state=tk.NORMAL)
    # update_type_options(selected_animation)
    # Check if the selected animation is "Transform"
    if selected_animation == "Transform":
        # Create "Choose Target Object" button and menu if not already created
        if not 'target_object_button' in globals():
            global target_object_button, target_object_menu
            target_object_button = tk.Button(features_frame, text="Choose Target Object", relief=tk.RAISED, bd=0,
                                             padx=5, pady=5, fg='white', bg='black')
            target_object_button.pack(side=tk.TOP, padx=5, pady=5)
            target_object_menu = tk.Menu(root, tearoff=0)

            target_object_button.config(command=open_target_object_menu)
    else:
        # If another animation is selected, remove the "Choose Target Object" button if it exists
        if 'target_object_button' in globals():
            target_object_button.pack_forget()
            del target_object_button
            del target_object_menu

def open_target_object_menu():
    if 'target_object_button' in globals():
        global selected_shape
        # Clear the menu
        target_object_menu.delete(0, tk.END)

        # Add the shapes to the menu, excluding the selected one
        for shape in all_of_drawings:
            if shape['id'] != selected_shape['id']:
                shape_name = f"{shape['type'].capitalize()}"
                target_object_menu.add_command(label=shape_name, command=lambda s=shape: select_target_object(s))


        # Display the menu
        target_object_menu.post(target_object_button.winfo_rootx(), target_object_button.winfo_rooty() + target_object_button.winfo_height())

def select_target_object(shape):
    global selected_target_shape
    selected_target_shape = shape
    target_object_button.config(text=f"Target Object: {shape['type'].capitalize()}")
    print(f"Selected target shape: {selected_target_shape}")
    update_all_of_drawings(selected_shape['id'],target_shape=selected_target_shape)

# def remove_target_shape(target_shape):
#     global all_of_drawings
#
#     # Find the shape in the all_of_drawings array and remove it
#     all_of_drawings = [shape for shape in all_of_drawings if shape['id'] != target_shape['id']]
#
#     print("Shape removed from all_of_drawings:")
#     print(all_of_drawings)

def end_open_type_menu():
    global selected_animation

    end_animation_menu = tk.Menu(root, tearoff=0)

    # Add commands for each animation option
    for option in end_animation_options:
        end_animation_menu.add_command(label=option, command=lambda opt=option: end_update_animation_button(opt))

    # Display the menu near the "Animations" button
    end_animation_menu.post(end_type_button.winfo_rootx(),
                        end_type_button.winfo_rooty() + end_type_button.winfo_height())



def end_update_animation_button(option):
    global selected_animation, selected_shape,all_of_drawings
    selected_animation = option
    print("in end_update_animation_button")
    print(all_of_drawings)
    update_all_of_drawings(selected_shape['id'], end_animation=selected_animation)
    end_type_button.config(text=f"animation: {selected_animation}")
    end_plus_button_time_obj.config(state=tk.NORMAL)
    end_minus_button_time_obj.config(state=tk.NORMAL)
    end_plus_button_speed_obj.config(state=tk.NORMAL)
    end_minus_button_speed_obj.config(state=tk.NORMAL)

# def update_type_options(animation):
#
#     type_menu.delete(0, tk.END)  # Clear previous options
#
#     if animation == "Fade":
#         type_options = ["FadeIn", "FadeOut"]
#     elif animation == "Transform":
#         type_options = ["Rotate", "Scale", "TransformToAnObject"]
#     elif animation == "Creation":
#         type_options = ["Create", "Uncreate", "Grow"]
#     elif animation == "Write":
#         type_options = ["Write", "ShowPassingFlash", "WriteOnce"]
#     else:
#         type_options = []  # Default empty options if no specific animation selected
#
#     # Add commands for each type option
#     for option in type_options:
#         type_menu.add_command(label=option, command=lambda opt=option: update_type_button(opt))


# def update_type_button(option):
#
#     global selected_type
#     selected_type = option
#
#     type_button.config(text=f"Type: {option}")
#     object_button.config(state=tk.NORMAL)  # Enable the object button
######

def open_object_menu():
    print("in open_object_menu")
    print(all_of_drawings)
    object_menu.post(object_button.winfo_rootx(), object_button.winfo_rooty() + object_button.winfo_height())

def find_page_index(page_number):
    for index, (page, _) in enumerate(page_with_time):
        if page == page_number:
            return index
    return None

def increment():
    global page_with_time, current_page
    # print("incrementincrementincrement")
    # print(page_with_time)
    try:
        # Find the index of the current page in page_with_time
        index = find_page_index(current_page)

        if index is not None:
            # Increment the time for the current page
            current_time = page_with_time[index][1] or 0
            new_time = current_time + 1
            page_with_time[index] = (current_page, new_time)

            # Update the entry field to reflect the new time
            # speed_entry.delete(0, tk.END)
            # speed_entry.insert(0, str(new_time))
    except ValueError:
        pass


def decrement():
    global page_with_time, current_page
    # print("decrementdecrementdecrement")
    # print(page_with_time)
    try:
        # Find the index of the current page in page_with_time
        index = find_page_index(current_page)

        if index is not None:
            # Decrement the time for the current page
            current_time = page_with_time[index][1] or 0
            if current_time > 0:
                new_time = current_time - 1
                page_with_time[index] = (current_page, new_time)

                # Update the entry field to reflect the new time
                # speed_entry.delete(0, tk.END)
                # speed_entry.insert(0, str(new_time))
            else:
                messagebox.showwarning("Warning", "You can't have negative values!")
    except ValueError:
        pass

def get_canvas_size(canvas):
    # Wait for the canvas to be fully rendered
    canvas.update_idletasks()
    return canvas.winfo_width(), canvas.winfo_height()

import subprocess
import os
from manim import Scene, Ellipse, Create, Transform, FadeIn, Uncreate, config  # Adjust imports as necessary

def play_video(video_path):
    """Open the video file with the default video player."""
    if os.name == 'nt':  # Windows
        os.startfile(video_path)
    elif os.name == 'posix':  # macOS or Linux
        subprocess.call(['xdg-open', video_path])  # For Linux
        # subprocess.call(['open', video_path])  # For macOS (use this if 'xdg-open' doesn't work)
    else:
        print(f"Unsupported OS: {os.name}")

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
    Shape_colore_height = [drawing['height'] for drawing in sorted_drawings]
    Shape_speed = [drawing['speed'] for drawing in sorted_drawings]
    Shape_start_time = [drawing['start_time'] for drawing in sorted_drawings]
    Shape_end_time = [drawing['end_time'] for drawing in sorted_drawings]
    Shape_anime = [drawing['animation'] for drawing in sorted_drawings]
    Shape_coords = [drawing['coords'] for drawing in sorted_drawings]
    Shape_end_speed = [drawing['end_speed'] for drawing in sorted_drawings]

    Shape_end_anime=[drawing['end_animation'] for drawing in sorted_drawings]
    Shape_target_shapes = [drawing.get('target_shape') for drawing in sorted_drawings]


    # print("ppkkppkkpp")
    # print(Shape_coords)
    print("i am in create anime")
    print(Shape_anime)
    class ShapeAnimation(Scene):

        def construct(self):
            self.camera.background_color = WHITE
            shapes = []
            target_shapes = []
            i = 0
            # print(Shape_Var)
            # print("9090909090909")
            # print(Shape_end_time)
            # Create shapes based on Shape_Var

            for i in range(len(Shape_target_shapes)):
                target_shape_data = Shape_target_shapes[i]
                if target_shape_data:
                    canvas_width, canvas_height = get_canvas_size(canvas)
                    manim_width, manim_height = config.frame_width, config.frame_height

                    target_shape_type = target_shape_data['type']
                    if target_shape_type == "circle":
                        target_shape = Ellipse(width=target_shape_data['width'] * (manim_width / canvas_width),
                                               height=target_shape_data['height'] * (manim_height / canvas_height),
                                               color=target_shape_data['fill'], fill_opacity=1)
                        target_shape.set_stroke(color=target_shape_data['color'])
                        x1, y1, x2, y2 = target_shape_data['coords']
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        width = abs(x2 - x1)
                        height = abs(y2 - y1)
                        x_manim = (x_center - canvas_width / 2) * (manim_width / canvas_width)
                        y_manim = (canvas_height / 2 - y_center) * (manim_height / canvas_height)

                        target_shape.move_to([x_manim, y_manim, 0])

                    elif target_shape_type == "square":
                        x1, y1, x2, y2 = target_shape_data['coords']
                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2
                        width = abs(x2 - x1)
                        height = abs(y2 - y1)
                        x_manim = (x_center - canvas_width / 2) * (manim_width / canvas_width)
                        y_manim = (canvas_height / 2 - y_center) * (manim_height / canvas_height)
                        target_shape = Rectangle(width=width * (manim_width / canvas_width),
                                                 height=height * (manim_height / canvas_height),
                                                 color=target_shape_data['fill'], fill_opacity=1)
                        target_shape.set_stroke(color=target_shape_data['color'])
                        target_shape.move_to([x_manim, y_manim, 0])

                    elif target_shape_type == "triangle":
                        x1, y1, x2, y2, x3, y3 = target_shape_data['coords']
                        x1_manim = (x1 - canvas_width / 2) * (manim_width / canvas_width)
                        y1_manim = (canvas_height / 2 - y1) * (manim_height / canvas_height)
                        x2_manim = (x2 - canvas_width / 2) * (manim_width / canvas_width)
                        y2_manim = (canvas_height / 2 - y2) * (manim_height / canvas_height)
                        x3_manim = (x3 - canvas_width / 2) * (manim_width / canvas_width)
                        y3_manim = (canvas_height / 2 - y3) * (manim_height / canvas_height)
                        target_shape = Polygon([x1_manim, y1_manim, 0],
                                               [x2_manim, y2_manim, 0],
                                               [x3_manim, y3_manim, 0],
                                               color=target_shape_data['fill'], fill_opacity=1)
                        target_shape.set_stroke(color=target_shape_data['color'])


                    elif target_shape_type == "line":
                        x1, y1, x2, y2 = target_shape_data['coords']
                        x1_manim = (x1 - canvas_width / 2) * (manim_width / canvas_width)
                        y1_manim = (canvas_height / 2 - y1) * (manim_height / canvas_height)
                        x2_manim = (x2 - canvas_width / 2) * (manim_width / canvas_width)
                        y2_manim = (canvas_height / 2 - y2) * (manim_height / canvas_height)
                        target_shape = Line(start=[x1_manim, y1_manim, 0], end=[x2_manim, y2_manim, 0],
                                            color=target_shape_data['color'])
                    elif target_shape_type == "curve":
                        def calculate_peak(x1, y1, x2, y2, x3, y3):
                            """Calculate the peak of the quadratic Bézier curve if possible."""
                            denominator = x3 - 2 * x2 + x1
                            if denominator != 0:
                                t = (x2 - x1) / denominator
                                x_peak = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * x2 + t ** 2 * x3
                                y_peak = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * y2 + t ** 2 * y3
                                return x_peak, y_peak
                            else:
                                x_peak = (x1 + x3) / 2
                                y_peak = (y1 + y3) / 2
                                return x_peak, y_peak

                        x1, y1, x2, y2, x3, y3 = target_shape_data['coords']
                        x1_manim = (x1 - canvas_width / 2) * (manim_width / canvas_width)
                        y1_manim = (canvas_height / 2 - y1) * (manim_height / canvas_height)
                        x2_manim = (x2 - canvas_width / 2) * (manim_width / canvas_width)
                        y2_manim = (canvas_height / 2 - y2) * (manim_height / canvas_height)
                        x3_manim = (x3 - canvas_width / 2) * (manim_width / canvas_width)
                        y3_manim = (canvas_height / 2 - y3) * (manim_height / canvas_height)
                        x_peak, y_peak = calculate_peak(x1, y1, x2, y2, x3, y3)
                        x_peak_manim = (x_peak - canvas_width / 2) * (manim_width / canvas_width)
                        y_peak_manim = (canvas_height / 2 - y_peak) * (manim_height / canvas_height)
                        curve = VMobject()
                        curve.set_points_as_corners(
                            [[x1_manim, y1_manim, 0], [x2_manim, y2_manim, 0], [x3_manim, y3_manim, 0]])
                        curve.make_smooth()
                        curve.set_color(target_shape_data['color'])
                        target_shape = curve


                    target_shapes.append(target_shape)

            i = 0
            for shape_type in Shape_Var:

                if shape_type == "circle":
                    # Extract width and height from stored properties
                    width = Shape_colore_Width[i]
                    height = Shape_colore_height[i]

                    # Calculate the center of the shape
                    x_center = (Shape_coords[i][0] + Shape_coords[i][2]) / 2
                    y_center = (Shape_coords[i][1] + Shape_coords[i][3]) / 2

                    # Get canvas size and Manim frame size
                    canvas_width, canvas_height = get_canvas_size(canvas)
                    manim_width, manim_height = config.frame_width, config.frame_height

                    # Convert center to Manim coordinates
                    x_manim = (x_center - canvas_width / 2) * (manim_width / canvas_width)
                    y_manim = (canvas_height / 2 - y_center) * (manim_height / canvas_height)

                    shape = Ellipse(width=width * (manim_width / canvas_width),
                                    height=height * (manim_height / canvas_height), color=Shape_colore_fill[i],
                                    fill_opacity=1)
                    shape.set_stroke(color=Shape_colore_Bor[i])
                    shape.move_to([x_manim, y_manim, 0])


                    i = i + 1

                elif shape_type == "triangle":
                    # Extract coordinates
                    x1, y1, x2, y2, x3, y3 = Shape_coords[i]

                    canvas_width, canvas_height = get_canvas_size(canvas)
                    manim_width, manim_height = config.frame_width, config.frame_height

                    # Convert coordinates to Manim coordinates
                    x1_manim = (x1 - canvas_width / 2) * (manim_width / canvas_width)
                    y1_manim = (canvas_height / 2 - y1) * (manim_height / canvas_height)
                    x2_manim = (x2 - canvas_width / 2) * (manim_width / canvas_width)
                    y2_manim = (canvas_height / 2 - y2) * (manim_height / canvas_height)
                    x3_manim = (x3 - canvas_width / 2) * (manim_width / canvas_width)
                    y3_manim = (canvas_height / 2 - y3) * (manim_height / canvas_height)

                    # Create Polygon for the triangle
                    shape = Polygon([x1_manim, y1_manim, 0],[x2_manim, y2_manim, 0],[x3_manim, y3_manim, 0],color=Shape_colore_fill[i],fill_opacity=1)
                    shape.set_stroke(color=Shape_colore_Bor[i])
                    i += 1

                elif shape_type == "square":
                    # Extract coordinates
                    x1, y1, x2, y2 = Shape_coords[i]

                    canvas_width, canvas_height = get_canvas_size(canvas)
                    manim_width, manim_height = config.frame_width, config.frame_height

                    # Calculate the center and size of the rectangle
                    x_center = (x1 + x2) / 2
                    y_center = (y1 + y2) / 2
                    width = abs(x2 - x1)
                    height = abs(y2 - y1)

                    # Convert center to Manim coordinates
                    x_manim = (x_center - canvas_width / 2) * (manim_width / canvas_width)
                    y_manim = (canvas_height / 2 - y_center) * (manim_height / canvas_height)

                    # Create Rectangle in Manim with specified width and height
                    shape = Rectangle(width=width * (manim_width / canvas_width),
                                      height=height * (manim_height / canvas_height), color=Shape_colore_fill[i],
                                      fill_opacity=1)
                    shape.set_stroke(color=Shape_colore_Bor[i])
                    shape.move_to([x_manim, y_manim, 0])

                    i += 1

                elif shape_type == "line":
                    # Extract coordinates
                    x1, y1, x2, y2 = Shape_coords[i]

                    canvas_width, canvas_height = get_canvas_size(canvas)
                    manim_width, manim_height = config.frame_width, config.frame_height

                    # Convert coordinates to Manim coordinates
                    x1_manim = (x1 - canvas_width / 2) * (manim_width / canvas_width)
                    y1_manim = (canvas_height / 2 - y1) * (manim_height / canvas_height)
                    x2_manim = (x2 - canvas_width / 2) * (manim_width / canvas_width)
                    y2_manim = (canvas_height / 2 - y2) * (manim_height / canvas_height)

                    # Create Line in Manim
                    shape = Line(start=[x1_manim, y1_manim, 0], end=[x2_manim, y2_manim, 0], color=Shape_colore_Bor[i])

                    i += 1

                elif shape_type == "curve":
                    def calculate_peak(x1, y1, x2, y2, x3, y3):
                        """Calculate the peak of the quadratic Bézier curve if possible."""
                        denominator = x3 - 2 * x2 + x1
                        if denominator != 0:
                            t = (x2 - x1) / denominator
                            x_peak = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * x2 + t ** 2 * x3
                            y_peak = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * y2 + t ** 2 * y3
                            return x_peak, y_peak
                        else:
                            # Handle the case where the curve is collinear
                            # Here, you can choose a default or approximate peak
                            # For example, use the midpoint of the control points
                            x_peak = (x1 + x3) / 2
                            y_peak = (y1 + y3) / 2
                            return x_peak, y_peak

                    # print(";;;;;;;;")
                    # Extract coordinates for the control points of the curve
                    x1, y1, x2, y2, x3, y3 = Shape_coords[i]

                    canvas_width, canvas_height = get_canvas_size(canvas)
                    manim_width, manim_height = config.frame_width, config.frame_height

                    # Convert coordinates to Manim coordinates
                    x1_manim = (x1 - canvas_width / 2) * (manim_width / canvas_width)
                    y1_manim = (canvas_height / 2 - y1) * (manim_height / canvas_height)
                    x2_manim = (x2 - canvas_width / 2) * (manim_width / canvas_width)
                    y2_manim = (canvas_height / 2 - y2) * (manim_height / canvas_height)
                    x3_manim = (x3 - canvas_width / 2) * (manim_width / canvas_width)
                    y3_manim = (canvas_height / 2 - y3) * (manim_height / canvas_height)

                    # Calculate the peak of the quadratic Bézier curve
                    x_peak, y_peak = calculate_peak(x1, y1, x2, y2, x3, y3)

                    # Convert peak coordinates to Manim coordinates
                    x_peak_manim = (x_peak - canvas_width / 2) * (manim_width / canvas_width)
                    y_peak_manim = (canvas_height / 2 - y_peak) * (manim_height / canvas_height)

                    # Create a VMobject for the quadratic Bézier curve
                    curve = VMobject()
                    curve.set_points_as_corners(
                        [[x1_manim, y1_manim, 0], [x2_manim, y2_manim, 0], [x3_manim, y3_manim, 0]])
                    curve.make_smooth()
                    curve.set_color(Shape_colore_Bor[i])
                    shape = curve

                    # Optional: Add a marker for the peak
                    # peak_dot = Dot([x_peak_manim, y_peak_manim, 0], color=RED)
                    # scene.add(peak_dot)

                    i += 1


                shapes.append(shape)
                print(";l;l;l;l;l;")
                print(shapes)

            # i=0
            # # Animation sequence for each shape
            # for shape in shapes:
            #
            #     # Calculate start_time for the shape
            #     wait_time = Shape_start_time[i] - Shape_start_time[0] if i > 0 else Shape_start_time[i]
            #
            #     self.wait(wait_time)
            #     if Shape_anime[i] == "Create":
            #         self.play(Create(shape), run_time=Shape_speed[i])
            #     elif Shape_anime[i] == "Uncreate":
            #         self.play(Uncreate(shape), run_time=Shape_speed[i])
            #     elif Shape_anime[i] == "Grow":
            #         self.play(GrowFromCenter(shape), run_time=Shape_speed[i])
            #     elif Shape_anime[i] == "FadeIn":
            #         self.play(FadeIn(shape), run_time=Shape_speed[i])
            #     elif Shape_anime[i] == "FadeOut":
            #         self.play(FadeOut(shape), run_time=Shape_speed[i])
            #     i=i+1
            # Group shapes by their start times




            start_time_groups = {}

            for i, start_time in enumerate(Shape_start_time):
                if Shape_anime[i]:
                    if start_time not in start_time_groups:
                        start_time_groups[start_time] = []
                    start_time_groups[start_time].append(i)

            # Sort start times
            sorted_start_times = sorted(start_time_groups.keys())
            print(sorted_start_times)
            # Animation sequence for each group of shapes
            for idx, start_time in enumerate(sorted_start_times):
                j=0
                # print("9999")
                # print(Shape_anime[i])
                print("Shape_anime[idx]")
                print(Shape_anime[idx])
                if Shape_anime[idx]:
                    wait_time = start_time - sorted_start_times[idx - 1] if idx > 0 else start_time
                    self.wait(wait_time)
                    # Play animations for shapes in the same start time group
                    animations_arr = []
                    print("start_time_groups[start_time]")
                    print(start_time_groups[start_time])
                    print("[start_time]")
                    print([start_time])
                    for i in start_time_groups[start_time]:
                        print("Shape_anime[i] ")
                        print(Shape_anime[i] )
                        print(i)
                        print(len(target_shapes))
                        if Shape_anime[i] == "Create":
                            animations_arr.append(Create(shapes[i], run_time=Shape_speed[i]))

                        elif Shape_anime[i] == "Transform" and j<len(target_shapes):
                            print("im here")
                            print(shapes)
                            print(i)
                            print(target_shapes)
                            animations_arr.append(Transform(shapes[i], target_shapes[j], run_time=Shape_speed[i]))
                            j=j+1

                        elif Shape_anime[i] == "Fade In":
                            # elif Shape_anime[i] == "FadeIn":
                            animations_arr.append(FadeIn(shapes[i], run_time=Shape_speed[i]))
                        # elif Shape_anime[i] == "FadeOut":
                        #     animations_arr.append(FadeOut(shapes[i], run_time=Shape_speed[i]))

                    # Play all animations for the current start time concurrently


                    # self.play(*animations_arr)
                    print("Animations to play at time", start_time, ":", animations_arr)
                    if animations_arr:
                        self.play(*animations_arr)
                    else:
                        print("No animations to play at this start time.")
            # # Handle end times for shapes
            # for i, end_time in enumerate(Shape_end_time):
            #     wait_time = end_time - Shape_start_time[i]
            #     shape_speed = Shape_end_speed[i]
            #     self.wait(wait_time/shape_speed)
            #     self.play(FadeOut(shapes[i]))

            # Handle end times for shapes
            for i, end_time in enumerate(Shape_end_time):
                if Shape_end_anime[i]:
                    wait_time = end_time - Shape_start_time[i]
                    shape_speed = Shape_end_speed[i]
                    self.wait(wait_time / shape_speed)

                    # Determine which end animation to apply
                    end_animation_arr = []
                    if Shape_end_anime[i] == "Fade Out":
                        end_animation_arr.append(FadeOut(shapes[i], run_time=shape_speed))
                    elif Shape_end_anime[i] == "Uncreate":
                        end_animation_arr.append(Uncreate(shapes[i], run_time=shape_speed))

                    # Play the end animation for the shape
                    # self.play(*end_animation_arr)
                    print("End animations for shape", i, ":", end_animation_arr)
                    if end_animation_arr:
                        self.play(*end_animation_arr)
                    else:
                        print("No end animations for shape", i)

    if __name__ == "__main__":
        # Configure Manim to open the file after rendering
        config.video_dir = "./"
        config.open_file = False  # Manim will not open the video file automatically

        # Render the scene
        scene = ShapeAnimation()
        scene.render()

        # Construct the path to the rendered video file
        video_file = "C:/Users/esraa/PycharmProjects/Manim_Project/FINALLL/ShapeAnimation.mp4"

        # Check if the video file exists
        if os.path.isfile(video_file):
            # Play the video file
            play_video(video_file)
        else:
            print(f"Video file not found: {video_file}")


#####################################Animation section###########################

# Create the main window
root = tk.Tk()
root.title("Manim")

# Create frame for buttons
button_frame = tk.Frame(root, bg='black', relief=tk.RAISED)
button_frame.pack(side=tk.LEFT, fill=tk.Y)


# Create a dropdown menu for shapes
# Load shape icons
circle_icon = PhotoImage(file="circle.png")
square_icon = PhotoImage(file="square.png")
triangle_icon = PhotoImage(file="triangle.png")
line_icon = PhotoImage(file="line.png")
curve_icon = PhotoImage(file="curve.png")
# cancel_icon = PhotoImage(file= "cancel.png")

# Create a dropdown menu for shapes
shape_menu = tk.Menu(button_frame, tearoff=0)
# Add shape options with icons
shape_menu.add_radiobutton(label="Circle", image=circle_icon, compound=tk.LEFT, command=lambda: select_shape("circle"))
shape_menu.add_radiobutton(label="Square", image=square_icon, compound=tk.LEFT, command=lambda: select_shape("square"))
shape_menu.add_radiobutton(label="Triangle", image=triangle_icon, compound=tk.LEFT, command=lambda: select_shape("triangle"))
shape_menu.add_radiobutton(label="Line", image=line_icon, compound=tk.LEFT, command=lambda: select_shape("line"))
shape_menu.add_radiobutton(label="Curve", image=curve_icon, compound=tk.LEFT, command=lambda: select_shape("curve"))

# shape_menu.add_command(label="Circle", command=lambda: select_shape("circle"))
# shape_menu.add_command(label="Square", command=lambda: select_shape("square"))
# shape_menu.add_command(label="Triangle", command=lambda: select_shape("triangle"))
# shape_menu.add_command(label="Line", command=lambda: select_shape("line"))
# shape_menu.add_command(label="Curve", command=lambda: select_shape("curve"))
shape_menu.add_separator()
# shape_menu.add_command(label="Add", command=enable_add_mode)
# shape_menu.add_command(label="Cancel",image=cancel_icon, compound=tk.LEFT, command=cancel_add_mode)


# shape_button = tk.Button(button_frame, text="Shapes", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
# shape_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
# Create a button to open the shape window

# Load the icon image
shapes_icon = PhotoImage(file="shapes.png")
# Create a button to open the shape window
shape_button = tk.Button(button_frame, image=shapes_icon, relief=tk.RAISED, bd=0, padx=10, pady=5,  bg='black', command=open_shape_window)
shape_button.pack(side=tk.TOP, padx=5, pady=10)  # Adjusted pady to 5 for compactness

shape_button.config(command=lambda: shape_menu.post(shape_button.winfo_rootx(), shape_button.winfo_rooty() + shape_button.winfo_height()))


border_icon = PhotoImage(file="border_color.png")
border_color_button= tk.Button(button_frame,image=border_icon, text="Border", relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black', command=change_color)
border_color_button.pack(side=tk.TOP, padx=5, pady=10)
fill_icon = PhotoImage(file="fill_color.png")
fill_color_button= tk.Button(button_frame,image=fill_icon, text="fill", relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black', command=change_fill_color)
fill_color_button.pack(side=tk.TOP, padx=5, pady=10)
# # Modify the edit button to show the menu
# edit_button = tk.Button(button_frame, text="Edit", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
# edit_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
# edit_button.config(command=lambda: edit_menu.post(edit_button.winfo_rootx(), edit_button.winfo_rooty() + edit_button.winfo_height()))

###%%%%%%%%%%%%% text %%%%%%%%%%%%%%%%%%%%
# # Create frame for top buttons (Add Text and Edit Text)
top_button_frame = tk.Frame(root, bg='black')
top_button_frame.pack(side=tk.TOP, fill=tk.X)


# undoo_icon = tk.PhotoImage(file='undo.png')
# redoo_icon = tk.PhotoImage(file='redo.png')
# undo_button = tk.Button(top_button_frame, image=undoo_icon, text="Undo", command=undo, relief=tk.RAISED, bd=0, padx=5, pady=5, bg='black')
# undo_button.pack(side=tk.LEFT, padx=10, pady=10) # Increased pady to 10
#
# redo_button = tk.Button(top_button_frame, image=redoo_icon, text="Redo", command=redo, relief=tk.RAISED, bd=0, padx=5, pady=5, bg='black')
# redo_button.pack(side=tk.LEFT, padx=5, pady=10)  # Increased pady to 10

# Create the Add Text button
# Load icon image
text_icon = tk.PhotoImage(file='text.png')
add_text_button = tk.Button(top_button_frame, image=text_icon, command=add_text, relief=tk.RAISED, bd=0, padx=5, pady=5, bg='black')
add_text_button.image = text_icon  # Keep a reference to the image
add_text_button.pack(side=tk.LEFT, padx=5, pady=5)

edit_icon = tk.PhotoImage(file="edit_text.png")

edit_text_button = tk.Button(top_button_frame, image=edit_icon, command=edit_text, relief=tk.RAISED, bd=0, padx=5, pady=5, bg='black')
edit_text_button.image = edit_icon  # Keep a reference to the image
edit_text_button.pack(side=tk.LEFT, padx=5, pady=5)


clear_button = tk.Button(top_button_frame,text="clear all", command=clear_current_page, relief=tk.RAISED, bd=0, padx=5, pady=5, bg='gray', fg='black')
clear_button.pack(side=tk.LEFT, padx=5, pady=5)


delete_button = tk.Button(top_button_frame, text="Delete shape", command=delete_shape,relief=tk.RAISED, bd=0, padx=5, pady=5, bg='gray', fg='black')
delete_button.pack(side=tk.LEFT, padx=10, pady=10)


###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
###################################FOR Pages ####################
add_page_ic = PhotoImage(file="add_page.png")
add_page_button = tk.Button(button_frame,image=add_page_ic, text="Add Page", command=add_page, relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black')
add_page_button.pack(side=tk.TOP, padx=5, pady=(10, 5))   # Increased pady to 10

delete_page_ic = PhotoImage(file="delete_page.png")
delete_page_button = tk.Button(button_frame,image=delete_page_ic, text="Delete Page", command=delete_page, relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black')
delete_page_button.pack(side=tk.TOP, padx=5, pady=(5, 10))  # Increased pady to 10

###################################FOR ANIMATION####################
# Create a frame on the right side
right_button_frame = tk.Frame(root, bg='black', relief=tk.RAISED)
right_button_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Object button and menu
object_button = tk.Button(right_button_frame, text="Choose Object", relief=tk.RAISED, bd=0, padx=5, pady=5, fg='white', bg='black')
object_button.pack(side=tk.TOP, padx=3, pady=3)
object_menu = tk.Menu(root, tearoff=0)

# Label for "START FEATURES"
start_features_label = tk.Label(right_button_frame, text="Animation Features", font=('Helvetica', 10, 'bold'), fg='purple', bg='black')
start_features_label.pack(side=tk.TOP, padx=5, pady=5)

#frame
features_frame = tk.Frame(right_button_frame, bg='black', relief=tk.RAISED, bd=2, highlightbackground='purple', highlightcolor='purple', highlightthickness=2)
features_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

#$$$
# Add an "Animations" button inside the features frame
# animation_button = tk.Button(features_frame, text="Animations", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
# animation_button.pack(side=tk.TOP, padx=5, pady=10)

# Define animation options
animation_options = ["Create","Transform","Fade In"]

# Create Type button (initially disabled)
type_button = tk.Button(features_frame, text="Choose animation",bd=0, relief=tk.RAISED, padx=5, pady=5, bg='black',fg='white')
type_button.pack(side=tk.TOP, padx=5, pady=5)

# Create menu for Type button
# type_menu = tk.Menu(root, tearoff=0)
#$$$

# Create a frame to hold the speed label, entry, and buttons
object_anim_frame = tk.Frame(features_frame, bg='black')

# Add speed label
speed_label_obj = tk.Label(object_anim_frame, text="Object-speed:", font=('Helvetica', 11), fg='white', bg='black')
speed_label_obj.pack(side=tk.LEFT)

# Add speed entry field with customized colors
speed_entry_obj = tk.Entry(object_anim_frame, width=5, font=('Helvetica', 11), fg='white', bg='black')
speed_entry_obj.insert(0, "0")  # Initial value
speed_entry_obj.pack(side=tk.LEFT)

# Add plus button
plus_button_speed_obj = tk.Button(object_anim_frame, text="+", command=increment_speed_obj, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
plus_button_speed_obj.pack(side=tk.LEFT, padx=5)

# Add minus button
minus_button_speed_obj = tk.Button(object_anim_frame, text="-", command=decrement_speed_obj, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
minus_button_speed_obj.pack(side=tk.LEFT, padx=5)

# Pack the speed frame under the Type button
object_anim_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create a frame to hold the start time label, entry, and buttons
object_anim_frame_tim = tk.Frame(features_frame, bg='black')

# Add start time label
time_label_obj = tk.Label(object_anim_frame_tim, text="Start-time:", font=('Helvetica', 11), fg='white', bg='black')
time_label_obj.pack(side=tk.LEFT)

# Add start time entry field with customized colors
time_entry_obj = tk.Entry(object_anim_frame_tim, width=5, font=('Helvetica', 11), fg='white', bg='black')
time_entry_obj.insert(0, "0")  # Initial value
time_entry_obj.pack(side=tk.LEFT)

# Add plus button
plus_button_time_obj = tk.Button(object_anim_frame_tim, text="+", command=increment_time_obj, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
plus_button_time_obj.pack(side=tk.LEFT, padx=5)

# Add minus button
minus_button_time_obj = tk.Button(object_anim_frame_tim, text="-", command=decrement_time_obj, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
minus_button_time_obj.pack(side=tk.LEFT, padx=5)

# Pack the start time frame under the speed frame
object_anim_frame_tim.pack(side=tk.TOP, padx=5, pady=5)

# Configure button commands
# animation_button.config(command=open_animation_menu)
type_button.config(command=open_type_menu)
object_button.config(command=open_object_menu)

#######
# Label for "END FEATURES"
def toggle_end_features():
    global selected_shape
    if end_features_var.get() == 1:
        # Enable all end features widgets
        end_type_button.config(state=tk.NORMAL)
        end_speed_entry_obj.config(state=tk.NORMAL)
        end_plus_button_speed_obj.config(state=tk.NORMAL)
        end_minus_button_speed_obj.config(state=tk.NORMAL)
        end_time_entry_obj.config(state=tk.NORMAL)
        end_plus_button_time_obj.config(state=tk.NORMAL)
        end_minus_button_time_obj.config(state=tk.NORMAL)
    else:
        selected_shape['end_animation']= None
        # Disable all end features widgets
        end_type_button.config(state=tk.DISABLED)
        end_speed_entry_obj.config(state=tk.DISABLED)
        end_plus_button_speed_obj.config(state=tk.DISABLED)
        end_minus_button_speed_obj.config(state=tk.DISABLED)
        end_time_entry_obj.config(state=tk.DISABLED)
        end_plus_button_time_obj.config(state=tk.DISABLED)
        end_minus_button_time_obj.config(state=tk.DISABLED)

# Checkbutton variable
end_features_var = tk.IntVar()

# "Do you want end features?" checkbutton
toggle_checkbutton = tk.Checkbutton(right_button_frame, text="Should the shape disappear later?", variable=end_features_var, command=toggle_end_features, fg='white', bg='black', selectcolor='purple', font=('Helvetica', 10))
toggle_checkbutton.pack(side=tk.TOP, padx=5, pady=5)

end_features_label = tk.Label(right_button_frame, text="Disappearance Features", font=('Helvetica', 10, 'bold'), fg='purple', bg='black')
end_features_label.pack(side=tk.TOP, padx=5, pady=5)

#frame
end_features_frame = tk.Frame(right_button_frame, bg='black', relief=tk.RAISED, bd=2, highlightbackground='purple', highlightcolor='purple', highlightthickness=2)
end_features_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)


# Add an "Animations" button inside the features frame
# end_animation_button = tk.Button(end_features_frame, text="Animations", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
# end_animation_button.pack(side=tk.TOP, padx=5, pady=10)

# Define animation options
end_animation_options = ["Fade Out","Uncreate"]

# Create Type button (initially disabled)
end_type_button = tk.Button(end_features_frame, text="Choose animation", relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black',fg='white',state=tk.DISABLED)
end_type_button.pack(side=tk.TOP, padx=5, pady=5)

# Create menu for Type button
# type_menu = tk.Menu(root, tearoff=0)

# Create a frame to hold the speed label, entry, and buttons
end_object_anim_frame = tk.Frame(end_features_frame, bg='black')

# Add speed label
end_speed_label_obj = tk.Label(end_object_anim_frame, text="Object-speed:", font=('Helvetica', 11), fg='white', bg='black')
end_speed_label_obj.pack(side=tk.LEFT)

# Add speed entry field with customized colors
end_speed_entry_obj = tk.Entry(end_object_anim_frame, width=5, font=('Helvetica', 11), fg='white', bg='black', state=tk.DISABLED)
end_speed_entry_obj.insert(0, "0")  # Initial value
end_speed_entry_obj.pack(side=tk.LEFT)

# Add plus button
end_plus_button_speed_obj = tk.Button(end_object_anim_frame, text="+", command=increment_speed_obj_end, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
end_plus_button_speed_obj.pack(side=tk.LEFT, padx=5)

# Add minus button
end_minus_button_speed_obj = tk.Button(end_object_anim_frame, text="-", command=decrement_speed_obj_end, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
end_minus_button_speed_obj.pack(side=tk.LEFT, padx=5)

# Pack the speed frame under the Type button
end_object_anim_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create a frame to hold the start time label, entry, and buttons
end_object_anim_frame_tim = tk.Frame(end_features_frame, bg='black')

# Add start time label
end_time_label_obj = tk.Label(end_object_anim_frame_tim, text="End-time:", font=('Helvetica', 11), fg='white', bg='black')
end_time_label_obj.pack(side=tk.LEFT)

# Add start time entry field with customized colors
end_time_entry_obj = tk.Entry(end_object_anim_frame_tim, width=5, font=('Helvetica', 11), fg='white', bg='black', state=tk.DISABLED)
end_time_entry_obj.insert(0, "0")  # Initial value
end_time_entry_obj.pack(side=tk.LEFT)

# Add plus button
end_plus_button_time_obj = tk.Button(end_object_anim_frame_tim, text="+", command=increment_time_obj_end, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
end_plus_button_time_obj.pack(side=tk.LEFT, padx=5)

# Add minus button
end_minus_button_time_obj = tk.Button(end_object_anim_frame_tim, text="-", command=decrement_time_obj_end, fg='white', bg='black', font=('Helvetica', 11), bd=0, state=tk.DISABLED)
end_minus_button_time_obj.pack(side=tk.LEFT, padx=5)

# Pack the start time frame under the speed frame
end_object_anim_frame_tim.pack(side=tk.TOP, padx=5, pady=5)

# Configure button commands
# end_animation_button.config(command=open_animation_menu)
end_type_button.config(command=end_open_type_menu)
######
add_button = tk.Button(right_button_frame, text="Add to video", command=show_add_button, relief=tk.RAISED, bd=0, padx=5, pady=5,fg='white',font=("Helvetica", 11), bg='black')
add_button.pack(side=tk.TOP, padx=5, pady=5)  # Increased pady to 10

add_button.config(command=show_add_button)


video_button = tk.Button(right_button_frame, text="Watch the video", relief=tk.RAISED, bd=0, padx=5, pady=5,fg='white',font=("Helvetica", 11), bg='black')
video_button.pack(side=tk.TOP, padx=5, pady=5)
video_button.config(command=create_animation)
############################################
# Create canvas for drawing shapes
canvas = tk.Canvas(root, width=600, height=400, bg='white', borderwidth=2, relief=tk.SUNKEN)
canvas.pack(fill=tk.BOTH, expand=True)

# Initialize empty drag data
canvas._drag_data = {"x": 0, "y": 0, "shape_id": None, "dot_id": None}

# Frame to contain the navigation buttons and page label
button_frame_p = tk.Frame(root, bg='black')
button_frame_p.pack(fill=tk.X)

left_arrow = PhotoImage(file="left_arrow.png")
right_arrow = PhotoImage(file="right_arrow.png")
# Previous page button
# Previous page button
prev_page_button = tk.Button(button_frame_p, image=left_arrow, text="Previous Page", command=previous_page, relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black')
prev_page_button.pack(side=tk.LEFT, padx=5, pady=10)

# Frame for page label to center it
label_frame = tk.Frame(button_frame_p, bg='black')
label_frame.pack(side=tk.LEFT, expand=True)

# Page label
page_label = tk.Label(label_frame, text=f" Page: {current_page}", bg='black', fg='white', font=("Arial", 14))
page_label.pack(expand=True)

# Next page button
next_page_button = tk.Button(button_frame_p, image=right_arrow, text="Next Page", command=next_page, relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black')
next_page_button.pack(side=tk.RIGHT, padx=5, pady=10)


canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<B1-Motion>", draw_shape)
canvas.bind("<ButtonRelease-1>", end_draw)
canvas.bind("<Button-3>", canvas_clicked)  # Right-click to select for resizing
canvas.bind("<B3-Motion>", resize_shape)     # Right-click drag to resize
canvas.bind("<ButtonRelease-3>", stop_resizing)

root.mainloop()

