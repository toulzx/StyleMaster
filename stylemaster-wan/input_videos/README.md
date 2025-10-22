# Input Videos Directory

Place your input videos here for V2V stylization.

## Supported Formats
- MP4 (recommended)
- AVI
- MOV
- Other common video formats supported by imageio

## Recommended Specifications
- **FPS**: 30
- **Duration**: ≤15 seconds
- **Resolution**: 360p (640x360) or 480p (832x480)
- **Max frames**: ~450 (for 15s @ 30fps)

## Example Usage

```bash
# Place your video
cp /path/to/your/video.mp4 input_videos/

# Run stylization
python inference_v2v_stylemaster.py \
    --input_video input_videos/video.mp4 \
    --style_image example_test_data/style_images/ukiyoe.jpg \
    --output_dir results_v2v/output
```

## Quick Start

```bash
# Using the quick start script
./quick_start_v2v.sh input_videos/your_video.mp4
```
