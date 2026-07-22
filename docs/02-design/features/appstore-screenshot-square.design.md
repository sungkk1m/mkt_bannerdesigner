# PDCA Design — App Store Screenshot 1080×1080 (Square) 변형

**Feature**: `appstore-screenshot-square`
**Created**: 2026-07-22
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Plan Doc**: `docs/01-plan/features/appstore-screenshot-square.plan.md`
**Architecture**: **C안 — Pragmatic Balance** (사용자 확정, 2026-07-22)

---

## Context Anchor

> Plan에서 승계. Do 단계로 전파.

| Key | Value |
|-----|-------|
| **WHY** | 정사각(1:1) 광고 지면용 App Store 모방 소재가 없어 세로형만으로 UA 운영 — 1080×1080 수요를 수작업으로 커버 중 |
| **WHO** | UA Manager (사내 마케팅) — 기존 appstore-screenshot 사용자 그대로 |
| **RISK** | DOM/Canvas 이중 렌더 불일치(R-1); KO 고지문구 폭 초과(R-2); hide-stats 토글과 1:1 y-플로우 상호작용(R-3); 배치 사이즈 중복 생성(R-4); 키아트 상하 크롭으로 핵심 비주얼 잘림(R-5) |
| **SUCCESS** | 1:1 단건/배치 정상 export; KO 1:1 고지문구 "앱 내 구입 · 확률형 아이템 포함" 한 줄; 9:16 출력 기존과 픽셀 동일(회귀 0); DOM 프리뷰 = Canvas export 일치 |
| **SCOPE** | Session 1: 공유 헬퍼 + CSS + DOM/Canvas 분기 / Session 2: 사이즈 셀렉터 + 배치 + 파일명 + UI 토글 + 검증 |

---

## 1. Overview

기존 `appstore-screenshot`(9:16 전용)에 `1x1`(1080×1080) 사이즈를 추가한다.
**아키텍처 원칙 (C안)**:

1. **9:16 코드 경로 무수정** — 분기 추가 외 기존 로직·좌표·상수를 건드리지 않는다 (NFR-02).
2. **드리프트 위험 2지점만 공유 소스화** — (a) KO IAP 고지문구 합성 문자열, (b) 1:1 키아트 높이. 이 둘은 DOM 빌더와 Canvas 빌더가 반드시 동일 값을 써야 하므로 공유 헬퍼로 단일화한다 (R37 `fitAppStoreDescription` 선례와 동일 패턴).
3. 나머지는 섹션 레벨 `cfg.size === '1x1'` 분기.

**설계안 비교 요약** (선택 근거):

| 안 | 특징 | 탈락/선택 사유 |
|---|---|---|
| A. Minimal | 인라인 분기만 (~170라인) | KO 고지문구·키아트 높이가 DOM/Canvas 두 곳 중복 → R-1 드리프트. 탈락 |
| B. Clean | `AS_SIZE_SPECS` 전면 리팩터 (~300라인+) | 9:16 기존 경로 수정 → 회귀 위험 + surgical changes 규칙 위배. 탈락 |
| **C. Pragmatic** | 무수정 원칙 + 공유 헬퍼 2지점 (~200라인) | **선택** — 위험 지점만 단일화, 사이즈 2개 수준에 적정 복잡도 |

---

## 2. Layout Spec — 1x1 (Canvas 절대좌표, DOM 동일)

상단 4개 섹션은 9:16과 **완전 동일 좌표** (픽셀 퍼펙트 원칙 — 코드 재사용, 신규 좌표 없음):

| # | 섹션 | Y 범위 | 비고 |
|---|---|---|---|
| [1] | 상태바 | 0–80 | 동일 |
| [2] | 헤더 (‹ 검색) | 80–158 | 동일 |
| [3] | 앱 정보 | 158–436 | 동일. **KO에서만 IAP 라벨 = `asIapLabelText()` 합성 문자열** |
| [4] | 스탯 4컬럼 | 440–588 | 동일 (`showStats !== false` 시) |
| [5] | 키아트 | keyartY = y + 28 / **H = `asSquareKeyartH(keyartY)`** | 하단 크롭 (아래 상세) |
| [6]~[8] | 디바이스 라벨 / 설명 본문 / KO 고지문구(구) / 탭바 | — | **렌더하지 않음** |

### 2.1 키아트 높이 공식 (공유 소스 — R-3 대응 포함)

```
asSquareKeyartH(keyartY) = min(1080 − keyartY − 28, 551)
```

- 하단 패딩 28px = 키아트 상단 패딩(28)과 대칭 — 라운드 카드(radius 28) 완결성 유지. Plan의 "0~24px Design 확정" 항목을 **28px로 확정** (측면 여백 50px과 함께 실제 App Store 카드 마진 감각 유지)
- `551` = 16:9 자연 높이(980×9/16) 상한 — 키아트는 절대 원본 비율보다 세로로 길게 늘어나지 않음

| 상태 | keyartY | H | 결과 |
|---|---|---|---|
| 스탯 표시 (기본) | 616 | **436** | ≈2.25:1, 16:9 원본의 세로 79% 중앙 크롭 (상하 각 ~10.5%) |
| 스탯 숨김 (hide-stats) | 464 | **551** | 16:9 완전 표시 (무크롭), 하단 여백 65px — B안 유사 효과 자연 지원 |

- 크롭 방식: 기존 `drawImageCover`(Canvas) / `object-fit: cover`(DOM) — 좌우 무손실, 상하 중앙 크롭
- **운영 가이드 (R-5)**: 키아트 상하 10.5%는 안전 영역 외 — README에 1줄 추가

### 2.2 KO 고지문구 합성 (공유 소스 — R-2 대응 포함)

```
asIapLabelText(lang, size):
  size==='1x1' && lang==='ko'
    → AS_LANG_PACK.ko.iap + ' · ' + (LANG_PACK.ko.disclaimer 선행 '*' 제거)   // "앱 내 구입 · 확률형 아이템 포함"
  그 외 → AS_LANG_PACK[lang].iap 그대로 (9:16 동작 불변, en '\n' 2줄 유지)
```

- 스타일: 기존 IAP 라벨과 동일 (22px, `--as-text-secondary`)
- 폭 검증: CTA "받기" 버튼(~160px) 우측 가용 폭 ≈ 524px vs 예상 문자열 폭 ≈ 350px → 한 줄 수용
- R-2 폭 초과 대비: DOM `.size-1x1 .as-iap-label { max-width: none; white-space: nowrap; }` + 구현 시 4언어 실측. 초과 발생 시 fallback = ` · ` 앞에서 줄바꿈 허용 (`white-space: normal`)
- 9:16 KO는 기존 위치(description 끝 `.as-ko-disclaimer`) **무수정** — ko-disclaimer-policy O-2 B 유지

---

## 3. 신규 공유 헬퍼/상수 (~30라인, `AS_LANG_PACK` 정의부 근처 삽입)

```js
// =========================================================================
// appstore-screenshot-square (C안): DOM/Canvas 드리프트 방지 공유 소스
// Design Ref: §2.1 §2.2 — 이 두 값/문자열은 반드시 양쪽 렌더러가 공유
// =========================================================================
const AS_SQUARE = { W: 1080, H: 1080, keyartTopPad: 28, keyartBottomPad: 28, keyartMaxH: 551 };

function asSquareKeyartH(keyartY) {
  return Math.min(AS_SQUARE.H - keyartY - AS_SQUARE.keyartBottomPad, AS_SQUARE.keyartMaxH);
}

function asIapLabelText(lang, size) {
  const pack = AS_LANG_PACK[lang] || AS_LANG_PACK['en'];
  if (size === '1x1' && lang === 'ko') {
    const disc = ((LANG_PACK.ko && LANG_PACK.ko.disclaimer) || '*확률형 아이템 포함').replace(/^\*/, '');
    return `${pack.iap} · ${disc}`;
  }
  return pack.iap;
}

function asSizeDim(size) {  // 파일명용 (§7)
  return size === '1x1' ? '1080x1080' : '1080x1920';
}
```

---

## 4. CSS 설계 (~20라인, 기존 AS 블록 끝 line ~902 뒤 추가)

```css
/* === appstore-screenshot-square: 1x1 (1080×1080) — Design §2 === */
.banner.tmpl-appstore-screenshot.size-1x1 {
  width: 1080px; height: 1080px; padding: 0;
  background: var(--as-bg);
  color: var(--as-text-primary);
  display: flex; flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Pretendard', sans-serif;
}
/* 키아트: aspect-ratio 해제 — 높이는 DOM 빌더가 asSquareKeyartH()로 inline 지정 (단일 소스) */
.banner.tmpl-appstore-screenshot.size-1x1 .as-keyart { aspect-ratio: auto; }
/* KO 고지문구 인라인 수용 (R-2) */
.banner.tmpl-appstore-screenshot.size-1x1 .as-iap-label { max-width: none; white-space: nowrap; }
```

- 기존 `.size-9x16` 블록은 무수정 (컨테이너 속성 5줄 중복은 의도 — 셀렉터 공유 리팩터링 금지)
- 섹션 숨김은 CSS가 아니라 **DOM 빌더에서 미출력** (Canvas와 동일 구조 — 숨김 CSS 방식은 DOM/Canvas 구조 차이를 만들므로 배제)

---

## 5. DOM 빌더 설계 — `buildAppStoreScreenshotBanner(cfg)` 분기 (~40라인)

```
1. const isSquare = cfg.size === '1x1';
2. banner.className = `banner tmpl-appstore-screenshot ${isSquare ? 'size-1x1' : 'size-9x16'} ...토글 클래스 동일`;
3. IAP 라벨: `${escapeHTML(asIapLabelText(lang, cfg.size)).replace(/\n/g,'<br/>')}` — 9:16 결과 기존과 동일 (en 2줄 유지)
4. innerHTML 템플릿: [6] 디바이스 라벨, [7] description, [7.1] ko-disclaimer, [8] 탭바 4개 섹션을
   isSquare ? '' : `...기존 마크업...` 로 조건 출력 (기존 마크업 문자열 무수정)
5. 키아트: isSquare 시 `.as-keyart`에 inline `style="height:${asSquareKeyartH(cfg.showStats !== false ? 616 : 464)}px"`
   — keyartY 산식: 스탯 표시 616 / 숨김 464 (Canvas y-플로우와 동일 값, §2.1 표 참조)
6. descFit/descHTML 계산은 isSquare 시 스킵 (불필요 연산 제거)
```

## 6. Canvas 빌더 설계 — `buildAppStoreScreenshotCanvas(cfg)` 분기 (~30라인)

```
1. const isSquare = cfg.size === '1x1';
2. const H = isSquare ? AS_SQUARE.H : 1920;  (canvas.height = H)
3. [3] IAP: `const iapLines = asIapLabelText(lang, cfg.size).split('\n');`  — 기존 pack.iap.split 1줄 치환 (9:16 동작 동일)
4. [5] 키아트 높이: `const keyartH = isSquare ? asSquareKeyartH(keyartY) : Math.round(keyartW * 9 / 16);`
5. [5] 키아트 렌더 직후 `if (isSquare) return canvas;`  — [6][7][7.1][8] 자연 스킵 (기존 코드 무수정)
```

- Canvas는 y-플로우 구조라 hide-stats 시 keyartY가 자동으로 464가 됨 → 헬퍼가 551 반환 (R-3 자연 해소)
- DOM 5번 항목의 정적 keyartY(616/464)와 Canvas 플로우 값이 일치함을 Test Plan §8-T5에서 검증

---

## 7. UI / 배치 / 파일명 설계

### 7.1 단건 사이즈 셀렉터 — `applyTemplateSwitch` AS 분기 수정 (line ~9936)

기존 (9x16 고정 + disabled) → sd-showcase 패턴으로 변경:

```js
if (newTemplate === 'appstore-screenshot') {
  // square: 9x16 + 1x1 허용, 그 외 사이즈면 9x16 fallback
  if (state.single.size !== '9x16' && state.single.size !== '1x1') {
    sizeSel.value = '9x16'; state.single.size = '9x16';
  } else { sizeSel.value = state.single.size; }
  sizeSel.disabled = false;
  Array.from(sizeSel.options).forEach(opt => {
    opt.disabled = !(opt.value === '9x16' || opt.value === '1x1');
  });
}
```

### 7.2 단건 패널 UI 3건 (line ~1046 패널 + s-size change 핸들러)

| 요소 | 동작 |
|---|---|
| "규격 (고정)" disabled input (line 1057) | id `s-as-size-note` 부여, 사이즈 변경 시 텍스트 갱신: `9:16 (1080×1920)` / `1:1 (1080×1080)` — 라벨 "규격 (고정)" → "규격" |
| 설명 본문 필드 (line 1070–1074) | wrapper div에 id `s-as-desc-wrap` 부여, 1x1 시 `display:none` (입력값은 state 보존 — 9:16 복귀 시 복원) |
| 탭바 토글 (s-as-show-tabbar, line 1110) | 1x1 시 checkbox `disabled` + 라벨 opacity 0.5 (1:1에서 탭바 항상 미표시) |

토글 지점: `applyTemplateSwitch` + `s-size` change 핸들러 양쪽에서 호출하는 소함수 `updateAsSquareUI()` 하나로 통합.

### 7.3 배치 — 사이즈 체크박스 + `buildBatchCfgs` (R-4 대응)

**체크박스** (`applyTemplateSwitch` bSizeBoxes AS 분기, line ~10020): 9x16 + 1x1 활성 (9x16 기본 checked 유지, 1x1은 사용자 선택), 나머지 disabled — sd-showcase 분기 패턴 이식.

**buildBatchCfgs**: 기존 AS 분기(combos.map 내부, size `'9x16'` 고정)를 **GP 패턴의 독립 선행 블록으로 이동** (R-4 중복 생성 원천 차단):

```js
// v1.16: App Store Screenshot — 선택 사이즈(9:16/1:1) × 4언어 × 1테마 (GP 패턴)
if (batchTmpl === 'appstore-screenshot') {
  const asSizes = sizes.filter(s => s === '9x16' || s === '1x1');
  if (asSizes.length === 0) asSizes.push('9x16');
  const cfgs = [];
  asSizes.forEach(sz => langs.forEach(lg => {
    cfgs.push({ ...기존 AS cfg 필드 동일..., size: sz, _combo: { size: sz, lang: lg } });
  }));
  return cfgs;
}
```

배치 언어별 입력의 description 필드는 유지 (9:16 겸용, 1x1 렌더 시 무시).

### 7.4 파일명 3곳 — `asSizeDim(size)` 적용

| 위치 | 변경 |
|---|---|
| `buildAppStoreScreenshotFilename` (line ~10646) | `_1080x1920.` → `` _${asSizeDim(s.size)}. `` |
| 배치 파일명 (line ~11801) | 동일 치환 (`cfg.size`) |
| 배치 파일명 (line ~12078) | 동일 치환 |

결과: `{prefix}_appstore_{lang}_{theme}_1080x1080.png` — 기존 9:16 파일명 불변.

---

## 8. Test Plan

| ID | 시나리오 | 기대 결과 | SC 매핑 |
|---|---|---|---|
| T1 | 문법: `node --check` (인라인 JS 추출 검증) | 통과 | NFR-04 |
| T2 | AS 선택 → s-size에 9:16/1:1만 활성, 1:1 선택 시 프리뷰 1080×1080 | 규격 노트/설명 필드/탭바 토글 UI 연동 | SC-01 |
| T3 | 1:1 프리뷰·export: 디바이스 라벨/설명/(구)고지문구/탭바 부재, 상단 4섹션 9:16과 동일 좌표 | 픽셀 확인 | SC-02 |
| T4 | KO 1:1 IAP = `앱 내 구입 · 확률형 아이템 포함` 한 줄, en/ja/zh-TW는 기존 문구 | 4언어 export | SC-03/04 |
| T5 | DOM 프리뷰 vs Canvas export 일치 (install-plz 방식 maxDiff), 특히 키아트 높이 436 | maxDiff 임계 내 | SC-08, R-1 |
| T6 | hide-stats + 1:1 → 키아트 551(16:9 무크롭), 하단 여백 65px | DOM/Canvas 동일 | R-3 |
| T7 | 9:16 회귀: KO 고지문구 description 끝 유지, export 기존과 픽셀 동일 | diff 0 | SC-05, NFR-02 |
| T8 | 배치: 9x16+1x1 체크 → 8장 ZIP / 1x1만 → 4장, 파일명 `1080x1080` 정확 | ZIP 내용 검증 | SC-07 |
| T9 | 기존 9템플릿 스모크 (단건 1장씩) | 회귀 0 | NFR-02 |
| T10 | 키아트 크롭: 기준 이미지(상하 마커 포함)로 중앙 크롭 확인 | 상하 대칭 ~10.5% 크롭 | SC-06 |

---

## 9. 수정 지점 요약 (patch list)

| # | 위치 (현행 라인 근사) | 작업 | 분량 |
|---|---|---|---|
| P1 | `AS_LANG_PACK` 정의부 근처 (~2860) | 공유 헬퍼/상수 4종 신규 (§3) | ~30 |
| P2 | CSS AS 블록 끝 (~902) | `.size-1x1` 규칙 3개 (§4) | ~20 |
| P3 | `buildAppStoreScreenshotBanner` (~4843) | isSquare 분기 (§5) | ~40 |
| P4 | `buildAppStoreScreenshotCanvas` (~5799) | H/IAP/키아트/early return (§6) | ~30 |
| P5 | 단건 패널 HTML (~1046) | 규격 노트 id·설명 wrap id·탭바 토글 (§7.2) | ~10 |
| P6 | `applyTemplateSwitch` (~9936, ~10020) | s-size + bSizeBoxes AS 분기 교체 (§7.1/7.3) | ~30 |
| P7 | `s-size` change 핸들러 + `updateAsSquareUI()` 신규 | 1:1 UI 토글 (§7.2) | ~25 |
| P8 | `buildBatchCfgs` (~11646) | AS 독립 블록 이동 + 사이즈 fan-out (§7.3) | ~30 |
| P9 | 파일명 3곳 (~10646, ~11801, ~12078) | `asSizeDim` 적용 (§7.4) | ~6 |
| P10 | `README.md` | 키아트 상하 10.5% 안전영역 가이드 1줄 (R-5) | ~2 |

합계 ~220라인 (추정 상한 250 이내).

---

## 11. Implementation Guide

### 11.1 구현 순서

P1(헬퍼) → P2(CSS) → P3(DOM) → P4(Canvas) → T1/T3/T4 중간 검증 → P5~P7(UI) → P8(배치) → P9(파일명) → P10(README) → T2/T5~T10 전체 검증

### 11.2 원칙

- 9:16 경로의 기존 라인은 P3-3(IAP 1줄 치환, 결과 동일)·P6(분기 교체) 외 수정 금지
- 코드 주석: 분기점마다 `// Design Ref: §N` / 핵심 로직에 `// Plan SC-NN`
- 각 세션 종료 시 `node --check`

### 11.3 Session Guide

**Module Map**

| Module | 범위 | 패치 | 분량 | 의존 |
|---|---|---|---|---|
| `module-1` renderer | 공유 헬퍼 + CSS + DOM/Canvas 분기 | P1–P4 | ~120 | — |
| `module-2` ui-batch | 사이즈 셀렉터 + 단건 UI 토글 + 배치 + 파일명 + README | P5–P10 | ~100 | module-1 |

**Recommended Session Plan**

| Session | Scope | 목표 | 검증 |
|---|---|---|---|
| 1 | `/pdca do appstore-screenshot-square --scope module-1` | 1:1 렌더 완성 (s-size 수동 조작 없이 콘솔로 cfg.size='1x1' 강제 확인 가능) | T1, T3, T4 |
| 2 | `/pdca do appstore-screenshot-square --scope module-2` | UI/배치/파일명 연결 + 전체 검증 | T2, T5–T10 |

단일 세션 진행도 가능 (~220라인 — 1세션 수용 범위). 컨텍스트 여유 시 `--scope` 생략 권장.

---

## 12. v1.17 개정 — 1:1 레이아웃 교체 (2026-07-22)

**배경**: 여러 시안(siaan1 크롬유지+무스탯 / siaan2 크롬제거+무스탯 / siaan3 크롬제거+스탯유지) 검토 결과 **siaan3 채택**. 기존 §2 레이아웃(상단 크롬 유지 + 키아트 하단 크롭 436px)을 아래로 **교체**한다. 9:16은 완전 무변경(회귀 0).

**확정 결정 (AskUserQuestion 4-round)**:
1. 적용: 현행 1:1 **교체** (별도 변형 아님)
2. 스탯: **4컬럼 전체 유지** (평점·연령·차트·개발자) — 9:16과 동일
3. 키아트: **16:9 풀 무크롭 551px** (세로형 16:9 에셋 그대로 재사용)
4. 유지: 아이콘 슬롯 · KO IAP 고지문구 · 9:16 무변경 · Single+Batch

**신규 1:1 레이아웃 (Canvas 절대좌표)**:

| 섹션 | Y 범위 | §2 대비 |
|---|---|---|
| ~~상태바 / 헤더~~ | — | **제거** (신규) |
| 앱정보 (아이콘 슬롯 + 제목/CTA/IAP) | topPad 40 – 306 | 상단 크롬 제거로 40부터 시작 |
| 스탯 4컬럼 | 310 – 458 | 동일 (위로 이동) |
| 키아트 (16:9 무크롭) | 486 – 1037 (**551px**) | 크롭 436 → 무크롭 551 |

- 키아트 높이: `asSquareKeyartH(486)` = min(1080−486−28, 551) = **551** (기존 공식 그대로, keyartY만 크롬 제거로 616→486). hide-stats 시 keyartY 334 → 여전히 551.
- 상단여백 `AS_SQUARE.topPad = 40` (Canvas) = `.size-1x1 .as-app-info { padding-top: 40px }` (DOM) — 동일값 유지. 상/하 여백 40/43 균형.

**구현 패치 (1:1 경로만, ~17라인)**:

| # | 위치 | 작업 |
|---|---|---|
| R1 | `AS_SQUARE` 상수 | `topPad: 40` 추가 |
| R2 | `buildAppStoreScreenshotCanvas` | 상태바·헤더 `if(!isSquare)` 게이팅 + `aiTop = isSquare ? topPad : y+12` |
| R3 | `buildAppStoreScreenshotBanner`(DOM) | 상태바·헤더 `isSquare ? '' :` 게이팅 + 키아트 inline 616/464 → 486/334 |
| R4 | CSS | `.size-1x1 .as-app-info { padding-top: 40px }` |

**검증 (브라우저 실측, 2026-07-22)**: Canvas 1:1=1080×1080 / 9:16=1080×1920 · DOM 1:1 상태바·헤더 부재 / 스탯 유지 / 키아트 551px / IAP 고지문구 · 9:16 회귀 0(상태바·헤더 유지, 키아트 inline 없음) · `node --check` 통과.
