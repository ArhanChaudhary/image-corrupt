# image-corrupt

Code provided from my blog post [Turning Image Corruption into Art](https://arhan.sh/blog/turning-image-corruption-into-art/). A shell script that repeatedly corrupts an image and generates a video of it happening.

## Required software

- Python
- ImageMagick
- ffmpeg

Optionally, parallel

## Usage

```bash
./image_corrupt.sh [image_file]
```

With ImageMagick installed, you can easily convert your image to other formats to see how the corruption changes.

```bash
magick [image_file_base].jpg [image_file_base].avif
```
