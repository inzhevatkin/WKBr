from WKBr import find_wkb_ef
from Compare2 import return_coordinates, prepare_data
# from math import pi, sin, asin

path = "C:/Users/konstantin/Documents/main-script/Test (Focus)/"
output = path + "wkbr.dat"
f1 = open(path + "focus1.dat", 'w')
f2 = open(path + "focus2.dat", 'w')
f3 = open(path + "change_sign.dat", 'w')
f4 = open(path + "double_solution_region.dat", 'w')
grid_path = path + "scattnlay-100-1.1-500.dat"
grid_path_prepered = path + "scattnlay-100-1.1-500_prepered.dat"
prepare_data(grid_path, grid_path_prepered, "scattnlay", "x-section", 0, R_determine=True, R=50)
x, y, z = return_coordinates(grid_path_prepered, type="adda")
find_wkb_ef(x, y, z, m=1.3, mi=0, radius=50, k=1, path=output, grid=300, type="complex_wkbr", find_grid=False,
            solution_method="iterative", focus1=f1, focus2=f2, change_sign=f3, double_solution_region=f4)
f1.close()
f2.close()
f3.close()
f4.close()


