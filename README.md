# Fit Plane In 3D
This short repo shows by example 3 different methods to fit a plane to 3D points. In general, the best way to fit a plane to 3D points is to first remove the centroid from the point coordinates and then either use the eigenvalues and eigenvectors of the points (method 1) or the singular value decomposition (SVD) of the points (method 2). Both methods yield similar results.


## Results
Because we create the 3D points randomly, every run of the code will be slightly different. Here are a sample set of results:

---- Using Eigen ----- 
normal vector: [-0.2312203   0.32084969  0.918473  ]
std of residuals: 0.11586616533827221

---- Using SVD ----- 
normal vector: [-0.2312203   0.32084969  0.918473  ]
std of residuals: 0.11586616533827221

---- Using Least Squares Along Z axis ----- 
normal vector: [-0.19844922  0.28130267  0.93887524]
std of residuals: 0.12467737196103701

----------------------------------
angular difference between normal vectors calculated from SVD and least squares is 3.167 degrees

## Plots
Now, let's plot everything:
* Original 3D points are plotted in green
* Best fit plane obtained from either SVD or Eigen approaches is plotted in blue
* Plane fitted by Least Squares method with Z-axis constraint is plotted in red
* Normal to best fit plane is plotted as a blue line
* Normal to least squares fit plane is plotted as a red line

You can see that there is a clear distinction between the two planes, proving that the least squares adjustment plane fitting with Z-axis constraint is not the best solution and does not quite achieve similar results to SVD or Eigen approaches. In this example, the angular difference between the normal to SVD plane and the normal to least squares plane is about 3.16 degrees.

![3d_plot](./img/3d_plot.png)
