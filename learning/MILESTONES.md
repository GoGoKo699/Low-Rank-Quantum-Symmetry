# Project understanding map: 30 milestones

This map follows one question: how can independent copies reveal the entire conjugation-symmetry subgroup of an unknown low-rank mixed state, even when its eigenvalues have no supplied gap? The targets are defined by the science and shared by every reader. They do not record a particular learner's assessment or progress.

The allocation is **11 background/preliminaries milestones** and **19 narrative/innovation milestones**. The background assembles states, operational distance, spectral subspaces, phase information and finite abelian characters into the complete access model. The narrative follows the spectrum-to-band-wedge reduction, its paid finite implementation, subgroup recovery and the resulting boundaries. More space goes to the narrative because mathematical encoding, physical preparation and inference are separate parts of the guarantee.

The single educational anchor is **John Watrous, The Theory of Quantum Information**. The [Watrous bridge](WATROUS_BRIDGE.md) specifies the source version and relevant sections, translates notation and supplies connections that the textbook does not teach. The linked scientific pages own exact statements, proofs and resource constants.

## Route through the project

| Phase | Milestones | Connection established |
|---|---|---|
| Background/preliminaries | M01–M04 | Independent states, their conjugation symmetries, supplied actions and operational separation |
| Background/preliminaries | M05–M08 | Physical measurement records, spectral subspaces, exterior powers and projective phases |
| Background/preliminaries | M09–M11 | Character information and finite error accounting joined into the full task |
| Narrative/innovation | M12–M17 | The support obstruction, coarse bands, an overlap gap and resolvable random boundaries |
| Narrative/innovation | M18–M23 | Paid spectral sampling, band discovery, valid streaming growth and a global finite hybrid |
| Narrative/innovation | M24–M26 | Fourier differences, subgroup generators and the complete resource account |
| Narrative/innovation | M27–M30 | Channel covariance, metric limits, attribution and the integrated scientific conclusion |

## Phase I: background/preliminaries

### M01 States and independent copies

**Central question.** What does the source supply when it supplies a copy?

**Understanding target.** Interpret a density operator as a positive trace-one matrix, distinguish a pure vector from its density operator, and interpret repeated input as independent preparations of the same unknown state. Explain why a supply of specimens is weaker access than a known preparation circuit and its inverse.

**Dependencies and story role.** None within this map. This fixes the physical input before any spectral procedure is proposed.

**Conceptual connection.** A matrix can be used in a proof without being given to the algorithm as a classical array. Independence licenses tensor-product source states; correlations would change that model.

**Source pointers.** Watrous §§2.1.2–2.1.3; [inputs and access](../science/model.md#1-inputs-and-access); [bridge: input and notation](WATROUS_BRIDGE.md#input-and-notation).

### M02 Rank, support and conjugation invariance

**Central question.** What exactly is a symmetry of a mixed state?

**Understanding target.** Define the support and rank of a density operator and explain the condition that a known unitary leaves the operator unchanged by conjugation. Distinguish preservation of the occupied subspace from preservation of all eigenvalue-weighted information inside it.

**Dependencies and story role.** M01. This identifies the unknown object the algorithm must learn, rather than a surrogate property of its support.

**Conceptual connection.** A degenerate eigenspace may rotate without changing the density operator; two states with the same support can have different conjugation symmetries.

**Source pointers.** Watrous §1.1.3 and §2.1.2; [symmetry promise and output](../science/model.md#2-symmetry-promise-and-output); [support example](../science/examples_and_channels.md#a-whole-support-wedge-can-return-the-wrong-subgroup).

### M03 A supplied group and its controlled action

**Central question.** How can the algorithm ask about many transformations coherently?

**Understanding target.** Interpret a finite abelian group supplied in cyclic coordinates and a linear unitary representation that respects its multiplication. Explain what a controlled group action does to a superposition of group labels, and distinguish a compact group description from an enumeration of its elements.

**Dependencies and story role.** M01–M02. This introduces the promised computational access that later makes group learning possible.

**Conceptual connection.** Knowing an abstract group does not supply an efficient action circuit. Its implementation and Fourier circuits remain charged inputs.

**Source pointers.** Watrous §§1.1.1–1.1.2 and §2.2.1 for the linear-algebra/channel language; [access model](../science/model.md#1-inputs-and-access); [bridge: characters and group access](WATROUS_BRIDGE.md#characters-and-group-access).

### M04 Operational distance and the exact-or-separated promise

**Central question.** How can a finite experiment identify an exact property?

**Understanding target.** Interpret half the trace norm as an operational distance and explain the promised alternative: a group element fixes the state exactly or moves it by at least the supplied positive separation. Distinguish this promise from a gap between eigenvalues.

**Dependencies and story role.** M01–M03. This supplies the accuracy scale that makes the exact output contract finite.

**Conceptual connection.** Exact equality without separation cannot be uniformly resolved from finitely many specimens. Arbitrary approximate-invariance sets need not form subgroups.

**Source pointers.** Watrous §§1.1.3 and 3.1.1; [promise](../science/model.md#2-symmetry-promise-and-output); [approximate-set example](../science/examples_and_channels.md#why-the-exact-separation-promise-matters).

### M05 Measurements with retained and discarded information

**Central question.** Why does a measurement's classical record matter to the remaining quantum state?

**Understanding target.** Distinguish measurement probabilities from a complete physical instrument, including the state left after each outcome. Explain why a binary predicate measurement can preserve coherence that is lost when the underlying labels are measured individually.

**Dependencies and story role.** M01 and M04. This prepares the reader to evaluate the growth procedure's success and failure branches.

**Conceptual connection.** Equal success probabilities alone do not establish equal adaptive algorithms: the state retained after failure affects all later trials.

**Source pointers.** Watrous §§2.2.1–2.2.2 and 2.3.1–2.3.2; [physical growth instrument](../science/copy_algorithm.md#lemma-1-exact-physical-instrument); [verification negative controls](../verification/README.md#why-the-physical-growth-negative-controls-matter).

### M06 Spectral projectors rather than an eigenbasis description

**Central question.** Which spectral information is intrinsic when eigenvectors are not unique?

**Understanding target.** Interpret a spectral decomposition as orthogonal projectors weighted by eigenvalues. Explain why collecting nearby eigenvalues into a band defines a subspace even if no individual eigenvector is learned classically, and why an exact conjugation symmetry preserves every such band.

**Dependencies and story role.** M01–M02. This changes the target representation from an eigenbasis to a small family of invariant subspaces.

**Conceptual connection.** Basis freedom inside a degenerate eigenspace motivates a basis-independent quantum encoding of each retained subspace.

**Source pointers.** Watrous §1.1.3; [coarse bands](../science/spectral_reduction.md#2-coarse-spectral-bands-preserve-the-exact-promised-subgroup); [bridge: why bands retain the answer](WATROUS_BRIDGE.md#why-bands-retain-the-answer).

### M07 Exterior powers encode a subspace up to phase

**Central question.** Can a pure quantum state describe a whole subspace without choosing a preferred basis?

**Understanding target.** Interpret the antisymmetric tensor of an orthonormal basis of a rank-sized subspace. Explain why a basis change multiplies the top wedge by a determinant phase and therefore leaves its density operator unchanged.

**Dependencies and story role.** M01 and M06. This supplies the pure-state representation that will carry mixed-state spectral information.

**Conceptual connection.** Permutations of registers and the physical symmetry group are different actions. Antisymmetry under register permutations is a construction tool, not the symmetry subgroup being learned.

**Source pointers.** Watrous §7.1.1 for tensor-factor permutation operators; the signed exterior-power construction is supplied locally in [the wedge definition and overlap lemma](../science/spectral_reduction.md#3-a-pure-state-encoding-all-retained-spectral-subspaces) and [bridge](WATROUS_BRIDGE.md#exterior-powers-and-the-overlap-gap).

### M08 Global phases and three different symmetry conditions

**Central question.** Which phase information should a symmetry learner ignore?

**Understanding target.** Distinguish a pure vector fixed literally, a pure density operator fixed up to vector phase, and a mixed density operator fixed by conjugation. Explain why requiring one common phase on the entire mixed-state support is stronger than ordinary conjugation invariance.

**Dependencies and story role.** M02 and M07. This identifies both the existing pure-state primitive and the mixed-state task to which it must be reduced.

**Conceptual connection.** A projective stabilizer of a constructed pure state can encode the desired conjugation subgroup, even though a direct strong-symmetry test on the original mixed state may miss it.

**Source pointers.** Watrous §2.1.2 and §3.2.1; [strong-symmetry counterexample](../science/examples_and_channels.md#a-strong-mixed-state-symmetry-condition-can-miss-exact-symmetries); [related-work boundary](../references/related_work.md#the-precise-contribution-boundary).

### M09 Characters and annihilators

**Central question.** What kind of Fourier information identifies a subgroup?

**Understanding target.** Interpret a character as a phase-valued homomorphism and an annihilator as the characters trivial on a subgroup. Explain how character labels are stored in the supplied cyclic coordinates and how taking an annihilator translates a dual-group description back into the original group.

**Dependencies and story role.** M03 and M08. This supplies the classical meaning of the later quantum measurement outcomes.

**Conceptual connection.** The Fourier step outputs character labels, rather than group elements known to be symmetries. Recovering the original subgroup requires the duality step.

**Source pointers.** The finite abelian material is supplied locally rather than attributed to Watrous: [Fourier recovery](../science/spectral_reduction.md#5-fourier-differences-recover-the-subgroup); [bridge](WATROUS_BRIDGE.md#characters-and-group-access).

### M10 Finite experiments and composable approximation

**Central question.** How can approximate physical operations support an exact promised answer?

**Understanding target.** Explain a hybrid argument that replaces finitely many approximate state sources one at a time and adds their trace-distance errors. Distinguish a bound on an unconditional source from a bound asserted only after rare postselection, and recognize why deterministic call caps matter.

**Dependencies and story role.** M04–M05. This establishes the proof architecture for approximation and adaptive stopping.

**Conceptual connection.** The ideal mathematical bands may have exact rank while physical outputs leak outside them. Comparing the complete finite experiments avoids assigning exact rank to a noisy output.

**Source pointers.** Watrous §§3.1.1 and 3.3.2–3.3.3; [global sampler hybrid](../science/copy_algorithm.md#the-global-sampler-hybrid); [bridge: physical approximation](WATROUS_BRIDGE.md#physical-approximation-and-finite-stopping).

### M11 The complete operational question

**Central question.** Which assumptions and costs must be joined before the theorem can be interpreted?

**Understanding target.** State the input, exact-or-separated promise, classical subgroup-generator output and constant success requirement together. Explain the distinct roles of rank, separation, group-description length and system size, including paid copies and supplied action circuits.

**Dependencies and story role.** M01–M10. This is the background phase's global synthesis.

**Conceptual connection.** Polynomial cost in rank and logarithmic dimension is useful for low-rank many-qubit states; it does not imply polynomial cost for unrestricted-rank states or free preparation.

**Source pointers.** [Model and theorem](../science/model.md); [interpretation](../science/interpretation.md); [bridge: input and notation](WATROUS_BRIDGE.md#input-and-notation).

## Phase II: narrative/innovation

### M12 Why the whole-support wedge loses the answer

**Central question.** Why is the inherited support encoding insufficient for a nonflat state?

**Understanding target.** Follow the rank-two example with unequal diagonal weights and a swap action. Explain why the density operator changes while its whole-support wedge changes only by phase, and how separating the two spectral bands restores the distinction.

**Dependencies and story role.** M02, M07–M08 and M11. This isolates the scientific obstruction before introducing the repair.

**Conceptual connection.** A basis-independent representation can still discard information relevant to the task. The missing information is the association between spectral weights and subspaces.

**Source pointers.** [Support counterexample](../science/examples_and_channels.md#a-whole-support-wedge-can-return-the-wrong-subgroup); [worked bridge example](WATROUS_BRIDGE.md#a-complete-two-dimensional-example).

### M13 Low rank controls discarded and rounded mass

**Central question.** How much spectral information can be removed safely?

**Understanding target.** Explain the two contributions to rounding error: discarding eigenvalues below the threshold and moving retained values to band midpoints. Use the number of positive eigenvalues, rather than the ambient dimension, to see why the normalized rounded state remains close to the input.

**Dependencies and story role.** M04, M06 and M12. This gives the approximation estimate that powers the reduction.

**Conceptual connection.** Arbitrarily tiny positive eigenvalues are allowed because their total mass is controlled by rank and threshold; they do not determine the algorithm's resolution.

**Source pointers.** [Rounding lemma](../science/spectral_reduction.md#lemma-1-rounding-error); [bridge: why bands retain the answer](WATROUS_BRIDGE.md#why-bands-retain-the-answer).

### M14 A coarse state preserves the exact subgroup

**Central question.** Why does a small rounding error preserve an exact answer?

**Understanding target.** Join the triangle inequality with the separation promise: an element fixing the rounded state moves the original by less than the promised nonsymmetry gap. Explain both subgroup inclusions and why distinct retained band weights turn invariance of the rounded state into preservation of every retained projector.

**Dependencies and story role.** M02, M04 and M13. This is the exact-answer step of the spectrum-to-subspaces reduction.

**Conceptual connection.** The promise protects the requested subgroup while allowing spectral approximation. It does not claim that nearby density operators generally have identical symmetry groups.

**Source pointers.** [Exact subgroup preservation](../science/spectral_reduction.md#lemma-2-exact-subgroup-preservation); [scope](../science/model.md#5-perturbations-and-scope).

### M15 Determinants convert subspace motion into overlap loss

**Central question.** How does a transformed band change its wedge state?

**Understanding target.** Interpret principal angles between a subspace and its image. Explain why the wedge overlap is a determinant whose squared magnitude is the product of squared cosines, while the projector trace distance is the sum of sines.

**Dependencies and story role.** M04 and M07. This connects an operator-distance promise to a pure-state measurement statistic.

**Conceptual connection.** A preserved subspace can have a nontrivial internal rotation and determinant phase. Unit-modulus wedge overlap recognizes that freedom without selecting an eigenbasis.

**Source pointers.** Watrous §1.1.3 for singular values and norms; [wedge overlap lemma](../science/spectral_reduction.md#lemma-3-wedge-overlap-and-principal-angles); [bridge](WATROUS_BRIDGE.md#exterior-powers-and-the-overlap-gap).

### M16 The tensor of band wedges has the right gap

**Central question.** Why is the encoded pure-state gap independent of the ambient dimension?

**Understanding target.** Join the rounded-state distance estimate, normalized band weights and principal-angle identities to obtain overlap loss of order the squared separation. Explain why unit overlap in every factor is equivalent to preservation of all retained bands and hence membership in the true subgroup.

**Dependencies and story role.** M14–M15. This completes the central mathematical encoding before its preparation cost is considered.

**Conceptual connection.** The tensor keeps spectral bands distinct, and normalization removes an unnecessary ambient-dimension factor from the overlap-gap argument.

**Source pointers.** [Dimension-independent projective gap](../science/spectral_reduction.md#theorem-4-dimension-independent-projective-symmetry-gap); [bridge](WATROUS_BRIDGE.md#exterior-powers-and-the-overlap-gap).

### M17 Random boundaries replace an input eigengap

**Central question.** How can spectral labels be resolved when eigenvalues may be arbitrarily close?

**Understanding target.** Explain why a finite random grid shift places every positive input eigenvalue away from relevant band boundaries with high probability. Distinguish separation from a chosen measurement boundary from separation between eigenvalues, and distinguish the role of randomization from exact subgroup preservation, which holds for every shift.

**Dependencies and story role.** M06 and M13–M16. This connects the mathematical bands to finite-resolution implementation.

**Conceptual connection.** The union bound ranges over at most the rank-many positive eigenvalues; nearby eigenvalues may safely share one band.

**Source pointers.** Watrous §1.2.2 for probability language; [finite random shift](../science/spectral_reduction.md#4-a-finite-random-shift-creates-resolvable-boundaries); [bridge: source construction](WATROUS_BRIDGE.md#constructing-the-band-source-from-paid-copies).

### M18 Copies implement controlled spectral evolution

**Central question.** Where does the Hamiltonian needed for spectral labeling come from?

**Understanding target.** Explain density-matrix exponentiation using fresh program copies and full-register partial swaps. Follow the extension with a known control qubit to obtain controlled evolution and understand why its simulation error must remain valid when the control is entangled with other registers.

**Dependencies and story role.** M01, M03, M05 and M10. This supplies paid access to the unknown spectrum without a preparation inverse.

**Conceptual connection.** Constructing a controlled evolution from copies of a known extension is a different access claim from controlling an unknown unitary oracle. Exponentiating a whole-register swap is not a product of independent bit-swap exponentials.

**Source pointers.** Watrous §§2.2.1–2.2.2 and 3.3.2 for channel language; [controlled DME](../science/copy_algorithm.md#32-controlled-density-matrix-exponentiation-is-charged); [full partial swap](../science/copy_algorithm.md#33-implementing-a-full-partial-swap); [DME attribution](../references/related_work.md#gkppw25).

### M19 A band sampler is an unconditional state source

**Central question.** What does the spectral measurement actually guarantee?

**Understanding target.** Describe a source output containing a classical band or tail label and its quantum target. Explain why repeated phase estimation and a median classify an input eigenstate correctly away from boundaries, and why the proved approximation concerns this source on input copies rather than an arbitrary-target ideal measurement channel.

**Dependencies and story role.** M05, M10 and M17–M18. This identifies the exact object that will be replaced in the global error argument.

**Conceptual connection.** A state-source guarantee can be sufficient for an algorithm while being weaker than a diamond-norm approximation to a general measurement channel.

**Source pointers.** [Unconditional band sampler](../science/copy_algorithm.md#3-an-unconditional-band-sampler); [phase estimation](../science/copy_algorithm.md#31-high-confidence-phase-estimation); [bridge](WATROUS_BRIDGE.md#constructing-the-band-source-from-paid-copies).

### M20 Discovering bands and paying for rejection

**Central question.** How can the algorithm find unknown occupied bands and obtain copies from one chosen band?

**Understanding target.** Explain why every retained ideal band has a known minimum source probability, so bounded sampling discovers it and capped rejection produces conditional copies. Distinguish a lower bound on the conditioned band's eigenvalues from an assumed lower bound on the original state's smallest positive eigenvalue.

**Dependencies and story role.** M13 and M19. This makes band access finite and explicitly paid.

**Conceptual connection.** Both discarded labels and rejected copies count. The conditional state belongs to a chosen ideal band, while physical leakage is controlled later through unconditional sources.

**Source pointers.** [Discovery and conditioning](../science/copy_algorithm.md#4-discovering-bands-and-requesting-conditional-copies); [finite parameters](../science/copy_algorithm.md#2-all-finite-parameters).

### M21 A failed growth attempt must preserve the invariant

**Central question.** How can antisymmetric growth continue after a failure?

**Understanding target.** Follow the coherent label circuit, binary zero test and second unitary on failure. Explain why the resulting success and failure operators preserve antisymmetry of the retained registers, and why measuring individual nonzero labels or omitting the correction changes the instrument.

**Dependencies and story role.** M05, M07 and M20. This establishes the physical invariant needed for repeated growth trials.

**Conceptual connection.** The retained state may change after failure; what is preserved is its membership in the relevant exterior-power subspace, which is enough for the next probability bound.

**Source pointers.** [Growth instrument](../science/copy_algorithm.md#5-antisymmetric-growth-with-a-valid-failure-branch); [exact physical lemma](../science/copy_algorithm.md#lemma-1-exact-physical-instrument); [inherited primitive](../references/related_work.md#bwbcglm26).

### M22 Unknown band rank can be learned by bounded stopping

**Central question.** How can growth stop correctly without being told a band's rank?

**Understanding target.** Explain the uniform lower bound on growth probability below the true rank and the zero growth probability at full rank. Use repeated-failure stopping, finite stage counts and a union bound to see why premature declarations are unlikely while every branch has a deterministic cap.

**Dependencies and story role.** M20–M21. This turns streaming antisymmetrization into a finite preparation routine for unknown bands.

**Conceptual connection.** Conditional success probabilities can be bounded after arbitrary earlier failures without assuming those trials are independent or that the retained state stayed unchanged.

**Source pointers.** [Growth probability](../science/copy_algorithm.md#lemma-2-a-uniform-growth-probability-below-the-true-rank); [unknown-rank stopping](../science/copy_algorithm.md#unknown-rank-stopping-rule).

### M23 One finite hybrid covers leakage and adaptive decisions

**Central question.** Why do small band-sampling errors not invalidate rank stopping?

**Understanding target.** Explain the replacement of each unconditional sampler in the complete capped experiment, including wrong labels, rejections, aborts and feedback. Identify the total sampler count and accuracy allocation that bound the final distributional error without dividing by a postselection probability.

**Dependencies and story role.** M10 and M19–M22. This closes the physical preparation proof with the mathematical ideal preparation.

**Conceptual connection.** Exact rank is used only in the ideal experiment. The physical experiment is controlled by its total distance from that experiment, together with a separate finite gate-compilation budget.

**Source pointers.** [Global sampler hybrid](../science/copy_algorithm.md#the-global-sampler-hybrid); [compilation budget](../science/copy_algorithm.md#72-a-finite-compilation-budget); [bridge](WATROUS_BRIDGE.md#physical-approximation-and-finite-stopping).

### M24 Fourier differences cancel the unknown stabilizer phase

**Central question.** Why does the algorithm subtract two character outcomes?

**Understanding target.** Explain why ordinary character samples of the band-wedge tensor lie in a coset determined by its phase character on the stabilizer. Taking differences cancels that unknown character and gives samples supported on the annihilator of the desired subgroup.

**Dependencies and story role.** M08–M09 and M16. This converts the projective encoding into classical subgroup information.

**Conceptual connection.** The difference distribution has a Fourier coefficient equal to squared overlap. Its support property uses exact ideal symmetries, while its escape probability uses the quantitative nonsymmetry gap.

**Source pointers.** [Fourier differences](../science/spectral_reduction.md#5-fourier-differences-recover-the-subgroup); [support and escape lemma](../science/spectral_reduction.md#lemma-6-support-and-escape-probability); [bridge](WATROUS_BRIDGE.md#characters-and-group-access).

### M25 Escape probability gives the entire subgroup

**Central question.** Why do a logarithmic number of successful enlargements suffice?

**Understanding target.** Explain why samples escape any proper subgroup of the annihilator with a probability controlled by the overlap gap. Connect subgroup-size doubling, a finite sample budget and classical annihilator computation to recovery of generators of the entire original subgroup.

**Dependencies and story role.** M09, M23–M24. This completes the exact output and success guarantee.

**Conceptual connection.** Merely observing some compatible characters does not certify completeness. The escape argument supplies that guarantee without enumerating the ambient group.

**Source pointers.** [Finite Fourier recovery](../science/spectral_reduction.md#theorem-7-finite-fourier-recovery); [full algorithm and success](../science/copy_algorithm.md#6-full-algorithm-and-success-probability).

### M26 Joining copies, action calls, gates and memory

**Central question.** Which cost is saved, and which cost remains large?

**Understanding target.** Trace the nested sampler, rejection, growth and Fourier budgets to the conservative copy polynomial. Distinguish raw copies, controlled-action calls, supplied-circuit gate cost, active streaming memory and output size. Explain why a dimension-independent copy bound does not make state preparation or controlled access free.

**Dependencies and story role.** M11, M18–M25. This is the complete implementation resource synthesis.

**Conceptual connection.** Polynomial dependence on rank can be exponential in qubit count when rank is large. The established copy exponents are upper bounds and need not be practically small or optimal.

**Source pointers.** [Resource accounting](../science/model.md#4-resource-accounting); [copy, gate, memory and bit accounting](../science/copy_algorithm.md#7-copy-gate-memory-and-bit-accounting); [bridge: resource interpretation](WATROUS_BRIDGE.md#resource-interpretation).

### M27 Channel covariance becomes state conjugation symmetry

**Central question.** What does the state theorem imply for a low-Kraus-rank channel?

**Understanding target.** Construct the normalized Choi state using one channel invocation and a maximally entangled input. Explain the conjugate-input/output representation, covariance equivalence and equality of minimal Kraus rank with Choi rank, retaining the stated access and metric assumptions.

**Dependencies and story role.** M01–M04 and M25–M26. This applies the completed state theorem to a concrete neighboring task.

**Conceptual connection.** Known gate descriptions permit a charged conjugated input action; access to an unknown unitary alone does not automatically provide its complex conjugate. Every DME program copy becomes another charged channel invocation.

**Source pointers.** Watrous §§2.2.1–2.2.2; [channel covariance reduction](../science/examples_and_channels.md#channel-covariance-from-low-kraus-rank); [bridge: Choi normalization](WATROUS_BRIDGE.md#normalized-choi-states-and-the-channel-boundary).

### M28 A channel metric change can destroy the useful gap

**Central question.** Why is a constant diamond-distance violation insufficient for this corollary?

**Understanding target.** Interpret the rank-one channel counterexample in which a transformation has constant diamond-distance violation but a normalized-Choi distance that vanishes with dimension. Explain why this blocks substituting the promise in the resource theorem, without proving impossibility for other channel-learning strategies.

**Dependencies and story role.** M04, M26–M27. This protects the exact scope of the application.

**Conceptual connection.** A maximally entangled probe averages input directions; optimal channel discrimination can select a direction that this average underweights. Low Choi rank alone does not remove this difference.

**Source pointers.** Watrous §§3.3.1–3.3.3; [Choi-versus-diamond example](../science/examples_and_channels.md#a-diamond-gap-need-not-provide-a-usable-choi-gap); [verification explanation](../verification/README.md#the-choi-versus-diamond-counterexample).

### M29 Attribution, necessary rank dependence and verification limits

**Central question.** Which part is established here, and how strong is the supporting evidence?

**Understanding target.** Identify the inherited spectral-simulation, antisymmetric-growth and Fourier primitives and the spectrum-to-band-wedge composition established here. Follow the mixedness-testing reduction that forces rank dependence, and distinguish analytical proof, finite diagnostic checks, a conservative upper bound and an unmatched lower bound.

**Dependencies and story role.** M12–M28. This integrates provenance and evidence before drawing the scientific conclusion.

**Conceptual connection.** A check of small examples can expose a physical-instrument error but cannot prove the general asymptotic theorem. An inherited lower bound does not establish optimality of the displayed copy polynomial.

**Source pointers.** [Related work and module ledger](../references/related_work.md); [rank lower bound](../science/examples_and_channels.md#rank-dependence-is-necessary); [verification scope](../verification/README.md#interpretation-limits).

### M30 The complete scientific story

**Central question.** What does low rank make possible, and why does the mechanism work?

**Understanding target.** Explain the whole chain: the support obstruction; promise-protected coarse spectral bands; a tensor of basis-independent wedges; paid finite preparation; phase cancellation and annihilator recovery; and the complete resource and error accounting. State the meaningful reach for low-rank states and the boundaries for approximate symmetry, arbitrary nonabelian groups, input noise and channel metrics.

**Dependencies and story role.** M01–M29. This is the narrative phase's global synthesis and the final understanding target.

**Conceptual connection.** The contribution is learning an entire exact conjugation subgroup from low-rank mixed-state specimens with arbitrary spectrum. The result does not require tomography, an input eigengap or an eigenbasis description, and its usefulness still depends on the declared source and circuit access.

**Source pointers.** [Model and theorem](../science/model.md); [scientific overview](../science/README.md); [interpretation](../science/interpretation.md); [bridge](WATROUS_BRIDGE.md).
