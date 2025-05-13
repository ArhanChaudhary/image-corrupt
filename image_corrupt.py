import sys
import subprocess
import random

# Change this how you like
COUNT = 1000

if len(sys.argv) <= 1:
    print("image_corrupt.py: Please provide the file to corrupt.")
    sys.exit(1)
file_parts = sys.argv[1].split(".")
if len(file_parts) != 2:
    print("image_corrupt.py: Please provide a file with one extension.")
    sys.exit(1)
base, ext = file_parts

with open(f"{base}.{ext}", "rb") as f:
    data = bytearray(f.read())

subprocess.run(["mkdir", "-p", f"{ext}s"])

for i in range(COUNT):
    while True:
        # The beginning has important metadata
        pos = random.randint(100, len(data) - 100)
        olddata = data[:]
        data[pos] = (data[pos] + 1) % 256
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
