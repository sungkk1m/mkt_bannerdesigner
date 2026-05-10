# PDCA Design — Steam Review 템플릿 (v1.9)

**Feature**: `steam-review`
**Created**: 2026-05-10
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/pdca design`
**Upstream**: [`docs/01-plan/features/steam-review.plan.md`](../../01-plan/features/steam-review.plan.md)
**Architecture (selected)**: **Option C — Pragmatic Balance** (`STEAM_REVIEW_HELPERS` 객체 + 글로벌 빌더, KVR v1.7 + pickup v1.8 패턴 일관)

---

## Context Anchor (propagated from Plan)

| Key | Value |
|-----|-------|
| **WHY** | Steam 스토어 분위기 "리뷰 + 추천" 광고 패턴 자동화 부재 — UA 매니저가 4언어 × 2사이즈 = 8장 매번 외주, 평가 라벨/플레이시간 일관성 깨지기 쉬움, 한국 규제 태그(확률형 아이템 포함) 누락 위험 |
| **WHO** | UA Manager (사내 마케팅), 잠재적으로 다른 사내 게임 BI 마케터 (게임별 키비주얼+텍스트만 교체하면 재활용) |
| **RISK** | CJK 텍스트 래핑 실패 (R-1); 긴 태그 wrap 시 reviews 영역 침범 (R-2, 4탭 통일로 위험 감소); zh-TW reviews[3] 누락 (R-3); 폰트 폴백 (R-4); Batch ZIP 8장 무거움 (R-5); 키비주얼 비율 불일치 (R-6); Steam 색상 토큰 정확도 (R-7) |
| **SUCCESS** | 단건 ≤1초, 배치 8장 ZIP ≤3초; 4언어 평가/플레이시간 라벨 정확; 한국어 4번째 태그 디폴트 자동 채움 (`확률형 아이템 포함`); 1080×1080 reviews[1,2,3] / 1200×628 reviews[0,1,2,3] 정확 렌더; 사용자 첨부 8장 스크린샷과 시각 90%+ 일치; 기존 6템플릿 회귀 0 |
| **SCOPE** | Session 1: data-switch (constants + state init + 자산 추출/임베딩) / Session 2: canvas-renderer (cfg/canvas/banner) / Session 3: single-ui (HTML 패널 + bind + lang switch) / Session 4: batch-ui-zip (배치 UI + ZIP) |

---

## Architecture (Selected: Option C — Pragmatic Balance)

| 측면 | 결정 |
|---|---|
| CSS 명명 | 기존 KVR/pickup 동일 패턴 — `.banner.tmpl-steam-review`. 단, KVR/pickup처럼 인라인 스타일 + Canvas 렌더링이 우선이라 별도 CSS 규칙은 최소화 |
| HTML | 기존 `data-tmpl="steam-review"` / `data-tmpl-hide` 패턴 그대로 |
| JS 분기 | 기존 `renderBanner` switch에 `'steam-review' → buildSteamReviewBanner` 추가, `buildBannerCanvas` dispatcher에도 `buildSteamReviewCanvas` 분기 |
| Helper 함수 | **분리** → `const STEAM_REVIEW_HELPERS = { drawTagPill, drawReviewCard, wrapDescription, filterTags, measureTagBlock }` (KVR_HELPERS / PICKUP_HELPERS 패턴 일관) |
| 빌더 함수 | 글로벌 — `buildSteamReviewCfg(stateNode, lang, size, mode='batch')`, `prepSteamReviewCfgImages`, `buildSteamReviewCanvas`, `buildSteamReviewBanner`, `buildSteamReviewFilename` |
| Mode 인자 | `pickup R5 패턴 차용` — `mode='single'` / `'batch'` 분기로 단건 슬라이더 직접값 vs 배치 perSize 구분 (Steam Review는 perSize 없으므로 단순 분기지만 일관성 차원에서 도입) |
| LANG_PACK | 신설 — `STEAM_REVIEW_LANG_PACK` (4언어 평가 라벨 + 플레이시간 포맷 함수) |
| 자산 | **base64 인라인** — `STEAM_REVIEW_ASSETS = { reviewerIcons: [4 base64], thumbsUp: 1 base64 }` (KVR mockup 인라인 패턴 일관, 외부 PNG 의존성 0) |
| State | `state.single.steam` + `state.batch.steam` (KVR R13 배치 자산 분리 패턴) |
| 추정 코드량 | HTML ~145 + JS ~710 ≈ **+855라인** (기존 ~8,437 → ~9,290) |

---

## 1. Overview

Steam 스토어의 게임 페이지 분위기(다크 블루 #1b2838 배경 + 추천 아이콘 + 플레이시간 메타)를 자동화한 7번째 템플릿. 두 가지 사이즈(1080×1080·1200×628)에 대해 hero(키비주얼+게임정보+태그) + 추천 리뷰 카드(3장 또는 4장)를 결합하여 광고임에도 자연스러운 사회적 증거(social proof) 인상을 준다.

KVR(앱스토어 모티브)과 달리 **Steam 특유의 카드 스택 형태**를 채택하며, 평가 라벨(Recommended/추천/おすすめ/推薦)·플레이시간 포맷·리뷰어 아이콘 4종을 언어별 하드코딩으로 일관성 보장. 한국어 5번째 태그(`확률형 아이템 포함`)는 한국 게임법 규제 대응으로 디폴트 자동 pre-fill.

기존 6 템플릿(KVR R28, pickup R5 등) 누적 미세조정 패턴을 바탕으로 Option C를 선택, **회귀 리스크 0**로 추가한다.

---

## 2. Architecture Decision Record

### 2.1 Why Option C (Pragmatic Balance)

| 평가 항목 | 결과 |
|---|---|
| 마지막 2 템플릿(KVR/pickup) 패턴 일관성 | ✅ STEAM_REVIEW_HELPERS 객체 + 글로벌 빌더 동일 |
| 회귀 리스크 | ✅ 0 (steam-review 분기만 추가) |
| 단일 HTML 정책 (CLAUDE.md) | ✅ 유지 |
| R-iteration 미세조정 (예: 패딩, drop shadow) | ✅ 헬퍼 단위로 수정 가능 |
| 사용자 "기존 템플릿 무영향" 기대 | ✅ 100% 충족 |
| 8번째 템플릿 추가 시 재활용 | ✅ 동일 레시피 |

### 2.2 Decision Record (Plan에서 확정)

| # | 결정 | 출처 |
|---|------|------|
| D-1 | 데이터 모델: 공유 4슬롯, 1080은 reviews[1,2,3], 1200은 reviews[0,1,2,3] | Brainstorming Q1 |
| D-2 | 평가 라벨/플레이시간: 언어별 하드코딩, 편집 불가 | Brainstorming Q2 |
| D-3 | 게임 태그: **모든 언어 4칸 통일** (빈 칸 hide). 한국어 4번째 디폴트 = `확률형 아이템 포함` (한국 규제 대응, "지금 플레이"보다 우선) | Brainstorming Q3 + 2026-05-10 사용자 결정 |
| D-4 | 모드: Single + Batch 양쪽 지원 | CLAUDE.md 정책 |
| D-5 | 자산: 사용자 8장 스크린샷에서 추출 → base64 인라인 (5 PNG) | Brainstorming Q4 |
| D-6 | 사이즈: 1x1 + 1200×628, 9:16 미지원 | Plan FR-02 |
| D-7 | 키비주얼: 1장만 업로드 → 전 언어 공유 + scale/x/y 슬라이더 | Plan FR-04 |
| D-8 | 슬롯-아이콘-시간 매핑 고정: 0=blue/56.9hrs, 1=knight/4.8, 2=pink/6.4, 3=corgi/203.4 | Plan |

---

## 3. Data Model

### 3.1 STEAM_REVIEW_DEFAULT (state shape)

```js
const STEAM_REVIEW_DEFAULT = {
  // 키비주얼 (전 언어 공유)
  keyvisualImage: null,           // dataURL
  keyvisualScale: 100,            // 50–600 %
  keyvisualX: 0,                  // –1500 to +1500 px
  keyvisualY: 0,                  // –1500 to +1500 px

  // 언어별 슬롯 (4언어 × {title, description, tags×4, reviews×4})
  langs: {
    'ko':    { title:'', description:'', tags:['','','','확률형 아이템 포함'], reviews:['','','',''] },
    'en':    { title:'', description:'', tags:['','','',''],                  reviews:['','','',''] },
    'ja':    { title:'', description:'', tags:['','','',''],                  reviews:['','','',''] },
    'zh-TW': { title:'', description:'', tags:['','','',''],                  reviews:['','','',''] },
  },
};
```

Plan 8장 스크린샷의 텍스트로 디폴트값을 채운다 (구현 시점에 사용자 8장에서 추출):

```js
// 디폴트값 (8장 스크린샷에서 추출)
'en': {
  title: 'UnderDark : Defense',
  description: 'Defense is all about tenacity and making it to the end\nDon\'t ever give up, no matter what.\n\nDefend the final camp!\nTactical indie game <UnderDark : Defense>',
  tags: ['Tactical Tower Defense', 'Overwhelmingly Positive', '+2 million downloads', 'Play now'],
  reviews: [
    "What I've been looking for!\nOnce you get the hang of the different towers and items you'll be playing for hours straight",
    'Pure dopamine!! 10/10!!',
    'No other game comes even close',
    'The game that keeps you coming back for more',
  ],
},
'ko': {
  title: '언더다크 : 디펜스',
  description: '디펜스란, 최후의 최후까지 버티는 자가 이기는 거야.\n그 어떤 적이 오더라도 포기하지 마.\n\n최후의 캠프를 방어하라!\n전략 인디게임 <언더다크:디펜스>',
  tags: ['전략 타워 디펜스', '압도적 긍정적 게임', '200만회+ 다운로드', '확률형 아이템 포함'],
  reviews: [
    '취향저격! 타워, 아이템 조합해가면서\n스테이지 공략하다 보니 하루 3시간 삭제돼요..!',
    '도파민!! 재밌어요!!!',
    '얘를 이길 디펜스 게임이 없다',
    '결국 돌고돌아 언닥임',
  ],
},
'ja': {
  title: 'UnderDark : Defense',
  description: 'ディフェンスなるもの…\n最後まで諦めない者が勝利するのだ！\nどんな敵でもネバーギブアップ\n\n基地を守り抜け！\n戦略インディーズゲーム【UnderDark : Defense】',
  tags: ['戦略タワーディフェンス', '圧倒的な神ゲー', '200万+ダウンロード', '今すぐプレイ'],
  reviews: [
    '超絶おすすめ！\nタワー＆アイテムを合成してステージ攻略してたら\nあっという間に夜の9時に…！',
    '脳汁ドーパミン！最強ゲー！！',
    'ディフェンスゲーム好きでこれ知らんとか草',
    '何だかんだでこれが1番だわ',
  ],
},
'zh-TW': {
  title: 'UnderDark : Defense',
  description: '堅持到最後的人才是防守遊戲的贏家\n絕對不要放棄\n\n守住最後的營地!\n策略獨立遊戲<UnderDark : Defense>',
  tags: ['策略塔防遊戲', '無負評的超讚遊戲', '超過200萬次下載', '馬上玩'],
  reviews: [
    '',  // 사용자 미제공 (1080×1080 zh-TW에서 slot 0 미사용)
    '發瘋!! 也太好玩!!',
    '沒有比這個更頂的遊戲了',
    '玩來玩去還是這個最頂',
  ],
},
```

### 3.2 STEAM_REVIEW_LANG_PACK (언어별 하드코딩)

```js
const STEAM_REVIEW_LANG_PACK = {
  'ko':    { evalLabel:'추천',       playtimeFmt:(h) => `기록상 ${h}시간` },
  'en':    { evalLabel:'Recommended', playtimeFmt:(h) => `${h} hrs on record` },
  'ja':    { evalLabel:'おすすめ',    playtimeFmt:(h) => `プレイタイム${h}時間` },
  'zh-TW': { evalLabel:'推薦',        playtimeFmt:(h) => `總時數${h}小時` },
};
const STEAM_REVIEW_PLAYTIMES = [56.9, 4.8, 6.4, 203.4];  // slot 0,1,2,3
```

### 3.3 STEAM_REVIEW_ASSETS (base64 인라인 5종)

```js
const STEAM_REVIEW_ASSETS = {
  reviewerIcons: [
    'data:image/png;base64,...',  // slot 0: 파란머리 소녀 (1200×628 only)
    'data:image/png;base64,...',  // slot 1: 녹색머리 기사
    'data:image/png;base64,...',  // slot 2: 분홍머리 소녀
    'data:image/png;base64,...',  // slot 3: 코기
  ],
  thumbsUp: 'data:image/png;base64,...',  // 블루 따봉 정사각
};
```

추출 워크플로(Session 1 사전작업): Preview/Figma 크롭(4 reviewer × 84×84, thumbs-up 26×26 → 2배 export) → tinypng 80% 압축 → `base64 -i` → 코드에 paste. 합산 ~33KB base64.

### 3.4 STEAM_REVIEW_CANVAS_SPECS (사이즈별 좌표)

```js
const STEAM_REVIEW_CANVAS_SPECS = {
  '1x1': {
    bg:          '#1b2838',
    cardBg:      '#16202d',
    heroBox:     { x:20, y:20, w:1040, h:340 },
    kvBox:       { x:40, y:40, w:520, h:300 },         // 2:1 비율, 4px 라운드 클립
    titleBox:    { x:580, y:60, w:480, fs:42, color:'#ffffff' },
    descBox:     { x:580, y:120, w:480, fs:18, lh:24, color:'#c6d4df', maxLines:3 },
    tagsBox:     { x:580, yStart:240, w:480, gap:8, padX:12, padY:6, fs:14,
                   pillBg:'rgba(102,159,209,0.18)', pillColor:'#a3cfe3', radius:3 },
    reviewsArea: { x:20, yStart:380, w:1040, slots:[1,2,3], cardGap:14 },
    cardLayout:  { iconSize:84, iconRadius:6, iconPad:18, thumbsSize:26, padX:20, padY:18,
                   evalFs:22, bodyFs:20, metaFs:14 },
  },
  '1200x628': {
    bg:          '#1b2838',
    cardBg:      '#16202d',
    heroBox:     { x:20, y:20, w:560, h:588 },
    kvBox:       { x:40, y:40, w:540, h:270 },         // 2:1 비율
    titleBox:    { x:40, y:330, w:520, fs:34, color:'#ffffff' },
    descBox:     { x:40, y:380, w:520, fs:16, lh:22, color:'#c6d4df', maxLines:3 },
    tagsBox:     { x:40, yStart:480, w:520, gap:6, padX:10, padY:5, fs:13,
                   pillBg:'rgba(102,159,209,0.18)', pillColor:'#a3cfe3', radius:3 },
    reviewsArea: { x:600, yStart:20, w:580, slots:[0,1,2,3], cardGap:8 },
    cardLayout:  { iconSize:64, iconRadius:5, iconPad:12, thumbsSize:22, padX:16, padY:12,
                   evalFs:18, bodyFs:18, metaFs:12 },
  },
};
```

색상값은 사용자 8장 스크린샷에서 Preview 픽셀-피킹으로 1회 락인.

---

## 4. Helper Functions (`STEAM_REVIEW_HELPERS`)

KVR_HELPERS / PICKUP_HELPERS 패턴 일관. 모두 순수 함수, ctx 인자 받아 그리기만 수행.

| Helper | 시그니처 | 역할 |
|---|---|---|
| `drawTagPill` | `(ctx, text, x, y, spec) → {w, h}` | 1개 태그 pill 그리기 (radius 3px rounded rect + 텍스트). 측정값 반환해 다음 위치 계산 |
| `measureTagBlock` | `(ctx, tags, spec) → {totalH, lines}` | 태그 wrap-flow 사전 측정 → 총 높이 반환 (R-2 대응: reviewsArea.y 동적 계산) |
| `drawReviewCard` | `(ctx, slot, body, x, y, w, h, lang, sizeKey)` | 카드 1장 전체 그리기 (cardBg fill + 아이콘 + 따봉 + 평가라벨 + 본문 + 시간 + 별 데코) |
| `wrapDescription` | `(ctx, text, x, y, w, lh, fs, lang, maxLines) → endY` | 게임 설명 줄바꿈 (`\n` 우선, 그 후 wrap). CJK = char-wrap, 라틴 = word-wrap. ellipsis 지원 |
| `filterTags` | `(tagsArray) → tagsArray` | 빈 슬롯 제거 (단순 filter, but 함수화로 테스트 가능) |

### 4.1 drawReviewCard 내부 로직

```js
// 카드 layout (cardLayout spec 기반):
//   ┌──────────────────────────────────────────────┐
//   │ [icon]  [thumbs] [evalLabel(굵게)]      [★] │
//   │ 84×84            "추천" / "Recommended"      │
//   │         [playtime meta (작은 #8a8a8a)]       │
//   │ ──────────────────────────────────────────── │
//   │  [reviewBody — 2-line clamp + ellipsis]       │
//   └──────────────────────────────────────────────┘
//
// 단계:
//   1. cardBg fill (rounded 4px)
//   2. icon: roundClip + drawImage (slot별 reviewerIcons[slot])
//   3. thumbs: drawImage (좌측 기준)
//   4. evalLabel: ctx.fillText(LANG_PACK[lang].evalLabel, ..., font: bold + cardLayout.evalFs)
//   5. playtime: ctx.fillText(LANG_PACK[lang].playtimeFmt(STEAM_REVIEW_PLAYTIMES[slot]), ..., color: '#8a8a8a', fs: cardLayout.metaFs)
//   6. star: 우측 상단에 ★ 회색 fill #5c7080 (Unicode 또는 Path2D)
//   7. body: wrapTextToNLines(2-line) → fillText
//   8. body 비어있으면 "" 처리 (R-3: 카드 자체는 렌더, 본문만 빈칸)
```

---

## 5. Builder Functions (Global)

### 5.1 `buildSteamReviewCfg(stateNode, lang, size, mode = 'batch')`

```js
function buildSteamReviewCfg(stateNode, lang, size, mode = 'batch') {
  const langSlot = stateNode.langs?.[lang] || { title:'', description:'', tags:[], reviews:[] };
  return {
    template: 'steam-review',
    size: size || '1x1',
    lang,
    mode,  // pickup R5 패턴 — 단건/배치 분리 일관성

    // 키비주얼 (전 언어 공유)
    keyvisualImage: stateNode.keyvisualImage || null,
    keyvisualScale: stateNode.keyvisualScale ?? 100,
    keyvisualX: stateNode.keyvisualX ?? 0,
    keyvisualY: stateNode.keyvisualY ?? 0,

    // 언어별 텍스트
    title: langSlot.title || '',
    description: langSlot.description || '',
    tags: STEAM_REVIEW_HELPERS.filterTags(langSlot.tags || []),  // 빈 슬롯 제거
    reviews: langSlot.reviews || ['', '', '', ''],

    scale: 1,
    format: 'png',
  };
}
```

### 5.2 `prepSteamReviewCfgImages(cfg)`

```js
async function prepSteamReviewCfgImages(cfg) {
  const tasks = [];
  if (cfg.keyvisualImage) tasks.push(loadCachedImage(cfg.keyvisualImage));
  // 자산 5종 (현재 사이즈에서 사용할 슬롯만)
  const slots = STEAM_REVIEW_CANVAS_SPECS[cfg.size === '1x1' ? '1x1' : '1200x628'].reviewsArea.slots;
  for (const i of slots) tasks.push(loadCachedImage(STEAM_REVIEW_ASSETS.reviewerIcons[i]));
  tasks.push(loadCachedImage(STEAM_REVIEW_ASSETS.thumbsUp));
  await Promise.all(tasks);
}
```

### 5.3 `buildSteamReviewCanvas(cfg)` (사이즈 분기 통합 단일 함수)

```js
async function buildSteamReviewCanvas(cfg) {
  const sizeKey = cfg.size === '1x1' ? '1x1' : '1200x628';
  const spec = STEAM_REVIEW_CANVAS_SPECS[sizeKey];
  const W = sizeKey === '1x1' ? 1080 : 1200;
  const H = sizeKey === '1x1' ? 1080 : 628;

  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d');

  // [1] 배경
  ctx.fillStyle = spec.bg;
  ctx.fillRect(0, 0, W, H);

  // [2] hero 영역
  // [2-1] 키비주얼 (kvBox 클립 + scale/X/Y 변환)
  if (cfg.keyvisualImage) {
    const img = await loadCachedImage(cfg.keyvisualImage);
    if (img) {
      ctx.save();
      // rounded clip
      ctx.beginPath();
      // 4px round rect path...
      ctx.clip();
      // cover fit + 사용자 transform
      const baseRatio = Math.max(spec.kvBox.w / img.naturalWidth, spec.kvBox.h / img.naturalHeight);
      const finalRatio = baseRatio * (cfg.keyvisualScale / 100);
      const drawW = img.naturalWidth * finalRatio;
      const drawH = img.naturalHeight * finalRatio;
      const drawX = spec.kvBox.x + (spec.kvBox.w - drawW) / 2 + cfg.keyvisualX;
      const drawY = spec.kvBox.y + (spec.kvBox.h - drawH) / 2 + cfg.keyvisualY;
      ctx.drawImage(img, drawX, drawY, drawW, drawH);
      ctx.restore();
    }
  }

  // [2-2] 게임 타이틀
  ctx.font = `bold ${spec.titleBox.fs}px ${getFontFamilyForLang(cfg.lang)}`;
  ctx.fillStyle = spec.titleBox.color;
  ctx.fillText(cfg.title, spec.titleBox.x, spec.titleBox.y + spec.titleBox.fs);

  // [2-3] 게임 설명 (3-line clamp)
  STEAM_REVIEW_HELPERS.wrapDescription(ctx, cfg.description,
    spec.descBox.x, spec.descBox.y, spec.descBox.w, spec.descBox.lh,
    spec.descBox.fs, cfg.lang, spec.descBox.maxLines);

  // [2-4] 태그 wrap-flow (먼저 측정, R-2 대응)
  const tagBlock = STEAM_REVIEW_HELPERS.measureTagBlock(ctx, cfg.tags, spec.tagsBox);
  let tagY = spec.tagsBox.yStart;
  let tagX = spec.tagsBox.x;
  for (const tag of cfg.tags) {
    const { w: pillW, h: pillH } = STEAM_REVIEW_HELPERS.drawTagPill(ctx, tag, tagX, tagY, spec.tagsBox);
    tagX += pillW + spec.tagsBox.gap;
    if (tagX + pillW > spec.tagsBox.x + spec.tagsBox.w) {
      tagX = spec.tagsBox.x;
      tagY += pillH + spec.tagsBox.gap;
    }
  }
  const tagBlockBottom = tagY + tagBlock.totalH;  // 다음 영역 시작점 (1x1만 동적 계산 필요)

  // [3] reviews 영역
  // 1080×1080은 tag 측정 결과로 reviewsArea.y 동적 조정 (R-2)
  // 1200×628은 hero가 좌측이라 reviews는 yStart 고정
  const reviewsY = sizeKey === '1x1' ? Math.max(spec.reviewsArea.yStart, tagBlockBottom + 24) : spec.reviewsArea.yStart;
  const slots = spec.reviewsArea.slots;
  const totalH = (sizeKey === '1x1' ? 1080 - reviewsY - 20 : 588);
  const cardH = (totalH - spec.reviewsArea.cardGap * (slots.length - 1)) / slots.length;

  let cardY = reviewsY;
  for (const slotIdx of slots) {
    STEAM_REVIEW_HELPERS.drawReviewCard(
      ctx, slotIdx, cfg.reviews[slotIdx] || '',
      spec.reviewsArea.x, cardY, spec.reviewsArea.w, cardH,
      cfg.lang, sizeKey
    );
    cardY += cardH + spec.reviewsArea.cardGap;
  }

  return canvas;
}
```

### 5.4 `buildSteamReviewBanner(cfg)`

KVR/pickup의 async wrapper 패턴. wrap div + canvas 비동기 mount.

```js
function buildSteamReviewBanner(cfg) {
  const wrap = document.createElement('div');
  wrap.className = `banner tmpl-steam-review size-${cfg.size}`;
  wrap.dataset.lang = cfg.lang;
  const W = cfg.size === '1x1' ? 1080 : 1200;
  const H = cfg.size === '1x1' ? 1080 : 628;
  wrap.style.cssText = `width:${W}px;height:${H}px;position:relative;overflow:hidden;background:#1b2838;`;

  (async () => {
    try {
      await prepSteamReviewCfgImages(cfg);
      const canvas = await buildSteamReviewCanvas(cfg);
      wrap.innerHTML = '';
      wrap.appendChild(canvas);
    } catch (e) {
      console.error('[steam-review] render failed:', e);
    }
  })();

  return wrap;
}
```

### 5.5 `buildSteamReviewFilename(cfg, prefix, ext)`

```js
function buildSteamReviewFilename(cfg, prefix, ext) {
  const sizeStr = cfg.size === '1x1' ? '1080x1080' : '1200x628';
  return `${prefix}_steam_${cfg.lang}_${sizeStr}.${ext}`;
}
```

---

## 6. UI Layout

### 6.1 Single 모드 패널 (`<div data-tmpl="steam-review">`)

| 영역 | 컨트롤 |
|---|---|
| 키비주얼 | dropzone(`s-drop-steam-kv`) + 3 슬라이더 (`s-steam-kv-{scale,x,y}`) |
| 텍스트 (현재 언어) | title input(`s-steam-title`), description textarea(`s-steam-desc`) |
| 태그 4칸 | `s-steam-tag-1` ~ `s-steam-tag-4` (한국어 4번째 디폴트 = `확률형 아이템 포함`, 모든 언어 동일 4칸) |
| 리뷰 4칸 | `s-steam-review-1` ~ `s-steam-review-4` (각 textarea, 슬롯별 라벨 명시 — slot 0 = 1200×628 only) |
| 안내 | "1080×1080 = 리뷰 slot 1·2·3 / 1200×628 = slot 0·1·2·3 / 9:16 미지원 / 빈 태그 자동 hide / 한국어 4번째 디폴트 = 확률형 아이템 포함" |

기존 today-tap의 keyart/icon 슬롯은 `data-tmpl-hide`에 `,steam-review` 추가하여 Steam Review 모드에서 자동 숨김.

### 6.2 Batch 모드 패널 (`<div data-tmpl="steam-review">` in batch)

KVR/pickup 동일 패턴 — `b-` prefix:
- 공통: 키비주얼 dropzone + 3 슬라이더
- `renderBatchLangFields` 내 `isSteam` 분기로 4개 언어 섹션 자동 생성, 각 섹션 = title + description + tags×4 + reviews×4 = 10 입력

### 6.3 언어 전환 동작

- `loadSteamReviewSlotToUI(lang)`: `state.single.steam.langs[lang]` → 11개 입력 필드 채움
- `applyTemplateSwitch('steam-review')` 시 자동 호출 + 언어 셀렉터 change 이벤트에서도 호출
- `9x16` 사이즈는 자동 disabled (sd-showcase/pickup 패턴)

---

## 7. Integration Points (기존 코드 패치 20곳)

| # | 위치 | 패치 내용 |
|---|---|---|
| 1 | `#template-selector` | `<option value="steam-review">Steam Review</option>` |
| 2 | `TEMPLATE_KEYS` | `'steam-review'` 추가 |
| 3 | `tmplLabelMap` | `'steam-review': 'Steam Review'` |
| 4 | `state.single` init | `steam: deepCopy(STEAM_REVIEW_DEFAULT)` |
| 5 | `state.batch` init | `steam: deepCopy(STEAM_REVIEW_DEFAULT)` |
| 6 | `renderBanner` switch | `case 'steam-review': return buildSteamReviewBanner(cfg);` |
| 7 | `buildBannerCanvas` dispatcher | `if (cfg.template === 'steam-review') return buildSteamReviewCanvas(cfg);` |
| 8 | `applyTemplateSwitch` | 9x16 disabled + `loadSteamReviewSlotToUI(state.single.lang)` |
| 9 | `data-tmpl-hide` 속성들 (4곳) | `,steam-review` append |
| 10 | `refreshSinglePreview` | `cfg = buildSteamReviewCfg(state.single.steam, lang, size, 'single')` 분기 |
| 11 | `handleSingleDownload` | steam-review 분기 (mode='single') |
| 12 | lang change 핸들러 | `loadSteamReviewSlotToUI(lang)` 호출 |
| 13 | `bindSingleMode` 끝 | `bindSteamReviewSingleUI()` 호출 |
| 14 | `bindBatchMode` 끝 | `bindSteamReviewBatchUI()` 호출 |
| 15 | `syncBatchStateFromUI` | 4언어 × 11필드 + 키비주얼 sync |
| 16 | `renderBatchLangFields` | `isSteam` 분기 |
| 17 | `copyLangFieldsToOthers` | steam-review 복사 로직 |
| 18 | `buildBatchCfgs` | `(size, lang)` 팬아웃 (mode='batch' default) |
| 19 | `downloadBatchItem` | steam-review canvas 분기 |
| 20 | `handleBatchExportZip` | 키비주얼 + 5 자산 1회 디코드 + 8장 캔버스 루프 |

---

## 8. Test Plan

| ID | 시나리오 | 수동/정적 |
|---|---|---|
| T-1 | 헤더 드롭다운에 "Steam Review" 노출 + 선택 시 컨트롤 패널 자동 전환 | 정적 + 수동 |
| T-2 | 사이즈 셀렉터 9:16 자동 disabled (sd-showcase/pickup 패턴) | 수동 |
| T-3 | 4언어 텍스트 슬롯 저장·복원 (언어 5회 전환 후 diff 0) | 수동 |
| T-4 | 키비주얼 1장 → 4언어 동일 적용 | 수동 |
| T-5 | scale/x/y 슬라이더 즉시 미리보기 반영 | 수동 |
| T-6 | 1x1 reviews[1,2,3] 정확 렌더 (slot 0 미사용) | 수동 + 시각 비교 |
| T-7 | 1200×628 reviews[0,1,2,3] 모두 렌더 | 수동 |
| T-8 | 평가 라벨/플레이시간 언어별 하드코딩 정확 (편집 입력 부재) | 정적 |
| T-9 | 한국어 디폴트 4번째 태그 = `확률형 아이템 포함` 자동 채움 (모든 언어 4탭 통일) | 수동 |
| T-10 | 긴 태그 wrap 시 reviews 영역과 안 겹침 (R-2 대응, 4탭 통일로 위험 감소했지만 안전장치 유지) | 수동 |
| T-11 | zh-TW reviews[3] 빈 칸일 때 1200×628 카드는 그려지되 본문만 비어 있음 (R-3) | 수동 |
| T-12 | Single PNG 다운로드 정상 (`{prefix}_steam_{lang}_{size}.png`) | 수동 |
| T-13 | Batch ZIP 8장 (4 lang × 2 size) 정상, 키비주얼 1회 디코드 공유 | 수동 |
| T-14 | 사용자 8장 스크린샷과 시각 90%+ 일치 | 시각 비교 |
| T-15 | 기존 6템플릿 회귀 0 | 수동 6번 |

---

## 9. Risk Mitigation

| ID | 리스크 | 대응 (Design 명시) |
|---|---|---|
| R-1 | CJK 텍스트 래핑 실패 | `STEAM_REVIEW_HELPERS.wrapDescription`에서 `getFontFamilyForLang(lang)` + ja/zh-TW char-wrap, en/ko word-wrap 분기. 기존 `wrapTextToNLines` 재사용 가능 |
| R-2 | 긴 태그 wrap 시 1x1 reviews 영역 침범 (4탭 통일로 위험 감소) | `measureTagBlock` 사전 측정 → `reviewsArea.y` 동적 계산 안전장치 유지. 1080×1080만 영향 (1200×628은 hero 좌측이라 무관) |
| R-3 | zh-TW reviews[3] 빈 칸 | `drawReviewCard`에서 빈 본문이라도 카드 프레임 + 아이콘 + 평가라벨 + 플레이시간까지 렌더. body 부분만 빈 줄 (Steam UI 일관성) |
| R-4 | 폰트 폴백 | `getFontFamilyForLang` 그대로. Pretendard 한국어 14pt pill 텍스트 줄바꿈 검증 (T-10) |
| R-5 | Batch ZIP 8장 무거움 | `handleBatchExportZip`에서 키비주얼 + 5 자산 1회 디코드 (KVR R5 패턴), size×lang 8조합 캔버스 루프. `_imgCache` 활용 |
| R-6 | 키비주얼 비율 불일치 | scale 50–600% + X/Y ±1500 (KVR R6 동일 폭) |
| R-7 | Steam 색상 토큰 정확도 | 사용자 8장 스크린샷에서 Preview 픽셀-피킹 1회 → `STEAM_REVIEW_CANVAS_SPECS` 락인. R-iteration 1회 정도 발생 가능 |

---

## 10. Asset Acquisition Workflow

Session 1 사전작업으로 사용자 8장 스크린샷에서 추출:

| 자산 | 추출 소스 | 크롭 가이드 | export 사이즈 |
|---|---|---|---|
| Reviewer slot 0 | 1200×628 (어떤 언어든) — 우측 첫 카드 | 정사각 ~64×64 | 128×128 (retina) |
| Reviewer slot 1 | 1080×1080 EN — 첫 카드 | 정사각 ~84×84 | 168×168 |
| Reviewer slot 2 | 1080×1080 EN — 두 번째 카드 | 동일 | 168×168 |
| Reviewer slot 3 | 1080×1080 EN — 세 번째 카드 | 동일 | 168×168 |
| Thumbs-up | 1200×628 어떤 카드든 | 26×26 | 64×64 |

워크플로:
1. Preview/Figma로 8장 스크린샷 열기
2. 위 영역 크롭 → PNG export (transparent BG 가능 시 우선)
3. tinypng.com 80% 압축
4. `base64 -i icon.png | pbcopy` → `STEAM_REVIEW_ASSETS` 의 해당 슬롯에 paste
5. 합산 ~33KB base64 (KVR mockup 117KB 대비 안전)

원본 PNG는 `repo/assets/steam-review/` 에 보관 권장 (base64 인라인 후에도 추적성).

---

## 11. Implementation Guide

### 11.1 Module Map

| ID | 모듈 | 분량 | 의존성 |
|---|---|---|---|
| M1 | TEMPLATE_KEYS / dropdown / tmplLabelMap / applyTemplateSwitch | ~10 라인 | - |
| M2 | 상수 4종 (DEFAULT, ASSETS, LANG_PACK, PLAYTIMES, CANVAS_SPECS) | ~115 라인 + base64 ~33KB | M1 |
| M3 | STEAM_REVIEW_HELPERS (5 헬퍼) | ~120 라인 | M2 |
| M4 | state.{single,batch}.steam init | ~5 라인 | M2 |
| M5 | data-tmpl-hide 속성 4곳 + 자산 추출 사전작업 | ~5 라인 코드 + 5 PNG | - |
| M6 | 빌더 5종 (Cfg / prep / Canvas / Banner / Filename) | ~380 라인 | M2, M3 |
| M7 | render dispatch (renderBanner + buildBannerCanvas + refreshSinglePreview) | ~10 라인 | M6 |
| M8 | Single HTML 패널 `<div data-tmpl="steam-review">` | ~75 라인 | - |
| M9 | bindSteamReviewSingleUI + loadSteamReviewSlotToUI | ~85 라인 | M4, M8 |
| M10 | handleSingleDownload steam 분기 | ~12 라인 | M6 |
| M11 | Batch HTML 패널 (공통 + renderBatchLangFields isSteam 분기) | ~70 라인 | - |
| M12 | bindSteamReviewBatchUI + syncBatchStateFromUI + copyLangFieldsToOthers | ~70 라인 | M4, M11 |
| M13 | buildBatchCfgs + downloadBatchItem + handleBatchExportZip steam 분기 | ~25 라인 | M6, M12 |
| M14 | assets/steam-review/ 폴더 + 5 PNG 원본 보관 (선택) | - | M5 |

총 신규 코드 ~870 라인 + 기존 코드 패치 ~25 라인 = **~895 라인** (Plan 추정 855 대비 +5%, 헬퍼 + Canvas 빌더 상세화).

### 11.2 File Plan

| 파일 | 작업 |
|---|---|
| `repo/today-banner-designer.html` | 모든 코드 변경 (단일 파일) |
| `repo/assets/steam-review/*.png` (선택) | 원본 PNG 5개 보관 |
| `repo/CLAUDE.md` | 진행 상황 업데이트 (각 phase) |
| `repo/docs/01-plan/features/steam-review.plan.md` | 본 plan (이미 작성됨) |
| `repo/docs/02-design/features/steam-review.design.md` | 본 design (이 문서) |
| `repo/docs/03-analysis/steam-review.analysis.md` | Check phase에서 작성 |
| `repo/docs/04-report/steam-review.report.md` | Report phase에서 작성 |

### 11.3 Session Guide (4-session 분할)

`pickup` v1.8 / `keyvisual-review` v1.7 의 4-session 분할 패턴 미러링.

#### Session 1 — `data-switch` (~155 라인 + 5 PNG 추출)

**모듈**: M1 + M2 + M3 + M4 + M5 (+M14 선택)
**산출물**:
- 헤더 드롭다운 + TEMPLATE_KEYS + tmplLabelMap에 'steam-review' 등록
- 상수 4종 정의 + STEAM_REVIEW_HELPERS 객체 5 헬퍼 정의 (drawReviewCard는 M6의 cfg가 없어도 ctx만 받으면 동작)
- state.{single,batch}.steam 초기화 (deepCopy)
- 사용자 8장 스크린샷에서 5 PNG 추출 → tinypng → base64 → STEAM_REVIEW_ASSETS에 paste
- data-tmpl-hide 속성 4곳에 ',steam-review' 추가

**검증**: `node --check` 통과 + 헤더 드롭다운에 옵션 노출 (선택해도 패널은 비어 있으나 에러 없음)
**실행**: `/pdca do steam-review --scope data-switch`

#### Session 2 — `canvas-renderer` (~390 라인)

**모듈**: M6 + M7
**산출물**:
- 빌더 5종 (Cfg / prep / Canvas / Banner / Filename)
- renderBanner switch + buildBannerCanvas dispatcher + refreshSinglePreview에 steam 분기 추가
- 정적 타이틀/설명/태그/리뷰 카드 그리기 검증

**검증**: `node --check` + 헤더에서 Steam Review 선택 시 빈 캔버스(배경만) 출력 OK + 디폴트값으로 텍스트 출력 시도
**실행**: `/pdca do steam-review --scope canvas-renderer`

#### Session 3 — `single-ui` (~170 라인)

**모듈**: M8 + M9 + M10
**산출물**:
- Single HTML 패널 (키비주얼 dropzone + 슬라이더 3 + 텍스트 11)
- bindSteamReviewSingleUI + loadSteamReviewSlotToUI
- 언어 전환 핸들러 + handleSingleDownload steam 분기

**검증**: `node --check` + 단건 모드에서 키비주얼 업로드 + 4언어 텍스트 입력 + 1080×1080 다운로드 정상 + zh-TW로 전환 시 입력 필드 복원
**실행**: `/pdca do steam-review --scope single-ui`

#### Session 4 — `batch-ui-zip` (~165 라인)

**모듈**: M11 + M12 + M13
**산출물**:
- Batch HTML 패널 (공통 + 4언어 섹션)
- bindSteamReviewBatchUI + syncBatchStateFromUI + copyLangFieldsToOthers + renderBatchLangFields isSteam 분기
- buildBatchCfgs + downloadBatchItem + handleBatchExportZip 분기 (자산 1회 디코드)

**검증**: `node --check` + 배치 모드에서 키비주얼 업로드 + 4언어 텍스트 채움 + ZIP 8장 다운로드 정상 + ZIP 내 8장 모두 정상 렌더
**실행**: `/pdca do steam-review --scope batch-ui-zip`

#### 전체 회귀 검증 (Session 4 완료 후)

- `node --check` 인라인 JS 문법 통과
- 6 기존 템플릿 (today-tap, app-badge, appstore-screenshot, sd-showcase, keyvisual-review, pickup) 단건/배치 회귀 0 확인
- 사용자 8장 스크린샷과 시각 비교 → 1차 완료
- `/pdca analyze steam-review` Gap 분석

---

## 12. Open Items (구현 단계 결정)

| ID | 항목 | 결정 시점 |
|---|---|---|
| O-1 | 8장 스크린샷에서 추출한 색상 hex 정확값 (#1b2838 등 추정 vs 실측) | Session 2 시작 시 픽셀-피킹 |
| O-2 | 별 아이콘: Unicode "★" vs Path2D 그리기 vs 작은 PNG (회색 데코) | Session 2 (T-15 회귀 위험 최소화 위해 Unicode 권장) |
| O-3 | 키비주얼 클립 corner radius 정확값 (4px vs 6px) | Session 2 사용자 시각 검증 |
| O-4 | tag pill 폰트 굵기 (regular vs medium) | Session 2 사용자 시각 검증 |
| O-5 | 1x1 hero 영역 높이 — 4탭 통일 후에도 긴 태그 wrap 시 여유 충분한가 | Session 2 R-2 검증 (안전장치 measureTagBlock 유지) |
| O-6 | 카드 drop shadow — Steam 원본은 약간 있음. 추가 여부 | Session 2 사용자 시각 검증 (KVR R21 vary strong은 과함) |
| O-7 | Batch에서 4언어 → 다른 3언어 복사 동작 (KVR과 동일 패턴인지) | Session 4 |

---

## Critical Files

- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/today-banner-designer.html` — 유일한 수정 대상
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/CLAUDE.md` — 각 session 후 "현황" 갱신
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/docs/01-plan/features/steam-review.plan.md` — Plan
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/docs/02-design/features/steam-review.design.md` — 본 Design
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/assets/steam-review/` — 추출 PNG 5개 보관 (선택)
