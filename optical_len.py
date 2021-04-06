from iterative_method import iterative_method
from BoundaryLines import region
from Fresnel_coefficients import transmission_coefficient, effective_refractive_indices
from Coordinate_systems import coordinates_in_meridional_plane, find_rotation_angle_in_mp, coordinates_in_lab_plane, \
    delta_angle, cos_refracted_angle_mp


# laboratory coordinate system - zero at the center of the sphere.
# x2_lab, y2_lab, z2_lab - coordinates of the point where the ray came in (lab. c.s.).
# z_ - the coordinate of the ray entrance into the sphere (WKB).
# type_ - "wkb+refraction", "analytic", "discrete".
# solution - "polynom", "approximate", "iterative".
def optical_len(x2_lab, y2_lab, z2_lab, z_, m, mi, radius, type_, lines, k, solution="iterative"):
    # Go to the meridian plane:
    y2, z2 = coordinates_in_meridional_plane(x2_lab, y2_lab, z2_lab, radius)
    # Find rotation angle:
    rotation_angle = find_rotation_angle_in_mp(x2_lab, y2_lab)

    # For WKBr:
    if type_ == "wkb+refraction" or type_ == "wkb+refraction2" or type_ == "wkb+refraction3" or \
            type_ == "wkb+refraction4" or type_ == "wkb+refraction5" or type_ == "wkb+refraction6" \
            or type_ == "wkb+refraction7" or type_ == "wkb+refraction8" or type_ == "wkb+refraction9"\
            or type_ == "wkb+refraction10":
        try:
            # Определили выходные параметры.
            info = "not_success"
            y1 = 0
            z1 = 0
            y1_2 = 0
            z1_2 = 0
            # Используем итеративный алгоритм:
            if solution == "iterative":
                if type_ == "wkb+refraction" or type_ == "wkb+refraction4" or type_ == "wkb+refraction5" \
                        or type_ == "wkb+refraction6":
                    # Используем область с одним решением.
                    # Первый вариант: в области 1, 2-х решений находим только один корень.
                    # В области 0 решений используем WKB.
                    cur_region = region(y2, z2, radius, m, lines)
                    if cur_region == "one_root" or cur_region == "two_roots":
                        cur_region = "one_root"
                        info, y1, z1, y1_2, z1_2 = iterative_method(y2, z2, radius, m, "one_root")
                    elif cur_region == "no_root":
                        info, y1, z1, y1_2, z1_2 = iterative_method(y2, z2, radius, m, "no_root")
                    else:
                        print("Error in optical_len() function! In if type_ == wkb+refraction.")
                elif type_ == "wkb+refraction2" or type_ == "wkb+refraction7":
                    # Используем область с одним и с двумя решениями.
                    # Второй вариант: в области 1, 2-х решений находим 1, 2 корня соответственно.
                    # В области 0 решений используем WKB.
                    cur_region = region(y2, z2, radius, m, lines)
                    info, y1, z1, y1_2, z1_2 = iterative_method(y2, z2, radius, m, cur_region)
                elif type_ == "wkb+refraction3":
                    # Используем область с одним и без решений.
                    # Третий вариант: в области 1, 2-х решений находим только один корень.
                    # В области 0 решений зануляем поле.
                    cur_region = region(y2, z2, radius, m, lines)
                    if cur_region == "one_root" or cur_region == "two_roots":
                        cur_region = "one_root"
                        info, y1, z1, y1_2, z1_2 = iterative_method(y2, z2, radius, m, "one_root")
                    elif cur_region == "no_root":
                        info = "no_calculation"
                    else:
                        print("Error in optical_len() function! In if type_ == wkb+refraction3.")
                elif type_ == "wkb+refraction8" or type_ == "wkb+refraction9":
                    # Используем область с одним и с двумя решениями.
                    # в области 1, 2-х решений находим 1, 2 корня соответственно.
                    # В области 0 решений зануляем поле.
                    cur_region = region(y2, z2, radius, m, lines)
                    if cur_region == "one_root" or cur_region == "two_roots":
                        info, y1, z1, y1_2, z1_2 = iterative_method(y2, z2, radius, m, cur_region)
                    elif cur_region == "no_root":
                        info = "no_calculation"
                elif type_ == "wkb+refraction10":
                    # в области 1, 2-х решений находим 1 корень.
                    # В области 0 решений зануляем поле.
                    cur_region = region(y2, z2, radius, m, lines)
                    if cur_region == "one_root" or cur_region == "two_roots":
                        info, y1, z1, y1_2, z1_2 = iterative_method(y2, z2, radius, m, "one_root")
                    elif cur_region == "no_root":
                        info = "no_calculation"
                    else:
                        print("Error in optical_len() function! In if type_ == wkb+refraction10.")
                else:
                    print("Error in optical_len() function! No such type. ")
            else:
                print("Error in optical_len() function! In if solution == iterative")
        except RuntimeError as error:
            print("Oops!", sys.exc_info()[0], "occured.")
            print(error)
            print("y2, z2 - ", y2, z2)
            info = "not_success"

        if info == "success":
            if cur_region == "one_root" or cur_region == "no_root":
                l1 = z1
                l2 = ((y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
                l1_2 = 0
                l2_2 = 0
                # Nr, Ni = find_adjusted_refractive_indices(m, mi, y1 / radius)
                t_per1, t_par1 = transmission_coefficient(y1, radius, m, mi, k)
                t_per2 = 0
                t_par2 = 0
                x1_lab, y1_lab, z1_lab = coordinates_in_lab_plane(y1, z1, rotation_angle, radius)
                da1 = delta_angle(x1_lab, radius, m)
                da2 = 0
                cos_t1 = cos_refracted_angle_mp(y1, radius, m)
                cos_t2 = 0
                N1, K1 = effective_refractive_indices(m, mi, cos_t1)
                N2, K2 = 0, 0
            elif cur_region == "two_roots":
                l1 = z1
                l2 = ((y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
                l1_2 = z1_2
                l2_2 = ((y2 - y1_2) ** 2 + (z2 - z1_2) ** 2) ** 0.5
                # Nr, Ni = find_adjusted_refractive_indices(m, mi, y1 / radius)
                # Nr2, Ni2 = find_adjusted_refractive_indices(m, mi, y1_2 / radius)
                t_per1, t_par1 = transmission_coefficient(y1, radius, m, mi, k)
                t_per2, t_par2 = transmission_coefficient(y1_2, radius, m, mi, k)
                x1_lab, y1_lab, z1_lab = coordinates_in_lab_plane(y1, z1, rotation_angle, radius)
                x1_lab_2, y1_lab_2, z1_lab_2 = coordinates_in_lab_plane(y1_2, z1_2, rotation_angle, radius)
                da1 = delta_angle(x1_lab, radius, m)
                da2 = delta_angle(x1_lab_2, radius, m)
                cos_t1 = cos_refracted_angle_mp(y1, radius, m)
                cos_t2 = cos_refracted_angle_mp(y1_2, radius, m)
                N1, K1 = effective_refractive_indices(m, mi, cos_t1)
                N2, K2 = effective_refractive_indices(m, mi, cos_t2)
            else:
                print("Error in optical_len() function!")
        elif info == "not_success":
            type_ = "analytic"
        elif info == "no_calculation":
            # Данный код выполняется если мы не хотим ничего считать и зануляем электрическое поле.
            l1 = 0
            l2 = 0
            l1_2 = 0
            l2_2 = 0
            t_per1 = 0
            t_per2 = 0
            t_par1 = 0
            t_par2 = 0
            da1 = 0
            da2 = 0
            cos_t1 = 0
            cos_t2 = 0
            N1, K1, N2, K2 = 0, 0, 0, 0
        else:
            print("Error in optical_len() function!")

    if type_ == "analytic" or type_ == "discrete":
        l1 = (z_ + radius)
        l2 = (z2_lab - z_)
        l1_2 = 0
        l2_2 = 0
        cur_region = "one_root"
        # в случае WKB нет преломления, поэтому вместо y1 использую y2.
        t_per1, t_par1 = transmission_coefficient(y2, radius, m, mi, k)
        t_per2 = t_per1
        t_par2 = t_par1
        x1_lab, y1_lab, z1_lab = coordinates_in_lab_plane(y2, z2, rotation_angle, radius)
        da1 = delta_angle(x1_lab, radius, m)
        da2 = da1
        cos_t1 = cos_refracted_angle_mp(y2, radius, m)
        cos_t2 = cos_refracted_angle_mp(y2, radius, m)
        N1, K1 = effective_refractive_indices(m, mi, cos_t1)
        N2, K2 = effective_refractive_indices(m, mi, cos_t2)

    return l1, l2, l1_2, l2_2, type_, cur_region, t_per1, t_per2, t_par1, t_par2, da1, da2, rotation_angle, \
           cos_t1, cos_t2, N1, K1, N2, K2