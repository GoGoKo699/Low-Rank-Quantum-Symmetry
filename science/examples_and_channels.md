# Examples, channel covariance, and scope

Throughout, $`D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1`$. The state theorem learns the exact conjugation stabilizer inside a supplied finite abelian group, assuming every non-symmetry is at least $`\epsilon`$ away in this distance. The group action and every source copy have a cost. See the [model and theorem](model.md), [spectral reduction](spectral_reduction.md), [copy algorithm](copy_algorithm.md), and [interpretation](interpretation.md) for the canonical statements; [related work](../references/related_work.md) records attribution.

## A whole-support wedge can return the wrong subgroup

Take $`G=\mathbb Z_2`$, with $`R(0)=I`$, $`R(1)=X`$, and

```math
\rho_\eta=
\begin{pmatrix}
\tfrac12+\eta&0\\
0&\tfrac12-\eta
\end{pmatrix},
\qquad 0<\eta<\tfrac12.
```

Conjugation by $`X`$ swaps the diagonal entries, so

```math
\rho_\eta-X\rho_\eta X
=\mathrm{diag}(2\eta,-2\eta),
\qquad
D(\rho_\eta,X\rho_\eta X)=2\eta.
```

The exact conjugation stabilizer is therefore $`\{0\}`$, and the theorem's promise holds for every $`0<\epsilon\leq2\eta`$.

The state has full support on its two-dimensional space. Its whole-support wedge is

```math
|w\rangle=\frac{|01\rangle-|10\rangle}{\sqrt2}.
```

But $`(X\otimes X)|w\rangle=-|w\rangle`$. Thus the projective stabilizer of this wedge is all of $`G`$, which is the wrong answer for $`\rho_\eta`$.

The spectral-band construction repairs the loss. For a concrete instance, take $`\eta=1/4`$ and $`\epsilon=1/2`$. The theorem's bands retain the eigenvalues $`3/4`$ and $`1/4`$ in different bands. Ordering the higher band first, the band wedges are the one-dimensional states $`|0\rangle`$ and $`|1\rangle`$. Their labeled tensor product is $`|0\rangle\otimes|1\rangle`$. Applying $`X`$ to both registers produces the orthogonal vector $`|1\rangle\otimes|0\rangle`$. The algorithm does not need to learn the basis vectors classically; this example just makes the distinction visible.

For a flat state $`P/r`$, the support does determine the density operator. Whole-support antisymmetrization is then enough in principle, which is why that special case is not the new boundary. The support primitive and the suggestion to use it for support learning are inherited from [BWBCGLM26, §§1.2 and 3](../references/related_work.md#bwbcglm26).

## A strong mixed-state symmetry condition can miss exact symmetries

Let $`G=\mathbb Z_2`$, $`R(1)=Z`$, and $`\rho=I_2/2`$. Then

```math
Z\rho Z=\rho,
\qquad
\mathrm{Tr}(Z\rho)=0.
```

The conjugation stabilizer is all of $`G`$. Both conditions $`\mathrm{Tr}(R(g)\rho)=1`$ and $`|\mathrm{Tr}(R(g)\rho)|=1`$ nevertheless reject its nonidentity element.

More generally, $`|\mathrm{Tr}(U\rho)|=1`$ for a unitary $`U`$ forces $`U`$ to act by one common phase on the support of $`\rho`$. Indeed, write $`\rho=\sum_i\lambda_i|i\rangle\langle i|`$ over its positive eigenvalues. Equality in

```math
\left|\sum_i\lambda_i\langle i|U|i\rangle\right|
\leq\sum_i\lambda_i|\langle i|U|i\rangle|
\leq1
```

forces each $`U|i\rangle`$ to equal $`e^{i\theta}|i\rangle`$, with the same phase. Conjugation invariance permits arbitrary unitary action within a degenerate eigenspace. The maximally mixed example realizes this difference.

This explains why the stronger mixed-state results in [HEC26, §II D](../references/related_work.md#hec26) and [HS26, §8](../references/related_work.md#hs26) do not already solve the present task.

## Channel covariance from low Kraus rank

### Access and metric

Let $`\mathcal E:\mathcal L(A)\to\mathcal L(B)`$ be an unknown channel with minimal Kraus rank at most $`r`$. The access model permits a call to $`\mathcal E`$ on an input entangled with a reference. Each invocation is charged. Independent invocations implement the same channel; a correlated memory process is a different model.

Let $`U_A(g)`$ and $`V_B(g)`$ be supplied linear unitary representations of a finite abelian group $`G`$, with efficiently implementable controlled actions. Define $`\mathrm{Ad}_U(X)=UXU^\dagger`$. The covariance subgroup is

```math
H_{\mathrm{cov}}
=\{g\in G:
\mathcal E\circ\mathrm{Ad}_{U_A(g)}
=\mathrm{Ad}_{V_B(g)}\circ\mathcal E\}.
```

Prepare the normalized Choi state

```math
J_{\mathcal E}
=(\mathrm{id}_{A'}\otimes\mathcal E)
  (|\Phi_A\rangle\langle\Phi_A|),
\qquad
|\Phi_A\rangle=\frac1{\sqrt{d_A}}\sum_{i=0}^{d_A-1}|i\rangle_{A'}|i\rangle_A.
```

One copy costs **one ordinary channel invocation**. For a qubit input of dimension $`d_A=2^{n_A}`$, the entangled input costs $`n_A`$ Hadamards and $`n_A`$ CNOTs. If another encoding is used, its actual maximally entangled-state preparation cost must be supplied.

The representation on the Choi registers is

```math
R_{\mathrm{Choi}}(g)=\overline{U_A(g)}\otimes V_B(g).
```

For known gate descriptions, complex conjugation can be compiled gate by gate with the usual precision overhead. Access to an unknown unitary oracle for $`U_A(g)`$ alone must not be treated as free access to $`\overline{U_A(g)}`$; the conjugated action has to be supplied or separately constructed and charged.

The required separation promise is

```math
D\!\left(J_{\mathcal E},
R_{\mathrm{Choi}}(g)J_{\mathcal E}R_{\mathrm{Choi}}(g)^\dagger\right)
\in\{0\}\cup[\epsilon,1]
\quad\text{for every }g\in G.
```

### Exact reduction

For any channel $`\Phi`$ and unitary $`U`$, the transpose identity for a maximally entangled state gives

```math
J_{\Phi\circ\mathrm{Ad}_{U^\dagger}}
=(\overline U\otimes I)J_\Phi(U^T\otimes I).
```

Applying this identity and the output action yields

```math
R_{\mathrm{Choi}}(g)J_{\mathcal E}R_{\mathrm{Choi}}(g)^\dagger
=J_{\mathrm{Ad}_{V_B(g)}
      \circ\mathcal E\circ\mathrm{Ad}_{U_A(g)^\dagger}}.
```

The Choi map is injective, since

```math
\mathcal E(X)
=d_A\mathrm{Tr}_{A'}[(X^T\otimes I)J_{\mathcal E}].
```

Consequently equality of the two Choi states is equivalent to

```math
\mathrm{Ad}_{V_B(g)}
\circ\mathcal E\circ\mathrm{Ad}_{U_A(g)^\dagger}
=\mathcal E,
```

which, after composing on the right by $`\mathrm{Ad}_{U_A(g)}`$, is exactly the covariance condition. The same unitary-change identity gives the useful metric equality

```math
\begin{aligned}
&D\!\left(J_{\mathcal E},
R_{\mathrm{Choi}}(g)J_{\mathcal E}R_{\mathrm{Choi}}(g)^\dagger\right)\\
&\qquad=
D\!\left(
J_{\mathcal E\circ\mathrm{Ad}_{U_A(g)}},
J_{\mathrm{Ad}_{V_B(g)}\circ\mathcal E}
\right).
\end{aligned}
```

The rank condition also transfers exactly. A Kraus representation $`\mathcal E(X)=\sum_aK_aXK_a^\dagger`$ gives

```math
J_{\mathcal E}
=\frac1{d_A}\sum_a |K_a\rangle\!\rangle
                    \langle\!\langle K_a|,
\qquad
|K_a\rangle\!\rangle=\sum_i|i\rangle\otimes K_a|i\rangle.
```

The rank of this positive operator is the dimension of the span of the vectorized Kraus operators. A spectral decomposition constructs a Kraus representation with precisely that many terms. Hence $`\mathrm{rank}(J_{\mathcal E})`$ equals the minimal Kraus rank.

### Resulting resources

Under the Choi separation promise, the state theorem returns generators of $`H_{\mathrm{cov}}`$ with constant success probability. Write $`L=1+\lceil\log_2|G|\rceil`$. Its conservative bound gives

```math
\widetilde O\!\left(
r^{12}\epsilon^{-10}L^2
\right)
```

channel invocations, because every raw state copy, including a DME program copy, costs one invocation. This is a polynomial existence bound, with no optimality or practical-size claim.

The controlled-action count is $`O(r\epsilon^{-2}L)`$ at constant confidence. Each such action uses the charged input-conjugate and output representation circuits. The remaining dimension overhead replaces $`\log d`$ by $`\log d_A+\log d_B`$. Streaming source generation and antisymmetric growth use $`O(r(\log d_A+\log d_B)+L+\log(r/\epsilon)) + A_{R_{\mathrm{Choi}}}(\zeta)+A_F(\zeta)`$ working qubits, where the final two terms are the declared controlled-action and QFT workspaces at the precision used by the [copy algorithm](copy_algorithm.md). If a channel invocation is expanded into an explicit circuit, its implementation gates and temporary workspace must also be charged. The rational precision parameter and its classical bit cost follow the [model](model.md).

No controlled call to $`\mathcal E`$, inverse channel, environment access, Kraus decomposition, or lower bound on a nonzero Kraus weight is assumed. The Choi correspondence and covariance formulation are standard; the new application is the low-rank state theorem. [BRRW23, §§3.2–3.3 and Remark 1](../references/related_work.md#brrw23) is the direct supplied-group testing comparator.

### A nonunitary channel with a proper covariance subgroup

Consider the qubit channel

```math
\mathcal E_p=(1-p)\mathrm{id}+p\,\mathrm{Ad}_X,
\qquad 0<p<1,
```

and let $`G=\mathbb Z_4`$ act on both input and output by $`U(g)=V(g)=\mathrm{diag}(1,i^g)`$. Its Choi state is

```math
J_{\mathcal E_p}
=(1-p)|\Phi^+\rangle\langle\Phi^+|
 +p|\Psi^+\rangle\langle\Psi^+|,
```

where $`|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2`$ and $`|\Psi^\pm\rangle=(|01\rangle\pm|10\rangle)/\sqrt2`$. It has rank two.

The Choi action $`\overline{U(g)}\otimes U(g)`$ fixes $`|\Phi^+\rangle`$. For $`g=2`$, it changes $`|\Psi^+\rangle`$ only by a minus sign. For either odd group element, it sends $`|\Psi^+\rangle`$ to a phase times the orthogonal state $`|\Psi^-\rangle`$. Therefore

```math
H_{\mathrm{cov}}=\{0,2\},
\qquad
D(J_{\mathcal E_p},R_{\mathrm{Choi}}(g)J_{\mathcal E_p}
  R_{\mathrm{Choi}}(g)^\dagger)=p
\quad\text{for odd }g.
```

The Choi promise holds with $`\epsilon=p`$, so the state theorem applies using one channel call per raw copy. Taking $`p=3/10`$ gives a nonflat spectrum and a constant gap.

This example also separates weak and strong symmetry at the channel level: at the exact covariance element $`g=2`$,

```math
\mathrm{Tr}(R_{\mathrm{Choi}}(2)J_{\mathcal E_p})=1-2p,
```

whose magnitude is strictly smaller than one. An algorithm that recognizes only a common phase on the Choi support misses that covariance element.

### A diamond gap need not provide a usable Choi gap

The distinction persists even for a rank-one Choi state. Let $`d\geq8`$, and define

```math
W_0=I-2|0\rangle\langle0|,
\qquad
W_1=I-2|1\rangle\langle1|.
```

Let $`S`$ swap basis vectors $`|0\rangle`$ and $`|1\rangle`$ and fix all others. Take $`G=\mathbb Z_2`$, $`U(1)=V(1)=S`$, and $`\mathcal E=\mathrm{Ad}_{W_0}`$. The conjugated channel is $`\mathrm{Ad}_{W_1}`$, since $`SW_0S=W_1`$. Their normalized Choi vectors have overlap

```math
\frac{\mathrm{Tr}(W_0^\dagger W_1)}d=1-\frac4d.
```

Thus the nontrivial Choi covariance distance is

```math
D_{\mathrm{Choi}}
=\sqrt{1-\left(1-\frac4d\right)^2}
=\sqrt{\frac8d-\frac{16}{d^2}}.
```

By contrast, the two channels send $`(|0\rangle+|2\rangle)/\sqrt2`$ to orthogonal pure states. Their half diamond distance is therefore one. Unitary precomposition preserves that distance, so the covariance violation between $`\mathcal E\circ\mathrm{Ad}_S`$ and $`\mathrm{Ad}_S\circ\mathcal E`$ also has half diamond distance one.

This explicitly shows why a constant diamond-distance promise cannot simply be substituted for the Choi-gap promise in the resource bound. It is not a lower bound against algorithms that use other channel inputs.

## Rank dependence is necessary

Let $`\tau`$ be an unknown state on an $`s`$-dimensional system, and let

```math
\omega_\tau
=\frac12|0\rangle\langle0|\otimes\tau
 +\frac12|1\rangle\langle1|\otimes\frac{I_s}{s}.
```

Use $`G=\mathbb Z_2`$ and $`R(1)=X\otimes I_s`$. The block-diagonal difference gives

```math
D(\omega_\tau,R(1)\omega_\tau R(1)^\dagger)
=D(\tau,I_s/s).
```

Also $`\mathrm{rank}(\omega_\tau)\leq2s`$. If $`\tau=I_s/s`$, the subgroup is all of $`G`$; if $`D(\tau,I_s/s)\geq\epsilon`$, it is trivial. A source copy of $`\omega_\tau`$ can be prepared with at most one copy of $`\tau`$, a fair classical bit, and a known maximally mixed state. Taking $`s`$ to be a power of two makes the latter preparation immediate.

Therefore a $`q`$-copy symmetry learner would give a $`q`$-copy mixedness tester. [OW15, Theorem 1.10](../references/related_work.md#ow15) gives an inherited worst-case lower bound

```math
q=\Omega(s/\epsilon^2)=\Omega(r/\epsilon^2)
```

for rank bound $`r=2s`$, in the usual constant-success, small-$`\epsilon`$ regime. When rank is comparable to $`d`$, even this necessary copy cost can be exponential in the number of qubits. The upper bound should therefore be read as efficient in the rank parameter, not as efficient for arbitrary-rank states.

## Why the exact separation promise matters

The algorithm does not require separation between distinct eigenvalues. It does require separation between exact symmetries and non-symmetries. These are different assumptions.

For example, let $`G=\mathbb Z_N`$, $`N\geq8`$, act by

```math
R(k)=\mathrm{diag}(1,e^{2\pi i k/N})
```

on $`|+\rangle`$. Its distance from its image under $`k`$ is $`|\sin(\pi k/N)|`$. A tolerance chosen strictly between $`\sin(\pi/N)`$ and $`\sin(2\pi/N)`$ accepts $`k=1`$ and $`k=-1`$, but rejects $`k=2`$. The accepted set is not a subgroup. Consequently an arbitrary tolerance-based version of the task cannot retain the same exact-subgroup output contract without additional definitions and promises.

The established result concerns iid source copies, a supplied rank bound and action, a finite abelian group, and an exact-or-separated subgroup. It neither performs full tomography nor learns an arbitrary approximately invariant set. Those restrictions are part of the capability proved, rather than omitted costs.
