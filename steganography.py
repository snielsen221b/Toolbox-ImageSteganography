"""A program that encodes and decodes hidden messages in images through LSB
steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the
     provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for x in range(x_size):
        for y in range(y_size):
            pixel = red_channel.load()[x, y]
            binary_pixel = bin(pixel)
            if binary_pixel[-1] == '1':
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)

    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode="BEEES!", template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by
    default.
    """
    image_to_encode = write_text(text_to_write=text_to_encode, image_size=(200,
                                                                           200))

    image_to_encode_with = Image.open(template_image)
    red_channel = image_to_encode_with.split()[0]
    green_channel = image_to_encode_with.split()[1]
    blue_channel = image_to_encode_with.split()[2]

    encoded_image = Image.new("RGB", image_to_encode_with.size)

    x_size = image_to_encode_with.size[0]
    y_size = image_to_encode_with.size[1]

    for x in range(x_size):
        for y in range(y_size):
            if x < image_to_encode.size[0] and y < image_to_encode.size[1]:
                pixel = image_to_encode.load()[x, y]
                if pixel == (0, 0, 0):
                    binary_pixel = bin(red_channel.load()[x, y])
                    binary_pixel = binary_pixel[:-2] + '1'
                    print(binary_pixel)
                    red_pixel = int(binary_pixel[2:], 2)
            encoded_image.load()[x, y] = (red_pixel, green_channel.load()[x, y],
                                          blue_channel.load()[x, y])

    encoded_image.save("images/encoded_image.png")


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image()
