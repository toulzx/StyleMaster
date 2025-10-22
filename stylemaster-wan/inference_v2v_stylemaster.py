"""
Video-to-Video Style Transfer using StyleMaster
This script takes an input video and a style reference image to generate a stylized video.

Usage:
    python inference_v2v_stylemaster.py --input_video <video_path> --style_image <image_path> --output_dir <output_dir>

Example:
    python inference_v2v_stylemaster.py \\
        --input_video ./input_videos/sample.mp4 \\
        --style_image ./example_test_data/style_images/002.jpg \\
        --prompt "A man and a woman dancing on a city street at dusk" \\
        --output_dir ./results_v2v
"""

import sys
import torch
import torch.nn as nn
from diffsynth import ModelManager, WanVideoStyleMasterPipeline, save_video, VideoData
import torch, os, imageio, argparse
from torchvision.transforms import v2
from einops import rearrange
import pandas as pd
import torchvision
from PIL import Image
import numpy as np
import json
from diffsynth.models.kolors_text_encoder import RMSNorm

from styleproj import Processor, StyleModel


def parse_args():
    parser = argparse.ArgumentParser(description="StyleMaster Video-to-Video Inference")
    parser.add_argument(
        "--input_video",
        type=str,
        required=True,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "--style_image",
        type=str,
        required=True,
        help="Path to the style reference image.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="",
        help="Text prompt describing the video content.",
    )
    parser.add_argument(
        "--negative_prompt",
        type=str,
        default="色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走",
        help="Negative prompt for generation.",
    )
    parser.add_argument(
        "--ckpt_path",
        type=str,
        default="checkpoints/stylemaster.ckpt",
        help="Path to the StyleMaster checkpoint.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./results_v2v",
        help="Path to save the stylized video.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="Output video height (must be divisible by 16).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=832,
        help="Output video width (must be divisible by 16).",
    )
    parser.add_argument(
        "--num_frames",
        type=int,
        default=None,
        help="Number of frames to process (default: all frames from input video, max recommended: 81 for 15s at 30fps you can use ~450 frames).",
    )
    parser.add_argument(
        "--cfg_scale",
        type=float,
        default=8.0,
        help="Classifier-free guidance scale for text.",
    )
    parser.add_argument(
        "--style_cfg_scale",
        type=float,
        default=4.0,
        help="Classifier-free guidance scale for style.",
    )
    parser.add_argument(
        "--num_inference_steps",
        type=int,
        default=50,
        help="Number of denoising steps.",
    )
    parser.add_argument(
        "--denoising_strength",
        type=float,
        default=0.85,
        help="Denoising strength (0.0-1.0). Lower values preserve more of the input video.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for generation.",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Output video FPS.",
    )
    args = parser.parse_args()
    return args


def load_video_frames(video_path, num_frames=None, height=480, width=832):
    """
    Load video frames from a video file.
    
    Args:
        video_path: Path to the video file
        num_frames: Number of frames to load (None = all frames)
        height: Target height for frames
        width: Target width for frames
    
    Returns:
        List of PIL Image objects
    """
    video_data = VideoData(video_file=video_path, height=height, width=width)
    
    total_frames = len(video_data)
    if num_frames is None:
        num_frames = total_frames
    else:
        num_frames = min(num_frames, total_frames)
    
    # Load frames
    frames = []
    for i in range(num_frames):
        frame = video_data[i]
        frames.append(frame)
    
    print(f"Loaded {len(frames)} frames from {video_path}")
    print(f"Frame size: {frames[0].size if frames else 'N/A'}")
    
    return frames


if __name__ == '__main__':
    args = parse_args()

    # Validate inputs
    if not os.path.exists(args.input_video):
        raise FileNotFoundError(f"Input video not found: {args.input_video}")
    if not os.path.exists(args.style_image):
        raise FileNotFoundError(f"Style image not found: {args.style_image}")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 80)
    print("StyleMaster Video-to-Video Stylization")
    print("=" * 80)
    print(f"Input video: {args.input_video}")
    print(f"Style image: {args.style_image}")
    print(f"Output directory: {args.output_dir}")
    print(f"Prompt: {args.prompt}")
    print(f"Denoising strength: {args.denoising_strength}")
    print("=" * 80)

    # 1. Load Wan2.1 pre-trained models
    print("\n[1/5] Loading models...")
    model_manager = ModelManager(torch_dtype=torch.bfloat16, device="cpu")
    model_manager.load_models([
        "models/Wan-AI/Wan2.1-T2V-1.3B/diffusion_pytorch_model.safetensors",
        "models/Wan-AI/Wan2.1-T2V-1.3B/models_t5_umt5-xxl-enc-bf16.pth",
        "models/Wan-AI/Wan2.1-T2V-1.3B/Wan2.1_VAE.pth",
    ])
    pipe = WanVideoStyleMasterPipeline.from_model_manager(model_manager, device="cuda")

    # 2. Initialize StyleMaster modules
    print("[2/5] Initializing StyleMaster modules...")
    processor = Processor().eval()
    dim = pipe.dit.blocks[0].cross_attn.q.weight.shape[0]
    pipe.dit.style_model = StyleModel()
    dim_s = pipe.dit.style_model.cross_attention_dim
    for block in pipe.dit.blocks:
        block.cross_attn.k_img = nn.Linear(dim_s, dim)
        block.cross_attn.v_img = nn.Linear(dim_s, dim)
        block.cross_attn.norm_k_img = RMSNorm(dim)

    # Load StyleMaster checkpoint
    if not os.path.exists(args.ckpt_path):
        raise FileNotFoundError(f"StyleMaster checkpoint not found: {args.ckpt_path}. Please run download_ckpt.py first.")
    
    state_dict = torch.load(args.ckpt_path, map_location="cpu")
    pipe.dit.load_state_dict(state_dict, strict=True)
    pipe.to("cuda")
    pipe.to(dtype=torch.bfloat16)

    # 3. Load input video
    print("[3/5] Loading input video...")
    input_frames = load_video_frames(
        args.input_video,
        num_frames=args.num_frames,
        height=args.height,
        width=args.width
    )
    
    # Adjust num_frames to match pipeline requirements (must be 4n+1)
    actual_num_frames = len(input_frames)
    if actual_num_frames % 4 != 1:
        actual_num_frames = (actual_num_frames + 2) // 4 * 4 + 1
        if actual_num_frames > len(input_frames):
            # Pad with last frame
            while len(input_frames) < actual_num_frames:
                input_frames.append(input_frames[-1])
        else:
            # Trim frames
            input_frames = input_frames[:actual_num_frames]
    
    print(f"Processing {len(input_frames)} frames (adjusted to match 4n+1 requirement)")

    # 4. Process style image
    print("[4/5] Processing style image...")
    style_img = Image.open(args.style_image).convert('RGB')
    image_embeds = processor.process_images([style_img])
    
    # 5. Run stylization
    print("[5/5] Running video stylization...")
    print(f"  - CFG scale: {args.cfg_scale}")
    print(f"  - Style CFG scale: {args.style_cfg_scale}")
    print(f"  - Inference steps: {args.num_inference_steps}")
    print(f"  - Denoising strength: {args.denoising_strength}")
    
    stylized_video = pipe(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        target_style=image_embeds,
        input_video=input_frames,
        denoising_strength=args.denoising_strength,
        cfg_scale=args.cfg_scale,
        style_cfg_scale=args.style_cfg_scale,
        num_inference_steps=args.num_inference_steps,
        height=args.height,
        width=args.width,
        num_frames=len(input_frames),
        seed=args.seed,
        tiled=True
    )
    
    # 6. Save output
    output_path = os.path.join(args.output_dir, "stylized_video.mp4")
    print(f"\nSaving stylized video to: {output_path}")
    save_video(stylized_video, output_path, fps=args.fps, quality=5)
    
    print("\n" + "=" * 80)
    print("✓ Video stylization completed successfully!")
    print(f"Output saved to: {output_path}")
    print("=" * 80)
