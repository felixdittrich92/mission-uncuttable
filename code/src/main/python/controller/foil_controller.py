from wand.image import Image as wa

"""currently save as a own image"""
def convert():
    pdf = wa(filename = "XXX.pdf", resolution = 720)
    pdfImage = pdf.convert("jpeg")
    i = 1
    for img in pdfImage.sequence:
        page = wa(image = img)
        page.save(filename = str(i) + ".jpg") 
        i += 1
