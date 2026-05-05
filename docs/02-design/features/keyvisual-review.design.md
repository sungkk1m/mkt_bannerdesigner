# PDCA Design — Key Visual + iPhone Review 템플릿 (v1.7)

**Feature**: `keyvisual-review`
**Created**: 2026-05-03
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/pdca design`
**Upstream**: [`docs/01-plan/features/keyvisual-review.plan.md`](../../01-plan/features/keyvisual-review.plan.md)
**Architecture (selected)**: **Option C — 기존 패턴 + helper 함수 분리** (`KVR_HELPERS` 객체)

---

## Context Anchor (propagated from Plan)

| Key | Value |
|-----|-------|
| **WHY** | 게임 광고에서 평점·리뷰 신뢰도 트리거 자동화 부재 — 디자이너가 4언어×1사이즈=4장 매번 수작업 |
| **WHO** | UA Manager + 잠재적으로 다른 사내 게임 마케터 |
| **RISK** | mockup 화면 영역 좌표 부정확(R-1) / 별점 부분 채움 시각 미세차(R-2) / zh-TW `萬` 변환(R-3) / zh-TW 긴 라벨 padding 초과(R-4) / 헤드라인 비활성 reflow(R-5) |
| **SUCCESS** | 단건 ≤1초, 배치 4장 ZIP ≤2초; 4언어 LANG_PACK 정확; 별점 5케이스 정밀; 평가 개수 4언어 변환 정확; 회귀 없음 |
| **SCOPE** | Session 1: plan + 좌표 분석 ✅ / Session 2: design (본 문서) ✅ / Session 3: 구현 / Session 4: 검증 + 보고 |

---

## Architecture (Selected: Option C — Pragmatic Balance)

| 측면 | 결정 |
|---|---|
| CSS 명명 | 기존 sd-showcase/app-badge와 동일 패턴 — `.banner.tmpl-keyvisual-review .kvr-{slot}` |
| HTML | 기존 `data-tmpl="..."` 패턴 그대로 — 입력 폼 + 배너 DOM 모두 |
| JS 분기 | 기존 render switch에 `case 'keyvisual-review'` 추가 |
| Helper 함수 | **분리** → `const KVR_HELPERS = { renderStars, formatRatingCount, formatReviewDate }` (전역 객체로 단일 HTML 안에 위치) |
| LANG_PACK | 기존 `LANG_PACK`/`AS_LANG_PACK` 패턴과 동일하게 `KVR_LANG_PACK` 신설 |
| 자산 | 외부 PNG `repo/assets/keyvisual-review/iphone.png` (base64 inline 안 함) |
| 추정 코드량 | CSS ~300라인 + HTML ~200라인 + JS ~200라인 ≈ **+700라인** (기존 6,105 → ~6,800) |

---

## 1. Overview

```
┌─────────────────────────────────────┐  1080×1080
│                                      │
│       [Key Visual Background]        │  ← cover-fit 키비주얼 (scale/x/y slider)
│                                      │
│         ┌─────────────┐              │  ← 로고 슬롯 (별도 PNG, scale/x/y)
│         │    LOGO     │              │
│         └─────────────┘              │
│                                      │
│        Real Player Reviews           │  ← 헤드라인 (LANG_PACK 프리셋, 비활성 가능)
│                                      │
│        ╭─────────────╮               │  ← black iPhone mockup (540×~1088, 하단 8px 잘림)
│        │ ▣           │               │
│        │             │               │
│        │ 평가 및 리뷰 >│               │  ← Screen padding 32px
│        │   4.8       │               │     평점 박스 (헤더+숫자+별+개수)
│        │ ★★★★★      │               │     부제목
│        │ 21,000개의 평가              │     리뷰 카드 (제목+메타+본문 2줄)
│        │ ─────────── │               │
│        │ 가장 도움이 되는 리뷰         │
│        │             │               │
│        │ 리뷰 제목     │               │
│        │ ★★★★★ 1월 23일 lanaqma     │
│        │ 본문 본문 본문 본문 본문…    │
│        │ 본문 본문 본문 본문 본문…    │
│        │             │               │
│ (mockup 하단 8px는 캔버스 밖)         │
└─────────────────────────────────────┘
```

---

## 2. Mockup 좌표 (PNG → CSS 변수 매핑)

**원본 PNG**: `repo/assets/keyvisual-review/iphone.png` (248×500, 검은 베젤)

```
PNG 좌표 (검출 결과):
  Body bbox    : x=0..246,  y=1..498   (W=247, H=498)
  Screen bbox  : x=14..233, y=16..487  (W=220, H=472)

PNG 비율:
  Screen left   = 14/247  = 5.67%
  Screen top    = 15/498  = 3.01%   (body offset y=1 보정)
  Screen width  = 220/247 = 89.07%
  Screen height = 472/498 = 94.78%
```

**1080×1080 캔버스 배치** (사용자 선택: 폭 540px / 하단 8px 잘림):
```css
:root {
  --kvr-canvas: 1080px;
  --kvr-mockup-w: 540px;                              /* 캔버스 폭의 50% */
  --kvr-mockup-h: calc(540px * (498 / 247));          /* = 1088.7px */
  --kvr-mockup-x: calc((1080px - 540px) / 2);         /* = 270px (가운데 정렬) */
  --kvr-mockup-y: calc(1080px - 1088.7px);            /* = -8.7px (하단 정렬, 윗부분 잘림 X) */
  /* ↑ 잘림은 mockup-y를 음수로 두지 않고 캔버스 overflow:hidden + bottom 정렬로 처리 */

  /* Screen inner area (mockup 표시 사이즈 기준) */
  --kvr-screen-x: calc(540px * 0.0567);               /* = 30.6px (mockup 안 좌상단 기준) */
  --kvr-screen-y: calc(1088.7px * 0.0301);            /* = 32.8px */
  --kvr-screen-w: calc(540px * 0.8907);               /* = 481.0px */
  --kvr-screen-h: calc(1088.7px * 0.9478);            /* = 1031.9px */

  /* Content padding inside screen */
  --kvr-screen-pad: 32px;                             /* Open Item #4 추천값 */
}
```

> **결정**: mockup이 캔버스 하단에 정렬되고 상단이 약 8.7px 캔버스 위로 솟아오르는 형태로 자연스럽게 배치.
> 키비주얼 영역은 mockup 위쪽 + 좌우 약 270px씩 = 약 캔버스 상단 절반.

---

## 3. CSS Class 트리

```
.banner.tmpl-keyvisual-review                        /* 루트, size-1x1만 활성 */
├── .kvr-bg                                          /* 키비주얼 배경 (img, cover) */
│   └── img                                          /* scale/x/y transform */
├── .kvr-logo                                        /* 로고 슬롯 (img wrapper) */
│   └── img                                          /* scale/x/y transform */
├── .kvr-headline                                    /* 헤드라인 텍스트 */
└── .kvr-mockup                                      /* iPhone mockup 컨테이너 */
    ├── .kvr-mockup-frame                            /* iphone.png background */
    └── .kvr-screen                                  /* 흰 화면 영역 */
        └── .kvr-screen-inner                        /* padding + 콘텐츠 */
            ├── .kvr-rating-box                      /* 평점 영역 */
            │   ├── .kvr-rating-header               /* "평가 및 리뷰 >" */
            │   ├── .kvr-rating-row                  /* flex: 숫자 + 별/개수 */
            │   │   ├── .kvr-rating-num              /* 4.8 (~120px bold) */
            │   │   └── .kvr-rating-meta
            │   │       ├── .kvr-stars               /* ★★★★½ (0.5 단위) */
            │   │       └── .kvr-rating-count        /* 2.1만개의 평가 */
            ├── .kvr-subtitle                        /* "가장 도움이 되는 리뷰" */
            └── .kvr-review-card                     /* 리뷰 카드 (외곽선 없음) */
                ├── .kvr-review-title                /* 제목 1줄 */
                ├── .kvr-review-meta                 /* 별·날짜·아이디 한 줄 */
                │   ├── .kvr-review-meta-stars
                │   ├── .kvr-review-meta-date
                │   └── .kvr-review-meta-id
                └── .kvr-review-body                 /* 본문 2줄 + ellipsis */
```

---

## 4. JS Helper 함수 시그니처 (`KVR_HELPERS`)

### 4.1 `renderStars(rating: number): string`
- 0.5 단위 부분 채움
- 알고리즘: `rounded = Math.round(rating * 2) / 2`. `full = Math.floor(rounded)`, `half = (rounded % 1 === 0.5)`, `empty = 5 - full - (half ? 1 : 0)`
- 출력: 채워진 별 div + half 별(linear-gradient masking) + 빈 별 div
- 색상: CSS 변수 `--kvr-star-color` (기본 `#1d1d1f`)
- 케이스 검증: 4.0→★★★★☆ / 4.3→★★★★☆ (rounded=4.5 아님, 4.0) ※ 정정: 4.3→4.5(rounded), 즉 ★★★★½ / 4.5→★★★★½ / 4.8→★★★★★ / 5.0→★★★★★

### 4.2 `formatRatingCount(num: number, lang: string): string`
- 케이스별 단위 변환:
  ```js
  if (lang === 'ko') {
    if (num >= 10000) return `${(num/10000).toFixed(1).replace(/\.0$/,'')}만개의 평가`;
    if (num >= 1000)  return `${(num/1000).toFixed(1).replace(/\.0$/,'')}천개의 평가`;
    return `${num}개의 평가`;
  }
  if (lang === 'en') {
    if (num >= 1000000) return `${(num/1000000).toFixed(1).replace(/\.0$/,'')}M Ratings`;
    if (num >= 1000)    return `${(num/1000).toFixed(1).replace(/\.0$/,'')}K Ratings`;
    return `${num} Ratings`;
  }
  if (lang === 'ja') {
    if (num >= 10000) return `${(num/10000).toFixed(1).replace(/\.0$/,'')}万件の評価`;
    return `${num}件の評価`;
  }
  if (lang === 'zh-TW') {
    if (num >= 10000) return `${(num/10000).toFixed(1).replace(/\.0$/,'')}萬個評價`;
    return `${num}個評價`;
  }
  ```

### 4.3 `formatReviewDate(iso: string, lang: string): string`
- ISO `2026-01-23` → 언어별 포맷
  ```js
  const d = new Date(iso); const m = d.getMonth()+1, dd = d.getDate();
  if (lang === 'ko')    return `${m}월 ${dd}일`;
  if (lang === 'en')    return `${['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]} ${dd}`;
  if (lang === 'ja')    return `${m}月${dd}日`;
  if (lang === 'zh-TW') return `${m}月${dd}日`;
  ```

---

## 5. LANG_PACK 설계 (`KVR_LANG_PACK`)

```js
const KVR_LANG_PACK = {
  'ko':    { ratingsHeader: '평가 및 리뷰', mostHelpful: '가장 도움이 되는 리뷰' },
  'en':    { ratingsHeader: 'Ratings & Reviews', mostHelpful: 'Most Helpful Review' },
  'ja':    { ratingsHeader: '評価とレビュー', mostHelpful: '最も役立つレビュー' },
  'zh-TW': { ratingsHeader: '評分與評論', mostHelpful: '最有用的評論' },
};

const KVR_HEADLINE_PRESETS = [
  { id: 'real-player',  ko: '유저 리얼 후기',     en: 'Real Player Reviews',  ja: 'プレイヤーの本音レビュー', 'zh-TW': '玩家真實評價' },
  { id: 'top-rated',    ko: '최고 평점',           en: 'Top Rated',            ja: '高評価',                 'zh-TW': '高評價' },
  { id: 'players-say',  ko: '유저들이 말하는',     en: 'What Players Say',     ja: 'プレイヤーの声',          'zh-TW': '玩家評語' },
  { id: 'five-star',    ko: '5점 리뷰 모음',       en: '5-Star Reviews',       ja: '5つ星レビュー',           'zh-TW': '5星評論' },
];
```

---

## 6. 데이터 모델 (입력)

```ts
type KvrCommon = {
  bgImage: File | null,
  bgScale: number,    // 50..200 (%)
  bgX: number,        // -500..+500 (px)
  bgY: number,
  logoImage: File | null,
  logoScale: number,  // 50..150 (%)
  logoX: number,      // -200..+200
  logoY: number,      // -100..+200
  headlinePreset: string | 'off',   // KVR_HEADLINE_PRESETS.id 또는 'off'
  rating: number,     // 0.0..5.0 (step 0.1)
  ratingCount: number,// >=0 integer
  reviewDate: string, // ISO 'YYYY-MM-DD'
  starColor: string,  // hex, default #1d1d1f
};

type KvrPerLang = {
  reviewTitle: string,
  reviewBody: string,
  reviewerId: string,
};

type KvrInput = KvrCommon & {
  ko: KvrPerLang, en: KvrPerLang, ja: KvrPerLang, 'zh-TW': KvrPerLang,
};
```

---

## 7. 입력 폼 UX (line 1545 부근, sd-showcase 다음)

```
[키비주얼 + 리뷰 입력]
├── 이미지 업로드
│   ├── 키비주얼 dropzone + scale/x/y slider
│   └── 로고 dropzone + scale/x/y slider
├── 헤드라인
│   └── select: [Real Player Reviews / Top Rated / What Players Say / 5-Star Reviews / OFF]
├── 평점 정보 (공통)
│   ├── 평점 number(0~5, step 0.1)
│   ├── 평가 개수 number
│   ├── 작성 날짜 date input
│   └── 별점 색상 colorpicker
└── 리뷰 (언어별 탭: ko/en/ja/zh-TW)
    ├── 리뷰 제목 text
    ├── 리뷰 본문 textarea (rows=2)
    └── 리뷰어 아이디 text
```

---

## 8. 렌더링 분기 (기존 render 함수)

기존 `setBannerData(banner, data)` 패턴에 분기 추가:
```js
case 'keyvisual-review':
  banner.classList.add('tmpl-keyvisual-review', 'size-1x1');
  banner.dataset.lang = lang;
  // bg
  setLayerImage(banner.querySelector('.kvr-bg img'), data.bgImage, data.bgScale, data.bgX, data.bgY);
  // logo
  setLayerImage(banner.querySelector('.kvr-logo img'), data.logoImage, data.logoScale, data.logoX, data.logoY);
  // headline
  const hl = banner.querySelector('.kvr-headline');
  if (data.headlinePreset === 'off') hl.textContent = '';
  else {
    const preset = KVR_HEADLINE_PRESETS.find(p => p.id === data.headlinePreset);
    hl.textContent = preset ? preset[lang] : '';
  }
  // rating
  banner.querySelector('.kvr-rating-header').textContent = KVR_LANG_PACK[lang].ratingsHeader + ' >';
  banner.querySelector('.kvr-rating-num').textContent = data.rating.toFixed(1);
  banner.querySelector('.kvr-stars').innerHTML = KVR_HELPERS.renderStars(data.rating);
  banner.querySelector('.kvr-rating-count').textContent = KVR_HELPERS.formatRatingCount(data.ratingCount, lang);
  banner.querySelector('.kvr-subtitle').textContent = KVR_LANG_PACK[lang].mostHelpful;
  // review card
  const perLang = data[lang];
  banner.querySelector('.kvr-review-title').textContent = perLang.reviewTitle;
  banner.querySelector('.kvr-review-meta-stars').innerHTML = KVR_HELPERS.renderStars(data.rating);
  banner.querySelector('.kvr-review-meta-date').textContent = KVR_HELPERS.formatReviewDate(data.reviewDate, lang);
  banner.querySelector('.kvr-review-meta-id').textContent = perLang.reviewerId;
  banner.querySelector('.kvr-review-body').textContent = perLang.reviewBody;
  // star color via CSS variable
  banner.style.setProperty('--kvr-star-color', data.starColor);
  break;
```

---

## 9. ZIP Export 분기

기존 ZIP export 함수에 `keyvisual-review` 분기 추가:
- 활성 사이즈: `1x1`만 (체크박스에서 9:16/1200×628 disabled)
- 활성 언어: ko, en, ja, zh-TW (체크박스, 기본 모두 ON)
- 출력: `keyvisual-review_{lang}_1080x1080.png` × 4개 → ZIP

---

## 10. Test Plan

| ID | 시나리오 | 합격 기준 |
|---|---|---|
| T-1 | 4언어 LANG_PACK 출력 | ko/en/ja/zh-TW 4장 생성 → 헤더/부제목/평가 개수 단위 모두 언어별 정확 |
| T-2 | 별점 5케이스 | rating = 4.0/4.3/4.5/4.8/5.0 입력 시 별 표시 ★★★★☆ / ★★★★½ / ★★★★½ / ★★★★★ / ★★★★★ |
| T-3 | 평가 개수 변환 | ratingCount = 100 / 1500 / 21000 / 215000 4언어 변환 정확 |
| T-4 | 키비주얼/로고 slider | scale·x·y 3 slider × 2 layer = 6개 모두 즉시 반영 |
| T-5 | 헤드라인 OFF | preset='off' 시 빈 텍스트 + mockup 위치 변동 없음 |
| T-6 | 회귀 — 기존 4템플릿 | 각 템플릿에서 활성 사이즈 × 활성 언어 모두 정상 출력 |
| T-7 | ZIP 4장 출력 시간 | 1080×1080 × 4언어 ZIP 묶음 ≤2초 |
| T-8 | mockup 좌표 정확성 | zh-TW 가장 긴 라벨(`評分與評論` + `21.5萬個評價`)도 mockup screen 안에 잘림 없이 표시 |

---

## 11. Implementation Guide

### Module Map

| Module | 파일/위치 | 라인 | 의존성 |
|---|---|---|---|
| M1 — TEMPLATE_KEYS + select 옵션 | line 909, 1758 | +2 | 없음 |
| M2 — CSS 클래스 | line 700 부근 | +300 | 없음 |
| M3 — KVR_LANG_PACK + KVR_HEADLINE_PRESETS | line 1746 부근 | +30 | 없음 |
| M4 — KVR_HELPERS (renderStars/formatRatingCount/formatReviewDate) | LANG_PACK 다음 | +60 | 없음 |
| M5 — 입력 폼 HTML | line 1545 부근 | +200 | M1 |
| M6 — 렌더링 분기 + setLayerImage helper | 기존 render switch | +80 | M2, M3, M4 |
| M7 — ZIP export 분기 | 기존 export 함수 | +30 | M6 |
| M8 — mockup PNG 자산 참조 | (CSS background-image url) | — | M2 |

### Recommended Session Plan (단일 세션 추천)

```
Session 3 (구현):
  Step 1: M1 (TEMPLATE_KEYS + select) → 템플릿 select에 옵션 보이는지 확인
  Step 2: M2 (CSS) — 빈 배너 DOM 만들고 mockup PNG 위치 확인 (브라우저 시각 검사)
  Step 3: M3 + M4 (LANG_PACK + HELPERS) — console에서 함수 동작 검증
  Step 4: M5 (입력 폼 HTML)
  Step 5: M6 (렌더링) — 각 슬라이더/입력이 실시간 반영되는지
  Step 6: M7 (ZIP)
  Step 7: 회귀 — 기존 4템플릿 각 1회 동작 확인
```

---

## Open Items (Design 단계에서 정리됨)

| # | 항목 | 결정 |
|---|---|---|
| D-1 | mockup 폭 / 잘림 정책 | 540px (50%) + 하단 8.7px 잘림 (사용자 선택) |
| D-2 | Architecture | Option C — 기존 패턴 + helper 함수 분리 (사용자 선택) |
| D-3 | mockup overflow 처리 | mockup 컨테이너 자체는 1088px 높이로 두고 banner overflow:hidden으로 잘림 처리 |
| D-4 | 별점 부분 채움 구현 | linear-gradient 배경 + ★ 유니코드 텍스트 마스킹 (브라우저 호환성 좋음) |
| D-5 | zh-TW 폰트 사이즈 자동 축소 | 기존 ja 0.85× 패턴 차용. zh-TW 라벨이 길 경우 0.92× 적용 |
