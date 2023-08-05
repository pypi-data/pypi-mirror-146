import tkinter
import numpy as np
import pandas as pds
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import random
import evolutionary
import os




### CHOOSE CHARACTERISTICS
characteristics={"woman":False,"man":False,"young":False,"old":False,"beard":False,"no_beard":False,"straight":False,"no_straight":False}
#print(characteristics )


def initialize() :
    for cle, valeur in characteristics.items() :
        characteristics[cle]=False
    #print(characteristics)


def onClick(event):
    for c in myWindow.winfo_children():
        c.destroy()
    initialize()
    mainFrame=tkinter.Frame(myWindow,bg='LightSkyBlue3',width=30, borderwidth=3, relief='groove')
    mainFrame.pack(side='top', padx=30, pady=30,fill="x" )
    tkinter.Label(mainFrame,bg='LightSkyBlue3',text="What did the agressor look like ?",font=(10)).pack(padx=20,pady=20)

    #the women/man frame
    Frame1=tkinter.Frame(myWindow,borderwidth=3, relief='groove')
    Frame1.pack(padx=5, pady=5)

    #to select only one option
    value = tkinter.StringVar()
    fButton=tkinter.Radiobutton(Frame1,text="Woman",variable=value, value=1)
    fButton.pack(side='left', padx=5, pady=5)
    fButton.bind('<Button-1>', fevent)

    hButton=tkinter.Radiobutton(Frame1,text="Man",variable=value, value=2)
    hButton.pack(side='right', padx=5, pady=5)
    hButton.bind('<Button-1>', hevent)

    #the young/old frame
    Frame2=tkinter.Frame(myWindow,borderwidth=3, relief='groove')
    Frame2.pack(padx=5, pady=5)

    value = tkinter.StringVar()
    yButton=tkinter.Radiobutton(Frame2,text="Young",variable=value, value=1)
    yButton.pack(side='left', padx=5, pady=5)
    yButton.bind('<Button-1>', yevent)

    oButton=tkinter.Radiobutton(Frame2,text="Old",variable=value, value=2)
    oButton.pack(side='right', padx=5, pady=5)
    oButton.bind('<Button-1>', oevent)


    #show a new window to propose some pictures depending on the characteristics
    myButton=tkinter.Button(myWindow,text='Next', width=50, bg="LightSkyBlue4", font=(1))
    myButton.pack(padx=20, pady=20, fill="x")
    myButton.bind('<ButtonRelease-1>',sex_characteristics)

def fevent(event):
    characteristics["woman"]=True
    characteristics["man"]=False

def hevent(event):
    characteristics["man"]=True
    characteristics["woman"]=False

def yevent(event):
    characteristics["young"]=True
    characteristics["old"]=False

def oevent(event):
    characteristics["old"]=True
    characteristics["young"]=False

def bevent(event):
    characteristics["beard"]=True
    characteristics["no_beard"]=False

def nbevent(event):
    characteristics["no_beard"]=True
    characteristics["beard"]=False

def sevent(event):
    characteristics["straight"]=True
    characteristics["no_straight"]=False

def nsevent(event):
    characteristics["no_straight"]=True
    characteristics["straight"]=False

def sex_characteristics(event):

    if characteristics["man"]==True:
        mainFrame=tkinter.Frame(myWindow,bg='LightSkyBlue3',width=30, borderwidth=3, relief='groove')
        mainFrame.pack(side='top', padx=30, pady=30,fill="x" )
        tkinter.Label(mainFrame,bg='LightSkyBlue3',text='And his beard?',font=(10)).pack(padx=20,pady=20)

        #the beard/no beard frame
        Frame3=tkinter.Frame(myWindow,borderwidth=3, relief='groove')
        Frame3.pack(padx=5, pady=5)

        value = tkinter.StringVar()
        bButton=tkinter.Radiobutton(Frame3,text="Beard",variable=value, value=1)
        bButton.pack(side='left', padx=5, pady=5)
        bButton.bind('<Button-1>', bevent)

        nbButton=tkinter.Radiobutton(Frame3,text="No Beard",variable=value, value=2)
        nbButton.pack(side='right', padx=5, pady=5)
        nbButton.bind('<Button-1>', nbevent)

    elif characteristics["man"]==False:
        mainFrame=tkinter.Frame(myWindow,bg='LightSkyBlue3',width=30, borderwidth=3, relief='groove')
        mainFrame.pack(side='top', padx=30, pady=30,fill="x" )
        tkinter.Label(mainFrame,bg='LightSkyBlue3',text='And her hair?',font=(10)).pack(padx=20,pady=20)

        #the straight/no straight hair frame
        Frame4=tkinter.Frame(myWindow,borderwidth=3, relief='groove')
        Frame4.pack(padx=5, pady=5)

        value = tkinter.StringVar()
        sButton=tkinter.Radiobutton(Frame4,text="Straight Hair",variable=value, value=1)
        sButton.pack(side='left', padx=5, pady=5)
        sButton.bind('<Button-1>', sevent)

        nsButton=tkinter.Radiobutton(Frame4,text="No Straight Hair",variable=value, value=2)
        nsButton.pack(side='right', padx=5, pady=5)
        nsButton.bind('<Button-1>', nsevent)

    myButton=tkinter.Button(myWindow,text='Show portraits', width=50, bg="LightSkyBlue4", font=(1))
    myButton.pack(padx=20, pady=20, fill="x")
    myButton.bind('<ButtonRelease-1>',inital_population)

#base de données correspondant aux critères
def choice_database(char):
    if char["woman"] and char["young"] and char["straight"]:
        return 'images/img_female_young_straight.csv.npy'
    if char["woman"] and char["young"] and char["no_straight"]:
        return 'images/img_female_young_wavy.csv.npy'
    if char["woman"] and char["old"] and char["straight"]:
        return 'images/img_female_old_straight.csv.npy'
    if char["woman"] and char["old"] and char["no_straight"]:
        return 'images/img_female_old_wavy.csv.npy'
    if char["man"] and char["young"] and char["beard"]:
        return 'images/img_male_young_beard.csv.npy'
    if char["man"] and char["young"] and char["no_beard"]:
        return 'images/img_male_young_nobeard.csv.npy'
    if char["man"] and char["old"] and char["beard"]:
        return 'images/img_male_old_beard.csv.npy'
    if char["man"] and char["old"] and char["no_beard"]:
        return 'images/img_male_old_nobeard.csv.npy'
    else :
        print('Im in else')
        return None


def reselect(event) :
    for c in myWindow.winfo_children():
        c.destroy()
    mainFrame=tkinter.Frame(myWindow,bg='LightSkyBlue3',width=30, borderwidth=3, relief='groove')
    mainFrame.pack(side='top', padx=30, pady=30,fill="x" )
    tkinter.Label(mainFrame,bg='LightSkyBlue3',text='A data is missing, please reselect',font=(10)).pack(padx=40,pady=40,fill="x")
    myButton=tkinter.Button(myWindow,text='Reselect', width=50, bg="LightSkyBlue4",font=(10))
    myButton.place(relx=0.5, rely=0.5, anchor="center")
    myButton.bind('<ButtonRelease-1>',onClick)


##PRESENTATION DE LA POPULATION INITIAL

def inital_population(event):
    database=choice_database(characteristics)
    if database == None:
        print('Im in none')
        reselect(event)
    if database != None:
        for c in myWindow.winfo_children():
            c.destroy()
        #print(characteristics)
        tkinter.Label(myWindow,bg='LightSkyBlue3',text='Do you recognise one of the suspects ?',font=(10)).pack(padx=10,pady=10,fill="x")
        #place(relx=0.5, rely=0.1, anchor="center",fill="x")
        #.pack(padx=10,pady=10)

        encoded_imgs=np.load(database, allow_pickle=True)
        sample_size=10
        img_index = np.random.choice(range(len(encoded_imgs)), sample_size)
        pop0=encoded_imgs[img_index]
        #print(len(pop0[1]))

        pop0_decoded_imgs = decoder.predict(pop0)

        photo=[]
        for i in range (len(pop0_decoded_imgs)) :

            plt.imsave("img", pop0_decoded_imgs[i].reshape(128,128,3), format="png")
            photo.append(ImageTk.PhotoImage(Image.open("img")))

    #for i in range(5):
    #    myWindow.columnconfigure(i, weight=1)

    #myWindow.rowconfigure(1, weight=1)


        imLab1=tkinter.Label(myWindow,image=photo[0])
        imLab1.place(relx=0.10, rely=0.35, anchor="center")
        imLab1.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[0], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab2=tkinter.Label(myWindow,image=photo[1])
        imLab2.place(relx=0.30, rely=0.35, anchor="center")
        imLab2.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[1], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab3=tkinter.Label(myWindow,image=photo[2])
        imLab3.place(relx=0.5, rely=0.35, anchor="center")
        imLab3.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[2], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab4=tkinter.Label(myWindow,image=photo[3])
        imLab4.place(relx=0.70, rely=0.35, anchor="center")
        imLab4.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[3], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab5=tkinter.Label(myWindow,image=photo[4])
        imLab5.place(relx=0.9, rely=0.35, anchor="center")
        imLab5.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[4], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab6=tkinter.Label(myWindow,image=photo[5])
        imLab6.place(relx=0.10, rely=0.65, anchor="center")
        imLab6.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[5], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab7=tkinter.Label(myWindow,image=photo[6])
        imLab7.place(relx=0.30, rely=0.65, anchor="center")
        imLab7.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[6], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab8=tkinter.Label(myWindow,image=photo[7])
        imLab8.place(relx=0.5, rely=0.65, anchor="center")
        imLab8.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[7], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab9=tkinter.Label(myWindow,image=photo[8])
        imLab9.place(relx=0.70, rely=0.65, anchor="center")
        imLab9.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[8], nb_children=4: chooseimage(pop, parent, nb_children))

        imLab10=tkinter.Label(myWindow,image=photo[9])
        imLab10.place(relx=0.90, rely=0.65, anchor="center")
        imLab10.bind('<Button-1>', lambda event,  pop=encoded_imgs, parent=pop0[9], nb_children=4: chooseimage(pop, parent, nb_children))


        myWindow.mainloop()




###### PRESENT CHILDREN

def chooseimage(pop, parent, nb_children) :
    for c in myWindow.winfo_children():
        c.destroy()
    tkinter.Label(myWindow,bg='LightSkyBlue3',text='Do you recognise one of the suspects ?',font=(10)).pack(padx=10,pady=10,fill="x")
    #place(relx=0.5, rely=0.1, anchor="center",fill="x")
    #print(i)
    new_pop=evolutionary.get_children_from_parent(pop, parent, nb_children)
    children_decoded_imgs = decoder.predict(new_pop)
    #print(len(children_decoded_imgs))
    photo=[]
    for j in range (len(children_decoded_imgs)) :
        plt.imsave("img", children_decoded_imgs[j].reshape(128,128,3), format="png")
        photo.append(ImageTk.PhotoImage(Image.open("img")))

    #print(len(photo))
    for k in range(3):
        myWindow.columnconfigure(k, weight=1)

    #myWindow.rowconfigure(1, weight=1)

    imLab1=tkinter.Label(myWindow,image=photo[0])
    imLab1.place(relx=0.5, rely=0.35, anchor="center")
    imLab1.bind('<Button-1>', lambda event, photo=photo[0], pop=pop, parent=new_pop[0], nb_children=4: end_or_continue(photo, pop, parent, nb_children))

    imLab2=tkinter.Label(myWindow,image=photo[1])
    imLab2.place(relx=0.3, rely=0.65, anchor="center")
    imLab2.bind('<Button-1>', lambda event, photo=photo[1], pop=pop, parent=new_pop[1], nb_children=4: end_or_continue(photo, pop, parent, nb_children))

    imLab3=tkinter.Label(myWindow,image=photo[2])
    imLab3.place(relx=0.5, rely=0.65, anchor="center")
    imLab3.bind('<Button-1>', lambda event, photo=photo[2], pop=pop, parent=new_pop[2], nb_children=4: end_or_continue(photo, pop, parent, nb_children))

    imLab4=tkinter.Label(myWindow,image=photo[3])
    imLab4.place(relx=0.7, rely=0.65, anchor="center")
    imLab4.bind('<Button-1>', lambda event, photo=photo[3], pop=pop, parent=new_pop[3], nb_children=4: end_or_continue(photo, pop, parent, nb_children))

    myWindow.mainloop()


### End loop or continue

def end_or_continue(photo, pop, parent, nb_children):

    for c in myWindow.winfo_children():
        c.destroy()
    tkinter.Label(myWindow,bg='LightSkyBlue3',text='Is this your agressor ?',font=(10)).pack(padx=10,pady=10,fill="x")
    #place(relx=0.5, rely=0.1, anchor="center",fill='x')

    imLab1=tkinter.Label(myWindow,image=photo)
    imLab1.place(relx=.5,rely=.5, anchor="center")


    myEndButton=tkinter.Button(myWindow,text='I have found my suspect', width=30, bg='LightSkyBlue4', font=(1))
    myEndButton.place(relx=0.3, rely=0.8, anchor="center")
    myEndButton.bind('<ButtonRelease-1>',lambda event, photo=photo: found_agressor(photo))

    myContinueButton=tkinter.Button(myWindow,text='Show other portraits', width=30, bg='LightSkyBlue4', font=(1))
    myContinueButton.place(relx=0.7, rely=0.8, anchor="center")
    myContinueButton.bind('<ButtonRelease-1>',lambda event, pop=pop, parent=parent, nb_children=4 : chooseimage(pop, parent, nb_children))




### CRIMINAL FOUND

def found_agressor(photo):
    for c in myWindow.winfo_children():
        c.destroy()
    Frame=tkinter.Frame(myWindow,borderwidth=3, relief='groove')
    Frame.pack(side='top', padx=10, pady=20,expand="yes",fill="both")

    #place(relx=0.5, rely=0.1, anchor="center",fill='x')

    imLab1=tkinter.Label(Frame,image=photo)
    imLab1.place(relx=.5,rely=.6, anchor="center")

    Frame1=tkinter.Frame(Frame,bg='LightSkyBlue3',borderwidth=1, relief='groove')
    Frame1.pack( padx=10, pady=10,fill="x")
    tkinter.Label(Frame1,bg='LightSkyBlue3',text='Portrait of the suspect',font=(20)).pack(padx=10,pady=10,fill="x")

    tkinter.Label(Frame,text='Thank you for your collaboration !',font=(10)).pack(padx=10,pady=10,fill="x")
    global emoji
    emoji = ImageTk.PhotoImage(file = "detective.png")
    tkinter.Label(Frame,image=emoji).pack()
    #place(relx=0.5, rely=0.9, anchor="center",fill='x')



if __name__=="__main__" :

    from keras.models import load_model
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    decoder = load_model("model/decodeur.h5")


    #First Window

    myWindow=tkinter.Tk()
    myWindow.geometry("1000x700")
    myWindow['bg']='white'




    Frame=tkinter.Frame(myWindow,borderwidth=3, relief='groove')
    Frame.pack(side='top', padx=10, pady=20,expand="yes",fill="both")
    logo = ImageTk.PhotoImage(file = "logo_insa.png")
    tkinter.Label(Frame,image=logo).pack()

    title= tkinter.Label(Frame,text='Project 4BIM',font=(20))
    title.place(relx=0.5, rely=0.35, anchor="center")

    descLabel=tkinter.Label(Frame, text='This is an application developped by 4BIM INSA students to help you create a robot portait of your agressor. \n The application will propose several faces, you just have to click on the photo to select it !  ')
    descLabel.place(relx=0.5, rely=0.5, anchor="center")
    #descLabel.pack()

    emoji1 = ImageTk.PhotoImage(file = "detective_fem.jpg")
    tkinter.Label(Frame,image=emoji1).place(relx=0.4, rely=0.655, anchor="center")
    emoji2 = ImageTk.PhotoImage(file = "detective_hom.png")
    tkinter.Label(Frame,image=emoji2).place(relx=0.6, rely=0.65, anchor="center")

    myButton=tkinter.Button(Frame,text='Start !', font=(10), width=50, bg="LightSteelBlue4")
    myButton.place(relx=0.5, rely=0.8, anchor="center")
    myButton.bind('<ButtonRelease-1>',onClick)


    myWindow.mainloop()
