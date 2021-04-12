import os
import numpy as np
from math import isclose
from math import isnan
# from Rounding import rounding2
import linecache
from BoundaryLines import region
from Coordinate_systems import  coordinates_in_meridional_plane


def rounding2(x, y, z, n):
    par = 10 ** n
    x = int(x * par) / par
    y = int(y * par) / par
    z = int(z * par) / par
    return x, y, z

def rounding(var):
    tmp = int(var * 10 ** 5) / 10 ** 5  # число до 5-го знака.
    tmp2 = (var - tmp) * 10 ** 6
    if tmp2 < 0:
        tmp2 = -tmp2
    six_sign = round(tmp2)  # 6-й знак числа.
    if var < 0:
        var_m = tmp
        var_l = tmp - 0.00001
    else:
        var_m = tmp + 0.00001
        var_l = tmp
    if six_sign < 5:
        flag = "low"
    elif six_sign > 5:
        flag = "high"
    elif six_sign == 5:
        flag = "both"
    return var_l, var_m, flag


def find_de_de2(exr1, exi1, eyr1, eyi1, ezr1, ezi1,
                exr2, exi2, eyr2, eyi2, ezr2, ezi2,
                exr3, exi3, use_rounding=False):
    if use_rounding:
        # Код для расчёта средней ошибки с учётом округления до 5-го знака после запятой
        exr1_l, exr1_m, exr1_flag = rounding(exr1)
        exi1_l, exi1_m, exi1_flag = rounding(exi1)
        eyr1_l, eyr1_m, eyr1_flag = rounding(eyr1)
        eyi1_l, eyi1_m, eyi1_flag = rounding(eyi1)
        ezr1_l, ezr1_m, ezr1_flag = rounding(ezr1)
        ezi1_l, ezi1_m, ezi1_flag = rounding(ezi1)
        e1_l = [exr1_l, eyr1_l, ezr1_l, exi1_l, eyi1_l, ezi1_l]
        e1_m = [exr1_m, eyr1_m, ezr1_m, exi1_m, eyi1_m, ezi1_m]
        e1_flag = [exr1_flag, eyr1_flag, ezr1_flag, exi1_flag, eyi1_flag, ezi1_flag]

        exr2_l, exr2_m, exr2_flag = rounding(exr2)
        exi2_l, exi2_m, exi2_flag = rounding(exi2)
        eyr2_l, eyr2_m, eyr2_flag = rounding(eyr2)
        eyi2_l, eyi2_m, eyi2_flag = rounding(eyi2)
        ezr2_l, ezr2_m, ezr2_flag = rounding(ezr2)
        ezi2_l, ezi2_m, ezi2_flag = rounding(ezi2)
        e2_l = [exr2_l, eyr2_l, ezr2_l, exi2_l, eyi2_l, ezi2_l]
        e2_m = [exr2_m, eyr2_m, ezr2_m, exi2_m, eyi2_m, ezi2_m]
        e2_flag = [exr2_flag, eyr2_flag, ezr2_flag, exi2_flag, eyi2_flag, ezi2_flag]

        dE_l1 = 0
        dE_l2 = 0
        dE1 = 0
        flag = False
        for i in range(0, 6):
            if e1_flag[i] == "low":
                first = e1_l[i]
            elif e1_flag[i] == "high":
                first = e1_m[i]

            if e2_flag[i] == "low":
                second = e2_l[i]
            elif e2_flag[i] == "high":
                second = e2_m[i]
            elif e2_flag[i] == "both":
                if e1_flag[i] != "both":
                    tmp1 = (first - e2_l[i]) ** 2
                    tmp2 = (first - e2_m[i]) ** 2
                    if tmp1 > tmp2:
                        dE1 = tmp2
                        flag = True
                    else:
                        dE1 = tmp1
                        flag = True
                else:
                    tmp1 = (e1_l[i] - e2_l[i]) ** 2
                    tmp2 = (e1_m[i] - e2_m[i]) ** 2
                    tmp3 = (e1_l[i] - e2_m[i]) ** 2
                    tmp4 = (e1_m[i] - e2_l[i]) ** 2
                    tmp_list = [tmp1, tmp2, tmp3, tmp4]
                    min = tmp_list[0]
                    for i in range(0, 3):
                        if min > tmp_list[i + 1]:
                            min = tmp_list[i + 1]
                    dE1 = min
                    flag = True

            if e1_flag[i] == "both" and not flag:
                tmp1 = (e1_l[i] - second) ** 2
                tmp2 = (e1_m[i] - second) ** 2
                if tmp1 < tmp2:
                    dE1 = tmp1
                    flag = True
                else:
                    dE1 = tmp2
                    flag = True

            if not flag:
                dE1 = (first - second) ** 2
            dE += dE1

        dE = dE ** 0.5

        dE2 = 0
        exr3_l, exr3_m, exr3_flag = rounding(exr3)
        exi3_l, exi3_m, exi3_flag = rounding(exi3)

        # Рассматриваем условие для exr3
        tmp1 = 0
        tmp2 = 0
        if exr3_flag == "low":
            exr3 = exr3_l
        elif exr3_flag == "high":
            exr3 = exr3_m
        elif exr3_flag == "both":
            tmp1 = abs(exr1 - exr3_l)
            tmp2 = abs(exr1 - exr3_m)
            if tmp1 < tmp2:
                exr3 = exr3_l
            else:
                exr3 = exr3_m

        # Рассматриваем условие для exi3
        tmp1 = 0
        tmp2 = 0
        if exi3_flag == "low":
            exi3 = exi3_l
        elif exi3_flag == "high":
            exi3 = exi3_m
        elif exi3_flag == "both":
            tmp1 = abs(exr1 - exi3_l)
            tmp2 = abs(exr1 - exi3_m)
            if tmp1 < tmp2:
                exi3 = exi3_l
            else:
                exi3 = exi3_m
    else:
        dE = (exr1 - exr2) ** 2 + (eyr1 - eyr2) ** 2 + (ezr1 - ezr2) ** 2 + \
             (exi1 - exi2) ** 2 + (eyi1 - eyi2) ** 2 + (ezi1 - ezi2) ** 2
        dE_l1 = dE ** 0.5
        dE_l2 = dE

    dE2 = (exr1 - exr3) ** 2 + (eyr1) ** 2 + (ezr1) ** 2 + \
          (exi1 - exi3) ** 2 + (eyi1) ** 2 + (ezi1) ** 2
    dE2 = dE2 ** 0.5

    return dE_l1, dE2, dE_l2


def norm(exr1, exi1, eyr1, eyi1, ezr1, ezi1,
         exr2, exi2, eyr2, eyi2, ezr2, ezi2):
    norm = ((exr1 - exr2) ** 2 + (eyr1 - eyr2) ** 2 + (ezr1 - ezr2) ** 2 + \
            (exi1 - exi2) ** 2 + (eyi1 - eyi2) ** 2 + (ezi1 - ezi2) ** 2) ** 0.5
    return norm


# Данную функцию нужно использовать если элементы в сравниваемых таблицах находятся в одном порядке.
# первая таблица может иметь типы: "mywkb", "scattnlay"
# type - тип первого элемента
def compare_mywkbscattnlay_wkb(path1,
                               path2,
                               path_inc,
                               f_log,
                               accuracy,
                               use_norm,
                               type,
                               R,
                               m,
                               lines,
                               find_addit_error = False,
                               addit_radius = None):
    print("Compare " + str(type) + " and wkb")
    f_log.write("\n")
    f_log.write("Compare my wkb and wkb \n")

    f1 = open(path1, 'r')
    f1.readline()

    f2 = open(path2, 'r')
    f2.readline()

    f3 = open(path_inc, 'r')
    f3.readline()

    count = 0
    count2 = 0
    aver_error = 0
    aver_error2 = 0
    aver_error_l1 = 0
    aver_error_l2 = 0
    aver_error_one_root = 0
    count_one_root = 0
    aver_error_two_root = 0
    count_two_root = 0
    aver_error_no_root = 0
    count_no_root = 0
    count_nan = 0
    max_error = 0
    count_not_equal = 0
    norm_value = 0

    while True:
        additional_error_flag = False

        # Читаю входные файлы построчно:
        numbers1 = f1.readline()
        numbers2 = f2.readline()
        numbers3 = f3.readline()

        # Разбиваем строку на части, используя разделитель, и возвращаем эти части списком.
        if type == 'mywkb':
            numbers1 = numbers1.split()
        elif type == 'scattnlay':
            numbers1 = numbers1.split(", ")

        numbers2 = numbers2.split()
        numbers3 = numbers3.split()

        if len(numbers1) <= 1 or len(numbers2) <= 1:
            break

        if type == "mywkb":
            x1 = float(numbers1[0])
            y1 = float(numbers1[1])
            z1 = float(numbers1[2])
            exr1 = float(numbers1[4])
            exi1 = float(numbers1[5])
            eyr1 = float(numbers1[6])
            eyi1 = float(numbers1[7])
            ezr1 = float(numbers1[8])
            ezi1 = float(numbers1[9])
        elif type == "scattnlay":
            x1 = float(numbers1[0])
            y1 = float(numbers1[1])
            z1 = float(numbers1[2])
            exr1 = float(numbers1[3])
            exi1 = float(numbers1[4])
            eyr1 = float(numbers1[5])
            eyi1 = float(numbers1[6])
            ezr1 = float(numbers1[7])
            ezi1 = float(numbers1[8])

        x2 = float(numbers2[0])
        y2 = float(numbers2[1])
        z2 = float(numbers2[2])
        exr2 = float(numbers2[4])
        exi2 = float(numbers2[5])
        eyr2 = float(numbers2[6])
        eyi2 = float(numbers2[7])
        ezr2 = float(numbers2[8])
        ezi2 = float(numbers2[9])

        x3 = float(numbers3[0])
        y3 = float(numbers3[1])
        z3 = float(numbers3[2])
        exr3 = float(numbers3[4])
        exi3 = float(numbers3[5])
        eyr3 = float(numbers3[6])
        eyi3 = float(numbers3[7])
        ezr3 = float(numbers3[8])
        ezi3 = float(numbers3[9])

        # Проверка что элемент не nan:
        if isnan(exr1) or isnan(eyr1) or isnan(ezr1) or isnan(exi1) or isnan(eyi1) or isnan(ezi1) or \
                isnan(exr2) or isnan(eyr2) or isnan(ezr2) or isnan(exi2) or isnan(eyi2) or isnan(ezi2):
            count_nan += 1
            continue

        if isclose(x1, x2, abs_tol=accuracy) and \
                isclose(y1, y2, abs_tol=accuracy) and \
                isclose(z1, z2, abs_tol=accuracy) and \
                isclose(x1, x3, abs_tol=accuracy) and \
                isclose(y1, y3, abs_tol=accuracy) and \
                isclose(z1, z3, abs_tol=accuracy):

            R1 = (x1 ** 2 + y1 ** 2 + z1 ** 2) ** 0.5
            R2 = (x2 ** 2 + y2 ** 2 + z2 ** 2) ** 0.5

            if find_addit_error:
                if R1 < addit_radius and R2 < addit_radius:
                    additional_error_flag = True

            count += 1

            norm_value = norm(exr1, exi1, eyr1, eyi1, ezr1, ezi1, exr2, exi2, eyr2, eyi2, ezr2, ezi2)

            aver_error_l1 += norm_value
            aver_error_l2 += norm_value ** 2

            # Определим область куда попала точка
            ym, zm = coordinates_in_meridional_plane(x1, y1, z1, R)
            cur_region = region(ym, zm, R, m, lines)

            # Считаю суммарную ошибку в каждой области
            if cur_region == "one_root":
                aver_error_one_root += aver_error_l1
                count_one_root += 1
            elif cur_region == "two_roots":
                aver_error_two_root += aver_error_l1
                count_two_root += 1
            elif cur_region == "no_root":
                aver_error_no_root += aver_error_l1
                count_no_root += 1
            else:
                print("Error in compare_mywkbscattnlay_wkb function! Invalid region defined. ")
        else:
            count_not_equal += 1

    f_log.write("Number of elements which were in work = " + str(count) + '\n')
    f_log.write("Number of not equal elements = " + str(count_not_equal) + '\n')
    f_log.write("Number of nan elements = " + str(count_nan) + '\n')
    if count_not_equal > 0:
        f_log.write("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    aver_error_l1 /= count
    aver_error_l2 /= count
    aver_error_l2 = aver_error_l2 ** 0.5
    if count_one_root != 0:
        # aver_error_one_root = aver_error_one_root ** 0.5
        aver_error_one_root /= count_one_root
    if count_two_root != 0:
        # aver_error_two_root = aver_error_two_root ** 0.5
        aver_error_two_root /= count_two_root
    if count_no_root != 0:
        # aver_error_no_root = aver_error_no_root ** 0.5
        aver_error_no_root /= count_no_root


    print("Compare ", path1, path2)
    print("Average error = ", aver_error)
    print("Average error 2 = ", aver_error2)

    f1.close()
    f2.close()
    f3.close()

    return aver_error_l1, aver_error_l2, aver_error_one_root, aver_error_two_root, aver_error_no_root



def compare_bhfield_all(path1, path2, grid, refr, type, accuracy, f_log, size, dots_number,
                        use_norm = True, dict_inc = None, find_addit_error = False, addit_radius = None):
    print("Compare bhfield and " + type)
    radius = size / 2
    f_log.write('\n')
    f_log.write("Compare bhfield and " + type + '\n')
    f2 = open("log-bhfield-" + str(type) +"-"+ str(size) + "-" + str(refr) + "-" + str(grid) + ".dat", 'w')
    f2.write("count x y z dE aver_err \n")

    f1 = open(path1, 'r')
    f1.readline()
    f1.readline()

    aver_error = 0
    aver_error2 = 0
    norm = 0
    count_inwork = 0
    count_not_eq = 0
    count = 0
    count2 = 0
    count_r = 0
    count_nan = 0
    count_getline_err = 0
    count_not_found_inc = 0
    max_error = 0

    for k in range(grid):
        for j in range(grid):
            for i in range(grid):
                additional_error_flag = False
                # Читаю входные файлы построчно.
                # Разбиваем строку на части, используя разделитель, и возвращаем эти части списком.
                numbers1 = f1.readline()
                numbers1 = numbers1.split()
                if len(numbers1) == 0 or count == dots_number:  # Нулевая длина обозначает конец файла (EOF)
                    break

                count_inwork += 1

                if type == "scattnlay":
                    # Нумерация для функции getline() начинается с 1.
                    numbers2 = linecache.getline(path2, 2 + grid*grid*i + grid*j + k)
                    numbers2 = numbers2.split(", ")
                elif type == "adda" or type == "wkb" or type == "addawkb" or type == "wkb_refraction":
                    numbers2 = linecache.getline(path2, 2 + i + grid*j + grid*grid*k)
                    numbers2 = numbers2.split()
                if not numbers2:
                    count_getline_err += 1
                    continue

                x1 = float(numbers1[0])
                y1 = float(numbers1[1])
                z1 = float(numbers1[2])

                x2 = float(numbers2[0])
                y2 = float(numbers2[1])
                z2 = float(numbers2[2])

                R1 = (x1 ** 2 + y1 ** 2 + z1 ** 2) ** 0.5
                R2 = (x2 ** 2 + y2 ** 2 + z2 ** 2) ** 0.5

                if R1 < radius and R2 < radius:
                    count_r += 1

                    if R1 < addit_radius and R2 < addit_radius:
                        additional_error_flag = True

                    if isclose(x1, x2, rel_tol=accuracy) and \
                            isclose(y1, y2, rel_tol=accuracy) and \
                            isclose(z1, z2, rel_tol=accuracy):

                        exr1 = float(numbers1[3])
                        exi1 = float(numbers1[6])
                        eyr1 = float(numbers1[4])
                        eyi1 = float(numbers1[7])
                        ezr1 = float(numbers1[5])
                        ezi1 = float(numbers1[8])

                        if type == "scattnlay":
                            exr2 = float(numbers2[3])
                            exi2 = float(numbers2[4])
                            eyr2 = float(numbers2[5])
                            eyi2 = float(numbers2[6])
                            ezr2 = float(numbers2[7])
                            ezi2 = float(numbers2[8])
                        elif type == "adda" or type == "wkb" or type == "addawkb" or type == "wkb_refraction":
                            exr2 = float(numbers2[4])
                            exi2 = float(numbers2[5])
                            eyr2 = float(numbers2[6])
                            eyi2 = float(numbers2[7])
                            ezr2 = float(numbers2[8])
                            ezi2 = float(numbers2[9])


                        if use_norm:
                            x1, y1, z1 = rounding2(x1, y1, z1, 2)
                            ret = dict_inc[(x1, y1, z1)]
                            exr3, exi3 = ret
                        else:
                            ret = not None
                            exr3 = 0
                            exi3 = 0

                        if ret is None:
                            count_not_found_inc += 1
                            continue

                        # Проверка что элемент не nan:
                        if isnan(exr1) or isnan(eyr1) or isnan(ezr1) or isnan(exi1) or isnan(eyi1) or isnan(ezi1) or \
                                isnan(exr2) or isnan(eyr2) or isnan(ezr2) or isnan(exi2) or isnan(eyi2) or isnan(ezi2):
                            count_nan += 1
                            continue

                        count += 1

                        if type == "scattnlay":
                            dE_l1, dE2, dE_l2 = find_de_de2(exr1, exi1, eyr1, eyi1, ezr1, ezi1,
                                                            exr2, exi2, eyr2, eyi2, ezr2, ezi2,
                                                            exr3, exi3, True)
                        else:
                            dE_l1, dE2, dE_l2 = find_de_de2(exr1, exi1, eyr1, eyi1, ezr1, ezi1,
                                                            exr2, exi2, eyr2, eyi2, ezr2, ezi2,
                                                            exr3, exi3, False)

                        aver_error_l1 += dE_l1
                        aver_error_l2 += dE_l2

                        if max_error < dE:
                            max_error = dE

                        norm += dE2

                        if additional_error_flag:
                            aver_error2 += dE
                            count2 += 1

                        # count x y z dE aver_err
                        tmp_str = str(count) + " " + str(x1) + " " + str(y1) + " " + str(z1) + " " + str(dE) + " " + \
                                  str(aver_error / count) + ' \n'
                        f2.write(tmp_str)

    f_log.write("Number of elements which were in work " + str(count_inwork) + '\n')
    f_log.write("Number of elements with R < radius = " + str(count_r) + '\n')
    f_log.write("Number of elements which used for calculation = " + str(count) + '\n')

    f_log.write("Number of nan elements = " + str(count_nan) + '\n')
    f_log.write("Number of error lines from getline = " + str(count_getline_err) + '\n')
    f_log.write("Number of not found points of incident wave = " + str(count_not_found_inc) + '\n')
    if count_nan > 0 or count_getline_err > 0 or count_not_found_inc > 0:
        f_log.write("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
    if count != dots_number:
        f_log.write("ERROR. Number of dots in bhfield doesn't equal to number of calculation elements\n")

    aver_error_l1 /= count
    aver_error_l2 /= count
    aver_error_l2 = aver_error_l2 ** 0.5
    norm /= count
    if use_norm:
        aver_error /= norm

    aver_error2 /= count2

    f1.close()
    f2.close()
    linecache.clearcache()
    if find_addit_error:
        return aver_error_l1, aver_error_l2, max_error
    else:
        return aver_error_l1, aver_error_l2, max_error

# Данная функция читает path1 и записывает в path2 только те данные, которые лежат в сфере с радиусом R1.
# type = 'bhfield' или 'scattnlay'.
# count - общее число записанных точек.
def prepare_bhfield_scattnlay(path1, path2, type, size):
    print("Prepare bhfield and scattnlay")
    radius = size / 2.
    f1 = open(path1, 'r')
    f2 = open(path2, 'w')

    if type == 'bhfield':
        f2.write(f1.readline())
        f2.write(f1.readline())
    elif type == 'scattnlay':
        f2.write(f1.readline())

    count = 0
    while True:
        numbers1 = f1.readline()
        if len(numbers1) == 0:  # Нулевая длина обозначает конец файла (EOF)
            break
        s = numbers1
        if type == 'bhfield':
            numbers1 = numbers1.split()
        elif type == 'scattnlay':
            numbers1 = numbers1.split(", ")

        if len(numbers1) <= 1:
            break

        x1 = float(numbers1[0])
        y1 = float(numbers1[1])
        z1 = float(numbers1[2])

        R1 = (x1 ** 2 + y1 ** 2 + z1 ** 2) ** 0.5
        if R1 < radius:
            f2.write(s)
            count += 1

    f1.close()
    f2.close()

    return count

def return_coordinates(path1, type="bhfield"):
    print("Return coordinates, type -", type)
    f1 = open(path1, 'r')
    if type == "bhfield":
        f1.readline()
        f1.readline()
    elif type == "wkb" or type == "scattnlay" or type == "adda":
        f1.readline()

    x = []
    y = []
    z = []

    while True:
        numbers1 = f1.readline()
        if type == 'bhfield' or type == 'wkb' or type == "adda":
            numbers1 = numbers1.split()
        elif type == 'scattnlay':
            numbers1 = numbers1.split(", ")
        if len(numbers1) <= 1:  # Нулевая длина обозначает конец файла (EOF)
            break
        x.append(float(numbers1[0]))
        y.append(float(numbers1[1]))
        z.append(float(numbers1[2]))

    f1.close()
    return x, y, z

# Функция генерирует координатную сетку.
# diameter - диаметр сферы.
# grid - размер сетки.
# type='adda'.
def return_coordinates2(diameter, grid, type='adda'):
    x_ret = []
    y_ret = []
    z_ret = []
    d = diameter / grid
    R = diameter / 2
    start_point = (-diameter + d) / 2
    finish_point = (diameter - d) / 2
    for z in np.linspace(start_point, finish_point, grid):
        for y in np.linspace(start_point, finish_point, grid):
            for x in np.linspace(start_point, finish_point, grid):
                R_cur = (x ** 2 + y ** 2 + z ** 2) ** 0.5
                if R >= R_cur:
                    x_ret.append(float(x))
                    y_ret.append(float(y))
                    z_ret.append(float(z))
    return x_ret, y_ret, z_ret

# Функция для подготовки данных.
# input - путь к входному файлу.
# output - путь к выходному файлу.
# type = "scattnlay", "inc".
# R - радиус сферы.
def prepare(input, output, type, R):
    print("Prepare " + type)
    f1 = open(input, 'r')
    f2 = open(output, 'w')
    if type == 'scattnlay':
        # Удаляю точки, которые не принадлежат сфере.
        f2.write(f1.readline())
        while True:
            numbers1 = f1.readline()
            if len(numbers1) == 0:  # Нулевая длина обозначает конец файла (EOF)
                break
            s = numbers1
            numbers1 = numbers1.split(", ")
            if len(numbers1) <= 1:
                break
            x1 = float(numbers1[0])
            y1 = float(numbers1[1])
            z1 = float(numbers1[2])

            R1 = (x1 ** 2 + y1 ** 2 + z1 ** 2) ** 0.5
            if R1 < R:
                f2.write(s)

    f1.close()
    f2.close()


# Данную функцию нужно использовать если элементы в сравниваемых таблицах находятся в одном порядке.
# Перед использованием нужно привести файлы к типу "ADDA".
def compare(path1, path2, R, m, lines):
    print("Compare two files")
    f1 = open(path1, 'r')
    f1.readline()
    f2 = open(path2, 'r')
    f2.readline()
    count_nan = 0
    accuracy = 1e-2
    count = 0
    aver_error_l1 = 0
    aver_error_l2 = 0
    count_not_equal = 0
    count_one_root = 0
    count_two_root = 0
    count_no_root = 0
    aver_error_l1_one_root = 0
    aver_error_l1_two_root = 0
    aver_error_l1_no_root = 0
    aver_error_l2_one_root = 0
    aver_error_l2_two_root = 0
    aver_error_l2_no_root = 0
    while True:
        # Читаю входные файлы построчно:
        numbers1 = f1.readline()
        numbers2 = f2.readline()
        # Разбиваем строку на части, используя разделитель, и возвращаем эти части списком.
        numbers1 = numbers1.split()
        numbers2 = numbers2.split()
        # Конец файла.
        if len(numbers1) <= 1 or len(numbers2) <= 1:
            break
        x1 = float(numbers1[0])
        y1 = float(numbers1[1])
        z1 = float(numbers1[2])
        exr1 = float(numbers1[4])
        exi1 = float(numbers1[5])
        eyr1 = float(numbers1[6])
        eyi1 = float(numbers1[7])
        ezr1 = float(numbers1[8])
        ezi1 = float(numbers1[9])
        x2 = float(numbers2[0])
        y2 = float(numbers2[1])
        z2 = float(numbers2[2])
        exr2 = float(numbers2[4])
        exi2 = float(numbers2[5])
        eyr2 = float(numbers2[6])
        eyi2 = float(numbers2[7])
        ezr2 = float(numbers2[8])
        ezi2 = float(numbers2[9])
        # Проверка что элемент не nan:
        if isnan(exr1) or isnan(eyr1) or isnan(ezr1) or isnan(exi1) or isnan(eyi1) or isnan(ezi1) or \
                isnan(exr2) or isnan(eyr2) or isnan(ezr2) or isnan(exi2) or isnan(eyi2) or isnan(ezi2):
            count_nan += 1
            continue
        if isclose(x1, x2, abs_tol=accuracy) and isclose(y1, y2, abs_tol=accuracy) and isclose(z1, z2, abs_tol=accuracy):
            count += 1
            norm_value = norm(exr1, exi1, eyr1, eyi1, ezr1, ezi1, exr2, exi2, eyr2, eyi2, ezr2, ezi2)
            aver_error_l2 += norm_value ** 2
            aver_error_l1 += norm_value
            # Определим область куда попала точка
            ym, zm = coordinates_in_meridional_plane(x1, y1, z1, R)
            cur_region = region(ym, zm, R, m, lines)
            # Считаю суммарную ошибку в каждой области
            if cur_region == "one_root":
                aver_error_l2_one_root += norm_value ** 2
                aver_error_l1_one_root += norm_value
                count_one_root += 1
            elif cur_region == "two_roots":
                aver_error_l2_two_root += norm_value ** 2
                aver_error_l1_two_root += norm_value
                count_two_root += 1
            elif cur_region == "no_root":
                aver_error_l2_no_root += norm_value ** 2
                aver_error_l1_no_root += norm_value
                count_no_root += 1
            else:
                print("Error in compare function! Invalid region defined. ")
        else:
            count_not_equal += 1
    print("Number of elements which were in work = " + str(count) + '\n')
    print("Number of not equal elements = " + str(count_not_equal) + '\n')
    print("Number of nan elements = " + str(count_nan) + '\n')
    if count_not_equal > 0:
        print("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if count != 0:
        aver_error_l1 /= count
        aver_error_l2 /= count
        aver_error_l2 = aver_error_l2 ** 0.5
    if count_one_root != 0:
        aver_error_l1_one_root /= count_one_root
        aver_error_l2_one_root /= count_one_root
        aver_error_l2_one_root = aver_error_l2_one_root ** 0.5
    if count_two_root != 0:
        aver_error_l1_two_root /= count_two_root
        aver_error_l2_two_root /= count_two_root
        aver_error_l2_two_root = aver_error_l2_two_root ** 0.5
    if count_no_root != 0:
        aver_error_l1_no_root /= count_no_root
        aver_error_l2_no_root /= count_no_root
        aver_error_l2_no_root = aver_error_l2_no_root ** 0.5
    f1.close()
    f2.close()
    return aver_error_l2, aver_error_l2_one_root, aver_error_l2_two_root, aver_error_l2_no_root, \
           aver_error_l1, aver_error_l1_one_root, aver_error_l1_two_root, aver_error_l1_no_root

# Функция для конвертации scattnlay, bhfield в adda.
# Проверил функцию для size = 10, grid = 16. Координатная сетка совпадает.
# path1 - путь до файла scattnlay, bhfield.
# path2 - путь до файла куда сохранить.
# type - "bhfield", "scattnlay"
# R - радиус сферы.
# grid - сетка.
def scattnlay_bhfield_to_adda(path1, path2, type, R, grid):
    count_nan = 0

    f1 = open(path1)
    if type == "bhfield":
        f1.readline()
        f1.readline()
    elif type == "scattnlay":
        f1.readline()
    else:
        print("Error in scattnlay_bhfield_to_adda()! Unknown type.")

    f2 = open(path2, 'w')
    f2.write('x y z |E|^2 Ex.r Ex.i Ey.r Ey.i Ez.r Ez.i \n')

    if type == "bhfield":
        while True:
            numbers1 = f1.readline()
            if len(numbers1) == 0:  # Нулевая длина обозначает конец файла (EOF)
                break
            numbers1 = numbers1.split()
            if len(numbers1) <= 1:
                break
            x1 = float(numbers1[0])
            y1 = float(numbers1[1])
            z1 = float(numbers1[2])
            R1 = (x1 ** 2 + y1 ** 2 + z1 ** 2) ** 0.5
            if R1 > R:
                continue

            exr = float(numbers1[3])
            eyr = float(numbers1[4])
            ezr = float(numbers1[5])
            exi = float(numbers1[6])
            eyi = float(numbers1[7])
            ezi = float(numbers1[8])
            e = exr ** 2 + exi ** 2 + eyr ** 2 + eyi ** 2 + ezr ** 2 + ezi ** 2
            f2.write(str(x1) + ' ' + str(y1) + ' ' + str(z1) + ' ' +
                     str(e) + ' ' +
                     str(exr) + ' ' + str(exi) + ' ' +
                     str(eyr) + ' ' + str(eyi) + ' ' +
                     str(ezr) + ' ' + str(ezi) + ' ' +
                     '\n')
    elif type == "scattnlay":
        for k in range(grid):
            for j in range(grid):
                for i in range(grid):
                    numbers1 = linecache.getline(path1, 2 + grid * grid * i + grid * j + k)

                    if len(numbers1) == 0:  # Нулевая длина обозначает конец файла (EOF)
                        break

                    if len(numbers1) <= 1: # Чтобы убрать в scattnlay в конце файла дополнительную строку.
                        break
                    numbers1 = numbers1.split(", ")

                    if len(numbers1) <= 1:
                        break

                    x1 = float(numbers1[0])
                    y1 = float(numbers1[1])
                    z1 = float(numbers1[2])
                    R1 = (x1 ** 2 + y1 ** 2 + z1 ** 2) ** 0.5
                    if R1 > R:
                        continue

                    exr = float(numbers1[3])
                    exi = float(numbers1[4])
                    eyr = float(numbers1[5])
                    eyi = float(numbers1[6])
                    ezr = float(numbers1[7])
                    ezi = float(numbers1[8])

                    if isnan(exr) or isnan(eyr) or isnan(ezr) or isnan(exi) or isnan(eyi) or isnan(ezi):
                        count_nan += 1
                        continue

                    e = exr ** 2 + exi ** 2 + eyr ** 2 + eyi ** 2 + ezr ** 2 + ezi ** 2
                    f2.write(str(x1) + ' ' + str(y1) + ' ' + str(z1) + ' ' +
                             str(e) + ' ' +
                             str(exr) + ' ' + str(exi) + ' ' +
                             str(eyr) + ' ' + str(eyi) + ' ' +
                             str(ezr) + ' ' + str(ezi) + ' ' +
                             '\n')
    else:
        print("Error in scattnlay_bhfield_to_adda()! Unknown type.")

    if count_nan != 0:
        print("There is nan! Number of nan: ", count_nan)
    f1.close()
    f2.close()









