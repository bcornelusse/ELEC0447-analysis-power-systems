import numpy as np


# Generate a set of abc phasors 

V_rms = 400 # V
Va = V_rms * complex(1, 0)  # magnitude V_rms, phase 0
a = np.exp(1j*2*np.pi/3)
Vb = Va * a**2
Vc = Va * a


# Plot Va, Vb, Vc in the complex plane
import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
plt.quiver(0, 0, Va.real, Va.imag, angles='xy', scale_units='xy', scale=1, color='r', label='Va')
plt.quiver(0, 0, Vb.real, Vb.imag, angles='xy', scale_units='xy', scale=1, color='g', label='Vb')
plt.quiver(0, 0, Vc.real, Vc.imag, angles='xy', scale_units='xy', scale=1, color='b', label='Vc')

plt.xlim(-V_rms*1.2, V_rms*1.2)
plt.ylim(-V_rms*1.2, V_rms*1.2)
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.grid(True)
plt.legend()
plt.title('Three-phase Phasors in Complex Plane')
plt.axis('equal')
plt.show()