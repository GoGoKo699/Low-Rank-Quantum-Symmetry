# Related work and attribution

Primary-source verification date: 1 November 2026. Bibliographic records are in [references.bib](references.bib). Section and theorem numbers below refer to the specified versions, rather than to an unpinned latest preprint.

## The precise contribution boundary

The problem is to recover generators of the conjugation stabilizer

```math
H=\{g\in G:R(g)\rho R(g)^\dagger=\rho\}
```

from independent copies of an unknown state of rank at most a supplied bound $`r`$. The ambient group is a supplied finite abelian group, its controlled linear representation is available at an explicitly charged cost, and every element outside $`H`$ changes the state by at least a supplied trace-distance gap $`\epsilon`$.

The new boundary addressed here is **arbitrary-spectrum, low-rank mixed-state conjugation symmetry learning without an input eigengap or a lower bound on the smallest nonzero eigenvalue**. The proposed spectrum-to-flag reduction retains enough spectral information to preserve the exact promised subgroup, while producing a pure state with a dimension-independent overlap gap. Its [finite implementation](../science/copy_algorithm.md) counts all source copies, including those consumed in filtering. The [model](../science/model.md) and [spectral proof](../science/spectral_reduction.md) give the canonical statements.

The basic subroutines are inherited. In particular, this project does not introduce density-matrix exponentiation, antisymmetric growth, the top exterior power of a subspace, or Fourier difference sampling. Applying antisymmetrization only to the whole support would not establish the stated result: a rank-two nonflat state and a basis swap already give a counterexample. See [examples and channels](../science/examples_and_channels.md).

## Comparison at a glance

| Primary comparator | Established ingredient or task | Boundary retained here |
|---|---|---|
| [HEC26](#hec26), §II D | Defines mixed StateHSP and explains why its character-measurement method need not solve ordinary mixed-state conjugation invariance | An efficient low-rank solution to that weaker symmetry task, under a trace-distance separation promise |
| [HS26](#hs26), §§8, 10.4 | Solves anyonic symmetry learning and explicitly defines ConjugateSL | The mixed-state anyonic condition is stronger than conjugation invariance; the ConjugateSL definition is a comparator, not an existing solution of this low-rank theorem |
| [BWBCGLM26](#bwbcglm26), §§1.2, 3 | Efficiently prepares a canonical pure wedge of an unknown state's support | A family of coarse spectral-band wedges retains information that a single support wedge discards |
| [LMR14](#lmr14); [GKPPW25](#gkppw25) | Sample-based density-matrix exponentiation and eigenvalue labeling | Filtering costs and finite errors are paid inside the new reduction |
| [BRRW23](#brrw23), §§3.1–3.3 | Tests asymmetry relative to a supplied group or action | The output here is generators of an unknown subgroup, without enumerating the ambient group |
| [OW15](#ow15), Theorem 1.10 | A mixedness-testing copy lower bound | An immediate reduction makes rank dependence unavoidable; it does not match the upper-bound exponent |
| [GJMM26](#gjmm26), §5.3 | States general mixed StateHSP hardness | Its near-invariance reduction is not used as an exact-null hardness theorem for this contract |

## Verified primary comparisons

### HEC26

Marcel Hinsche, Jens Eisert, and Jose Carrasco, **Abelian State Hidden Subgroup Problem: Learning Stabilizer Groups and Beyond**, *PRX Quantum* **7**, 020337 (published 26 May 2026). [Journal article](https://journals.aps.org/prxquantum/abstract/10.1103/6frk-891j), [journal PDF](https://journals.aps.org/prxquantum/pdf/10.1103/6frk-891j), DOI: 10.1103/6frk-891j.

The comparison is with **§II D, Definition 6, Eqs. (39)–(40), journal pages 020337-9–020337-10**. Definition 6 permits ordinary conjugation invariance and a specified norm gap outside the subgroup. The authors explain that the mixed-state character distribution can put weight outside the true annihilator. They establish success under the stronger condition $`\operatorname{Tr}(R(h)\rho)=1`$, with a character gap outside the subgroup, and leave efficient learning under the weaker invariance condition open.

The present rank-parameterized theorem addresses a restricted regime of that open task. It does not claim unrestricted polynomial-time mixed StateHSP. Their §§II B–C are also part of the attribution for character measurements and their efficient realization.

### HS26

Isaac Holt and Sathyawageeswar Subramanian, **Learning quantum symmetries**, arXiv:2609.38085, **version 2**. [Version record](https://arxiv.org/abs/2609.38085v2), [inspected version-2 PDF](https://pdfs.assets.alphaxiv.org/2609.38085v2.pdf).

**§8, Problem 8.1 and Lemma 8.3, pp. 22–23**, defines the anyonic condition $`|\operatorname{Tr}(R(g)\rho)|=1`$ and uses the doubled representation $`R(g)\otimes R(g^{-1})`$. Its coefficient is $`|\operatorname{Tr}(R(g)\rho)|^2`$. This supplies the phase-insensitive Fourier-sampling ingredient after our reduction to a pure state. Their mixed-state stabilizer application should not be described as learning every ordinary conjugation symmetry.

**§10.4, Problems 10.13–10.14, p. 41**, defines subspace symmetry learning and ConjugateSL, and reduces the former to the latter using maximally mixed subspace states. That section does not provide a general ConjugateSL algorithm. The new claim here concerns a finite abelian group with a linear action, low rank, arbitrary spectrum, and an explicit trace-distance promise; it does not inherit the paper's broader projective or nonabelian scope.

### BWBCGLM26

Adam Bene Watts, John Bostanci, Matthias C. Caro, Daniel Grier, Sihan Liu, and Gaurav Mahajan, **Anti-symmetrization is cheap and useful**, arXiv:2610.06737, **version 1, 5 October 2026**. [Version record](https://arxiv.org/abs/2610.06737v1), [full text](https://arxiv.org/html/2610.06737v1).

**§3, Algorithm 1 and Theorem 3** supply the growth instrument and its preservation of antisymmetry after failure. **Algorithm 2 and Theorem 5** supply streaming growth from copies, with a bound depending on the smallest nonzero eigenvalue. All of that mechanism is inherited.

**§1.2, “Anti-symmetrization for support learning and testing,”** explicitly suggests using the unique wedge to study support properties, and explains that whole-support antisymmetrization loses spectral information. A flat-spectrum special case would therefore be too close to their stated application direction. The present reduction uses multiple labeled coarse spectral bands and the symmetry separation promise to retain the needed information. Random boundaries and truncation make the inherited growth primitive usable without a spectral-floor assumption on the original input.

### LMR14

Seth Lloyd, Masoud Mohseni, and Patrick Rebentrost, **Quantum principal component analysis**, *Nature Physics* **10**, 631–633 (2014). [Journal article](https://www.nature.com/articles/nphys3029), [arXiv record](https://arxiv.org/abs/1307.0401), DOI: 10.1038/nphys3029.

This is the original attribution for density-matrix exponentiation and its use with phase estimation to access spectral information from copies. The relevant mechanism is in the main-text density-matrix exponentiation and quantum-PCA construction. The finite error guarantee used in this repository is taken from the more recent source below. No uncharged preparation oracle, inverse preparation, or block encoding of the unknown state is assumed.

### GKPPW25

Byeongseon Go, Hyukjoon Kwon, Siheon Park, Dhrumil Patel, and Mark M. Wilde, **Sample-based Hamiltonian and Lindbladian simulation: Non-asymptotic analysis of sample complexity**, *Quantum Science and Technology* **10**, 045058 (2025). Inspected **arXiv:2412.02134v3, 29 September 2025**. [Version record](https://arxiv.org/abs/2412.02134v3), [full text](https://arxiv.org/html/2412.02134v3), DOI: 10.1088/2058-9565/ae075b.

**Theorem 2, Eq. (30)** bounds the normalized diamond error of $`n`$-step DME by $`4t^2/n`$, under $`n>t`$. **Appendix E** discusses controlled DME and its use in phase estimation. These are the quantitative filtering dependencies. The theorem can also be applied to the extended density matrix $`|1\rangle\langle1|\otimes\rho`$, whose copies cost one original copy each, to obtain a controlled evolution with reference-safe error.

We count target copies and program copies separately before adding them. The global finite-call hybrid is a composition argument in this repository, rather than a claim that approximate filtering preserves exact rank.

### BRRW23

Rahul Bandyopadhyay, Alex H. Rubin, Marina Radulaski, and Mark M. Wilde, **Efficient quantum algorithms for testing symmetries of open quantum systems**, *Open Systems & Information Dynamics* **30**(3), 2350017 (2023), DOI: 10.1142/S1230161223500178. [Author-hosted manuscript, dated 3 September 2023](https://rlab.engineering.ucdavis.edu/sites/g/files/dgvnsk8056/files/media/documents/Efficient_quantum_algorithms_for_testing_symmetry_of_open_quantum_systems_0.pdf), [arXiv record](https://arxiv.org/abs/2309.02515).

**§3.1** treats state symmetry tests; **§3.2** estimates Hilbert–Schmidt distances of Choi states; **§3.3 and Remark 1, Eq. (79)** treat channel covariance, including different input and output actions. The method estimates supplied-group asymmetry using SWAP-based quantities. The introduction explicitly identifies testing as a component of learning.

The present output is the unknown subgroup itself. Efficiently testing a specified action, or estimating group-averaged asymmetry, does not by itself reconstruct generators with polynomial dependence on $`\log|G|`$. The [channel corollary](../science/examples_and_channels.md#channel-covariance-from-low-kraus-rank) uses a normalized-Choi trace gap; it does not replace their task by a stronger metric without paying the conversion cost.

### OW15

Ryan O'Donnell and John Wright, **Quantum Spectrum Testing**, STOC 2015, pp. 529–538, DOI: 10.1145/2746539.2746582. Inspected **arXiv:1501.05028v1** and the [author-hosted full manuscript dated 20 January 2015](https://people.eecs.berkeley.edu/~jswright/papers/quantum-spectrum-testing.pdf).

**Theorem 1.10**, with its proof in **§4**, gives $`\Theta(s/\epsilon^2)`$ copies for testing whether an $`s`$-dimensional state is maximally mixed. The reduction in [examples and channels](../science/examples_and_channels.md#rank-dependence-is-necessary) converts this into an inherited $`\Omega(r/\epsilon^2)`$ worst-case lower bound for the present problem, even for $`G=\mathbb Z_2`$. Norm-normalization changes only constants. This lower bound justifies the role of rank; it does not show that the conservative polynomial upper bound is optimal.

### GJMM26

Alexandru Gheorghiu, Dale Jacobs, Saeed Mehraban, and Arsalan Motamedi, **Quantum state isomorphism problems for groups**, arXiv:2605.12615, **version 1, 12 May 2026**. [Full text](https://arxiv.org/html/2605.12615v1).

**§5.3, Theorem 5.7** states QSZK-hardness for mixed StateHSP. Its displayed reduction starts from quantum state distinguishability with exponentially close states in the YES case; the resulting label-swap state is exponentially nearly invariant, rather than necessarily exactly invariant. This repository therefore does not use that proof to claim QSZK-hardness of its exact-null promise problem. Its own rank lower bound rests on the exact mixedness-testing reduction above.

## Inherited modules and the remaining claim

| Module | Attribution or status |
|---|---|
| Sample-based spectral labeling | [LMR14](#lmr14), with finite simulation bounds from [GKPPW25](#gkppw25) |
| Streaming antisymmetric growth; useful failure branches | [BWBCGLM26](#bwbcglm26) |
| Character measurements and phase-insensitive sampling | [HEC26](#hec26), [HS26](#hs26) |
| Exterior-power determinant and principal-angle identities | Standard finite-dimensional linear algebra; the relevant identities are derived in the proof files |
| Random coarse bands preserving the exact promised stabilizer | The spectrum-to-flag reduction established in this repository |
| Dimension-independent overlap gap for the tensor of band wedges | The quantitative reduction established in this repository |
| Discovery, rank stopping, caps, and a global filtering-error budget | The finite copy-only composition established in this repository |
| Low-Kraus-rank channel covariance | A direct Choi-state corollary of the state theorem; the Choi reduction itself is inherited |

The substantive distinction is the recovery of ordinary conjugation symmetries of a nonflat low-rank state. It is not a new support-learning primitive or a renamed strong-symmetry problem. The copy bound is an existence bound with large exponents. Optimal exponents, approximate symmetry learning, unrestricted rank, continuous groups, and a dimension-independent diamond-gap channel theorem are outside the established claim.
