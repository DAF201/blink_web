import base64
from PIL import Image
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


def extract_binary_data_from_image_object(image: Image.Image, format: str = 'PNG') -> bytes:
    try:
        byte_buffer = io.BytesIO()
        image.save(byte_buffer, format=format)
        return byte_buffer.getvalue()
    except:
        return b''
    finally:
        byte_buffer.close()
        gc.collect()


def blink_in_encode(data) -> bytes:
    data = base64.b64encode(data)
    image_size = factors(len(data))
    data_image = Image.new('L', image_size, (255))
    data_image_pixels = data_image.load()
    counter = 0
    for x in range(data_image.size[0]):
        for y in range(data_image.size[1]):
            data_image_pixels[x, y] = data[counter]
            counter = counter+1
    gc.collect()
    return extract_binary_data_from_image_object(data_image)


def blink_in_decode(data) -> bytes:
    byte_buffer = io.BytesIO(data)
    data_image = Image.open(byte_buffer)
    data_image_pixels = data_image.load()
    data_buffer = []
    for x in range(data_image.size[0]):
        for y in range(data_image.size[1]):
            data_buffer.append(data_image_pixels[x, y])
    data_buffer = base64.b64decode(bytes(data_buffer))
    gc.collect()
    return data_buffer
