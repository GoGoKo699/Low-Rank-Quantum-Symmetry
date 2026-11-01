# Spectral reduction and subgroup recovery

This page proves the mathematical reduction from mixed-state conjugation symmetries to pure-state projective symmetries. The finite copy-access implementation is proved in [copy_algorithm.md](copy_algorithm.md). The input and output conventions are collected in [model.md](model.md).

## 1. Setting and notation

Let $`\rho`$ be a density operator on $`\mathcal H\cong\mathbb C^d`$, and suppose a known integer $`r\ge 1`$ satisfies $`\mathrm{rank}\rho\le r`$. Replacing $`r`$ by $`\min\{r,d\}`$ is permitted. Throughout,

```math
D(\rho,\tau)=\frac12\|\rho-\tau\|_1,
\qquad 0\lt\varepsilon\le1.
```

Let $`G`$ be a finite abelian group and let $`R:G\to U(\mathcal H)`$ be a linear unitary representation. Define

```math
H=\{g\in G:R(g)\rho R(g)^\dagger=\rho\}.
```

The promise is that every $`g\notin H`$ satisfies

```math
D\bigl(\rho,R(g)\rho R(g)^\dagger\bigr)\ge\varepsilon.
```

The set $`H`$ is a subgroup. For finite accounting, use

```math
L=1+\left\lceil\log_2|G|\right\rceil.
```

The spectral and geometric lemmas below hold without commutativity of $`G`$. The final Fourier recovery algorithm uses the abelian hypothesis.

## 2. Coarse spectral bands preserve the exact promised subgroup

Set

```math
w=\frac{\varepsilon}{100r}.
```

Choose any $`u\in[w,2w)`$. Consider the intervals

```math
I_j=[u+jw,u+(j+1)w),\qquad j=0,1,2,\ldots.
```

The interval containing the eigenvalue $`1`$, if present, extends beyond $`1`$. There is no additional fixed boundary at $`1`$. Let $`P_j`$ be the spectral projector of $`\rho`$ onto $`I_j`$, retaining only nonzero projectors. Write

```math
r_j=\mathrm{rank}P_j,
\qquad b_j=u+\left(j+\frac12\right)w,
\qquad A=\sum_j b_jP_j,
\qquad s=\mathrm{Tr}A,
\qquad \sigma=A/s.
```

Eigenvalues below $`u`$ are discarded. If $`B`$ is the number of nonempty retained bands and $`R_{\rm eff}=\sum_jr_j`$, then $`B\le R_{\rm eff}\le r`$.

### Lemma 1: rounding error

The operator $`A`$ is nonzero, and

```math
D(\rho,\sigma)\le\frac52rw=\frac{\varepsilon}{40}.
```

**Proof.** There are at most $`r`$ positive eigenvalues. The discarded trace is at most $`ru\le2rw`$. Each retained eigenvalue differs from its band midpoint by at most $`w/2`$, so

```math
\|\rho-A\|_1\le2rw+\frac12rw=\frac52rw.
```

In particular, the retained trace is at least $`1-2rw\ge49/50`$, so $`A\ne0`$. Moreover,

```math
|s-1|\le\|A-\rho\|_1,
\qquad
\|A-\sigma\|_1=|s-1|.
```

The triangle inequality gives the claimed half-trace-norm bound. ∎

### Lemma 2: exact subgroup preservation

The following three subgroups coincide:

```math
H
=\{g:R(g)\sigma R(g)^\dagger=\sigma\}
=\{g:R(g)P_jR(g)^\dagger=P_j\text{ for every retained }j\}.
```

**Proof.** Every exact symmetry of $`\rho`$ preserves its spectral projectors and therefore every $`P_j`$ and $`\sigma`$. Conversely, if $`g`$ fixes $`\sigma`$, then

```math
\begin{aligned}
D\bigl(\rho,R(g)\rho R(g)^\dagger\bigr)
&\le D(\rho,\sigma)
 +D\bigl(\sigma,R(g)\sigma R(g)^\dagger\bigr)
 +D\bigl(R(g)\sigma R(g)^\dagger,R(g)\rho R(g)^\dagger\bigr)\\
&\le\varepsilon/20\lt\varepsilon.
\end{aligned}
```

The promise forces $`g\in H`$. Finally, the positive coefficients $`b_j/s`$ are distinct for distinct bands. Thus the retained $`P_j`$ are precisely the nonzero spectral projectors of $`\sigma`$, proving the remaining equality. ∎

The lemma explains why discarding arbitrarily small eigenvalues is legitimate here: the supplied separation promise prevents the discarded and rounded part from being the sole witness against a group element outside $`H`$.

## 3. A pure state encoding all retained spectral subspaces

For a rank-$`k`$ projector $`P`$, choose any orthonormal basis $`v_1,\ldots,v_k`$ of its range and define

```math
|\wedge P\rangle
=\frac1{\sqrt{k!}}\sum_{\pi\in S_k}\mathrm{sgn}(\pi)
|v_{\pi(1)}\rangle\otimes\cdots\otimes|v_{\pi(k)}\rangle.
```

A different orthonormal basis changes this vector only by a phase. Its density operator is therefore determined by $`P`$ alone. Define, in increasing band-label order,

```math
|W\rangle=\bigotimes_j|\wedge P_j\rangle,
\qquad
\mathcal R(g)=R(g)^{\otimes R_{\rm eff}}.
```

### Lemma 3: wedge overlap and principal angles

Let $`U`$ be unitary, and let $`\theta_1,\ldots,\theta_k\in[0,\pi/2]`$ be the principal angles between $`\mathrm{range}P`$ and $`U\mathrm{range}P`$. Then

```math
\left|\langle\wedge P|U^{\otimes k}|\wedge P\rangle\right|^2
=\prod_{\ell=1}^k\cos^2\theta_\ell,
\qquad
\frac12\|P-UPU^\dagger\|_1=\sum_{\ell=1}^k\sin\theta_\ell.
```

In particular, the wedge is invariant up to phase if and only if $`UPU^\dagger=P`$.

**Proof.** If $`V`$ is the matrix with columns $`v_1,\ldots,v_k`$, expansion of the two antisymmetric vectors gives

```math
\langle\wedge P|U^{\otimes k}|\wedge P\rangle=\det(V^\dagger UV).
```

The singular values of $`V^\dagger UV`$ are $`\cos\theta_\ell`$. This proves the determinant formula. In the principal-angle decomposition, each nontrivial pair of subspaces contributes eigenvalues $`\pm\sin\theta_\ell`$ to $`P-UPU^\dagger`$; the common subspace contributes zeros. Summing absolute eigenvalues proves the trace-norm formula. The product of squared cosines is one exactly when all principal angles vanish. ∎

### Theorem 4: dimension-independent projective symmetry gap

The projective stabilizer of $`W`$ under $`\mathcal R`$ is exactly $`H`$. For every $`g\notin H`$,

```math
\left|\langle W|\mathcal R(g)|W\rangle\right|^2
\le \exp(-\varepsilon^2/4),
```

and consequently

```math
1-\left|\langle W|\mathcal R(g)|W\rangle\right|^2
\ge\varepsilon^2/8.
```

**Proof.** Let $`U=R(g)`$, write $`\sigma=\sum_ja_jP_j`$, and let $`\theta_{j\ell}`$ denote the principal angles for band $`j`$. The coefficients obey

```math
a_j>0,\qquad \sum_ja_jr_j=1,\qquad a_j\le1.
```

Using Lemma 3, the triangle inequality, and weighted Cauchy–Schwarz,

```math
\begin{aligned}
D(\sigma,U\sigma U^\dagger)
&\le\sum_ja_j\sum_{\ell=1}^{r_j}\sin\theta_{j\ell}\\
&\le\sqrt{\left(\sum_ja_jr_j\right)
             \left(\sum_ja_j\sum_\ell\sin^2\theta_{j\ell}\right)}\\
&\le\sqrt{\sum_{j,\ell}\sin^2\theta_{j\ell}}.
\end{aligned}
```

If $`g\notin H`$, Lemma 1 and the separation promise imply

```math
D(\sigma,U\sigma U^\dagger)
\ge\varepsilon-2D(\rho,\sigma)
\ge19\varepsilon/20\ge\varepsilon/2.
```

Therefore $`\sum_{j,\ell}\sin^2\theta_{j\ell}\ge\varepsilon^2/4`$. Since $`1-x\le e^{-x}`$ for $`0\le x\le1`$,

```math
\left|\langle W|\mathcal R(g)|W\rangle\right|^2
=\prod_{j,\ell}\cos^2\theta_{j\ell}
\le\exp\!\left(-\sum_{j,\ell}\sin^2\theta_{j\ell}\right)
\le e^{-\varepsilon^2/4}.
```

For $`0\le x\le1`$, $`1-e^{-x}\ge x/2`$, giving the final bound. An element of $`H`$ preserves every band projector by Lemma 2 and hence every wedge up to phase. Conversely, unit overlap for the tensor product forces unit overlap in every factor, so Lemmas 2–3 give membership in $`H`$. ∎

## 4. A finite random shift creates resolvable boundaries

The preceding statements hold for every shift. The next lemma makes the band measurement implementable without an input spectral gap.

Set

```math
a=\frac{w}{1000r},\qquad
Q=2^{\lceil\log_2(100000r)\rceil}.
```

Choose an integer $`z`$ uniformly from $`\{0,\ldots,Q-1\}`$, and set

```math
u=w\left(1+\frac zQ\right).
```

Call the shift **good** if every positive eigenvalue of $`\rho`$ has distance at least $`a`$ from every retained-band boundary.

### Lemma 5: good-shift probability

The probability of a bad shift is at most

```math
\frac{2ra}{w}+\frac{2r}{Q}
\le\frac{101}{50000}\lt\frac1{100}.
```

**Proof.** For one fixed eigenvalue, reduction modulo $`w`$ turns the bad shifts into an arc of length at most $`2a/w`$ on the unit circle. An equally spaced grid of $`Q`$ points has at most $`2aQ/w+2`$ points in such an arc. The union bound over at most $`r`$ positive eigenvalues gives the claim. This upper bound allows all translated-lattice boundaries, including irrelevant ones below the first retained band, so it also bounds the stated event. Zero eigenvalues are never sampled from $`\rho`$ and lie at distance at least $`w`$ from the first retained boundary. ∎

Only $`\lceil\log_2(100000r)\rceil`$ random bits are required. With rational $`\varepsilon`$, the shift is rational and has finite bit length. The randomization concerns measurement resolution; exact subgroup preservation already holds for every shift.

## 5. Fourier differences recover the subgroup

This section uses the existing Fourier-difference principle for projective state symmetries. It is included to fix the success constants and the output contract; the sampling primitive is attributed to the symmetry-learning literature [HS].

For each character $`\chi\in\widehat G`$, let

```math
\Pi_\chi=\frac1{|G|}\sum_{g\in G}\overline{\chi(g)}\,\mathcal R(g).
```

Ordinary group Fourier sampling on $`W`$ outputs $`\chi`$ with probability

```math
p(\chi)=\|\Pi_\chi W\|^2.
```

The circuit prepares a uniform group register, applies the controlled representation, performs the group Fourier transform with the matching convention, and measures the character label. It uses one $`W`$ and at most $`r`$ applications of the supplied controlled $`R`$ circuit.

Draw $`\chi_1,\chi_2`$ independently and output $`\chi=\chi_1\chi_2^{-1}`$. Let $`q`$ be this difference distribution. Then

```math
\mathbb E_{\chi\sim q}\chi(g)
=\left|\sum_\chi p(\chi)\chi(g)\right|^2
=\left|\langle W|\mathcal R(g)|W\rangle\right|^2.
```

### Lemma 6: support and escape probability

The distribution $`q`$ is supported on

```math
H^\perp=\{\chi\in\widehat G:\chi(h)=1\text{ for all }h\in H\}.
```

If $`K`$ is a proper subgroup of $`H^\perp`$, then

```math
\Pr_{\chi\sim q}\{\chi\notin K\}\ge\varepsilon^2/16.
```

**Proof.** On $`H`$, the vector $`W`$ transforms by a character $`\alpha:H\to U(1)`$. Every character with nonzero $`p`$ has restriction $`\alpha`$ to $`H`$, so its difference with another such character is trivial on $`H`$.

By finite abelian duality, a proper $`K\lneq H^\perp`$ has an element $`g\in K^\perp\setminus H`$. Let $`t=\Pr_q(\chi\notin K)`$. Characters in $`K`$ have $`\chi(g)=1`$, and the real part of any character value is at least $`-1`$. Hence

```math
1-2t\le\mathrm{Re}\mathbb E_q\chi(g)
=|\langle W|\mathcal R(g)|W\rangle|^2
\le1-\varepsilon^2/8,
```

which proves the claim. ∎

### Theorem 7: finite Fourier recovery

Let

```math
m=\left\lceil\frac{128(L+7)}{\varepsilon^2}\right\rceil,
\qquad N_W=2m.
```

With $`m`$ independent difference samples, the generated subgroup equals $`H^\perp`$ with probability at least $`99/100`$. Its annihilator is $`H`$, and generators can be computed in time polynomial in $`m`$ and the given group-description bit length.

**Proof.** Starting from the trivial subgroup, every strict increase at least doubles the generated subgroup size. Fewer than $`L`$ strict increases can occur before the full $`H^\perp`$ is reached. Until that happens, Lemma 6 lower-bounds the conditional probability of a strict increase by $`\gamma=\varepsilon^2/16`$. Couple these increases to independent Bernoulli variables with success probability $`\gamma`$. Failure to recover $`H^\perp`$ implies fewer than $`L`$ Bernoulli successes.

The binomial mean satisfies $`\mu=m\gamma\ge8(L+7)`$. The multiplicative Chernoff bound gives

```math
\Pr\{\mathrm{Bin}(m,\gamma)\lt L\}
\le\Pr\{\mathrm{Bin}(m,\gamma)\lt\mu/2\}
\le e^{-\mu/8}
\le e^{-(L+7)}\lt1/100.
```

For a group supplied as a product of cyclic groups, characters are tuples of modular integers. Character multiplication, subgroup generation, and annihilator computation reduce to integer lattice arithmetic, for example Smith normal form. These computations are polynomial in the encoded integer lengths and do not require enumeration of $`G`$. ∎

## 6. What the reduction establishes

No positive eigenvalue or eigengap of $`\rho`$ appears in the construction's resolution parameter: $`a=\varepsilon/(100000r^2)`$ is chosen from the supplied rank bound and separation alone. The implementation must still pay for producing the band wedges. That payment, including unknown band ranks and all approximation errors, is made in [copy_algorithm.md](copy_algorithm.md).

The wedge representation and Fourier-difference machinery are inherited ingredients. The spectral-band argument above establishes that their combination retains the full exact promised conjugation subgroup for arbitrary spectra.

## References used on this page

- **[HS]** Isaac Holt and Sathyawageeswar Subramanian, *Learning quantum symmetries*, arXiv:2609.38085v2 (2026), especially Fourier difference sampling and §10.4 on conjugation symmetries. [Primary manuscript](https://pdfs.assets.alphaxiv.org/2609.38085v2.pdf).
- **[HEC]** Marcel Hinsche, Jens Eisert, and Jose Carrasco, *Abelian State Hidden Subgroup Problem: Learning Stabilizer Groups and Beyond*, PRX Quantum **7**, 020337 (2026), DOI 10.1103/6frk-891j. [Publisher](https://journals.aps.org/prxquantum/abstract/10.1103/6frk-891j).
- **[AS]** Adam Bene Watts, John Bostanci, Matthias C. Caro, Daniel Grier, Sihan Liu, and Gaurav Mahajan, *Anti-symmetrization is cheap and useful*, arXiv:2610.06737v1 (2026). [Primary manuscript](https://arxiv.org/html/2610.06737v1).
