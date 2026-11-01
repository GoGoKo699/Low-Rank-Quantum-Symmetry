# Model, task and guarantees

A mixed quantum state can be unchanged by a transformation while its eigenvectors acquire different phases or rotate inside a degenerate eigenspace. The task here is to identify every such transformation inside a supplied finite abelian group. The learner receives independent copies of the state and returns a classical generating set for its symmetry subgroup.

The result applies to an unknown state of low rank with arbitrary eigenvalues. Its accuracy scale comes from a promised separation between exact symmetries and nonsymmetries, rather than gaps between eigenvalues. The [spectral reduction](spectral_reduction.md) and [finite algorithm](copy_algorithm.md) prove the result.

## 1. Inputs and access

Let $`\mathcal H\cong\mathbb C^d`$, with $`d\ge2`$, and let $`\rho`$ be an unknown density operator. The learner is given:

| Input | Meaning and cost |
|---|---|
| Independent state copies | Each requested specimen is in state $`\rho`$, independent of the others. Every target and program copy is counted. |
| Rank bound | A known integer $`1\le r\le d`$ with $`\mathrm{rank}\rho\le r`$. The exact rank and eigenbasis are unknown. A larger supplied bound can be replaced by $`\min\{r,d\}`$. |
| Finite abelian group | A decomposition $`G\cong\mathbb Z_{N_1}\times\cdots\times\mathbb Z_{N_k}`$, with efficient arithmetic and a charged approximate quantum Fourier transform. |
| Known group action | A linear unitary representation $`R:G\to U(\mathcal H)`$ and controlled implementation of $`C_R=\sum_g\lvert g\rangle\langle g\rvert\otimes R(g)`$. |
| Separation parameter | A rational $`0\lt\varepsilon\le1`$ for the promise below. Its input length is part of classical preprocessing. |

The representation satisfies $`R(gh)=R(g)R(h)`$ at the mathematical level. Finite gate synthesis approximates its supplied implementation within an allocated total error budget. The theorem does not automatically cover a merely projective representation. Phases of the constructed pure state's stabilizer are handled within an ordinary linear representation.

For a qubit implementation, set $`n=\lceil\log_2d\rceil`$. Padding uses a known embedding and a supplied extension of the action that preserves the physical space.

There is no supplied purification, controlled preparation unitary, inverse preparation, classical eigenbasis, or block encoding of $`\rho`$. Spectral operations are constructed from paid copies. If one specimen costs $`C_{\rm prep}`$ to prepare, add $`NC_{\rm prep}`$ to the implementation cost. Efficient source preparation is a separate condition for an efficient end-to-end application.

## 2. Symmetry promise and output

We use half the trace norm:

```math
D(\rho,\sigma)=\frac12\|\rho-\sigma\|_1.
```

Define

```math
H_\rho=\{g\in G:R(g)\rho R(g)^\dagger=\rho\}.
```

The identity fixes $`\rho`$, and invariance is closed under products and inverses, so $`H_\rho`$ is a subgroup. The input promise is

```math
\forall g\in G,\qquad
D\!\left(\rho,R(g)\rho R(g)^\dagger\right)
\in\{0\}\cup[\varepsilon,1].
```

The output is generators of the **entire exact subgroup** $`H_\rho`$, with probability at least $`2/3`$. Failure includes an incorrect answer or a declared abort. Every branch has finite caps; success is not conditional on an uncharged postselection event.

At most $`\lceil\log_2|G|\rceil`$ generators suffice. The output therefore fits in $`O((1+\log|G|)^2)`$ bits in the supplied group coordinates. The task does not ask for a density matrix, eigenbasis, or enumeration of all elements.

A trivial $`G`$ is handled without copies. We use $`L=1+\lceil\log_2|G|\rceil`$ throughout.

The separation promise is essential: arbitrarily small violations cannot be distinguished from exact invariance with a uniform finite number of copies. Elements selected by a threshold on approximate invariance also need not form a subgroup.

## 3. Main theorem

**Theorem 1 (learning low-rank conjugation symmetries).** Under the stated access model and promise, a quantum algorithm returns generators of $`H_\rho`$ with probability at least $`2/3`$. It uses polynomially many copies and elementary operations in $`r`$, $`\varepsilon^{-1}`$, $`L`$ and $`n`$, provided the supplied action and group Fourier circuits have polynomial cost.

A deliberately conservative implementation uses

```math
N=\widetilde O\!\left(r^{12}\varepsilon^{-10}L^2\right)
```

raw copies and

```math
Q_R=O\!\left(r\varepsilon^{-2}L\right)
```

calls to the controlled action. The tilde hides logarithmic factors in the displayed parameters, not a dependence on $`d`$. Exact finite caps, success allocation and arithmetic conventions are given in [the algorithm](copy_algorithm.md).

The source-independent gate overhead is polynomial in these parameters. Paid copy-simulation steps require $`O(n)`$ swap-related gates per program copy, plus finite synthesis overhead. Action circuits, Fourier transforms and subgroup arithmetic are charged separately. A unit oracle query does not include the physical cost of building that oracle.

Program copies can arrive in a stream. Active quantum memory is

```math
O\!\left(rn+L+\log(r/\varepsilon)\right),
```

apart from workspace for supplied circuits. This is an implementation upper bound, not an optimal-memory theorem. Receiving all copies before processing would require additional storage for that supply.

No lower bound on a nonzero eigenvalue and no gap between distinct eigenvalues is imposed. Low rank is essential to the cost: if $`d=2^n`$ and $`r`$ is exponential in $`n`$, this algorithm can also be exponentially costly.

### Proof dependencies

| Step | Statement | Proof |
|---|---|---|
| Coarse spectrum | Discarding a small tail and rounding retained eigenvalues preserves the exact promised subgroup. | [Spectral reduction](spectral_reduction.md) |
| Pure-state encoding | The tensor of band exterior-power states has projective stabilizer $`H_\rho`$ and squared-overlap gap $`\Omega(\varepsilon^2)`$. | [Spectral reduction](spectral_reduction.md) |
| Paid preparation | Random boundaries, copy-based spectral estimates, rejection caps and antisymmetric growth produce those states with finite costs. | [Copy algorithm](copy_algorithm.md) |
| Subgroup output | Fourier differences generate $`H_\rho^\perp`$; abelian arithmetic returns its annihilator. | [Copy algorithm](copy_algorithm.md) |
| Physical approximation | A hybrid over unconditional samplers controls the complete adaptive experiment, including abort branches. | [Copy algorithm](copy_algorithm.md) |

The determinant identities and sampling primitives are established tools. [Related work](../references/related_work.md) identifies the inherited results and the arbitrary-spectrum reduction used for this task.

## 4. Resource accounting

Rank bounds the mass lost under coarse graining, the number of retained bands, and the number of quantum registers needed for their exterior powers. The separation parameter determines the precision needed to preserve the answer. The controlled action supplies coherent access to the large group; repeated tests of separately specified elements do not automatically reconstruct the subgroup.

A physical accounting is

```math
NC_{\rm prep}+Q_RC_R+Q_{\rm F}C_{\rm F}
+C_{\rm known}+C_{\rm classical},
```

where $`Q_{\rm F}=O(\varepsilon^{-2}L)`$. The costs $`C_R`$ and $`C_{\rm F}`$ refer to the supplied action and Fourier circuits at the precisions used. Initialized ancillas, controlled swaps, discarded program systems and finite gate synthesis are covered in the [construction](copy_algorithm.md). No QRAM or inverse access to the unknown source is supplied.

The polynomial is an existence bound. A large gap remains to the inherited mixedness-testing lower bound in [examples and channels](examples_and_channels.md). Optimal rank and precision exponents are not established.

## 5. Perturbations and scope

If independent input specimens instead have state $`\widetilde\rho`$ with $`D(\rho,\widetilde\rho)\le\eta`$, a capped implementation using at most $`N`$ copies changes its final output distribution by at most $`N\eta`$. Replace copies one at a time and apply trace-distance contractivity. This basic continuity statement is not constant-noise robust learning: $`N`$ may be large, and the perturbed state's exact subgroup may change.

The theorem concerns finite abelian groups, supplied controlled linear actions, exact symmetries separated from alternatives, and low-rank states. Continuous groups, arbitrary nonabelian groups, unknown actions, and unrestricted rank are outside the theorem.

The [channel corollary](examples_and_channels.md) uses normalized Choi states and a Choi trace-distance separation promise. A fixed diamond-distance covariance violation does not provide the same dimension-independent promise.

**Next:** [spectral reduction](spectral_reduction.md), then [finite algorithm](copy_algorithm.md).
