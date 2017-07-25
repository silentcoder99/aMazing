from PIL import Image

def show_maze(pixelData, size, scale):
    #create black image
    im = Image.new("1", (size * scale, size * scale))

    #add pixels scaled to fix desired size
    im.putdata(pixelData, scale)
    im.show()
