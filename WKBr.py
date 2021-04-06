from BoundaryLines import BoundaryLines
from optical_len import optical_len
from math import sin, cos, exp
from Coordinate_systems import apply_rotation_electric_field_vector, sum_ef, apply_transmission_coefficient


# Function for finding the argument of the exponent of the electric field of the transmitted wave:
# l1 - outside the particle
# l2 - in the particle
def find_arg(k, radius, m, l1, l2):
    return - k * radius + k * l1 + k * m * l2


# Function for finding the attenuation of the electric field of the transmitted wave:
def find_attenuation(k, l2, mi, cos_t):
    return exp(- k * mi * l2 * cos_t)


# A plane wave is incident along the z axis.
def find_wkb_ef(x_arr, y_arr, z_arr, m, mi, radius, k, path, grid, type="analytic", find_grid=False,
                solution_method="iterative"):
    # Separate regions using rays:
    lines = BoundaryLines(m, radius)
    # Find electric field WKB:
    f = open(path, 'w')
    f.write('x y z |E|^2 Ex.r Ex.i Ey.r Ey.i Ez.r Ez.i \n')
    num_one_root = 0
    num_two_roots = 0
    num_no_roots = 0

    diameter = 2 * radius
    d = diameter / grid
    start = (-diameter + d) / 2
    finish = (diameter - d) / 2
    i = 0
    x_cur = start - d
    y_cur = start
    z_cur = start
    while True:
        if find_grid:
            # Build a coordinate grid.
            x_cur += d
            if x_cur > finish:
                x_cur = start
                y_cur += d
                if y_cur > finish:
                    print('z = ', z_cur)
                    y_cur = start
                    z_cur += d
                    if z_cur > finish:
                        break
            R_cur = (x_cur ** 2 + y_cur ** 2 + z_cur ** 2) ** 0.5
            if radius < R_cur:
                continue
        else:
            # Use the already made grid.
            if i == len(x_arr):
                # End of calculations:
                break
            else:
                x_cur = x_arr[i]
                y_cur = y_arr[i]
                z_cur = z_arr[i]
                i += 1

        # The boundary is set analytically (not like in ADDA).
        # The usual sphere equation is used here. 0 coordinate system at the center of the sphere.
        z_ = - (radius ** 2 - x_cur ** 2 - y_cur ** 2) ** 0.5
        l1, l2, l1_2, l2_2, type2, cur_region, t_per1, t_per2, t_par1, t_par2, da1, da2, rotation_angle, \
        cos_t1, cos_t2, N1, K1, N2, K2 \
            = optical_len(x_cur,
                          y_cur,
                          z_cur,
                          z_,
                          m,
                          mi,
                          radius,
                          type,
                          lines,
                          k,
                          solution=solution_method)

        if type2 == "discrete" or \
                (type2 == "analytic" and
                 type != "wkb+refraction6" and
                 type != "wkb+refraction7" and
                 type != "wkb+refraction8" and
                 type != "wkb+refraction9") or \
                type2 == "wkb+refraction":
            # WKBr version 1.
            arg = find_arg(k, radius, N1, l1, l2)
            attenuation1 = find_attenuation(k, l2, K1, cos_t1)
            exr_new = cos(arg) * attenuation1
            exi_new = sin(arg) * attenuation1
            eyr_new = 0
            eyi_new = 0
            ezr_new = 0
            ezi_new = 0
            e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
            num_one_root += 1
        elif type == "wkb+refraction6":
            # WKBr version 2.
            if cur_region == "one_root" or cur_region == "two_roots" or cur_region == "no_root":
                arg = find_arg(k, radius, N1, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                exr_new = cos(arg) * attenuation1
                exi_new = sin(arg) * attenuation1
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = \
                    apply_rotation_electric_field_vector(exr_new, exi_new, da1)
                e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_one_root += 1
            else:
                print("Error in find_wkb_ef() function, in elif type == wkb+refraction6")
        elif type == "wkb+refraction7":
            # WKBr version 3.
            if cur_region == "one_root" or cur_region == "no_root":
                arg = find_arg(k, radius, N1, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                exr_new = cos(arg) * attenuation1
                exi_new = sin(arg) * attenuation1
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = \
                    apply_rotation_electric_field_vector(exr_new, exi_new, da1)
                e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_one_root += 1
            elif cur_region == "two_roots":
                arg1 = find_arg(k, radius, N1, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                arg2 = find_arg(k, radius, N2, l1_2, l2_2)
                attenuation2 = find_attenuation(k, l2_2, K2, cos_t2)
                exr_new1 = cos(arg1) * attenuation1
                exr_new2 = cos(arg2) * attenuation2
                exi_new1 = sin(arg1) * attenuation1
                exi_new2 = sin(arg2) * attenuation2
                exr_new1, exi_new1, eyr_new1, eyi_new1, ezr_new1, ezi_new1 = \
                    apply_rotation_electric_field_vector(exr_new1, exi_new1, da1)
                exr_new2, exi_new2, eyr_new2, eyi_new2, ezr_new2, ezi_new2 = \
                    apply_rotation_electric_field_vector(exr_new2, exi_new2, da2)
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = sum_ef(exr_new1, exr_new2, exi_new1, exi_new2,
                                                                              eyr_new1, eyr_new2, eyi_new1, eyi_new2,
                                                                              ezr_new1, ezr_new2, ezi_new1, ezi_new2)
                e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_two_roots += 1
        elif type == "wkb+refraction8":
            # WKBr version 4.
            if cur_region == "one_root":
                arg = find_arg(k, radius, N1, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                exr_new = cos(arg) * attenuation1
                exi_new = sin(arg) * attenuation1
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = \
                    apply_rotation_electric_field_vector(exr_new, exi_new, da1)
                e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_one_root += 1
            elif cur_region == "two_roots":
                arg1 = find_arg(k, radius, N1, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                arg2 = find_arg(k, radius, N2, l1_2, l2_2)
                attenuation2 = find_attenuation(k, l2_2, K2, cos_t2)
                exr_new1 = cos(arg1) * attenuation1
                exr_new2 = cos(arg2) * attenuation2
                exi_new1 = sin(arg1) * attenuation1
                exi_new2 = sin(arg2) * attenuation2
                exr_new1, exi_new1, eyr_new1, eyi_new1, ezr_new1, ezi_new1 = \
                    apply_rotation_electric_field_vector(exr_new1, exi_new1, da1)
                exr_new2, exi_new2, eyr_new2, eyi_new2, ezr_new2, ezi_new2 = \
                    apply_rotation_electric_field_vector(exr_new2, exi_new2, da2)
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = sum_ef(exr_new1, exr_new2, exi_new1, exi_new2,
                                                                              eyr_new1, eyr_new2, eyi_new1, eyi_new2,
                                                                              ezr_new1, ezr_new2, ezi_new1, ezi_new2)
                e = (exr_new ** 2 + exi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_two_roots += 1
            elif cur_region == "no_root":
                exr_new = 0
                exi_new = 0
                eyr_new = 0
                eyi_new = 0
                ezr_new = 0
                ezi_new = 0
                e = 0
                num_no_roots += 1
            else:
                print("Error in find_wkb_ef() function, in elif type == wkb+refraction8")
        elif type == "wkb+refraction9":
            # WKBr version 5.
            if cur_region == "one_root":
                arg = find_arg(k, radius, N1, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                exr_new = cos(arg) * attenuation1
                exi_new = sin(arg) * attenuation1
                exr_new, exi_new, eyr_new, eyi_new = \
                    apply_transmission_coefficient(exr_new, exi_new, t_per1, t_par1, rotation_angle)
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = \
                    apply_rotation_electric_field_vector(exr_new, exi_new, da1)
                e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_one_root += 1
            elif cur_region == "two_roots":
                arg1 = find_arg(k, radius, m, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                arg2 = find_arg(k, radius, m, l1_2, l2_2)
                attenuation2 = find_attenuation(k, l2_2, K2, cos_t2)
                exr_new1 = cos(arg1) * attenuation1
                exr_new2 = cos(arg2) * attenuation2
                exi_new1 = sin(arg1) * attenuation1
                exi_new2 = sin(arg2) * attenuation2
                exr_new1, exi_new1, eyr_new1, eyi_new1 = \
                    apply_transmission_coefficient(exr_new1, exi_new1, t_per1, t_par1, rotation_angle)
                exr_new1, exi_new1, eyr_new1, eyi_new1, ezr_new1, ezi_new1 = \
                    apply_rotation_electric_field_vector(exr_new1, exi_new1, da1)
                exr_new2, exi_new2, eyr_new2, eyi_new2 = \
                    apply_transmission_coefficient(exr_new2, exi_new2, t_per2, t_par2, rotation_angle)
                exr_new2, exi_new2, eyr_new2, eyi_new2, ezr_new2, ezi_new2 = \
                    apply_rotation_electric_field_vector(exr_new2, exi_new2, da2)
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = sum_ef(exr_new1, exr_new2, exi_new1, exi_new2,
                                                                              eyr_new1, eyr_new2, eyi_new1, eyi_new2,
                                                                              ezr_new1, ezr_new2, ezi_new1, ezi_new2)
                e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_two_roots += 1
            elif cur_region == "no_root":
                exr_new = 0
                exi_new = 0
                eyr_new = 0
                eyi_new = 0
                ezr_new = 0
                ezi_new = 0
                e = 0
                num_no_roots += 1
            else:
                print("Error in find_wkb_ef() function, in elif type == wkb+refraction9")
        elif type == "wkb+refraction10":
            # WKBr version 6.
            # Всё то же что в WKBr version 2, но добавляем зануление эл. поля в области R0.
            if cur_region == "one_root" or cur_region == "two_roots":
                arg = find_arg(k, radius, N1, l1, l2)
                attenuation1 = find_attenuation(k, l2, K1, cos_t1)
                exr_new = cos(arg) * attenuation1
                exi_new = sin(arg) * attenuation1
                if mi != 0:
                    exr_new, exi_new, eyr_new, eyi_new = \
                        apply_transmission_coefficient(exr_new, exi_new, t_per1, t_par1, rotation_angle)
                exr_new, exi_new, eyr_new, eyi_new, ezr_new, ezi_new = \
                    apply_rotation_electric_field_vector(exr_new, exi_new, da1)
                e = (exr_new ** 2 + exi_new ** 2 + eyr_new ** 2 + eyi_new ** 2 + ezr_new ** 2 + ezi_new ** 2) ** 0.5
                num_one_root += 1
            elif cur_region == "no_root":
                exr_new = 0
                exi_new = 0
                eyr_new = 0
                eyi_new = 0
                ezr_new = 0
                ezi_new = 0
                e = 0
                num_no_roots += 1
            else:
                print("Error in find_wkb_ef() function, in elif type == wkb+refraction6")
        else:
            print("Error in find_wkb_ef() function!")

        f.write(str(x_cur) + ' ' + str(y_cur) + ' ' + str(z_cur) + ' ' + str(e) + ' '
                + str(exr_new) + ' ' + str(exi_new) + ' '
                + str(eyr_new) + ' ' + str(eyi_new) + ' '
                + str(ezr_new) + ' ' + str(ezi_new) + '\n')

    f.close()

    print("Number of dots in one root region = ", num_one_root)
    print("Number of dots in two root region = ", num_two_roots)
    print("Number of dots in no root region = ", num_no_roots)
    sum_ = num_no_roots + num_one_root + num_two_roots
    print("Number of all dots = ", sum_)

    return sum_, num_no_roots, num_one_root, num_two_roots