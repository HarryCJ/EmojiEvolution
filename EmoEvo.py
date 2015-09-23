import PIL
import os
from PIL import Image

print "hello world"

# module_folder = os.path.join("C:/Users/hjohnson/Documents/EmojiEvolution/emoji-photos")
emoji_images = []

for root, dirs, files in os.walk('emoji-images'):
    emoji_images.append(root.replace("\\","/")+"/"+f for f in files)

# im = Image.open(emoji_images[0])
# im.show()
print emoji_images[0]
# print emoji_images
