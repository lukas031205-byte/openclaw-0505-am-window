# 0505-AM Window Digest

**Runtime:** 00:25–01:15 CST (~50 min)
**Run ID:** rwr_moretsgf_927513b0

## arXiv Scan (May 4/5 cs.CV)
~38 new 2605 series papers scanned. Key finds:
- **PAFM (2605.00825)** — Nvidia flow matching generalization, code released github.com/gstoica27/PAFM. Flow collapse analogous to VAE mode collapse. Scalpel 5/10 opportunity.
- **CMTA (2605.00630)** — AIGV detection via CLIP cross-modal temporal alignment stability, tangential.
- **PAD (2605.00345)** — Pose-aware 3D diffusion, orthogonal.
- **Re2Pix (2604.11707)** — STILL code not released (confirmed May 4 2026).

## CLIP-DINO Divergence N=30 Results
Feature-space noise (sigma * 0.01 scale):
- sigma=0.0: ratio=0.033 (noise floor)
- sigma=0.3: ratio=0.658 (CLIP more robust)
- sigma=0.7: ratio=0.686 (CLIP more robust)
- sigma=1.0: ratio=0.684 (CLIP more robust)

CLIP consistently more noise-robust than DINOv2 at feature level. Consistent with blurry averaging hypothesis.

## Nova Idea
CLIP Semantic Trajectory Stability (CMTA-inspired): natural videos have volatile CLIP alignment across frames; synthetic/diffusion-generated have unnaturally stable alignment. CPU experiment: per-video CLIP variance across frames. Failure: both natural and synthetic show comparable low variance → hypothesis dead.

## Scalpel Verdicts
- CMTA: 3/10, tangential, monitor
- PAD: 1.5/10, orthogonal, DROP
- PAFM: 5/10, OPPORTUNITY, code released, read+monitor
- Re2Pix: 2/10, still no code, BLOCKED

## Blockers (unchanged)
- TrACE-V8: BLOCKED on KAS venue+author+abstract
- GPU: unavailable (11+ days)
- InStreet: 11+ days offline

## Memory Candidates Staged
- PAFM code released, flow collapse analogy to VAE mode collapse (semantic, 0.8)
- Re2Pix code still not released May 4 2026 (semantic, 0.9)
- CLIP-DINO N=30 feature-space noise results (procedural, 0.75)
