from subprocess import Popen, PIPE
from PIL import Image

#---Image Output Options---
imageScale = 8 #scaling for output image

#---Video Output Options---
videoScale = 1 #scaling for individual frames
fps = 120 #frame rate
frameInterval = 8 #every nth frame to be rendered

def show_maze(pixelData, sizeX, sizeY, name):
    #create black image
    im = Image.new("RGB", (sizeX, sizeY))

    #create image from pixelData
    im.putdata(pixelData)

    #scale image
    im = im.resize((sizeX * imageScale, sizeY * imageScale))

    #save image
    im.save(name)

class VideoBuilder:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.frameCount = 0

        #ensure frame dimensions are divisible by 2 (needed for encoding)
        if videoScale == 1:
            self.sizeX += 1
            self.sizeY += 1

        #create initial frame
        self.currentFrame = Image.new("RGB", (self.sizeX, self.sizeY))
        newFrame = self.currentFrame.resize((self.sizeX * videoScale, self.sizeY * videoScale))

        #create and open pipe to ffmpeg process
        self.p = Popen(["ffmpeg", "-y", "-f", "image2pipe", "-vcodec", "png", "-r", str(fps), "-i", "-", "-vcodec", "libx264", "-qscale", "5", "-r", str(fps), "output.mp4"], stdin = PIPE)

        #save initial frame
        newFrame.save(self.p.stdin, "PNG")

    def add_frame(self, x, y):
        #add new pixel to current frame
        self.currentFrame.putpixel((x, y), (255, 255, 255))

        #for every n frames send current frame to ffmpeg
        self.frameCount += 1
        if self.frameCount >= frameInterval:
            newFrame = self.currentFrame.resize((self.sizeX * videoScale, self.sizeY * videoScale))
            newFrame.save(self.p.stdin, "PNG")

            self.frameCount = 0

    def release(self):
        #close ffmpeg process
        p.stdin.close()
