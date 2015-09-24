import PIL
import os
from PIL import Image
import random

def myround(x, base=15):
    return int(base * round(float(x)/base))

def average_colour(image):
  colour_tuple = [None, None, None]
  for channel in range(3):

      # Get data for one channel at a time
      pixels = image.getdata(band=channel)

      values = []
      for pixel in pixels:
          values.append(pixel)

      colour_tuple[channel] = sum(values) / len(values)

  return tuple(colour_tuple)

emoji_names = []
for root, dirs, files in os.walk('emoji-images'):
    emoji_names += [str(root.replace("\\","/")+"/"+f) for f in files]

print "loading"
emoji_images = []
for name in emoji_names:
    try:
        img = Image.open(name).resize((30, 30),Image.ANTIALIAS)
        emoji_images += [[name, img, img.convert('RGBA'), average_colour(img)]]
    except Exception, e:
        print e
print "loading complete"

# print emoji_images

img_addr = "E:/Users/Harry/Documents/emojievolution/I8QlqUVh.jpeg"#"E:/Users/Harry/Documents/emojievolution/Super_Paper_Mario_Bowser.jpg"#"E:/Users/Harry/Documents/emojievolution/emoji-images/Emoji Smiley/Emoji Smiley-90.png"#
# img_addr = "E:/Actual Pics/1418155982593.jpg"#"E:/Actual Pics/1402943716291.jpg"#"E:/Actual Pics/tumblr_ndlqrusbY51sqx8y7o8_540.jpg"
original_raw_im = Image.open(img_addr).resize((400, 400),Image.ANTIALIAS)
original_im = original_raw_im.convert('RGB')
working_im = Image.new("RGB", (original_im.size[0], original_im.size[1]), "white")

# print emoji_images
gen = 0
# while True:
    # x_pos = myround(random.randint(0, working_im.size[0]-emoji.size[0]))
    # y_pos = myround(random.randint(0, working_im.size[1]-emoji.size[1]))

for x_pos in range(0, working_im.size[0]-30, 30):
    for y_pos in range(0, working_im.size[1]-30, 30):

        bbox = (x_pos, y_pos, 30, 30)
        working_slice = original_im.crop(bbox)

        best_emoji = None
        best_fitness = 0

        for emoji_tuple in emoji_images:
            # emoji = Image.open(emoji_images[random.randint(0, len(emoji_images)-1)]).resize((30, 30),Image.ANTIALIAS)
            # emoji = Image.open(emoji_url).resize((30, 30),Image.ANTIALIAS)
            # print emoji_tuple
            # print emoji_tuple[1]
            emoji = emoji_tuple[1]
            emoji_rgba = emoji_tuple[2]#emoji.convert('RGBA')

            potential_fitness = current_fitness = 0

            for x in range(0, emoji.size[0]):
                for y in range(0, emoji.size[1]):

                    potential_pixel = emoji_rgba.getpixel((x, y))
                    if potential_pixel[3] > 10:
                        current_pixel = working_im.getpixel((x+x_pos, y+y_pos))
                        original_pixel = original_im.getpixel((x+x_pos, y+y_pos))

                        potential_dif = current_dif = 0

                        for rgb in range(0, 3):
                            if original_pixel[rgb] > potential_pixel[rgb]:
                                potential_dif += original_pixel[rgb] - potential_pixel[rgb]
                            else:
                                potential_dif += potential_pixel[rgb] - original_pixel[rgb]

                        for rgb in range(0, 3):
                            if original_pixel[rgb] > current_pixel[rgb]:
                                current_dif += original_pixel[rgb] - current_pixel[rgb]
                            else:
                                current_dif += current_pixel[rgb] - original_pixel[rgb]

                        if potential_dif > current_dif:
                            current_fitness += 1
                        else:
                            potential_fitness += 1

                        # working_im.putpixel( (x_pos+x, y_pos+y), original_pixel)

                    # print "potential color: %s" % str(emoji_rgb.getpixel((x, y)))
                    # print "current color: %s" % str(working_im.getpixel((x+x_pos, y+y_pos)))
                    # print "original color: %s" % str(original_im.getpixel((x+x_pos, y+y_pos)))
                    # working_im.putpixel( (x_pos+x, y_pos+y), (0,0,0))

            if potential_fitness > best_fitness:
                best_fitness = potential_fitness
                best_emoji = emoji

        working_im.paste(best_emoji, (x_pos, y_pos), best_emoji)
        gen += 1
        if gen%25 == 0:
            working_im.save("results/gen-%s.jpg" % str(gen), "JPEG")
        print gen

            # print potential_fitness, current_fitness
            # if potential_fitness > current_fitness:
            #     # print 'better'
            #     working_im.paste(emoji, (x_pos, y_pos), emoji)
            #     gen += 1
            #     if gen%25 == 0:
            #         working_im.save("results/gen-%s.jpg" % str(gen), "JPEG")
            #     print gen
    # else:
        # print 'worse'


working_im.show()
