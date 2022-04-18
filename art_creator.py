from PIL import Image, ImageDraw, ImageChops
import random
import colorsys


def random_color():
    h = random.random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]
    return tuple(rgb)


def interpolate(start_color, end_color, factor: float):
    recip = 1-factor
    return(int(start_color[0] * recip + end_color[0] * factor),
           int(start_color[1] * recip + end_color[1] * factor),
           int(start_color[2] * recip + end_color[2] * factor))


def draw(path: str):
    print("Drawing...")
    target_size_px = 256
    scale_factor = 2
    image_size_px = target_size_px * scale_factor
    padding = 12 * scale_factor
    image_bg_color = (0, 0, 0)
    start_color = random_color()
    end_color = random_color()
    image = Image.new("RGB",
                      size=(image_size_px, image_size_px),
                      color=image_bg_color)

    # draw some lines
    points = []

    # Generate the points
    for _ in range(10):
        random_point = (random.randint(padding, image_size_px-padding),
                        random.randint(padding, image_size_px-padding))
        points.append(random_point)

    # Bounding box
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    # Center the image
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)

    for _, point in enumerate(points):
        points[_] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    # Draw the points
    thickness = 0
    n_points = len(points) - 1
    for _, point in enumerate(points):

        # Overlay canvas
        overlay_image = Image.new("RGB",
                                  size=(image_size_px, image_size_px),
                                  color=image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point
        if _ == n_points:
            p2 = points[0]
        else:
            p2 = points[_ + 1]
        thickness += scale_factor
        color_factor = _ / n_points
        line_color = interpolate(start_color, end_color, color_factor)

        overlay_draw.line((p1, p2), fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((target_size_px, target_size_px), resample=Image.ANTIALIAS)
    image.save(path)


if __name__ == "__main__":
    for i in range(10):
        draw(path=f"output files/test_image_{i}.png")
