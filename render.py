from PIL import Image

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

def show_gif():
    pass
