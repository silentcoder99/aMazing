from PIL import Image
import os

#---Video Output Options---
dBuffer = 5 #Number of digits used for frame numbering

#absolute path of script
path = os.path.dirname(os.path.abspath(__file__))

def show_maze(pixelData, sizeX, sizeY, scale):
    #create black image
    im = Image.new("1", (sizeX, sizeY))

    #create image from pixelData
    im.putdata(pixelData)

    #scale image
    im = im.resize((sizeX * scale, sizeY * scale))

    #display and save image
    im.show()
    im.save("maze.png")

class GifBuilder:
    def __init__(self, sizeX, sizeY, scale):
        self.frameCount = 0
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.scale = scale
        self.lastFrame = Image.new("1", (self.sizeX, self.sizeY))
        im = self.lastFrame.resize((self.sizeX * scale, self.sizeY * scale))

        #create frames directory if one doesn't exist
        if not os.path.exists(path + "\\frames"):
            os.makedirs(path + "\\frames")

        #save initial frame
        im.save(path + "\\frames\\frame" + str(self.frameCount).zfill(dBuffer) + ".png")
        self.frameCount += 1

    def add_frame(self, x, y):
        #saves a copy of last frame with added pixel at (x, y)
        newFrame = self.lastFrame.copy()
        newFrame.putpixel((x, y), 1)
        self.lastFrame = newFrame
        newFrame = newFrame.resize((self.sizeX * self.scale, self.sizeY * self.scale))
        newFrame.save(path + "\\frames\\frame" + str(self.frameCount).zfill(dBuffer) + ".png")

        self.frameCount += 1

    def build_gif(self):
        #TODO: Implement ffmpeg automation
        pass
