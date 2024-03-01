from PIL import Image
import imagehash
import os

def find_similar_image(ref_picture, folder_path, output_file):
    # Read the smaller image
    smaller_image = Image.open(ref_picture)

    # Compute the hash of the smaller image
    smaller_hash = imagehash.average_hash(smaller_image)

    # Get the horizontally flipped version of the smaller image
    smaller_flipped_image = smaller_image.transpose(Image.FLIP_LEFT_RIGHT)
    smaller_flipped_hash = imagehash.average_hash(smaller_flipped_image)

    # Get the total number of files in the folder
    total_files = len([f for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg"))])

    # Initialize a counter for the processed files
    processed_files = 0

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # Compute the hash of the original image
            original_image_path = os.path.join(folder_path, filename)
            original_hash = imagehash.average_hash(Image.open(original_image_path))

            # Compare the hashes
            hash_difference_original = smaller_hash - original_hash
            hash_difference_flipped = smaller_flipped_hash - original_hash

            # Define a threshold for similarity
            threshold = 10  # Adjust as needed

            # Check if either the original or flipped image has a hash difference below the threshold
            if hash_difference_original < threshold or hash_difference_flipped < threshold:
                print(f"Matching image found: {filename}")
                
                # Append the filename to the output file
                with open(output_file, 'a') as file:
                    file.write(f"{filename}\n")

        # Increment the processed files counter
        processed_files += 1

        # Print the progress percentage on the same line
        progress_percentage = (processed_files / total_files) * 100
        print(f"\rProgress: {progress_percentage:.2f}%", end='', flush=True)

    print("\nSearch complete.")


# Example usage
ref_picture = "path/to/image.jpg"
folder_path = "path/to/folder" #no '/' at the end
output_file = "path/to/file/"

find_similar_image(ref_picture, folder_path, output_file)
