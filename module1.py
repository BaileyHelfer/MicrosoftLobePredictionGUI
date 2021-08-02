from lobe import ImageModel

onnxModel = ImageModel.load(r"C:\Users\bhelf\source\repos\LiveStreamVideoAPP\LiveStreamVideoAPP")
result = onnxModel.predict_from_file(r"C:\Users\bhelf\source\repos\LiveStreamVideoAPP\LiveStreamVideoAPP\frames\frame-27-07-2021-13-21-11.jpg")
print(type(result))
print(result.prediction)
newResult = result.labels[0]
print(newResult)
#for label, confidence in result.labels:
#    if confidence > 0.1:
       
