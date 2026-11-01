# What the algorithm makes possible

The algorithm returns a symmetry group: a compact classical description of transformations leaving an unknown mixed state unchanged. Its cost in the independent-copy access model can be polynomial in the number of qubits even when a matrix or eigenbasis description would be exponentially large. An efficient end-to-end application also requires efficient source preparation. The conditions are low rank, a supplied symmetry-distance separation, and efficient coherent access to a known finite abelian action.

## The information missing from a support-only description

For a pure state, conjugation invariance means that a unitary maps its vector to a scalar phase. A mixed state may be invariant while its eigenvectors acquire different phases or rotate inside degenerate eigenspaces. Its symmetry need not appear as a unit-modulus matrix coefficient $`\operatorname{Tr}(\rho R(g))`$. [Related work](../references/related_work.md) explains the resulting limitation of existing strong-symmetry methods.

A canonical exterior-power state encodes a subspace without selecting an eigenbasis. For a rank-$`k`$ projector $`P`$ with orthonormal basis $`v_1,\ldots,v_k`$, its normalized top wedge is

```math
|{\wedge P}\rangle=
\frac1{\sqrt{k!}}\sum_{\pi\in S_k}\operatorname{sgn}(\pi)
|v_{\pi(1)}\rangle\otimes\cdots\otimes|v_{\pi(k)}\rangle.
```

Changing this basis changes the vector only by a global phase. A unitary preserves the subspace exactly when its tensor-power action preserves that wedge up to phase.

One wedge of the whole support does not suffice for an arbitrary spectrum. States with the same support but different eigenvalue patterns can have different symmetry groups. A [rank-two counterexample](examples_and_channels.md) makes this failure explicit.

## Why coarse spectral bands suffice

The symmetry-distance promise supplies an accuracy scale. Construct a rounded state $`\sigma`$ close enough to $`\rho`$ that an element fixing $`\sigma`$ cannot be an $`\varepsilon`$-separated nonsymmetry of $`\rho`$. Every exact symmetry of $`\rho`$ already preserves all its spectral projectors and hence fixes $`\sigma`$.

The learner therefore needs only retained spectral bands. Each band has its own top wedge, and their tensor product keeps the bands separate. The construction gives

```math
D(\rho,\sigma)\le\varepsilon/40,
```

and, for an element outside the true subgroup,

```math
\left|\langle W|R(g)^{\otimes R_{\rm eff}}|W\rangle\right|^2
\le e^{-\varepsilon^2/4},\qquad R_{\rm eff}\le r.
```

This dimension-independent gap connects the mixed-state trace-distance promise to the pure-state Fourier method. The [spectral proof](spectral_reduction.md) uses principal angles and determinant overlaps.

## Random boundaries and eigenvalue gaps

A fixed threshold may lie arbitrarily close to an unknown eigenvalue. A randomly shifted grid avoids all relevant eigenvalues by a controlled margin with high constant probability, using a union bound over at most $`r`$ nonzero eigenvalues.

Filtering resolution is therefore polynomial in $`r`$ and $`\varepsilon^{-1}`$ regardless of how close two eigenvalues are to one another. Tiny eigenvalues may be discarded because their total mass is rank-bounded; nearby eigenvalues may share a band. No input eigenvalue-gap assumption is introduced.

The symmetry-distance promise remains essential. It guarantees that merging and discarding this spectral information does not change the requested answer.

## Preparation is paid

Spectral operations on the unknown density operator are implemented using controlled density-matrix exponentiation, which consumes independent program copies. Antisymmetric growth then consumes filtered copies until each band's top exterior power is reached.

A failed growth attempt can change the retained state. The correct circuit nevertheless returns it to the same exterior-power subspace so growth can continue. The [finite construction](copy_algorithm.md) includes that failure recovery, bounded stopping, and every rejected copy.

Physical filtering also introduces leakage. It would be incorrect to assign an approximate filtered state the exact rank and eigenvalue floor of its ideal counterpart. The proof instead compares the entire finite experiment with an ideal one, replacing unconditional samplers one at a time. The common error budget covers incorrect labels, early stopping, leakage and the final group output.

## Reach and remaining questions

For $`n`$-qubit states with polynomial rank and inverse-polynomial separation, the construction has polynomial costs in the independent-copy access model when the supplied group operations do. Source preparation is charged separately. It identifies a subgroup of a potentially exponentially large group without enumeration or full state tomography.

A channel of low Kraus rank supplies a low-rank normalized Choi state with one ordinary channel call per copy. This gives a covariance-learning application under a Choi trace-distance promise. The [channel example](examples_and_channels.md) shows why a constant diamond-distance violation alone is insufficient.

The current copy exponent is conservative. Improving it, finding simpler state-construction procedures, optimizing active memory and obtaining stronger noise tolerance remain open. The theorem establishes a tractable regime for a defined learning task; it does not establish a practical speedup over every classical experiment or a matching complexity law.

The [verification suite](../verification/README.md) checks finite instances of the geometry, circuits and counterexamples. The asymptotic guarantee comes from the written proofs and the precisely attributed primitives.
