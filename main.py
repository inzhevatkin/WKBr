from WKBr import find_wkb_ef, find_convergence_factor
# from math import pi, sin, asin

# print(find_convergence_factor(1, 2.5, 0.5, pi/4, asin(sin(pi/4)/2.5)))
mypath = "C:/Users/konstantin/Documents/main-script/data 100, grid 160, section (convergence factor)/"
find_wkb_ef(0, 0, 0, m=1.1, mi=0, radius=100, k=1, path=mypath, grid=160, type="wkb+refraction11", find_grid=True)

