from wand.image import Image as wa

class Presentation:
        """A class used to divide a slide into images"""

        def __init__(self, path, filename):
                """Constructor of the class"""

                print('Image erstellt')
                pass

        def convert(self, path, filename):
                """Method that divides a slide into individual images and stores them in the working memory"""

                pdf = wa(file = path + filename, resolution = 720)
                pdf_image = pdf.convert("jpeg")
                i = 1
                for img in pdf_image.sequence:
                        page = wa(image = img)
                        filename = (str(1) + ".jpg")
                        presentation = Presentation(page, filename)
                        i += 1
                

