from Compare2 import point_field, return_coordinates, scattnlay_bhfield_to_adda

if __name__ == "__main__":
    my_abs_tol = 0.01
    size = 200
    radius = size / 2
    grid = 320
    xp = 0
    yp = 0.31348
    m = 1.145
    path_main = "C:/Users/konstantin/Documents/main-script/"
    path_to_dir = path_main + "data size " + str(size) + ", grid " + str(grid) + ", section/"
    path_write = path_to_dir

    for type in ["wkbr", "wkb", "bhfield"]:  # "wkbr"
        print("Current type: ", type)
        if type == "bhfield":
            path_to_file = path_to_dir + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
            path_to_file2 = path_to_dir + type + "-adda-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
            scattnlay_bhfield_to_adda(path_to_file, path_to_file2, type, size / 2, grid)
            path_to_file = path_to_file2
        else:
            path_to_file = path_to_dir + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
        x, y, z = return_coordinates(path_to_file, type="adda")
        flag = True
        prev = 0
        for zp in z:
            cur = zp
            if cur == prev:
                continue
            print("Current z: ", zp)
            if flag:
                flag = False
                path_write += type + '-field-x' + str(xp) + '-y' + str(yp) + '.dat'
                f2 = open(path_write, 'w')
                f2.write('x y z m |E_av| exr_av exi_av eyr_av eyi_av ezr_av ezi_av dots_number \n')
                point_field(path_to_file, f2, xp, yp, zp, my_abs_tol, m)
            elif flag is False:
                point_field(path_to_file, f2, xp, yp, zp, my_abs_tol, m)
            else:
                print("Error! flag is not defined.")
            prev = cur
