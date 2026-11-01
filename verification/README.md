# Finite scientific verification

These checks target specific failure modes in the low-rank symmetry-learning argument. They compare explicit finite matrices, tensor states and group distributions; they are not an implementation of the complete copy-only learning algorithm or a numerical proof of its asymptotic guarantees.

The current recorded run passes all seven diagnostic groups. The full metrics, fixed seed, dependency versions, execution time and SHA-256 of the executed script are in [results.json](results.json).

The separate [hosted mathematics check](hosted/README.md) compares every tracked Markdown expression with its actual commit-pinned GitHub rendering at wide and narrow viewports. Its read-only workflow retains a report and screenshots for visual inspection. These presentation checks and the scientific diagnostics answer different questions.

## Run

From the repository root:

```bash
python -m pip install -r verification/requirements.txt
python -B verification/checks.py
```

The script can also run from another directory. Its default output is `results.json` beside the script; `--output PATH` selects a different destination. It writes results even if a check fails, reports the failed assertion, and returns a nonzero exit status. The numerical environment used for the stored run is Python 3.12, NumPy 2.3.5 and SciPy 1.17.0. No quantum software development kit, network access or GPU is required.

Random bases and test states use fixed seed `20261101` with separate deterministic offsets for each diagnostic. The largest explicitly stored tensor state has dimension 7,776. Tensor powers of unitaries are applied by contractions, avoiding allocation of their full matrices. The recorded execution takes less than one second in the supplied environment; this is a statement about these small checks, not the learning algorithm's runtime.

## What is checked

| Diagnostic | Independent comparison and risk addressed | Recorded observation |
|---|---|---|
| Coarse-band subgroup preservation | Enumerate all actions of selected cyclic/product groups, compare the original state stabilizer with the rounded-state and band-projector stabilizers, and verify the trace-distance budget over 37 safe offsets per example. | All three stabilizers agree. Examples include nontrivial subgroups, an eigenvalue gap of approximately `2e-11`, and discarded eigenvalues of order `1e-12`. |
| Tensor-wedge geometry | Compare an explicit alternating tensor and local-unitary contraction with determinant and singular-value formulas; check the weighted principal-angle and trace-distance inequalities. | Maximum overlap-identity residual below `2.4e-15`; maximum positive inequality residual below `1.6e-15` in the recorded run. |
| Growth probabilities and retained sector | Use arbitrary mixed states on exterior-power sectors of a random three-dimensional support. Compare explicit permutation projectors with the partial-trace identity and spectral-floor success bound. | Failure preserves both the old antisymmetric sector and the support. Growth probability is zero at the true support rank, where the retained state is the unique top wedge. |
| Physical growth circuit | Implement the ancilla preparation, controlled negative SWAPs, coarse binary measurement and coherent failure correction; compare with an independently formed Lüders projector branch. | Corrected rejection preserves the sector. Omitting the correction produces leakage `0.5`; measuring individual nonzero ancilla labels before correction also produces leakage `0.5`. |
| Support-only and strong-symmetry counterexamples | Test explicit rank-two states for which the support or representation trace carries the wrong symmetry information. | A whole-support wedge has squared overlap `1` for an action that moves the mixed state by trace distance `0.3`; separate spectral-band wedges have overlap `0`. |
| Fourier difference and recovery | Construct character probabilities from explicit representation projectors, form their difference distribution, and propagate the exact finite distribution over generated subgroups. | Ordinary samples lie outside the required annihilator in the chosen example; difference samples lie inside it. Exact recovery probability after 12 samples is `0.999755859375`. |
| Choi covariance and norm limitation | Compare channel covariance on matrix units with normalized Choi-state invariance for a noisy rank-two channel. Give a separate low-Kraus-rank family with a constant diamond-distance violation and decreasing Choi trace distance. | Both covariance calculations give subgroup `{0,2}` of `Z4`, with Choi gap `0.3` outside it. The norm counterexample has half diamond distance `1` while its Choi gap tends to zero with dimension. |

## Why the physical growth negative controls matter

The streaming construction inherits its growth instrument from [Bene Watts et al., *Anti-symmetrization is cheap and useful*, arXiv:2610.06737v1, Algorithm 1](https://arxiv.org/html/2610.06737v1). The success block of its linear combination of permutations is the desired antisymmetric projector, but that fact alone does not establish the required failure behavior.

The ancilla must be measured with the two outcomes “zero” and “its orthogonal complement,” preserving coherence within the second outcome. On failure, the prescribed `SELECT · W` correction is applied before discarding the ancilla. An additional inverse of `W` resets the ancilla to zero; equivalently, the failure branch applies `B = W† · SELECT · W` a second time. Both forms are checked. The finite check compares the complete circuit with the ideal projector instrument. Its two negative controls diagnose a genuine implementation error rather than merely rechecking normalization: both removing the correction and refining the failure measurement destroy the invariant needed to continue streaming without restart.

## Spectral rounding and floating-point boundaries

The code uses a classical eigensolver to construct reference spectral projectors for small test matrices. This is a verification convenience, not access granted to the quantum algorithm. The actual proposed algorithm obtains approximate band samples through paid controlled density-matrix exponentiation and phase estimation.

An initial numerical trial placed a boundary exactly between two eigenvalues separated by about `2e-11`, after a random basis change. The double-precision eigensolver then produced an apparent rounded-state covariance residual of about `1.7e-8`. The individual eigenvectors were ill-conditioned at that boundary; the exact subgroup theorem was not contradicted. The retained checks use midpoint offsets and explicitly verify that every eigenvalue has the declared good-shift margin `a = w/(1000r)`. Nearly equal eigenvalues can then be handled as a stable joint projector. This numerical limitation is one reason the finite checks do not replace the analytic random-boundary and filtering arguments.

The test set deliberately includes a retained nearly degenerate cluster and a separate state with extremely small discarded eigenvalues. It does not establish uniform numerical stability for arbitrary floating-point descriptions of all low-rank states.

## The Choi-versus-diamond counterexample

For input dimension `d >= 4`, let `V` flip the phase of basis vector `|0>` and let `P` exchange `|0>` with `|1>`. Compare the unitary channel generated by `V` with its conjugate under `P`. The relative unitary is negative on two basis vectors and positive on the remainder. The input `(|0> + |2>)/sqrt(2)` gives orthogonal outputs, so the half diamond distance is exactly one.

The normalized Choi states are pure, with overlap `(d-4)/d`, so their half trace distance is

```math
D_{\mathrm{Choi}} = \sqrt{1-\left(1-\frac4d\right)^2}
                   = \sqrt{\frac8d-\frac{16}{d^2}}.
```

This tends to zero even though the channels have Kraus rank one. The channel-covariance corollary therefore needs its own Choi trace-distance separation promise; low Kraus rank alone does not convert a constant diamond gap into a dimension-independent Choi gap. The script checks the formula and explicit distinguishing input for dimensions 4, 8, 16, 32 and 64.

## Interpretation limits

These checks provide evidence against selected algebraic, normalization and implementation mistakes. They do not establish novelty, the theorem for every dimension, the copy or gate complexity, the controlled-DME approximation theorem, the QPE tail bounds, the rank-stopping tail bound, or the complete adaptive error budget. Those remain analytic arguments in the scientific writeup and cited primary sources.

The test matrices have explicit classical descriptions so they can be audited. Their construction does not provide a classical description, eigenbasis, purification or preparation inverse to the proposed learning algorithm. The script does not simulate the enormous conservative number of source copies in the existence bound and is not a performance benchmark.

All equality checks use an explicit floating-point tolerance recorded in `results.json`. Small residuals are finite numerical observations, not exact proof statements. The exact assertions about the counterexample families and general identities must be read with their accompanying analytic arguments.
