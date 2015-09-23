import PIL
import os
from PIL import Image
import random

emoji_images = []
for root, dirs, files in os.walk('emoji-images'):
    emoji_images += [root.replace("\\","/")+"/"+f for f in files]

img_addr = "E:/Users/Harry/Documents/emojievolution/I8QlqUVh.jpeg"#"E:/Users/Harry/Documents/emojievolution/Super_Paper_Mario_Bowser.jpg"#"E:/Users/Harry/Documents/emojievolution/emoji-images/Emoji Smiley/Emoji Smiley-90.png"#
# img_addr = "E:/Actual Pics/1418155982593.jpg"#"E:/Actual Pics/1402943716291.jpg"#"E:/Actual Pics/tumblr_ndlqrusbY51sqx8y7o8_540.jpg"
original_raw_im = Image.open(img_addr)#.resize((400, 400),Image.ANTIALIAS)
original_im = original_raw_im.convert('RGB')
working_im = Image.new("RGB", (original_im.width, original_im.height), "white")

print working_im.getpixel((1, 1))

# print emoji_images
gen = 0
while True:
    emoji = Image.open(emoji_images[random.randint(0, len(emoji_images)-1)]).resize((25, 25),Image.ANTIALIAS)
    emoji_rgba = emoji.convert('RGBA')
    x_pos = random.randint(0, working_im.width-emoji.width)
    y_pos = random.randint(0, working_im.height-emoji.height)

    potential_fitness = current_fitness = 0

    for x in range(0, emoji.width):
        for y in range(0, emoji.height):

            potential_pixel = emoji_rgba.getpixel((x, y))
            if potential_pixel[3] > 10:
                current_pixel = working_im.getpixel((x+x_pos, y+y_pos))
                original_pixel = original_im.getpixel((x+x_pos, y+y_pos))

                potential_total = potential_pixel[0]+potential_pixel[1]+potential_pixel[2]
                current_total = current_pixel[0]+current_pixel[1]+current_pixel[2]
                original_total = original_pixel[0]+original_pixel[1]+original_pixel[2]

                # print potential_pixel, current_pixel, original_pixel

                if original_total > potential_total:
                    potential_dif = original_total - potential_total
                else:
                    potential_dif = potential_total - original_total

                if original_total > current_total:
                    current_dif = original_total - current_total
                else:
                    current_dif = current_total - original_total

                # print potential_dif, current_dif

                if potential_dif > current_dif:
                    current_fitness += 1
                else:
                    potential_fitness += 1

                # working_im.putpixel( (x_pos+x, y_pos+y), original_pixel)

            # print "potential color: %s" % str(emoji_rgb.getpixel((x, y)))
            # print "current color: %s" % str(working_im.getpixel((x+x_pos, y+y_pos)))
            # print "original color: %s" % str(original_im.getpixel((x+x_pos, y+y_pos)))
            # working_im.putpixel( (x_pos+x, y_pos+y), (0,0,0))

    # print potential_fitness, current_fitness
    if potential_fitness > current_fitness:
        # print 'better'
        working_im.paste(emoji, (x_pos, y_pos), emoji)
        gen += 1
        if gen%25 == 0:
            working_im.save("results/gen-%s.jpg" % str(gen), "JPEG")
        print gen
    # else:
        # print 'worse'


working_im.show()
