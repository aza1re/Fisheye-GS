# UPDATE(Apr 10th 2025)
I am surprised that the work from the workshop have drawn much more attention than expected. 

And I am sorry that I have put it aside since its publication. 

I will maintain Fisheye-GS, debug the code and reply the issues as soon as possible. 

Fisheye-GS cannot render through cameras with extremely large distortion, because of the error from the first-order approximation. If you want to render 3DGS with distorted cameras, you can try [3DGUT](https://research.nvidia.com/labs/toronto-ai/3DGUT/) for better performance.

In the future, I will develop the compiler for more distortion models for both rendering or training.
# Fisheye-GS
ECCV 2024 Workshop NFBCC

[arxiv](https://arxiv.org/abs/2409.04751)

![Teaser image](assets/teaser1.jpg)

**Abstract**:  Recently, 3D Gaussian Splatting (3DGS) has garnered attention for its high fidelity and real-time rendering. However, adapting 3DGS to different camera models, particularly fisheye lenses, poses challenges due to the unique 3D to 2D projection calculation. Additionally, there are inefficiencies in the tile-based splatting, especially for the extreme curvature and wide field of view of fisheye lenses, which are crucial for its broader real-life applications. To tackle these challenges, we introduce Fisheye-GS. This innovative method recalculates the projection transformation and its gradients for fisheye cameras. Our approach can be seamlessly integrated as a module into other efficient 3D rendering methods, emphasizing its extensibility, lightweight nature, and modular design. Since we only modified the projection component, it can also be easily adapted for use with different camera models. Compared to methods that train after undistortion, our approach demonstrates a clear improvement in visual quality.

## TODO
+ Release paper ✔
+ Release Fisheye-GS for FlashGS
+ Release the dataset we use
+ Release panorama
### Hardware Requirements

- CUDA-ready GPU with Compute Capability 7.0+
- 24 GB VRAM (to train to paper evaluation quality)

### Software Requirements
- Conda (recommended for easy setup)
- C++ Compiler for PyTorch extensions 
- CUDA SDK 11 for PyTorch extensions
- C++ Compiler and CUDA SDK must be compatible

## Setup
```shell
.\install_miniconda.ps1
```
## Prepare Training Data on Scannet++ Dataset
Undistort the distortions excluding the radial distortion from $k_1$
```shell
.\prepare.ps1
```
## Training on Scannet++ Dataset
```shell
.\train.ps1
```
## Rendering on Scannet++ Dataset
```shell
.\render.ps1
```
## Evaluating
```shell
.\eval.ps1
```

## License
Please follow the LICENSE of <a href='https://github.com/graphdeco-inria/gaussian-splatting'>3D-GS</a>.

## Acknowledgement
We thank all authors from <a href='https://github.com/graphdeco-inria/gaussian-splatting'>3D-GS</a> for presenting such an excellent work.
