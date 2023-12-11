from PIL import Image, ImageDraw


def crop_to_circle(input_path):
    # Open the image
    original_image = Image.open(input_path)
    # Create a circular mask
    mask = Image.new('L', original_image.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = original_image.size
    draw.ellipse((0, 0, width, height), fill=255)

    # Apply the circular mask to the image
    circular_image = Image.new('RGBA', original_image.size)
    circular_image.paste(original_image, mask=mask)

    # Save the result
    return circular_image
