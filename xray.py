import matplotlib.pyplot as plt
import numpy as np
import math
from Tkinter import *
import Tkinter as ttk
from ttk import *

def xRaySim():
    #Creates the matrix where our phantom is
    phantom = [[0 for row in range(255)] for col in range(255)]
    broken_leg = [[0 for row in range(255)] for col in range(255)]
    #matrices for our layers
    muscle_matrix = [[0 for row in range(255)] for col in range(255)]
    bone_matrix = [[0 for row in range(255)] for col in range(255)]
    bbone_matrix = [[0 for row in range(255)] for col in range(255)]
    absorption_matrix = [[0 for row in range(255)] for col in range(255)]
    broken_matrix = [[0 for row in range(255)] for col in range(255)]
    #matrices that stores the I values that the beam sees
    storage = [[-1 for row in range(255)] for col in range(255)]

    #degree value that is converted to degrees and calculated
    degrees = tkvar2.get()
    angle = math.tan(degrees * math.pi/180)


    i_values = []
    xray_distance = tkvar4.get()
    film_distance = tkvar3.get()
    initial_energy = tkvar.get()
    fracture_width = tkvar6.get()
    final_energy = initial_energy

    pixel_energy = 0
    if initial_energy == 1.0:
        muscle_absorption = .050
        bone_absorption = 1.2
    else:
        muscle_absorption = .020
        bone_absorption = 1.0

    outer_left_boundary = 50

    inner_left_boundary = 100

    inner_right_boundary = tkvar5.get() + 100

    outer_right_boundary = 240

    #Different loops to set up the phantom
    #This loop first places 0 to everything in the phantom matrix
    for i in range(255):
        for j in range(255):
            absorption_matrix[i][j] = 0
            broken_matrix[i][j] = 0
    #This loop places the first layer from 50 to 240 both horizontally and vertically
    for i in range(outer_left_boundary, outer_right_boundary):
        for j in range(outer_left_boundary, outer_right_boundary):
                absorption_matrix[i][j] = muscle_absorption
                muscle_matrix[i][j] = 1
    #This loop places the bone layer from 100 to 180 both horizonally and vertically
    for i in range(100, 180):
        for j in range(100, inner_right_boundary):
            if(fracture_width > 0 and j >= (140) and j <= 140 + fracture_width):
                absorption_matrix[i][j]= 0
                broken_leg[i][j] = 1
            else:
                absorption_matrix[i][j] = bone_absorption
                bone_matrix[i][j] = 1
    #This is for the line graph. Basically stores the I value. If it hits bone, it does not continue to the other muscle layer, it just uses that I value.
    for i in range(255):
        i_values.append(final_energy)
        final_energy = initial_energy
        for j in range(255):
            if(absorption_matrix[i][j] != 0):
                if(bone_matrix[i][j] == 1):
                    final_energy = initial_energy * math.exp(-1 * (absorption_matrix[j][i]) * 1)
                    break
                else:
                    pixel_energy = initial_energy * math.exp(-1 * (absorption_matrix[j][i]) * 1)
                    phantom[i][j] = initial_energy * math.exp(-1 * (absorption_matrix[j][i]) * 1)
                    final_energy = pixel_energy
            else:
                continue
    #This loop creates the phantom image based on the I values of every pixel
    for i in range(255):
        for j in range(255):
            if(absorption_matrix[i][j] != 0):
                phantom[i][j] = initial_energy * math.exp(-1 * (absorption_matrix[i][j]) * 1)
            else:
                phantom[i][j] = -1
    ph = plt.figure(1)
    ph.canvas.set_window_title('Phantom')
    plt.imshow(phantom, cmap='Blues')
    plt.savefig("phantom.png")
    #This calculates the x value which are the pixels that the beam goes through on each row and then puts the values into a matrix
    #I made the y of the triangle the center and worked backwards
    for i in range(255):
        x_value = round((angle * (xray_distance + (i + 1))))
        k = 127
        f = 127
        left_side = 127 - x_value
        right_side = 127 + x_value
        if(left_side < 0):
            left_side = 0
        if(right_side > 255):
            right_side = 255
        for j in range(int(left_side), 127):
            storage[i][k] = phantom[i][k]
            k = k - 1
        for j in range(127, int(right_side)):
            storage[i][f] = phantom[i][f]
            f = f + 1
    #This calculates the total x_value
    x_value = int(round((angle * (xray_distance + film_distance + 255))))

    #This initializes the film matrix based on x_value, setting all inital pixel values to -1 so that they appear black on the image
    film = [[-1 for row in range(x_value)] for col in range(x_value)]
    #This loop projects the image to the film, the size or sensors is based on the x value
    for i in range(x_value):
       k = 0
       f = 0
       left_side = x_value
       if(left_side < 0):
           left_side = 0
       for j in range(0, int(x_value/2)):
           if k < 128 and i < 255:
               film[i][int(x_value/2) - k] = storage[i][127 - k]
           else:
               continue
           k = k + 1
       for j in range(int(x_value/2), x_value):
           if f < 128 and i < 255:
               film[i][int(x_value/2) + f] = storage[i][127 + f]
           else:
               continue
           f = f + 1



    #Two windows should pop up, a line graph and the stored values from the angled beam

    line_graph = plt.figure(2)
    line_graph.canvas.set_window_title('I-Values')
    plt.plot(i_values)
    projection = plt.figure(3)
    projection.canvas.set_window_title('X-Ray')
    plt.ion()
    plt.imshow(film, cmap='gray')

    plt.show(block = True)

root = Tk()
root.title("X-Ray Simulation")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady = 200, padx=200)

# Create a Tkinter variable
tkvar = DoubleVar(root)
tkvar2 = IntVar(root)
tkvar3 = IntVar(root)
tkvar4 = IntVar(root)
tkvar5 = IntVar(root)
tkvar6 = IntVar(root)

# Dictionary with options
choices = {'.5','1.2'}
choices2 = {'1','30','35','40','45'}
choices3 = {'5','10','20','50','100','500'}
choices4 = {'50','60','80','100','5','500'}
choices5 = {'55', '65', '80', '95'}
choices6 = {'0','5', '10', '20'}


popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Select an initial Intensity").grid(row=1, column=0)
popupMenu.grid(row=2, column=0)
#tkvar.set('')  # set the default option
popupMenu = OptionMenu(mainframe, tkvar2, *choices2)
Label(mainframe, text="Select an initial angle").grid(row=3, column=0)
popupMenu.grid(row=4, column=0)
popupMenu = OptionMenu(mainframe, tkvar3, *choices3)
Label(mainframe, text="Distance from film").grid(row=5, column=0)
popupMenu.grid(row=6, column=0)
popupMenu = OptionMenu(mainframe, tkvar4, *choices4)
Label(mainframe, text="Distance of source from phantom").grid(row=7, column=0)
popupMenu.grid(row=8, column=0)
popupMenu = OptionMenu(mainframe, tkvar5, *choices5)
Label(mainframe, text="Width of Bone").grid(row=9, column=0)
popupMenu.grid(row=10, column=0)
popupMenu = OptionMenu(mainframe, tkvar6, *choices6)
Label(mainframe, text="Width of Bone Fracture").grid(row=11, column=0)
popupMenu.grid(row=12, column=0)

submit_button = ttk.Button(mainframe, text="Submit")
submit_button.grid(row=13, column=1)
submit_button['command'] = xRaySim

#root.Button(self.root, text="OK", command=root.update()).grid(row=9, column=1)
#popupMenu.grid(row=8, column= 1)


# on change dropdown value
def change_dropdown(*args):
    print(tkvar.get())
    print(tkvar2.get())
    print(tkvar3.get())
    print(tkvar4.get())
    print(tkvar5.get())
    print(tkvar6.get())


# link function to change dropdown
tkvar.trace('w', change_dropdown)
tkvar2.trace('w', change_dropdown)
tkvar3.trace('w', change_dropdown)
tkvar4.trace('w', change_dropdown)
tkvar5.trace('w', change_dropdown)
tkvar6.trace('w', change_dropdown)


root.mainloop()