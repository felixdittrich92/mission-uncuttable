from wand.image import Image as wa

class Presentation:
        
        def __init__(self, path, filename):
                print('Image erstellt')
                pass

        def convert(self, path, filename):
                pdf = wa(file = path + filename, resolution = 720)
                pdf_image = pdf.convert("jpeg")
                i = 1
                for img in pdf_image.sequence:
                        page = wa(image = img)
                        #filename = (str(1) + ".jpg")
                        slide[i] = Slide(i, page)
                        i += 1

