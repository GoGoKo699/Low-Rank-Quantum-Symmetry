# Scientific account

The task is to learn which transformations in a known finite abelian group leave an unknown low-rank mixed state unchanged. The input consists of independent copies, a rank upper bound, a controlled linear representation, and a trace-distance separation between exact symmetries and every alternative. The output is generators of the complete exact subgroup.

A mixed state's support does not determine this subgroup. The central reduction retains coarse spectral bands, encodes each band as a pure exterior-power state, and passes their tensor product to an existing phase-insensitive Fourier method. Random boundaries and a finite copy-based implementation avoid assumptions about input eigenvalue gaps or the smallest nonzero eigenvalue.

## Reading order

1. [Model and guarantees](model.md) defines the access model, promise, output and resource theorem.
2. [Spectral reduction](spectral_reduction.md) proves exact subgroup preservation, the wedge-overlap gap, the random-boundary bound and finite Fourier recovery.
3. [Finite copy algorithm](copy_algorithm.md) implements the reduction, including unknown band ranks, coherent failure recovery, bounded stopping, approximation and all paid resources.
4. [Examples and channels](examples_and_channels.md) distinguishes support, strong and conjugation symmetries; proves the channel corollary; and records a metric limitation and inherited lower bound.
5. [Interpretation](interpretation.md) connects the mechanism to the learning capability and remaining questions.

## Proof dependencies

The exact subgroup theorem first uses a trace-distance rounding estimate. The principal-angle bound then turns that estimate into a squared-overlap gap for a tensor of pure states. Fourier differences recover the annihilator of the subgroup from this gap.

The implementation proof is separate from that geometric reduction. It constructs unconditional spectral-band samplers from paid copies, proves the correct physical growth instrument, and bounds rank discovery and every stopping rule. A hybrid over a fixed finite number of unconditional samples controls the complete adaptive experiment, including erroneous and aborting branches.

The [related-work comparison](../references/related_work.md) pins the inherited sampling, antisymmetrization and simulation results and distinguishes the present theorem from nearby tasks. The [finite checks](../verification/README.md) probe selected identities and implementation mistakes; they do not replace the general proofs.

Each theorem has one authoritative proof location. The top-level [README](../README.md) and [LLM guide](../llms.txt) are navigation routes.
