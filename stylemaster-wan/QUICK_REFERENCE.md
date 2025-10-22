# StyleMaster V2V Quick Reference

## 🎯 TL;DR

**Q: 支持视频风格化吗？**  
**A: 是的！✅**

**一行命令开始：**
```bash
cd stylemaster-wan && ./quick_start_v2v.sh input_videos/your_video.mp4
```

---

## 📦 Setup (First Time Only)

```bash
cd stylemaster-wan
pip install -e .
python download_ckpt.py
python verify_setup.py  # Optional: verify installation
```

---

## 🚀 Usage Methods

### Method 1: Quick Start (Recommended for Beginners)

```bash
./quick_start_v2v.sh input_videos/my_video.mp4
```

### Method 2: Custom Parameters (Advanced Users)

```bash
python inference_v2v_stylemaster.py \
    --input_video input_videos/my_video.mp4 \
    --style_image example_test_data/style_images/ukiyoe.jpg \
    --prompt "video description" \
    --height 480 \
    --width 832 \
    --denoising_strength 0.85 \
    --style_cfg_scale 4.0 \
    --output_dir results_v2v
```

---

## 🎨 Style Examples

| Style | Command |
|-------|---------|
| 浮世绘 (Ukiyoe) | `--style_image example_test_data/style_images/ukiyoe.jpg` |
| 梵高 (Van Gogh) | `--style_image example_test_data/style_images/vangough.png` |
| Fine Art | `--style_image example_test_data/style_images/fine_1.jpg` |
| Custom | `--style_image /path/to/your/style.jpg` |

---

## ⚙️ Key Parameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `--denoising_strength` | 0.85 | 0.6-1.0 | Higher = more stylized, less original content |
| `--style_cfg_scale` | 4.0 | 2.0-8.0 | Higher = stronger style |
| `--num_inference_steps` | 50 | 30-80 | Higher = better quality, slower |
| `--height` | 480 | 360-720+ | Video height (must be ÷16) |
| `--width` | 832 | 640-1280+ | Video width (must be ÷16) |
| `--num_frames` | auto | 1-450+ | Number of frames to process |

---

## 🎛️ Common Scenarios

### Scenario 1: Light Stylization (Preserve Details)
```bash
--denoising_strength 0.70 --style_cfg_scale 3.0
```

### Scenario 2: Balanced (Recommended)
```bash
--denoising_strength 0.85 --style_cfg_scale 4.0
```

### Scenario 3: Heavy Stylization
```bash
--denoising_strength 0.95 --style_cfg_scale 6.0
```

### Scenario 4: Fast Processing
```bash
--num_inference_steps 30 --height 360 --width 640
```

### Scenario 5: High Quality
```bash
--num_inference_steps 60 --height 720 --width 1280
```

---

## 💻 Hardware Requirements

| Resolution | Frames | VRAM | Time (A100) |
|------------|--------|------|-------------|
| 360x640 | 81 | ~20GB | ~4-6 min |
| 480x832 | 81 | ~30GB | ~5-8 min |
| 540x960 | 81 | ~40GB | ~6-10 min |
| 720x1280 | 81 | ~60GB | ~8-12 min |

**Your Setup: A100-80G** ✅ All configs supported!

---

## 📁 File Structure

```
stylemaster-wan/
├── inference_v2v_stylemaster.py  ← Main script
├── quick_start_v2v.sh            ← Quick start
├── verify_setup.py               ← Setup check
├── input_videos/                 ← Put your videos here
│   └── README.md
├── example_test_data/
│   └── style_images/             ← Style references
├── results_v2v/                  ← Output videos
└── [documentation]
```

---

## 📖 Documentation

| Language | File | Purpose |
|----------|------|---------|
| 🇨🇳 Chinese | [视频风格化功能说明.md](../视频风格化功能说明.md) | Quick answer |
| 🇨🇳 Chinese | [使用指南.md](使用指南.md) | Complete guide |
| 🇬🇧 English | [VIDEO_STYLIZATION.md](VIDEO_STYLIZATION.md) | Full docs |
| 📋 Tech | [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Technical details |

---

## ❓ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "checkpoint not found" | Run `python download_ckpt.py` |
| "CUDA out of memory" | Reduce `--height`, `--width`, or `--num_frames` |
| Style not strong enough | Increase `--style_cfg_scale` to 6.0 |
| Content changed too much | Decrease `--denoising_strength` to 0.70 |
| Slow processing | Reduce `--num_inference_steps` to 30 |
| Flickering video | Increase `--num_inference_steps`, use better prompt |

---

## 🔗 Quick Links

- **Main README**: [../README.md](../README.md)
- **Project Page**: https://zixuan-ye.github.io/stylemaster
- **Paper**: https://arxiv.org/abs/2412.07744
- **Base Model**: [Wan-2.1](https://github.com/Wan-Video/Wan2.1)

---

## ⚡ One-Liners

```bash
# Verify installation
python verify_setup.py

# Stylize video (default settings)
./quick_start_v2v.sh input_videos/video.mp4

# Stylize with custom style
./quick_start_v2v.sh input_videos/video.mp4 path/to/style.jpg

# Light stylization
python inference_v2v_stylemaster.py --input_video video.mp4 --style_image style.jpg --denoising_strength 0.70

# Heavy stylization
python inference_v2v_stylemaster.py --input_video video.mp4 --style_image style.jpg --denoising_strength 0.95 --style_cfg_scale 6.0

# Fast preview
python inference_v2v_stylemaster.py --input_video video.mp4 --style_image style.jpg --num_frames 41 --num_inference_steps 30

# High quality
python inference_v2v_stylemaster.py --input_video video.mp4 --style_image style.jpg --num_inference_steps 60 --height 720 --width 1280
```

---

## 📊 Your Specs Support

✅ FPS: 30  
✅ Duration: ≤15s (450 frames max)  
✅ Resolution: 360p+ (all resolutions supported)  
✅ GPU: A100-80G (optimal performance)

**You're all set! Start stylizing! 🎨**

---

*For detailed information, see the full documentation files listed above.*
