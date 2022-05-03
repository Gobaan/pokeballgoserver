import easyocr
reader = easyocr.Reader(['en'])
text = reader.readtext('zubat.jpg', detail=0)
print (text)
