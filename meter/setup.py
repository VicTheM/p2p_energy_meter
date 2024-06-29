""" This file creates the installation file for the firmware """

filename = "main/main.ino"
sources = ["meter/header.h", "meter/connections.cpp", "meter/operations.cpp", "meter/meter.ino"]

with open(filename, 'w', encoding="utf-8") as mainfile:
    x = 1
    for source in sources:
        with open(source, encoding="utf-8") as fd:
            readData = fd.read()
            mainfile.write(readData)
            mainfile.write("\n\n\n")

        print("File written: {}".format(x))
        x += 1