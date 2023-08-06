import dolfin
import matplotlib.pyplot as plt

sqrmsh = dolfin.UnitSquareMesh(nx=10, ny=4)

V = dolfin.VectorFunctionSpace(sqrmsh, 'CG', 2)

exprfun = dolfin.Expression(('-2.1+x[0]+x[1]', 'x[0]*x[1]'), degree=2)
tfun = dolfin.interpolate(exprfun, V)
(xfun, yfun) = tfun.split(deepcopy=True)

# xfv = tfun.sub(0).vector().get_local()
xfv = xfun.vector().get_local()
print(xfv)
print(f'xmin={xfv.min()} -- xmax={xfv.max()}')

yfv = yfun.vector().get_local()
print(f'ymin={yfv.min()} -- ymax={yfv.max()}')

plt.figure(1)
dolfin.plot(tfun.sub(0))
plt.figure(2)
dolfin.plot(tfun.sub(1))

plt.show()
