# StyleMaster-Wan

This repository contains an implementation of **StyleMaster** T2V model upon the **Wan-2.1** base model. 


## 🚀 Getting Started

Follow these steps to set up the environment, install dependencies, and download the necessary models.

### 1. Open the Workspace

```bash
cd stylemaster-wan
```

### 2. Create and Activate Conda Environment

```bash
curl --proto '=https' --tlsv1.2 -sSf [https://sh.rustup.rs](https://sh.rustup.rs/) | sh
. "$HOME/.cargo/env"
conda create --name stylemaster python=3.10
conda activate stylemaster
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Download Checkpoints

Run the provided script to download the pre-trained checkpoints. 
```bash
python download_ckpt.py
```
After this step, you should have `checkpoints/` and `Models/`directory containing the necessary model files.

### 5. Verify Setup (Optional)

Verify that everything is correctly installed:
```bash
python verify_setup.py
```
This will check:
- Python version
- Required packages
- CUDA availability
- Model files
- Scripts and directories

## 🎨 Inference

StyleMaster supports two inference modes:

### 1. Text-to-Video (T2V) Generation

Generate stylized videos from text descriptions:

```bash
python inference_stylemaster.py 
```

### 2. Video-to-Video (V2V) Stylization ✨ NEW

Stylize existing videos with artistic styles:

```bash
python inference_v2v_stylemaster.py \
    --input_video <video_path> \
    --style_image <style_image_path> \
    --prompt "description of video content" \
    --output_dir ./results_v2v
```

**Example:**
```bash
python inference_v2v_stylemaster.py \
    --input_video ./input_videos/sample.mp4 \
    --style_image ./example_test_data/style_images/ukiyoe.jpg \
    --prompt "A man and a woman dancing on a city street" \
    --output_dir ./results_v2v
```

For detailed V2V usage, parameters, and examples, see [VIDEO_STYLIZATION.md](VIDEO_STYLIZATION.md).

## 🎓 Training

You can train your own StyleMaster adapter on a custom dataset to capture a specific style. The complete workflow for data processing and training is detailed in `script.sh`.

### General Workflow

The training process generally involves two main steps:

1.  **Data Preparation:** Refer to the `./data` folder for examples. 

2.  **Training Execution:** Once the dataset is prepared, you can launch the training script. 

## Acknowledgements

This project is an implementation of the **StyleMaster** method on the **Wan-2.1** model.

Our code heavily relies on [Diffsynth-Studio](https://github.com/modelscope/DiffSynth-Studio) and [ReCamMaster](https://github.com/KwaiVGI/ReCamMaster), thanks for their contribution!

