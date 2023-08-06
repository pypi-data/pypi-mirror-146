<img src="./3d-unet.png" width="500px"></img>

## Video Diffusion - Pytorch (wip)

Implementation of <a href="https://arxiv.org/abs/2204.03458">Video Diffusion Models</a>, <a href="http://www.jonathanho.me/">Jonathan Ho</a>'s new paper extending DDPMs to Video Generation - in Pytorch. It uses a special space-time factored U-net, extending generation from 2d images to 3d videos

Text to video, it is happening!

<a href="https://video-diffusion.github.io/">Project Page</a>

## Install

```bash
$ pip install video-diffusion-pytorch
```

## Usage

```python
import torch
from video_diffusion_pytorch import Unet3D, GaussianDiffusion

model = Unet3D(
    dim = 64,
    dim_mults = (1, 2, 4, 8)
)

diffusion = GaussianDiffusion(
    model,
    image_size = 32,
    num_frames = 5,
    timesteps = 1000,   # number of steps
    loss_type = 'l1'    # L1 or L2
)

videos = torch.randn(1, 3, 5, 32, 32)
loss = diffusion(videos)
loss.backward()
# after a lot of training

sampled_videos = diffusion.sample(batch_size = 4)
sampled_videos.shape # (4, 3, 5, 32, 32)
```

For conditioning on text, they derived text embeddings by first passing the tokenized text through BERT-large. Then you just have to train it like so

```python
import torch
from video_diffusion_pytorch import Unet3D, GaussianDiffusion

model = Unet3D(
    dim = 64,
    cond_dim = 64,
    dim_mults = (1, 2, 4, 8)
)

diffusion = GaussianDiffusion(
    model,
    image_size = 32,
    num_frames = 5,
    timesteps = 1000,   # number of steps
    loss_type = 'l1'    # L1 or L2
)

videos = torch.randn(2, 3, 5, 32, 32) # your video
text = torch.randn(2, 64)             # assume output of BERT-large has dimension of 64

loss = diffusion(videos, cond = text)
loss.backward()
# after a lot of training

sampled_videos = diffusion.sample(cond = text)
sampled_videos.shape # (2, 3, 5, 32, 32)
```

## Todo

- [x] wire up text conditioning, use classifier free guidance
- [ ] relative positional encodings in attention (space and time) - use T5 relative positional bias instead of what they used
- [ ] find a good torchvideo-like library (torchvideo seems immature) for training on fireworks
- [ ] consider doing a 3d version of CLIP, so one can eventually apply the lessons of DALL-E2 to video
- [ ] add a forward keyword argument that arrests attention across time (as reported / claimed in the paper, this type of image + video simultaneous training improves results)

## Citations

```bibtex
@misc{ho2022video,
  title   = {Video Diffusion Models}, 
  author  = {Jonathan Ho and Tim Salimans and Alexey Gritsenko and William Chan and Mohammad Norouzi and David J. Fleet},
  year    = {2022},
  eprint  = {2204.03458},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV}
}
```
