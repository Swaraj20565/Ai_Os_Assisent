import os

def find_file(filename):

    search_path = "C:/Users"
    matched_files = []

    for root, dirs, files in os.walk(search_path):

        for file in files:

            if (
                filename.lower() in file.lower()
                and not file.endswith(".lnk")
            ):

                matched_files.append(os.path.join(root, file))

    return matched_files