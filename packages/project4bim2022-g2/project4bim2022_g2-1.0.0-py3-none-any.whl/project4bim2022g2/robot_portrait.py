from .autoencoder import *
from .genetic_algorithm import *

import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Fonctions de l'interface graphique

def start_algo():
    '''This function creates a 2nd window (on which the images will be displayed after) as a subwindow of the main window.
    With just this function, the window is empty but created.
    After creating the window, the function texte_window is called, which will display text in the window'''
    # On crée la 2ème fenêtre
    global window2
    window2 = tk.Toplevel(window)
    # window.withdraw()
    window.iconify()
    window2.title("Robot Portrait")
    window2.geometry("1000x650")
    window2.resizable(height=False, width=False)
    window2.configure(bg='white')

    texte_window()


def texte_window():
    '''This function adds in the 2nd window a text. It's a kind of tutorial/explanation of how to use the graphical interface and what it's supposed to do.
    At the end of the function, the function contenu_window is called, to add extra content to this 2nd window'''
    ToDo = tk.Label(window2, text="Choose between 1 and 4 images that most represent the suspect.\n You can select an image by clicking on the associated button, which will then turn blue.\n When you are done with the selection, click on the >>NEXT button. \n Then, the program will propose you other images generated from the ones you have selected. \n If you think there is one image representing exactly the suspect, after selecting it, you can click on 'I have found my suspect'. \n The program will display the chosen image and end", wraplength=900, bg="white", width=window_width)
    # fontTitle=tkFont.Font(size=16)
    ToDo.configure(font=("Helvetica", 12))
    ToDo.place(relx=0.5, rely=0.5)
    ToDo.pack()
    contenu_window(z)


def contenu_window(z):
    '''This function adds content to the 2nd window.
    It allows displaying the 10 images that are in the list z, the buttons to choose the images and the "next", "quit" and "I have found my suspect" buttons, at the bottom of the window, with which the user can interact

    Args:
        z(np.array): List containing 10 latent vectors representing the 10 images that have been calculated by the algorithm or that have been generated randomly thanks to the neural network (for the 1st iteration)
    Return:
        None'''
    nbr_columns = 5

    # On définit la liste suspects, dans laquelle les indices des images sélectionnées par l'utilisateur seront stockées
    global suspects
    suspects = []

    # Buttons
    try:
        Button1 = tk.Button(window2, command=lambda: [returnperson(0), ChangeColor(
            Button1)], text="Person 1", width=15, font=('Helvetica', 10), bg="white")
        Button1.place(x=40, rely=0.47)

        Button2 = tk.Button(window2, command=lambda: [returnperson(1), ChangeColor(
            Button2)], text="Person 2", width=15, font=('Helvetica', 10), bg="white")
        Button2.place(x=240, rely=0.47)

        Button3 = tk.Button(window2, command=lambda: [returnperson(2), ChangeColor(
            Button3)], text="Person 3", width=15, font=('Helvetica', 10), bg="white")
        Button3.place(x=440, rely=0.47)

        Button4 = tk.Button(window2, command=lambda: [returnperson(3), ChangeColor(
            Button4)], text="Person 4", width=15, font=('Helvetica', 10), bg="white")
        Button4.place(x=640, rely=0.47)

        Button5 = tk.Button(window2, command=lambda: [returnperson(4), ChangeColor(
            Button5)], text="Person 5", width=15, font=('Helvetica', 10), bg="white")
        Button5.place(x=840, rely=0.47)

        Button6 = tk.Button(window2, command=lambda: [returnperson(5), ChangeColor(
            Button6)], text="Person 6", width=15, font=('Helvetica', 10), bg="white")
        Button6.place(x=40, rely=0.8)

        Button7 = tk.Button(window2, command=lambda: [returnperson(6), ChangeColor(
            Button7)], text="Person 7", width=15, font=('Helvetica', 10), bg="white")
        Button7.place(x=240, rely=0.8)

        Button8 = tk.Button(window2, command=lambda: [returnperson(7), ChangeColor(
            Button8)], text="Person 8", width=15, font=('Helvetica', 10), bg="white")
        Button8.place(x=440, rely=0.8)

        Button9 = tk.Button(window2, command=lambda: [returnperson(8), ChangeColor(
            Button9)], text="Person 9", width=15, font=('Helvetica', 10), bg="white")
        Button9.place(x=640, rely=0.8)

        Button10 = tk.Button(window2, command=lambda: [returnperson(9), ChangeColor(
            Button10)], text="Person 10", width=15, font=('Helvetica', 10), bg="white")
        Button10.place(x=840, rely=0.8)

        print("Iteration", iteration)

        # On reconstruit l'image (on decode le vecteur latent)
        z2 = np.array(reconstruct_image_from_latent_vectors(decoder, z))

        # On convertit les listes de pixels en objet image
        list_images = list_to_images(z2)

        # On affiche ces images dans la fenêtre
        Images(list_images)

        # Bouton next, qui fait passer à l'itération suivante
        button_next = tk.Button(window2, text=">>NEXT", fg="black", bg="white", height=1,
                                width=8, command=lambda: [ask_confirmation(z)], font=('Helvetica', 11))
        button_next.place(x=870, y=600)

        # Bouton 'I have found my suspect', qui permet de terminer le programme avant d'atteindre le nombre d'itérations maximal
        bouton_fin = tk.Button(window2, text="I have found my suspect", command=lambda: [
                               ask_confirmation_end(z), set_iteration()], bg="white", font=('Helvetica', 11))
        bouton_fin.place(x=420, y=600)

        # Bouton quit, qui permet de fermer tout le programme
        bouton = tk.Button(window2, text="QUIT", bg="white", command=lambda: [
                           set_iteration(), fermer_tout()], font=('Helvetica', 11))
        bouton.pack()
        bouton.place(x=50, y=600)

        # Quand on arrive à la dernière itération, il faut choisir une seule image
        if iteration == (nbre_iter_max-1):
            messagebox.showwarning(
                "Last iteration", "This is the last iteration, you have to choose only one image that will be the one of the suspect. If you are not satisfied, you can close the window and restart")
            button_next.config(state=tk.DISABLED)
        window2.mainloop()
    except:
        quit()


def fermer_tout():
    '''This function ends the program and closes all the windows. It is called when the user clicks on the button QUIT'''
    ask_the_client = tk.messagebox.askyesno(
        "Quit", "Do you really want to quit ? All the windows will be closed")
    if ask_the_client == 1:
        # On détruit tous les widgets (y compris les sous-fenêtres) de window2
        for c in window2.winfo_children():
            c.destroy()
        # On détruit tous les widgets (y compris les sous-fenêtres) de window
        for c in window.winfo_children():
            c.destroy()
        # On détruit la fenêtre principale
        window.destroy()


def end_algo(z, suspects):
    '''This function creates a window in which the image of the chosen suspect will appear.
    It also saves the suspect's image in the suspects folder and contains a QUIT button

    Args:
        z (np.array): List containing 10 latent vectors representing the 10 images that have been calculated by the algorithm or that have been generated randomly thanks to the neural network (for the 1st iteration)
        suspects(list): List containing the index of the image chosen by the user
    Return:
        None'''
    window3 = tk.Toplevel(window2)
    window2.withdraw()
    window3.title("Robot Portrait")
    window3.configure(bg='white')
    window3.geometry("450x550")
    window3.resizable(height=False, width=False)
    texte = tk.Label(window3, anchor='center', text="Here is your suspect !", font=(
        'Helvetica', 20, 'bold'), wraplength=700, bg="white")
    texte.pack()
    texte.place(x=225, y=70, anchor="center")
    bouton = tk.Button(window3, text="QUIT", command=fermer_tout)
    bouton.pack()
    bouton.place(x=225, y=470, anchor="center")
    # Dans le cas où le témoin arrête le programme avant la fin du nombre d'itération prévu
    z_selected = []
    for indice in suspects:
        z_selected.append(z[indice])
    L = np.array(reconstruct_image_from_latent_vectors(
        decoder, np.array(z_selected)))
    Im = list_to_images(L)
    image = Im[0]
    Im = image.resize((300, 300))
    try:
        Im.save('./suspects/image_suspect.png')
    except:
        os.mkdir('suspects')
        Im.save('./suspects/image_suspect.png')
    Im.save('./suspects/image_suspect.png')
    Im = ImageTk.PhotoImage(Im, master=window3)
    Im_widget = tk.Label(window3, image=Im)
    Im_widget.image = Im
    Im_widget.place(x=225, y=270, anchor='center')
    messagebox.showinfo(
        "Save image", "The image has been save in the folder /suspects")
    window3.mainloop()


# On crée la fenêtre
def welcome_window():
    '''This function allows display the welcome window. It creates the "root" window of the graphical interface, the first window that the user will see.
    On this window, there is a title, a little explicative text (objectives and the task the user will have to do) and a START button.
    When clicking on it, it activates the function start_algo, which creates another window in which the images will be displayed and the core of the program will start
    '''
    global window
    window = tk.Tk()
    # Titre de la fenêtre
    window.title("Robot Portrait")
    # On choisit la couleur du fond
    window.configure(bg='white')
    # On fixe la taille de la fenêtre pour qu'il n'y ait pas de problème en redimensionnant
    window.resizable(height=False, width=False)

    # On choisit les dimensions
    window.geometry("1000x650")
    global window_width
    window_width = 1000
    global window_height
    window_height = 650

    # On définit le texte de la première page
    texte1 = tk.Label(window, anchor='center', text="Welcome to our program to generate robot portraits and identify criminals !", font=(
        'Helvetica', 20, 'bold'), wraplength=700, bg="white")
    texte1.pack()
    texte1.place(x=500, y=200, anchor="center")
    texte2 = tk.Label(window, text="In a few seconds, 10 faces will be displayed on the screen and you will have to choose between 1 and 4 images that most look like the suspect that you have in mind ",
                      font='Helvetica', anchor='center', wraplength=500,  bg="white")
    texte2.pack()
    texte2.place(x=500, y=300, anchor="center")

    # On définit le bouton qui va permettre de démarrer le programme
    bouton1 = tk.Button(window, text="START", command=lambda: [
                        reinitialize_iteration(), start_algo()])
    bouton1.pack()
    bouton1.place(x=500, y=500, anchor="center")

    window.mainloop()


def ask_confirmation(z):
    '''This function asks confirmation of the choice of image(s) made by the user.
    It is called by clicking on the ">> NEXT" button.
    If the user answers "no", the current window is reinitialized (the user can make new choices if he/she made a mistake)
    If the user answers "yes", the function checks if the user chose a right number of images and runs the function next_step

    Args:
        z (np.array): List containing 10 latent vectors representing the 10 images that have been calculated by the algorithm or that have been generated randomly thanks to the neural network (for the 1st iteration)
    Return:
        None'''
    ask_the_client = tk.messagebox.askyesno(
        "Your selection", "Did you select all the wanted files? [yes/no]")
    if ask_the_client == 1:
        if (len(suspects) == 0 or len(suspects) >= 5):
            messagebox.showwarning(
                "Wrong number of images selected", "You should select between 1 and 4 images")
            contenu_window(z)
        else:
            add_1()
            next_step(z, suspects)
    else:
        contenu_window(z)


def ask_confirmation_end(z):
    '''This function asks confirmation of the choice of the suspect's image when clicking on "I have found my suspect".
    If the user answers "no", the current window is reinitialized
    If the user answers "yes", the function calls the end_algo function, that will finally displays the image of the suspect chosen

    Args:
        z (np.array): List containing 10 latent vectors representing the 10 images that have been calculated by the algorithm or that have been generated randomly thanks to the neural network (for the 1st iteration)
    Return:
        None'''
    ask_the_client = tk.messagebox.askyesno(
        "Your selection", "Did you select the suspect's image? [yes/no]")
    if ask_the_client == 1:
        if len(suspects) == 1:
            end_algo(z, suspects)
        else:
            messagebox.showwarning(
                "Wrong number of images selected", "You should select only one image")
            contenu_window(z)
    else:
        contenu_window(z)


def reinitialize_iteration():
    '''This function reinitialize the number of iterations.
    It is called every time the user clicks on the START button, which enables the program to be restarted if the user wants, as the welcome_window is iconified.'''
    global iteration
    iteration = 0


def next_step(z, suspects):
    '''This function generates and calculates the next generation of images thanks to the genetic algorithm/evolution strategy.
    It is called every time the user clicks on the ">> NEXT" button and confirms his/her choice

    Args:
        (np.array): List containing 10 latent vectors representing the 10 images that have been calculated by the algorithm or that have been generated randomly thanks to the neural network (for the 1st iteration)
        suspects (list): List containing the index of the image(s) chosen by the user
    '''
    while iteration < nbre_iter_max:
        if z is not None:
            n = len(z)
            z_selected = []
            for indice in suspects:
                z_selected.append(z[indice])
            z = adjust_children(z_selected, prior)
            suspects = []
            contenu_window(z)


def add_1():
    '''This function increases the variable iteration by 1.
    It is called every time the user clicks on the >> NEXT button and confirms his/her choice'''
    global iteration
    iteration += 1


def set_iteration():
    '''This function sets the global variable "iteration" at its maximum'''
    global iteration
    iteration = nbre_iter_max


def Images(list_images):
    '''This function enables the images to be displayed in the window ; list_images changes at each iteration of the algorithm

    Args:
        list_images (list) : list of 10 PIL images, that will be displayed in the window and the user will choose between them
    '''
    # new size for the images
    newsize = (150, 150)
    for i in range(10):
        Im = list_images[i]
        Im = Im.resize(newsize)
        Im = ImageTk.PhotoImage(Im, master=window2)
        # i va de 0 à 9
        j = i+1
        if j == 1:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=30, rely=0.22)
        if j == 2:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=230, rely=0.22)
        if j == 3:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=430, rely=0.22)
        if j == 4:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=630, rely=0.22)
        if j == 5:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=830, rely=0.22)
        if j == 6:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=30, rely=0.55)
        if j == 7:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=230, rely=0.55)
        if j == 8:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=430, rely=0.55)
        if j == 9:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=630, rely=0.55)
        if j == 10:
            Im_widget = tk.Label(window2, image=Im)
            Im_widget.image = Im  # nécessaire
            Im_widget.place(x=830, rely=0.55)


def list_to_images(L):
    '''This function converts a list of pixels of images (between 0 and 1) in a list of PIL images

    Args:
        L (np.array): np.array of 10 np.array of pixels
    Return:
        list_images (list) : list of PIL images obtained from the lists of pixels in L '''
    list_images = []
    for image in L:
        pil_image = Image.fromarray((image*255).astype(np.uint8))
        list_images.append(pil_image)
    return list_images


def returnperson(x):
    '''This function adds the index of each image (in the z np.array) chosen by the user in the list "suspects".
    It is called every time the user clicks on "Person x" button '''
    if x not in suspects:
        suspects.append(x)


def ChangeColor(button):
    '''This function changes the color of the button to blue.
    It is called the 1st time the user clicks on "Person x" button'''
    button.configure(fg="blue")


def run():
    '''This function makes run the whole program and graphical interface, by defining the encoder, decoder, necessary for decoding the image, the 1st images contained in list z generated randomly by the autoencoder.
    It also defines the number of maximum iterations and the global variable suspects where the indexes of the images chosen by the user will be stored'''
    this_dir, _ = os.path.split(__file__)

    global prior
    prior = get_prior(num_modes=2, latent_dim=50)
    global encoder
    encoder = get_encoder(
        latent_dim=50, kl_regularizer=get_kl_regularizer(prior))
    global decoder
    decoder = get_decoder(latent_dim=50)

    encoder.load_weights(os.path.join(
        this_dir, "model_vae/VAE_encoder6"))
    decoder.load_weights(os.path.join(
        this_dir, "model_vae/VAE_decoder6"))

    # encoder.load_weights("./model_vae/encoder/saved_encoder")
    # decoder.load_weights("./model_vae/decoder/saved_decoder")

    global z
    z = generate_latent_vectors(prior, 10)

    global iteration
    iteration = 0

    global suspects
    suspects = []

    global nbre_iter_max
    nbre_iter_max = 15

    welcome_window()
