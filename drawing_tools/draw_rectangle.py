from PIL import Image, ImageDraw

def draw_rectangle(image_path, output_path, top_left, bottom_right, color, width):
    # Open an image file
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        # Draw a rectangle
        for i in range(width):
            draw.rectangle([top_left, bottom_right], outline=color)
            top_left = (top_left[0] + 1, top_left[1] + 1)
            bottom_right = (bottom_right[0] - 1, bottom_right[1] - 1)
        # Save the image
        img.save(output_path)

# Example usage
draw_rectangle(
    image_path='input_image.jpg',
    output_path='output_image.jpg',
    top_left=(50, 50),
    bottom_right=(200, 200),
    color='red',
    width=5
)