from PIL import Image

def show_maze(pixelData, size, scale):
    #create black image
    im = Image.new("1", (size, size))

    #create image from pixelData
    im.putdata(pixelData)

    #scale image
    im = im.resize((size * scale, size * scale))

    #display and save image
    im.show()
    im.save("maze.png")
