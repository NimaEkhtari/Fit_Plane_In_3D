# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 15:16:31 2023

This code uses different methods to calculate the normal vector of a plane given
a bunch of 3D points and also calculates the RMSE of the misclosure error.

@author: nekhtari
"""
import numpy as np
import matplotlib.pyplot as plt



''' ----------------------------------------------------------------------- '''
'''
Randomly creating n points in 3D space given parameters A, B, C, and D using
the plane equation
                        Ax + By + Cz = D

which can be re-written as
                        z = (D - (Ax + By)) / C
'''

A = -0.2
B = 0.36
C = 0.97
D = 2.2
n = 100
error_scale = 0.12

p = np.random.rand(n, 2)
pz = (D - np.sum(p * np.repeat(np.array([[A, B]]), n, axis = 0), axis = 1)) / C
pz = pz + (error_scale * np.random.randn(n, ))
points = np.column_stack((p, pz))





''' ----------------------------------------------------------------------- '''
'''
To begin with, we calculate the centroid of the points and adjust all 
coordinates relative to centroid. This helps insure a solution for methods
that require data stability when it comes to coordinate scales
'''
centroid = np.mean(points, axis=0)      # Mean of X, Y, Z coordinates = centroid
cr = points - centroid                  # Centroid removed points





''' ----------------------------------------------------------------------- '''
''' Method 1, using eigen values of centroid removed points '''
''' ----------------------------------------------------------------------- '''
Cov = np.cov(cr, rowvar=False)          # Covariance matrix of centroid-removed points
[val, vec] = np.linalg.eig(Cov)         # Eigen values and vectors of points
normal= vec[:, np.argmin(val)]
if normal[2] < 0: normal *= -1          # Ensure normal vector always points upward


residual = np.zeros((n,))
for jj in range(n):
    residual[jj] = np.dot(normal, points[jj])
std_residual = np.std(residual)

print('\n---- Using Eigen ----- ')    
print('normal vector: {}'.format(normal))
print('std of residuals: {}'.format(std_residual))




''' ----------------------------------------------------------------------- '''
''' Method 2, using SVD '''
''' ----------------------------------------------------------------------- '''
a, b, c = np.linalg.svd(cr)
Std_residual = min(b) / np.sqrt(n)
Normal = c[np.argmin(b)]
if Normal[2] < 0: Normal *= -1          # Ensure normal vector always points upward

print('\n---- Using SVD ----- ')
print('normal vector: {}'.format(Normal))
print('std of residuals: {}'.format(Std_residual))




''' ----------------------------------------------------------------------- '''
''' MEthod 3, Least squares adjustment along Z axis '''
''' The least squares method forms a coefficients (design) matrix with derivatives
    of a plane equation. 
                AX + BY + Z = D
                AX + BY - D = -Z
    The constraint is that C is set to 1 so the least squares solution minimizes
    sum of squares of delta_Z values.                                       '''
''' ----------------------------------------------------------------------- '''
AA = np.array([points[:, 0].T, points[:, 1].T, -np.ones(n).T]).T
L = -points[:, 2]
XX = np.matmul(np.linalg.inv(np.matmul(AA.T, AA)), np.matmul(AA.T, L))

nv = np.array([XX[0], XX[1], 1])
nv = nv / np.linalg.norm(nv)

res = np.matmul(AA, XX) - L
std_res = np.std(res)

print('\n---- Using Least Squares Along Z axis ----- ')
print('normal vector: {}'.format(nv))
print('std of residuals: {}'.format(std_res))

ang = np.arccos(np.dot(normal, nv)) * 180 / np.pi
print('\n----------------------------------')
print('angular difference between normal vectors calculated from SVD and least squares is {} degrees'.format(np.round(ang, 3)))




''' ----------------------------------------------------------------------- '''
''' Plotting points and the fit planes '''
''' ----------------------------------------------------------------------- '''
x_range = np.linspace(np.min(points[:,0]), np.max(points[:,0]), 10)
y_range = np.linspace(np.min(points[:,1]), np.max(points[:,1]), 10)
X, Y = np.meshgrid(x_range, y_range)
distance = -np.dot(normal, np.mean(points, axis=0))
Z = (-normal[0] * X - normal[1] * Y - distance) / normal[2]



fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Plot the points
ax.scatter(points[:,0], points[:,1], points[:,2], color='green', label='Original Points')

# Setting axes titles and plot title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Fitted Planes')
mi = np.min(points, axis = 0)
ma = np.max(points, axis = 0)
rg = np.max(ma - mi) / 2

ax.set_xlim(centroid[0] - rg, centroid[0] + rg)
ax.set_ylim(centroid[1] - rg, centroid[1] + rg)
ax.set_zlim(centroid[2] - rg, centroid[2] + rg)


''' Plot the best fit plane using SVD (or Eigenvalues and vectors) '''
ax.plot_surface(X, Y, Z, alpha=0.5, color='blue', label='Fitted Plane')


''' Plotting the fittend plane using Least Squares along Z axis '''
xx = X.reshape(X.size)
yy = Y.reshape(Y.size)
Z2 = - np.matmul(np.column_stack((xx, yy, -np.ones(xx.shape))), XX)
ax.plot_surface(X, Y, Z2.reshape(X.shape), alpha=0.5, color='red', label='LS Plane')


''' Plotting the normal vector to the best fit plane (SVD or Eig method) '''
scale = (np.max(points[:,2]) - np.min(points[:,2])) * 0.5
vx = np.array([centroid[0], scale * normal[0] + centroid[0]])
vy = np.array([centroid[1], scale * normal[1] + centroid[1]])
vz = np.array([centroid[2], scale * normal[2] + centroid[2]])
ax.plot3D(vx, vy, vz, color='blue', label='nomal svd')

''' Plotting the normal vector to the plane fit using least squares '''
vx = np.array([centroid[0], scale * nv[0] + centroid[0]])
vy = np.array([centroid[1], scale * nv[1] + centroid[1]])
vz = np.array([centroid[2], scale * nv[2] + centroid[2]])
ax.plot3D(vx, vy, vz, color='red', label='normal ls')


#ax.legend(['Points', 'SVD Plane', 'LS Plane'])
plt.show()