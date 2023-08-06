import os
import base64
import io
import numpy as np
import random
from PIL import Image
from ficaptcha.process import noise

class Captcha():
    def __init__(self,
                size: tuple = (512,512),
                image_dir: str = None,
                background_color: str = "white",
                noise_bg: bool = True,
                noise_im: bool = True,
                rotate_im: bool = True,
                count_images: int = 5,
                maxH: list = [70, 80],
                maxW: list = [70, 80],):
        self.image_dir = image_dir
        self.size = size
        self.background_color = background_color
        self.noise_bg = noise_bg
        self.noise_im = noise_im
        self.rotate_im = rotate_im
        self.maxH = maxH
        self.maxW = maxW
        self.count_images = count_images
        self.captcha = None


    def generate(self):
        cls = os.listdir(self.image_dir)
        class_i = []
        cache = []

        for c in cls:
            ca = os.listdir(f"{self.image_dir}/{c}")
            for p in ca:
                class_i.append([c, f"{self.image_dir}/{c}/{p}"])
        t = random.choice(class_i)

        bg = Image.new('RGBA', self.size, self.background_color)

        if self.noise_bg:
            bg = noise(bg, random.uniform(0.001, 1.0))

        isp = []

        for i in range(self.count_images - 1):
            v = random.choice(class_i)
            if v[0] in isp or v[0] == t[0]:
                pass
            else:
                isp.append(v[0])
                v = Image.open(v[1])
                v = v.resize((random.randint(self.maxH[0], self.maxH[1]), random.randint(self.maxW[0], self.maxW[1])))

                if self.rotate_im:
                    v = v.rotate(random.randint(-360, 360), expand=True)

                if self.noise_im:
                    v = noise(v, random.uniform(0.001, 0.1))
            
                bg.paste(v, (random.randint(10, self.size[0] - 100), random.randint(10, self.size[1] - 100)))
            
        one = random.randint(10, self.size[0] - 100)
        two = random.randint(10, self.size[1] - 100)
        r = Image.open(t[1])
        r = r.resize((random.randint(self.maxH[0], self.maxH[1]), random.randint(self.maxW[0], self.maxW[1])))
        if self.rotate_im:
            r = r.rotate(random.randint(-360, 360), expand=True)

        if self.noise_im:
            r = noise(r, random.uniform(0.001, 0.1))
        bg.paste(r, (one, two))
        
        self.captcha = bg

        return {"class": t[0], "file": t[1], "position": (one, two)}

    def save(self, path: str, mode: str = None):
        if self.captcha != None:
            if mode == None:
                self.captcha.save(path)
                return 1
            elif mode == "base64":
                im_file = io.BytesIO()
                self.captcha.save(im_file, format="PNG")
                im_bytes = im_file.getvalue() 
                if path != None:
                    self.captcha = None
                    with open(path, 'ab') as p:
                        p.write(base64.b64encode(im_bytes))
                    return 1
                else:
                    self.captcha = None
                    return str(base64.b64encode(im_bytes)).replace("b'", "")
            else:
                raise ValueError('The "mode" parameter is exclusively None or "base64"')