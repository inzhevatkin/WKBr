import numpy as np
from math import isclose
import matplotlib.pyplot as plt
import scipy.interpolate
import math
from math import isnan
from Region import region, BoundaryLines
from Coordinate_systems import coordinates_in_meridional_plane
import os
from Compare2 import scattnlay_bhfield_to_adda


# path1 - путь до массива данных
# path2 - путь до места сохранения данных
# section - тип сечения которое фиксируется (x-section, y-section)
# coordinate - координата выбранного сечения
def prepare_data(path1, path2, type, section, coordinate):
    print("prepare_data ", path1, ' ', path2)
    f1 = open(path2, 'w')
    if type == "scattnlay":
        data = np.loadtxt(path1, dtype=np.float32, delimiter=", ", skiprows=1, usecols=range(9))
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        Exr = data[:, 3]
        Exi = data[:, 4]
        Eyr = data[:, 5]
        Eyi = data[:, 6]
        Ezr = data[:, 7]
        Ezi = data[:, 8]
        f1.write("x y z Ex.r Ex.i Ey.r Ey.i Ez.r Ez.i \n")
    elif type == "bhfield" or type == "adda":
        data = np.loadtxt(path1, dtype=np.float32, delimiter=" ", skiprows=1, usecols=range(10))
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        E = data[:, 3]
        Exr = data[:, 4]
        Exi = data[:, 5]
        Eyr = data[:, 6]
        Eyi = data[:, 7]
        Ezr = data[:, 8]
        Ezi = data[:, 9]
        f1.write("x y z |E|^2 Ex.r Ex.i Ey.r Ey.i Ez.r Ez.i \n")
    else:
        print("Error in prepare_data function! Not defined type.")
    L = len(x)

    if section == "y-section":
        for i in range(L):
            y_tmp = y[i]
            if isclose(y_tmp, coordinate, abs_tol=1e-2):
                if type == "scattnlay":
                    line = str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + \
                           str(Exr[i]) + ' ' + str(Exi[i]) + ' ' + \
                           str(Eyr[i]) + ' ' + str(Eyi[i]) + ' ' + \
                           str(Ezr[i]) + ' ' + str(Ezi[i]) + '\n'
                elif type == "bhfield" or type == "adda":
                    line = str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + str(E[i]) + ' ' + \
                           str(Exr[i]) + ' ' + str(Exi[i]) + ' ' + \
                           str(Eyr[i]) + ' ' + str(Eyi[i]) + ' ' + \
                           str(Ezr[i]) + ' ' + str(Ezi[i]) + '\n'
                f1.write(line)
    elif section == "x-section":
        for i in range(L):
            if isclose(x[i], coordinate, abs_tol=1e-2):
                if type == "scattnlay":
                    line = str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + \
                           str(Exr[i]) + ' ' + str(Exi[i]) + ' ' + \
                           str(Eyr[i]) + ' ' + str(Eyi[i]) + ' ' + \
                           str(Ezr[i]) + ' ' + str(Ezi[i]) + '\n'
                elif type == "bhfield" or type == "adda":
                    line = str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + str(E[i]) + ' ' + \
                           str(Exr[i]) + ' ' + str(Exi[i]) + ' ' + \
                           str(Eyr[i]) + ' ' + str(Eyi[i]) + ' ' + \
                           str(Ezr[i]) + ' ' + str(Ezi[i]) + '\n'
                f1.write(line)

    f1.close()


def find_difference(path1, path2, path3, type):
    print("find_difference ", path1, " ", path2, " ", path3)
    if type == "scattnlay":
        print("Not yet implemented.")
    elif type == "bhfield":
        data1 = np.loadtxt(path1, dtype=np.float32, delimiter=" ", skiprows=1, usecols=range(10))
        x = data1[:, 0]
        y = data1[:, 1]
        z = data1[:, 2]
        E1 = data1[:, 3]
        Exr1 = data1[:, 4]
        Exi1 = data1[:, 5]
        Eyr1 = data1[:, 6]
        Eyi1 = data1[:, 7]
        Ezr1 = data1[:, 8]
        Ezi1 = data1[:, 9]

        data2 = np.loadtxt(path2, dtype=np.float32, delimiter=" ", skiprows=1, usecols=range(10))
        E2 = data2[:, 3]
        Exr2 = data2[:, 4]
        Exi2 = data2[:, 5]
        Eyr2 = data2[:, 6]
        Eyi2 = data2[:, 7]
        Ezr2 = data2[:, 8]
        Ezi2 = data2[:, 9]
    f3 = open(path3, 'w')
    f3.write("x y z E1 dExr dExi dEyr dEyi dEzr dEzi \n")
    for i in range(len(x)):
        line = str(x[i]) + " " +str(y[i]) + " " + str(z[i]) + " " + \
               str(E1[i]) + " " + \
               str(Exr1[i] - Exr2[i]) + " " + str(Exi1[i] - Exi2[i]) + " " + \
               str(Eyr1[i] - Eyr2[i]) + " " + str(Eyi1[i] - Eyi2[i]) + " " + \
               str(Ezr1[i] - Ezr2[i]) + " " + str(Ezi1[i] - Ezi2[i]) + " \n"
        f3.write(line)
    f3.close()


# path - путь до массива данных,
# path2 - путь до места сохранения графика,
# type - тип входных данных.
# component - real, imagine
# use_log - использовать логарифм?
# use_my_range - использовать свой диапазон или по-умолчанию?
def plot3d_E(path, path2, R, m, lines, type, graph_title, component, section, v_min, v_max, use_log=True,
             use_small_region=False, use_region='one_root', use_my_range=False):
    if type == "scattnlay":
        data = np.loadtxt(path, dtype=np.float32, delimiter=", ", skiprows=1, usecols=range(9))
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        Exr = data[:, 3]
        Exi = data[:, 4]
        Eyr = data[:, 5]
        Eyi = data[:, 6]
        Ezr = data[:, 7]
        Ezi = data[:, 8]
        E = Exr
    elif type == "bhfield" or type == "adda":
        data = np.loadtxt(path, dtype=np.float32, delimiter=" ", skiprows=1, usecols=range(10))
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        E = data[:, 3]
        Exr = data[:, 4]
        Exi = data[:, 5]
        Eyr = data[:, 6]
        Eyi = data[:, 7]
        Ezr = data[:, 8]
        Ezi = data[:, 9]
    elif type == "wkb" or type == "wkb+":
        data = np.loadtxt(path, dtype=np.float32, delimiter=" ", skiprows=1, usecols=range(10))
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        E = data[:, 3]
        Exr = data[:, 4]
        Exi = data[:, 5]
        Eyr = data[:, 6]
        Eyi = data[:, 7]
        Ezr = data[:, 8]
        Ezi = data[:, 9]

    if use_small_region:
        xnew = np.empty(0)
        ynew = np.empty(0)
        znew = np.empty(0)
        Enew = np.empty(0)
        Exrnew = np.empty(0)
        Eyrnew = np.empty(0)
        Ezrnew = np.empty(0)
        Exinew = np.empty(0)
        Eyinew = np.empty(0)
        Ezinew = np.empty(0)
        for i in range(0, len(Exr)):
            if y[i] >= 0 and z[i] >= 0:
                y2, z2 = coordinates_in_meridional_plane(x[i], y[i], z[i], R)
                cur_region = region(y2, z2, R, m, lines)
                if cur_region == use_region:
                    xnew = np.append(xnew, x[i])
                    ynew = np.append(ynew, y[i])
                    znew = np.append(znew, z[i])
                    Enew = np.append(Enew, E[i])
                    Exrnew = np.append(Exrnew, Exr[i])
                    Eyrnew = np.append(Eyrnew, Eyr[i])
                    Ezrnew = np.append(Ezrnew, Ezr[i])
                    Exinew = np.append(Exinew, Exi[i])
                    Eyinew = np.append(Eyinew, Eyi[i])
                    Ezinew = np.append(Ezinew, Ezi[i])
    else:
        xnew = x
        ynew = y
        znew = z
        Enew = E
        Exrnew = Exr
        Eyrnew = Eyr
        Ezrnew = Ezr
        Exinew = Exi
        Eyinew = Eyi
        Ezinew = Ezi

    if use_log:
        if component == "real":
            for i in range(0, len(Exrnew)):
                if isnan(Exrnew[i]) or isnan(Exinew[i]):
                    Enew[i] = 0
                else:
                    Enew[i] = math.log10(abs(Exrnew[i]))
        elif component == "imagine":
            for i in range(0, len(Exrnew)):
                if isnan(Exrnew[i]) or isnan(Exinew[i]):
                    Enew[i] = 0
                else:
                    Enew[i] = math.log10(abs(Exinew[i]))
        elif component == "both":
            for i in range(0, len(Exrnew)):
                if isnan(Exrnew[i]) or isnan(Exinew[i]):
                    Enew[i] = 0
                else:
                    Enew[i] = Exrnew[i] ** 2 + Exinew[i] ** 2 + Eyrnew[i] ** 2 + Eyinew[i] ** 2 + Ezrnew[i] ** 2 + Ezinew[i] ** 2
                    Enew[i] = Enew[i] ** 0.5
                    Enew[i] = math.log10(Enew[i])
    elif use_log == False:
        if component == "real":
            for i in range(0, len(Exrnew)):
                if isnan(Exrnew[i]) or isnan(Exinew[i]):
                    Enew[i] = 0
                else:
                    Enew[i] = Exrnew[i]
        elif component == "imagine":
            for i in range(0, len(Exrnew)):
                if isnan(Exrnew[i]) or isnan(Exinew[i]):
                    Enew[i] = 0
                else:
                    Enew[i] = Exinew[i]
        elif component == "both":
            for i in range(0, len(Exrnew)):
                if isnan(Exrnew[i]) or isnan(Exinew[i]):
                    Enew[i] = 0
                else:
                    Enew[i] = Exrnew[i] ** 2 + Exinew[i] ** 2 + Eyrnew[i] ** 2 + Eyinew[i] ** 2 + Ezrnew[i] ** 2 + Ezinew[i] ** 2
                    Enew[i] = Enew[i] ** 0.5
                    print(Enew[i])

    Enew_min = 1000
    Enew_max = 0
    for i in range(len(Enew)):
        if Enew[i] < Enew_min:
            Enew_min = Enew[i]
        if Enew[i] > Enew_max:
            Enew_max = Enew[i]
    if use_my_range is False:
        v_min = Enew_min
        v_max = Enew_max
        print("v_min", v_min)
        print("v_max", v_max)

    if section == "x-section":
        # Set up a regular grid of interpolation points
        xi = np.linspace(ynew.min(), ynew.max(), 3000)
        yi = np.linspace(znew.min(), znew.max(), 3000)
        xi, yi = np.meshgrid(xi, yi)
        # Interpolate; there's also method='cubic' for 2-D data such as here
        zi = scipy.interpolate.griddata((ynew, znew), Enew, (xi, yi), method='linear')
        plt.imshow(zi, vmin=v_min, vmax=v_max, origin='lower',
                   extent=[ynew.min(), ynew.max(), znew.min(), znew.max()], cmap='rainbow')
        plt.xlabel('y')
    elif section == "y-section":
        xi = np.linspace(xnew.min(), xnew.max(), 3000)
        yi = np.linspace(znew.min(), znew.max(), 3000)
        xi, yi = np.meshgrid(xi, yi)
        zi = scipy.interpolate.griddata((xnew, znew), Enew, (xi, yi), method='linear')
        plt.imshow(zi, vmin=v_min, vmax=v_max, origin='lower',
                   extent=[xnew.min(), xnew.max(), znew.min(), znew.max()], cmap='rainbow')
        plt.xlabel('x')
    else:
        print("Error in plot3d_E function! No such section.")

    plt.ylabel('z')
    plt.title(graph_title)
    plt.colorbar()
    # plt.xticks([])
    plt.savefig(path2, dpi=300)
    plt.close()


# Функция для постоения 3D графика.
# path - путь до массива данных
# path2 - путь до места сохранения графика
# section - тип сечения которое фиксируется (x-section, y-section)
def plot3d(path, path2, section, graph_title, value_type):
    data = np.loadtxt(path, dtype=np.float32, delimiter=" ", skiprows=1, usecols=range(10))
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    e = data[:, 3]
    exr = data[:, 4]
    exi = data[:, 5]
    eyr = data[:, 6]
    eyi = data[:, 7]
    Ezr = data[:, 8]
    ezi = data[:, 9]
    if value_type == 'exr':
        val = exr
    elif value_type == 'exi':
        val = exi

    if section == "x-section":
        x = y
    # Set up a regular grid of interpolation points
    xi = np.linspace(x.min(), x.max(), 3000)
    yi = np.linspace(z.min(), z.max(), 3000)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate; there's also method='cubic' for 2-D data such as here
    zi = scipy.interpolate.griddata((x, z), val, (xi, yi), method='linear')

    plt.imshow(zi, vmin=val.min(), vmax=val.max(), origin='lower',
               extent=[x.min(), x.max(), z.min(), z.max()], cmap='rainbow')
    if section == "x-section":
        plt.xlabel('Y')
    elif section == "y-section":
        plt.xlabel('X')
    plt.ylabel('Z')
    plt.title(graph_title)
    plt.colorbar()
    plt.savefig(path2, dpi=300)
    plt.close()


if __name__ == "__main__":
    size = 100
    grid = 160
    R = size / 2
    m = 1.1
    m_im = 0
    type = "bhfield" # "scattnlay" #
    section_coordinate = 0 # 2.5 #
    lines = BoundaryLines(m)
    path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + " (clear)/"
    # path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + "/"
    tail = str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
    version = "Maps of error for WKBr v1, WKBr v2"

    if version == "WKB":
        # Найдём сечение x-section WKB:
        section_coordinate = 0.3125
        path1 = path + "WKB from ADDA-" + tail
        path1_section = path + "wkb-x-section-" + tail
        prepare_data(path1, path1_section, "adda", "x-section", section_coordinate)
        # Строим карту
        path_map = path + "wkb-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
        plot3d_E(path1_section,
                 path_map,
                 R,
                 m,
                 lines,
                 type="adda",
                 graph_title="",  # WKBv"+ str(version) +", both components
                 component="both",
                 section="x-section",
                 v_min=-2.5, v_max=0.5,
                 use_log=True,
                 use_small_region=False,
                 use_region="two_roots",
                 use_my_range=False)
    elif version == "Maps of error for WKBr v1, WKBr v2":
        # Find the cross section y-section WKBr v1:
        section_coordinate = 0.3125
        path1 = path + "wkb_refraction (v1)-" + tail
        path1_section = path + "wkb_refraction (v1)-y-section-" + tail
        prepare_data(path1, path1_section, "adda", "y-section", section_coordinate)

        # Find the cross y-section bhfield:
        path_bh = path + "bhfield" + "-" + tail
        pathbh_adda = path + "bhfield-adda" + "-" + tail
        scattnlay_bhfield_to_adda(path_bh, pathbh_adda, type, size / 2, grid)
        path_bh_section = path + "bhfield-y-section" + "-" + tail
        prepare_data(pathbh_adda, path_bh_section, "adda", "y-section", section_coordinate)

        # Let's find the difference at each point:
        path_dif = path + "wkb_refraction (v1)-dif-" + tail
        find_difference(path1_section, path_bh_section, path_dif, "bhfield")

        # Building the map
        path_map = path + "wkb_refraction (v1)-dif-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
        plot3d_E(path_dif,
                 path_map,
                 R,
                 m,
                 lines,
                 type="adda",
                 graph_title="",  # WKBv"+ str(version) +", both components
                 component="both",
                 section="y-section",
                 v_min=-2.5, v_max=0.5,
                 use_log=True,
                 use_small_region=False,
                 use_region="two_roots",
                 use_my_range=True)

        # Find the cross x-section WKBr v2:
        path2 = path + "wkb_refraction (v2)-" + tail
        path2_section = path + "wkb_refraction (v2)-y-section-" + tail
        prepare_data(path2, path2_section, "adda", "y-section", section_coordinate)

        # Find the difference at each point:
        path_dif2 = path + "wkb_refraction (v2)-dif-" + tail
        path_bh_section = path + "bhfield-y-section" + "-" + tail
        find_difference(path2_section, path_bh_section, path_dif2, "bhfield")

        # Building the map
        path_map2 = path + "wkb_refraction (v2)-dif-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
        plot3d_E(path_dif2,
                 path_map2,
                 R,
                 m,
                 lines,
                 type="adda",
                 graph_title="",  # WKBv"+ str(version) +", both components
                 component="both",
                 section="y-section",
                 v_min=-2.5, v_max=0.5,
                 use_log=True,
                 use_small_region=False,
                 use_region="two_roots",
                 use_my_range=True)
    elif version == "Maps of e.f. amplitude error for WKBr v2, WKBr v3, exact":
        # Найдём сечение x-section WKBr v2:
        path2 = path + "wkb_refraction (v2)-" + tail
        path2_section = path + "wkb_refraction (v2)-x-section-" + tail
        prepare_data(path2, path2_section, "adda", "x-section", section_coordinate)

        # Строим карту
        path_map2 = path + "wkb_refraction (v2)-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
        plot3d_E(path2_section,
                 path_map2,
                 R,
                 m,
                 lines,
                 type="adda",
                 graph_title="",  # WKBv"+ str(version) +", both components
                 component="both",
                 section="x-section",
                 v_min=0.95, v_max=1.05,
                 use_log=False,
                 use_small_region=True,
                 use_region="two_roots",
                 use_my_range=True)
        # Найдём сечение x-section WKBr v3:
        path3 = path + "wkb_refraction (v3)-" + tail
        path3_section = path + "wkb_refraction (v3)-x-section-" + tail
        prepare_data(path3, path3_section, "adda", "x-section", section_coordinate)

        # Строим карту
        path_map3 = path + "wkb_refraction (v3)-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
        plot3d_E(path3_section,
                 path_map3,
                 R,
                 m,
                 lines,
                 type="adda",
                 graph_title="",  # WKBv"+ str(version) +", both components
                 component="both",
                 section="x-section",
                 v_min=0.95, v_max=1.05,
                 use_log=False,
                 use_small_region=True,
                 use_region="two_roots",
                 use_my_range=False)
        # Найдём сечение x-section bhfield:
        path_bh = path + "bhfield" + "-" + tail
        pathbh_adda = path + "bhfield-adda" + "-" + tail
        path_bh_section = path + "bhfield-x-section" + "-" + tail
        scattnlay_bhfield_to_adda(path_bh, pathbh_adda, type, size / 2, grid)
        prepare_data(pathbh_adda, path_bh_section, "adda", "x-section", section_coordinate)
        # Строим карту
        path_map4 = path + "bhfield-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
        plot3d_E(path_bh_section,
                 path_map4,
                 R,
                 m,
                 lines,
                 type="adda",
                 graph_title="",  # WKBv"+ str(version) +", both components
                 component="both",
                 section="x-section",
                 v_min=0.95, v_max=1.05,
                 use_log=False,
                 use_small_region=True,
                 use_region="two_roots",
                 use_my_range=False)
    elif version == "Maps of e.f. amplitude error for WKBr v2, WKBr v4, exact (no solution region)":
        # Найдём сечение x-section bhfield:
        path_bh = path + type + "-" + tail
        pathbh_adda = path + type + "-adda" + "-" + tail
        path_bh_section = path + type + "-x-section" + "-" + tail
        scattnlay_bhfield_to_adda(path_bh, pathbh_adda, type, size / 2, grid)
        prepare_data(pathbh_adda, path_bh_section, "adda", "x-section", section_coordinate)
        # Строим карту
        path_map4 = path + "bhfield-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
        plot3d_E(path_bh_section,
                 path_map4,
                 R,
                 m,
                 lines,
                 type="adda",
                 graph_title="",  # WKBv"+ str(version) +", both components
                 component="both",
                 section="x-section",
                 v_min=0.95, v_max=1.05,
                 use_log=False,
                 use_small_region=False,
                 use_region="no_root",
                 use_my_range=False)