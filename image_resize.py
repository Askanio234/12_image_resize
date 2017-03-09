import argparse
import os
from PIL import Image


def load_image(path_to_original):
    if os.path.exists(path_to_original):
        image = Image.open(path_to_original)
        return image
    else:
        print("Некорректный путь к файлу")


def indentify_parameters_of_resize(image, args):
    original_width, original_height = image.size
    original_proportions = round(original_width/original_height, 1)
    default_scale = 1
    if args.scale is not None:
        return original_width, original_height, args.scale
    if (args.height and args.width) is not None:
        if (args.width / args.height) != original_proportions:
            print("Введеные параметры не соответсвуют оригинальному"
                    "соотношению({})".format(original_proportions))
            return args.width, args.height, default_scale
    if args.height is not None:
        new_width = args.height * original_proportions
        return new_width, args.height, default_scale
    if args.width is not None:
        new_height = args.width / original_proportions
        return args.width, new_height, default_scale
    else:
        return original_width, original_height, default_scale


def resize_image(image, width, height, scale):
    return image.resize((int(width*scale), int(height*scale)))


def save_rezised_image(resized_image, path_to_outfile, path_to_original):
    if path_to_outfile is not None:
        resized_image.save(path_to_outfile)
    else:
        resized_image.save("{}_{}x{}.jpg".format(
                            path_to_original.split(".")[0],
                            resized_image.size[0],
                            resized_image.size[1]))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Путь к оригинальному файлу")
    parser.add_argument("--height", help="Высота", type=int)
    parser.add_argument("--width", help="Ширина", type=int)
    parser.add_argument("--scale", help="Масштаб", type=float)
    parser.add_argument("--output", help="Путь к измененному файлу")
    args = parser.parse_args()
    if (args.scale is not None) and (args.scale <= 0):
        raise ValueError("Масштаб не может быть меньше нуля!")
    if args.scale and (args.height or args.width):
        raise ValueError("Надо указать либо масштаб либо высоту с шириной!")

    return args


if __name__ == '__main__':
    args = get_args()
    image = load_image(args.input)
    width, height, scale = indentify_parameters_of_resize(image, args)
    new_image = resize_image(image, width, height, scale)
    image.close()
    save_rezised_image(new_image, args.output, args.input)
