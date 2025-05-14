#!/bin/bash

input_file="$1"

if [ -z "$input_file" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

for cmd in magick ffmpeg python; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: '$cmd' is not installed or not in your PATH."
        exit 1
    fi
done

python "${0%.*}".py "$input_file" || exit 1

filename=$(basename -- "$input_file")
ext="${filename##*.}"
base="${filename%."$ext"}"

cd "${ext}s" || exit 1
# The results of this loop are uninteresting for jpg
if [ "$ext" != "jpg" ]; then
    if command -v parallel &> /dev/null; then
        parallel --progress --eta ffmpeg -y -i {} _{} ::: *."$ext"
        for file in [!_]*."$ext"; do
            mv "_$file" "$file"
        done
    else
        for file in *."$ext"; do
            ffmpeg -y -i "$file" "_$file"
            mv "_$file" "$file"
        done
    fi
fi
# I had to resort to ImageMagick's deprecated `convert` program because
# ImageMagick would sometimes crash more than half way through without
# generating the GIF. The old version handled this correctly, and I
# couldn't figure out how to make the current version do this.
magick convert -limit memory 100000 ./*."$ext" "$base".gif
ffmpeg -itsscale 0.2 -i "$base".gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "$base".mp4

echo
echo Done! Generated "$base".gif and "$base".mp4 in the directory "${ext}s".
