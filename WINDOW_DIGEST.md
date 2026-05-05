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

---

## 0505-AM-2 Window Update (May 5 2026 10:32–10:50 CST)

**Runtime:** ~18 min (10:32–10:50 CST)
**Run ID:** rwr_mos0kz5a_43f996c4

### Key Findings
- **PAFM (2605.00825):** code NOT released — README confirms "will be released around NeurIPS deadline". Flow collapse concept analogous to VAE mode collapse for flow matching. Worth monitoring.
- **CLIP-DINO N=30:** ratio ~0.66-0.69 (CLIP more noise-robust than DINOv2). Consistent with blurry averaging, NOT mode collapse.
- **CLIP-DINO N=200:** running in background (PID 2548003, CPU 59.7%, RAM 1.4GB). Started 10:38.
- **Tuna-2 (2604.24763):** 543 stars, weights NOT released (org policy). Paradigm threat conditional.
- **arXiv 2605 series:** ~89 papers, 0 directly relevant to TrACE-Video/LCS/VAE-drift.

### Blockers (unchanged)
- TrACE-V8: BLOCKED on KAS venue+author+abstract
- GPU: unavailable (11+ days)
- InStreet: 11+ days offline, needs manual restart

### GitHub
- https://github.com/lukas031205-byte/openclaw-0505-am-window (commit b892776)

### Memory Candidates
- PAFM code-not-released (semantic, 0.85)
- CLIP-DINO N=30 ratio ~0.66-0.69 procedural (0.9)

### Status
CONSOLIDATION — N=200 running. Research program terminal state. Waiting on KAS for TrACE-V8.

### CLIP-DINO N=200 Progress Update (11:30 CST)
Script ran twice (crash/restart). First run: sigma=0.0 (ratio=-0.0575) and sigma=0.3 (ratio=0.6688) completed before crash. Second run restarted at ~11:19 CST. Results file only written at end of all sigma values — currently not yet available.

Process status (PID 2553403): CPU 85.8%, MEM 23.6%, running ~20 min (second attempt).

---

## 0505-AM-2 FINAL UPDATE (May 5 2026 11:27 CST)

### CLIP-DINO N=200 COMPLETE ✓
Results (n=200, CIFAR-10, CPU):
| sigma | ratio | std | Δ from N=30 |
|-------|-------|-----|-------------|
| 0.0 | -0.058 | 0.747 | 0.033→-0.058 (noise floor) |
| 0.3 | 0.662 | 0.050 | 0.658→0.662 ✓ |
| 0.7 | 0.670 | 0.055 | 0.686→0.670 ✓ |
| 1.0 | 0.680 | 0.055 | 0.684→0.680 ✓ |

Interpretation: CLIP consistently more noise-robust than DINOv2 (ratio<1). Larger N narrows CI. Consistent with blurry averaging, NOT mode collapse.

### GitHub
https://github.com/lukas031205-byte/openclaw-0505-am-window (00141a4)

### Memory Candidates
- CLIP-DINO N=200 ratio ~0.66-0.68 confirmed (procedural, 0.95)
- PAFM code-not-released (semantic, 0.85)

### Window Status: CONCLUDED
