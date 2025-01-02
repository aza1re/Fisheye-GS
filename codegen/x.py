from sympy import *
import random
import numpy as np
from tqdm import tqdm

# define variable
x, y, w = symbols('x y w', real=True)
z = symbols('z', positive=True)
x_1, y_1, w_1 = symbols('x_1 y_1 w_1', real=True)
w = 1
# X, Y = symbols('X Y')

# define constant
f_x, f_y = symbols('f_x f_y')
c_x, c_y = symbols('c_x c_y')
z_1 = symbols('z_1')
z_1 = 0

# fisheye projection
theta1, lz, l2, X1, Y1 = symbols('theta l_{z} l_2 X Y')
theta = atan(sqrt((x ** 2 + y ** 2) / z ** 2))
l_z = sqrt(x ** 2 + y ** 2)
# l_2 = x ** 2 + y ** 2 + z ** 2
l_2 = l_z ** 2 + z ** 2
X = f_x * x * theta / l_z + c_x
Y = f_y * y * theta / l_z + c_y
X1 = simplify(X)
Y1 = simplify(Y)

lz2 = symbols('lz2')
lz_2 = lz ** 2

def ss(x):
    global theta, theta1, l_z, lz, l_2, l2, lz2, lz_2
    x_expr = x.subs([(lz_2, lz2)])
    x_expr = simplify(x_expr)
    x_expr = x_expr.subs([(theta, theta1), (l_z, lz), (l_2, l2)])
    x_expr = factor(cancel(x_expr))
    return simplify(x_expr)
    
    
print("\\theta=", latex(theta))
print("l_z=", latex(l_z))
print("l_2=", latex(l_2))

X_expr = ss(X1)
Y_expr = ss(Y1)

print("X=", latex(X_expr))
print("Y=", latex(Y_expr))

# Jacobian Matrix
p = Matrix([x, y, z])
P = Matrix([X, Y])
J = P.jacobian(p)
J_expr = ss(J)

print("J=", latex(J_expr))

# Gradients of Covariance
dJx = diff(J, x)
dJy = diff(J, y)
dJz = diff(J, z)

# dJx_expr = simplify(dJx).subs([(theta, theta1), (l_z, lz), (l_2, l2)])
# dJy_expr = simplify(dJy).subs([(theta, theta1), (l_z, lz), (l_2, l2)])
# dJz_expr = simplify(dJz).subs([(theta, theta1), (l_z, lz), (l_2, l2)])

# dJx_expr = factor(cancel(dJx_expr))
# dJy_expr = factor(cancel(dJy_expr))
# dJz_expr = factor(cancel(dJz_expr))

dJx_expr = ss(dJx)
dJy_expr = ss(dJy)
dJz_expr = ss(dJz)

print("\dfrac{\partial{J}}{\partial{x}}=",latex(dJx_expr))
print("\dfrac{\partial{J}}{\partial{y}}=",latex(dJy_expr))
print("\dfrac{\partial{J}}{\partial{x}}=",latex(dJz_expr))

E = -l_2 ** 2 * l_z ** 2 * theta + l_2 * l_z ** 3 * z
F = 3 * l_2 ** 2 * theta - 3 * l_2 * l_z * z - 2 * l_z ** 3 * z

# E = E.subs([(theta, theta1), (l_z, lz), (l_2, l2)])
# F = F.subs([(theta, theta1), (l_z, lz), (l_2, l2)])

A = x * (3 * E + x ** 2 * F)
B = y * (E + x ** 2 * F)
C = x * (E + y ** 2 * F)
D = y * (3 * E + y ** 2 * F)

FM = l_2 ** 2 * l_z ** 5

S = x ** 2 - y ** 2 - z ** 2
T = y ** 2 - x ** 2 - z ** 2

# A1, B1, C1, D1, E1, F1, FM1 = symbols('A B C D E F FM')

# A = A.subs([(theta, theta1), (l_z, lz), (l_2, l2)])
# B = B.subs([(theta, theta1), (l_z, lz), (l_2, l2)])
# C = C.subs([(theta, theta1), (l_z, lz), (l_2, l2)])
# D = D.subs([(theta, theta1), (l_z, lz), (l_2, l2)])
# FM = FM.subs([(theta, theta1), (l_z, lz), (l_2, l2)])

dJx1 = Matrix(([[f_x * A / FM, f_x * B / FM, f_x * S / (l_2 ** 2)],
               [f_y * B / FM, f_y * C / FM, 2 * f_y * x * y / (l_2 ** 2)]]))
dJy1 = Matrix(([[f_x * B / FM, f_x * C / FM, 2 * f_x * x * y / (l_2 ** 2)],
               [f_y * C / FM, f_y * D / FM, f_y * T / (l_2 ** 2)]]))
dJz1 = Matrix(([[f_x * S / (l_2 ** 2), 2 * f_x * x * y / (l_2 ** 2), 2 * f_x * x * z / (l_2 ** 2)],
                [2 * f_y * x * y / (l_2 ** 2), f_y * T / (l_2 ** 2), 2 * f_y * y * z / (l_2 ** 2)]]))


x_val = -1.7192244530
y_val = -0.7767219543
z_val = 9.855030823
h_x = 2317.6450195312
h_y = 2317.6450195312

subs = [(x, x_val), (y, y_val), (z, z_val), (f_x, h_x), (f_y, h_y)]
J_val = J.subs(subs)
dJx_val = dJx.subs(subs)
dJy_val = dJy.subs(subs)
dJz_val = dJz.subs(subs)
print("J = ", J_val)
print("dJx_val = ", dJx_val)
print("dJy_val = ", dJy_val)
print("dJz_val = ", dJz_val)
# Test
# for idx in tqdm(range(500)):
#     def rand():
#         return random.uniform(0.1, 2.0)
    
#     class CustomError:
#         def __init__(self, index):
#             print("FAILED TO PASS NUMERICAL TEST! idx: ", index)
        
#     sx, sy, sz, sfx, sfy = rand(), rand(), rand(), rand(), rand()
#     dJx_res = dJx.subs([(x, sx), (y, sy), (z, sz), (f_x, sfx),(f_y, sfy)])
#     dJy_res = dJy.subs([(x, sx), (y, sy), (z, sz), (f_x, sfx),(f_y, sfy)])
#     dJz_res = dJz.subs([(x, sx), (y, sy), (z, sz), (f_x, sfx),(f_y, sfy)])
#     dJx1_res = dJx1.subs([(x, sx), (y, sy), (z, sz), (f_x, sfx),(f_y, sfy)])
#     dJy1_res = dJy1.subs([(x, sx), (y, sy), (z, sz), (f_x, sfx),(f_y, sfy)])
#     dJz1_res = dJz1.subs([(x, sx), (y, sy), (z, sz), (f_x, sfx),(f_y, sfy)])
#     dis1 = (dJx_res - dJx1_res)
#     dis2 = (dJy_res - dJy1_res)
#     dis3 = (dJz_res - dJz1_res)
#     qwq = dis1.norm() + dis2.norm() + dis3.norm()
#     if qwq > 1e-8:
#         print(idx)
#         raise CustomError
    
    