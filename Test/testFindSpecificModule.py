# importing random module
import idna

# importing the os module
import os

if __name__ == "__main__":
    # storing the path of modules file
    # in variable file_path
    file_path = idna.__file__

    # storing the directory in dir variable
    directory = os.path.dirname(file_path)
    # printing the directory
    print(directory)
