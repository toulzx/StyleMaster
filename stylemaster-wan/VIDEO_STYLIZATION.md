# Video-to-Video Stylization Guide

本文档介绍如何使用 StyleMaster 进行视频风格化。

## 功能说明

StyleMaster 支持两种视频生成模式：

1. **Text-to-Video (T2V)**: 从文本描述生成风格化视频（使用 `inference_stylemaster.py`）
2. **Video-to-Video (V2V)**: 将已有视频进行风格化转换（使用 `inference_v2v_stylemaster.py`）✨ **新增功能**

## Video-to-Video 使用方法

### 基本用法

```bash
python inference_v2v_stylemaster.py \
    --input_video <输入视频路径> \
    --style_image <风格参考图片路径> \
    --prompt "视频内容描述" \
    --output_dir ./results_v2v
```

### 完整参数示例

```bash
python inference_v2v_stylemaster.py \
    --input_video ./input_videos/sample.mp4 \
    --style_image ./example_test_data/style_images/ukiyoe.jpg \
    --prompt "A man and a woman dancing on a city street at dusk" \
    --negative_prompt "色调艳丽，过曝，静态，细节模糊不清" \
    --output_dir ./results_v2v \
    --height 480 \
    --width 832 \
    --num_frames 81 \
    --denoising_strength 0.85 \
    --cfg_scale 8.0 \
    --style_cfg_scale 4.0 \
    --num_inference_steps 50 \
    --seed 0 \
    --fps 30
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--input_video` | str | **必需** | 输入视频文件路径 |
| `--style_image` | str | **必需** | 风格参考图片路径 |
| `--prompt` | str | "" | 描述视频内容的文本提示 |
| `--negative_prompt` | str | 预设 | 负向提示词 |
| `--ckpt_path` | str | checkpoints/stylemaster.ckpt | StyleMaster 权重文件路径 |
| `--output_dir` | str | ./results_v2v | 输出目录 |
| `--height` | int | 480 | 输出视频高度（必须能被16整除）|
| `--width` | int | 832 | 输出视频宽度（必须能被16整除）|
| `--num_frames` | int | None | 处理的帧数（None=全部，推荐≤450）|
| `--cfg_scale` | float | 8.0 | 文本引导强度 |
| `--style_cfg_scale` | float | 4.0 | 风格引导强度 |
| `--num_inference_steps` | int | 50 | 去噪步数（越大质量越高但速度越慢）|
| `--denoising_strength` | float | 0.85 | 去噪强度（0.0-1.0，越低越保留原视频）|
| `--seed` | int | 0 | 随机种子 |
| `--fps` | int | 30 | 输出视频帧率 |

### 输入视频规格

根据您的需求，推荐的输入视频规格：

- **帧率 (FPS)**: 30
- **时长**: ≤15秒
- **分辨率**: 360p (640x360) 或 480p (832x480)
- **格式**: MP4, AVI, MOV 等常见视频格式

对于 15 秒 30fps 的视频，总帧数为 450 帧。由于显存限制，可以：
- 使用 `--num_frames` 参数限制处理的帧数
- 调整分辨率以节省显存

### 计算资源

- **推荐配置**: 1x A100-80G（您的配置✓）
- **显存占用**: 
  - 480x832 分辨率，81 帧：约 30-40GB
  - 360x640 分辨率，81 帧：约 20-30GB

### 风格控制技巧

1. **调整 `style_cfg_scale`**：
   - 增大（如 6.0-8.0）：风格更明显
   - 减小（如 2.0-3.0）：保留更多原始内容

2. **调整 `denoising_strength`**：
   - 0.7-0.8：轻度风格化，保留更多原视频细节
   - 0.85-0.95：中度风格化（推荐）
   - 0.95-1.0：强烈风格化，可能改变较多内容

3. **使用合适的 prompt**：
   - 提供准确的视频内容描述有助于保持内容一致性
   - 可以通过 prompt 引导风格方向

## 示例工作流

### 1. 准备输入视频

```bash
# 创建输入目录
mkdir -p input_videos

# 将你的视频放入该目录
# 例如: input_videos/my_video.mp4
```

### 2. 选择风格图片

使用仓库中提供的风格图片，或准备自己的风格参考：

```bash
ls example_test_data/style_images/
# 输出: 002.jpg  0001.jpg  05.jpg  fine_1.jpg  fine_3.jpg  ukiyoe.jpg  vangough.png  等
```

### 3. 运行风格化

```bash
python inference_v2v_stylemaster.py \
    --input_video input_videos/my_video.mp4 \
    --style_image example_test_data/style_images/vangough.png \
    --prompt "描述你的视频内容" \
    --output_dir results_v2v/my_output
```

### 4. 查看结果

```bash
ls results_v2v/my_output/
# 输出: stylized_video.mp4
```

## 常见问题

### Q: 如何处理超过 15 秒的视频？

A: 可以：
1. 使用视频编辑工具分割视频为多个片段
2. 分别处理每个片段
3. 使用 `--num_frames` 限制处理的帧数

### Q: 显存不足怎么办？

A: 尝试以下方法：
1. 降低分辨率（如使用 360x640）
2. 减少处理的帧数（`--num_frames`）
3. 减少 `--num_inference_steps`

### Q: 风格化效果不理想？

A: 可以调整：
1. 增大 `style_cfg_scale` 以增强风格
2. 调整 `denoising_strength`
3. 尝试不同的风格参考图片
4. 优化 prompt 描述

### Q: 处理速度慢？

A: 可以：
1. 减少 `--num_inference_steps`（推荐不低于 30）
2. 减少分辨率
3. 减少处理的帧数

## 进阶功能

### 批量处理

创建一个脚本批量处理多个视频：

```bash
#!/bin/bash
for video in input_videos/*.mp4; do
    basename=$(basename "$video" .mp4)
    python inference_v2v_stylemaster.py \
        --input_video "$video" \
        --style_image example_test_data/style_images/ukiyoe.jpg \
        --prompt "视频内容描述" \
        --output_dir "results_v2v/$basename"
done
```

### 实验不同参数

创建参数网格搜索：

```bash
for strength in 0.7 0.85 0.95; do
    for style_cfg in 2.0 4.0 6.0; do
        python inference_v2v_stylemaster.py \
            --input_video input_videos/test.mp4 \
            --style_image example_test_data/style_images/002.jpg \
            --denoising_strength $strength \
            --style_cfg_scale $style_cfg \
            --output_dir "results_v2v/grid_${strength}_${style_cfg}"
    done
done
```

## 与 T2V 模式的对比

| 特性 | T2V (inference_stylemaster.py) | V2V (inference_v2v_stylemaster.py) |
|------|-------------------------------|-----------------------------------|
| 输入 | 文本描述 | 视频 + 文本描述 |
| 内容控制 | 由文本生成 | 保留原视频内容 |
| 风格控制 | 风格参考图片 | 风格参考图片 |
| 应用场景 | 创意生成 | 视频风格转换 |
| 处理速度 | 较快 | 稍慢（需编码输入视频）|

## 技术细节

### 工作原理

1. **视频编码**: 使用 VAE 编码器将输入视频转换为潜在空间表示
2. **风格提取**: 使用 StyleMaster 的风格提取模块处理风格参考图片
3. **去噪过程**: 在潜在空间中进行风格化去噪，结合文本和风格引导
4. **视频解码**: 将风格化的潜在表示解码回像素空间

### 关键模块

- **WanVideoStyleMasterPipeline**: 核心推理管道
- **StyleModel**: 风格提取和投影模块
- **Processor**: 图像预处理器
- **VAE**: 视频编解码器

## 参考

- 主 README: [../README.md](../README.md)
- StyleMaster-Wan 文档: [readme.md](readme.md)
- 论文: [StyleMaster: Stylize Your Video with Artistic Generation and Translation](https://arxiv.org/abs/2412.07744)
