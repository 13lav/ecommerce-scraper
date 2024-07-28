import os
import requests


def download_image(image_url, save_dir='images'):
    try:
        # Create the save directory if it does not exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Extract the image file name from the URL
        image_name = os.path.basename(image_url)
        image_path = os.path.join(save_dir, image_name)

        # Send a GET request to the image URL
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Check if the request was successful

        # Write the image content to a file
        with open(image_path, 'wb') as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                image_file.write(chunk)

        print(f"Image downloaded: {image_path}")
        return image_path

    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
        return None
