# From Watrous to low-rank quantum symmetry

A source repeatedly supplies the same unknown mixed quantum state. A finite group supplies candidate transformations through a known controlled circuit. The question is to return generators of every transformation that leaves the state unchanged, with all other transformations promised to move it by an observable minimum amount.

Low rank makes it possible to retain the relevant spectral information in a relatively small quantum encoding. The algorithm does not first reconstruct the state or learn its eigenvectors. It groups nearby eigenvalues into bands, prepares one exterior-power state per retained band, and uses a Fourier measurement to identify the subgroup.

The single educational anchor is **John Watrous, The Theory of Quantum Information**, Cambridge University Press, 2018. Section references below use the author's **January 2018 prepublication manuscript**, available through the [author's page](https://cs.uwaterloo.ca/~watrous/TQI/) and its [contents](https://cs.uwaterloo.ca/~watrous/TQI/TQI.frontmatter.pdf). The author's page identifies the book's publication as April 2018. This repository links the manuscript and does not reproduce it.

Watrous supplies the mathematical quantum-information language. The group Fourier procedure, signed exterior-power construction, density-matrix exponentiation and finite stopping argument are supplied by the project's scientific pages and attributed research dependencies. They are not presented as results taught by the book. The [30-milestone map](MILESTONES.md) organizes the route; the [model](../science/model.md) and the linked proofs remain authoritative.

## Targeted reading from the single anchor

Read the indicated portions alongside the relevant project argument. Completing the book first is unnecessary.

| Project use | Watrous manuscript sections | What to carry into the project |
|---|---|---|
| States, spectra, support and rank; M01–M02 and M06 | [§1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf), [§§2.1.2–2.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Spectral decompositions, positive operators and independent quantum registers. |
| Known transformations and physical outcomes; M03 and M05 | [§§2.2.1–2.2.2 and 2.3.1–2.3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Channels, their physical representations, measurements and retained records. |
| State distance and approximation; M04, M10, M13–M14 and M23 | [§1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf), [§3.1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Trace norm and the operational distinguishability of states. |
| Tensor-factor permutations; M07, M15 and M21 | [§7.1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.7.pdf) | Permutation operators. The project's signed averaging and growth instrument are additional constructions. |
| Pure-state phase and overlap; M08 and M16 | [§2.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), [§3.2.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Vector representatives of pure states and their overlaps. |
| Finite probability arguments; M17, M20, M22 and M25 | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Probability distributions and events. The particular concentration estimates are stated and applied in the project proofs. |
| Reference-safe simulation errors; M18 and M23 | [§§3.3.2–3.3.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Completely bounded trace norm and channel distances, including ancillary references. |
| Choi states, Kraus rank and channel metrics; M27–M28 | [§§2.2.1–2.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), [§§3.3.1–3.3.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Channel representations and their operational distinction from one fixed probe state. |

The finite abelian character theory in M09 and M24–M25 is explained below and in [spectral reduction §5](../science/spectral_reduction.md#5-fourier-differences-recover-the-subgroup). It is not an additional educational-anchor assignment. The same boundary applies to the primary research modules in the [attribution ledger](../references/related_work.md#inherited-modules-and-the-remaining-claim).

## Input and notation

Watrous commonly writes vectors and adjoints without Dirac notation. The following translation fixes the conventions used here.

| Object | Watrous-style notation | Project notation and convention |
|---|---|---|
| A unit vector and its pure state | A column vector and its outer product | A ket and its rank-one projector |
| One system | A finite-dimensional complex space | The Hilbert space of dimension d |
| State | A positive trace-one operator | The unknown density operator rho |
| Rank | Dimension of the image of an operator | At most the supplied integer r |
| Unitary adjoint | An asterisk | A dagger |
| Trace distance | Trace-norm expressions | D is one half the trace norm of the state difference |
| Channel distance | Completely bounded trace norm | Delta-diamond is one half the diamond norm of the channel difference |
| Choi operator | The unnormalized operator of a linear map | The project uses a normalized Choi state, divided by the input dimension |

In formulas, the state's exact conjugation subgroup is

```math
H_\rho=\{g\in G:R(g)\rho R(g)^\dagger=\rho\},
\qquad
D(\rho,\sigma)=\frac12\|\rho-\sigma\|_1.
```

The promise says that every element outside this subgroup has distance at least the supplied positive parameter $`\varepsilon`$ from invariance. A state may have eigenvalues arbitrarily close together or arbitrarily close to zero. That spectral freedom is distinct from allowing arbitrarily small nonsymmetry violations.

A source copy is a specimen, including a program specimen consumed during simulation. It is not a classical density matrix, a purification, a controlled preparation unitary or a preparation inverse. With $`n=\lceil\log_2d\rceil`$ qubits and $`L=1+\lceil\log_2|G|\rceil`$, the theorem's independent parameters are rank, inverse separation, system size and group-description length. The [access model](../science/model.md#1-inputs-and-access) specifies the supplied circuits and the [resource account](../science/model.md#4-resource-accounting) charges them.

## A complete two-dimensional example

Consider a state with probabilities three quarters and one quarter in the computational basis. Let the two-element group act by either doing nothing or exchanging the basis vectors:

```math
\rho=\begin{pmatrix}3/4&0\\0&1/4\end{pmatrix},
\qquad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
```

After the exchange, the probabilities are reversed. The state difference has diagonal entries one half and minus one half, so its half trace norm is one half. The exact subgroup therefore contains only the identity, and the promise holds with $`\varepsilon=1/2`$.

The support is the whole two-dimensional space. Its top wedge is the antisymmetric two-register vector

```math
|w\rangle=\frac{|01\rangle-|10\rangle}{\sqrt2},
\qquad
(X\otimes X)|w\rangle=-|w\rangle.
```

The minus sign changes no pure-state density operator. A procedure that encoded only this support would report the whole group as a projective stabilizer and lose the actual answer.

The algorithm instead retains two different spectral bands. With $`r=2`$ and $`\varepsilon=1/2`$, its width is $`w=1/400`$, so the two eigenvalues are always in different retained bands. In increasing band order, their one-dimensional wedges give $`|W\rangle=|10\rangle`$. The exchange maps this state to $`|01\rangle`$, an orthogonal vector. The band encoding now distinguishes the nonsymmetry.

For this two-element group, the Fourier measurement has two characters, taking values plus one or minus one on the exchange. The orthogonal orbit gives each character probability one half. Differences of independent character outcomes are again uniform, so each difference has probability one half of being nontrivial. After m differences, the chance of having seen no nontrivial character is $`2^{-m}`$. Once that character is present, its annihilator is the identity subgroup, which is the desired answer.

By comparison, the whole-support wedge always gives the same minus character. Its differences are always trivial, and the annihilator of those differences is the whole group. The example shows exactly what the spectral bands restore. It is a hand calculation for understanding; the general guarantee comes from the proofs, and the actual algorithm never learns these basis vectors classically.

## Why bands retain the answer

The first missing step beyond the textbook is task-specific spectral coarse graining. With width $`w=\varepsilon/(100r)`$, discard eigenvalues below a shifted threshold between w and twice w and round every retained eigenvalue to its band's midpoint. Normalize the resulting positive operator to obtain a state called sigma.

There are at most r positive eigenvalues. The discarded mass is at most twice rw, and the retained rounding error is at most rw divided by two. Normalization costs at most the same trace-norm discrepancy, giving

```math
D(\rho,\sigma)\le\frac{\varepsilon}{40}.
```

Every symmetry of rho preserves its spectral projectors and therefore sigma. Conversely, if a group element fixes sigma, unitary invariance of distance and the triangle inequality show that it moves rho by at most twice this rounding error. That is strictly below the promised nonsymmetry separation. The promise forces it to be an exact symmetry of rho.

Distinct retained bands have distinct rounded positive coefficients. Preserving sigma is therefore equivalent to preserving each retained spectral projector. The algorithm has reduced a mixed-state problem to a list of subspace-preservation problems without assuming any spectral gap in the input.

The mechanism relies on the promised task. Nearby states do not generally have the same exact subgroup; a sufficiently small perturbation can break an exact symmetry. The proof works because its rounded state is built from rho's own spectral projectors and the original nonsymmetries are separated. See [the two rounding lemmas](../science/spectral_reduction.md#2-coarse-spectral-bands-preserve-the-exact-promised-subgroup).

## Exterior powers and the overlap gap

For a k-dimensional subspace, place an orthonormal basis into k registers and take its normalized signed sum over permutations. Changing the basis multiplies the resulting top wedge by the determinant of the basis change. The pure-state density operator consequently depends only on the subspace.

Watrous §7.1.1 supplies the register-permutation operators and unsigned symmetric-subspace language. Here the sign of each permutation selects an exterior-power subspace instead. The signed projector and the physical streaming construction are supplied and attributed in this project's proofs; a symmetric-subspace projector cannot simply replace them.

If V lists an orthonormal basis of a retained band and U is a group transformation, the wedge overlap is the determinant of $`V^\dagger UV`$. Its singular values are cosines of the principal angles between the band and its image. Thus

```math
|\langle\wedge P|U^{\otimes k}|\wedge P\rangle|^2
=\prod_{\ell=1}^k\cos^2\theta_\ell,
\qquad
\frac12\|P-UPU^\dagger\|_1
=\sum_{\ell=1}^k\sin\theta_\ell.
```

The first expression measures pure-state overlap loss; the second measures subspace motion. Taking one wedge per band and their ordered tensor product keeps all the band information. Unit overlap in the tensor requires unit overlap in every factor, which requires preservation of every band.

For the quantitative gap, write sigma as a sum of retained projectors weighted by positive coefficients. Those coefficients times the projector ranks sum to one. Weighted Cauchy–Schwarz bounds the trace distance moved by sigma by the square root of the sum of squared principal-angle sines over all bands. A nonsymmetry moves sigma by at least half the input separation. Finally, a product of one minus each squared sine is at most the exponential of the negative sum. The result is

```math
|\langle W|R(g)^{\otimes R_{\rm eff}}|W\rangle|^2
\le e^{-\varepsilon^2/4}
\quad\text{for }g\notin H_\rho,
\qquad R_{\rm eff}\le r.
```

No ambient-dimension factor is needed. This is the bridge from the mixed-state separation promise to the pure-state Fourier method. Exact stabilizer equality and the quantitative bound are proved together in [Theorem 4](../science/spectral_reduction.md#theorem-4-dimension-independent-projective-symmetry-gap).

## Constructing the band source from paid copies

A spectral band is an exact mathematical subspace. Its physical measurement needs finite resolution, and a fixed band boundary could lie arbitrarily close to an unknown eigenvalue. The algorithm chooses one of finitely many random shifts. A union bound over at most r positive eigenvalues makes it likely that every relevant boundary is separated from every positive eigenvalue by a prescribed margin. This margin is chosen from rank and the supplied symmetry separation; it is not an assumed eigengap.

Phase estimation then labels a target copy by its band. Repeating the experiment with fresh ancillas and taking a median controls the label error. This must leave a usable quantum specimen as well as a classical label. The input is the state itself, which is a mixture of its eigenstates, so the proof establishes an approximation to an unconditional classical–quantum state source. It does not claim a diamond approximation to an ideal spectral measurement on every possible target state.

The needed evolutions are built by density-matrix exponentiation. Fresh copies of rho act as program registers in partial-SWAP operations and are discarded after use. To get coherent controlled evolution, use the extended density matrix consisting of rho and a known control state. Its exponential is a controlled exponential of rho. This preserves the access model: no source preparation inverse or source purification is supplied.

Each program step must exponentiate the full-register SWAP operator. A product of exponentiated bit swaps generally implements another operator. The construction resolves the full SWAP's two eigenvalues coherently, applies a phase and uncomputes the eigenvalue register. The [finite implementation](../science/copy_algorithm.md#3-an-unconditional-band-sampler) pays for all these steps, bounds reference-safe simulation error and allocates the finite gate-synthesis precision.

Once a retained band is selected ideally, it has probability at least w and every eigenvalue of its normalized conditional state is at least w. These facts make band discovery and capped rejection finite. They are derived properties of retained ideal bands, not new promises on the smallest positive eigenvalue of the original state.

## Physical approximation and finite stopping

The streaming growth routine keeps an antisymmetric state on k data registers and appends a fresh copy from one band. A coherent ancilla circuit implements the test for growth to k plus one registers. On failure, it applies a correction before discarding the appended register. The binary zero predicate is measured while the nonzero ancilla labels remain coherent.

The resulting success and failure operators are the projector onto the larger exterior power and its complement, restricted to the old antisymmetric input subspace. Both preserve antisymmetry of the retained registers. Failure may change the state within that subspace; the proof needs its subspace membership, rather than state equality.

Below the true band rank, every trial has a lower-bounded chance to grow, even after previous failures. At full rank, growth is impossible and the retained top wedge is a unique pure state. Stopping after a fixed number of consecutive failures therefore estimates the unknown rank with bounded premature-stop probability. Caps on requests, samples and retained registers apply on all branches, including erroneous ones.

Physical filtering can leak outside an ideal band's support. It would be invalid to assign exact ideal rank to each approximate filtered state and then reuse the ideal stopping proof directly. Instead, compare the entire physical experiment with an ideal one before conditioning:

```math
D(\widetilde\Omega_u,\Omega_u)\le\xi,
\qquad
\text{at most }T\text{ source calls},
\qquad
\text{total output-distance error}\le T\xi.
```

Here Omega is the unconditional band source, including its tail label. Each call uses fresh independent copies. Replace the calls one at a time and apply trace-distance contractivity to the entire remaining adaptive experiment. Wrong labels, leakage, changed stopping decisions and aborts are included. This argument neither divides an error by a rare event probability nor assumes that the physical output has exact rank. A separate compilation budget covers the known circuit blocks. See [the physical instrument](../science/copy_algorithm.md#lemma-1-exact-physical-instrument), [stopping rule](../science/copy_algorithm.md#unknown-rank-stopping-rule) and [global hybrid](../science/copy_algorithm.md#the-global-sampler-hybrid).

## Characters and group access

For a cyclic factor of order N, a character is specified by an integer j modulo N and assigns the phase $`e^{2\pi i jg/N}`$ to element g. For a product of cyclic groups, multiply those phases coordinate by coordinate. Character labels therefore have a compact classical representation of the same order of bit length as group labels.

The characters trivial on a subgroup H form its annihilator, written $`H^\perp`$. Taking an annihilator twice returns H. The algorithm will learn generators of the annihilator first and then compute generators of H by integer arithmetic in the supplied cyclic coordinates.

Prepare a uniform group register, apply the supplied controlled tensor-power action to W, perform the group Fourier transform and measure a character. If W acquires a phase character on H, every possible outcome restricts to that same character on H. The outcomes can lie in an unknown coset of the annihilator rather than the annihilator itself.

Take two independent outcomes and multiply the first by the inverse of the second. The common stabilizer phase cancels. The difference distribution q is supported on the annihilator, and its character expectation is

```math
\mathbb E_{\chi\sim q}\chi(g)
=|\langle W|R(g)^{\otimes R_{\rm eff}}|W\rangle|^2.
```

Now suppose observed differences generate only a proper subgroup of the true annihilator. There is a group element outside H on which that observed subgroup is trivial. The overlap gap forces a lower-bounded probability that the next sample escapes it. Every strict subgroup enlargement at least doubles its size, so only logarithmically many successful enlargements are needed. A finite sample budget gives constant-confidence recovery of the entire annihilator. No ambient-group enumeration or classical state reconstruction is required.

The pure-state character-measurement and difference-sampling mechanisms are inherited. The spectral-band construction makes them applicable to ordinary conjugation symmetries of nonflat low-rank mixed states. The [Fourier proof](../science/spectral_reduction.md#5-fourier-differences-recover-the-subgroup) supplies the constants and the [related-work account](../references/related_work.md) gives the source-specific task distinctions.

## Resource interpretation

The conservative construction uses

```math
N=\widetilde O(r^{12}\varepsilon^{-10}L^2)
\quad\text{raw copies},
\qquad
Q_R=O(r\varepsilon^{-2}L)
\quad\text{controlled-action calls}.
```

The large copy polynomial contains discovery, rejected band samples, repeated growth trials, finite stopping and every density-matrix-exponentiation program copy. The supplied action and group Fourier circuits have their own gate costs. If preparing one source specimen is expensive, multiply that cost by the raw-copy budget.

At most rank-many data registers are retained, while program copies arrive and are consumed in a stream. The resulting active memory is linear in rank times the qubit count, with additional group and precision registers and the declared supplied-circuit workspaces. Holding every input copy simultaneously would be a different memory requirement.

Polynomial rank and inverse-polynomial separation on many qubits give a polynomial existence result under efficient supplied operations. Exponential rank can make even the necessary copy cost exponential. The inherited mixedness-testing reduction gives an order $`r/\varepsilon^2`$ lower bound in its stated regime; it does not match the conservative upper polynomial. Optimal exponents and practical crossover claims remain open. See [complete resource accounting](../science/copy_algorithm.md#7-copy-gate-memory-and-bit-accounting) and [the lower bound](../science/examples_and_channels.md#rank-dependence-is-necessary).

## Normalized Choi states and the channel boundary

Watrous's Choi operator convention is unnormalized. For an input dimension d-A, this project divides that operator by d-A to obtain a trace-one state. It can be prepared by applying the unknown channel once to one half of a known maximally entangled state. Minimal Kraus rank equals the rank of this normalized Choi state; normalization changes no rank.

The channel's input covariance action is complex conjugated on the reference half, while the output action acts directly on the output half. Under that representation, Choi-state conjugation invariance is equivalent to channel covariance. Known gate descriptions allow the conjugated input action to be constructed with a charged implementation. An unknown input-unitary oracle alone is not a free conjugated-action oracle.

Each raw Choi-state specimen costs one channel invocation, including all program specimens used for density-matrix exponentiation. The resulting corollary therefore learns covariance under a **normalized-Choi trace-distance** separation promise. It assumes no controlled channel invocation, environment access, inverse channel or supplied Kraus decomposition.

A diamond-distance promise is different. The [rank-one example](../science/examples_and_channels.md#a-diamond-gap-need-not-provide-a-usable-choi-gap) has constant optimal channel-discrimination distance while its normalized-Choi distance tends to zero with dimension. One fixed maximally entangled input can dilute a change concentrated in a small subspace. This prevents a dimension-independent substitution of metrics in the corollary; it does not rule out algorithms using other inputs.

## What completes the bridge

The textbook foundations become this result through four additional connections: task-protected spectral coarse graining; a band-by-band exterior-power encoding with a quantitative overlap gap; paid finite preparation with a valid failure instrument and unconditional error control; and phase-insensitive Fourier recovery of an entire subgroup.

These connections keep the conclusion aligned with its assumptions: finite abelian groups, supplied controlled linear actions, independent low-rank specimens and an exact-or-separated symmetry promise. Arbitrary approximate-symmetry sets, general nonabelian recovery, unrestricted rank and constant-noise robustness are outside the established theorem. The [scientific interpretation](../science/interpretation.md) joins the mechanism to its reach, and [M30](MILESTONES.md#m30-the-complete-scientific-story) is the map's final synthesis.
