#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/kas/.openclaw/workspace-domain/research/0504-pm-window')
import torch
import clip
import json
import numpy as np
from PIL import Image
from torchvision import datasets

device = 'cpu'
print('Loading CLIP ViT-B/32...', flush=True)
clip_model, clip_preprocess = clip.load('ViT-B/32', device=device)
clip_model.eval()
print('Loading DINOv2 ViT-B/14...', flush=True)
dinov2 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14')
dinov2.eval()
dinov2.to(device)
print('Models loaded OK', flush=True)

# Load CIFAR-10 test set
cifar = datasets.CIFAR10(root='/tmp/cifar10', train=False, download=True)
indices = list(range(50))  # N=50
images = [cifar[i][0] for i in indices]
print(f'Loaded {len(images)} CIFAR-10 images', flush=True)

results = {}
for sigma in [0.0, 0.3, 0.7, 1.0]:
    degs_clip, degs_dino, ratios = [], [], []
    for img in images:
        # CLIP input (1,3,224,224) normalized
        clip_img = clip_preprocess(img).unsqueeze(0).to(device)
        # DINOv2 input (1,3,224,224) ImageNet norm
        pil_img = img.resize((224, 224))
        dino_img = torch.from_numpy(np.array(pil_img)).permute(2,0,1).float().unsqueeze(0) / 255.0
        dino_img = torch.nn.functional.interpolate(dino_img, size=(224, 224), mode='bilinear')
        dino_img_norm = (dino_img - 0.45) / 0.22
        
        with torch.no_grad():
            f_clip_orig = clip_model.encode_image(clip_img)
            f_clip_orig = f_clip_orig / f_clip_orig.norm(dim=-1, keepdim=True)
            f_dino_orig = dinov2(dino_img_norm.to(device))
            f_dino_orig = f_dino_orig / f_dino_orig.norm(dim=-1, keepdim=True)
            
            # Noise (sigma in pixel space, same for both)
            scale = sigma / 255.0 * 2
            # CLIP noisy
            clip_noisy = (clip_img + torch.randn_like(clip_img) * scale).clamp(-2, 2)
            f_clip_noisy = clip_model.encode_image(clip_noisy)
            f_clip_noisy = f_clip_noisy / f_clip_noisy.norm(dim=-1, keepdim=True)
            # DINOv2 noisy
            dino_noisy = (dino_img_norm + torch.randn_like(dino_img_norm) * scale).clamp(-2, 2)
            f_dino_noisy = dinov2(dino_noisy.to(device))
            f_dino_noisy = f_dino_noisy / f_dino_noisy.norm(dim=-1, keepdim=True)
            
            deg_clip = (1 - (f_clip_orig * f_clip_noisy).sum(-1).item()) * 180 / np.pi
            deg_dino = (1 - (f_dino_orig * f_dino_noisy).sum(-1).item()) * 180 / np.pi
            ratio = deg_clip / deg_dino if deg_dino > 1e-6 else 0
            
            degs_clip.append(deg_clip)
            degs_dino.append(deg_dino)
            ratios.append(ratio)
    
    print(f'sigma={sigma}: CLIP_deg={np.mean(degs_clip):.3f}, DINO_deg={np.mean(degs_dino):.3f}, ratio={np.mean(ratios):.4f}', flush=True)
    results[f'sigma_{sigma}'] = {
        'mean_deg_clip': float(np.mean(degs_clip)),
        'mean_deg_dino': float(np.mean(degs_dino)),
        'mean_ratio': float(np.mean(ratios)),
        'std_ratio': float(np.std(ratios)),
        'n_images': len(images)
    }

out = {'results': results, 'n_images': len(images), 'config': {'device': device, 'models': ['ViT-B/32', 'dinov2_vitb14']}}
with open('/home/kas/.openclaw/workspace-domain/research/0505-am-window/clip_dino_full_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print('DONE', flush=True)