import numpy as np
import matplotlib.pyplot as plt

# Activer le rendu LaTeX
plt.rcParams['text.usetex'] = True

# Définir la police pour les textes LaTeX
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino']
plt.rcParams['font.sans-serif'] = ['Helvetica']

# --- Paramètres du système ---
# Les valeurs sont normalisées (en pu - per-unit)
Pm = 0.8  # Puissance mécanique d'entrée (constante)
Pmax1 = 1.6  # Puissance électrique max pré-défaut
Pmax2 = 0.45  # Puissance électrique max pendant le défaut
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
delta_acc = np.linspace(delta0, delta_c_crit, 500)
Pe2_acc = Pmax2 * np.sin(delta_acc)
plt.fill_between(delta_acc, Pm, Pe2_acc, color='blue', alpha=0.3, label='Area A (accelaration)')

# Aire de décélération (A_dec)
delta_dec = np.linspace(delta_c_crit, delta_max, 500)
Pe3_dec = Pmax3 * np.sin(delta_dec)
plt.fill_between(delta_dec, Pm, Pe3_dec, where=(Pe3_dec > Pm), color='red', alpha=0.3, label='Area B (decelaration)')

# --- MODIFICATION CLÉ POUR L'AXE DES X ---
plt.xticks([0, np.pi/2, np.pi],
           [r'$0$', r'$\pi/2$', r'$\pi$'])


# --- Ajout de marqueurs et de texte ---
# Angles clés
plt.vlines([delta0, delta_c_crit, delta_max, delta_f], 0, 1.8, linestyles=':', color='gray')
plt.text(delta0, -0.1, r'$\delta_0$', ha='center', color="blue")
plt.text(delta_c_crit, -0.1, r'$\delta_{cct}$', ha='center', color="green")
plt.text(delta_max, -0.1, r'$\delta_{max}$', ha='center', color="red")
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
plt.savefig("Lectures/transient/images/CCT_max.pdf")
#plt.show()
#plt.close(fig)