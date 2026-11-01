#!/usr/bin/env python3
"""Finite diagnostic checks for low-rank mixed-state symmetry learning.

This is not an implementation or a numerical proof of the copy algorithm.
The checks compare independently constructed finite matrices and include
negative controls for two changes that invalidate the claimed reduction.
Run from any directory; results default to the adjacent results.json.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sys
import time
import traceback

import numpy as np
import scipy
from scipy import linalg


SEED = 20261101
TOL = 2e-10


def require(condition: bool, message: str) -> None:
    if not bool(condition):
        raise AssertionError(message)


def ket(d: int, index: int) -> np.ndarray:
    ans = np.zeros(d, dtype=complex)
    ans[index] = 1
    return ans


def pure_density(vector: np.ndarray) -> np.ndarray:
    return np.outer(vector, vector.conj())


def tensor(vectors: list[np.ndarray]) -> np.ndarray:
    ans = np.ones(1, dtype=complex)
    for vector in vectors:
        ans = np.kron(ans, vector)
    return ans


def trace_distance(a: np.ndarray, b: np.ndarray) -> float:
    diff = a - b
    diff = (diff + diff.conj().T) / 2
    return float(np.abs(linalg.eigvalsh(diff)).sum() / 2)


def random_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = phases / np.abs(phases)
    return q * phases.conj()[None, :]


def random_density(d: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    ans = z @ z.conj().T
    return ans / np.trace(ans)


def permutation_sign(perm: tuple[int, ...]) -> int:
    inversions = sum(perm[i] > perm[j] for i in range(len(perm))
                     for j in range(i + 1, len(perm)))
    return -1 if inversions % 2 else 1


def permutation_matrix(d: int, perm: tuple[int, ...]) -> np.ndarray:
    """Explicit permutation on tensor factors, independent of growth LCU."""
    n = len(perm)
    size = d**n
    out = np.zeros((size, size), dtype=complex)
    for column, digits in enumerate(itertools.product(range(d), repeat=n)):
        image = tuple(digits[p] for p in perm)
        row = int(np.ravel_multi_index(image, (d,) * n))
        out[row, column] = 1
    return out


def swap_matrix(d: int, n: int, i: int, j: int) -> np.ndarray:
    perm = list(range(n))
    perm[i], perm[j] = perm[j], perm[i]
    return permutation_matrix(d, tuple(perm))


def antisymmetric_projector(d: int, n: int) -> np.ndarray:
    out = np.zeros((d**n, d**n), dtype=complex)
    for perm in itertools.permutations(range(n)):
        out += permutation_sign(perm) * permutation_matrix(d, perm)
    return out / math.factorial(n)


def wedge(columns: np.ndarray) -> np.ndarray:
    """Explicit normalized alternating tensor of orthonormal columns."""
    d, rank = columns.shape
    if rank == 0:
        return np.ones(1, dtype=complex)
    out = np.zeros(d**rank, dtype=complex)
    for perm in itertools.permutations(range(rank)):
        out += permutation_sign(perm) * tensor(
            [columns[:, index] for index in perm])
    return out / math.sqrt(math.factorial(rank))


def exterior_basis(columns: np.ndarray, degree: int) -> np.ndarray:
    basis = [wedge(columns[:, subset])
             for subset in itertools.combinations(range(columns.shape[1]), degree)]
    return np.column_stack(basis)


def apply_tensor_power(unitary: np.ndarray, vector: np.ndarray,
                       copies: int) -> np.ndarray:
    """Apply local matrices by contractions, without allocating U**tensor n."""
    d = unitary.shape[0]
    out = vector.reshape((d,) * copies)
    for axis in range(copies):
        out = np.tensordot(unitary, out, axes=(1, axis))
        out = np.moveaxis(out, 0, axis)
    return out.reshape(-1)


def trace_last(rho: np.ndarray, last_dimension: int) -> np.ndarray:
    first = rho.shape[0] // last_dimension
    reshaped = rho.reshape(first, last_dimension, first, last_dimension)
    return np.einsum("aibi->ab", reshaped)


def group_elements(moduli: tuple[int, ...]) -> list[tuple[int, ...]]:
    return list(itertools.product(*(range(n) for n in moduli)))


def add_group(x: tuple[int, ...], y: tuple[int, ...],
              moduli: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % n for a, b, n in zip(x, y, moduli))


def subtract_group(x: tuple[int, ...], y: tuple[int, ...],
                   moduli: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a - b) % n for a, b, n in zip(x, y, moduli))


def character(g: tuple[int, ...], label: tuple[int, ...],
              moduli: tuple[int, ...]) -> complex:
    return np.exp(2j * np.pi * sum(a * b / n
                  for a, b, n in zip(g, label, moduli)))


def generated_subgroup(generators: list[tuple[int, ...]],
                       moduli: tuple[int, ...]) -> frozenset[tuple[int, ...]]:
    zero = (0,) * len(moduli)
    found = {zero}
    queue = [zero]
    while queue:
        current = queue.pop()
        for generator in generators:
            candidate = add_group(current, generator, moduli)
            if candidate not in found:
                found.add(candidate)
                queue.append(candidate)
    return frozenset(found)


def coarse_bands(rho: np.ndarray, width: float, offset: float
                 ) -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray]]:
    """Finite exact-eigensolver reference object, not the copy-only sampler."""
    values, vectors = linalg.eigh(rho)
    groups: dict[int, list[int]] = {}
    for i, value in enumerate(values):
        if value >= offset:
            band = int(math.floor((float(value) - offset) / width))
            groups.setdefault(band, []).append(i)
    rounded = np.zeros_like(rho)
    projectors, bases = [], []
    for band, indices in sorted(groups.items()):
        columns = vectors[:, indices]
        projector = columns @ columns.conj().T
        midpoint = offset + (band + 0.5) * width
        rounded += midpoint * projector
        projectors.append(projector)
        bases.append(columns)
    require(float(np.trace(rounded).real) > 0, "All spectral bands discarded")
    return rounded / np.trace(rounded), projectors, bases


def check_coarse_band_subgroups() -> dict:
    rng = np.random.default_rng(SEED + 1)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    z = np.diag([1, -1]).astype(complex)
    eye2 = np.eye(2, dtype=complex)
    cases = []

    cases.append(("nonflat_full_support", (2,), np.diag([0.65, 0.35]),
                  [eye2, x], 2, 0.2))

    v0 = (ket(4, 0) + ket(4, 2)) / math.sqrt(2)
    v1 = (ket(4, 1) + 1j * ket(4, 3)) / math.sqrt(2)
    rho = (0.5 + 1e-11) * pure_density(v0) + (0.5 - 1e-11) * pure_density(v1)
    rep = [np.diag(np.exp(2j * np.pi * np.arange(4) * g / 4))
           for g in range(4)]
    cases.append(("almost_degenerate_nontrivial_subgroup", (4,), rho, rep, 2, 0.4))

    small = 1e-12
    plus = (ket(2, 0) + ket(2, 1)) / math.sqrt(2)
    rho = np.kron(np.kron(np.diag([0.6, 0.4]), pure_density(plus)),
                  np.diag([1 - small, small]))
    rep = [np.kron(np.kron(np.linalg.matrix_power(z, a),
                          np.linalg.matrix_power(z, b)), eye2)
           for a, b in group_elements((2, 2))]
    cases.append(("discarded_tiny_eigenvalues", (2, 2), rho, rep, 4, 0.4))

    reports = []
    for name, moduli, rho, rep, rank_bound, epsilon in cases:
        # A common random basis change prevents these checks from relying on
        # computational-basis diagonalization of the group or the state.
        change = random_unitary(rho.shape[0], rng)
        rho = change @ rho @ change.conj().T
        rep = [change @ u @ change.conj().T for u in rep]
        elements = group_elements(moduli)
        lookup = dict(zip(elements, rep))
        representation_residual = max(
            float(np.linalg.norm(lookup[g] @ lookup[h] -
                                 lookup[add_group(g, h, moduli)]))
            for g in elements for h in elements)
        require(representation_residual < TOL, "Not a finite-group representation")
        distances = [trace_distance(rho, u @ rho @ u.conj().T) for u in rep]
        true_h = {g for g, distance in zip(elements, distances) if distance < TOL}
        outside = [distance for g, distance in zip(elements, distances) if g not in true_h]
        require(min(outside) >= epsilon - TOL, "Finite case violates promised gap")
        width = epsilon / (100 * rank_bound)
        # Use midpoint shifts. Putting an almost-degenerate eigenspace
        # exactly across a boundary is ill-conditioned for a double-precision
        # eigensolver; the physical algorithm separately budgets bad shifts.
        offsets = width * (1 + (np.arange(37) + 0.5) / 37)
        max_rounding = 0.0
        min_band_count = rank_bound
        max_band_count = 0
        min_retained_rank = rank_bound
        minimum_boundary_margin = float("inf")
        values = linalg.eigvalsh(rho)
        required_margin = width / (1000 * rank_bound)
        for offset in offsets:
            for value in values:
                if value < offset:
                    margin = float(offset - value)
                else:
                    position = float((value - offset) / width)
                    margin = width * abs(position - round(position))
                minimum_boundary_margin = min(minimum_boundary_margin, margin)
                require(margin >= required_margin,
                        "Reference eigensolver case is too close to a band boundary")
            sigma, projectors, bases = coarse_bands(rho, width, float(offset))
            distance = trace_distance(rho, sigma)
            max_rounding = max(max_rounding, distance)
            require(distance <= epsilon / 40 + TOL, "Rounding bound exceeded")
            rounded_h = {g for g, u in zip(elements, rep)
                         if trace_distance(sigma, u @ sigma @ u.conj().T) < TOL}
            projector_h = {g for g, u in zip(elements, rep)
                           if max(np.linalg.norm(p - u @ p @ u.conj().T)
                                  for p in projectors) < 10 * TOL}
            require(rounded_h == true_h,
                    f"Rounding changed the promised subgroup in {name}, offset={offset}: "
                    f"true={sorted(true_h)}, rounded={sorted(rounded_h)}, "
                    f"distances={[trace_distance(sigma, u @ sigma @ u.conj().T) for u in rep]}")
            require(projector_h == true_h, "Band stabilizer disagrees with subgroup")
            min_band_count = min(min_band_count, len(projectors))
            max_band_count = max(max_band_count, len(projectors))
            min_retained_rank = min(min_retained_rank, sum(b.shape[1] for b in bases))
        reports.append({
            "case": name, "dimension": rho.shape[0], "rank_bound": rank_bound,
            "group_moduli": list(moduli), "exact_subgroup": sorted(map(list, true_h)),
            "promised_epsilon": epsilon, "minimum_outside_distance": min(outside),
            "offsets_checked": len(offsets), "maximum_rounding_distance": max_rounding,
            "rounding_bound": epsilon / 40,
            "retained_band_count_range": [min_band_count, max_band_count],
            "minimum_retained_rank": min_retained_rank,
            "minimum_boundary_margin": minimum_boundary_margin,
            "required_good_shift_margin": required_margin,
            "representation_residual": representation_residual,
        })
    return {"cases": reports,
            "scope": "Enumerated finite actions and 37 offsets per case; no spectral-filter circuit simulated."}


def check_wedge_geometry() -> dict:
    rng = np.random.default_rng(SEED + 2)
    maximum_overlap_residual = 0.0
    maximum_inequality_violation = 0.0
    minimum_gap_over_distance_squared = float("inf")
    cases = 0
    for d, ranks in [(5, [2, 1, 1]), (6, [2, 1, 2])]:
        basis = random_unitary(d, rng)
        bases = []
        start = 0
        for rank in ranks:
            bases.append(basis[:, start:start + rank])
            start += rank
        weights = np.array([0.31, 0.18, 0.07])
        weights /= np.dot(weights, ranks)
        sigma = sum(a * b @ b.conj().T for a, b in zip(weights, bases))
        state = tensor([wedge(b) for b in bases])
        require(abs(np.vdot(state, state) - 1) < TOL, "Tensor wedge is not normalized")
        total_rank = sum(ranks)
        for strength in [0.0, 0.015, 0.08, 0.3, 0.9, 2.0]:
            raw = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
            generator = (raw + raw.conj().T) / 2
            generator /= np.linalg.norm(generator, 2)
            unitary = linalg.expm(1j * strength * generator)
            distance = trace_distance(sigma, unitary @ sigma @ unitary.conj().T)
            direct = float(abs(np.vdot(state,
                           apply_tensor_power(unitary, state, total_rank))) ** 2)
            determinant = float(abs(np.prod([np.linalg.det(b.conj().T @ unitary @ b)
                                            for b in bases])) ** 2)
            sum_sines = 0.0
            weighted_sines = 0.0
            product_cosines = 1.0
            for weight, b in zip(weights, bases):
                singular_values = np.clip(linalg.svdvals(b.conj().T @ unitary @ b), 0, 1)
                sines = 1 - singular_values**2
                sum_sines += float(sines.sum())
                weighted_sines += weight * float(sines.sum())
                product_cosines *= float(np.prod(singular_values**2))
            residual = max(abs(direct - determinant), abs(direct - product_cosines))
            maximum_overlap_residual = max(maximum_overlap_residual, residual)
            violations = [distance**2 - weighted_sines,
                          weighted_sines - sum_sines,
                          direct - math.exp(-sum_sines),
                          direct - math.exp(-distance**2)]
            maximum_inequality_violation = max(maximum_inequality_violation, *violations)
            require(residual < 10 * TOL, "Explicit tensor disagrees with wedge determinant")
            require(max(violations) < 10 * TOL, "Principal-angle gap inequality violated")
            if distance > 1e-5:
                minimum_gap_over_distance_squared = min(
                    minimum_gap_over_distance_squared, (1 - direct) / distance**2)
            cases += 1
    return {"cases": cases, "largest_explicit_tensor_dimension": 6**5,
            "maximum_overlap_identity_residual": maximum_overlap_residual,
            "maximum_gap_inequality_violation": maximum_inequality_violation,
            "minimum_observed_gap_over_trace_distance_squared": minimum_gap_over_distance_squared,
            "scope": "Explicit tensor contractions versus SVD/determinant identities; finite floating-point checks."}


def check_growth_probability_and_sector() -> dict:
    rng = np.random.default_rng(SEED + 3)
    d, rank = 4, 3
    support = random_unitary(d, rng)[:, :rank]
    projector = support @ support.conj().T
    spectrum = np.array([0.55, 0.30, 0.15])
    tau = support @ np.diag(spectrum) @ support.conj().T
    floor = float(spectrum.min())
    reports = []
    for degree in range(1, rank + 1):
        exterior = exterior_basis(support, degree)
        omega = exterior @ random_density(exterior.shape[1], rng) @ exterior.conj().T
        full = antisymmetric_projector(d, degree + 1)
        previous = antisymmetric_projector(d, degree)
        incoming = np.kron(omega, tau)
        success = float(np.trace(full @ incoming).real)
        exact_partial_trace_identity = float(np.trace(full @ np.kron(omega, projector)).real)
        identity_target = (rank - degree) / (degree + 1)
        require(abs(exact_partial_trace_identity - identity_target) < TOL,
                "Antisymmetric partial-trace identity failed")
        lower_bound = floor * identity_target
        require(success >= lower_bound - TOL, "Growth floor bound failed")
        reject = np.eye(d**(degree + 1)) - full
        failure = reject @ incoming @ reject
        failure_probability = float(np.trace(failure).real)
        retained = trace_last(failure, d) / failure_probability
        support_exterior_projector = exterior @ exterior.conj().T
        antisymmetry_leakage = float(np.trace((np.eye(d**degree) - previous) @ retained).real)
        support_leakage = float(np.trace((np.eye(d**degree) - support_exterior_projector) @ retained).real)
        require(abs(antisymmetry_leakage) < TOL, "Failure lost retained antisymmetry")
        require(abs(support_leakage) < TOL, "Failure left the support exterior power")
        if degree == rank:
            require(abs(success) < TOL, "Growth continued beyond true support rank")
            target = pure_density(wedge(support))
            require(trace_distance(retained, target) < TOL,
                    "Correct rank stop did not leave unique top wedge")
        reports.append({"degree": degree, "success_probability": success,
                        "proven_floor_bound": lower_bound,
                        "partial_trace_identity_residual": abs(exact_partial_trace_identity - identity_target),
                        "retained_antisymmetry_leakage": antisymmetry_leakage,
                        "retained_support_leakage": support_leakage})
    return {"ambient_dimension": d, "support_rank": rank, "spectrum": spectrum.tolist(),
            "cases": reports,
            "scope": "Arbitrary random mixed states on exterior sectors, including the true-rank stopping case."}


def check_physical_growth_instrument() -> dict:
    """Test the actual coherent LCU failure correction and two invalid variants."""
    d, degree = 3, 2
    ancilla_dimension = degree + 1
    active_dimension = d**(degree + 1)
    preparation = np.exp(2j * np.pi * np.outer(np.arange(ancilla_dimension),
                                             np.arange(ancilla_dimension)) /
                         ancilla_dimension) / math.sqrt(ancilla_dimension)
    selects = [np.eye(active_dimension, dtype=complex)] + [
        -swap_matrix(d, degree + 1, i, degree) for i in range(degree)]
    state = np.kron(wedge(np.eye(d)[:, :degree]), ket(d, degree))
    prepared = preparation[:, 0, None] * state[None, :]
    selected = np.stack([s @ row for s, row in zip(selects, prepared)])
    after_unprepare = preparation.conj().T @ selected
    full = antisymmetric_projector(d, degree + 1)
    success_vector = after_unprepare[0]
    success_residual = float(np.linalg.norm(success_vector - full @ state))
    require(success_residual < TOL, "LCU success branch is not full antisymmetry")

    failed = after_unprepare.copy()
    failed[0] = 0
    failure_probability = float(np.vdot(failed, failed).real)

    def correction(branch: np.ndarray) -> np.ndarray:
        restored = preparation @ branch
        return np.stack([s @ row for s, row in zip(selects, restored)])

    corrected = correction(failed)
    target_failure = (np.eye(active_dimension) - full) @ state
    target_joint = preparation[:, 0, None] * target_failure[None, :]
    correction_residual = float(np.linalg.norm(corrected - target_joint))
    require(correction_residual < TOL, "Coherent failure uncomputation failed")
    # Applying W-dagger after the source's SELECT.W failure correction
    # is the equivalent second application of B = W-dagger.SELECT.W.
    cleaned = preparation.conj().T @ corrected
    clean_target = np.zeros_like(cleaned)
    clean_target[0] = target_failure
    clean_ancilla_residual = float(np.linalg.norm(cleaned - clean_target))
    require(clean_ancilla_residual < TOL, "Double-B failure cleanup did not reset ancilla")

    def active_density(branch: np.ndarray) -> np.ndarray:
        return sum(pure_density(row) for row in branch) / failure_probability

    corrected_active = active_density(corrected)
    naive_active = active_density(failed)
    # Incorrectly measuring each nonzero label dephases the failure subspace
    # before correction; sum its individual corrected branches explicitly.
    dephased_active = np.zeros_like(corrected_active)
    for label in range(1, ancilla_dimension):
        measured_branch = np.zeros_like(failed)
        measured_branch[label] = failed[label]
        dephased_active += active_density(correction(measured_branch))

    previous = antisymmetric_projector(d, degree)
    retained_identity = np.eye(d**degree)

    def leakage(active: np.ndarray) -> float:
        return float(np.trace((retained_identity - previous) @ trace_last(active, d)).real)

    corrected_leakage = leakage(corrected_active)
    missing_uncompute_leakage = leakage(naive_active)
    fine_measurement_leakage = leakage(dephased_active)
    require(abs(corrected_leakage) < TOL, "Correct physical instrument lost sector")
    require(missing_uncompute_leakage > 0.05,
            "Negative control failed to expose missing failure uncomputation")
    require(fine_measurement_leakage > 0.05,
            "Negative control failed to expose destructive ancilla refinement")
    expected_active = pure_density(target_failure) / failure_probability
    require(trace_distance(corrected_active, expected_active) < TOL,
            "Physical failure instrument differs from the required Lueders branch")
    return {"dimension": d, "retained_degree": degree,
            "success_probability": float(np.vdot(success_vector, success_vector).real),
            "failure_probability": failure_probability,
            "success_vector_residual": success_residual,
            "coherent_failure_correction_residual": correction_residual,
            "clean_ancilla_double_B_residual": clean_ancilla_residual,
            "corrected_retained_sector_leakage": corrected_leakage,
            "negative_control_omitted_uncompute_leakage": missing_uncompute_leakage,
            "negative_control_fine_ancilla_measurement_leakage": fine_measurement_leakage,
            "source": "Bene Watts et al., arXiv:2610.06737v1, Algorithm 1, especially steps 4 and 6.",
            "scope": "Full finite ancilla/active circuit; verifies the coarse binary measurement and failure correction are essential."}


def check_support_only_counterexample() -> dict:
    rho = np.diag([0.65, 0.35]).astype(complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    support_state = wedge(np.eye(2, dtype=complex))
    support_overlap = float(abs(np.vdot(support_state,
                            apply_tensor_power(x, support_state, 2))) ** 2)
    band_state = np.kron(ket(2, 0), ket(2, 1))
    band_overlap = float(abs(np.vdot(band_state,
                         apply_tensor_power(x, band_state, 2))) ** 2)
    distance = trace_distance(rho, x @ rho @ x)
    require(abs(distance - 0.30) < TOL, "Rank-two symmetry distance incorrect")
    require(abs(support_overlap - 1) < TOL, "Support wedge negative control is wrong")
    require(band_overlap < TOL, "Band wedges did not retain spectral distinction")
    flat = np.eye(2) / 2
    z = np.diag([1, -1])
    require(trace_distance(flat, z @ flat @ z) < TOL, "Flat state should be invariant")
    require(abs(np.trace(z @ flat)) < TOL, "Strong symmetry counterexample failed")
    return {"rank": 2, "conjugation_distance_under_X": distance,
            "whole_support_wedge_squared_overlap": support_overlap,
            "separate_band_wedges_squared_overlap": band_overlap,
            "flat_state_conjugation_distance_under_Z": 0.0,
            "flat_state_representation_trace_under_Z": 0.0,
            "scope": "Exact two-dimensional counterexamples to support-only and strong-symmetry substitutions."}


def check_fourier_difference_recovery() -> dict:
    moduli = (4,)
    elements = group_elements(moduli)
    d = 4
    v0 = (ket(d, 0) + ket(d, 2)) / math.sqrt(2)
    v1 = (ket(d, 1) + 1j * ket(d, 3)) / math.sqrt(2)
    state = np.kron(v0, v1)
    reps = [np.diag(np.exp(2j * np.pi * np.arange(d) * g[0] / 4)) for g in elements]
    actions = [apply_tensor_power(u, state, 2) for u in reps]
    f = np.array([np.vdot(state, acted) for acted in actions])
    p = np.array([float(np.linalg.norm(sum(character(g, label, moduli).conjugate() * acted
                  for g, acted in zip(elements, actions)) / len(elements)) ** 2)
                  for label in elements])
    require(abs(p.sum() - 1) < TOL, "Character projector probabilities do not sum to one")
    p = np.maximum(p, 0) / p.sum()
    lookup = {g: index for index, g in enumerate(elements)}
    q = np.zeros(len(elements))
    for i, first in enumerate(elements):
        for j, second in enumerate(elements):
            q[lookup[subtract_group(first, second, moduli)]] += p[i] * p[j]
    transformed = np.array([sum(prob * character(g, label, moduli)
                           for label, prob in zip(elements, q)) for g in elements])
    transform_residual = float(np.max(np.abs(transformed - np.abs(f)**2)))
    require(transform_residual < TOL, "Difference distribution has wrong Fourier transform")

    h = frozenset(g for g, value in zip(elements, f) if abs(abs(value) - 1) < TOL)
    annihilator = frozenset(label for label in elements
                           if all(abs(character(g, label, moduli) - 1) < TOL for g in h))
    q_outside = sum(prob for label, prob in zip(elements, q) if label not in annihilator)
    p_outside = sum(prob for label, prob in zip(elements, p) if label not in annihilator)
    require(q_outside < TOL, "Difference sampling left the annihilator")
    require(p_outside > 0.99, "Ordinary-sampling phase negative control is not discriminating")
    require(generated_subgroup([label for label, prob in zip(elements, q) if prob > TOL], moduli)
            == annihilator, "Difference support does not generate the correct annihilator")

    zero_group = frozenset({(0,)})
    law: dict[frozenset[tuple[int, ...]], float] = {zero_group: 1.0}
    exact_recovery_probabilities = []
    for _ in range(12):
        updated: dict[frozenset[tuple[int, ...]], float] = {}
        for subgroup, mass in law.items():
            for label, probability in zip(elements, q):
                if probability < 1e-15:
                    continue
                new_group = generated_subgroup(list(subgroup) + [label], moduli)
                updated[new_group] = updated.get(new_group, 0.0) + mass * probability
        law = updated
        exact_recovery_probabilities.append(float(law.get(annihilator, 0.0)))
    require(exact_recovery_probabilities[-1] > 0.999,
            "Finite Fourier experiment did not recover subgroup with high probability")
    # Every proper reachable subgroup must lose a nonzero amount of mass.
    gap = min(1 - abs(value)**2 for g, value in zip(elements, f) if g not in h)
    minimum_escape = min(sum(prob for label, prob in zip(elements, q) if label not in subgroup)
                         for subgroup in law if subgroup != annihilator)
    require(minimum_escape >= gap / 2 - TOL, "Subgroup-escape inequality failed")
    return {"group_moduli": list(moduli), "subgroup": sorted(map(list, h)),
            "annihilator": sorted(map(list, annihilator)),
            "ordinary_character_distribution": p.tolist(),
            "difference_character_distribution": q.tolist(),
            "fourier_transform_residual": transform_residual,
            "difference_mass_outside_annihilator": float(q_outside),
            "negative_control_ordinary_mass_outside_annihilator": float(p_outside),
            "minimum_proper_subgroup_escape_probability": float(minimum_escape),
            "squared_overlap_gap": float(gap),
            "exact_recovery_probability_after_1_to_12_samples": exact_recovery_probabilities,
            "scope": "Exact finite subgroup-state probability propagation, not Monte Carlo or an asymptotic proof."}


def choi_state(kraus: list[np.ndarray]) -> np.ndarray:
    d = kraus[0].shape[1]
    return sum(pure_density(k.reshape(-1)) for k in kraus) / d


def channel(kraus: list[np.ndarray], matrix: np.ndarray) -> np.ndarray:
    return sum(k @ matrix @ k.conj().T for k in kraus)


def check_choi_covariance_and_norm_caveat() -> dict:
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    eye = np.eye(2, dtype=complex)
    kraus = [math.sqrt(0.7) * eye, math.sqrt(0.3) * x]
    choi = choi_state(kraus)
    require(abs(np.trace(choi) - 1) < TOL, "Choi state is not normalized")
    require(np.count_nonzero(linalg.eigvalsh(choi) > TOL) == 2, "Choi rank is not Kraus rank two")
    output_trace = np.einsum("iaib->ab", choi.reshape(2, 2, 2, 2))
    require(np.linalg.norm(output_trace - eye / 2) < TOL, "Choi marginal is wrong")
    covariance_cases = []
    for g in range(4):
        unitary = np.diag([1, (1j)**g])
        rep = np.kron(unitary, unitary.conj())
        distance = trace_distance(choi, rep @ choi @ rep.conj().T)
        direct_residual = 0.0
        for i, j in itertools.product(range(2), repeat=2):
            matrix_unit = np.outer(ket(2, i), ket(2, j).conj())
            residual = channel(kraus, unitary @ matrix_unit @ unitary.conj().T) - (
                unitary @ channel(kraus, matrix_unit) @ unitary.conj().T)
            direct_residual = max(direct_residual, float(np.linalg.norm(residual)))
        require((distance < TOL) == (direct_residual < TOL),
                "Choi invariance and channel covariance disagree")
        require((distance < TOL) == (g % 2 == 0), "Wrong subgroup for noisy channel")
        if g % 2:
            require(abs(distance - 0.3) < TOL, "Unexpected Choi symmetry gap")
        covariance_cases.append({"group_element": g, "choi_trace_distance": distance,
                                 "direct_covariance_residual": direct_residual})

    norm_cases = []
    for d in [4, 8, 16, 32, 64]:
        v = np.ones(d)
        v[0] = -1
        conjugate = np.ones(d)
        conjugate[1] = -1
        # V and PVP are diagonal reflections. Their pure normalized Choi
        # overlap is the normalized inner product of these diagonal vectors.
        overlap = complex(np.vdot(v, conjugate) / d)
        choi_distance = math.sqrt(max(0.0, 1 - abs(overlap)**2))
        predicted = math.sqrt(8 / d - 16 / d**2)
        witness = (ket(d, 0) + ket(d, 2)) / math.sqrt(2)
        first_output, second_output = v * witness, conjugate * witness
        witnessed_channel_distance = math.sqrt(max(0.0, 1 - abs(np.vdot(first_output, second_output))**2))
        require(abs(choi_distance - predicted) < TOL, "Choi dimension-gap formula failed")
        require(abs(witnessed_channel_distance - 1) < TOL, "No constant channel-distance witness")
        norm_cases.append({"input_dimension": d, "kraus_rank": 1,
                           "choi_trace_distance": choi_distance,
                           "half_diamond_distance": witnessed_channel_distance,
                           "explanation": "An explicit pure input gives distance one; this saturates the universal channel-distance upper bound."})
    require(norm_cases[-1]["choi_trace_distance"] < norm_cases[0]["choi_trace_distance"],
            "Dimension caveat is not visible in the selected family")
    return {"noisy_channel_kraus_rank": 2, "covariance_group_modulus": 4,
            "covariance_subgroup": [0, 2], "covariance_cases": covariance_cases,
            "dimension_gap_counterexample": norm_cases,
            "scope": "Choi-trace covariance identity and a rank-one channel family separating Choi and diamond gaps."}


CHECKS = [
    ("coarse_band_subgroups", check_coarse_band_subgroups),
    ("tensor_wedge_geometry", check_wedge_geometry),
    ("growth_probability_and_sector", check_growth_probability_and_sector),
    ("physical_growth_instrument", check_physical_growth_instrument),
    ("support_only_counterexample", check_support_only_counterexample),
    ("fourier_difference_recovery", check_fourier_difference_recovery),
    ("choi_covariance_and_norm_caveat", check_choi_covariance_and_norm_caveat),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    results = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "seed": SEED,
        "base_numerical_tolerance": TOL,
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "platform": platform.system()},
        "claim_boundary": (
            "Finite diagnostics only. These checks do not prove general correctness, novelty, "
            "copy/gate complexity, controlled-DME accuracy, asymptotic rank stopping, "
            "or robustness beyond the stated exact-symmetry promise."
        ),
        "checks": [],
    }
    failed = False
    for name, check in CHECKS:
        check_started = time.perf_counter()
        record = {"name": name}
        try:
            record["metrics"] = check()
            record["status"] = "passed"
            print(f"PASS {name}", flush=True)
        except Exception as error:  # Preserve diagnostic output even after a failure.
            failed = True
            record["status"] = "failed"
            record["error"] = f"{type(error).__name__}: {error}"
            record["traceback"] = traceback.format_exc()
            print(f"FAIL {name}: {error}", file=sys.stderr, flush=True)
        record["wall_seconds"] = time.perf_counter() - check_started
        results["checks"].append(record)
    results["status"] = "failed" if failed else "passed"
    results["wall_seconds"] = time.perf_counter() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(f"Saved {args.output}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
