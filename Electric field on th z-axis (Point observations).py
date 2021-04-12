

if __name__ == "__main__":
    my_abs_tol = 0.01
    size = 200
    radius=size/2
    grid = 320
    xp = 0
    yp = 0.31348
    m = 1.145

    for type in ["wkbr"]: #, "wkb", "wkbr"
        print("Current type: ", type)
        path_main = "C:/Users/konstantin/Documents/main-script/"
        path_to_dir = path_main + "data size " + str(size) + ", grid " + str(grid) + ", section/"
        path_to_file = path_to_dir + type + "-" + str(size) + "-" + str(m) + "-" + str(grid) + ".dat"

