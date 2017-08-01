from subprocess import Popen, PIPE
from PIL import Image

#---Image Output Options---
imageScale = 8

#---Video Output Options---
videoScale = 2 #scaling for individual frames
fps = 120
qScale = 5 #quality of output video

def show_maze(pixelData, sizeX, sizeY):
    #create black image
    im = Image.new("1", (sizeX, sizeY))

    #create image from pixelData
    im.putdata(pixelData)

    #scale image
    im = im.resize((sizeX * imageScale, sizeY * imageScale))

    #display and save image
    im.show()
    im.save("maze.png")

class VideoBuilder:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.lastFrame = Image.new("1", (self.sizeX, self.sizeY))
        im = self.lastFrame.resize((self.sizeX * videoScale, self.sizeY * videoScale))

        #create and open pipe to ffmpeg process

        self.p = Popen(["ffmpeg", "-y", "-f", "image2pipe", "-vcodec", "png", "-r", str(fps), "-i", "-", "-vcodec", "libx264", "-qscale", str(qScale), "-r", str(fps), "output.mp4"], stdin = PIPE)
        #save initial frame
        im.save(self.p.stdin, "PNG")

    def add_frame(self, x, y):
        #saves a copy of last frame with added pixel at (x, y)
        newFrame = self.lastFrame.copy()
        newFrame.putpixel((x, y), 1)
        self.lastFrame = newFrame
        newFrame = newFrame.resize((self.sizeX * videoScale, self.sizeY * videoScale))
        newFrame.save(self.p.stdin, "PNG")

    def build_video(self):
        #clean up
        p.stdin.close()
