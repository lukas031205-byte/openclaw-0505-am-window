#!/usr/bin/env python3
"""CLIP-DINO Divergence full experiment — N=30, sigma in {0.0, 0.3, 0.7, 1.0}"""
import sys
sys.path.insert(0, '/home/kas/.openclaw/workspace-domain/research/0504-pm-window')
import torch
import clip
import json
import numpy as np
from torchvision import datasets

device = 'cpu'
print('Loading CLIP...', flush=True)
clip_model, clip_preprocess = clip.load('ViT-B/32', device=device)
clip_model.eval()
print('Loading DINOv2...', flush=True)
dinov2 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14')
dinov2.eval()
dinov2.to(device)
print('OK', flush=True)

# Load CIFAR-10
cifar = datasets.CIFAR10(root='/tmp/cifar10', train=False, download=True)
images = [cifar[i][0] for i in range(200)]
print(f'N={len(images)}', flush=True)

results = {}
for sigma in [0.0, 0.3, 0.7, 1.0]:
    d_clip, d_dino, ratios = [], [], []
    for img in images:
        clip_t = clip_preprocess(img).unsqueeze(0).to(device)
        pil = img.resize((224, 224))
        dino_t = torch.from_numpy(np.array(pil)).permute(2,0,1).float().unsqueeze(0) / 255.0
        dino_t = torch.nn.functional.interpolate(dino_t, size=(224, 224), mode='bilinear')
        dino_norm = (dino_t - 0.45) / 0.22

        with torch.no_grad():
            fc = clip_model.encode_image(clip_t)
            fc = fc / fc.norm(dim=-1, keepdim=True)
            fd = dinov2(dino_norm.to(device))
            fd = fd / fd.norm(dim=-1, keepdim=True)

            # Feature-space Gaussian noise (sigma in cosine space)
            scale = sigma * 0.01  # scale noise relative to unit features
            clip_noisy = (fc + torch.randn_like(fc) * scale)
            clip_noisy = clip_noisy / clip_noisy.norm(dim=-1, keepdim=True)
            dino_noisy = (fd + torch.randn_like(fd) * scale)
            dino_noisy = dino_noisy / dino_noisy.norm(dim=-1, keepdim=True)

            dc = (1 - (fc * clip_noisy).sum(-1).item()) * 180 / np.pi
            dd = (1 - (fd * dino_noisy).sum(-1).item()) * 180 / np.pi
            d_clip.append(dc)
            d_dino.append(dd)
            ratios.append(dc / dd if dd > 1e-6 else 0)

    print(f'sigma={sigma}: clip={np.mean(d_clip):.3f}, dino={np.mean(d_dino):.3f}, ratio={np.mean(ratios):.4f}', flush=True)
    results[f'sigma_{sigma}'] = {
        'mean_deg_clip': float(np.mean(d_clip)),
        'mean_deg_dino': float(np.mean(d_dino)),
        'mean_ratio': float(np.mean(ratios)),
        'std_ratio': float(np.std(ratios)),
        'n': len(images)
    }

out = {'results': results, 'n_images': len(images), 'device': device}
with open('/home/kas/.openclaw/workspace-domain/research/0505-am-window/clip_dino_v2_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print('DONE', flush=True)