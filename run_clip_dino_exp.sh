#!/bin/bash
set -e
cd /home/kas/.openclaw/workspace-domain/research/0505-am-window
python3 -c "
import sys
sys.path.insert(0, '/home/kas/.openclaw/workspace-domain/research/0504-pm-window')
import torch
import clip
import json
import numpy as np
from PIL import Image
import os

# Load CLIP and DINOv2
device = 'cpu'
print('Loading CLIP...', flush=True)
clip_model, clip_preprocess = clip.load('ViT-B/32', device=device)
clip_model.eval()
print('Loading DINOv2...', flush=True)
dinov2 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14')
dinov2.eval()
dinov2.to(device)
print('Models loaded', flush=True)

# Load CIFAR-10 test images
from torchvision import datasets
cifar = datasets.CIFAR10(root='/tmp/cifar10', train=False, download=True)
indices = list(range(0, 50))  # N=50
images = [cifar[i][0] for i in indices]
print(f'Loaded {len(images)} CIFAR-10 images', flush=True)

results = {}
for sigma in [0.0, 0.3, 0.7, 1.0]:
    degs_clip = []
    degs_dino = []
    ratios = []
    for i, img in enumerate(images):
        # Preprocess
        clip_img = clip_preprocess(img).unsqueeze(0).to(device)
        pil_img = img.resize((224, 224))
        dino_img = torch.from_numpy(np.array(pil_img)).permute(2,0,1).float().unsqueeze(0) / 255.0
        dino_img = torch.nn.functional.interpolate(dino_img, size=(224, 224), mode='bilinear')
        dino_img = (dino_img - 0.45) / 0.22
        dino_img = dino_img.to(device)
        
        with torch.no_grad():
            # Original features
            clip_feats_orig = clip_model.encode_image(clip_img)
            dino_feats_orig = dinov2(dino_img)
            clip_feats_orig = clip_feats_orig / clip_feats_orig.norm(dim=-1, keepdim=True)
            dino_feats_orig = dino_feats_orig / dino_feats_orig.norm(dim=-1, keepdim=True)
            
            # Noisy version for DINOv2
            noise = torch.randn_like(dino_img) * sigma / 255.0 * 2
            dino_noisy = (dino_img + noise).clamp(0, 1)
            dino_noisy = (dino_noisy - 0.45) / 0.22
            dino_feats_noisy = dinov2(dino_noisy.to(device))
            dino_feats_noisy = dino_feats_noisy / dino_feats_noisy.norm(dim=-1, keepdim=True)
            
            # CLIP noise
            clip_noise = torch.randn_like(clip_img) * (sigma / 255.0 * 2)
            clip_noisy = (clip_img + clip_noise).clamp(-2, 2)
            clip_feats_noisy = clip_model.encode_image(clip_noisy)
            clip_feats_noisy = clip_feats_noisy / clip_feats_noisy.norm(dim=-1, keepdim=True)
            
            # Angular degradation
            deg_clip = (1 - (clip_feats_orig * clip_feats_noisy).sum(-1).item()) * 180 / 3.14159
            deg_dino = (1 - (dino_feats_orig * dino_feats_noisy).sum(-1).item()) * 180 / 3.14159
            ratio = deg_clip / deg_dino if deg_dino > 0 else 0
            
            degs_clip.append(deg_clip)
            degs_dino.append(deg_dino)
            ratios.append(ratio)
    
    mean_clip = np.mean(degs_clip)
    mean_dino = np.mean(degs_dino)
    mean_ratio = np.mean(ratios)
    print(f'sigma={sigma}: CLIP_deg={mean_clip:.3f}, DINO_deg={mean_dino:.3f}, ratio={mean_ratio:.4f}', flush=True)
    results[f'sigma_{sigma}'] = {
        'mean_deg_clip': mean_clip,
        'mean_deg_dino': mean_dino,
        'mean_ratio': mean_ratio,
        'std_ratio': np.std(ratios),
        'n_images': len(images)
    }

with open('clip_dino_full_results.json', 'w') as f:
    json.dump({'results': results, 'n_images': len(images)}, f, indent=2)
print('DONE', flush=True)
" 2>&1 | tee clip_dino_run.log
