from maya import cmds 
import csv
import random
import os
import sys

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")

class LegoColors(object):
    def __init__(self):
        os.chdir("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")
        
        with open('maya_lego_plugin\\colors.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]

        self.colors = data

    def get_random_color(self):
        rand = random.randint(0, len(self.colors) - 1)
        return self.colors[rand]

    def get_colors(self):
        return self.colors