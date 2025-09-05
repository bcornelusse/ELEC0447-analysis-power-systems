import numpy as np
import matplotlib.pyplot as plt
import math

# Activer le rendu LaTeX
plt.rcParams['text.usetex'] = True

# Définir la police pour les textes LaTeX
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino']
plt.rcParams['font.sans-serif'] = ['Helvetica']

def solve_transcendental(a, b, c, initial_guess, tolerance=1e-4, max_iterations=100):
    """
    Solves the transcendental equation a*x + b*cos(x) = c for x using
    the Newton-Raphson method.

    Args:
        a (float): The coefficient of x.
        b (float): The coefficient of cos(x).
        c (float): The constant on the right side of the equation.
        initial_guess (float): An initial guess for the solution.
        tolerance (float): The desired precision for the solution.
        max_iterations (int): The maximum number of iterations to perform.

    Returns:
        float: The approximate solution for x.
        None: If the method fails to converge within the max_iterations.
    """
    x = initial_guess

    for i in range(max_iterations):
        # Define the function f(x) and its derivative f'(x)
        f_x = a * x + b * math.cos(x) - c
        print(f"current guess  {x},  value={f_x}")
        f_prime_x = a - b * math.sin(x)

        # Check for division by zero, which indicates a flat slope.
        if abs(f_prime_x) < 1e-9:
            print("Warning: Derivative is close to zero. The method may not converge.")
            return None

        # Calculate the next approximation using the Newton-Raphson formula
        x_next = x - f_x / f_prime_x

        # Check if the change in x is within the desired tolerance
        if abs(x_next - x) < tolerance:
            return x_next

        # Update x for the next iteration
        x = x_next
 

    # If the loop finishes, the method did not converge
    print("Error: The Newton-Raphson method did not converge within the maximum number of iterations.")
    return None

# --- Paramètres du système ---
# Les valeurs sont normalisées (en pu - per-unit)
Pm = 0.8  # Puissance mécanique d'entrée (constante)
Pmax1 = 1.6  # Puissance électrique max pré-défaut
Pmax2 = 0.5  # Puissance électrique max pendant le défaut
Pmax3 = 1.3  # Puissance électrique max post-défaut

# --- Calcul des angles importants ---
# Angle de fonctionnement initial (stable)
delta0 = np.arcsin(Pm / Pmax1)
# Nouvel angle de fonctionnement stable post-défaut
delta_f = np.arcsin(Pm / Pmax3)
# Angle de swing maximal (le rotor ne revient pas en arrière)
delta_max = np.pi - delta_f

# Angle de dégagement critique (où A_acc = A_dec)
# Formule dérivée de la condition d'égalité des aires
numerator = -Pm * (delta_max - delta0) - (Pmax3 * np.cos(delta_max)) + (Pmax2 * np.cos(delta0))
denominator = Pmax2 - Pmax3
delta_c_crit = np.arccos(numerator / denominator)

# Clear the fault before the critical angle
lam = 0.6 # in [0,1]
delta_cl = lam * delta0 + (1-lam) * delta_c_crit

# Computing delta_stop
# From the formulas we get an equation a*x+b*cos(x) = c with 
a = Pm
b = Pmax3
#c = np.cos(delta_cl) * (Pmax3-Pmax2) + (Pm+Pmax2) * np.cos(delta0)
c = np.cos(delta_cl) * (Pmax3-Pmax2) + Pm * delta0 + Pmax2 * np.cos(delta0)
delta_stop = solve_transcendental(a, b,c, initial_guess=0.5*(delta_cl+delta_max))

print(f"delta stop = {delta_stop}")

# --- Génération des courbes ---
# Plage d'angles pour le tracé
delta = np.linspace(0, np.pi, 500)

# Courbes de puissance électrique pour les trois états du système
Pe1 = Pmax1 * np.sin(delta)  # Pré-défaut
Pe2 = Pmax2 * np.sin(delta)  # Pendant le défaut
Pe3 = Pmax3 * np.sin(delta)  # Post-défaut

# Ligne de puissance mécanique
Pm_line = np.full_like(delta, Pm)

# --- Tracé du graphe ---
fig = plt.figure(figsize=(10, 6))

# Tracé des courbes de puissance
plt.plot(delta, Pe1, 'k-', label='Pre-fault')
plt.plot(delta, Pe2, 'b-', label='During-fault')
plt.plot(delta, Pe3, 'r--', label='Post-fault')
plt.plot(delta, Pm_line, 'k--', label='$P_m$')

# --- Mise en évidence des aires ---
# Aire d'accélération (A_acc)
delta_acc = np.linspace(delta0, delta_cl, 500)
Pe2_acc = Pmax2 * np.sin(delta_acc)
plt.fill_between(delta_acc, Pm, Pe2_acc, color='blue', alpha=0.3, label='Area A (accelaration)')

# Aire de décélération (A_dec)
delta_dec = np.linspace(delta_cl, delta_stop, 500)
Pe3_dec = Pmax3 * np.sin(delta_dec)
plt.fill_between(delta_dec, Pm, Pe3_dec, where=(Pe3_dec > Pm), color='red', alpha=0.3, label='Area B (decelaration)')

# --- MODIFICATION CLÉ POUR L'AXE DES X ---
plt.xticks([0, np.pi/2, np.pi],
           [r'$0$', r'$\pi/2$', r'$\pi$'])


# --- Ajout de marqueurs et de texte ---
# Angles clés
plt.vlines([delta0, delta_cl, delta_stop, delta_f], 0, 1.8, linestyles=':', color='gray')
plt.text(delta0, -0.1, r'$\delta_0$', ha='center', color="blue")
plt.text(delta_cl, -0.1, r'$\delta_{cl}$', ha='center', color="green")
plt.text(delta_stop, -0.1, r'$\delta_{m}$', ha='center', color="red")
plt.text(delta_f, -0.1, r'$\delta_f$', ha='center')

# Titres et étiquettes
#plt.title('Critical Clearing Angle illustration', fontsize=16)
plt.xlabel(r'$\delta$ [rad]')
plt.ylabel(r'$P_e$ [pu]')
plt.grid(True)
plt.legend()
plt.ylim(0, 1.8)
plt.xlim(0, np.pi)
plt.axhline(0, color='black', linewidth=0.5)

#plt.show()

plt.grid(False)

fig.set_size_inches(6*2.5/2.54, 4*2.5/2.54)  # Set figure size to 6cm x 4cm
plt.tight_layout()
plt.savefig("Lectures/transient/images/EAC.pdf")
#plt.show()
#plt.close(fig)


