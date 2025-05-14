import argparse
import sys
import subprocess
import random
from pathlib import Path

# Change this how you like
COUNT = 1000

parser = argparse.ArgumentParser(description="Corrupt an image file.")
parser.add_argument(
    "image_file",
    type=str,
    help="The image file to corrupt"
)

args = parser.parse_args()
file = Path(args.image_file)
base = file.stem
ext = file.suffix[1:]
if not ext:
    print("image_corrupt.py: Please provide an image file with an extension.")
    sys.exit(1)
if not file.exists():
    print(f"image_corrupt.py: File {file} does not exist.")
    sys.exit(1)

with open(file, "rb") as f:
    data = bytearray(f.read())

subprocess.run(["mkdir", "-p", f"{ext}s"])

for i in range(COUNT):
    while True:
        olddata = data[:]
        # The beginning has important metadata
        pos = random.randint(100, len(data) - 1)
        data[pos] = (data[pos] + 1) % 256
        # data[pos] ^= (1 << random.randint(0, 7))
        with open(f"{ext}s/{i:04}.{ext}", "wb") as f:
            f.write(data)
        if (
            subprocess.run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-i",
                    f"{ext}s/{i:04}.{ext}",
                    "-f",
                    "null",
                    "-",
                ],
                stderr=subprocess.DEVNULL,
            ).returncode
            == 0
        ):
            break
        data = olddata
