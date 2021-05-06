from Compare2 import return_coordinates, scattnlay_bhfield_to_adda, compare
from WKBr import find_wkb_ef, BoundaryLines
import os

# This file main3 (Numerical investigation).py  is needed to find the average error for a section / particle.

size = 100
grid = 160
type = "bhfield"  # "bhfield" #"scattnlay"  # "WKB from ADDA" #  #  scattnlay "bhfield" #
m = [1.01, 1.05, 1.1, 1.2, 1.3]  # 1.01, 1.05, 1.1, 1.2, 1.3
m_im = 0  # 0.01
# path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + ", section/"
path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + " (clear)/"
# path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + ", section (clear)/"

if __name__ == "__main__":
    for version in ["v16"]: # "wkb", "v1", "v2", "v5", "v12", "v7", "v13", "v13-2", "v15", "v16"
        if version == "wkb":
            f0 = open(path + "dE-sc-wkb" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f0.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v1":
            f1 = open(path + "dE-sc-wkbr (v1)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f1.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v2":
            f2 = open(path + "dE-sc-wkbr (v2)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f2.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v7":
            f7 = open(path + "dE-sc-wkbr (v7)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f7.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v4":
            f4 = open(path + "dE-sc-wkbr (v4)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f4.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v5":
            f5 = open(path + "dE-sc-wkbr (v5)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f5.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v11":
            f11 = open(path + "dE-sc-wkbr (v11)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f11.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v12":
            f12 = open(path + "dE-sc-wkbr (v12)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f12.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                     "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v13":
            f13 = open(path + "dE-sc-wkbr (v13)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f13.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                      "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v13-2":
            f13_2 = open(path + "dE-sc-wkbr (v13-2)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f13_2.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                      "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v15":
            f15 = open(path + "dE-sc-wkbr (v15)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f15.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                      "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        elif version == "v16":
            f16 = open(path + "dE-sc-wkbr (v16)" + str(size) + "-" + "all" + "-" + str(grid) + ".dat", 'w')
            f16.write("m <dE_l2> <dE_one_root_l2> <dE_two_root_l2> <dE_no_root_l2> " +
                      "<dE_l1> <dE_one_root_l1> <dE_two_root_l1> <dE_no_root_l1> \n")
        for i in m:
            print("Current size = ", size)
            print("Current grid = ", grid)
            print("Current m = ", i)
            print("Current version: ", version)
            # tail = str(size) + "-" + str(i) + "-" + str(m_im) + "-" + str(grid) + ".dat"

            if m_im != 0:
                tail = str(size) + "-" + str(i) + "-" + str(m_im) + "-" + str(grid) + ".dat"
            else:
                tail = str(size) + "-" + str(i) + "-" + str(grid) + ".dat"

            # Let's create a class object that will constrain regions.
            lines = BoundaryLines(i)
            pathsc = path + type + "-" + tail
            pathsc_adda = path + type + "-adda-" + tail
            pathmywkb = path + "wkb-" + tail
            if type == "bhfield" or type == "scattnlay":
                scattnlay_bhfield_to_adda(pathsc, pathsc_adda, type, size / 2, grid)
                x, y, z = return_coordinates(pathsc_adda, type="adda")
                '''
                if not os.path.exists(pathsc_adda):
                    x, y, z = return_coordinates(pathsc_adda, type="adda")
                else:
                    scattnlay_bhfield_to_adda(pathsc, pathsc_adda, type, size / 2, grid)
                    x, y, z = return_coordinates(pathsc_adda, type="adda")
                '''
            elif type == "WKB from ADDA":
                x, y, z = return_coordinates(pathsc, type="adda")
            if version == "wkb":
                if type == "WKB from ADDA":
                    pathsc_adda = pathsc
                path_wkb = path + "wkb-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, pathmywkb, grid)
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root,\
                    aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb, i, lines, size / 2)
                f0.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v1":
                # Simple WKBr.
                path_wkb_refraction = path + "wkb_refraction (v1)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction, grid, type="wkb+refraction")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root,\
                    aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction, i, lines, size / 2)
                f1.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v2":
                # WKBr with rotation of the electric field.
                path_wkb_refraction2 = path + "wkb_refraction (v2)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction2, grid, type="wkb+refraction6")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root,\
                    aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction2, i, lines, size / 2)
                f2.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v5":
                # WKBr with rotation of the electric field + Fresnel transmission coefficients.
                path_wkb_refraction5 = path + "wkb_refraction (v5)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction5, grid, type="wkb+refraction14")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root, \
                aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction5, i, lines, size / 2)
                f5.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v12":
                # Everything is the same as in WKBr v.2, but here we account for "convergence factor", Fresnel coefficient.
                path_wkb_refraction12 = path + "wkb_refraction (v12)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction12, grid, type="wkb+refraction12")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root, \
                aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction12, i, lines, size / 2)
                f12.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v7":
                # WKBr sums the electric field in the double solution region.
                path_wkb_refraction7 = path + "wkb_refraction (v7)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction7, grid, type="wkb+refraction7")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root,\
                    aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction7, i, lines, size / 2)
                f7.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v13":
                # WKBr sums the electric field in the double solution region.
                # It also account for additional phase pi/2.
                path_wkb_refraction13 = path + "wkb_refraction (v13)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction13, grid, type="wkb+refraction13")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root,\
                    aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction13, i, lines, size / 2)
                f13.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v13-2":
                # WKBr sums the electric field in the double solution region.
                # It also account for additional phase pi/2.
                path_wkb_refraction13_2 = path + "wkb_refraction (v13-2)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction13_2, grid, type="wkb+refraction13-2")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root,\
                    aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction13_2, i, lines, size / 2)
                f13_2.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v4":
                path_wkb_refraction4 = path + "wkb_refraction (v4)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction4, grid, type="wkb+refraction8")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root,\
                    aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction4, i, lines, size / 2)
                f4.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v11":
                # Everything is the same as in WKBr v.2, but here we account for "convergence factor".
                path_wkb_refraction11 = path + "wkb_refraction (v11)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction11, grid, type="wkb+refraction11")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root, \
                aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction11, i, lines, size / 2)
                f11.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v15":
                # Version 1.
                # R1 - use one solution. R2 - sum. R0 - use zero solution.
                path_wkb_refraction15 = path + "wkb_refraction (v15)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction15, grid, type="wkb+refraction15")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root, \
                aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction15, i, lines, size / 2)
                f15.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')
            elif version == "v16":
                # Version 3.
                # R1 - use one solution. R2 - sum, rotation, transmission coefficients. R0 - zero.
                path_wkb_refraction16 = path + "wkb_refraction (v16)-" + tail
                find_wkb_ef(x, y, z, i, m_im, size / 2, 1, path_wkb_refraction16, grid, type="wkb+refraction16")
                aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root, \
                aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root = \
                    compare(pathsc_adda, path_wkb_refraction16, i, lines, size / 2)
                f16.write(str(i) + ' ' +
                         str(aver_error_l2) + ' ' +
                         str(aver_error_l2_one_root) + ' ' +
                         str(aver_error_l2_two_root) + ' ' +
                         str(aver_error_l2_no_root) + ' ' +
                         str(aver_error_l1) + ' ' +
                         str(aver_error_l1_one_root) + ' ' +
                         str(aver_error_l1_two_root) + ' ' +
                         str(aver_error_l1_no_root) + ' ' + '\n')

        if version == "wkb":
            f0.close()
        elif version == "v1":
            f1.close()
        elif version == "v2":
            f2.close()
        elif version == "v7":
            f7.close()
        elif version == "v4":
            f4.close()
        elif version == "v5":
            f5.close()
        elif version == "v11":
            f11.close()
        elif version == "v12":
            f12.close()
        elif version == "v13":
            f13.close()
        elif version == "v13-2":
            f13_2.close()
        elif version == "v15":
            f15.close()
        elif version == "v16":
            f15.close()




