#!/bin/bash
# Quick start script for video stylization
# This script demonstrates how to stylize a video using StyleMaster

set -e

echo "StyleMaster Video-to-Video Stylization - Quick Start"
echo "======================================================"

# Check if input video is provided
if [ -z "$1" ]; then
    echo "Usage: ./quick_start_v2v.sh <input_video_path> [style_image_path]"
    echo ""
    echo "Example:"
    echo "  ./quick_start_v2v.sh input_videos/my_video.mp4"
    echo "  ./quick_start_v2v.sh input_videos/my_video.mp4 example_test_data/style_images/ukiyoe.jpg"
    echo ""
    echo "If style_image_path is not provided, ukiyoe.jpg will be used as default."
    exit 1
fi

INPUT_VIDEO="$1"
STYLE_IMAGE="${2:-example_test_data/style_images/ukiyoe.jpg}"

# Validate inputs
if [ ! -f "$INPUT_VIDEO" ]; then
    echo "Error: Input video not found: $INPUT_VIDEO"
    exit 1
fi

if [ ! -f "$STYLE_IMAGE" ]; then
    echo "Error: Style image not found: $STYLE_IMAGE"
    exit 1
fi

# Get video name for output directory
VIDEO_NAME=$(basename "$INPUT_VIDEO" | sed 's/\.[^.]*$//')
OUTPUT_DIR="./results_v2v/${VIDEO_NAME}_$(date +%Y%m%d_%H%M%S)"

echo ""
echo "Configuration:"
echo "  Input Video:  $INPUT_VIDEO"
echo "  Style Image:  $STYLE_IMAGE"
echo "  Output Dir:   $OUTPUT_DIR"
echo ""

# Run stylization with default parameters optimized for 360p-480p videos
python inference_v2v_stylemaster.py \
    --input_video "$INPUT_VIDEO" \
    --style_image "$STYLE_IMAGE" \
    --prompt "video content" \
    --output_dir "$OUTPUT_DIR" \
    --height 480 \
    --width 832 \
    --num_frames 81 \
    --denoising_strength 0.85 \
    --cfg_scale 8.0 \
    --style_cfg_scale 4.0 \
    --num_inference_steps 50 \
    --fps 30 \
    --seed 0

echo ""
echo "======================================================"
echo "✓ Stylization completed!"
echo "  Output: ${OUTPUT_DIR}/stylized_video.mp4"
echo "======================================================"
