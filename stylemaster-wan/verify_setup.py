#!/usr/bin/env python
"""
Setup verification script for StyleMaster V2V pipeline.
Checks if all dependencies and models are properly installed.
"""

import sys
import os

def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        return False

def check_imports():
    """Check if required packages are installed."""
    print("\nChecking required packages...")
    packages = {
        'torch': 'torch',
        'torchvision': 'torchvision',
        'PIL': 'Pillow',
        'imageio': 'imageio',
        'einops': 'einops',
        'pandas': 'pandas',
        'safetensors': 'safetensors',
        'transformers': 'transformers',
        'diffsynth': 'diffsynth (from this repo)',
    }
    
    all_ok = True
    for module, package_name in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} (not installed)")
            all_ok = False
    
    return all_ok

def check_cuda():
    """Check CUDA availability."""
    print("\nChecking CUDA...")
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"  ✓ CUDA available")
            print(f"    Device: {device_name}")
            print(f"    Memory: {memory_gb:.1f} GB")
            return True
        else:
            print("  ✗ CUDA not available")
            return False
    except ImportError:
        print("  ✗ Cannot check CUDA (torch not installed)")
        return False

def check_model_files():
    """Check if required model files exist."""
    print("\nChecking model files...")
    
    model_paths = [
        "models/Wan-AI/Wan2.1-T2V-1.3B/diffusion_pytorch_model.safetensors",
        "models/Wan-AI/Wan2.1-T2V-1.3B/models_t5_umt5-xxl-enc-bf16.pth",
        "models/Wan-AI/Wan2.1-T2V-1.3B/Wan2.1_VAE.pth",
    ]
    
    checkpoint_path = "checkpoints/stylemaster.ckpt"
    
    all_ok = True
    
    for path in model_paths:
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / 1024**2
            print(f"  ✓ {path} ({size_mb:.1f} MB)")
        else:
            print(f"  ✗ {path} (not found)")
            all_ok = False
    
    if os.path.exists(checkpoint_path):
        size_mb = os.path.getsize(checkpoint_path) / 1024**2
        print(f"  ✓ {checkpoint_path} ({size_mb:.1f} MB)")
    else:
        print(f"  ✗ {checkpoint_path} (not found)")
        all_ok = False
    
    if not all_ok:
        print("\n  → Run 'python download_ckpt.py' to download missing models")
    
    return all_ok

def check_scripts():
    """Check if main scripts exist."""
    print("\nChecking scripts...")
    
    scripts = [
        "inference_v2v_stylemaster.py",
        "inference_stylemaster.py",
        "styleproj.py",
        "quick_start_v2v.sh",
    ]
    
    all_ok = True
    for script in scripts:
        if os.path.exists(script):
            print(f"  ✓ {script}")
        else:
            print(f"  ✗ {script} (not found)")
            all_ok = False
    
    return all_ok

def check_directories():
    """Check if required directories exist."""
    print("\nChecking directories...")
    
    dirs = [
        "example_test_data/style_images",
        "input_videos",
    ]
    
    all_ok = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} (not found)")
            all_ok = False
    
    return all_ok

def print_summary(results):
    """Print summary and recommendations."""
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
    
    print("=" * 70)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to use StyleMaster V2V.")
        print("\nQuick start:")
        print("  ./quick_start_v2v.sh input_videos/your_video.mp4")
        print("\nOr:")
        print("  python inference_v2v_stylemaster.py \\")
        print("      --input_video input_videos/your_video.mp4 \\")
        print("      --style_image example_test_data/style_images/ukiyoe.jpg \\")
        print("      --output_dir results_v2v")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install dependencies: pip install -e .")
        print("  2. Download models: python download_ckpt.py")
        print("  3. Create missing directories")
    
    print()

def main():
    print("=" * 70)
    print("StyleMaster V2V Setup Verification")
    print("=" * 70)
    print()
    
    # Run all checks
    results = {
        "Python version": check_python_version(),
        "Required packages": check_imports(),
        "CUDA availability": check_cuda(),
        "Model files": check_model_files(),
        "Scripts": check_scripts(),
        "Directories": check_directories(),
    }
    
    # Print summary
    print_summary(results)
    
    # Exit with appropriate code
    sys.exit(0 if all(results.values()) else 1)

if __name__ == "__main__":
    main()
