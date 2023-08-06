import matplotlib.pyplot as plt
plt.style.use('Solarize_Light2')
plt.rc('font', size=24)
plt.rc('axes', labelsize=32)

codesl = [3, 5, 8, 12]
cnners = [0.0416, 0.0248, 0.0176, 0.0092]
poders = [0.06455998967702727, 0.029626014656090327,
          0.017976456724285245, 0.008664898974187176]

fig = plt.figure(figsize=[9, 6])
plt.semilogy(codesl, poders, 'X', markersize=18, label='POD')
plt.semilogy(codesl, cnners, 'X', markersize=18, label='CNN')
plt.xticks(codesl)
plt.xlabel('Dimension $r$')
plt.title('Averaged Projection Error $\\| v_i - \\tilde v(\\rho_i)\\|_M^2$')
plt.legend()
fig.tight_layout()
plt.savefig('plot-one.png', transparent=True)
