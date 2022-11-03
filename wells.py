
class WellReader():
    def __init__(self, file):
        self.file = file
        # pass

    def createList(self):       # from txt file create list of wells with coordinates
        with open(self.file) as f:
            lines = [line.strip() for line in f]
        lines = [line.split('\t') for line in lines]
        # lines = [col.replace(',', '.') for line in lines for col in line]
        # lines = [lines[line][col].replace(",", ".") for line in range(len(lines)) for col in range(len(lines[line]))]

        for line in range(len(lines)):
            for col in range(len(lines[line])):
                lines[line][col] = lines[line][col].replace(",", ".")
            # print(lines[line])
        return lines

    def linkToGrid(self, xllcorner, yllcorner, nrows, cellsize):       # link wells to grid coordinates
        wellsList = WellReader.createList(self)
        i = 0
        for row in wellsList:
            xIndxWell = round((float(row[0]) - xllcorner) / cellsize)       # Cell index in grid array
            # yIndxWell = round((float(row[1]) - yllcorner) / cellsize)
            yIndxWell = (nrows-1) - (round((float(row[1]) - yllcorner) / cellsize))     # Reverse index in array for y-coordinate for the further saving into file
            newX = xllcorner + cellsize * xIndxWell
            newY = yllcorner + cellsize * round((float(row[1]) - yllcorner) / cellsize)
            wellsList[i] = [newX, newY, wellsList[i][2], xIndxWell, yIndxWell]
            i += 1
        # print(wellsList)
        return wellsList

    '''
    def saveWells(self, file_name):

        with open(file_name, 'w') as file:
            file.writelines('\t'.join(str(j) for j in i) + '\n' for i in self)

        """
        with open(file_name, "w") as f:
            for line in array:
                f.write(line)
        """
    '''