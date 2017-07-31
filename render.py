from PIL import Image
import os

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
        im.save(path + "\\frames\\frame" + str(self.frameCount) + ".png")
        self.frameCount += 1

    def add_frame(self, x, y):
        #saves a copy of last frame with added pixel at (x, y)
        newFrame = self.lastFrame.copy()
        newFrame.putpixel((x, y), 1)
        self.lastFrame = newFrame
        newFrame = newFrame.resize((self.sizeX * self.scale, self.sizeY * self.scale))
        newFrame.save(path + "\\frames\\frame" + str(self.frameCount) + ".png")

        self.frameCount += 1

    def build_gif(self):
        #resize all frames based on scale
        try:
            for i in range(0, len(self.frames)):
                self.frames[i] = self.frames[i].resize((self.sizeX * self.scale, self.sizeY * self.scale))
        except ValueError:
            print("Bad Image Mode:", self.frames[i].mode)
            self.frames[i].show()
            raise

        #create gif from frames
        with Image.open("maze.gif") as im:
            im.save("maze.gif", save_all = True, append_images = self.frames, duration = delay)
