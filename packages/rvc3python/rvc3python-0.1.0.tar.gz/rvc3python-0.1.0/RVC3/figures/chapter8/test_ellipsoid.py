# test ellipsoid, take 2

import pyvista as pv
import numpy as np
from scipy import linalg as sp


sphere = pv.Sphere(radius=1)

# sphere.plot(show_edges=True, show_bounds=True)

E = np.diag([1, 1/2, 1/4])

# if not inverted:
#     E = np.linalg.inv(E)

pts = sp.sqrtm(E) @ sphere.points.T
sphere.points = pts.T

# e = (
#     s * sp.linalg.sqrtm(E) @ np.array([x.flatten(), y.flatten(), z.flatten()])
#     + np.c_[centre].T
# )
# return e[0, :].reshape(x.shape), e[1, :].reshape(x.shape), e[2, :].reshape(x.shape)
sphere.plot(show_edges=True, show_bounds=True)


plotter.add_axes(xlabel='X', ylabel='Y', zlabel='Z', line_width=5, 
    labels_off=False)