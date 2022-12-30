import base64
from PIL import Image
import hashlib
import gc
import io


def factors(num):
    def is_prime(x):
        if (x == 2) or (x == 3):
            return True
        if (x % 6 != 1) and (x % 6 != 5):
            return False
        for i in range(5, int(x ** 0.5) + 1, 6):
            if (x % i == 0) or (x % (i + 2) == 0):
                return False
        return True

    if is_prime(num):
        return (1, num)
    else:
        start = int(pow(num, 0.5))
        if start < num-start:
            while (num % start != 0):
                start -= 1
            return (start, int(num/start))
        else:
            while (num % start != 0):
                start += 1
            return (start, int(num/start))


class Blink_in():
    def __init__(self, data):
        self.data = data
        self.size = [0, 0]
        self.file_encode()

    def file_encode(self):
        self.__convert__()
        self.__image_filling__()

    def __convert__(self):
        try:
            self.data = base64.b64encode(self.data)
            self.size = factors(len(self.data))
            self.image = Image.new('L', self.size, (255))
            self.image_pixels = self.image.load()
        except:
            pass

    def __image_filling__(self):
        try:
            counter = 0
            for x in range(self.image.size[0]):
                for y in range(self.image.size[1]):
                    self.image_pixels[x, y] = self.data[counter]
                    counter = counter+1
        except:
            pass

    @classmethod
    def extract_binary_data_from_image_object(self, image: Image.Image, format: str = "PNG") -> bytes:
        byte_buffer = io.BytesIO()
        image.save(byte_buffer, format=format)
        return byte_buffer.getvalue()


with open(r"C:\Users\daf20\Documents\GitHub\blink_web_en\test.png", 'rb')as test_file:
    encoded_image = Blink_in(test_file.read()).image

with open("TEST_SAVE.png", "rb")as test_image:
    print(Blink_in.extract_binary_data_from_image_object(
        encoded_image) == test_image.read())


# encoded_image.save("TEST_SAVE.png")









# DECODE


# encoded = Image.open("TEST_SAVE.png")
# pixels = encoded.load()
# byte_map = []

# for x in range(encoded.size[0]):
#     for y in range(encoded.size[1]):
#         byte_map.append(pixels[x, y])

# with open("TEST_RES.png", "wb")as test_result:
#     byte_map = base64.b64decode(bytes(byte_map))
#     test_result.write(byte_map)
