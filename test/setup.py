""" 
This file creates the installation file for the firmware

It does the following:
1. Creates a folder named "main" in the root directory
2. Creates a filed named main.ino in the "main" folder
3. Copies the contents of all .h, .cpp and .ino file in the "meter" folder to the "main.ino" file
4. deletes all #include header.h from the "main.ino" file
"""

import os
import shutil
import re

def main():
    # Create the main folder
    if not os.path.exists("main"):
        os.makedirs("main")

    # Create the main.ino file
    with open("main/main.ino", "w") as main_file:
        # Get all the files in the meter folder
        for file in os.listdir("meter"):
            # Check if the file is a header file
            if file.endswith(".h") or file.endswith(".cpp") or file.endswith(".ino"):
                # Open the file and copy the contents to the main.ino file
                with open(f"meter/{file}", "r") as f:
                    for line in f:
                        # Remove all "#include header.h" statements
                        if not re.match(r"#include header.h", line):
                            main_file.write(line)
    
    # Copy the main.ino file to the main folder
    shutil.copy("main/main.ino", "main.ino")
    print("main.ino file created successfully")

if __name__ == "__main__":
    main()