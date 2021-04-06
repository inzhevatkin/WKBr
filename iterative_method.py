

# Exact solution using iterative method.
# The function returns the coordinates of the input point (y1, z1) and root_flag = True (if point is found).
def func(y2, z2, R, m, init_approx):
    y1 = 0
    z1 = 0
    count = 0
    root_flag = False

    sin = init_approx
    cos = (1 - sin ** 2) ** 0.5
    tmp1 = (m ** 2 - sin ** 2) ** 0.5
    g = sin * (tmp1 - cos) / (sin ** 2 + cos * tmp1)

    while count < 200:
        # По оценке правой функции (g) нахожу новый синус (sin_new):
        tmp2 = y2 + (z2 - R) * g
        tmp3 = (1 + g ** 2)
        sin_new = (tmp2 + g * (tmp3 * R ** 2 - tmp2 ** 2) ** 0.5) / (tmp3 * R)
        # Нахожу чему при данном синусе (sin_new) равна функция справа:
        cos_new = (1 - sin_new ** 2) ** 0.5
        tmp1_new = (m ** 2 - sin_new ** 2) ** 0.5
        g_new = sin_new * (tmp1_new - cos_new) / (sin_new ** 2 + cos_new * tmp1_new)
        # Нахожу чему при данном синусе (sin_new) равна функция слева:
        fnew = (R * sin_new - y2) / (z2 + R * (cos_new - 1))
        d = abs(fnew - g_new)
        if d < 1e-8:
            y1 = sin_new * R
            root_flag = True
            break
        count += 1
        g = g_new

    if root_flag and y2 <= y1 < R:
        z1 = - (R ** 2 - y1 ** 2) ** 0.5 + R
        if z2 < z1 <= R:
            root_flag = False
    else:
        root_flag = False

    return root_flag, y1, z1


# The function solves the equation and finds the right root.
def func2(y2, z2, R, m, init_approx):
    y1 = 0
    z1 = 0
    count = 0
    root_flag = False

    sin = init_approx
    cos = (1 - sin ** 2) ** 0.5
    f = (R * sin - y2) / (z2 - R * (1 - cos))

    while count < 200:
        # По оценке левой функции (f) нахожу новый синус (sin_new):
        tmp1 = 1 + m ** 2 + 2 * m * (1 / (1 + f ** 2)) ** 0.5
        tmp2 = f ** 2 * (1 + m ** 2) ** 2 + (m ** 2 - 1) ** 2
        sin_new = f * m * (tmp1 / tmp2) ** 0.5

        # Нахожу чему при данном синусе (sin_new) равна функция слева:
        cos_new = (1 - sin_new ** 2) ** 0.5
        f_new = (R * sin_new - y2) / (z2 - R * (1 - cos_new))

        # Нахожу чему при данном синусе (sin_new) равна функция справа:
        tmp1 = (m ** 2 - sin_new ** 2) ** 0.5
        f2 = sin_new * (tmp1 - cos_new) / (sin_new ** 2 + cos_new * tmp1)
        d = abs(f2 - f_new)
        if d < 1e-8:
            y1 = sin_new * R
            root_flag = True
            break
        count += 1
        f = f_new

    if root_flag and y2 <= y1 < R:
        z1 = - (R ** 2 - y1 ** 2) ** 0.5 + R
        if z2 < z1 <= R:
            root_flag = False
    else:
        root_flag = False

    return root_flag, y1, z1


def iterative_method(y2, z2, R, m, cur_region):
    info = "not_success"
    y1 = 0
    z1 = 0
    y1_2 = 0
    z1_2 = 0
    if cur_region == "one_root":
        root_flag, y1, z1 = func(y2, z2, R, m, y2 / R)
        if root_flag:
            if 0 <= y1 <= R and 0 <= z1 <= R:
                info = "success"
            else:
                print("Error in iterative_method() function! 0 <= y1 <= R and 0 <= z1 <= R not performed.")
                info = "not_success"
    elif cur_region == "two_roots":
        root_flag, y1, z1 = func(y2, z2, R, m, y2 / R)
        root_flag2, y1_2, z1_2 = func2(y2, z2, R, m, 1)
        if root_flag and root_flag2:
            if 0 <= y1 <= y1_2 <= R and 0 <= z1 <= z1_2 <= R:
                info = "success"
            else:
                print(
                    "Error in iterative_method() function! 0 <= y1 <= y1_2 <= R and 0 <= z1 <= z1_2 <= R not performed.")
                info = "not_success"
    elif cur_region == "no_root":
        info = "not_success"
    else:
        print("Error iterative_method() function!")
    return info, y1, z1, y1_2, z1_2