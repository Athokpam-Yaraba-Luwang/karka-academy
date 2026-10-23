# Karka AI & Tech Academy website · SiteSprint, Karka Infini AI 2026
# Built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
"""Generate the Open Graph share card from the brand assets. Run: python tools/make_images.py

Favicons / app icons (icon-*.png), the logo and the mascot are hand-prepared assets
in app/static/img and are not regenerated here.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

IMG = Path(__file__).resolve().parent.parent / "app" / "static" / "img"
# Bold fonts that include the ₹ (U+20B9) glyph; Arial Bold does not and renders a box.
FONTS = [
    ("/System/Library/Fonts/HelveticaNeue.ttc", 1),               # macOS: Helvetica Neue Bold
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0),  # Linux
]


def font(size):
    for path, index in FONTS:
        if Path(path).exists():
            return ImageFont.truetype(path, size, index=index)
    return ImageFont.load_default(size)


def og():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), (28, 5, 38))
    d = ImageDraw.Draw(img)
    for x in range(0, w, 44):
        d.line([(x, 0), (x, h)], fill=(40, 12, 54))
    for y in range(0, h, 44):
        d.line([(0, y), (w, y)], fill=(40, 12, 54))

    glow = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(glow)
    for r in range(320, 0, -8):
        a = int(70 * (1 - r / 320))
        gd.ellipse([930 - r, 330 - r, 930 + r, 330 + r], fill=(155, 77, 255, a))
    img.paste(glow, (0, 0), glow)

    logo = Image.open(IMG / "karka-logo-light.webp").convert("RGBA")
    logo = logo.resize((round(logo.width * 70 / logo.height), 70), Image.LANCZOS)
    img.paste(logo, (64, 56), logo)

    bot = Image.open(IMG / "mascot-640.webp").convert("RGBA")
    bot = bot.resize((round(bot.width * 560 / bot.height), 560), Image.LANCZOS)
    img.paste(bot, (w - bot.width - 70, h - bot.height + 20), bot)

    d.text((64, 196), "Your future,", font=font(84), fill="white")
    d.text((64, 290), "powered by AI.", font=font(84), fill=(255, 95, 210))
    d.rounded_rectangle([64, 440, 600, 512], radius=36, fill=(255, 210, 63))
    d.text((96, 457), "₹0 upfront · Pay after placement", font=font(28), fill=(28, 5, 38))
    d.text((64, 548), "Fullstack · Gen AI · Data · UI/UX  ·  Nagercoil", font=font(26), fill=(212, 184, 255))
    # JPEG keeps it well under WhatsApp's ~300 KB link-preview limit
    img.save(IMG / "og.jpg", quality=86, optimize=True, progressive=True)


if __name__ == "__main__":
    og()
    print("ok")
