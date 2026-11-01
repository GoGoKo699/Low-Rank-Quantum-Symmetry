# Finite algorithm from independent copies

This page implements the reduction proved in [spectral_reduction.md](spectral_reduction.md). It includes unknown band ranks, all stopping rules, coherent control, finite precision, and a worst-case copy budget. All bounds refer to independent copies of the input state; no preparation unitary, preparation inverse, purification, or eigenbasis description is supplied.

## 1. Theorem and computational convention

Let $`\rho\in\mathcal D(\mathbb C^d)`$, let $`r`$ be a known positive integer upper bound on its rank, and let $`\varepsilon\in(0,1]`$ be a supplied positive rational lower bound, encoded with $`b_\varepsilon`$ bits. Let $`G`$ be a finite abelian group supplied as a product of cyclic groups. A supplied linear representation $`R:G\to U(\mathbb C^d)`$ has an efficiently implementable controlled action

```math
C_R:|g\rangle|v\rangle\longmapsto|g\rangle R(g)|v\rangle.
```

Assume the promise

```math
D\bigl(\rho,R(g)\rho R(g)^\dagger\bigr)
\in\{0\}\cup[\varepsilon,1],
\qquad D(\rho,\tau)=\tfrac12\|\rho-\tau\|_1.
```

Write

```math
H=\{g:R(g)\rho R(g)^\dagger=\rho\},\quad
L=1+\lceil\log_2|G|\rceil,\quad
q=\lceil\log_2d\rceil.
```

For a channel difference, use normalized diamond distance

```math
\Delta_\diamond(\mathcal E,\mathcal F)
=\tfrac12\|\mathcal E-\mathcal F\|_\diamond.
```

The supplied controlled-action circuit and the group Fourier transform may either be exact charged oracles or have finite-precision implementations. Denote their gate costs at normalized diamond error at most $`\zeta`$ by $`C_R(\zeta)`$ and $`C_F(\zeta)`$, and their additional quantum workspace by $`A_R(\zeta)`$ and $`A_F(\zeta)`$. The group structure supplies the usual efficient Fourier implementation; a general controlled representation is a separate input assumption.

### Main theorem

There is a finite algorithm that outputs generators of $`H`$ with probability at least $`2/3`$. Its worst-case resources are

```math
N=\widetilde O\!\left(r^{12}\varepsilon^{-10}L^2\right)
```

independent copies of $`\rho`$, at most $`O(r\varepsilon^{-2}L)`$ applications of the supplied controlled action, and

```math
\widetilde O\bigl(N(q+1)\bigr)
+O(r\varepsilon^{-2}L)C_R(\zeta)
+O(\varepsilon^{-2}L)C_F(\zeta)
```

elementary gates. Here $`\zeta`$ is explicitly inverse-polynomial in the finite circuit budget below. The working quantum memory is

```math
O\!\left(rq+L+\log(r/\varepsilon)\right)
+A_R(\zeta)+A_F(\zeta).
```

The tilde hides powers of logarithms of $`r,L,\varepsilon^{-1}`$ and gate-synthesis precision. The cost of reading and processing the $`b_\varepsilon`$ input bits is additional and polynomial. No factor polynomial in $`d`$, no reciprocal of an input eigengap, and no reciprocal of the smallest positive input eigenvalue is hidden in the bound. The exponent of $`r`$ and $`\varepsilon^{-1}`$ is a conservative implementation bound, without an optimality assertion.

If $`G`$ is trivial or $`d=1`$, output the evident whole symmetry group directly. Otherwise the construction below applies. One may replace $`r`$ by $`\min\{r,d\}`$ before setting its parameters.

## 2. All finite parameters

For a positive integer $`x\ge2`$, let $`\ell(x)=\lceil\log_2x\rceil`$. These are integer bit-length operations. In particular, $`\ell(x)\ge\ln x`$.

Use the spectral parameters

```math
w=\frac{\varepsilon}{100r},\qquad
a=\frac{w}{1000r},\qquad
Q=2^{\ell(100000r)}.
```

Choose $`z\in\{0,\ldots,Q-1\}`$ uniformly and set $`u=w(1+z/Q)`$. This same shift is used throughout the run. Bands have boundaries $`u+jw`$ and extend past $`1`$; estimates below $`u`$ receive a tail label.

Set the Fourier and stopping parameters in the following order:

```math
\begin{aligned}
m&=\left\lceil128(L+7)/\varepsilon^2\right\rceil,
&N_W&=2m,\\
S_g&=2rN_W,
&N_0&=\left\lceil w^{-1}\ell(100r)\right\rceil,\\
M_g&=\left\lceil(r+1)w^{-1}\ell(100S_g)\right\rceil,
&J&=S_gM_g,\\
M_f&=\left\lceil w^{-1}\ell(100J)\right\rceil,
&T&=N_0+JM_f.
\end{aligned}
```

The meanings of the budgets are:

| Symbol | Finite role |
|---|---|
| $`N_0`$ | Unconditional band samples for discovering the nonempty bands |
| $`M_g`$ | Consecutive failed growth trials before declaring the current band rank |
| $`J`$ | Maximum total number of requests for a conditioned band copy |
| $`M_f`$ | Maximum unconditional band-sampler attempts in each such request |
| $`T`$ | Maximum number of unconditional band-sampler invocations in the entire run |
| $`N_W`$ | Number of pure wedge-tensor preparations, one per ordinary Fourier sample |

The band sampler receives the accuracy parameters

```math
\xi=\frac1{100T},\qquad
\nu=\beta=\frac\xi2=\frac1{200T}.
```

Its phase-estimation parameters are

```math
M=2^s\text{, the least power of two with }M\ge512/a,
\qquad
h=4\ell(200T)+1,
\qquad
S=h(M-1).
```

The odd integer $`h`$ counts repetitions. The quantity $`S`$ is the sum of the simulated evolution times in one complete band-sampler invocation.

All of these parameters are computable from finite classical input. No test of an unknown eigenvalue is used to choose a running-time bound.

## 3. An unconditional band sampler

For a fixed shift, the ideal band sampler is a state source with classical–quantum output

```math
\Omega_u
=|\mathsf{tail}\rangle\langle\mathsf{tail}|\otimes P_{\mathsf{tail}}\rho P_{\mathsf{tail}}
+\sum_j|j\rangle\langle j|\otimes P_j\rho P_j.
```

Here $`P_j`$ are the nonempty retained spectral projectors from the reduction, and $`P_{\mathsf{tail}}`$ is the spectral projector below $`u`$. The total trace is one. Every physical invocation starts with a fresh target copy of $`\rho`$ and fresh independent program copies.

### 3.1 High-confidence phase estimation

Use $`s`$-qubit phase estimation for $`e^{i\rho}`$, with controlled evolutions at times $`1,2,\ldots,2^{s-1}`$. Repeat this experiment $`h`$ times on the same target, using fresh phase registers. Convert each measured phase to its principal angle in $`[-\pi,\pi)`$, compute that angle to absolute error at most $`a/8`$, and clip it to $`[0,1]`$. Take the ordinary median of the $`h`$ real estimates and assign its band label. The target register is retained.

Principal-angle decoding is necessary at zero: an outcome close to phase $`2\pi`$ represents a small negative angle and is clipped to zero. The choice $`e^{i\rho}`$ keeps the actual eigenvalue $`1`$ distinct from the phase of the eigenvalue zero.

**Single-run bound.** For an eigenstate of eigenvalue $`\lambda`$, write $`\theta=\lambda/(2\pi)`$. Exact phase estimation has outcome probabilities

```math
p_y=\frac{\sin^2(\pi M(\theta-y/M))}
{M^2\sin^2(\pi(\theta-y/M))},
```

with the continuous value used when the denominator vanishes. If $`\delta_y`$ is the circular distance from $`\theta`$ to $`y/M`$, then $`p_y\le1/(4M^2\delta_y^2)`$ whenever $`\delta_y\ne0`$.

An angle error larger than $`a/4`$ requires circular index error larger than

```math
\frac{Ma}{8\pi}\ge\frac{64}{\pi}>20.
```

Relative to the closest integer to $`M\theta`$, such an outcome is at least 20 integers away. Summing the two tails gives the bound

```math
\Pr\{\text{principal-angle error}>a/4\}
\le2\sum_{n=20}^{\infty}\frac1{4(n-1/2)^2}
\le\frac1{37}\lt\frac1{16}.
```

The finite angle calculation adds at most $`a/8`$. Clipping to $`[0,1]`$ cannot increase distance from $`\lambda\in[0,1]`$. Thus a good repetition has error at most $`3a/8`$.

**Median bound.** Conditional on an input eigenstate, the exact phase-estimation experiments leave that eigenstate unchanged, and their fresh ancillas give independent outcomes. Hoeffding's inequality bounds the probability that at least half the repetitions are bad by

```math
\exp\!\left[-2h\left(\frac12-\frac1{16}\right)^2\right]
\le e^{-h/4}\le\nu.
```

On a good shift, every positive input eigenvalue is at least $`a`$ from a band boundary. A median within $`3a/8`$ therefore gives the correct band label.

The input is $`\rho`$ itself, an eigenstate mixture. Accordingly, with exact controlled evolutions, the output classical–quantum state has trace distance at most $`\nu`$ from $`\Omega_u`$. This is a guarantee for this state source. We do not assume that finite-confidence phase estimation implements an ideal spectral-measurement channel in diamond norm on arbitrary targets.

### 3.2 Controlled density-matrix exponentiation is charged

For the phase-estimation control qubit $`c`$, define the density matrix

```math
H_c=|1\rangle\langle1|_c\otimes\rho.
```

Its evolution is exactly a controlled evolution of the target:

```math
e^{itH_c}
=|0\rangle\langle0|\otimes I
+|1\rangle\langle1|\otimes e^{it\rho}.
```

A program copy of $`H_c`$ is prepared from one known qubit in $`|1\rangle`$ and one fresh copy of $`\rho`$. Ordinary sample-based exponentiation applied to this extended program state therefore gives the required coherent control. The control qubit may be entangled with every other register; the error bound below is a diamond bound.

For completeness, a partial-SWAP step has a dimension-independent error bound. Let $`F`$ be the full SWAP between the system and one program register. The step applies $`e^{i\Delta F}`$ and discards the program. Its first-order channel is $`\mathrm{id}+i\Delta[H_c,\cdot]`$. Both this reduced unitary channel and the ideal channel $`\mathrm{Ad}_{e^{i\Delta H_c}}`$ have Taylor remainder of ordinary diamond norm at most $`2\Delta^2`$: their Hamiltonians have operator norm at most one, so their unitary-channel second derivatives have diamond norm at most four. Hence their normalized diamond distance is at most $`2\Delta^2`$, and in particular at most $`4\Delta^2`$.

Composition with $`n`$ fresh program copies at step size $`t/n`$ gives

```math
\Delta_\diamond\bigl(\widetilde{\mathcal U}_t,
\mathrm{Ad}_{e^{itH_c}}\bigr)
\le4t^2/n.
```

This is the standard density-matrix-exponentiation ingredient [DME], applied to the extended program state. It neither assumes a controlled preparation of $`\rho`$ nor converts a supplied unknown unitary into a controlled unitary.

There are $`hs`$ evolutions in the repeated phase-estimation circuit. For each occurrence with time $`t\in\{1,2,\ldots,M/2\}`$, allocate diamond error

```math
\eta_t=\beta t/S
```

and consume

```math
n_t=\left\lceil\frac{4St}{\beta}\right\rceil
```

program copies. The sum of these error allocations is $`\beta`$. The exact number of program copies per sampler is

```math
n_{\rm prog}
=h\sum_{j=0}^{s-1}\left\lceil\frac{4S2^j}{\beta}\right\rceil
\le hs+\frac{4S^2}{\beta}.
```

Combining the diamond error of the controlled evolutions with the exact-evolution label bound gives, on a good shift,

```math
D(\widetilde\Omega_u,\Omega_u)\le\beta+\nu=\xi.
```

Known-gate compilation error is assigned a separate budget in Section 7.

### 3.3 Implementing a full partial SWAP

The Hamiltonian SWAP here exchanges entire $`q+1`$-qubit registers. Its exponential is not the product of the exponentials of the individual bit swaps. To implement it, coherently compute the $`\pm1`$ eigenvalue of the full SWAP into a one-qubit ancilla with a Hadamard, a controlled full SWAP, and a Hadamard. Apply the appropriate one-qubit phase rotation and undo that eigenvalue computation. This realizes $`e^{i\Delta F}`$ with two controlled full SWAPs and one phase rotation. A controlled full SWAP is $`q+1`$ Fredkin gates. Thus each DME program copy costs $`O(q+1)`$ exact swap-related gates and one compilable rotation, with constant additional ancilla space.

## 4. Discovering bands and requesting conditional copies

First invoke the unconditional band sampler $`N_0`$ times, record all non-tail labels, and discard the quantum outputs. Abort if the label set is empty or has more than $`r`$ elements. Sort the observed labels.

In the ideal experiment, a retained band has mass

```math
p_j=\mathrm{Tr}(P_j\rho)\ge w.
```

There are at most $`r`$ such bands. Consequently the probability of missing any retained band is at most

```math
r(1-w)^{N_0}\le r e^{-wN_0}\le1/100.
```

A request for a copy in a specified observed band $`j`$ invokes the unconditional sampler up to $`M_f`$ times. Discard outputs with other labels; return the quantum register of the first output labeled $`j`$. Abort if all $`M_f`$ attempts fail. In the ideal experiment, a returned state is exactly

```math
\tau_j=P_j\rho P_j/p_j,
\qquad \tau_j\ge wP_j.
```

The inequality uses $`p_j\le1`$ and the retained eigenvalue floor $`\lambda\ge u\ge w`$. Each capped request fails with probability at most

```math
e^{-wM_f}\le\frac1{100J}.
```

The caps below allow at most $`J`$ requests, so their total ideal abort probability is at most $`1/100`$. Correctly returned conditional states are independent fresh samples of $`\tau_j`$; the capped search does not change their conditional state.

## 5. Antisymmetric growth with a valid failure branch

The streaming growth primitive is inherited from [AS, Algorithm 1]. The coherent failure correction is essential to its use here.

Let $`\Pi_k`$ be the antisymmetric projector on the first $`k`$ data registers. Suppose the current data state lies in its range, and append a new data register. For $`k\ge1`$, define

```math
A_k=\frac1{k+1}\left(I-\sum_{i=1}^k\mathrm{SWAP}_{i,k+1}\right).
```

The permutation expansion of the antisymmetric projector gives

```math
A_k\Pi_k=\Pi_kA_k=\Pi_{k+1},
\qquad
\Pi_k\Pi_{k+1}=\Pi_{k+1}\Pi_k=\Pi_{k+1}.
```

Let $`W_k`$ be a known unitary preparing the uniform state on labels $`0,\ldots,k`$ from ancilla $`|0\rangle`$. Let $`\mathrm{SELECT}_k`$ apply the identity on label zero and $`-\mathrm{SWAP}_{i,k+1}`$ on label $`i\in\{1,\ldots,k\}`$; define it as the identity on padding labels. Set

```math
B_k=(W_k^\dagger\otimes I)\mathrm{SELECT}_k(W_k\otimes I).
```

This is a Hermitian unitary. The growth trial is:

1. Start the ancilla in $`|0\rangle`$ and apply $`B_k`$.
2. Measure only the binary predicate “the ancilla is zero,” preserving coherence among all nonzero labels.
3. On the zero outcome, report success and retain all $`k+1`$ data registers.
4. On the other outcome, apply $`B_k`$ once more, discard the ancilla and the appended data register, and report failure.

For $`k=0`$, simply accept the first conditional copy; this is the identity measurement $`\Pi_1=I`$.

### Lemma 1: exact physical instrument

On the input subspace $`\mathrm{range}\Pi_k`$, the data Kraus operators before discarding the appended register are $`\Pi_{k+1}`$ on success and $`I-\Pi_{k+1}`$ on failure. Both outcomes preserve antisymmetry of the first $`k`$ registers, and success grows it to $`k+1`$.

**Proof.** The zero-to-zero block of $`B_k`$ is $`A_k`$, which equals $`\Pi_{k+1}`$ on the input subspace. On a fully antisymmetric $`k+1`$-register vector, every negative transposition in $`\mathrm{SELECT}_k`$ acts as the identity. Hence

```math
B_k\bigl(|0\rangle\otimes\Pi_{k+1}|\psi\rangle\bigr)
=|0\rangle\otimes\Pi_{k+1}|\psi\rangle.
```

After the nonzero outcome and the second application of $`B_k`$, the unnormalized joint state is

```math
\begin{aligned}
B_k(I-|0\rangle\langle0|\otimes I)B_k|0\rangle|\psi\rangle
&=|0\rangle|\psi\rangle
-B_k|0\rangle\Pi_{k+1}|\psi\rangle\\
&=|0\rangle(I-\Pi_{k+1})|\psi\rangle.
\end{aligned}
```

Commutation with $`\Pi_k`$ proves the retained antisymmetry. The argument extends by linearity to mixed inputs and inputs entangled with other retained registers. All operations on the data are permutations, so a common support subspace is preserved. ∎

Measuring the individual nonzero ancilla labels, or omitting the failure correction, does not implement this instrument and is not part of the algorithm.

### Lemma 2: a uniform growth probability below the true rank

Let $`V=\mathrm{range}P_j`$ have dimension $`r_j`$. For any current state $`\omega`$ on $`\wedge^kV`$ and any independent incoming $`\tau_j\ge wP_j`$, if $`k\lt r_j`$ then

```math
\Pr(\text{growth})
=\mathrm{Tr}\!\left[(\omega\otimes\tau_j)\Pi_{k+1}\right]
\ge w\frac{r_j-k}{k+1}
\ge\frac{w}{r+1}.
```

At $`k=r_j`$, the growth probability is exactly zero.

**Proof.** On $`V^{\otimes(k+1)}`$, partial trace of the antisymmetric projector satisfies

```math
\mathrm{Tr}_{k+1}\Pi_{k+1}^{V}
=\frac{r_j-k}{k+1}\Pi_k^{V}.
```

One can verify this in the orthonormal wedge basis: every $`k`$-element basis subset has $`r_j-k`$ possible added basis vectors, each contributing $`1/(k+1)`$, and all off-diagonal entries vanish. Since $`\tau_j-wP_j\ge0`$, taking its tensor product with $`\omega`$ and pairing with the positive projector proves the lower bound. At full rank, $`\wedge^{r_j+1}V`$ is zero. ∎

### Unknown-rank stopping rule

For each observed band, start with the empty wedge and counter $`k=0`$. Request a conditioned band copy and run a growth trial. After a success, increment $`k`$ and reset the consecutive-failure counter. After a failure, discard only the appended register and increment that counter. Stop this band when the counter reaches $`M_g`$; declare its rank to be the current $`k`$ and retain the current wedge.

Repeat in the sorted band order and tensor the retained results. During every complete tensor preparation:

- Abort before exceeding $`2rM_g`$ conditioned-copy requests.
- Abort if a growth success would make the total number of retained data registers exceed $`r`$.

These caps apply even on erroneous physical branches. In the ideal experiment they do not abort: the sum of the true band ranks is at most $`r`$, and the number of growth stages, including each final unsuccessful stage, is at most

```math
\sum_j(r_j+1)\le2r.
```

For a stage below the true rank, Lemma 2 applies after every preceding failure. Thus the probability of $`M_g`$ consecutive failures there is at most

```math
\left(1-\frac{w}{r+1}\right)^{M_g}
\le e^{-M_gw/(r+1)}\le\frac1{100S_g}.
```

Across $`N_W`$ tensor preparations there are at most $`S_g=2rN_W`$ stages. The probability of any premature stop is therefore at most $`1/100`$. A correct stop leaves the unique pure state $`|\wedge P_j\rangle`$ in that band. At full rank, the final failed trials act as the identity before their fresh input is discarded, so they do not disturb this state.

On correct discovery and stopping, every complete preparation is the same $`|W\rangle`$ from the spectral reduction, up to an irrelevant overall phase. Fresh input copies give independent preparations. The implementation never needs a description of any eigenvector.

## 6. Full algorithm and success probability

The complete algorithm is now finite:

1. Choose the shift and all budgets from Section 2.
2. Discover the nonempty retained band labels with $`N_0`$ unconditional samples.
3. Repeat $`N_W`$ times: prepare a band-wedge tensor using the capped rank-discovery routine; apply one ordinary group Fourier sample; store the character classically and discard the quantum registers.
4. Pair successive characters and take their differences in $`\widehat G`$.
5. Compute the subgroup generated by these differences and output generators of its annihilator in $`G`$.

Every abort returns a distinguished failure flag. Unused quantum slots can be padded, so the adaptive circuit has a fixed finite maximum workspace. All classical counts and labels have finite ranges.

The following events bound the ideal experiment's failure:

| Event | Probability bound |
|---|---:|
| A spectral eigenvalue lies too near a shifted boundary | $`101/50000`$ |
| A retained band is missing from discovery | $`1/100`$ |
| Any conditioned-copy rejection cap is exhausted | $`1/100`$ |
| Any band rank is declared prematurely | $`1/100`$ |
| Fourier differences fail to generate $`H^\perp`$ | $`1/100`$ |

The first and last lines are Lemma 5 and Theorem 7 of [spectral_reduction.md](spectral_reduction.md). The other lines were proved above. All cap probabilities allow arbitrary preceding measurement histories.

### The global sampler hybrid

At most

```math
N_0+N_W(2rM_g)M_f=T
```

unconditional band-sampler invocations can occur. On a good shift, each physical invocation has classical–quantum output within trace distance $`\xi`$ of its ideal output, and is prepared from fresh independent input copies. Replace the invocations one at a time. Trace-distance contractivity, with all previous retained registers included, bounds the change in the final classical output distribution by

```math
T\xi=1/100.
```

The replacement is made before conditioning on a band label. Consequently the proof does not divide an error by a rare postselection probability, and does not assert that the approximate filtered states have exact finite rank. Wrong labels, small leaked eigenvalues, changed stopping decisions, and all adaptive feedback are included in this one finite hybrid.

After the additional $`1/100`$ compilation budget in Section 7, the total failure probability is at most

```math
\frac{101}{50000}+6\left(\frac1{100}\right)
=\frac{3101}{50000}\lt\frac1{10}.
```

This proves the stated success probability of at least $`2/3`$, with additional slack.

## 7. Copy, gate, memory, and bit accounting

### 7.1 Raw copies

Every unconditional sampler consumes one target copy plus $`n_{\rm prog}`$ program copies. Thus a deterministic worst-case upper bound is

```math
\begin{aligned}
N&\le T(1+n_{\rm prog})\\
&\le T\left(1+hs+\frac{4S^2}{\beta}\right)\\
&=T\left(1+hs+800TS^2\right).
\end{aligned}
```

All rejected and discarded copies are included. A preparation cost attached to each input copy can be multiplied by this bound; it is not treated as free input loading.

The explicit parameter choices imply

```math
\begin{aligned}
N_W&=O(L\varepsilon^{-2}),
&M_g&=\widetilde O(r^2\varepsilon^{-1}),\\
J&=\widetilde O(r^3L\varepsilon^{-3}),
&M_f&=\widetilde O(r\varepsilon^{-1}),\\
T&=\widetilde O(r^4L\varepsilon^{-4}),
&M&=O(r^2\varepsilon^{-1}),\\
h&=O(\log T),
&S&=\widetilde O(r^2\varepsilon^{-1}).
\end{aligned}
```

Substitution gives $`N=\widetilde O(r^{12}L^2\varepsilon^{-10})`$.

### 7.2 A finite compilation budget

Let $`N_P=Tn_{\rm prog}`$ be the worst-case number of partial-SWAP program steps, and set

```math
B_{\rm circ}=1+N_P+Th+4J+(r+2)N_W,
\qquad
\zeta=\frac1{100B_{\rm circ}}.
```

Compile each of the following complete known unitary blocks to normalized diamond error at most $`\zeta`$:

- Each full-register partial-SWAP exponential: at most $`N_P`$ calls.
- Each $`s`$-qubit phase-estimation Fourier transform: at most $`Th`$ calls.
- Each $`W_k`$ or $`W_k^\dagger`$ in growth: at most $`4J`$ calls.
- Each group Fourier transform, including uniform group-state preparation: at most $`2N_W`$ calls.
- Each supplied controlled representation: at most $`rN_W`$ calls, if not exact.

Their total error is at most $`B_{\rm circ}\zeta=1/100`$. State-preparation blocks $`W_k`$ are approximated as full unitaries, because they are also used coherently in the failure correction. Measurements of computational basis bits, Boolean control logic, and the exact Clifford–Toffoli implementation of selected swaps need no continuous rotation approximation.

This is an error allocation for a finite noiseless circuit implementation. It does not assume uncharged arbitrary-precision gates or an unmodeled noisy-device guarantee.

### 7.3 Gate and representation counts

There are at most $`rN_W=O(rL\varepsilon^{-2})`$ controlled-representation calls. The action is applied sequentially to each occupied data register with the same group control. No inverse representation oracle is required.

A growth trial at size $`k`$ can be built with $`O(k(q+\log(k+1)))`$ swap and Boolean-control gates, together with $`O(k\log(k+1))`$ compilable gates for the uniform ancilla unitary. The equality controls can be implemented sequentially, so unbounded fanout is unnecessary. A binary zero-predicate flag is measured while the underlying label ancilla is kept coherent.

One $`s`$-qubit phase-estimation Fourier transform has $`O(s^2)`$ controlled phase rotations. Each DME step has the $`O(q+1)`$ cost described in Section 3.3. For a fixed universal gate set, synthesis adds only powers of the logarithm of the inverse requested error. Thus a direct gate bound, before simplifying, consists of:

```math
\widetilde O\!\left(
N_P(q+1)+Ths^2+Jr(q+\log(r+1))
\right)
+rN_WC_R(\zeta)+2N_WC_F(\zeta).
```

Using the displayed parameter bounds simplifies the first term to $`\widetilde O(N(q+1))`$. The costs of the supplied representation and group transform remain separately charged.

### 7.4 Streaming memory

During tensor preparation, at most $`r`$ data registers are retained. A conditional-copy sampler needs one additional target register and one program register at a time. Its $`h`$ phase-estimation outcomes are measured and stored classically, so only one $`s`$-qubit phase register is needed. The growth ancilla uses $`O(\log(r+1))`$ qubits. After preparing a tensor, Fourier sampling uses an $`O(L)`$-qubit group register. The group and representation routines may require their declared workspaces.

These observations give

```math
O\!\left(rq+L+\log(r/\varepsilon)\right)
+A_R(\zeta)+A_F(\zeta)
```

working qubits. The memory bound does not count a reservoir of all $`N`$ copies: copies arrive as a stream and are consumed. Input preparations must be independent as specified in the model.

### 7.5 Classical bits and computation

The rational shift, grid endpoints, and stopping counters have bit length polynomial in

```math
b_\varepsilon+L+\log(r+1)+\log(1/\varepsilon)+\log N.
```

The grid need not be listed. At most $`r`$ observed band labels are stored, each with $`O(\log(r/\varepsilon))`$ index bits, and a label is computed by rational interval arithmetic. Principal-angle conversion requires only an approximation to $`\pi`$ sufficient for additive error $`a/8`$. Growth rotations and partial-SWAP rotations have explicit classical descriptions and are computed to the prescribed synthesis accuracy.

The median uses $`h`$ finite phase estimates. Character labels have $`O(L)`$ bits. Subgroup and annihilator computations use polynomial-time integer arithmetic on these character labels and the supplied cyclic moduli. There is no $`|G|`$-sized table and no $`d`$-entry state description. Classical bookkeeping, arithmetic, and gate synthesis take time polynomial in the displayed resource counts and encoded bit lengths.

## References used on this page

- **[AS]** Adam Bene Watts, John Bostanci, Matthias C. Caro, Daniel Grier, Sihan Liu, and Gaurav Mahajan, *Anti-symmetrization is cheap and useful*, arXiv:2610.06737v1 (2026), especially Algorithm 1, its failure correction, and Algorithm 2. [Primary manuscript](https://arxiv.org/html/2610.06737v1).
- **[DME]** Byeongseon Go, Hyukjoon Kwon, Siheon Park, Dhrumil Patel, and Mark M. Wilde, *Sample-based Hamiltonian and Lindbladian simulation: Non-asymptotic analysis of sample complexity*, arXiv:2412.02134v3 (2025), especially the diamond-distance DME bound and Appendix E. [Primary manuscript](https://arxiv.org/html/2412.02134v3).
- **[HS]** Isaac Holt and Sathyawageeswar Subramanian, *Learning quantum symmetries*, arXiv:2609.38085v2 (2026). [Primary manuscript](https://pdfs.assets.alphaxiv.org/2609.38085v2.pdf).
