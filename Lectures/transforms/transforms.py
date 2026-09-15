"""
transforms.py - Core mathematical transformations used in power systems analysis.

Course: ELEC0447 - Analysis of Electric Power and Energy Systems
University of Liège

This module implements:
1. Symmetrical Components (Fortescue decomposition: direct, inverse, zero sequence)
2. Clarke Transformation (abc to alpha-beta-0 stationary reference frame)
3. Park Transformation (alpha-beta to d-q rotating reference frame and direct abc to dq0)
4. Kron Reduction (Network admittance matrix reduction)
5. Full-Cycle Discrete Fourier Transform (DFT phasor estimation for PMUs and digital relays)

Zero external dependencies required (supports pure Python and NumPy if available).
"""

import math
import cmath

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# ==============================================================================
# 1. Symmetrical Components (Fortescue Transformation)
# ==============================================================================

# Fortescue complex rotation operator: a = e^(j * 2*pi/3) = -0.5 + j * sqrt(3)/2
A_OP = cmath.exp(1j * 2.0 * math.pi / 3.0)


def fortescue_transform(v_a, v_b, v_c):
    """
    Decomposes 3-phase complex phasors into symmetrical components (0, 1, 2).
    
    Parameters
    ----------
    v_a, v_b, v_c : complex or float
        Phase phasors in a, b, c order.

    Returns
    -------
    v_0 : complex
        Zero sequence phasor (homopolar).
    v_1 : complex
        Positive (direct) sequence phasor.
    v_2 : complex
        Negative (inverse) sequence phasor.
    """
    if HAS_NUMPY and isinstance(v_a, np.ndarray):
        v_0 = (1.0 / 3.0) * (v_a + v_b + v_c)
        v_1 = (1.0 / 3.0) * (v_a + A_OP * v_b + (A_OP**2) * v_c)
        v_2 = (1.0 / 3.0) * (v_a + (A_OP**2) * v_b + A_OP * v_c)
        return v_0, v_1, v_2

    v_0 = (v_a + v_b + v_c) / 3.0
    v_1 = (v_a + A_OP * v_b + (A_OP**2) * v_c) / 3.0
    v_2 = (v_a + (A_OP**2) * v_b + A_OP * v_c) / 3.0
    return v_0, v_1, v_2


def inv_fortescue_transform(v_0, v_1, v_2):
    """
    Reconstructs 3-phase complex phasors from symmetrical components (0, 1, 2).
    
    Parameters
    ----------
    v_0 : complex
        Zero sequence component.
    v_1 : complex
        Positive (direct) sequence component.
    v_2 : complex
        Negative (inverse) sequence component.

    Returns
    -------
    v_a, v_b, v_c : complex
        Phase phasors in a, b, c order.
    """
    if HAS_NUMPY and isinstance(v_0, np.ndarray):
        v_a = v_0 + v_1 + v_2
        v_b = v_0 + (A_OP**2) * v_1 + A_OP * v_2
        v_c = v_0 + A_OP * v_1 + (A_OP**2) * v_2
        return v_a, v_b, v_c

    v_a = v_0 + v_1 + v_2
    v_b = v_0 + (A_OP**2) * v_1 + A_OP * v_2
    v_c = v_0 + A_OP * v_1 + (A_OP**2) * v_2
    return v_a, v_b, v_c


# ==============================================================================
# 2. Clarke Transformation (abc -> alpha, beta, 0)
# ==============================================================================

def clarke_transform(v_a, v_b, v_c, variant='amplitude'):
    """
    Converts 3-phase quantities (a, b, c) into the stationary orthogonal
    reference frame (alpha, beta, 0).
    
    The alpha-axis is aligned with phase a.
    The beta-axis leads alpha by 90 electrical degrees.

    Parameters
    ----------
    v_a, v_b, v_c : float or ndarray
        Instantaneous 3-phase quantities.
    variant : {'amplitude', 'power'}
        'amplitude' (default): Peak-preserving transformation (factor 2/3).
            v_alpha peak equals phase voltage peak in balanced condition.
        'power': Power-invariant transformation (orthogonal, factor sqrt(2/3)).

    Returns
    -------
    v_alpha, v_beta, v_0 : float or ndarray
    """
    sqrt3 = math.sqrt(3.0)
    if variant == 'amplitude':
        k = 2.0 / 3.0
        k0 = 1.0 / 3.0
    elif variant == 'power':
        k = math.sqrt(2.0 / 3.0)
        k0 = 1.0 / sqrt3
    else:
        raise ValueError(f"Unknown variant '{variant}'. Use 'amplitude' or 'power'.")

    v_alpha = k * (v_a - 0.5 * v_b - 0.5 * v_c)
    v_beta = k * (sqrt3 / 2.0 * (v_b - v_c))
    v_0 = k0 * (v_a + v_b + v_c)

    return v_alpha, v_beta, v_0


def inv_clarke_transform(v_alpha, v_beta, v_0=0.0, variant='amplitude'):
    """
    Converts stationary frame quantities (alpha, beta, 0) back to 3-phase (a, b, c).
    """
    sqrt3 = math.sqrt(3.0)
    if variant == 'amplitude':
        v_a = v_alpha + v_0
        v_b = -0.5 * v_alpha + (sqrt3 / 2.0) * v_beta + v_0
        v_c = -0.5 * v_alpha - (sqrt3 / 2.0) * v_beta + v_0
    elif variant == 'power':
        k = math.sqrt(2.0 / 3.0)
        k0 = 1.0 / sqrt3
        v_a = k * v_alpha + k0 * v_0
        v_b = k * (-0.5 * v_alpha + (sqrt3 / 2.0) * v_beta) + k0 * v_0
        v_c = k * (-0.5 * v_alpha - (sqrt3 / 2.0) * v_beta) + k0 * v_0
    else:
        raise ValueError(f"Unknown variant '{variant}'. Use 'amplitude' or 'power'.")

    return v_a, v_b, v_c


# ==============================================================================
# 3. Park Transformation (alpha, beta -> d, q) and Direct (abc -> dq0)
# ==============================================================================

def park_transform(v_alpha, v_beta, theta, alignment='cosine'):
    """
    Converts 2-phase stationary quantities (alpha, beta) into a rotating
    reference frame (d, q) with electrical angle theta.

    Parameters
    ----------
    v_alpha, v_beta : float or ndarray
        Stationary orthogonal components.
    theta : float or ndarray
        Angle of the d-axis with respect to alpha-axis [radians].
    alignment : {'cosine', 'sine'}
        'cosine' (default): d-axis aligned with alpha when theta = 0.
        'sine': d-axis aligned with beta when theta = 0.

    Returns
    -------
    v_d, v_q : float or ndarray
    """
    if HAS_NUMPY and isinstance(theta, np.ndarray):
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
    else:
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

    if alignment == 'cosine':
        v_d = v_alpha * cos_t + v_beta * sin_t
        v_q = -v_alpha * sin_t + v_beta * cos_t
    elif alignment == 'sine':
        v_d = v_alpha * sin_t - v_beta * cos_t
        v_q = v_alpha * cos_t + v_beta * sin_t
    else:
        raise ValueError(f"Unknown alignment '{alignment}'.")

    return v_d, v_q


def inv_park_transform(v_d, v_q, theta, alignment='cosine'):
    """
    Converts rotating frame quantities (d, q) back to stationary frame (alpha, beta).
    """
    if HAS_NUMPY and isinstance(theta, np.ndarray):
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
    else:
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

    if alignment == 'cosine':
        v_alpha = v_d * cos_t - v_q * sin_t
        v_beta = v_d * sin_t + v_q * cos_t
    elif alignment == 'sine':
        v_alpha = v_d * sin_t + v_q * cos_t
        v_beta = -v_d * cos_t + v_q * sin_t
    else:
        raise ValueError(f"Unknown alignment '{alignment}'.")

    return v_alpha, v_beta


def abc_to_dq0(v_a, v_b, v_c, theta, variant='amplitude', alignment='cosine'):
    """
    Direct transformation from 3-phase (a, b, c) to rotating frame (d, q, 0).
    """
    v_alpha, v_beta, v_0 = clarke_transform(v_a, v_b, v_c, variant=variant)
    v_d, v_q = park_transform(v_alpha, v_beta, theta, alignment=alignment)
    return v_d, v_q, v_0


def dq0_to_abc(v_d, v_q, v_0, theta, variant='amplitude', alignment='cosine'):
    """
    Direct transformation from rotating frame (d, q, 0) back to 3-phase (a, b, c).
    """
    v_alpha, v_beta = inv_park_transform(v_d, v_q, theta, alignment=alignment)
    return inv_clarke_transform(v_alpha, v_beta, v_0, variant=variant)


# ==============================================================================
# 4. Kron Reduction (Network Admittance Reduction)
# ==============================================================================

def _matrix_inverse(mat):
    """Helper for pure Python matrix inversion of 2D list."""
    n = len(mat)
    # Augment with identity
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(mat)]
    for i in range(n):
        # Pivot
        pivot = aug[i][i]
        if abs(pivot) < 1e-14:
            # find non-zero row
            for r in range(i + 1, n):
                if abs(aug[r][i]) > 1e-14:
                    aug[i], aug[r] = aug[r], aug[i]
                    pivot = aug[i][i]
                    break
        if abs(pivot) < 1e-14:
            raise ValueError("Matrix is singular and cannot be inverted for Kron reduction.")
        for j in range(2 * n):
            aug[i][j] /= pivot
        for r in range(n):
            if r != i:
                factor = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= factor * aug[i][j]
    return [[aug[i][j] for j in range(n, 2 * n)] for i in range(n)]


def kron_reduction(Y_bus, kept_buses, eliminated_buses):
    """
    Performs Kron reduction on a bus admittance matrix Y_bus to eliminate
    passive (zero-injection) nodes.

    Given nodal equations:
        [ I_k ]   [ Y_kk  Y_ke ] [ V_k ]
        [ 0   ] = [ Y_ek  Y_ee ] [ V_e ]

    The eliminated voltages satisfy:
        V_e = - Y_ee^(-1) * Y_ek * V_k

    Yielding the reduced admittance matrix:
        Y_kron = Y_kk - Y_ke * Y_ee^(-1) * Y_ek
    """
    if HAS_NUMPY:
        Y = np.asarray(Y_bus, dtype=complex)
        k = np.asarray(kept_buses, dtype=int)
        e = np.asarray(eliminated_buses, dtype=int)
        Y_kk = Y[np.ix_(k, k)]
        Y_ke = Y[np.ix_(k, e)]
        Y_ek = Y[np.ix_(e, k)]
        Y_ee = Y[np.ix_(e, e)]
        Y_ee_inv = np.linalg.inv(Y_ee)
        return Y_kk - Y_ke @ Y_ee_inv @ Y_ek

    # Pure Python implementation
    nk = len(kept_buses)
    ne = len(eliminated_buses)
    Y_kk = [[Y_bus[i][j] for j in kept_buses] for i in kept_buses]
    Y_ke = [[Y_bus[i][j] for j in eliminated_buses] for i in kept_buses]
    Y_ek = [[Y_bus[i][j] for j in kept_buses] for i in eliminated_buses]
    Y_ee = [[Y_bus[i][j] for j in eliminated_buses] for i in eliminated_buses]

    Y_ee_inv = _matrix_inverse(Y_ee)

    # Multiply Y_ke * Y_ee_inv * Y_ek
    # Step 1: temp = Y_ke @ Y_ee_inv (nk x ne)
    temp = [[sum(Y_ke[i][m] * Y_ee_inv[m][j] for m in range(ne)) for j in range(ne)] for i in range(nk)]
    # Step 2: Schur = temp @ Y_ek (nk x nk)
    schur = [[sum(temp[i][m] * Y_ek[m][j] for m in range(ne)) for j in range(nk)] for i in range(nk)]
    # Step 3: Y_kron = Y_kk - schur
    Y_kron = [[Y_kk[i][j] - schur[i][j] for j in range(nk)] for i in range(nk)]
    return Y_kron


# ==============================================================================
# 5. Discrete Fourier Transform (DFT Phasor Estimation)
# ==============================================================================

def dft_phasor_estimation(samples, sampling_rate, nominal_freq=50.0):
    """
    Computes the fundamental frequency complex phasor from time-domain sampled
    waveform using a Full-Cycle Discrete Fourier Transform (DFT) filter.

    Convention:
        X = (sqrt(2) / N) * sum_{k=0}^{N-1} x[k] * exp(-j * 2 * pi * k / N)
    where:
        - Magnitude |X| corresponds to the RMS value of the fundamental component.
        - Angle arg(X) corresponds to the phase angle relative to the start of the window.
    """
    samples_per_cycle = int(round(sampling_rate / nominal_freq))
    N = samples_per_cycle

    if len(samples) < N:
        raise ValueError(
            f"Need at least {N} samples for full-cycle DFT, got {len(samples)}."
        )

    # Pure Python & NumPy compatible
    window = samples[:N]
    acc = 0.0 + 0.0j
    for k in range(N):
        angle = -2.0 * math.pi * k / N
        acc += window[k] * cmath.exp(1j * angle)

    X_rms = (math.sqrt(2.0) / N) * acc
    return X_rms


# ==============================================================================
# Self-test / Verification
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing transforms.py (Course ELEC0447)")
    print("=" * 60)

    # 1. Fortescue Symmetrical Components test
    V_a = 230.0 + 0.0j
    V_b = 230.0 * cmath.exp(-1j * 2.0 * math.pi / 3.0)
    V_c = 230.0 * cmath.exp(1j * 2.0 * math.pi / 3.0)

    v0, v1, v2 = fortescue_transform(V_a, V_b, V_c)
    print(f"Balanced test: |V0|={abs(v0):.2e} V, |V1|={abs(v1):.2f} V, |V2|={abs(v2):.2e} V")
    assert abs(v0) < 1e-10 and abs(v2) < 1e-10
    assert abs(abs(v1) - 230.0) < 1e-10

    # Invert back
    ra, rb, rc = inv_fortescue_transform(v0, v1, v2)
    assert abs(ra - V_a) < 1e-10 and abs(rb - V_b) < 1e-10 and abs(rc - V_c) < 1e-10
    print("✓ Fortescue transform & inversion passed.")

    # 2. Clarke and Park test
    t_val = 0.005
    w_val = 2 * math.pi * 50
    va = 230.0 * math.sqrt(2) * math.sin(w_val * t_val)
    vb = 230.0 * math.sqrt(2) * math.sin(w_val * t_val - 2 * math.pi / 3)
    vc = 230.0 * math.sqrt(2) * math.sin(w_val * t_val + 2 * math.pi / 3)

    valpha, vbeta, v0 = clarke_transform(va, vb, vc, variant='amplitude')
    rec_va, rec_vb, rec_vc = inv_clarke_transform(valpha, vbeta, v0, variant='amplitude')
    assert abs(rec_va - va) < 1e-10 and abs(rec_vb - vb) < 1e-10 and abs(rec_vc - vc) < 1e-10
    print("✓ Clarke transform & inversion passed.")

    theta = w_val * t_val - math.pi / 2
    vd, vq = park_transform(valpha, vbeta, theta, alignment='cosine')
    expected_peak = 230.0 * math.sqrt(2)
    print(f"Park values at t={t_val}s: Vd={vd:.2f} V (expected {expected_peak:.2f} V), Vq={vq:.2e} V")
    assert abs(vd - expected_peak) < 1e-6 and abs(vq) < 1e-6
    print("✓ Park transform produces constant DC quantities.")

    # 3. Kron Reduction test
    Y3 = [
        [ 2 - 5j, -1 + 2j, -1 + 3j],
        [-1 + 2j,  3 - 7j, -2 + 5j],
        [-1 + 3j, -2 + 5j,  3 - 8j]
    ]
    Y_reduced = kron_reduction(Y3, kept_buses=[0, 1], eliminated_buses=[2])
    print(f"Kron reduced 2x2 matrix: Y[0][1]={Y_reduced[0][1]:.3f}, Y[1][0]={Y_reduced[1][0]:.3f}")
    assert abs(Y_reduced[0][1] - Y_reduced[1][0]) < 1e-10
    print("✓ Kron reduction passed.")

    # 4. DFT Phasor test
    fs = 4000.0  # 4 kHz sampling
    N_samples = int(fs * 0.02)
    sig = [230.0 * math.sqrt(2) * math.cos(2 * math.pi * 50 * (k / fs) + math.radians(30.0)) for k in range(N_samples)]
    X_p = dft_phasor_estimation(sig, fs, 50.0)
    print(f"DFT extracted: RMS={abs(X_p):.2f} V (expected 230.00 V), Phase={math.degrees(cmath.phase(X_p)):.2f}° (expected 30.00°)")
    assert abs(abs(X_p) - 230.0) < 1e-2
    assert abs(math.degrees(cmath.phase(X_p)) - 30.0) < 1e-2
    print("✓ DFT phasor estimation passed.")

    print("=" * 60)
    print("All transform tests passed successfully!")
    print("=" * 60)
