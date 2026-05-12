# PDCA Plan — SD Showcase 템플릿 (v1.6)

**Feature**: sd-showcase
**Created**: 2026-04-29
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/plan-plus` → `/pdca plan`
**Upstream Doc**: `~/.claude/plans/brainstorming-spicy-plum.md` (Plan-Plus brainstorming output)

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | SD Showcase 템플릿 추가 (4번째 템플릿) |
| 시작 | 2026-04-29 |
| 본체 파일 | `today-banner-designer.html` (단일 HTML, 5,097 → 추정 5,750라인) |
| 사이즈 | 1200×628 + 1080×1080 (9:16 미지원) |
| 언어 | en / ko / ja / zh-TW (4개 고정) |
| FR | 16건 |
| NFR | 5건 |
| SC | 8건 |
| R | 5건 |
| 결정사항 | 15건 (Plan-Plus 14 + Persistence 1) |
| Implementation | 4 sessions (~650 lines 추가) |

### Value Delivered (4관점)

| 관점 | 내용 |
|---|---|
| **Problem** | 게임 SD/캐릭터를 전면에 내세우는 단순 쇼케이스 배너가 기존 3개 템플릿(Today Tap·App Badge·App Store Screenshot) 어디에도 없어, UA 매니저가 4언어 × 2사이즈 = 8장 생산을 디자이너 수작업·외주에 의존 (1~2시간 소요) |
| **Solution** | 6 SD 슬롯 + 4언어 텍스트 + 2 사이즈 + 외곽 검정 테두리 시그니처 룩을 자동화한 4번째 템플릿. 배경 컬러피커 + 자동 대비(휘도 이진)로 다른 게임 BI에도 재사용 가능 |
| **Function/UX Effect** | 헤더 셀렉터 "SD Showcase" → 1200×628 / 1080×1080 자동 활성, 4언어 입력 + SD 6장 업로드 → Single 1초 / Batch 8장 ZIP 2초. KO 광고만 "확률형 아이템 포함" 자동 첨부 → 광고법 준수 자동화. 픽 ON/OFF로 픽 없는 디자인 게임에도 적용 |
| **Core Value** | UA 자산 생산 속도 60~120× 향상 + 4언어 다국어 운영 자동화 + KO 광고법 준수 자동화 + 다른 사내 게임 재활용 가능 인프라화 |

---

## Context Anchor

> Auto-generated from Executive Summary. Propagated to Design/Do documents for context continuity.

| Key | Value |
|-----|-------|
| **WHY** | 게임 SD를 전면에 내세우는 쇼케이스 배너 템플릿 부재 — 디자이너 수작업으로 4언어×2사이즈=8장 생산 비효율 |
| **WHO** | UA Manager (사내 마케팅), 잠재적으로 다른 사내 게임 BI 운영자 |
| **RISK** | EN 레퍼런스의 "Friends" 라인 1.6× 강조가 v1 균등 사이즈로 평이해짐 (R-3); 픽 OFF 시 레이아웃 reflow 없음 의도된 동작 (R-1); 휘도 0.5 경계 깜빡임 (R-2) |
| **SUCCESS** | 단건 ≤1초 다운로드, 배치 8장 ZIP ≤2초; 8장 레퍼런스 픽셀 일치 (Friends 라인 사이즈 제외); KO만 고지문구; 빈 슬롯 reflow 없음 |
| **SCOPE** | Session 1: Data+Switch / Session 2: Canvas Renderer / Session 3: Single UI / Session 4: Batch UI+ZIP |

---

## Context

`today-banner-designer.html`(단일 HTML, v1.5 — App Store Screenshot 추가 후 5,097라인)는 기존 3개 템플릿을 제공한다. 사용자(Mobile Game UA Manager)가 첨부한 8개 레퍼런스 이미지(Underdark:Defense SD 라인업, ko/en/ja/zh-TW × 1200×628 + 1080×1080)를 픽셀 모방한 4번째 템플릿을 추가해 SD 라인업 광고 소재 제작 시간을 단축한다.

기존 템플릿이 모두 "특정 광고 면(Today Tap, 앱 정보, App Store 스샷)"을 모방하는 데 집중된 반면, **SD Showcase는 게임 캐릭터 자체를 전면에 내세우는 단순 쇼케이스**로 다른 게임 배너에도 재활용 가능한 형태로 설계한다 (브랜드 픽 텍스트 사용자 입력, 배경 컬러피커, 자동 대비).

**스킬 매핑**: 추후 비슷한 요청은 `/plan-plus sd-template-v2` 으로 시작. 보조 — `bkit:phase-3-mockup`(레이아웃 검증), `bkit:phase-5-design-system`(컬러 팔레트 일관성).

---

## 사용자 결정 요약 (확정 — 2026-04-29, Plan-Plus 14 + Checkpoint 1)

| # | 항목 | 결정 |
|---|------|------|
| 1 | 템플릿 이름 (헤더 드롭다운) | **"SD Showcase"** (key: `sd-showcase`) |
| 2 | 사이즈 | **1200×628 + 1080×1080** (9:16 미지원) |
| 3 | 언어 | en, ko, ja, zh-TW (4개 고정 + LANG_PACK 폰트 자동 스왑) |
| 4 | 브랜드 픽 텍스트 | **4언어 각각 사용자 입력** (배치 시 ko/en/ja/zh-TW 별도) |
| 5 | 브랜드 픽 ON/OFF 토글 | **있음** — 픽 숨김 시 레이아웃 고정(reflow 없음) |
| 6 | 타이틀 텍스트 | 4언어 각각, **`\n`으로 직접 줄바꿈** |
| 7 | KO 고지문구 | "확률형 아이템 포함" **양 사이즈 KO에서만 자동 표시**, 우하단 |
| 8 | 외곽 테두리 | **고정** — 검정, 사이즈별 자동 두께(1200×628: 8px / 1080×1080: 10px) |
| 9 | 배경 | **사용자 컬러피커**, 기본 `#FFFFFF` |
| 10 | 자동 대비 | **휘도 이진** — `getLuminance(bg) > 0.5` ? darkOnLight : lightOnDark |
| 11 | 타이틀 폰트 스타일 | 검정/흰 채움 + 반대색 외곽선(자동) — UI는 **외곽선 두께 슬라이더(4–14px)만** |
| 12 | SD 슬롯 | **6개 고정**, 빈 슬롯 투명(자리보존, reflow 없음) |
| 13 | EN 라인별 가변 폰트 사이즈 | **균등 사이즈 고수 (v1 제외)** — Friends 1.6× 강조는 v2 후보 |
| 14 | 1080×1080 타이틀 디폴트 줄수 | **1줄 기본**, 사용자 `\n`으로 2줄 가능 |
| 15 | SD 슬롯 영속화 | **세션 전용 (기존 3 템플릿 패턴 유지)** — 리로드 시 재업로드 |

---

## Functional Requirements (FR)

- **FR-01**: 헤더 템플릿 셀렉터에 `sd-showcase` 옵션 추가 (4번째)
- **FR-02**: `TEMPLATE_KEYS` 배열에 `'sd-showcase'` 추가 + `.tmpl-sd-showcase` CSS 스코프
- **FR-03**: 신규 상수 `SDS_CANVAS_SPECS` (1200×628 + 1080×1080 사이즈별 좌표 테이블) + `SD_SHOWCASE_DEFAULT` (4언어 기본 타이틀/픽 + 배경 #FFFFFF + 외곽선 8px + 픽 ON + slots [null]×6)
- **FR-04**: `applyTemplateSwitch` 분기 — `sd-showcase` 선택 시 `s-size`에서 `1x1`+`1200x628` 활성, `9x16` disabled. 배치 사이즈 체크박스 동기화
- **FR-05**: state 확장 — `state.single.sdshowcase` (deepCopy SD_SHOWCASE_DEFAULT), `state.batch.{sd_bgColor, sd_strokeWidth, sd_showPill, sd_slots}` + `langOverrides[lang].{sds_title, sds_pill}`
- **FR-06**: 6개 SD 드롭존 (단건 `#s-sds-slot-1~6`, 배치 `#b-sds-slot-1~6`) — `setupDropzone()` 헬퍼 + `updateStateImageAt(arr, i, url)` 신규 헬퍼로 `_imgCache` 누수 방지
- **FR-07**: 단건 모드 UI — 타이틀 textarea, 픽 텍스트 input + ON/OFF 체크박스, 배경 컬러피커, 외곽선 두께 슬라이더(4~14)
- **FR-08**: 배치 모드 UI — 글로벌 4개(배경, 외곽선, 픽 ON/OFF, 사이즈 체크박스 2개), 언어별 필드 `b-sds-title-${lang}` textarea + `b-sds-pill-${lang}` input × 4언어
- **FR-09**: `renderBatchLangFields()` SDS 분기 추가 — `isSDS` 분기에서 title textarea + pill input 렌더
- **FR-10**: `copyLangFieldsToOthers` SDS 분기 — title/pill 4언어 복사 지원
- **FR-11**: 자동 대비 — `getLuminance(hex)` (WCAG sRGB 상대 휘도) + `getContrastPalette(bgHex)` (border/title/pill/disclaimer 6색 반전) 신규 헬퍼
- **FR-12**: Canvas 렌더러 `buildSdShowcaseCanvas(cfg)` — 7단계 그리기 순서:
  1. 배경 fillRect (cfg.bgColor)
  2. palette 결정
  3. 외곽 테두리 strokeRect
  4. 6 슬롯 `drawImageContain` (null skip — M-4 fix 함수 재사용)
  5. 타이틀 멀티라인 stroke + fill double-pass (`lineJoin='round'`, stroke≥12 시 lineHeight 1.10 자동 보정)
  6. 픽 (showPill && pill.trim() — `ctx.roundRect` polyfill 재사용)
  7. KO 고지문구 우하단 (`LANG_PACK.ko.disclaimer` 재사용, 선두 `*` strip)
- **FR-13**: 단건 다운로드 — `handleSingleDownload` SDS 분기 추가, `buildSdShowcaseCfg → prepSdShowcaseCfgImages → buildSdShowcaseCanvas → canvasToDataURL → buildSdShowcaseFilename`
- **FR-14**: 배치 ZIP — `buildBatchCfgs` SDS 분기 (selected sizes × 4 langs fan-out), 글로벌 ZIP 다운로드 흐름 재사용
- **FR-15**: 파일명 규칙 — `{prefix}_sdshowcase_{lang}_{size}.{ext}` (`sizeKey` 매핑: `1x1` → `1080x1080`, `1200x628` → `1200x628`); slug 빈 문자열 시 `'banner'` fallback (M-3 mitigation)
- **FR-16**: DOM 프리뷰 — `buildSdShowcaseBanner(cfg)` 신규 (Canvas embed 형태로 단순화 — DOM/Canvas 이중 구현 회피)

## Non-Functional Requirements (NFR)

- **NFR-01**: Canvas 기반 export (`USE_CANVAS_EXPORT=true` 동선 유지) — html-to-image 미사용
- **NFR-02**: 폰트 — 기존 `getFontFamilyForLang(lang)` 재사용 (Pretendard/Noto Sans JP/Noto Sans TC 자동 스왑) + `ensureFontsLoaded()` 사전 디코드 재사용
- **NFR-03**: 이미지 캐시 — `_imgCache` 재사용, batch 시 SD 6장 1회 디코드 → 4언어×2사이즈=8장 모두 공유 (M-2 패턴 확장)
- **NFR-04**: 단일 HTML 정책 유지 — 외부 모듈/번들 도입 금지, 인라인 `<script>` + `<style>` 내 추가
- **NFR-05**: 휘도 임계값 hysteresis — 0.46~0.54 밴드에서 직전 상태 유지 (경계 깜빡임 방지)

## Scenarios (SC)

- **SC-01**: 사용자가 헤더 셀렉터에서 "SD Showcase" 선택 → `s-size`에서 1x1+1200x628만 활성, 9:16 비활성. 단건/배치 패널이 SD 전용 UI로 전환
- **SC-02**: SD 6장 업로드 + 4언어 타이틀 입력 + 픽 텍스트 입력 + 배경 흰색 유지 → 미리보기에 검정 테두리 + 검정 타이틀 + 흰 외곽선 + 검정 픽 + 흰 픽 글자
- **SC-03**: 배경 검정(`#000000`) 변경 → 자동 대비로 외곽 테두리·타이틀·픽 모두 흰/검 반전 (테두리 흰색, 타이틀 흰색 + 검정 외곽선, 픽 흰색 배경 + 검정 글자)
- **SC-04**: KO 단건 모드 1200×628 다운로드 → "확률형 아이템 포함" 우하단 자동 표시. EN/JA/zh-TW에서는 미표시
- **SC-05**: 픽 ON/OFF 토글 OFF → 픽 사라짐, 다른 요소 위치 그대로(reflow 없음)
- **SC-06**: SD 6장 중 3장만 업로드 → 빈 3 슬롯 투명, 다른 요소 위치 그대로
- **SC-07**: 외곽선 슬라이더 4~14 조정 → 타이틀 외곽선 두께 실시간 반영 + stroke≥12 시 lineHeight 자동 1.10 보정
- **SC-08**: 배치 모드 1200×628 + 1080×1080 두 사이즈 체크 + 4언어 입력 → ZIP 다운로드 8장 (4언어 × 2사이즈), KO 출력 2장만 고지문구

## Risks (R)

- **R-01 (의도된 동작 혼선)**: 픽 OFF 시 레이아웃 reflow 없이 빈 자리 노출 → 사용자가 버그로 오인 가능. **완화**: README/툴팁에 "픽 OFF는 픽만 숨김, 레이아웃 보존" 명시
- **R-02 (휘도 0.5 경계 깜빡임)**: 중간 명도 색(`#7F7F7F`)에서 컬러피커 미세 변경 시 테두리/글자색 갑작 반전. **완화**: NFR-05 hysteresis 0.46~0.54 적용
- **R-03 (EN 시각적 평이함)**: EN 3줄 균등 사이즈로 "Friends" 강조 효과 사라짐 (레퍼런스 1.6× 미반영). **완화**: 첫 출력 후 사용자 확인 → v2 라인별 가변 사이즈 추가 검토
- **R-04 (단일파일 비대화)**: 5,097 → 5,750라인 추정. **완화**: 큰 함수는 명명 분리(`buildSdShowcaseCanvas`, `prepSdShowcaseCfgImages` 등), 추후 모듈화 후보
- **R-05 (롤백)**: `TEMPLATE_KEYS`에서 신규 키 제거 + `applyTemplateSwitch` 분기 + state.sdshowcase + 신규 함수 5개 + UI 블록 삭제로 1커밋 롤백 가능. **완화**: 기능별 4 세션 커밋 분리 (Data / Renderer / Single-UI / Batch-UI)

---

## Impact Analysis

### Changed Resources

| Resource | Type | Change Description |
|----------|------|--------------------|
| `today-banner-designer.html` L1591 `TEMPLATE_KEYS` | JS const | `'sd-showcase'` 추가 |
| `today-banner-designer.html` L1769 부근 | JS const | `SDS_CANVAS_SPECS`, `SD_SHOWCASE_DEFAULT` 신규 |
| `today-banner-designer.html` L1987 `state.single` | JS state | `sdshowcase` 필드 추가 |
| `today-banner-designer.html` L2034 `state.batch` | JS state | `sd_*` 4개 필드 추가 + `langOverrides[lang].sds_*` 2 필드 |
| `today-banner-designer.html` L2365 `renderBanner` | JS function | `sd-showcase` 분기 추가 |
| `today-banner-designer.html` L3346 (canvas dispatcher) | JS function | `sd-showcase` 분기 추가 |
| `today-banner-designer.html` L3893 `applyTemplateSwitch` | JS function | `sd-showcase` 분기 추가 (사이즈 select 활성화 패턴) |
| `today-banner-designer.html` L4156 `handleSingleDownload` | JS function | `sd-showcase` 분기 추가 |
| `today-banner-designer.html` L4584 `renderBatchLangFields` | JS function | `isSDS` 분기 추가 (title textarea + pill input) |
| `today-banner-designer.html` L4738 `buildBatchCfgs` | JS function | `sd-showcase` 분기 추가 (selected sizes × 4 langs) |
| `today-banner-designer.html` HTML body | DOM | `<option value="sd-showcase">SD Showcase</option>` + 단건/배치 UI 블록 |

### Current Consumers (검증 대상)

| Resource | Operation | Impact |
|----------|-----------|--------|
| `TEMPLATE_KEYS` | iteration (UI dropdown render, `applyTemplateSwitch` 매칭) | None — append-only |
| `state.single` / `state.batch` | render, `syncBatchStateFromUI`, JSON serialize | None — 새 필드만 추가, 기존 필드 무영향 |
| `renderBanner` / `buildBannerCanvas` dispatcher | per-template branch | None — 새 분기만 추가 |
| `applyTemplateSwitch` | template switch UI sync | None — 새 분기만 추가, 기존 3 분기 변경 없음 |
| `handleSingleDownload` / `buildBatchCfgs` | export pipelines | None — 새 분기만 추가 |
| `renderBatchLangFields` | per-lang field render | None — 새 분기만 추가 |
| `_imgCache` | image cache (M-2 fix) | `updateStateImageAt` 헬퍼로 누수 방지 패턴 확장 |
| `LANG_PACK.ko.disclaimer` | KO 고지문구 출처 | Read-only 재사용 (Today Tap에서도 사용) |

### Verification

- [ ] 기존 3 템플릿(Today Tap, App Badge, App Store Screenshot) 단건/배치 모두 회귀 0건
- [ ] `TEMPLATE_KEYS` iteration 코드 (예: 헤더 `<select>` 옵션 렌더)에서 `sd-showcase` 정상 출력
- [ ] 배경 컬러피커 + 자동 대비 작동 시 기존 3 템플릿 영향 없음 (SD Showcase에서만 적용)
- [ ] `_imgCache` 6 SD 슬롯 교체 반복 시 누수 0건 (`_imgCache.size`가 슬롯 변경 후에도 6 이내 유지)

---

## Architecture Considerations

### Project Level

| Level | 적합도 | Selected |
|-------|--------|:--------:|
| Starter | 적합 — 단일 HTML, 외부 의존 없음, 인라인 JS+CSS | ☑ |
| Dynamic | 부적합 — BaaS/서버 없음 | ☐ |
| Enterprise | 부적합 — 단일 사용자 사내 툴 | ☐ |

### Key Architectural Decisions

| Decision | Options | Selected | Rationale |
|----------|---------|----------|-----------|
| File structure | Single HTML / Multi-file | **Single HTML** | 정책 — `today-banner-designer.html` 단일 파일 유지 |
| Rendering | DOM-only / Canvas-only / Both | **Canvas-only (DOM은 wrapper)** | App Store Screenshot v1.5 패턴, 픽셀 일관성, M-4 fix 검증됨 |
| State | Vanilla object / Reactive lib | **Vanilla `state.single` + `state.batch`** | 기존 패턴 유지 |
| Image cache | per-render / shared `_imgCache` | **Shared `_imgCache` + `updateStateImageAt`** | M-2 패턴 확장 (누수 방지) |
| Auto-contrast | Manual theme select / Luminance binary / WCAG ratio | **Luminance binary + hysteresis** | KISS, 사용자 결정 #10 |
| Title style | Full custom / Stroke-only slider / Fixed | **Stroke-only slider (4~14)** | YAGNI, 사용자 결정 #11 |
| Persistence | localStorage / sessionStorage / In-memory | **In-memory (기존 패턴)** | Checkpoint 1 결정, 일관성 |

### Clean Architecture Approach

```
Single HTML 정책 유지

today-banner-designer.html (5,097 → 5,750라인 추정)
├─ <style>
│   ├─ 기존 3 템플릿 CSS
│   └─ .tmpl-sd-showcase CSS (신규 ~30라인)
├─ <body>
│   ├─ 헤더 <select> (기존 + sd-showcase option)
│   ├─ 단건 모드 UI (기존 3 + sd-showcase data-tmpl 블록 신규)
│   └─ 배치 모드 UI (기존 3 + sd-showcase data-tmpl 블록 신규)
└─ <script>
    ├─ 상수 (LANG_PACK, AS_LANG_PACK, CANVAS_SPECS, APP_BADGE_CANVAS_SPECS,
    │   APPSTORE_SCREENSHOT_DEFAULT, **SDS_CANVAS_SPECS**, **SD_SHOWCASE_DEFAULT**)
    ├─ 헬퍼 (drawImageCover, drawImageContain, ensureFontsLoaded, _imgCache,
    │   updateStateImage, **getLuminance**, **getContrastPalette**, **updateStateImageAt**)
    ├─ 빌더 (Today Tap × 2 + App Badge × 2 + App Store × 2 + **SD Showcase × 5**)
    ├─ state (state.single + state.batch — 기존 + sd 필드 추가)
    └─ 이벤트 (단건/배치 UI 바인딩 — 기존 + sd UI 바인딩)
```

---

## Convention Prerequisites

### 8.1 기존 프로젝트 컨벤션 확인

- [x] `CLAUDE.md` 정책 섹션 존재 (v1.5+ — Single+Batch 양쪽 의무, 4언어 기본, 픽셀 퍼펙트 등)
- [x] 단일 HTML 인라인 `<script>` + `<style>` 정책
- [x] `data-tmpl` / `data-tmpl-hide` 속성으로 UI 분기
- [x] `_imgCache` + `updateStateImage` 메모리 관리 패턴 (M-2 fix)
- [x] `drawImageContain` (M-4 fix) — Canvas stretch 0%
- [ ] 신규 템플릿 추가 시 컨벤션 변경 없음 — 기존 패턴 그대로 적용

### 8.2 정의/검증할 컨벤션

| 항목 | 현재 상태 | 정의/검증할 내용 | 우선순위 |
|------|-----------|----------|:--------:|
| 사이즈 키 명명 | exists (`1x1`, `9x16`, `1200x628`) | 변경 없음 — `1x1`을 1080×1080으로 재사용 | High |
| state 필드 명명 | exists (per-template, `as_*`, `ab_*`) | `sd_*` (batch globals), `sds_*` (langOverrides) 추가 | High |
| 함수 명명 | exists (`buildXxxCanvas`, `prepXxxCfgImages`) | `buildSdShowcaseCanvas`, `prepSdShowcaseCfgImages` 동일 패턴 | High |
| 자동 대비 헬퍼 | missing | `getLuminance` + `getContrastPalette` 신규 (재사용 가능 형태) | Medium |
| 슬롯 배열 helper | missing | `updateStateImageAt(arr, idx, url)` 신규 (M-2 패턴 확장) | Medium |

### 8.3 환경 변수

해당 없음 — 단일 HTML 사내 툴, 환경 변수 없음.

---

## Implementation Order (Session-based)

`/pdca do sd-showcase --scope module-{N}` 분할 가능.

| Session | Module | 범위 | 추정 라인 |
|---------|--------|------|-----------|
| **1** | `data-switch` | TEMPLATE_KEYS·상수·state·`applyTemplateSwitch` 분기·헤더 `<option>` | ~50 |
| **2** | `canvas-renderer` | `getLuminance`/`getContrastPalette`/`updateStateImageAt`/`buildSdShowcaseCfg`/`prepSdShowcaseCfgImages`/`buildSdShowcaseCanvas`/`buildSdShowcaseBanner`/`buildSdShowcaseFilename` + `renderBanner`/canvas dispatcher 라우팅 | ~250 |
| **3** | `single-ui` | `data-tmpl="sd-showcase"` 단건 HTML 블록, 6 single 드롭존, 컬러피커, slider, 픽 토글, 타이틀/픽 input + state 바인딩 + `handleSingleDownload` 분기 | ~150 |
| **4** | `batch-ui-zip` | 배치 글로벌 4개, `renderBatchLangFields` SDS 분기, `copyLangFieldsToOthers` 확장, `syncBatchStateFromUI` 확장, 6 batch 드롭존, `buildBatchCfgs` SDS 분기 | ~200 |

---

## 변경 파일

### 코드
- `today-banner-designer.html` (단일 파일, +650 라인 추정)

### 문서
- `CLAUDE.md` — "현황" v1.6 항목 추가 (Session 1~4 진행 시점마다)
- `docs/01-plan/features/sd-showcase.plan.md` (이 문서)
- `docs/02-design/features/sd-showcase.design.md` (다음 단계 — `/pdca design sd-showcase`)
- `~/.claude/plans/brainstorming-spicy-plum.md` (Plan-Plus 산출물, 백업 보존)

### 재사용한 기존 자산
- `loadCachedImage()`, `_imgCache`, `updateStateImage()` — 이미지 캐시 (M-2 fix)
- `drawImageContain()` — SD 슬롯 무 stretch (M-4 fix)
- `prepCfgImages` 패턴 — `prepSdShowcaseCfgImages` 신규
- `setupDropzone()` 헬퍼 — 6 single + 6 batch 드롭존
- `getFontFamilyForLang(lang)` — 다국어 폰트 자동 스왑
- `ensureFontsLoaded()` — Pretendard/Noto JP/Noto TC 사전 디코드
- `LANG_PACK.ko.disclaimer` — "확률형 아이템 포함" 텍스트 출처
- `ctx.roundRect()` polyfill (L2562) — 픽 rounded-rect 그리기
- `canvasToDataURL()` 글로벌 wrapper — export 형식
- `applyTemplateSwitch` 패턴 — appstore-screenshot 9:16 잠금 로직 참조 (1200×628 + 1x1 활성 / 9:16 비활성으로 변형)

---

## Out of Scope (v1 명시 제외)

- ❌ 사용자 프리셋 저장 (텍스트, SD, 또는 둘 다)
- ❌ 다크 테마 명시 셀렉터 (배경 컬러피커 + 자동 대비로 대체)
- ❌ 9:16 사이즈
- ❌ 슬롯별 수동 위치/스케일/회전
- ❌ 픽 색상/모양/위치 커스터마이즈
- ❌ 외곽 테두리 두께/색상 UI 노출
- ❌ 고지문구 텍스트 편집 (KO 외 언어 강제 표시 포함)
- ❌ 그라데이션·이미지 배경
- ❌ SD 자동 그림자 추가
- ❌ **타이틀 라인별 가변 폰트 사이즈** (EN "Friends" 1.6× 강조 등)
- ❌ SD 슬롯 localStorage 영속화 (Checkpoint 1 결정 #15)

이상 11개 항목은 v1 완성 후 별도 PDCA cycle로 사용자 요청 시 개별 추가.

---

## Next Steps

1. [ ] `/pdca design sd-showcase` — 3 Architecture Options 비교 + 선택 + Design 문서 작성
2. [ ] `/pdca do sd-showcase --scope data-switch` — Session 1 구현 시작
3. [ ] `/pdca do sd-showcase --scope canvas-renderer` — Session 2
4. [ ] `/pdca do sd-showcase --scope single-ui` — Session 3
5. [ ] `/pdca do sd-showcase --scope batch-ui-zip` — Session 4
6. [ ] `/pdca analyze sd-showcase` — Gap 분석 (gap-detector)
7. [ ] `/pdca report sd-showcase` — 완료 리포트

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-04-29 | Plan-Plus 14 결정 + Checkpoint 1 (1결정) → PDCA Plan 정식화. 16 FR / 5 NFR / 8 SC / 5 R / 4 Sessions | ksk@superplanet.net |
| 0.2 | 2026-05-12 | **R5 Evolved Decision 추가**: r1 G2 후속 결정 `cellScale` 글로벌 슬라이더(50~150%) **폐기** → 슬롯별 `slotAdjustPerSize` (사이즈별 6 슬롯 × X/Y/Scale 개별) 진화. 사유: 12일 실사용 후 캐릭터별 자세/체형 차이로 글로벌 일괄 스케일 한계. R5 상세는 `docs/04-report/sd-showcase.report.md` §R5 Iteration. | ksk@superplanet.net |
