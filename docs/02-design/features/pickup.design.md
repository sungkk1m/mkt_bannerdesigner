# PDCA Design — Pickup 템플릿 (v1.8)

**Feature**: `pickup`
**Created**: 2026-05-05
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/pdca design`
**Upstream**: [`docs/01-plan/features/pickup.plan.md`](../../01-plan/features/pickup.plan.md)
**Architecture (selected)**: **Option C — Pragmatic Balance** (`PICKUP_HELPERS` 객체 + 글로벌 빌더, KVR v1.7 패턴 일관)

---

## Context Anchor (propagated from Plan)

| Key | Value |
|-----|-------|
| **WHY** | 신규/픽업 캐릭터를 강조하면서 등급·속성·클래스·캐릭터명을 같이 노출하는 광고 배너 템플릿 부재 — 디자이너 수작업으로 4언어×2사이즈=8장 생산 비효율 |
| **WHO** | UA Manager (Superplanet 사내 마케팅), 잠재적으로 다른 사내 게임 픽업 광고 운영자 |
| **RISK** | 번들 PNG(name-frame×2, star) 디자이너 미제공 시점 placeholder 필요 (R-1) / 다국어 텍스트 길이 차이로 프레임 영역 초과 (R-2) / 1200×628 가로 비율에서 정사각 캐릭터 PNG 비율 왜곡 (R-3) |
| **SUCCESS** | 단건 ≤1초, 배치 8장 ZIP ≤2초; 8장 레퍼런스 비주얼 일치 (±5%); CTA 4언어 자동 매핑; 슬라이더 6개 실시간; 회귀 0건 |
| **SCOPE** | Session 1: data-switch / Session 2: canvas-renderer / Session 3: single-ui / Session 4: batch-ui-zip |

---

## Architecture (Selected: Option C — Pragmatic Balance)

| 측면 | 결정 |
|---|---|
| CSS 명명 | 기존 sd-showcase/KVR 동일 패턴 — `.banner.tmpl-pickup .pickup-{slot}` |
| HTML | 기존 `data-tmpl="..."` / `data-tmpl-hide` 패턴 그대로 |
| JS 분기 | 기존 render switch에 `case 'pickup'` 추가, canvas dispatcher에도 `pickup` 분기 |
| Helper 함수 | **분리** → `const PICKUP_HELPERS = { fitText, drawGradientText, drawStarRow, getFramePath }` (KVR_HELPERS 패턴) |
| 빌더 함수 | 글로벌 — `buildPickupCfg`, `prepPickupCfgImages`, `buildPickupCanvas`, `buildPickupBanner`, `buildPickupFilename` (sd-showcase 패턴) |
| LANG_PACK | 신설 — `PICKUP_CTA_MAP` (4언어 CTA 고정 매핑) |
| 자산 | 외부 PNG `repo/assets/pickup/{name-frame-1x1, name-frame-1200x628, star}.png` (KVR 자산 분리 패턴) |
| State | `state.single.pickup` + `state.batch.pickup` (KVR R13 배치 자산 분리) |
| 추정 코드량 | CSS ~80 + HTML ~200 + JS ~420 ≈ **+700라인** (기존 7,169 → ~7,870) |

---

## 1. Overview

### 1080×1080 (정사각)
```
┌─────────────────────────────────────────┐  1080×1080
│ [LOGO]                                  │  ← 게임 로고 (X/Y/Scale slider, default 좌측 상단)
│                                         │
│                                         │
│                          [CHARACTER]    │  ← 캐릭터 일러스트 (X/Y/Scale slider)
│                            transparent  │     중앙-우측 큰 비중
│                            PNG          │
│                                         │
│         {character description}         │  ← 캐릭터 설명 (i18n, drop-shadow)
│       ┏━━━━━━━━━━━━━━━━━━━━━━━━━┓     │
│       ┃   {NAME (gradient)}      ┃     │  ← 이름 프레임 (번들 PNG, name-frame-1x1.png)
│       ┃  ★★★★★ │ {ele} {cls}    ┃     │     캐릭터명·별·속성·클래스 텍스트 오버레이
│       ┗━━━━━━━━━━━━━━━━━━━━━━━━━┛     │
│         {지금 플레이하세요 (CTA)}        │  ← CTA (코드 고정 매핑, 흰 + drop-shadow)
└─────────────────────────────────────────┘
                ↑ 배경: 사용자 업로드 키아트 (cover)
```

### 1200×628 (가로형)
```
┌────────────────────────────────────────────────────────────┐  1200×628
│ [LOGO]                                                      │  ← 좌측 상단
│                                                             │
│   {character description}                                   │  ← 좌측 텍스트 영역
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━┓                                │
│ ┃   {NAME (gradient)}      ┃             [CHARACTER]        │  ← 이름 프레임 (좌측)
│ ┃  ★★★★★ │ {ele} {cls}    ┃                                │     + 캐릭터 (우측)
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━┛                                │
│     {지금 플레이하세요 (CTA)}                                 │  ← 좌측 하단 CTA
└────────────────────────────────────────────────────────────┘
                ↑ 배경: 사용자 업로드 키아트 (cover)
```

> **결정**: 두 사이즈 모두 동일 정보(로고/설명/이름프레임/CTA + 캐릭터)이지만 배치만 다름.
> 1080×1080은 수직 흐름 + 캐릭터 우측 큰 비중. 1200×628은 좌측 텍스트 + 우측 캐릭터 분할.

---

## 2. Canvas 좌표 사양 (`PICKUP_CANVAS_SPECS`)

> 모든 좌표는 캔버스 기본값. 사용자 슬라이더로 ±offset 적용.
> 배경 키아트는 `drawImageCover` (사이즈별 자동 fit). 사용자 슬라이더 없음.

### 2.1 1080×1080 좌표

```js
'1x1': {
  w: 1080, h: 1080,
  bg: { fit: 'cover' },                                          // 배경 키아트
  logo: {
    defaultX: 80, defaultY: 80,                                  // 좌측 상단 (X/Y slider 0)
    defaultMaxW: 280, defaultMaxH: 120,                          // contain (Scale 100% 기준)
  },
  character: {
    defaultCx: 720, defaultCy: 480,                              // 우측-중앙 (X/Y slider 0)
    defaultMaxW: 760, defaultMaxH: 920,                          // contain
  },
  desc: {
    cx: 540, y: 700, maxW: 760, fontSize: 36,                    // 프레임 위 캐릭터 설명
    align: 'center', shadow: '0 4px 12px rgba(0,0,0,0.7)',
  },
  frame: {
    cx: 540, cy: 820, w: 760, h: 220,                            // 이름 프레임 PNG 위치/크기
    asset: 'assets/pickup/name-frame-1x1.png',
  },
  name: {
    cx: 540, cy: 800, maxW: 640, baseFs: 88, minFs: 56,          // 프레임 안 캐릭터명 (그라디언트)
    align: 'center',
  },
  stars: {
    cx: 410, cy: 880, starSize: 44, gap: 8,                      // 프레임 안 별 5개 (좌측)
    asset: 'assets/pickup/star.png',
  },
  elementClass: {
    x: 600, cy: 880, fontSize: 28, separator: '|',               // 프레임 안 속성/클래스 (우측)
    color: '#FFFFFF',
  },
  cta: {
    cx: 540, y: 1010, fontSize: 44,                              // 최하단 중앙
    align: 'center', color: '#FFFFFF',
    shadow: '0 4px 16px rgba(0,0,0,0.6)',
  },
},
```

### 2.2 1200×628 좌표

```js
'1200x628': {
  w: 1200, h: 628,
  bg: { fit: 'cover' },
  logo: {
    defaultX: 60, defaultY: 50,
    defaultMaxW: 200, defaultMaxH: 90,
  },
  character: {
    defaultCx: 880, defaultCy: 314,                              // 우측 영역
    defaultMaxW: 600, defaultMaxH: 580,
  },
  desc: {
    cx: 320, y: 230, maxW: 520, fontSize: 26,
    align: 'center', shadow: '0 3px 10px rgba(0,0,0,0.7)',
  },
  frame: {
    cx: 320, cy: 360, w: 540, h: 170,
    asset: 'assets/pickup/name-frame-1200x628.png',
  },
  name: {
    cx: 320, cy: 345, maxW: 440, baseFs: 64, minFs: 40,
    align: 'center',
  },
  stars: {
    cx: 200, cy: 410, starSize: 32, gap: 6,
    asset: 'assets/pickup/star.png',
  },
  elementClass: {
    x: 360, cy: 410, fontSize: 20, separator: '|',
    color: '#FFFFFF',
  },
  cta: {
    cx: 320, y: 560, fontSize: 32,
    align: 'center', color: '#FFFFFF',
    shadow: '0 3px 12px rgba(0,0,0,0.6)',
  },
},
```

> **사용자 슬라이더 적용 방식**:
> - `logo.x = defaultX + state.logoX`, `logo.y = defaultY + state.logoY`
> - `logo.scaleFactor = state.logoScale / 100` → `maxW *= scaleFactor`, `maxH *= scaleFactor`
> - `character.cx = defaultCx + state.charX`, 동일 방식
> - 슬라이더 범위: X/Y ±200px, Scale 50~150%

---

## 3. CSS Class 트리

```
.banner.tmpl-pickup                                  /* 루트 */
├── .pickup-bg                                       /* 배경 키아트 (img, cover) */
│   └── img
├── .pickup-character                                /* 캐릭터 일러스트 wrapper */
│   └── img                                          /* X/Y/scale transform */
├── .pickup-logo                                     /* 게임 로고 wrapper */
│   └── img                                          /* X/Y/scale transform */
├── .pickup-desc                                     /* 캐릭터 설명 텍스트 */
├── .pickup-frame-area                               /* 이름 프레임 영역 (PNG + 오버레이) */
│   ├── .pickup-frame-img                            /* 번들 frame PNG (background-image) */
│   ├── .pickup-name                                 /* 캐릭터명 (그라디언트 텍스트) */
│   ├── .pickup-stars                                /* 별 5개 컨테이너 */
│   │   └── img × 5                                  /* star.png 5번 */
│   └── .pickup-element-class                        /* "{ele} | {cls}" */
└── .pickup-cta                                      /* CTA 텍스트 */
```

CSS 사이즈별 분기:
- `.banner.tmpl-pickup.size-1x1 { ... }` — 1080×1080 위치/폰트 크기
- `.banner.tmpl-pickup.size-1200x628 { ... }` — 1200×628 위치/폰트 크기
- `.banner.tmpl-pickup[data-lang="ja"] .pickup-name { font-family: 'Noto Sans JP', ... }`
- `.banner.tmpl-pickup[data-lang="zh-TW"] .pickup-name { font-family: 'Noto Sans TC', ... }`

---

## 4. JS Helper 함수 시그니처 (`PICKUP_HELPERS`)

### 4.1 `fitText(ctx, text, maxW, baseFs, minFs, fontFamily, weight): number`

자동 폰트 축소 (sd-showcase `fitSdsTitle` 패턴 준용).

```js
fitText(ctx, text, maxW, baseFs, minFs = 24, fontFamily, weight = '700') {
  let fs = baseFs;
  while (fs > minFs) {
    ctx.font = `${weight} ${fs}px ${fontFamily}`;
    const w = ctx.measureText(text).width;
    if (w <= maxW) return fs;
    fs -= 2;
  }
  return minFs;
}
```

### 4.2 `drawGradientText(ctx, text, x, y, fs, fontFamily, weight, gradTop, gradBottom): void`

그라디언트 텍스트 + 그림자.

```js
drawGradientText(ctx, text, x, y, fs, fontFamily, weight, gradTop, gradBottom) {
  ctx.font = `${weight} ${fs}px ${fontFamily}`;
  const grad = ctx.createLinearGradient(0, y - fs * 0.4, 0, y + fs * 0.6);
  grad.addColorStop(0, gradTop);
  grad.addColorStop(1, gradBottom);
  ctx.fillStyle = grad;
  ctx.shadowColor = 'rgba(0,0,0,0.5)';
  ctx.shadowBlur = 8;
  ctx.shadowOffsetY = 4;
  ctx.fillText(text, x, y);
  ctx.shadowColor = 'transparent';
}
```

### 4.3 `drawStarRow(ctx, starImg, cx, cy, count, starSize, gap): void`

5개 별 자동 스케일·정렬.

```js
drawStarRow(ctx, starImg, cx, cy, count = 5, starSize, gap) {
  if (!starImg || starImg.naturalWidth === 0) {
    // placeholder fallback (자산 누락 시): ★ Unicode 텍스트
    ctx.font = `${starSize}px serif`;
    ctx.fillStyle = '#FFD700';
    ctx.textAlign = 'center';
    ctx.fillText('★'.repeat(count), cx, cy + starSize * 0.3);
    return;
  }
  const totalW = starSize * count + gap * (count - 1);
  const startX = cx - totalW / 2;
  for (let i = 0; i < count; i++) {
    const x = startX + i * (starSize + gap);
    ctx.drawImage(starImg, x, cy - starSize / 2, starSize, starSize);
  }
}
```

### 4.4 `getFramePath(size): string`

사이즈별 번들 프레임 PNG 경로 반환.

```js
getFramePath(size) {
  return PICKUP_ASSETS.frame[size] || PICKUP_ASSETS.frame['1x1'];
}
```

### 4.5 `drawFramePlaceholder(ctx, frameSpec): void` (자산 누락 시)

번들 프레임 PNG 미제공 시 placeholder rect 그리기 (개발용).

```js
drawFramePlaceholder(ctx, frameSpec) {
  ctx.strokeStyle = '#FFD700';
  ctx.lineWidth = 4;
  ctx.strokeRect(
    frameSpec.cx - frameSpec.w / 2,
    frameSpec.cy - frameSpec.h / 2,
    frameSpec.w, frameSpec.h
  );
}
```

---

## 5. LANG_PACK + CTA 매핑 설계

### 5.1 `PICKUP_CTA_MAP` (코드 고정 매핑)

```js
const PICKUP_CTA_MAP = {
  'ko':    '지금 플레이하세요',
  'en':    'Play Now',
  'ja':    '今すぐプレイ',
  'zh-TW': '立即遊玩',
};
```

> 사용자 결정 #13 — 코드 고정, 사용자 수정 불가. 언어 전환 시 자동 변경.

### 5.2 `PICKUP_ASSETS` (번들 자산 경로)

```js
const PICKUP_ASSETS = {
  frame: {
    '1x1':      'assets/pickup/name-frame-1x1.png',
    '1200x628': 'assets/pickup/name-frame-1200x628.png',
  },
  star: 'assets/pickup/star.png',
};
```

### 5.3 기존 `LANG_PACK` 재사용

폰트 자동 스왑은 기존 `getFontFamilyForLang(lang)` 헬퍼 그대로 활용:
- `ko`/`en` → Pretendard
- `ja` → Noto Sans JP
- `zh-TW` → Noto Sans TC

---

## 6. 데이터 모델 (입력)

```ts
type PickupCommon = {
  // 사용자 업로드 (한 장 공용, 두 사이즈에 자동 적용)
  logo: string | null,        // dataURL
  keyart: string | null,
  character: string | null,

  // 게임 로고 위치/크기
  logoX: number,              // -200..+200 (px offset)
  logoY: number,
  logoScale: number,          // 50..150 (%)

  // 캐릭터 위치/크기
  charX: number,              // -200..+200
  charY: number,
  charScale: number,          // 50..150

  // 캐릭터명 그라디언트 (사용자 색상 선택)
  nameGradTop: string,        // hex, default '#FFD700'
  nameGradBottom: string,     // hex, default '#FFFFFF'
};

type PickupPerLang = {
  description: string,        // "운명의 힘을 품은 구미호"
  name: string,               // "미나"
  element: string,            // "불"
  class: string,              // "원거리"
};

type PickupInput = PickupCommon & {
  langs: {
    ko:    PickupPerLang,
    en:    PickupPerLang,
    ja:    PickupPerLang,
    'zh-TW': PickupPerLang,
  },
};

// PICKUP_DEFAULT 초기값
const PICKUP_DEFAULT = {
  logo: null, keyart: null, character: null,
  logoX: 0, logoY: 0, logoScale: 100,
  charX: 0, charY: 0, charScale: 100,
  nameGradTop: '#FFD700', nameGradBottom: '#FFFFFF',
  langs: {
    'ko':    { description: '', name: '', element: '', class: '' },
    'en':    { description: '', name: '', element: '', class: '' },
    'ja':    { description: '', name: '', element: '', class: '' },
    'zh-TW': { description: '', name: '', element: '', class: '' },
  },
};
```

---

## 7. 입력 폼 UX (line ~1700 부근, KVR 다음에 삽입)

### 7.1 단건 모드 (`data-tmpl="pickup"`)

```
[Pickup 입력 폼]
├── 자산 업로드
│   ├── 게임 로고 dropzone (#s-drop-pickup-logo)
│   │   + X/Y/Scale 슬라이더 3개
│   ├── 배경 키아트 dropzone (#s-drop-pickup-keyart)
│   │   (슬라이더 없음, cover 자동)
│   └── 캐릭터 일러스트 dropzone (#s-drop-pickup-character)
│       + X/Y/Scale 슬라이더 3개
├── 캐릭터명 그라디언트
│   ├── 상단 색상 picker (#s-pickup-name-grad-top, default #FFD700)
│   └── 하단 색상 picker (#s-pickup-name-grad-bottom, default #FFFFFF)
└── 다국어 텍스트 (현재 선택된 언어만 노출)
    ├── 캐릭터 설명 input (#s-pickup-desc)
    ├── 캐릭터명 input (#s-pickup-name)
    ├── 속성 input (#s-pickup-element)
    └── 클래스 input (#s-pickup-class)
```

### 7.2 배치 모드 (`data-tmpl="pickup"`, prefix `b-`)

```
[Pickup 배치 입력 폼]
├── 자산 업로드 (별도, state.batch.pickup 저장)
│   ├── 게임 로고 dropzone (#b-drop-pickup-logo) + 3 slider
│   ├── 배경 키아트 dropzone (#b-drop-pickup-keyart)
│   └── 캐릭터 일러스트 dropzone (#b-drop-pickup-character) + 3 slider
├── 캐릭터명 그라디언트 (#b-pickup-name-grad-top/bottom)
├── 사이즈 체크박스 (1x1 + 1200x628, 9:16 disabled)
├── 언어 체크박스 (ko/en/ja/zh-TW, 기본 모두 ON)
└── 언어별 텍스트 입력 (renderBatchLangFields() pickup 분기)
    └── 각 체크된 언어마다:
        ├── 캐릭터 설명 input
        ├── 캐릭터명 input
        ├── 속성 input
        └── 클래스 input
```

---

## 8. 렌더링 분기 (Canvas dispatcher + render switch)

기존 canvas dispatcher (`buildBannerCanvas` 또는 유사 분기 함수)에 `pickup` 분기 추가.

### 8.1 Canvas 빌더 (`buildPickupCanvas(cfg)`)

10단계 그리기 순서 (FR-14 정의):

```js
async function buildPickupCanvas(cfg) {
  const spec = PICKUP_CANVAS_SPECS[cfg.size];
  const canvas = document.createElement('canvas');
  canvas.width = spec.w;
  canvas.height = spec.h;
  const ctx = canvas.getContext('2d');
  const fontFamily = getFontFamilyForLang(cfg.lang);

  // [1] 배경 (검정 fallback or 사용자 키아트)
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, spec.w, spec.h);

  // [2] 배경 키아트 (cover)
  if (cfg.bgImg) {
    drawImageCover(ctx, cfg.bgImg, 0, 0, spec.w, spec.h);
  }

  // [3] 캐릭터 일러스트 (X/Y/scale 슬라이더 적용)
  if (cfg.characterImg) {
    const cs = spec.character;
    const sf = cfg.charScale / 100;
    const cw = cs.defaultMaxW * sf;
    const ch = cs.defaultMaxH * sf;
    const cx = cs.defaultCx + cfg.charX;
    const cy = cs.defaultCy + cfg.charY;
    drawImageContain(ctx, cfg.characterImg, cx - cw/2, cy - ch/2, cw, ch);
  }

  // [4] 게임 로고 (X/Y/scale 슬라이더 적용)
  if (cfg.logoImg) {
    const ls = spec.logo;
    const sf = cfg.logoScale / 100;
    const lw = ls.defaultMaxW * sf;
    const lh = ls.defaultMaxH * sf;
    drawImageContain(ctx, cfg.logoImg,
      ls.defaultX + cfg.logoX, ls.defaultY + cfg.logoY, lw, lh);
  }

  // [5] 캐릭터 설명 (drop-shadow + i18n)
  const desc = cfg.langs[cfg.lang].description;
  if (desc) {
    ctx.fillStyle = '#FFFFFF';
    ctx.font = `400 ${spec.desc.fontSize}px ${fontFamily}`;
    ctx.textAlign = 'center';
    ctx.shadowColor = 'rgba(0,0,0,0.7)';
    ctx.shadowBlur = 12; ctx.shadowOffsetY = 4;
    ctx.fillText(desc, spec.desc.cx, spec.desc.y);
    ctx.shadowColor = 'transparent';
  }

  // [6] 이름 프레임 PNG (사이즈별 자산 로드, _imgCache 활용)
  const f = spec.frame;
  if (cfg.frameImg) {
    ctx.drawImage(cfg.frameImg, f.cx - f.w/2, f.cy - f.h/2, f.w, f.h);
  } else {
    // 자산 누락 placeholder
    PICKUP_HELPERS.drawFramePlaceholder(ctx, f);
  }

  // [7] 캐릭터명 (그라디언트 fillStyle, 자동 폰트 축소)
  const name = cfg.langs[cfg.lang].name;
  if (name) {
    const ns = spec.name;
    const fs = PICKUP_HELPERS.fitText(ctx, name, ns.maxW, ns.baseFs, ns.minFs, fontFamily, '900');
    ctx.textAlign = 'center';
    PICKUP_HELPERS.drawGradientText(
      ctx, name, ns.cx, ns.cy, fs, fontFamily, '900',
      cfg.nameGradTop, cfg.nameGradBottom
    );
  }

  // [8] 별 5개 (PNG 5번 반복, placeholder fallback)
  const ss = spec.stars;
  PICKUP_HELPERS.drawStarRow(ctx, cfg.starImg, ss.cx, ss.cy, 5, ss.starSize, ss.gap);

  // [9] 속성/클래스 ("{ele} | {cls}", 자동 폰트 축소)
  const ec = cfg.langs[cfg.lang];
  const ecText = `${ec.element || ''} ${spec.elementClass.separator} ${ec.class || ''}`.trim();
  if (ecText && ecText !== '|') {
    const es = spec.elementClass;
    const fs = PICKUP_HELPERS.fitText(ctx, ecText, ns.maxW * 0.5, es.fontSize, 14, fontFamily, '500');
    ctx.fillStyle = es.color;
    ctx.font = `500 ${fs}px ${fontFamily}`;
    ctx.textAlign = 'left';
    ctx.fillText(ecText, es.x, es.cy + fs * 0.3);
  }

  // [10] CTA (PICKUP_CTA_MAP[lang], 흰 + drop-shadow)
  const cta = PICKUP_CTA_MAP[cfg.lang];
  ctx.fillStyle = '#FFFFFF';
  ctx.font = `700 ${spec.cta.fontSize}px ${fontFamily}`;
  ctx.textAlign = 'center';
  ctx.shadowColor = 'rgba(0,0,0,0.6)';
  ctx.shadowBlur = 16; ctx.shadowOffsetY = 4;
  ctx.fillText(cta, spec.cta.cx, spec.cta.y);
  ctx.shadowColor = 'transparent';

  return canvas;
}
```

### 8.2 Render switch 분기

```js
// renderBanner / setBannerData 분기
case 'pickup':
  banner.classList.add('tmpl-pickup', `size-${data.size}`);
  banner.dataset.lang = data.lang;
  // Canvas embed 형태 (sd-showcase/KVR 패턴 일관)
  const canvas = await buildPickupCanvas(data);
  banner.replaceChildren(canvas);
  break;
```

### 8.3 Image preparation (`prepPickupCfgImages`)

```js
async function prepPickupCfgImages(cfg) {
  // 사용자 자산 (dataURL)
  cfg.logoImg = cfg.logo ? await loadCachedImage(cfg.logo) : null;
  cfg.bgImg = cfg.keyart ? await loadCachedImage(cfg.keyart) : null;
  cfg.characterImg = cfg.character ? await loadCachedImage(cfg.character) : null;
  // 번들 자산 (URL)
  cfg.frameImg = await loadCachedImage(PICKUP_HELPERS.getFramePath(cfg.size));
  cfg.starImg = await loadCachedImage(PICKUP_ASSETS.star);
  return cfg;
}
```

---

## 9. ZIP Export 분기

기존 `buildBatchCfgs` + `handleBatchExportZip`에 `pickup` 분기 추가.

### 9.1 `buildBatchCfgs` pickup 분기

```js
if (tmpl === 'pickup') {
  const sizes = state.batch.sizes.filter(s => s !== '9x16');  // 1x1, 1200x628만
  const langs = state.batch.langs;                              // 4개
  for (const size of sizes) {
    for (const lang of langs) {
      cfgs.push({
        ...state.batch.pickup,                                  // 자산 + 슬라이더 + 그라디언트
        size, lang,
        template: 'pickup',
      });
    }
  }
}
```

### 9.2 사전 디코드 (성능)

```js
// handleBatchExportZip 진입 시
if (template === 'pickup') {
  // 사용자 자산 1회 디코드 → 8장 모두 공유 (M-2 패턴)
  await loadCachedImage(state.batch.pickup.logo);
  await loadCachedImage(state.batch.pickup.keyart);
  await loadCachedImage(state.batch.pickup.character);
  // 번들 자산 사전 디코드 (사이즈별 frame + star)
  await loadCachedImage(PICKUP_ASSETS.frame['1x1']);
  await loadCachedImage(PICKUP_ASSETS.frame['1200x628']);
  await loadCachedImage(PICKUP_ASSETS.star);
}
```

### 9.3 파일명 규칙 (`buildPickupFilename`)

```js
function buildPickupFilename(cfg, prefix, ext) {
  const sizeKey = cfg.size === '1x1' ? '1080x1080' : cfg.size;
  const safePrefix = (prefix || '').trim() || 'pickup';
  return `${safePrefix}_pickup_${cfg.lang}_${sizeKey}.${ext}`;
}
// 예: "banner_pickup_ko_1080x1080.png"
```

---

## 10. Test Plan

| ID | 시나리오 | 합격 기준 |
|---|---|---|
| T-1 | Template selector 전환 | "Pickup" 선택 시 `s-size`에서 1x1+1200x628 활성, 9:16 disabled |
| T-2 | 4언어 LANG_PACK 출력 | ko/en/ja/zh-TW 4장 생성 → 캐릭터명/설명/속성/클래스 모두 언어별 정확, CTA `PICKUP_CTA_MAP` 자동 변환 |
| T-3 | 폰트 자동 스왑 | ja → Noto Sans JP, zh-TW → Noto Sans TC, ko/en → Pretendard 모두 정상 |
| T-4 | 캐릭터 슬라이더 | charX/Y ±200, scale 50~150% 모두 실시간 반영 |
| T-5 | 게임 로고 슬라이더 | logoX/Y ±200, scale 50~150% 모두 실시간 반영 |
| T-6 | 그라디언트 색상 | 상/하 색상 picker 변경 시 캐릭터명 fillStyle 즉시 반영 |
| T-7 | 자동 폰트 축소 | 캐릭터명 maxW 초과 시 자동 축소 (예: en "Aurora Stardust" 16자) |
| T-8 | 자산 누락 fallback | `assets/pickup/` 비어 있을 때 frame placeholder rect + ★ Unicode 별 5개로 fallback |
| T-9 | 자산 도착 후 정상 | PNG 3개 배치 후 placeholder 자동 제거 + 정상 PNG 로드 |
| T-10 | 1080×1080 비주얼 일치 | 레퍼런스 미나 PNG와 ±5% 일치 (로고 위치, 캐릭터 비중, 프레임 위치, CTA 위치) |
| T-11 | 1200×628 비주얼 일치 | 레퍼런스 미나 PNG와 ±5% 일치 |
| T-12 | Single 다운로드 | 1080×1080 ko PNG 다운로드 ≤1초, `{prefix}_pickup_ko_1080x1080.png` 명명 |
| T-13 | Batch ZIP | 2 사이즈 × 4 언어 = 8장, ≤2초 생성, 파일명 규칙 준수 |
| T-14 | _imgCache 누수 | 사용자 자산(logo/keyart/character × single/batch = 6) + 번들(frame×2+star = 3) = 9 entries 유지 |
| T-15 | 회귀 — 기존 5 템플릿 | today-tap, app-badge, appstore-screenshot, sd-showcase, keyvisual-review 모두 회귀 0건 |

---

## 11. Implementation Guide

### 11.1 Module Map

| Module | 파일/위치 | 라인 | 의존성 |
|---|---|---|---|
| **M1** — TEMPLATE_KEYS + select 옵션 + 사이즈 분기 | `~L1951` (TEMPLATE_KEYS), `~L905` (select), `~L5694` (applyTemplateSwitch) | +6 | 없음 |
| **M2** — 상수 (`PICKUP_CTA_MAP`, `PICKUP_ASSETS`, `PICKUP_CANVAS_SPECS`, `PICKUP_DEFAULT`) | `~L2200` (KVR_LANG_PACK 다음) | +120 | 없음 |
| **M3** — `PICKUP_HELPERS` 객체 (fitText/drawGradientText/drawStarRow/getFramePath/drawFramePlaceholder) | `~L2330` (PICKUP_DEFAULT 다음) | +90 | M2 |
| **M4** — state 확장 (`state.single.pickup`, `state.batch.pickup`) | `~L2495`, `~L2518` | +4 | M2 |
| **M5** — CSS `.tmpl-pickup` (사이즈별 분기, 폰트 스왑) | `~L700` 부근 (style 블록) | +80 | 없음 |
| **M6** — Canvas 빌더 (`buildPickupCfg`/`prepPickupCfgImages`/`buildPickupCanvas`/`buildPickupBanner`/`buildPickupFilename`) | `~L4500` (KVR 빌더 다음) | +280 | M2, M3, M4 |
| **M7** — Render switch + dispatcher 분기 | `~L4321`, `~L4809` | +20 | M6 |
| **M8** — 단건 UI HTML 블록 (`data-tmpl="pickup"`) | `~L1700` 부근 (KVR 다음) | +110 | M1, M5 |
| **M9** — 단건 UI 이벤트 바인딩 (`bindPickupSingleUI`) | `~L5114` (bindSingleMode) | +90 | M4, M6, M8 |
| **M10** — `handleSingleDownload` pickup 분기 | `~L6000` | +15 | M6 |
| **M11** — 배치 UI HTML 블록 + `renderBatchLangFields` pickup 분기 | `~L1721` (KVR batch 다음), `~L6491` | +90 | M1, M5 |
| **M12** — 배치 UI 이벤트 바인딩 (`bindPickupBatchUI`) | `~L5437` (bindBatchMode) | +60 | M4, M6, M11 |
| **M13** — `buildBatchCfgs` + `handleBatchExportZip` pickup 분기 | `~L6738`, `~L7000` | +30 | M6, M12 |
| **M14** — 자산 폴더 (`repo/assets/pickup/`) 생성 + placeholder 안내 | (신규 폴더) | — | M2 |

**총합**: ~995라인 (CSS 80 + HTML 200 + JS 715) — Plan 추정 ~700라인보다 다소 많음 (Canvas 빌더 상세화). 실제 구현 시 ±15% 변동 가능.

### 11.2 Recommended Session Plan

`/pdca do pickup --scope module-{N}` 분할 구현.

```
Session 1 (data-switch, M1+M2+M3+M4+M14, ~220라인):
  Step 1: M14 — repo/assets/pickup/ 폴더 생성 (placeholder 안내 README.md 추가)
  Step 2: M1 — TEMPLATE_KEYS + <option> 추가 → select에 "Pickup" 보이는지 확인
  Step 3: M2 — 상수 4개 추가 (PICKUP_CTA_MAP/ASSETS/CANVAS_SPECS/DEFAULT)
  Step 4: M3 — PICKUP_HELPERS 객체 (fitText/drawGradientText/drawStarRow 등 5개 함수)
  Step 5: M4 — state 확장 (state.{single,batch}.pickup)
  Step 6: M1 applyTemplateSwitch 분기 — 9:16 disabled 동작 확인
  검증: console에서 PICKUP_HELPERS 함수 호출 + state.single.pickup 객체 확인

Session 2 (canvas-renderer, M5+M6+M7, ~380라인):
  Step 1: M5 — CSS .tmpl-pickup (사이즈별, 폰트 스왑)
  Step 2: M6 — buildPickupCfg / prepPickupCfgImages
  Step 3: M6 — buildPickupCanvas (10단계 그리기)
  Step 4: M6 — buildPickupBanner / buildPickupFilename
  Step 5: M7 — render switch + canvas dispatcher 분기
  검증: 자산 placeholder fallback (frame rect + ★ Unicode) 정상 동작
       임의 cfg로 buildPickupCanvas 호출 → toDataURL → 이미지 미리보기

Session 3 (single-ui, M8+M9+M10, ~215라인):
  Step 1: M8 — 단건 UI HTML 블록 (자산 dropzone 3 + 슬라이더 6 + picker 2 + 텍스트 4)
  Step 2: M9 — bindPickupSingleUI 이벤트 바인딩
  Step 3: M10 — handleSingleDownload pickup 분기
  검증: 단건 모드에서 ko 자산 업로드 + 텍스트 입력 + 슬라이더 조정 → 미리보기 실시간 반영
       1080×1080 PNG 다운로드 → 레퍼런스 미나 비주얼과 시각 비교
       1200×628 전환 → 레이아웃 자동 재배치 확인

Session 4 (batch-ui-zip, M11+M12+M13, ~180라인):
  Step 1: M11 — 배치 UI HTML 블록 (별도 자산 dropzone + 슬라이더, prefix b-)
  Step 2: M11 — renderBatchLangFields pickup 분기 (4언어 × 4필드 = 16개)
  Step 3: M12 — bindPickupBatchUI
  Step 4: M13 — buildBatchCfgs + handleBatchExportZip 분기
  검증: 배치 모드에서 자산 + 4언어 텍스트 입력 → 8장 ZIP 다운로드 ≤2초
       파일명 규칙 (`{prefix}_pickup_{lang}_{size}.png`) 8장 모두 정확

Session 5 (디자이너 자산 도착 후 — optional):
  Step 1: assets/pickup/{name-frame-1x1, name-frame-1200x628, star}.png 배치
  Step 2: 페이지 새로고침 → placeholder 자동 제거 + 정상 PNG 로드
  Step 3: T-10/T-11 비주얼 일치 검증 + 미세조정
```

### 11.3 Session Guide (`/pdca do pickup --scope`)

| --scope | Modules | 추정 라인 |
|---|---|---|
| `data-switch` | M1, M2, M3, M4, M14 | ~220 |
| `canvas-renderer` | M5, M6, M7 | ~380 |
| `single-ui` | M8, M9, M10 | ~215 |
| `batch-ui-zip` | M11, M12, M13 | ~180 |

```
/pdca do pickup --scope data-switch
/pdca do pickup --scope canvas-renderer
/pdca do pickup --scope single-ui
/pdca do pickup --scope batch-ui-zip
```

---

## Open Items (Design 단계에서 정리됨)

| # | 항목 | 결정 |
|---|---|---|
| D-1 | Architecture | Option C — Pragmatic Balance (PICKUP_HELPERS + 글로벌 빌더, KVR v1.7 패턴 일관) ✅ |
| D-2 | Canvas 좌표 (1080×1080) | logo (80,80,280) / char (cx=720, cy=480, w=760) / frame (cx=540, cy=820, 760×220) / cta (cx=540, y=1010, fs=44) |
| D-3 | Canvas 좌표 (1200×628) | logo (60,50,200) / char (cx=880, cy=314, w=600) / frame (cx=320, cy=360, 540×170) / cta (cx=320, y=560, fs=32) |
| D-4 | 자동 폰트 축소 알고리즘 | sd-showcase `fitSdsTitle` 패턴 — 2px씩 단계 축소, minFs까지 |
| D-5 | 그라디언트 적용 방식 | `ctx.createLinearGradient(0, y-fs*0.4, 0, y+fs*0.6)` (텍스트 baseline 기준 수직 그라디언트) |
| D-6 | 자산 누락 placeholder | frame: stroke rect (gold #FFD700, 4px) / star: ★ Unicode + gold fill |
| D-7 | 별 5개 자동 스케일 | starSize 1080×1080=44px, 1200×628=32px (사이즈별 PICKUP_CANVAS_SPECS) |
| D-8 | CTA placeholder | 코드 매핑 고정, 사용자 입력 불필요 (PICKUP_CTA_MAP 단순 lookup) |
| D-9 | 단일 HTML 정책 | 유지 (CSS+HTML+JS 모두 인라인, 외부 파일은 PNG 자산만) |
| D-10 | 배치 자산 분리 | KVR R13 패턴 — `state.batch.pickup` 자산 별도 (콘텐츠는 단건 데이터 자동 사용 옵션 검토) |

> **D-10 보충**: KVR R13에서 사용한 "배치 자산 분리 + 콘텐츠는 단건 데이터 사용" 절충 패턴이 Pickup에 적용 가능하나, Pickup은 다국어 텍스트가 4×4=16개로 많아서 **콘텐츠도 배치 별도**가 자연스러움 (사용자 결정 #10~#11 — 언어별 수동 입력). Session 4에서 최종 결정.
