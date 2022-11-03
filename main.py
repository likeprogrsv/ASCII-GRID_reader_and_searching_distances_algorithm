# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import numpy as np
import linecache
import wells
from numpy import *

gotRiverbed = False
searchingCatchmentAreaValue = 5e+6
distancesArr = []

# N = 1
# print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
# print("PATH:", os.environ.get('PATH'))

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def readASCIIgrid(file):
    global ascii_Array, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value

    ascii_Array = np.loadtxt(file, skiprows=6)

    ncols = int(get_parameters(file, 1))
    nrows = int(get_parameters(file, 2))
    xllcorner = float(get_parameters(file, 3))
    yllcorner = float(get_parameters(file, 4))
    cellsize = float(get_parameters(file, 5))
    NODATA_value = float(get_parameters(file, 6))


def get_parameters(ascFile, parameterLine):
    return linecache.getline(ascFile, parameterLine).split()[1]




def circle_searching(n, well_arr):
    global gotRiverbed, searchingCatchmentAreaValue
    # Find the unique distances
    X,Y = meshgrid(arange(n), arange(n))
    G = sqrt(X**2+Y**2)
    U = unique(G)

    # Identify these coordinates
    blocks = [[pair for pair in zip(*where(G==idx))] for idx in U if idx < n / 2]

    # Permute along the different orthogonal directions
    directions = np.array([[1,1],[-1,1],[1,-1],[-1,-1]])

    all_R = []
    for b in blocks:
        R = set()
        for item in b:
            for x in item*directions:
                R.add(tuple(x))

        R = np.array(list(R))

        # Sort by angle
        T = np.array([arctan2(*x) for x in R])
        R = R[argsort(T)]
        all_R.append(R)

    if len(all_R) > 1:
        #print('%s, %s' % (list[-2], list[-1]))
        for array in all_R:
            for item in array:
                col_currnt = well_arr[3] + item[0]      # current column index
                row_currnt = well_arr[4] + item[1]      # current row index
                if col_currnt < 0 or row_currnt < 0:
                    col_currnt, row_currnt = 0, 0
                if col_currnt > ascii_Array.shape[1] - 1:
                    col_currnt = ascii_Array.shape[1] - 1
                if row_currnt > ascii_Array.shape[0] - 1:
                    row_currnt = ascii_Array.shape[0] - 1

                if ascii_Array[row_currnt, col_currnt] > searchingCatchmentAreaValue:
                    print(f'Riverbed found in cell with index [{row_currnt}, {col_currnt}] '
                          f'and catchment area is {ascii_Array[row_currnt, col_currnt]}. Well number {well_arr[2]}, step N = {n}')
                    riverCellCoord = getCellCoord(row_currnt, col_currnt)

                    #

                    """
                    # distances = nex X-coord well;  new Y-coord well;  well name;  catchment area at well point;
                    #               searched riverbed cell X, Y -coordinate of current well;    name of riverbed cell;
                    #               catchment area of searched riverbed cell;   distance between well and searched cell.
                    """

                    dist = [well_arr[0], well_arr[1], well_arr[2], ascii_Array[well_arr[4], well_arr[3]], riverCellCoord[0],
                                 riverCellCoord[1], f'riverbed_well_{well_arr[2]}', ascii_Array[row_currnt, col_currnt],
                                 distance(well_arr, riverCellCoord)]

                    distancesArr.append(dist)


                    gotRiverbed = True
                    break
            if gotRiverbed == True:
                break



def printGridParams():
    print("_______________""\nncols %s" % ncols + "\nnrows %s" % nrows + "\nxllcorner %s" % xllcorner
          + "\nyllcorner %s " % yllcorner + "\ncellsize %s" % cellsize + "\nNODATA_value %s" % NODATA_value + "\n_______________")


def getCellCoord(row, col):
    return [col * cellsize + xllcorner, ((nrows - 1) - row) * cellsize + yllcorner]


def distance(well, searchedPoint):
    return math.hypot(searchedPoint[0] - well[0], searchedPoint[1] - well[1])


def saveToFile(arr, file_name):
    with open(file_name, 'w') as file:
        file.writelines('\t'.join(str(j) for j in i) + '\n' for i in arr)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    readASCIIgrid("!!!Flow_Accumulation_MODIFIED_METHOD_Article.asc")
    printGridParams()

    # wellsList = wells.WellReader('RIVERBED_wells_lithofacies_tevlin_u2.txt').createList()
    # RIVERBED_wells_lithofacies_tevlin_u2.txt  ||  TESTwells.txt
    wellsLinked = wells.WellReader('RIVERBED_wells_lithofacies_tevlin_u2.txt').linkToGrid(xllcorner, yllcorner, nrows, cellsize)

    # Searching nearest to well a riverbed and calculate the distance
    for well in wellsLinked:
        N = 200
        gotRiverbed = False
        while not gotRiverbed:
            circle_searching(N, well)
            N += N
    print(distancesArr)

    saveToFile(distancesArr, 'distances_Modified_version.txt')