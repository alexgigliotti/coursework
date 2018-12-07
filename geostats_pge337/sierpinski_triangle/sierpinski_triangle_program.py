import numpy as np
import matplotlib.pyplot as plt
import animatplot as aplt


def calc_points(n_dots, start_pt, triangle_pts, pt_list):
    for i in range(0, n_dots):  # Edit later without for loop. Use Numpy
        rand_vert = np.random.randint(0, 3)
        new_point = [(triangle_pts[rand_vert][0] + start_pt[0]) / 2, (triangle_pts[rand_vert][1] + start_pt[1]) / 2]
        pt_list[i] = new_point
        start_pt = new_point

    return point_list

triangle_points = [[1/np.sqrt(3), 0], [0, 1], [-1/np.sqrt(3), 0]]

x_start = 0
y_start = 0
start_point = [x_start, y_start]
n = 10000
point_list = np.zeros([n, 2])
point_list = calc_points(n, start_point, triangle_points, point_list)

t = np.linspace(1, n, n)
x = point_list[:, 0]
y = point_list[:, 1]
X, Y = aplt.util.parametric_line(x, y)

timeline = aplt.Timeline(t, r'$\ pts$', fps=60)

ax = plt.axes()
for j in range(0, len(triangle_points)):
    plt.plot(triangle_points[j][0], triangle_points[j][1], 'ro')
plt.plot(x_start, y_start, 'bo')
plt.axis('equal')
plt.grid()

block1 = aplt.blocks.Line(X, Y, ax, marker='o', color='k', linestyle='', markersize='0.5')
# or equivalently
# block1 = aplt.blocks.ParametricLine(x, y, ax)

anim = aplt.Animation([block1], timeline)

# Your standard matplotlib stuff
plt.title('Sierpinski Triangle')
plt.xlabel('x')
plt.ylabel('y')

# Create Interactive Elements
anim.toggle()
anim.timeline_slider()

# anim.save('parametric.gif', writer=PillowWriter(fps=5))
plt.show()

