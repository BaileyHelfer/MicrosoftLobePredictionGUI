# Microsoft Lobe Prediction GUI!
![](preview.PNG)
This program is designed to take a Machine Learning Model created from Lobe and use that
model to make inference on the images selected.

# Installation
Clone the repository and create a virutal environment using the requirements.txt. To install the Lobe library you must install from their github here: https://github.com/lobe/lobe-python

# How to use GUI

Step 1
* Make sure you have a trained model from Lobe and that you exported it to onnx format.

Step 2
* If the name of your folder containing the images you want to infer is the name of the class you want to infer
it will make using GUI easier as it predict based off the folder name selected(you can change this in Image Class box)

Step 3
* After selecting the image folder and model path load the images and from there you can either predict each image indivisually or do a scan of the whole folder. The choice is yours!
