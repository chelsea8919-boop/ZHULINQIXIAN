from PIL import Image, ImageOps, ImageDraw, ImageEnhance
import os

base = "C:/Users/Ms.赵/WorkBuddy/2026-10-04-task-9/assets"
p1 = os.path.join(base, "拼1.png")
p2 = os.path.join(base, "拼2.png")
out = os.path.join(base, "hero-combined.png")

i1 = Image.open(p1).convert("RGBA")
i2 = Image.open(p2).convert("RGBA")

target_w = 1600

def scale_to_width(img, w):
    ratio = w / img.width
    new_h = int(round(img.height * ratio))
    return img.resize((w, new_h), Image.LANCZOS)

s1 = scale_to_width(i1, target_w)
s2 = scale_to_width(i2, target_w)

combined_h = s1.height + s2.height
combined = Image.new("RGBA", (target_w, combined_h), (235, 243, 232, 255))
combined.paste(s1, (0, 0), s1)
combined.paste(s2, (0, s1.height), s2)

# Convert to grayscale, then colorize with a bamboo-green duotone
gray = combined.convert("RGB").convert("L")
line_green = (26, 112, 64)        # 鲜竹绿，用于线条
paper_green = (232, 250, 226)    # 亮青纸色，用于背景
colorized = ImageOps.colorize(gray, line_green, paper_green)

# Build a subtle radial vignette: center stays clear, edges gently darken
vignette = Image.new("L", (target_w, combined_h), 0)
draw = ImageDraw.Draw(vignette)
cx, cy = target_w // 2, combined_h // 2
max_r = int((target_w**2 + combined_h**2) ** 0.5 / 2)
# Draw from outside in: outer rings are bright (more overlay), inner rings are dark (no overlay)
for r in range(max_r, 0, -3):
    alpha = int(90 * ((r / max_r) ** 2.0))
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=alpha)

# Composite a dark green overlay only where the vignette mask is bright (edges)
edge_color = Image.new("RGB", (target_w, combined_h), (30, 92, 52))
result = Image.composite(edge_color, colorized, vignette)

# Very faint grain for relic texture
noise = Image.effect_noise((target_w, combined_h), 10).convert("L")
noise = noise.point(lambda x: x if x > 235 else 0)
noise_color = Image.new("RGB", (target_w, combined_h), (70, 135, 85))
result = Image.composite(noise_color, result, noise)

# Boost brightness and color to make the green tones feel fresher
result = ImageEnhance.Brightness(result).enhance(1.06)
result = ImageEnhance.Color(result).enhance(1.18)

# Gentle autocontrast to keep tones clean
result = ImageOps.autocontrast(result, cutoff=0.3)

result.save(out, "PNG")
print("Saved", out, result.size)
