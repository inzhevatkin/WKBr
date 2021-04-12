from Compare2 import scattnlay_bhfield_to_adda, return_coordinates, point_field
from WKBr import find_wkb_ef
from math import isclose
import os
import shutil

# This code prepares the electric field at a given point and outputs it to a file depending on the p parameter.

if __name__ == "__main__":
    my_abs_tol = 0.01
    size = 200
    radius=size/2
    grid = 320
    xp = 0
    yp = 50.47
    zp = 0.3134

    for type in ["wkbr"]: #, "wkb", "wkbr"
        print("Current type: ", type)
        path_main = "C:/Users/konstantin/Documents/main-script/"
        path_bash = path_main + "main-section-python.sh"
        path_to_file = path_main + "data size " + str(size) + ", grid " + str(grid) + ", section/"
        path3 = path_to_file + type + "-ElField" + str(size) + "-" + "1-1.2" + "-" + str(grid) + ".dat"
        m = 1
        flag = True
        step = 0.001
        while m < 1.2:
            m += step
            m = round(m, 3)
            print("Current m = ", m)
            if type == "bhfield" or type == "scattnlay":
                command = path_bash + ' ' + str(size) + ' ' + str(grid) + ' ' + str(radius) + ' ' + str(m) + ' ' + type
                os.system(command)  # генерация точного поля
                path_exact_tmp = path_main + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
                path_exact = path_to_file + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
                shutil.move(path_exact_tmp, path_exact)
                path2 = path_to_file + type + "-adda-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
                scattnlay_bhfield_to_adda(path_exact, path2, type, size / 2, grid)
                if type == "bhfield":
                    # Delete log file:
                    os.remove(path_main + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".log")
            elif type == "wkbr":
                path2 = path_to_file + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
                path_mie_adda = path_to_file + "bhfield-adda-" + str(size) + "-1.2-" + str(grid) + ".dat"
                x, y, z = return_coordinates(path_mie_adda, type="adda")
                find_wkb_ef(x, y, z, m, 0, radius, 1, path2, grid, type="wkb+refraction12")
            elif type == "wkb":
                path2 = path_to_file + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
                path_mie_adda = path_to_file + "bhfield-adda-" + str(size) + "-1.2-" + str(grid) + ".dat"
                x, y, z = return_coordinates(path_mie_adda, type="adda")
                find_wkb_ef(x, y, z, m, 0, radius, 1, path2, grid)
            else:
                print("Error! Undefined type. ")

            if flag:
                flag = False
                f2 = open(path3, 'w')
                f2.write('x y z m |E_av| exr_av exi_av eyr_av eyi_av ezr_av ezi_av dots_number \n')
                point_field(path2, f2, xp, yp, zp, my_abs_tol, m)
            else:
                point_field(path2, f2, xp, yp, zp, my_abs_tol, m)
        f2.close()











