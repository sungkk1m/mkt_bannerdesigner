"""Install Plz text-plate generator.

Extracts the text bands from the reference memes as pixel-exact "text plates"
(character region removed, white background), so the tool can swap only the SD
character while keeping the meme font 100% unmodified.

Design Ref: docs/02-design/features/install-plz.design.md §1
Usage:  python3 make_plates.py <ref_dir>
        <ref_dir> must contain {한|영|일|번}_UD_설치구걸_{1080x1080|1200x628}.png
Output: text-plate_{ko|en|ja|zh-TW}_{1x1|1200x628}.png next to this script.

NOTE (Plan R-04): the crop boundaries below are measured for the 2026-07-19
Underdark:Defense reference set only. A new reference set needs re-measurement
(see docs/01-plan/features/install-plz.plan.md "사전 검증 결과" for the method).
"""
import os
import sys

import numpy as np
from PIL import Image

LANGS = {"ko": "한", "en": "영", "ja": "일", "zh-TW": "번"}

# 1080x1080: keep top band [0..Y1) + bottom band [Y2..1080), erase the rest.
SPEC_1X1 = {
    "ko":    {"Y1": 212, "Y2": 811},
    "en":    {"Y1": 252, "Y2": 823},  # bottom text is 2 lines (835..1010)
    "ja":    {"Y1": 245, "Y2": 823},
    "zh-TW": {"Y1": 245, "Y2": 823},
}
# 1200x628: keep left text rect [0..X1) x [0..Y1200); ref is 1200x625 -> pad
# 3 white rows at the bottom (no scaling, keeps text pixels 1:1).
SPEC_1200 = {"ko": 631, "en": 612, "ja": 624, "zh-TW": 549}
Y1200 = 553
# ko disclaimer ("확률형 아이템 포함") sits over the character column at the
# top-right; re-stamp it from the source after erasing the character region.
KO_DISCLAIMER_RECT = (1050, 8, 1192, 40)


def blue_key_clean(img):
    """Erase watery-blue pixels (rain drops / puddle tips bleeding into the
    text crops). Text is black/white/red/gray only, so it is never touched."""
    a = np.asarray(img).astype(np.int16)
    mask = (a[..., 2] - a[..., 0] > 50) & (a[..., 2] > 140)
    a[mask] = 255
    return Image.fromarray(a.astype(np.uint8))


def main(ref_dir):
    out_dir = os.path.dirname(os.path.abspath(__file__))
    for lang, prefix in LANGS.items():
        # --- 1x1 (1080x1080) ---
        ref = Image.open(os.path.join(ref_dir, f"{prefix}_UD_설치구걸_1080x1080.png")).convert("RGB")
        s = SPEC_1X1[lang]
        plate = Image.new("RGB", (1080, 1080), (255, 255, 255))
        plate.paste(ref.crop((0, 0, 1080, s["Y1"])), (0, 0))
        plate.paste(ref.crop((0, s["Y2"], 1080, 1080)), (0, s["Y2"]))
        plate = blue_key_clean(plate)
        plate.save(os.path.join(out_dir, f"text-plate_{lang}_1x1.png"), optimize=True)

        # --- 1200x628 (ref is 1200x625) ---
        ref = Image.open(os.path.join(ref_dir, f"{prefix}_UD_설치구걸_1200x628.png")).convert("RGB")
        plate = Image.new("RGB", (1200, 628), (255, 255, 255))
        plate.paste(ref.crop((0, 0, SPEC_1200[lang], Y1200)), (0, 0))
        plate = blue_key_clean(plate)
        if lang == "ko":
            x0, y0, x1, y1 = KO_DISCLAIMER_RECT
            plate.paste(ref.crop((x0, y0, x1, y1)), (x0, y0))
        plate.save(os.path.join(out_dir, f"text-plate_{lang}_1200x628.png"), optimize=True)
        print(f"{lang}: ok")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
