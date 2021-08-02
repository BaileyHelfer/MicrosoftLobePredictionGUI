from lobe import ImageModel
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.scrolledtext as st
import os
import natsort
import threading
from tkinter import filedialog as fd
import TkWidgets
HEIGHT = 900
WIDTH = 1340
imgWIDTH = 450
imgHEIGHT = 300
images =[]
prevImgs =[]
img2 = ""
original = images
badImg = 0
totalImg = 0

############     BACKEND     ############

#loadImgs takes the path from user and loads the imgs in that path into a list
#1.Put img files from folder inside list 'images'
#2.Sort the files in list so they appear like they do in windows folder
#3.Take the first img in the list and load it into img frame and get loab prediction
def loadImgs():
    global images
    global reverse
    global img2
    global original
    images = []
    folderName = os.path.dirname(imageLabel.get())
    className = os.path.basename(folderName)
    imgClass.on_entry()
    imgClass.delete(0,'end')
    imgClass.insert(tk.INSERT,className)
    imgClass.on_exit()
    try:
        for filename in os.listdir(folderName):
            if filename.endswith(".jpeg") or filename.endswith(".png"):       
               images.append(filename)
        images = natsort.natsorted(images,reverse = False)
        original = images.copy()
        img2 = os.path.basename(imageLabel.get())
        img = Image.open(folderName + "\\" + img2)
        img = img.resize((imgWIDTH,imgHEIGHT),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img) 
        my_img.img = img
        my_img['image'] = img
        scanImage()
        outBox.insert(tk.INSERT,"Succesfully Loaded Images!\n\n")
    except:
        outBox.config(state = 'normal')
        outBox.insert(tk.INSERT,"Error: Incorrect image and/or model path given.'\n")
        outBox.config(state = 'disabled')
 
#This function takes the current loaded image and gets the one after it
#1.Retrieve the path to the folder the user selected
#2.Get the location of the current img in list
#3.Create 
#4.Make the list an iter object and get the next images in list
#5.Open up the current image and place it in frame.
#6.Lastly scan that image for lobePrediction
def nextImg():
    global images
    global img2
    folderName = os.path.dirname(imageLabel.get())
    try:
        index = original.index(img2)
        images = original[index:]
        images = iter(images)
        img2 = next(images)
        img2 = next(images)
        img = Image.open(folderName + "\\" + img2)
        img = img.resize((imgWIDTH,imgHEIGHT),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img) 
        my_img.img = img
        my_img['image'] = img
        scanImage()
    except StopIteration:
        outBox.config(state = 'normal')
        outBox.insert(tk.INSERT,"Error: Reached End of Images.\n")
        outBox.config(state = 'disabled')
    except:
        outBox.config(state = 'normal')
        outBox.insert(tk.INSERT,"Error: Image/Model path must be correct and must click 'load images.'\n")
        outBox.config(state = 'disabled')
#This function takes the current loaded image and gets the one before it
#1.Retrieve the path to the folder the user selected
#2.Make a copy of the original list containing all the images and put list in reverse order
#3.Set the list to the index of the current image to the end of the list
#4.Make the list an iter object and get the next images in list
#5.Open up the current image and place it in frame.
#6.Lastly scan that image for lobePrediction
def prevImg():
    global prevImgs
    global original
    global img2
    try:
        folderName = os.path.dirname(imageLabel.get())
        prevImgs = original.copy()
        prevImgs.reverse()
        index = prevImgs.index(img2)
        images = prevImgs[index:]
        images = iter(images)
        img2 = next(images)
        img2 = next(images)
        img = Image.open(folderName + "\\" + img2)
        img = img.resize((imgWIDTH,imgHEIGHT),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img) 
        my_img.img = img
        my_img['image'] = img
        scanImage()
    except StopIteration:
        outBox.config(state = 'normal')
        outBox.insert(tk.INSERT,"Error: Reached Start of Images.\n")
        outBox.config(state = 'disabled')
    except:
        outBox.config(state = 'normal')
        outBox.insert(tk.INSERT,"Error: Image/Model path must be correct and must click 'load images.'\n")
        outBox.config(state = 'disabled')
    
#scanFolder takes the folder path from user and gets prediction of every image in folder
#1.Get the onnx model from entry label
#2.Create for loop that goes through every label inside the 'images' list
#3.Inside for loop create an image at specified index in list and place in frame
#4.With this image, get the Lobe prediction
#5.Print out the result name and confidence %
def scanFolder():
    global img2,badImg,totalImg
    outBox.config(state = 'normal')
    try:
        onnxModel = ImageModel.load(modelLabel.get())
        folderName = os.path.dirname(imageLabel.get())
        for filename in images:    
            image = Image.open(folderName + "\\" + filename)
            image = image.resize((imgWIDTH,imgHEIGHT),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            my_img.img = img
            my_img['image'] = img
            result = onnxModel.predict_from_file(folderName + "\\" + filename)
            outBox.insert(tk.INSERT,filename + '-' + result.prediction +"\n")
            for label, confidence in result.labels:
                if confidence > 0.1:
                    if imgClass.get() != label:
                        outBox.insert(tk.INSERT,(f"{label}: {confidence*100}%" + "\n\n"),('Highlight'))
                        resultLabel.config(text = f"{label}: {confidence*100}%")
                        badImg+=1
                        totalImg+=1
                        accuracyPercent.config(text = getPercentage())
                    else:
                        outBox.insert(tk.INSERT,(f"{label}: {confidence*100}%" + "\n\n"))
                        resultLabel.config(text = f"{label}: {confidence*100}%")
                        totalImg += 1
                        accuracyPercent.config(text = getPercentage())
            else:
                continue

        img2 = filename
    except OSError as err:
        outBox.insert(tk.INSERT,"Error {0}: ".format(err) + "\n\n")
    except:
        outBox.insert(tk.INSERT,"Error {0}: Invalid signature or model. \n\n") 
    outBox.config(state = 'disabled')

#scanImage takes the path given for image and uses it to scan for lobe prediction
#1.Get the onnx model from entry label
#2.Get the img file stored at img2 and load it into an image
#3.Set the result from using the lobe prediction of a file
#4.Print out the result name and confidence %
def scanImage():
    global img2,badImg,totalImg
    outBox.config(state = 'normal')
    try:
        onnxModel = ImageModel.load(modelLabel.get())
        path = os.path.dirname(imageLabel.get())
        image = Image.open(path + "\\" +img2)
        image = image.resize((imgWIDTH,imgHEIGHT),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        my_img.img = img
        my_img['image'] = img
        file = os.path.basename(imageLabel.get())
        result = onnxModel.predict_from_file(path+ "\\" + img2)
        for label, confidence in result.labels:
            if confidence > 0.1:
                if imgClass.get() != label:
                    outBox.insert(tk.INSERT,img2 + '-' + result.prediction +"\n",('Highlight'))
                    outBox.insert(tk.INSERT,(f"{label}: {confidence*100}%" + "\n\n"),('Highlight'))
                    resultLabel.config(text = f"{label}: {confidence*100}%")
                    badImg+=1
                    totalImg+=1
                    accuracyPercent.config(text = getPercentage())
                else:
                    outBox.insert(tk.INSERT,img2 + '-' + result.prediction +"\n")
                    outBox.insert(tk.INSERT,(f"{label}: {confidence*100}%" + "\n\n"))
                    resultLabel.config(text = f"{label}: {confidence*100}%")
                    totalImg+=1
                    accuracyPercent.config(text = getPercentage())

    except OSError as err:
        outBox.insert(tk.INSERT,"Error {0}: ".format(err) + "\n\n")
    except:
        outBox.insert(tk.INSERT,"Error {0}: Invalid signature or model. \n\n")
    outBox.config(state = 'disabled')

def getPercentage():
    temp = badImg/totalImg
    temp2 = 1 - temp
    temp2 = temp2*100
    return temp2,'%'

############     GUI     ############
root = tk.Tk()
root.geometry("+200+50")
root.resizable(False,False)
root.title("Lobe Predictions")
root.iconbitmap("resources/uss_icon.ico")

#Method to select a file and return its path
#1.set filename to the path the user clicks
#2.enter the box to get rid of default text
#3.insert file path obtained from filename
#4.call on exit function for leaving entrybox
def selectFile(entry):
    filename = fd.askopenfilename()
    entry.on_entry()
    entry.delete(0,'end')
    entry.insert(tk.INSERT,filename)
    entry.on_exit()

#Method to get the directory of file selected
#1.Ask user to open file inside the folder they want
#2.Insert the selected folder path inside the selected entry box
def selectFolder(entry):
    filename = fd.askopenfilename()
    folderNAME = os.path.dirname(filename)
    entry.on_entry()
    entry.delete(0,'end')
    entry.insert(tk.INSERT,folderNAME)
    tk.messagebox.askokcancel("Warning","Make sure model and signature.json are in same folder")
    entry.on_exit()
#Method to clear the text from the log scrolledtext
#1.Enable the textbox and clear its entry
def clearLog():
    global badImg,totalImg
    badImg = 0
    totalImg = 0
    outBox.config(state = 'normal') 
    outBox.delete('1.0',tk.END)
    outBox.config(state = 'disabled')

#Method opens up about text file for user to read
def openAbout():
    os.system("start ABOUT.txt")

#Method to confirm the user wants to quit program
#1.Get result if user clicked yes to confirm or no to deny
#2.If yes then quit program else return to program
def askQuit():
    result = tk.messagebox.askquestion("Warning", "Are you sure you want to quit?")
    if result == 'yes':
        root.destroy()
    else:
        return

#Displaywindow to set its size when first opened
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

#Menu bars at top left to show about program and to quit
menubar = tk.Menu(root)
root.config(menu = menubar)
fileMenu = tk.Menu(menubar)
menubar.add_cascade(label = "File",menu = fileMenu)
fileMenu.add_cascade(label = "About",command = openAbout)
fileMenu.add_cascade(label = "Quit",command = askQuit)

#Container to place widgets and organize 
frame = tk.Canvas(root, bg = '#7D6FC0')
frame.place(relx = 0, rely = 0, relwidth = 1, relheight= 1)


#Img handling container
imgContainer =tk.Canvas(frame,width = imgWIDTH,height = imgHEIGHT,bg = "black")
imgContainer.place(relx = .65,rely = .025)
emptyIMG = Image.open("resources/emptyimg.jpg")
emptyIMG = emptyIMG.resize((imgWIDTH,imgHEIGHT),Image.ANTIALIAS)
img = ImageTk.PhotoImage(emptyIMG)
my_img = tk.Label(imgContainer,image = img)
my_img.image = img
my_img.place(relx = 0,rely = 0)

#Load and create image for 'scanImg' button
redo = Image.open("resources/redo.png")
redo = redo.resize((40,30),Image.ANTIALIAS)
redoImg = ImageTk.PhotoImage(redo)

#Button to scan the current image being displayed
scanImageBtn = TkWidgets.HoverButton(frame,bg = 'light blue',activebackground = 'white',image = redoImg,command =scanImage)
scanImageBtn.place(relx = .80,rely  = .38)

#Button to go through each image in selected image folder and get lobe prediction
scanFolderBtn = TkWidgets.HoverButton(frame,bg = 'light blue',activebackground = 'white',text = "Scan Folder",command =lambda:threading.Thread(target = scanFolder).start())
scanFolderBtn.place(relx = .64,rely = .3825)
scanFolderBtn.config(font = ("Lato", 12 ,"bold"))

#Button to initialize the images that the user selected
loadImgBtn = TkWidgets.HoverButton(frame,bg = 'light blue',activebackground = 'white',text = "Load Images",command = loadImgs)
loadImgBtn.place(relx = .25,rely = .27)
loadImgBtn.config(font = 'bold')

#Loading and creating image icon for 'nextImg' button
rightArrow = Image.open("resources/rightarrow.png")
rightArrow = rightArrow.resize((40,30),Image.ANTIALIAS)
rightArrowImg = ImageTk.PhotoImage(rightArrow)

#Button to flip through images after the current one being displayed
nextImgBtn = TkWidgets.HoverButton(frame,bg = 'light blue',activebackground = 'white',image = rightArrowImg,command = lambda:threading.Thread(target = nextImg).start())
nextImgBtn.place(relx = .87,rely = .38)

#Loading and creating image icon for 'prevImg' button
leftArrow = Image.open("resources/leftarrow.png")
leftArrow = leftArrow.resize((40,30),Image.ANTIALIAS)
leftArrowImg = ImageTk.PhotoImage(leftArrow)

#Button to flip through previous images of the current image displayed
prevImgBtn = TkWidgets.HoverButton(frame,bg = 'light blue',activebackground = 'white',image = leftArrowImg,command = lambda:threading.Thread(target = prevImg).start())
prevImgBtn.place(relx = .73,rely = .38)

#Title placed at top of frame with background color matching frame and fg color of white
title = tk.Label(frame,fg = 'white', bg = '#808080',text = "LobePrediction")
title.place(relx = 0.05, rely = 0.05, relwidth = 0.25, relheight = 0.05)
title.config(font = ("Lato", 15 ,"bold"))

#Entrybox for user to enter in path to tensorflow model 
modelLabel = TkWidgets.LabeledEntry(frame,bg = 'white', bd = 5,fg = 'grey',label = "Path To ONNX model...")
modelLabel.config(font = ("Roboto", 10))
modelLabel.place(relx = 0.12, rely = 0.12, relwidth = 0.40,relheight = 0.05)

#Entrybox for user to enter in path to labels document
imageLabel = TkWidgets.LabeledEntry(frame,bg = 'white', bd = 5,fg = 'grey',label = "Path To image folder...")
imageLabel.config(font = ("Roboto", 10))
imageLabel.place(relx = 0.12, rely = 0.20, relwidth = 0.4,relheight = 0.05)


classLabel = tk.Label(frame,fg = 'white', bg = 'black',text = "Image Class")
classLabel.place(relx = 0.06,rely = 0.65,relheight = .05)
classLabel.config(font = ("Roboto", 10,'bold') )
imgClass = TkWidgets.LabeledEntry(frame,bg = 'white', bd = 5,fg = 'grey',label = "Class to Scan...")
imgClass.config(font = ("Roboto", 10))
imgClass.place(relx = 0.12, rely = 0.65, relwidth = 0.4,relheight = 0.05)

#Image icon for selecting onnx model and image folder
imageIcon = Image.open("resources/fileicon.png")
imageIcon = imageIcon.resize((40,30),Image.ANTIALIAS)
imageImg = ImageTk.PhotoImage(imageIcon)

#Button to select model path
modelButton = TkWidgets.HoverButton(frame,fg = 'black',bg = 'light blue',activebackground = 'white',image = imageImg,command = lambda:selectFolder(modelLabel))
modelButton.place(relx = 0.05, rely = 0.1225, relwidth = 0.07, relheight = 0.04)
modelButton.config(font = ("Lato", 9 ))

#Button to select labels file
imagesButton = TkWidgets.HoverButton(frame,bg = 'light blue',fg = 'black',image = imageImg,command = lambda:selectFile(imageLabel))
imagesButton.place(relx = 0.05, rely = 0.2, relwidth = 0.07, relheight = 0.04)
imagesButton.config(font = ("Lato", 9 ))

#Status label and log textbox
outLabel = tk.Label(frame,fg = 'white', bg = 'black',text = "Results Log")
outLabel.place(relx = 0.55, rely = 0.65, relwidth = 0.45, relheight = 0.05)
outLabel.config(font = ("Lato", 15 ,"bold"))
outBox = st.ScrolledText(frame)
outBox.place(relx = 0.55, rely = 0.7, relwidth = 0.45,relheight = 0.3)
outBox.config(font = ("Roboto", 10),state = 'disabled')
outBox.tag_add('Highlight','current','end-1line')
outBox.tag_config("Highlight", background= "yellow", foreground= "black")


#Button for clearing the log text entry
clearLogBtn = TkWidgets.HoverButton(frame,bg = 'light blue',fg = 'black',text = "Clear Log/Stats",command = clearLog)
clearLogBtn.place(relx = .45,rely = 0.85)
clearLogBtn.config(font = ("Lato", 12 ,"bold"))

#Label displaying default slot for the current prediction form lobe 
currentPredict = tk.Label(frame,fg = 'white', bg = '#7D6FC0',text = "Current Prediction:")
currentPredict.place(relx = 0.55, rely = 0.45, relwidth = 0.15, relheight = 0.05)
currentPredict.config(font = ("Lato", 15 ,"bold"))

#Label that actually displays the current prediction from lobe
resultLabel = tk.Label(frame,fg = 'white', bg = '#7D6FC0',text = "Waiting...",anchor = 'w')
resultLabel.place(relx = 0.70, rely = 0.45, relwidth = 0.25, relheight = 0.05)
resultLabel.config(font = ("Lato", 15 ,"bold"))

accuracyLabel = tk.Label(frame,fg = 'white',bg ='#7D6FC0',text = 'Accuracy =')
accuracyLabel.place(relx = 0.555,rely = 0.50)
accuracyLabel.config(font = ("Lato", 15 ,"bold"))

accuracyPercent = tk.Label(frame,fg = 'white',bg ='#7D6FC0',text = '100%')
accuracyPercent.place(relx = 0.65,rely = 0.50)
accuracyPercent.config(font = ("Lato", 15 ,"bold"))
#Main root calls askQuit function when windows exit button is clicked
root.protocol("WM_DELETE_WINDOW",askQuit)
root.mainloop()