from PIL import Image, ImageDraw, ImageFont
import os
import time
import random


def render_carriage(scheme, available = [], place_size = 90):
    padding = place_size / 15
    random.seed(time.time())
    script_dir = os.path.dirname(__file__)
    filename = "{}/carriages/{}.gif".format(script_dir, random.randint(0, 999_999_999))

    carriage_size = scheme['model']['floor']['1']
    places = scheme['places']['floor']['1']

    width = carriage_size['width'] * place_size
    height = carriage_size['height'] * place_size

    places_offset_x = place_size * 2
    places_offset_y = place_size

    wall_width = place_size / 30

    image_width = int(width + places_offset_x * 2 - padding + place_size)
    image_height = int(height + places_offset_y * 2 - padding)
    image = Image.new('RGBA', (image_width, image_height), (255,255,255,0))
    draw = ImageDraw.Draw(image)

    # Draw outline
    rounded_rectangle(
        draw, 
        xy=(
            (places_offset_x - padding / 2 - place_size, places_offset_y - place_size / 4), 
            (places_offset_x - padding / 2 + width + place_size, places_offset_y + height - padding + place_size / 4)
        ),
        corner_radius=35,
        fill=(237,240,244)
    )
    
    # Draw places
    for place in places:
        place_x = (place['x'] - 1) * place_size + places_offset_x
        place_y = (place['y'] - 1) * place_size + places_offset_y

        if place['type'] == 'place':
            place_width = place['w']
            place_height = place['h']
            place_num = place['num']
            
            headrest = None
            if 'headrest' in place:
                headrest = place['headrest']
            elif 'pos' in place:
                if place['pos'] == 'up':
                    headrest = 'top'
                else:
                    headrest = 'bottom'

            font = ImageFont.truetype("{}/resources/{}".format(script_dir, "Roboto-Regular.ttf"), int(place_size / 2.2))
            text_size = font.getsize(place_num)

            border_color = (67,102,130)
            border_width = place_size / 10
            border_corner_radius = place_size / 15

            rounded_rectangle(
                draw,
                xy=(
                    (place_x + padding, place_y + padding),
                    (place_x + place_width * place_size - padding * 2, place_y + place_height * place_size - padding * 2)
                ),
                corner_radius=border_corner_radius,
                fill=(84,127,162) if place_num in available else (0,0,0,75)
            )

            if headrest == 'left':
                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + padding, place_y + padding),
                        (place_x + padding + border_width, place_y + place_height * place_size - padding * 2)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )

                draw.text(
                    (
                        place_x + padding / 2 + border_width / 2 + (place_size - padding * 2) / 2 - text_size[0] / 2, 
                        place_y + (place_size - padding * 2) / 2 - text_size[1] / 2
                    ), 
                    place_num, 
                    (255,255,255,255), 
                    font=font
                )
            elif headrest == 'right':
                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + place_width * place_size - padding * 2 - border_width, place_y + padding),
                        (place_x + place_width * place_size - padding * 2, place_y + place_height * place_size - padding * 2)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )

                draw.text(
                    (
                        place_x + padding / 2 - border_width / 2 + (place_size - padding * 2) / 2 - text_size[0] / 2, 
                        place_y + (place_size - padding * 2) / 2 - text_size[1] / 2
                    ), 
                    place_num, 
                    (255,255,255,255), 
                    font=font
                )
            elif headrest == 'top':
                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + padding, place_y + padding),
                        (place_x + place_width * place_size - padding * 2, place_y + padding + border_width)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )

                draw.text(
                    (
                        place_x + padding / 2 + (place_size - padding * 2) / 2 - text_size[0] / 2, 
                        place_y + (place_size - padding * 2) / 2 + border_width / 2 - text_size[1] / 2
                    ), 
                    place_num, 
                    (255,255,255,255), 
                    font=font
                )
            elif headrest == 'bottom':
                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + padding, place_y + place_height * place_size - padding * 2 - border_width),
                        (place_x + place_width * place_size - padding * 2, place_y + place_height * place_size - padding * 2)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )

                draw.text(
                    (
                        place_x + padding / 2 + (place_size - padding * 2) / 2 - text_size[0] / 2, 
                        place_y + (place_size - padding * 2) / 2 - border_width / 2 - text_size[1] / 2
                    ), 
                    place_num, 
                    (255,255,255,255), 
                    font=font
                )

            if headrest == 'left' or headrest == 'right':
                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + padding, place_y + padding),
                        (place_x + place_width * place_size - padding * 2, place_y + padding + border_width)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )

                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + padding, place_y + place_height * place_size - padding * 2 - border_width),
                        (place_x + place_width * place_size - padding * 2, place_y + place_height * place_size - padding * 2)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )
            elif headrest == 'top' or headrest == 'bottom':
                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + padding, place_y + padding),
                        (place_x + padding + border_width, place_y + place_height * place_size - padding * 2)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )

                rounded_rectangle(
                    draw,
                    xy=(
                        (place_x + place_width * place_size - padding * 2 - border_width, place_y + padding),
                        (place_x + place_width * place_size - padding * 2, place_y + place_height * place_size - padding * 2)
                    ),
                    corner_radius=border_corner_radius,
                    fill=border_color if place_num in available else (0,0,0,100)
                )

        elif place['type'] == 'wall':
            place_height = place['h']

            draw.rectangle(
                [
                    place_x - padding / 2, 
                    place_y, 
                    place_x - padding / 2 + wall_width, 
                    place_y + place_height * place_size - padding
                ],
                (0,0,0,75)
            )
        elif place['type'] == 'table':
            place_width = place['w']
            place_height = place['h']

            rounded_rectangle(
                draw,
                xy=(
                    (place_x + padding, place_y + padding),
                    (place_x + place_width * place_size - padding * 2, place_y + place_height * place_size - padding * 2)
                ),
                corner_radius=(place_size / 15),
                fill=(0,0,0,50)
            )
        elif place['type'] == 'toilet':
            place_width = place['w']
            place_height = place['h']

            image_size = int(place_size - padding * 3)
            toilet_image = Image.open('{}/resources/{}'.format(script_dir, 'toilet-icon.png')).convert('RGBA')
            toilet_image = toilet_image.resize((image_size, image_size))

            image.paste(
                toilet_image, 
                (
                    int(place_x + (place_width * place_size) / 2 - image_size / 2), 
                    int(place_y + (place_height * place_size) / 2 - image_size / 2)
                ), 
                toilet_image
            )

        elif place['type'] == 'bag':
            place_width = place['w']
            place_height = place['h']

            image_size = int(place_size - padding * 3)
            toilet_image = Image.open('{}/resources/{}'.format(script_dir, 'bag-icon.png')).convert('RGBA')
            toilet_image = toilet_image.resize((image_size, image_size))

            image.paste(
                toilet_image, 
                (
                    int(place_x + (place_width * place_size) / 2 - image_size / 2), 
                    int(place_y + (place_height * place_size) / 2 - image_size / 2)
                ), 
                toilet_image
            )
        elif place['type'] == 'wheelchair':
            place_width = place['w']
            place_height = place['h']

            image_size = int(place_size - padding * 3)
            toilet_image = Image.open('{}/resources/{}'.format(script_dir, 'wheelchair-icon.png')).convert('RGBA')
            toilet_image = toilet_image.resize((image_size, image_size))

            image.paste(
                toilet_image, 
                (
                    int(place_x + (place_width * place_size) / 2 - image_size / 2), 
                    int(place_y + (place_height * place_size) / 2 - image_size / 2)
                ), 
                toilet_image
            )
        elif place['type'] == 'bar':
            place_width = place['w']
            place_height = place['h']

            image_size = int(place_size - padding * 3)
            toilet_image = Image.open('{}/resources/{}'.format(script_dir, 'bar-icon.png')).convert('RGBA')
            toilet_image = toilet_image.resize((image_size, image_size))

            image.paste(
                toilet_image, 
                (
                    int(place_x + (place_width * place_size) / 2 - image_size / 2), 
                    int(place_y + (place_height * place_size) / 2 - image_size / 2)
                ), 
                toilet_image
            )
    
    image.save(filename, "PNG")
    return filename


def rounded_rectangle(self: ImageDraw, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    self.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius)
        ],
        fill=fill,
        outline=outline
    )
    self.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1])
        ],
        fill=fill,
        outline=outline
    )
    self.pieslice([upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
        180,
        270,
        fill=fill,
        outline=outline
    )
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0,
        90,
        fill=fill,
        outline=outline
    )
    self.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
        90,
        180,
        fill=fill,
        outline=outline
    )
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
        270,
        360,
        fill=fill,
        outline=outline
    )