import tkinter as tk
from tkinter import colorchooser, Toplevel, messagebox, ttk,font
from tkinter import PhotoImage, Menu
from tkinter import Canvas, Entry, Toplevel, Label, OptionMenu, StringVar
from manim import *

selected_text=None
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
max_page=1
# Declare global variables for UI elements
shape_window = None
width_scale = None
height_scale = None
# Global variable for animation selection
selected_animation = None
selected_type = None
speed_value = 0
start_time_value = 0
add_shape_mode = True  # To enable drawing mode after clicking "Add"
drawing_mode = True

text_mode = False
text_rectangle = None
text_entry = None
text_entry_id = None
selected_text_id = None
adding_text = False
selected_color = None


undo_stack = []
redo_stack = []

all_of_drawings = []
sorted_drawings = []

page_with_time = [(1, None)]

########################################DRAWING SECTION##############################

################################################ Text functions: #########################################
#((((((((((((((((((((((((((((((((((((((((((((((( TEXT TEXT TEXT  )))))))))))))))))))))))))))))))))))))))))
#
# def enable_add_text_mode():
#     print("enable add text mode to add text")
#     global adding_text, drawing_mode
#     adding_text = True
#     drawing_mode = False
#     canvas.bind("<Button-1>", add_text)
#
# def add_text(event):
#     global adding_text, text_entry, text_entry_id
#     if not adding_text:
#         return
#     print("no we are in add text function itself")
#     x, y = event.x, event.y
#     text_entry = tk.Entry(root, width=20)
#     text_entry_id = canvas.create_window(x, y, window=text_entry, anchor='nw')
#     text_entry.focus_set()
#     # Bind canvas click event to select text
#     canvas.bind("<Button-1>", select_text)
#     text_entry.bind('<Return>', save_text)
#     adding_text = False  # Disable text adding mode after placing the entry
#
# def save_text():
#     global text_entry, text_entry_id
#     text = text_entry.get()
#     if text:
#         canvas.create_text(canvas.coords(text_entry_id), text=text, anchor='nw', tags="text")
#         print("now we are in save text function")
#     canvas.delete(text_entry_id)
#     text_entry.destroy()
#
# def select_text():
#     print("now we are in select text function without checking any thing")
#     global selected_text_id
#     item = canvas.find_withtag("current")
#     if item and "text" in canvas.gettags(item[0]):
#         if selected_text_id:
#             print("selected_text_id is: ")
#             print(selected_text_id)
#             canvas.itemconfig(selected_text_id, outline="")
#         selected_text_id = item[0]
#         print("failed if, selected_text_id is: ")
#         print(selected_text_id)
#
#         canvas.itemconfig(selected_text_id, outline="blue")
#         print("now we are in the end of select text function")
#         messagebox.showinfo("Success", "Text selected successfully!")
#
# # def select_text(event):
# #     global selected_text, drawing_mode
# #     if drawing_mode:
# #         item = canvas.find_closest(event.x, event.y)
# #         tags = canvas.gettags(item)
# #         if 'window' in tags:
# #             text_widget = canvas.itemcget(item, 'window')
# #             selected_text = (item, text_widget)
# #             drawing_mode = False  # Switch to text selection mode
# #     else:
# #         edit_text()
#
#
#
# # def change_text_color():
# #     print("now we are in change text color")
# #     global selected_text_id
# #     if selected_text_id:
# #         color = colorchooser.askcolor()[1]  # Prompt user to choose color
# #         if color:
# #             canvas.itemconfigure(selected_text_id, fill=color)
#
# def edit_text():
#     print("edit text function")
#     global selected_text
#     if selected_text:
#         canvas_id, text_entry = selected_text
#
#         # Retrieve current text and properties
#         current_text = text_entry.get("1.0", tk.END)
#         current_font = text_entry.cget('font')
#         current_color = text_entry.cget('foreground')
#
#         # Create a popup window for editing text properties
#         edit_window = tk.Toplevel(root)
#         edit_window.title("Edit Text Properties")
#
#         # Font family selection
#         font_label = tk.Label(edit_window, text="Font Family:")
#         font_label.grid(row=0, column=0, padx=10, pady=5)
#
#         font_family = font.Font(font=current_font).actual()['family']
#         font_var = tk.StringVar(value=font_family)
#         font_combo = tk.OptionMenu(edit_window, font_var, *font.families())
#         font_combo.grid(row=0, column=1, padx=10, pady=5)
#
#         # Font size selection
#         size_label = tk.Label(edit_window, text="Font Size:")
#         size_label.grid(row=1, column=0, padx=10, pady=5)
#
#         font_size = font.Font(font=current_font).actual()['size']
#         size_var = tk.IntVar(value=font_size)
#         size_spinbox = tk.Spinbox(edit_window, from_=8, to=72, textvariable=size_var)
#         size_spinbox.grid(row=1, column=1, padx=10, pady=5)
#
#         # Font color selection
#         def choose_color():
#             color = colorchooser.askcolor(initialcolor=current_color)[1]
#             if color:
#                 text_entry.config(foreground=color)
#
#         color_button = tk.Button(edit_window, text="Choose Color", command=choose_color)
#         color_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
#
#         # Font style selection (Bold, Italic, Underline)
#         bold_var = tk.BooleanVar(value='bold' in current_font)
#         bold_check = tk.Checkbutton(edit_window, text="Bold", variable=bold_var)
#         bold_check.grid(row=3, column=0, padx=10, pady=5)
#
#         italic_var = tk.BooleanVar(value='italic' in current_font)
#         italic_check = tk.Checkbutton(edit_window, text="Italic", variable=italic_var)
#         italic_check.grid(row=3, column=1, padx=10, pady=5)
#
#         underline_var = tk.BooleanVar(value='underline' in current_font)
#         underline_check = tk.Checkbutton(edit_window, text="Underline", variable=underline_var)
#         underline_check.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
#
#         def apply_changes():
#             new_font = (font_var.get(), size_var.get())
#             if bold_var.get():
#                 new_font += ('bold',)
#             if italic_var.get():
#                 new_font += ('italic',)
#             if underline_var.get():
#                 new_font += ('underline',)
#
#             text_entry.config(font=new_font)
#
#             # Update text on canvas
#             canvas.itemconfig(canvas_id, text=text_entry.get("1.0", tk.END))
#
#             edit_window.destroy()
#
#         # Apply button
#         apply_button = tk.Button(edit_window, text="Apply Changes", command=apply_changes)
#         apply_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
#
# # def change_text_font(font_name):
# #     print("now we are in change text font")
# #     global selected_text_id
# #     if selected_text_id:
# #         current_font = tkfont.Font(font=canvas.itemcget(selected_text_id, "font"))
# #         canvas.itemconfigure(selected_text_id, font=(font_name, current_font.actual()["size"]))
# #
# # def change_text_size(size):
# #     print("now we are in change text size")
# #     global selected_text_id
# #     if selected_text_id:
# #         current_font = tkfont.Font(font=canvas.itemcget(selected_text_id, "font"))
# #         canvas.itemconfigure(selected_text_id, font=(current_font.actual()["family"], size))
# #
# # def toggle_text_bold():
# #     global selected_text_id
# #     print("now we are in toggle text bold")
# #     if selected_text_id:
# #         current_font = tkfont.Font(font=canvas.itemcget(selected_text_id, "font"))
# #         weight = "bold" if "normal" in current_font.actual()["weight"] else "normal"
# #         canvas.itemconfigure(selected_text_id, font=(current_font.actual()["family"], current_font.actual()["size"], weight))
# #
# # def toggle_text_italic():
# #     print("now we are in toggle text italic")
# #     global selected_text_id
# #     if selected_text_id:
# #         current_font = tkfont.Font(font=canvas.itemcget(selected_text_id, "font"))
# #         slant = "italic" if "roman" in current_font.actual()["slant"] else "roman"
# #         canvas.itemconfigure(selected_text_id, font=(current_font.actual()["family"], current_font.actual()["size"], slant))
# #
# # def toggle_text_underline():
# #     print("now we are in toggle text underline")
# #     global selected_text_id
# #     if selected_text_id:
# #         current_font = tkfont.Font(font=canvas.itemcget(selected_text_id, "font"))
# #         underline = not current_font.actual()["underline"]
# #         canvas.itemconfigure(selected_text_id, font=(current_font.actual()["family"], current_font.actual()["size"], "underline" if underline else "normal"))
# #
# # def edit_text_properties():
# #     print("now we are in edit text properties function to see the edit options")
# #     global selected_text_id
# #     print("selected_text_id in edit text properties function is:")
# #     print(selected_text_id)
# #     if selected_text_id:
# #         edit_menu = tk.Menu(root, tearoff=0)
# #         edit_menu.add_command(label="Font", command=lambda: change_text_font("Helvetica"))
# #         edit_menu.add_command(label="Size", command=lambda: change_text_size(16))
# #         edit_menu.add_command(label="Color", command=change_text_color)
# #         edit_menu.add_command(label="Bold", command=toggle_text_bold)
# #         edit_menu.add_command(label="Italic", command=toggle_text_italic)
# #         edit_menu.add_command(label="Underline", command=toggle_text_underline)
# #         edit_menu.post(root.winfo_pointerx(), root.winfo_pointery())
# #     else:
# #         messagebox.showerror("Error", "Please select a text to edit!")
# # def canvas_click():
# #     global selected_text
# #     if selected_text:
# #         canvas_id, text_entry = selected_text
# #         text_entry.destroy()  # Destroy the text entry widget
# #         canvas.itemconfig(canvas_id, text=text_entry.get("1.0", tk.END))  # Update text on canvas
# #         selected_text = None  # Reset selected_text after editing
#
#
#
# # def canvas_click():
# #     print("now we are in canvas click function, we are calling to select text")
# #     select_text()
# #     print("we are in canvas select and returned from select text")
# #     edit_text()
# #     print("we are in canvas click function after we called edit text function and return from it ")
# #

def start_drag(event, canvas_id):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def drag_text(event, canvas_id):
    global start_x, start_y

    # Calculate the movement
    dx, dy = event.x - start_x, event.y - start_y

    # Move the text entry
    canvas.move(canvas_id, dx, dy)

    # Update start position
    start_x, start_y = event.x, event.y

def end_drag(event, canvas_id):
    pass  # Optional: Add any final actions needed when dragging ends

def add_text():
    global selected_text, drawing_mode

    # if not drawing_mode:
    #     return

    text_entry = tk.Text(canvas, wrap=tk.WORD, height=2, width=20)
    canvas_id = canvas.create_window(300, 150, window=text_entry, anchor='center')
    text_entry.focus_set()  # Set focus to the text entry
    selected_text = (canvas_id, text_entry)

    # Bind events for dragging the text entry
    text_entry.bind("<ButtonPress-1>", lambda event: start_drag(event, canvas_id))
    text_entry.bind("<B1-Motion>", lambda event: drag_text(event, canvas_id))
    text_entry.bind("<ButtonRelease-1>", lambda event: end_drag(event, canvas_id))

    drawing_mode = False  # Switch to text input mode

def edit_text():
    global selected_text, selected_color
    if selected_text:
        canvas_id, text_entry = selected_text

        # Retrieve current text and properties
        current_text = text_entry.get("1.0", tk.END)
        current_font = text_entry.cget('font')
        current_color = text_entry.cget('foreground')

        # Create a popup window for editing text properties
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Text Properties")

        # Font family selection
        font_label = tk.Label(edit_window, text="Font Family:")
        font_label.grid(row=0, column=0, padx=10, pady=5)

        font_family = font.Font(font=current_font).actual()['family']
        font_var = tk.StringVar(value=font_family)
        font_combo = tk.OptionMenu(edit_window, font_var, *font.families())
        font_combo.grid(row=0, column=1, padx=10, pady=5)

        # Font size selection
        size_label = tk.Label(edit_window, text="Font Size:")
        size_label.grid(row=1, column=0, padx=10, pady=5)

        font_size = font.Font(font=current_font).actual()['size']
        size_var = tk.IntVar(value=font_size)
        size_spinbox = tk.Spinbox(edit_window, from_=8, to=72, textvariable=size_var)
        size_spinbox.grid(row=1, column=1, padx=10, pady=5)

        # Font color selection
        def choose_color():
            color = colorchooser.askcolor(initialcolor=current_color)[1]
            if color:
                selected_color = color
                text_entry.config(foreground=color)

        color_button = tk.Button(edit_window, text="Color", command=choose_color)
        color_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Font style selection (Bold, Italic, Underline)
        bold_var = tk.BooleanVar(value='bold' in current_font)
        bold_check = tk.Checkbutton(edit_window, text="Bold", variable=bold_var)
        bold_check.grid(row=3, column=0, padx=10, pady=5)

        italic_var = tk.BooleanVar(value='italic' in current_font)
        italic_check = tk.Checkbutton(edit_window, text="Italic", variable=italic_var)
        italic_check.grid(row=3, column=1, padx=10, pady=5)

        underline_var = tk.BooleanVar(value='underline' in current_font)
        underline_check = tk.Checkbutton(edit_window, text="Underline", variable=underline_var)
        underline_check.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        def apply_changes():
            new_font = (font_var.get(), size_var.get())
            if bold_var.get():
                new_font += ('bold',)
            if italic_var.get():
                new_font += ('italic',)
            if underline_var.get():
                new_font += ('underline',)

            text_entry.config(font=new_font)

            if selected_color:
                text_entry.config(foreground=selected_color)
            edit_window.destroy()
            # Update text on canvas
            canvas.itemconfig(canvas_id, text=text_entry.get("1.0", tk.END))



        # Apply button
        apply_button = tk.Button(edit_window, text="Apply Changes", command=apply_changes)
        apply_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

def select_text(event):
    global selected_text, drawing_mode

    if drawing_mode:
        item = canvas.find_closest(event.x, event.y)
        tags = canvas.gettags(item)
        if 'text' in tags:
            text_widget = canvas.itemcget(item, 'window')
            selected_text = (item, text_widget)
            drawing_mode = False  # Switch to text selection mode
    else:
        edit_text()

def canvas_clicked(event):
    global selected_text

    if selected_text:
        canvas_id, text_entry = selected_text
        text_entry.destroy()
        canvas.itemconfig(canvas_id, text=text_entry.get("1.0", tk.END))
        selected_text = None


# Function to add text
# def add_text():
#     global selected_text, drawing_mode
#     if not drawing_mode:
#         return
#
#     text_entry = tk.Text(canvas, wrap=tk.WORD, height=2, width=20)
#     canvas_id = canvas.create_window(300, 150, window=text_entry, anchor='center')
#     text_entry.focus_set()  # Set focus to the text entry
#     selected_text = (canvas_id, text_entry)
#     drawing_mode = False  # Switch to text input mode
#
# # Function to edit text properties
#
# def edit_text():
#     global selected_text
#     if selected_text:
#         canvas_id, text_entry = selected_text
#
#         # Retrieve current text and properties
#         current_text = text_entry.get("1.0", tk.END)
#         current_font = text_entry.cget('font')
#         current_color = text_entry.cget('foreground')
#
#         # Create a popup window for editing text properties
#         edit_window = tk.Toplevel(root)
#         edit_window.title("Edit Text Properties")
#
#         # Font family selection
#         font_label = tk.Label(edit_window, text="Font Family:")
#         font_label.grid(row=0, column=0, padx=10, pady=5)
#
#         font_family = font.Font(font=current_font).actual()['family']
#         font_var = tk.StringVar(value=font_family)
#         font_combo = tk.OptionMenu(edit_window, font_var, *font.families())
#         font_combo.grid(row=0, column=1, padx=10, pady=5)
#
#         # Font size selection
#         size_label = tk.Label(edit_window, text="Font Size:")
#         size_label.grid(row=1, column=0, padx=10, pady=5)
#
#         font_size = font.Font(font=current_font).actual()['size']
#         size_var = tk.IntVar(value=font_size)
#         size_spinbox = tk.Spinbox(edit_window, from_=8, to=72, textvariable=size_var)
#         size_spinbox.grid(row=1, column=1, padx=10, pady=5)
#
#         # Font color selection
#         def choose_color():
#             color = colorchooser.askcolor(initialcolor=current_color)[1]
#             if color:
#                 text_entry.config(foreground=color)
#
#         color_button = tk.Button(edit_window, text="Color", command=choose_color)
#         color_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
#
#         # Font style selection (Bold, Italic, Underline)
#         bold_var = tk.BooleanVar(value='bold' in current_font)
#         bold_check = tk.Checkbutton(edit_window, text="Bold", variable=bold_var)
#         bold_check.grid(row=3, column=0, padx=10, pady=5)
#
#         italic_var = tk.BooleanVar(value='italic' in current_font)
#         italic_check = tk.Checkbutton(edit_window, text="Italic", variable=italic_var)
#         italic_check.grid(row=3, column=1, padx=10, pady=5)
#
#         underline_var = tk.BooleanVar(value='underline' in current_font)
#         underline_check = tk.Checkbutton(edit_window, text="Underline", variable=underline_var)
#         underline_check.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
#
#         def apply_changes():
#             new_font = (font_var.get(), size_var.get())
#             if bold_var.get():
#                 new_font += ('bold',)
#             if italic_var.get():
#                 new_font += ('italic',)
#             if underline_var.get():
#                 new_font += ('underline',)
#
#             text_entry.config(font=new_font)
#
#             # Update text on canvas
#             canvas.itemconfig(canvas_id, text=text_entry.get("1.0", tk.END))
#
#             edit_window.destroy()
#
#         # Apply button
#         apply_button = tk.Button(edit_window, text="Apply Changes", command=apply_changes)
#         apply_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
#
# # Function to handle canvas click for selecting text or other interactive elements
# def select_text(event):
#     global selected_text, drawing_mode
#     if drawing_mode:
#         item = canvas.find_closest(event.x, event.y)
#         tags = canvas.gettags(item)
#         if 'window' in tags:
#             text_widget = canvas.itemcget(item, 'window')
#             selected_text = (item, text_widget)
#             drawing_mode = False  # Switch to text selection mode
#     else:
#         edit_text()
#
#
# def canvas_clicked(event):
#     global selected_text
#     if selected_text:
#         canvas_id, text_entry = selected_text
#         text_entry.destroy()
#         canvas.itemconfig(canvas_id, text=text_entry.get("1.0", tk.END))
#         selected_text = None
###############################################################################################################
###############################################################################################################
#%%%%%%%%%%%%%%%%%%% shape functions ^^^^^^^^^
def select_shape(shape):
    global selected_shape
    selected_shape = shape
    ####ISRAA###
    if shape_window:
        shape_window.destroy()  # Close the shape selection window

def enable_add_mode():
    global add_shape_mode, shape_window
    if selected_shape:
        add_shape_mode = True
        shape_window.destroy()  # Close the shape selection window
    else:
        messagebox.showerror("Error", "Please choose a shape!")

def cancel_add_mode():
    global shape_window
    shape_window.destroy()


def open_shape_window():
    global shape_window, drawing_mode
    drawing_mode = True
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

    cancel_button = tk.Button(shape_window, text="Cancel", command=shape_window.destroy)
    cancel_button.pack(side=tk.TOP, padx=5, pady=5)

def start_draw(event):
    global drawing, start_x, start_y, shape_id
    if add_shape_mode and selected_shape:  # Start drawing only if a shape is selected and add mode is enabled
        drawing = True
        start_x = event.x
        start_y = event.y


def draw_shape(event):
    global drawing, shape_id, start_x, start_y

    if drawing and selected_shape:
        if shape_id:
            canvas.delete(shape_id)
        # Update start_x and start_y if they are None
        if start_x is None:
            start_x = event.x
        if start_y is None:
            start_y = event.y

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
        # Update current_shape and draw yellow dots around it
        current_shape = shape_id
        canvas.delete("yellow_dot")
        draw_yellow_dots(canvas, current_shape)

# Function to start edit mode and show edit options
def start_edit_mode():
    global edit_mode
    edit_mode = True
    # show_edit_options()

# Function to show edit options for current shape
def show_edit_options():
    global edit_mode
    if not edit_mode:
        messagebox.showinfo("Information", "Enable edit mode first.")
        return

    if current_shape:
        edit_menu.post(root.winfo_pointerx(), root.winfo_pointery())
    else:
        messagebox.showinfo("Information", "Please select a shape to edit.")

# def end_draw(event):
#     global drawing, shape_id, add_shape_mode
#     if drawing:
#         drawing = False
#         if shape_id:
#             canvas.tag_bind(shape_id, '<ButtonPress-1>', on_shape_click)
#             if edit_mode:
#                 canvas.tag_bind(shape_id, '<B1-Motion>', resize_shape)
#             else:
#                 canvas.tag_bind(shape_id, '<B1-Motion>', drag_shape)
#             undo_stack.append(shape_id)
#             save_shape_properties()
#         shape_id = None
#         redo_stack.clear()
#         # start_edit_mode()  # Automatically start edit mode after drawing a shape
#         add_shape_mode = False  # Disable add mode after drawing one shape
def end_draw(event):
    global drawing, shape_id, add_shape_mode, current_shape, object_text
    if drawing:
        drawing = False
        if shape_id:
            canvas.tag_bind(shape_id, '<ButtonPress-1>', on_shape_click)
            if edit_mode:
                canvas.tag_bind(shape_id, '<B1-Motion>', resize_shape)
            else:
                canvas.tag_bind(shape_id, '<B1-Motion>', drag_shape)
            undo_stack.append(shape_id)
            current_shape = shape_id  # Set current_shape to the newly drawn shape
            save_shape_properties()

        shape_id = None
        redo_stack.clear()
        update_object_menu()
        # start_edit_mode()  # Optionally start edit mode after drawing a shape
        add_shape_mode = False  # Disable add mode after drawing one shape

# def on_shape_click(event):
#     global current_shape, start_x, start_y
#     current_shape = canvas.find_closest(event.x, event.y)[0]
#     start_x = event.x
#     start_y = event.y
# Function to draw a shape with yellow dots around it
def draw_yellow_dots(canvas, shape_id):
    bbox = canvas.bbox(shape_id)
    x1, y1, x2, y2 = bbox

    if canvas.type(shape_id) == "oval":  # Circle
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        radius = (x2 - x1) / 2
        dots = [
            (cx + radius, cy),     # Right
            (cx - radius, cy),     # Left
            (cx, cy + radius),     # Bottom
            (cx, cy - radius)      # Top
        ]
    elif canvas.type(shape_id) == "rectangle":  # Square or Rectangle
        dots = [
            (x1 - 5, y1 - 5),      # Top-left corner
            (x2 + 5, y1 - 5),      # Top-right corner
            (x1 - 5, y2 + 5),      # Bottom-left corner
            (x2 + 5, y2 + 5)       # Bottom-right corner
        ]
    elif canvas.type(shape_id) == "polygon":  # Triangle or other polygons
        points = canvas.coords(shape_id)
        dots = [
            (points[0] - 5, points[1] - 5),    # First vertex
            (points[2] + 5, points[3] - 5),    # Second vertex
            ((points[0] + points[2]) / 2, points[3] + 5)   # Third vertex (middle)
        ]
    elif canvas.type(shape_id) == "line":  # Line or curve
        dots = [
            (x1, y1),       # Start point
            (x2, y2)        # End point
        ]
    else:
        return  # Return if the shape type is not recognized

    for dot in dots:
        canvas.create_oval(dot[0] - 2, dot[1] - 2, dot[0] + 2, dot[1] + 2, fill="yellow", tags="yellow_dot")


def on_shape_click(event):
    global current_shape, start_x, start_y
    current_shape = canvas.find_closest(event.x, event.y)[0]
    start_x = event.x
    start_y = event.y

    # Remove previous yellow dots if any
    canvas.delete("yellow_dot")

    # Draw yellow dots around the clicked shape
    draw_yellow_dots(canvas, current_shape)
    # Show edit options for the clicked shape
    # show_edit_options()


def resize_shape(event):
    global start_x, start_y
    if current_shape:
        dx = event.x - start_x
        dy = event.y - start_y
        coords = canvas.coords(current_shape)
        if len(coords) == 4:  # Rectangle or oval
            x1, y1, x2, y2 = coords
            canvas.coords(current_shape, x1, y1, x2 + dx, y2 + dy)
        elif len(coords) == 6:  # Triangle
            x1, y1, x2, y2, x3, y3 = coords
            canvas.coords(current_shape, x1, y1, x2 + dx, y2, (x1 + x2 + dx) / 2, y3 + dy)
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

# def drag_shape(event):
#     global start_x, start_y
#     if current_shape:
#         dx = event.x - start_x
#         dy = event.y - start_y
#         canvas.move(current_shape, dx, dy)
#         update_all_of_drawings(current_shape, coords=canvas.coords(current_shape))
#         start_x = event.x
#         start_y = event.y
def drag_shape(event):
    global current_shape, start_x, start_y

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

def open_width_scale():
    global width_scale
    width_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Width (%)", command=change_width)
    width_scale.pack(side=tk.LEFT, padx=5, pady=5)


def open_height_scale():
    global height_scale
    height_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Height (%)", command=change_height)
    height_scale.pack(side=tk.LEFT, padx=5, pady=5)


# def finish_editing():
#     global edit_mode, width_scale, height_scale
#     edit_mode = False
#     if width_scale:
#         width_scale.pack_forget()  # Remove width scale from view
#     if height_scale:
#         height_scale.pack_forget()  # Remove height scale from view
# Function to finish editing mode
def finish_editing():
    global edit_mode, current_shape
    edit_mode = False
    current_shape = None

def open_rotate_scale():
    rotate_scale = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label='Rotate', command=rotate_shape)
    rotate_scale.pack(side=tk.LEFT, padx=5, pady=5)

#### edit button mode  #####
# Function to enable edit mode and show edit options
def start_edit_mode():
    global edit_mode
    edit_mode = True
    show_edit_options()

# Function to show edit options for current shape
def show_edit_options():
    global edit_mode
    if not edit_mode:
        messagebox.showinfo("Information", "Enable edit mode first.")
        return

    if current_shape:
        edit_menu.post(root.winfo_pointerx(), root.winfo_pointery())
    else:
        messagebox.showinfo("Information", "Please select a shape to edit.")


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
#####################################Drawing section###########################
#####################################Animation section###########################


def update_object_menu():
    object_menu.delete(0, tk.END)  # Clear previous options
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            shape_name = f"{shape['type'].capitalize()}"
            object_menu.add_command(label=shape_name, command=lambda s=shape: select_object(s))

def show_add_button():
    global sorted_drawings
    # print(all_of_drawings[0].get('type'))
    # Filter out drawings that have animations and ensure 'details' key exists
    drawings_with_animations = [d for d in all_of_drawings if d.get('animation')]

    sorted_drawings = sorted(drawings_with_animations, key=lambda x: int(x['start_time']))

    print(sorted_drawings)

    window = tk.Tk()
    window.title("Drawings Per Page")

    # Create a treeview widget to display the data
    tree = ttk.Treeview(window, columns=('Shape', 'Animation', 'Type', 'Start Time', 'Speed'), show='headings')

    # Define the columns
    tree.heading('Shape', text='Shape')
    tree.heading('Animation', text='Animation')
    tree.heading('Type', text='Type')
    tree.heading('Start Time', text='Start Time')
    tree.heading('Speed', text='Speed')

    # Insert data into the treeview
    for draws in sorted_drawings:
        print("pppp")
        print(draws['page'])
        print(current_page)
        if (draws['page']== (current_page)):
            tree.insert('', tk.END,
                        values=(draws['type'], draws['animation'], draws['typeAnimation'], draws['start_time'], draws['speed']))

    # Pack the treeview widget
    tree.pack(expand=True, fill='both')


# def open_settings_window(shape):
#     global speed_value, start_time_value  # Declare them as global to store the values
#
#     # Create a new window
#     settings_window = tk.Toplevel()
#     settings_window.title("Object Settings")
#
#     # Speed label and entry
#     speed_label = tk.Label(settings_window, text="Speed:")
#     speed_label.pack(padx=10, pady=5, anchor=tk.W)
#
#     speed_entry = tk.Entry(settings_window)
#     speed_entry.pack(padx=10, pady=5)
#
#     # Start Time label and entry
#     start_time_label = tk.Label(settings_window, text="Start Time:")
#     start_time_label.pack(padx=10, pady=5, anchor=tk.W)
#
#     start_time_entry = tk.Entry(settings_window)
#     start_time_entry.pack(padx=10, pady=5)
#
#
#     def close_window():
#         global speed_value, start_time_value
#         # Retrieve the entered values
#         speed_value = float(speed_entry.get())
#         start_time_value = float(start_time_entry.get())
#         update_all_of_drawings(shape['id'], speed=speed_value)
#         update_all_of_drawings(shape['id'], start_time=start_time_value)
#         settings_window.destroy()
#
#     # Button to close the window
#     close_button = tk.Button(settings_window, text="Close", command=close_window)
#     close_button.pack(pady=10)

def increment_time_obj():
    global selected_shape

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
    print(all_of_drawings)

def decrement_time_obj():
    global selected_shape

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
        print(all_of_drawings)
    else:
        messagebox.showwarning("Warning", "You can't have negative values!")


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
        print(all_of_drawings)
    else:
        messagebox.showwarning("Warning", "You can't have negative values!")


def select_object(shape):
    global selected_shape, speed_value
    selected_shape = shape
    # print("**************************")
    # print("in select_object:")
    # print("the selected animation:", selected_animation)
    # print("the selected type:", selected_type)
    # print("**************************")
    print(";l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l in select obj")
    print(all_of_drawings)
    print(";l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l;l in select obj")
    object_button.config(text=f"Object: {shape['type'].capitalize()}", fg="black")
    update_all_of_drawings(shape['id'], animation=selected_animation, typeAnimation=selected_type)
    canvas.delete("yellow_dot")
    draw_yellow_dots(canvas, shape['id'])
    print(all_of_drawings)

    # Initialize speed_value for the selected shape
    # speed_value = shape.get('speed', 0)  # Use 0 as the default value if 'speed' is not present
    # speed_entry.delete(0, tk.END)
    # speed_entry.insert(0, str(speed_value))

    plus_button_speed_obj.config(state=tk.NORMAL)
    minus_button_speed_obj.config(state=tk.NORMAL)

    plus_button_time_obj.config(state=tk.NORMAL)
    minus_button_time_obj.config(state=tk.NORMAL)

    # Assuming shape['speed'] is stored as a string with leading zeros
    speed_value = int(shape['speed'])  # Convert to integer to remove leading zeros
    time_value = int(shape['start_time'])  # Convert to integer to remove leading zeros

    # Clear the entry fields and insert the new values
    speed_entry_obj.delete(0, tk.END)
    speed_entry_obj.insert(0, str(speed_value))

    time_entry_obj.delete(0, tk.END)
    time_entry_obj.insert(0, str(time_value))


def next_page():
    global current_page ,max_page
    # print("99999999")
    # print("CURRENT PAGE  ")
    # print(current_page)
    # print("MAX    ")
    # x=max(shape['page'] for shape in all_of_drawings)
    # print(all_of_drawings)
    ###if drawings is not empty###
    if all_of_drawings and current_page < max(shape['page'] for shape in all_of_drawings):
        current_page += 1
        update_canvas()

    ###if drawings is empty###
    if not all_of_drawings and current_page<max_page:
        print("II")
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
    print("in prevrevious:")
    print(current_page)
    print(";;;")
    print(max_page)

def update_all_of_drawings_after_page_change():
    global all_of_drawings
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            draw_saved_shape(shape)

def add_page():
    global current_page, max_page,page_with_time
    current_page += 1
    max_page +=1
    # Add new page with None time to page_with_time
    page_with_time.append((current_page, None))

    update_canvas()
    page_label.config(text=f"Page: {current_page}")
    reassign_page_numbers()
    update_all_of_drawings_after_page_change()
    print(current_page)
    print(";;;")
    print(max_page)
def delete_page():
    global current_page, all_of_drawings, max_page,page_with_time
    print("in deleteeee")
    print(current_page)
    print(";;;")
    print(max_page)

    if all_of_drawings and max_page > 1 :  # Ensure at least one page remains
        all_of_drawings = [shape for shape in all_of_drawings if shape['page'] != current_page]
        # Remove the current page from page_with_time
        page_with_time = [entry for entry in page_with_time if entry[0] != current_page]

        reassign_page_numbers()
        if current_page > len(set(shape['page'] for shape in all_of_drawings)):
            current_page -= 1
        update_canvas()
        page_label.config(text=f"Page: {current_page}")
        update_all_of_drawings_after_page_change()
        max_page = max(shape['page'] for shape in all_of_drawings)

    if not all_of_drawings and max_page > 1:
        # When there are no drawings but more than one page
        max_page -= 1
        current_page = max_page  # Adjust current_page to the new max_page
        page_with_time = [entry for entry in page_with_time if entry[0] <= max_page]

        update_canvas()
        page_label.config(text=f"Page: {current_page}")

    else:
        messagebox.showinfo("Delete the only page", "This is the only page")




def update_canvas():
    global canvas, current_page
    canvas.delete("all")  # Clear the canvas
    # Redraw shapes for the current page
    for shape in all_of_drawings:
        if shape['page'] == current_page:
            draw_saved_shape(shape)
    page_label.config(text=f"Page: {current_page}")

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
            speed_entry.delete(0, tk.END)
            speed_entry.insert(0, str(new_time))
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
                speed_entry.delete(0, tk.END)
                speed_entry.insert(0, str(new_time))
            else:
                messagebox.showwarning("Warning", "You can't have negative values!")
    except ValueError:
        pass


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
cancel_icon = PhotoImage(file= "cancel.png")

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
shape_menu.add_command(label="Cancel",image=cancel_icon, compound=tk.LEFT, command=cancel_add_mode)


# shape_button = tk.Button(button_frame, text="Shapes", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
# shape_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
# Create a button to open the shape window

# Load the icon image
shapes_icon = PhotoImage(file="shapes.png")
# Create a button to open the shape window
shape_button = tk.Button(button_frame, image=shapes_icon, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray', command=open_shape_window)
shape_button.pack(side=tk.TOP, padx=5, pady=10)  # Adjusted pady to 5 for compactness

shape_button.config(command=lambda: shape_menu.post(shape_button.winfo_rootx(), shape_button.winfo_rooty() + shape_button.winfo_height()))


# # Create a smaller button for "Add"
# add_button = tk.Button(button_frame, text="Add", relief=tk.RAISED, bd=2, padx=5, pady=3, bg='lightgray', command=enable_add_mode)
# add_button.pack(side=tk.TOP, padx=5, pady=5)  # Smaller pady and padx for a smaller button

# Load the icon image
add_icon = PhotoImage(file="add.png")

# Create a button with the icon
add_button = tk.Button(button_frame, image=add_icon, command=enable_add_mode, borderwidth=0)
add_button.pack(pady=10)

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
edit_button = tk.Button(button_frame, text="Edit", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray', command=start_edit_mode)
edit_button.pack(side=tk.TOP, padx=5, pady=10)

# # Modify the edit button to show the menu
# edit_button = tk.Button(button_frame, text="Edit", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
# edit_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10
# edit_button.config(command=lambda: edit_menu.post(edit_button.winfo_rootx(), edit_button.winfo_rooty() + edit_button.winfo_height()))

###%%%%%%%%%%%%% text %%%%%%%%%%%%%%%%%%%%
# Create frame for top buttons (Add Text and Edit Text)
top_button_frame = tk.Frame(root, bg='black')
top_button_frame.pack(side=tk.TOP, fill=tk.X)
# Create the Add Text button
# Load icon image
text_icon = tk.PhotoImage(file='text.png')
add_text_button = tk.Button(top_button_frame, image=text_icon, command=add_text, relief=tk.RAISED, bd=2, padx=10, pady=10, bg='lightgray')
add_text_button.image = text_icon  # Keep a reference to the image
add_text_button.pack(side=tk.LEFT, padx=5, pady=5)
# # Button to add text with icon
# add_text_button = tk.Button(root, image=text_icon, command=add_text, bd=0, highlightthickness=0)
# add_text_button.pack(side=tk.TOP, padx=10, pady=10)


edit_icon = tk.PhotoImage(file="edit_text.png")
# edit_text_button = tk.Button(button_frame, image=edit_icon, command=edit_text, relief=tk.RAISED, bd=2, padx=10, pady=10, bg='lightgray')
# edit_text_button.image = edit_icon  # Keep a reference to the image
# edit_text_button.pack(side=tk.TOP, padx=5, pady=10)  # Use pack for consistency
#


edit_text_button = tk.Button(top_button_frame, image=edit_icon, command=edit_text, relief=tk.RAISED, bd=2, padx=10, pady=10, bg='lightgray')
edit_text_button.image = edit_icon  # Keep a reference to the image
edit_text_button.pack(side=tk.LEFT, padx=5, pady=5)
# add_text_button = tk.Button(root, text="Add Text", command=enable_add_text_mode)
# add_text_button.pack(side=tk.TOP, anchor=tk.CENTER, padx=10, pady=10)
#
# # Create the Edit Text button
# edit_text_button = tk.Button(root, text="Edit Text", command=select_text)
# edit_text_button.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)

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


# Create a frame to hold the speed label, entry, and buttons
speed_frame = tk.Frame(right_button_frame,bg='black')

# Add speed label
speed_label = tk.Label(speed_frame, text="Page-time:", font=('Helvetica', 11),fg='white', bg='black')
speed_label.pack(side=tk.LEFT)

# Add speed entry field with customized colors
speed_entry = tk.Entry(speed_frame, width=5,font=('Helvetica', 11), fg='white', bg='black')
speed_entry.insert(0, "0")  # Initial value
speed_entry.pack(side=tk.LEFT)


# Add plus button
plus_button = tk.Button(speed_frame, text="+", command=increment, fg='white', bg='black',font=('Helvetica', 11),bd=0)
plus_button.pack(side=tk.LEFT, padx=5)

# Add minus button
minus_button = tk.Button(speed_frame, text="-", command=decrement,fg='white', bg='black',font=('Helvetica', 11),bd=0)
minus_button.pack(side=tk.LEFT, padx=5)

# Pack the speed frame under the Type button
speed_frame.pack(side=tk.TOP, padx=5, pady=10)


# Object button and menu
object_button = tk.Button(right_button_frame, text="Choose Object", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray', state=tk.DISABLED)
object_button.pack(side=tk.TOP, padx=5, pady=10)

object_menu = tk.Menu(root, tearoff=0)

#$$$
# Create a frame to hold the speed label, entry, and buttons
object_anim_frame = tk.Frame(right_button_frame,bg='black')

# Add speed label
speed_label_obj = tk.Label(object_anim_frame, text="  Object-speed:", font=('Helvetica', 11),fg='white', bg='black')
speed_label_obj.pack(side=tk.LEFT)

# Add speed entry field with customized colors
speed_entry_obj = tk.Entry(object_anim_frame, width=5,font=('Helvetica', 11), fg='white', bg='black')
speed_entry_obj.insert(0, "0")  # Initial value
speed_entry_obj.pack(side=tk.LEFT)


# Add plus button
plus_button_speed_obj = tk.Button(object_anim_frame, text="+", command=increment_speed_obj, fg='white', bg='black',font=('Helvetica', 11),bd=0,state=tk.DISABLED)
plus_button_speed_obj.pack(side=tk.LEFT, padx=5)

# Add minus button
minus_button_speed_obj = tk.Button(object_anim_frame, text="-",command=decrement_speed_obj, fg='white', bg='black',font=('Helvetica', 11),bd=0,state=tk.DISABLED)
minus_button_speed_obj.pack(side=tk.LEFT, padx=5)

# Pack the speed frame under the Type button
object_anim_frame.pack(side=tk.TOP, padx=5, pady=10)

# Create a frame to hold the speed label, entry, and buttons
object_anim_frame_tim = tk.Frame(right_button_frame,bg='black')

# Add speed label
time_label_obj = tk.Label(object_anim_frame_tim, text="Object-time:", font=('Helvetica', 11),fg='white', bg='black')
time_label_obj.pack(side=tk.LEFT)

# Add speed entry field with customized colors
time_entry_obj = tk.Entry(object_anim_frame_tim, width=5,font=('Helvetica', 11), fg='white', bg='black')
time_entry_obj.insert(0, "0")  # Initial value
time_entry_obj.pack(side=tk.LEFT)


# Add plus button
plus_button_time_obj = tk.Button(object_anim_frame_tim, text="+",command=increment_time_obj,  fg='white', bg='black',font=('Helvetica', 11),bd=0,state=tk.DISABLED)
plus_button_time_obj.pack(side=tk.LEFT, padx=5)

# Add minus button
minus_button_time_obj = tk.Button(object_anim_frame_tim, text="-",command=decrement_time_obj, fg='white', bg='black',font=('Helvetica', 11),bd=0,state=tk.DISABLED)
minus_button_time_obj.pack(side=tk.LEFT, padx=5)

# Pack the speed frame under the Type button
object_anim_frame_tim.pack(side=tk.TOP, padx=5, pady=10)

#$$$

animation_button.config(command=open_animation_menu)
type_button.config(command=open_type_menu)
object_button.config(command=open_object_menu)


add_button = tk.Button(right_button_frame, text="Add", command=show_add_button, relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
add_button.pack(side=tk.TOP, padx=5, pady=10)  # Increased pady to 10

add_button.config(command=show_add_button)


video_button = tk.Button(right_button_frame, text="Preview", relief=tk.RAISED, bd=2, padx=10, pady=5, bg='lightgray')
video_button.pack(side=tk.TOP, padx=5, pady=80)
video_button.config(command=create_animation)
############################################
# Create canvas for drawing shapes
canvas = tk.Canvas(root, width=600, height=400, bg='white', borderwidth=2, relief=tk.SUNKEN)
canvas.pack(fill=tk.BOTH, expand=True)


# Frame to contain the navigation buttons and page label
button_frame_p = tk.Frame(root, bg='black')
button_frame_p.pack(side=tk.BOTTOM, fill=tk.X)

left_arrow = PhotoImage(file="left_arrow.png")
right_arrow = PhotoImage(file="right_arrow.png")
# Previous page button
prev_page_button = tk.Button(button_frame_p, image=left_arrow, text="Previous Page", command=previous_page, relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black')
prev_page_button.pack(side=tk.LEFT, padx=5, pady=10)

# Page label
page_label = tk.Label(button_frame_p, text=f" Page: {current_page}", bg='black', fg='white', font=("Arial", 14))
page_label.pack(side=tk.LEFT, fill=tk.X, padx=250, pady=10)  # Adjust padx and pady as needed

# Next page button
next_page_button = tk.Button(button_frame_p,image=right_arrow, text="Next Page", command=next_page, relief=tk.RAISED, bd=0, padx=10, pady=5, bg='black')
next_page_button.pack(side=tk.RIGHT, padx=5, pady=10)


# Optionally add a grid or guides
# for i in range(0, 800, 20):
#     canvas.create_line(i, 0, i, 600, fill="lightgray", tags="grid")
# for i in range(0, 600, 20):
#     canvas.create_line(0, i, 800, i, fill="lightgray", tags="grid")
#
# # Consider using a different cursor when drawing shapes
# canvas.config(cursor="dot")

# Bind mouse click on canvas to select text item
canvas.bind("<Button-1>", select_text)
canvas.bind("<Button-3>", canvas_clicked)

# Bind events to canvas
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<B1-Motion>", draw_shape)
canvas.bind("<ButtonRelease-1>", end_draw)

# rebind_canvas_events()
# Start the main loop
root.mainloop()