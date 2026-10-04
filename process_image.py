from PIL import Image, ImageOps, ImageFilter, ImageDraw
import os, random

base = "C:/Users/Ms.赵/WorkBuddy/2026-10-04-task-9/assets"
p1 = os.path.join(base, "拼1.png")
p2 = os.path.join(base, "拼2.png")
out = os.path.join(base, "hero-combined.png")

i1 = Image.open(p1).convert("RGBA")
i2 = Image.open(p2).convert("RGBA")

target_w = 1400

def scale_to_width(img, w):
    ratio = w / img.width
    new_h = int(round(img.height * ratio))
    return img.resize((w, new_h), Image.LANCZOS)

s1 = scale_to_width(i1, target_w)
s2 = scale_to_width(i2, target_w)

combined_h = s1.height + s2.height
combined = Image.new("RGBA", (target_w, combined_h), (232, 242, 229, 255))
# paste centered vertically? both scaled to same width, so x=0
combined.paste(s1, (0, 0), s1)
combined.paste(s2, (0, s1.height), s2)

# Convert to RGB then grayscale
gray = combined.convert("RGB").convert("L")

# Colorize: dark tones -> deep bamboo green, light tones -> pale celadon
line_green = (18, 55, 35)        # 深竹绿
paper_green = (228, 240, 224)    # 瓷青纸色
colorized = ImageOps.colorize(gray, line_green, paper_green)

# Add a subtle green vignette
vignette = Image.new("L", (target_w, combined_h), 0)
draw = ImageDraw.Draw(vignette)
cx, cy = target_w // 2, combined_h // 2
max_r = int((target_w**2 + combined_h**2) ** 0.5 / 2)
for r in range(max_r, 0, -4):
    alpha = int(255 * (r / max_r) ** 1.4)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=alpha)
# Invert so edges are darker
vignette = ImageOps.invert(vignette)
# Apply vignette as an overlay with low opacity
vignette_color = Image.new("RGB", (target_w, combined_h), (10, 35, 20))
result = Image.composite(vignette_color, colorized, vignette)

# Add a very faint grain/noise texture for museum relic feel
noise = Image.effect_noise((target_w, combined_h), 8).convert("L")
noise = noise.point(lambda x: x if x > 220 else 0)  # mostly transparent, sparse specks
noise_color = Image.new("RGB", (target_w, combined_h), (35, 70, 45))
result = Image.composite(noise_color, result, noise)

# Slight contrast boost
result = ImageOps.autocontrast(result, cutoff=0.5)

result.save(out, "PNG")
print("Saved", out, result.size)
