from PIL import Image

def resize_image(image_path, output_path, new_width, new_height):
    # Open the image
    image = Image.open(image_path)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)  # Using ANTIALIAS filter

    # Save the resized image
    resized_image.save(output_path)


# Example usage
input_image = "./static/place-holder.PNG"
output_image = "./static/somefuture.png"
crop_width = 200
crop_height = 125
