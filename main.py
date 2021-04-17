from rembg.bg import remove
import numpy as np
import io
from PIL import Image

input_path = 'profil.png'
output_path = 'cutout.png'

f = np.fromfile(input_path)
result = remove(f,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_structure_size=6)
img = Image.open(io.BytesIO(result)).convert("RGBA")
img.save(output_path)
