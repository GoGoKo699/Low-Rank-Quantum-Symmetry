# Low-Rank Quantum Symmetry

**Can independent copies reveal every symmetry of an unknown mixed state?** This project gives a finite quantum algorithm that recovers the entire conjugation-symmetry subgroup inside a supplied finite abelian group, for states of bounded rank and arbitrary spectrum.

The learner receives independent copies of $`\rho`$, a rank upper bound $`r`$, and a known controlled linear group action. Every group element either fixes the state exactly or moves it by at least a supplied half-trace-distance gap $`\varepsilon`$. The output is a classical generating set for the exact subgroup, with probability at least $`2/3`$. No input eigengap, lower bound on the smallest positive eigenvalue, purification, or preparation inverse is supplied.

## Result and resources

Write $`d`$ for the Hilbert-space dimension and $`L=1+\lceil\log_2|G|\rceil`$. A conservative implementation has the following worst-case costs.

| Resource | Bound |
|---|---|
| Raw independent copies | $`\widetilde O(r^{12}\varepsilon^{-10}L^2)`$ |
| Controlled group-action calls | $`O(r\varepsilon^{-2}L)`$ |
| Quantum memory, apart from supplied circuit workspace | $`O(r\lceil\log_2d\rceil+L+\log(r/\varepsilon))`$ |
| Output | Generators of the entire exact conjugation-symmetry subgroup |

The [model and theorem](science/model.md) state the access assumptions and full contract. The [finite algorithm](science/copy_algorithm.md) gives explicit integer budgets, every abort rule, precision allocations, and paid gate and classical-arithmetic costs. State preparation, the controlled action, and group Fourier operations must be efficient for an efficient end-to-end application. The large copy polynomial is an existence bound; optimal rank and precision exponents are not established.

For polynomial-rank states on many qubits, the result identifies a subgroup without constructing a density matrix or enumerating the ambient group. It does not extend to unrestricted rank at polynomial cost in the qubit count.

## Why spectral bands matter

A pure exterior-power state can encode a subspace without choosing an eigenbasis. One such state for the whole support loses the spectral information needed to determine the symmetries of a nonflat mixed state.

The reduction instead discards a small spectral tail, rounds the remaining eigenvalues on a randomly shifted grid, and encodes each retained band by its own top exterior power. The symmetry-distance promise ensures that this coarse graining preserves the exact answer. The tensor of these band states has the correct projective stabilizer and a dimension-independent squared-overlap gap.

Controlled density-matrix exponentiation and streaming antisymmetric growth prepare the band states from paid copies. Fourier differences then reconstruct the subgroup. Those primitives are inherited; the [attribution ledger](references/related_work.md) identifies their sources and the arbitrary-spectrum reduction established here.

## Read the science

Start with the [connected scientific overview](science/README.md), or go directly to the relevant question.

| To inspect | Read |
|---|---|
| Exact task, promises, access and theorem | [Model and guarantees](science/model.md) |
| Coarse bands, exact subgroup preservation, overlap gap and Fourier recovery | [Spectral reduction](science/spectral_reduction.md) |
| Unknown ranks, valid failure branches, finite stopping, copy and gate budgets | [Finite copy algorithm](science/copy_algorithm.md) |
| Support counterexamples, channel covariance and the inherited rank lower bound | [Examples and channels](science/examples_and_channels.md) |
| What the capability means and what remains open | [Interpretation](science/interpretation.md) |
| Closest results and inherited ingredients | [Related work](references/related_work.md) and [bibliography](references/references.bib) |
| Finite diagnostic checks and their limits | [Verification](verification/README.md) |

The [LLM reading guide](llms.txt) maps scientific questions to their authoritative files.

## Learn the construction

The [learning route](learning/README.md) connects John Watrous's *The Theory of Quantum Information* to this problem. The [30 milestones](learning/MILESTONES.md) follow the argument from state distinguishability through spectral bands, exterior powers, Fourier recovery and finite resource accounting. The [source bridge](learning/WATROUS_BRIDGE.md) identifies the textbook foundations and the additional algorithmic steps developed in the scientific account.

## Reproduce the finite checks

From the repository root:

```bash
python -m pip install -r verification/requirements.txt
python -B verification/checks.py
```

All seven recorded diagnostic groups pass. They check finite subgroup examples, wedge geometry, the complete physical growth instrument, Fourier differences, and channel counterexamples. The [verification account](verification/README.md) explains the negative controls, numerical tolerances and scope; [results.json](verification/results.json) records the executed script hash and environment. The general theorem and resource bounds rest on the written proofs.

The [hosted mathematics check](verification/hosted/README.md) compares expressions with their actual GitHub rendering at wide and narrow viewports. Its report and screenshots require separate visual review.

## Scope

The group is finite and abelian, its controlled linear representation is supplied, and exact symmetries are separated from all other elements by a promised trace distance. The channel corollary assumes a normalized-Choi trace-distance gap; a constant diamond-distance violation alone is insufficient, even at Kraus rank one. Approximate symmetry learning, arbitrary nonabelian groups, unknown actions and constant-noise robustness are outside the established result.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
