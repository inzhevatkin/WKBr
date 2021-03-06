import numpy as np
from math import isclose
import matplotlib.pyplot as plt
import scipy.interpolate
import math
from math import isnan
from Region import region, BoundaryLines
from Coordinate_systems import coordinates_in_meridional_plane
import os
from Compare2 import scattnlay_bhfield_to_adda, prepare_data


def find_difference(path1, path2, path3, type):
    print("find_difference ", path1, " ", path2, " ", path3)
    if type == "scattnlay":
        print("Not yet implemented.")
    elif type == "adda":
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
        Exr2 = data2[:, 4]
        Exi2 = data2[:, 5]
        Eyr2 = data2[:, 6]
        Eyi2 = data2[:, 7]
        Ezr2 = data2[:, 8]
        Ezi2 = data2[:, 9]
    f3 = open(path3, 'w')
    f3.write("x y z dE dExr dExi dEyr dEyi dEzr dEzi \n")
    for i in range(len(x)):
        dExr = Exr1[i] - Exr2[i]
        dExi = Exi1[i] - Exi2[i]
        dEyr = Eyr1[i] - Eyr2[i]
        dEyi = Eyi1[i] - Eyi2[i]
        dEzr = Ezr1[i] - Ezr2[i]
        dEzi = Ezi1[i] - Ezi2[i]
        dE = (dExr ** 2 + dExi ** 2 + dEyr ** 2 + dEyi ** 2 + dEzr ** 2 + dEzi ** 2) ** 0.5
        line = str(x[i]) + " " + str(y[i]) + " " + str(z[i]) + " " + str(dE) + " " + \
               str(dExr) + " " + str(dExi) + " " + str(dEyr) + " " + str(dEyi) + " " + str(dEzr) + " " + str(
            dEzi) + " \n"
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
            # I only use the area on the right to display the map:
            if x[i] < 0 and section == "y-section":
                continue
            elif y[i] < 0 and section == "x-section":
                continue
            y2, z2 = coordinates_in_meridional_plane(x[i] / R, y[i] / R, z[i] / R)
            cur_region = region(y2, z2, m, lines)
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
                    Enew[i] = Exrnew[i] ** 2 + Exinew[i] ** 2 + Eyrnew[i] ** 2 + Eyinew[i] ** 2 + Ezrnew[i] ** 2 + \
                              Ezinew[i] ** 2
                    Enew[i] = Enew[i] ** 0.5
                    Enew[i] = math.log10(Enew[i])
    elif use_log is False:
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
                    Enew[i] = Exrnew[i] ** 2 + Exinew[i] ** 2 + Eyrnew[i] ** 2 + Eyinew[i] ** 2 + Ezrnew[i] ** 2 + \
                              Ezinew[i] ** 2
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


# The function selects points from the specified region.
def select_region(path_in, path_out, my_region):
    print("select_region() started...")
    f_out = open(path_out, 'w')
    f_out.write("x y z E Exr Exi Eyr Eyi Ezr Ezi \n")
    # assume that type "adda"
    data = np.loadtxt(path_in, dtype=np.float32, delimiter=" ", skiprows=1, usecols=range(10))
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
    L = len(x)
    for i in range(0, L):
        # I only use the area on the right to display the map:
        if x[i] < 0 and section == "y-section":
            continue
        elif y[i] < 0 and section == "x-section":
            continue
        y2, z2 = coordinates_in_meridional_plane(x[i] / R, y[i] / R, z[i] / R)
        cur_region = region(y2, z2, m, lines)
        if cur_region == my_region:
            f_out.write(str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + str(E[i]) + ' ' +
                        str(Exr[i]) + ' ' + str(Exi[i]) + ' ' +
                        str(Eyr[i]) + ' ' + str(Eyi[i]) + ' ' +
                        str(Ezr[i]) + ' ' + str(Ezi[i]) + '\n')
    f_out.close()


# version = v1, v2 ...
# section = x-section, y-section.
# type_exact - exact solution type.
def diff_map(tail, version, section, type_exact, section_coordinate=0.3125,
             use_small_region=False, region="two_roots",
             use_my_range=True, min=-0.5, max=0.5):
    # Find the cross y-section:
    path1 = path + "wkb_refraction (" + version + ")-" + tail
    path1_section = path + "wkb_refraction (" + version + ")-" + section + "-" + tail
    prepare_data(path1, path1_section, "adda", section, section_coordinate)

    # Find the cross section exact:
    path_ex = path + type_exact + "-" + tail
    pathex_adda = path + type_exact + "-adda" + "-" + tail
    scattnlay_bhfield_to_adda(path_ex, pathex_adda, type_exact, size / 2, grid)
    path_ex_section = path + type_exact + "-" + section + "-" + tail
    prepare_data(pathex_adda, path_ex_section, "adda", section, section_coordinate)

    # Let's find the difference at each point:
    path_dif = path + "wkb_refraction (" + version + ")-dif-" + tail
    find_difference(path1_section, path_ex_section, path_dif, "adda")

    # Building the map
    path_map = path + "wkb_refraction (" + version + ")-dif-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
    plot3d_E(path_dif,
             path_map,
             R,
             m,
             lines,
             type="adda",
             graph_title="",  # WKBv"+ str(version) +", both components
             component="both",
             section=section,
             v_min=min, v_max=max,
             use_log=True,
             use_small_region=use_small_region,
             use_region=region,
             use_my_range=use_my_range)


def ef_map(path1, path_out):
    # Find the cross section:
    # path1 = path + "wkb_refraction (" + version + ")-" + tail
    path1_section = path + "wkb_refraction (" + version + ")-" + section + "-" + tail
    prepare_data(path1, path1_section, "adda", section, section_coordinate)
    # Select region:
    path_in = path + "wkb_refraction (" + version + ")-" + section + "-" + tail
    select_region(path_in, path_out, my_region)
    # Building the map
    '''
    plot3d_E(path_out,
             path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-"
                + str(size) + "-" + str(m) + "-" + str(grid) + ".png",
             R,
             m,
             lines,
             type="adda",
             graph_title="",  # WKBv"+ str(version) +", both components
             component="both",
             section=section,
             v_min=min, v_max=max,
             use_log=True,
             use_small_region=False,
             use_region=False,
             use_my_range=False)
    '''


if __name__ == "__main__":
    size = 100  # 500
    grid = 200  # 100
    R = size / 2
    m = 1.1
    m_im = 0  # 0.01
    type = "bhfield"  # "scattnlay"/"bhfield"
    section = "y-section"
    section_coordinate = 0  # 2.5252  # 0.3125
    use_my_range = False
    min = -0.5
    max = 0.5
    use_small_region_flag = False
    my_region = "no_root"
    # tail = str(size) + "-" + str(m) + "-" + str(m_im) + "-" + str(grid) + ".dat"
    tail = str(size) + "-" + str(m) + "-" + str(grid) + ".dat"
    path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + ", section (clear)/"
    # path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + " (clear)/"
    # path = "C:/Users/konstantin/Documents/main-script/data size " + str(size) + ", grid " + str(grid) + "/"
    lines = BoundaryLines(m)
    for version in ["Maps of error for WKBr v1",
                    "Maps of error for WKBr v2",
                    "Maps of error for WKBr v5",
                    "Maps of error for WKBr v12"]:
        print(version)
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
        elif version == "Maps of error for WKBr v1":
            diff_map(tail, "v1", section, type, section_coordinate=section_coordinate)
        elif version == "Maps of error for WKBr v2":
            diff_map(tail, "v2", section, type, section_coordinate=section_coordinate)
        elif version == "Maps of error for WKBr v5":
            diff_map(tail, "v5", section, type, section_coordinate=section_coordinate)
        elif version == "Maps of error for WKBr v12":
            diff_map(tail, "v12", section, type, section_coordinate=section_coordinate)
        elif version == "Maps of error for WKBr v7":
            diff_map(tail, "v7", section, type, section_coordinate=section_coordinate, use_small_region=True,
                     use_my_range=use_my_range, min=min, max=max)
        elif version == "Maps of error for WKBr v13":
            diff_map(tail, "v13", section, type, section_coordinate=section_coordinate, use_small_region=True,
                     use_my_range=use_my_range, min=min, max=max)
        elif version == "Maps of error for WKBr v13-2":
            diff_map(tail, "v13-2", section, type, section_coordinate=section_coordinate, use_small_region=True,
                     use_my_range=use_my_range, min=min, max=max)
        elif version == "Maps of error for WKBr v2, WKBr v3, exact":
            # Find the cross y-section WKBr v2:
            path2 = path + "wkb_refraction (v2)-" + tail
            path2_section = path + "wkb_refraction (v2)-y-section-" + tail
            prepare_data(path2, path2_section, "adda", "y-section", section_coordinate)

            # Find the y-section bhfield:
            path_bh = path + "bhfield" + "-" + tail
            pathbh_adda = path + "bhfield-adda" + "-" + tail
            scattnlay_bhfield_to_adda(path_bh, pathbh_adda, type, size / 2, grid)
            path_bh_section = path + "bhfield-y-section" + "-" + tail
            prepare_data(pathbh_adda, path_bh_section, "adda", "y-section", section_coordinate)

            # Let's find the difference at each point:
            path_dif = path + "wkb_refraction (v2)-dif-" + tail
            find_difference(path2_section, path_bh_section, path_dif, "bhfield")

            # Map building
            path_map2 = path + "wkb_refraction (v2)-" + str(size) + "-" + str(m) + "-" + str(grid) + ".png"
            plot3d_E(path_dif,
                     path_map2,
                     R,
                     m,
                     lines,
                     type="adda",
                     graph_title="",  # WKBv"+ str(version) +", both components
                     component="both",
                     section="y-section",
                     v_min=0.5, v_max=-0.6,
                     use_log=True,
                     use_small_region=False,
                     use_region="two_roots",
                     use_my_range=True)
            '''
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
            '''
        elif version == "Maps of error for WKBr v2, WKBr v4, exact (no solution region)":
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
        elif version == "Maps of error for WKBr v2 in R2":
            diff_map(tail, "v2", section, type, section_coordinate=section_coordinate,
                     use_small_region=use_small_region_flag, region=my_region,
                     use_my_range=use_my_range, min=min, max=max)
        elif version == "Maps of error for WKBr v12 in R2":
            diff_map(tail, "v12", section, type, section_coordinate=section_coordinate,
                     use_small_region=use_small_region_flag, region=my_region,
                     use_my_range=use_my_range, min=min, max=max)
        elif version == "Map of EF for WKBr v2 (one ray)":
            version = "v2"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v4 (one ray)":
            version = "v12"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v1":
            version = "v15"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v2":
            version = "v7"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v2-1":
            version = "v13"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v2-2":
            version = "v13-2"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v3":
            version = "v16"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v3-2":
            version = "v16-2"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v4":
            version = "v17"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v4-1":
            version = "v17-1"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v4-2":
            version = "v17-2"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v5":
            version = "v18"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v5-1":
            version = "v18-1"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of EF for WKBr v5-2":
            version = "v18-2"
            path1 = path + "wkb_refraction (" + version + ")-" + tail
            path_out = path + "wkb_refraction (" + version + ")-" + section + "-" + my_region + "-" + tail
            ef_map(path1, path_out)
        elif version == "Map of exact":
            path1 = path + str(type) + "-y-section-" + tail
            path2 = path + str(type) + "-y-section-" + my_region + "-" + tail
            ef_map(path1, path2)

