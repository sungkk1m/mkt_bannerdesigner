from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "siaan3_nochrome_stats_1080x1080.png"

W = H = 1080
BLUE = (0, 122, 255, 255)
TEXT = (0, 0, 0, 255)
SECONDARY = (108, 108, 114, 255)
TERTIARY = (142, 142, 147, 255)
DIVIDER = (229, 229, 234, 255)
ICON_BG = (244, 244, 249, 255)
CARD_BG = (255, 255, 255, 255)


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default(size=size)


KOREAN_FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
LATIN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LATIN_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

font_title = font(LATIN_BOLD, 62)
font_subtitle = font(KOREAN_FONT, 28)
font_cta = font(KOREAN_FONT, 33)
font_iap = font(KOREAN_FONT, 25)
font_stat_label = font(KOREAN_FONT, 22)
font_stat_value = font(LATIN_BOLD, 40)
font_stat_bot = font(KOREAN_FONT, 21)


def rounded_shadow(base, box, radius, blur, offset_y, alpha):
    x0, y0, x1, y1 = box
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x0, y0 + offset_y, x1, y1 + offset_y), radius=radius, fill=(0, 0, 0, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow)


def draw_center(draw, xy, text, fill, fnt):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x - tw / 2, y - th / 2 - bbox[1] / 2), text, fill=fill, font=fnt)


def draw_star(draw, cx, cy, r_outer=10, r_inner=4.4, fill=TERTIARY):
    pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw.polygon(pts, fill=fill)


def draw_ranking_icon(draw, cx, cy, color=TERTIARY):
    pts = [(cx - 20, cy + 7), (cx - 12, cy - 1), (cx - 4, cy + 5), (cx + 8, cy - 11), (cx + 17, cy - 2), (cx + 22, cy - 12)]
    draw.line(pts, fill=color, width=4, joint="curve")


def draw_developer_icon(draw, cx, cy, color=TERTIARY):
    draw.ellipse((cx - 8, cy - 21, cx + 8, cy - 5), fill=color)
    draw.rounded_rectangle((cx - 23, cy - 1, cx + 23, cy + 25), radius=12, fill=color)


def cover_resize(img, size):
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def paste_rounded(base, img, box, radius):
    x, y, w, h = box
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    base.paste(img.convert("RGBA"), (x, y), mask)


def main():
    keyart_candidates = [p for p in ROOT.glob("*1200x628.png") if p.name != OUT.name]
    if not keyart_candidates:
        raise FileNotFoundError("No 1200x628 keyart asset found in appstore-square assets")
    keyart_src = keyart_candidates[0]

    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # App icon placeholder, matching the no-chrome draft.
    icon_x, icon_y, icon_s = 50, 49, 242
    rounded_shadow(canvas, (icon_x, icon_y, icon_x + icon_s, icon_y + icon_s), 52, 24, 10, 34)
    draw.rounded_rectangle((icon_x, icon_y, icon_x + icon_s, icon_y + icon_s), radius=52, fill=ICON_BG)

    # App info.
    tx = 324
    draw.text((tx, 77), "Superplanet", fill=TEXT, font=font_title)
    draw.text((tx, 148), "롤플레잉", fill=SECONDARY, font=font_subtitle)
    cta_x, cta_y, cta_w, cta_h = tx, 194, 168, 59
    draw.rounded_rectangle((cta_x, cta_y, cta_x + cta_w, cta_y + cta_h), radius=30, fill=BLUE)
    draw_center(draw, (cta_x + cta_w / 2, cta_y + cta_h / 2 + 1), "받기", (255, 255, 255, 255), font_cta)
    draw.text((514, 206), "앱 내 구입 · 확률형 아이템 포함", fill=SECONDARY, font=font_iap)

    # Store meta row: rating, age, chart, developer.
    stats_y, stats_h = 322, 144
    draw.rectangle((0, stats_y, W, stats_y + 1), fill=DIVIDER)
    draw.rectangle((0, stats_y + stats_h, W, stats_y + stats_h + 1), fill=DIVIDER)
    col_w = W / 4
    for i in range(1, 4):
        x = round(col_w * i)
        draw.rectangle((x, stats_y + 16, x + 1, stats_y + stats_h - 16), fill=DIVIDER)

    labels = ["3.8천", "연령", "차트", "개발자"]
    values = ["4.8", "4+", "", ""]
    bottoms = ["", "세", "#2", "SeungHo"]
    label_y = stats_y + 25
    value_y = stats_y + 70
    bot_y = stats_y + 116
    for i in range(4):
        cx = col_w * (i + 0.5)
        draw_center(draw, (cx, label_y), labels[i], SECONDARY, font_stat_label)
        if values[i]:
            draw_center(draw, (cx, value_y), values[i], TERTIARY, font_stat_value)
        if i == 0:
            star_total = 5 * 20 + 4 * 4
            start_x = cx - star_total / 2 + 10
            for s in range(5):
                draw_star(draw, start_x + s * 24, bot_y - 2, 9.5, 4.2, TERTIARY)
        elif i == 2:
            draw_ranking_icon(draw, cx, value_y + 1, TERTIARY)
            draw_center(draw, (cx, bot_y), bottoms[i], SECONDARY, font_stat_bot)
        elif i == 3:
            draw_developer_icon(draw, cx, value_y + 6, TERTIARY)
            draw_center(draw, (cx, bot_y), bottoms[i], SECONDARY, font_stat_bot)
        else:
            draw_center(draw, (cx, bot_y), bottoms[i], SECONDARY, font_stat_bot)

    # Keyart card from the repo asset.
    keyart_x, keyart_y, keyart_w, keyart_h = 50, 514, 980, 510
    rounded_shadow(canvas, (keyart_x, keyart_y, keyart_x + keyart_w, keyart_y + keyart_h), 28, 36, 12, 18)
    draw.rounded_rectangle((keyart_x, keyart_y, keyart_x + keyart_w, keyart_y + keyart_h), radius=28, fill=CARD_BG)
    keyart = Image.open(keyart_src).convert("RGBA")
    keyart_fit = cover_resize(keyart, (keyart_w, keyart_h))
    paste_rounded(canvas, keyart_fit, (keyart_x, keyart_y, keyart_w, keyart_h), 28)

    canvas.convert("RGB").save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
