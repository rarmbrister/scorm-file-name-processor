import os
import re
import zipfile
import shutil
import time
import sys


# ├── _app
# │   ├── app.py
# │   ├── zipped
# │   ├── processed


# define path seperator "\" for windows and "/"" for other operating systems
if sys.platform == "Windows":
    path_separator = "\\"
else:
    path_separator = "//"


# Function takes file name, extracts name and extension,
# then removes non-alphaneumeric characters
# and returns processed new_name (with extension), name (without extension),
# and the old_name (without extension)
def process_file(file_name):
    # split file name by "." and add strings to a list
    list = file_name.split(".")

    # define file extension
    extension = "." + list[-1]

    # save current file name before renaming
    old_name = ".".join(list[: len(list) - 1])  #

    # create new file name without extension
    name = re.sub(r"\W+", "_", old_name)

    # add extension to new file name
    new_name = name + extension

    # add extension to old file name
    old_name = old_name + extension

    # return new name with extension, new name without extension and old_name without extension.
    return new_name, name, old_name


# path used when developed on windows machine
# alpha = r"C:\Users\rxa877\Documents\alpha"


def main():
    app_directory = r"/Users/rarmbrister/Downloads/alpha"

    # define folder where processed file(s) will be stored without alphanumeric characters in the name(s)
    processed = f"{path_separator}processed"

    # define folder where you will place file(s) which contain alphanumeric characters to be processed later
    zipped = f"{path_separator}zipped"

    os.chdir(app_directory + zipped)

    print("Processing....")

    for file in os.listdir():

        # ensure that folder is not the Apple Desktop Services Store folder.
        if file != ".DS_Store":
            file = process_file(file)

            with zipfile.ZipFile(
                f"{app_directory}{zipped}{path_separator}{file[2]}", "r"
            ) as zip_ref:
                os.mkdir(f"{app_directory}{processed}{path_separator}{file[1]}")
                zip_ref.extractall(
                    f"{app_directory}{processed}{path_separator}{file[1]}"
                )

            for inner_file in os.listdir(
                f"{app_directory}{processed}{path_separator}{file[1]}"
            ):
                new_inner_file = process_file(inner_file)
                os.rename(
                    f"{app_directory}{processed}{path_separator}{file[1]}{path_separator}{inner_file}",
                    f"{app_directory}{processed}{path_separator}{file[1]}{path_separator}{new_inner_file[0]}",
                )

    os.chdir(app_directory + processed)

    for file in os.listdir():
        # ensure that folder is not the Apple Desktop Services Store folder.
        if file != ".DS_Store":
            # create an archive file
            shutil.make_archive(file, "zip", file)
            
            # delete an directory tree of unzziped file
            shutil.rmtree(file)

    print("Complete.")


main()
