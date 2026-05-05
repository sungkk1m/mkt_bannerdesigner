# PDCA Plan — Pickup 템플릿 (v1.8)

**Feature**: pickup
**Created**: 2026-05-05
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/plan-plus` → `/pdca plan`
**Upstream Doc**: `~/.claude/plans/pdca-plan-plus-twinkly-hellman.md` (Plan-Plus brainstorming output)

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | Pickup 템플릿 추가 (6번째 템플릿) |
| 시작 | 2026-05-05 |
| 본체 파일 | `today-banner-designer.html` (단일 HTML, 7,169 → 추정 7,800라인) |
| 사이즈 | 1080×1080 + 1200×628 (9:16 미지원) |
| 언어 | ko / en / ja / zh-TW (4개 고정) |
| FR | 18건 |
| NFR | 6건 |
| SC | 9건 |
| R | 5건 |
| 결정사항 | 22건 (Plan-Plus brainstorming 22) |
| Implementation | 4 sessions (~700 lines 추가) |

### Value Delivered (4관점)

| 관점 | 내용 |
|---|---|
| **Problem** | 모바일 게임 신규/픽업 캐릭터 광고 배너에 등급(★) + 속성/클래스 + 캐릭터명을 한꺼번에 노출하는 템플릿이 기존 5개 템플릿에 부재. UA 매니저가 4언어 × 2사이즈 = 8장을 디자이너 수작업·외주에 의존 |
| **Solution** | 캐릭터 일러스트 + 키아트 배경 + 게임 로고 + 메탈릭 골드 이름 프레임(번들 PNG) + 등급/속성/클래스 텍스트를 자동화한 6번째 템플릿. 자유 텍스트(속성/클래스) + 사용자 색상 선택(이름 그라디언트)으로 다른 게임 픽업 광고에도 재사용 가능 |
| **Function/UX Effect** | 헤더 셀렉터 "Pickup" → 1080×1080 / 1200×628 자동 활성, 4언어 텍스트 입력 + 자산 3종 업로드 → Single 1초 / Batch 8장 ZIP 2초. CTA "지금 플레이하세요"는 코드 고정 매핑(ko/en/ja/zh-TW 자동 변환). 슬라이더 6개(로고 X/Y/Scale, 캐릭터 X/Y/Scale)로 레이아웃 유연성 확보 |
| **Core Value** | 픽업 캐릭터 배너 자산 생산 속도 60~120× 향상 + 4언어 자동 번역(CTA) + 메탈릭 골드 톤 일관성 + 다른 사내 게임 픽업 광고 재활용 가능 인프라화 |

---

## Context Anchor

> Auto-generated from Executive Summary. Propagated to Design/Do documents for context continuity.

| Key | Value |
|-----|-------|
| **WHY** | 신규/픽업 캐릭터를 강조하면서 등급·속성·클래스·캐릭터명을 같이 노출하는 광고 배너 템플릿 부재 — 디자이너 수작업으로 4언어×2사이즈=8장 생산 비효율 |
| **WHO** | UA Manager (Superplanet 사내 마케팅), 잠재적으로 다른 사내 게임 픽업 광고 운영자 |
| **RISK** | 번들 PNG(name-frame×2, star) 디자이너 미제공 시점에 코드 작업 진행 → placeholder fallback 필요 (R-1); 다국어 텍스트 길이 차이가 커서 이름 프레임 내부 영역 초과 → 자동 폰트 축소 필요 (R-2); 1200×628 가로 비율에서 캐릭터 일러스트가 정사각 PNG일 때 비율 왜곡 위험 (R-3) |
| **SUCCESS** | 단건 ≤1초 다운로드, 배치 8장 ZIP ≤2초; 8장 레퍼런스(미나/구미호) 비주얼 일치 (±5% 오차); CTA 4언어 자동 매핑; 슬라이더 6개 실시간 반영; 기존 5개 템플릿 회귀 0건 |
| **SCOPE** | Session 1: Data+Switch / Session 2: Canvas Renderer / Session 3: Single UI / Session 4: Batch UI+ZIP |

---

## Context

`today-banner-designer.html`(단일 HTML, v1.7 — Key Visual + Review 추가 후 7,169라인)는 기존 5개 템플릿(today-tap, app-badge, appstore-screenshot, sd-showcase, keyvisual-review)을 제공한다. 사용자(Mobile Game UA Manager)가 첨부한 2개 레퍼런스 이미지(몬길 STAR DIVE의 "미나" 픽업 광고, 1080×1080 + 1200×628)를 비주얼 모방한 6번째 템플릿을 추가해 픽업 캐릭터 광고 소재 제작 시간을 단축한다.

기존 템플릿은 모두 "특정 광고 면(Apple Today, App Store 스샷)" 또는 "단순 SD 라인업/리뷰 모방"에 집중된 반면, **Pickup은 신규 캐릭터 1인을 전면에 내세우면서 동시에 등급(★5 고정)·속성·클래스·메탈릭 골드 이름 프레임을 노출하는 픽업 전용 쇼케이스**로 다른 게임 픽업 광고에도 재활용 가능하도록 자유 텍스트(속성/클래스) + 사용자 색상 선택(이름 그라디언트) 등 유연성을 확보한다.

번들 자산 + 다중 사이즈 조합은 KVR(단일 사이즈)와 달리 **첫 시도**다. 디자이너 제공 PNG 3종(`name-frame-1x1.png`, `name-frame-1200x628.png`, `star.png`)을 `repo/assets/pickup/`에 위치시키고, 코드는 자산 미제공 시점에도 placeholder fallback으로 개발 진행 가능하도록 설계한다.

**스킬 매핑**: 추후 비슷한 요청은 `/plan-plus pickup-v2`로 시작. 보조 — `bkit:phase-3-mockup`(레이아웃 검증), `bkit:phase-5-design-system`(메탈릭 골드 톤 일관성).

---

## 사용자 결정 요약 (확정 — 2026-05-05, Plan-Plus brainstorming 22)

| # | 항목 | 결정 |
|---|------|------|
| 1 | 템플릿 이름 (헤더 드롭다운) | **"Pickup"** (key: `pickup`) |
| 2 | 사이즈 | **1080×1080 + 1200×628** (9:16 미지원) |
| 3 | 언어 | ko / en / ja / zh-TW (4개 고정 + LANG_PACK 폰트 자동 스왑) |
| 4 | 게임 로고 자산 | **사용자 업로드** (단일 파일, 4언어 공통) |
| 5 | 이름 프레임 자산 | **번들 PNG + 텍스트 오버레이** (`assets/pickup/name-frame-{size}.png`, border만 / 내부 transparent) |
| 6 | 이름 프레임 사이즈 정책 | **사이즈별 분리 2 PNG** (`name-frame-1x1.png` + `name-frame-1200x628.png`) |
| 7 | 별 자산 | **번들 단일 PNG** (`assets/pickup/star.png` 1개, 코드에서 5번 자동 스케일 배치) |
| 8 | 등급 | **5★ 고정** (가변 슬라이더 없음) |
| 9 | 속성/클래스 | **자유 텍스트 입력 (2개 필드)** — 언어별 별도 입력 |
| 10 | 속성 옆 아이콘 | **아이콘 없음** — 텍스트만 (`{속성} | {클래스}` 구분자) |
| 11 | 배경/캐릭터 이미지 계층 | **2개 별도 업로드** (배경 키아트 1장 + 캐릭터 transparent PNG 1장) |
| 12 | 사용자 업로드 사이즈 정책 | **한 장 공용** (today-tap 패턴, 두 사이즈에 자동 적용) |
| 13 | CTA "지금 플레이하세요" | **코드 고정 매핑** (ko/en/ja/zh-TW 자동 변환, 사용자 수정 불가) |
| 14 | 캐릭터 설명 (예: "운명의 힘을 품은 구미호") | **언어별 수동 입력 (4필드)** |
| 15 | 캐릭터명 (예: "미나") | **언어별 수동 입력 (4필드)** |
| 16 | 속성/클래스 다국어 | **언어별 수동 입력 (4언어 × 2필드)** |
| 17 | 레이아웃 (사이즈별) | **레퍼런스 동일 구조** (각 사이즈 레퍼런스 그대로) |
| 18 | 캐릭터명 텍스트 스타일 | **사용자 그라디언트 2색 선택** (상→하), 기본 골드 `#FFD700` → 흰 `#FFFFFF` |
| 19 | 사용자 컨트롤 (슬라이더) | **캐릭터 X/Y/Scale + 게임 로고 X/Y/Scale** (총 6개) — 배경 키아트 슬라이더 미제공 |
| 20 | 1200×628 CTA | **두 사이즈 모두 표시** (CTA 위치는 사이즈별 자동 배치) |
| 21 | CTA 시각 스타일 | **흰 텍스트 + drop-shadow** (레퍼런스 동일) |
| 22 | 운용 모드 | **Single + Batch 모두 지원** (CLAUDE.md 정책 의무) |

### 제외 사항 (요구사항 명시)

- ❌ 하단 copyright 문구 ("© Netmarble Corp...." 등)
- ❌ 우상단 게임 회사 로고 (netmarble 등)
- ❌ 9:16 사이즈
- ❌ 별 개수 가변 (5★ 고정)
- ❌ 속성 옆 작은 아이콘 (🔥, ⚪ 등)
- ❌ 배경 키아트 위치/크기 슬라이더 (cover 자동)
- ❌ 배경 어두움(dim) 슬라이더
- ❌ CTA/캐릭터명 폰트 크기 슬라이더 (자동 피팅)

---

## Functional Requirements (FR)

- **FR-01**: 헤더 템플릿 셀렉터에 `pickup` 옵션 추가 (6번째)
- **FR-02**: `TEMPLATE_KEYS` 배열에 `'pickup'` 추가 + `.tmpl-pickup` CSS 스코프
- **FR-03**: 신규 상수 — `PICKUP_CTA_MAP` (ko/en/ja/zh-TW 4언어 자동 매핑) + `PICKUP_ASSETS` (frame 2 + star 1 경로) + `PICKUP_CANVAS_SPECS` (1080×1080 + 1200×628 사이즈별 좌표 테이블) + `PICKUP_DEFAULT` (4언어 텍스트 + 6 슬라이더 + 그라디언트 2색 + 자산 3 슬롯)
- **FR-04**: `applyTemplateSwitch` 분기 — `pickup` 선택 시 `s-size`에서 `1x1`+`1200x628` 활성, `9x16` disabled. 배치 사이즈 체크박스 동기화 (sd-showcase 패턴 준용)
- **FR-05**: state 확장 — `state.single.pickup` (deepCopy `PICKUP_DEFAULT`), `state.batch.pickup` (deepCopy) — KVR R13 패턴 준용 (배치 자산 분리)
- **FR-06**: 단건 모드 자산 슬롯 3개 — `#s-drop-pickup-logo`, `#s-drop-pickup-keyart`, `#s-drop-pickup-character` — `setupDropzone()` + `updateStateImage()` 헬퍼 (M-2 fix 패턴)
- **FR-07**: 단건 모드 슬라이더 6개 — `#s-pickup-logo-{x,y,scale}`, `#s-pickup-char-{x,y,scale}` — `range` input + 실시간 미리보기 반영
- **FR-08**: 단건 모드 색상 picker 2개 — `#s-pickup-name-grad-top`, `#s-pickup-name-grad-bottom` (기본 `#FFD700`, `#FFFFFF`)
- **FR-09**: 단건 모드 4언어 텍스트 입력 — 현재 선택된 언어의 4 필드만 노출 (description, name, element, class) + 언어 스위처 (today-tap 패턴)
- **FR-10**: 배치 모드 자산 슬롯 3개 (별도) — `#b-drop-pickup-{logo,keyart,character}` — `state.batch.pickup`에 저장 (KVR R13 패턴)
- **FR-11**: 배치 모드 슬라이더 6개 + 색상 picker 2개 (별도, prefix `b-`) — `state.batch.pickup`에 저장
- **FR-12**: 배치 모드 4언어 텍스트 입력 — `renderBatchLangFields()` `pickup` 분기 추가, 4언어 × 4 필드 = 16개 input/textarea 자동 렌더 (description textarea + name input + element input + class input)
- **FR-13**: 자동 폰트 축소 — 캐릭터명/속성/클래스 텍스트가 프레임 내부 영역을 넘으면 `ctx.measureText` 기반 자동 축소 (sd-showcase `fitSdsTitle` 패턴 준용)
- **FR-14**: Canvas 렌더러 `buildPickupCanvas(cfg)` — 10단계 그리기 순서:
  1. 배경 fillStyle (cfg.bgColor 또는 검정 fallback)
  2. 배경 키아트 `drawImageCover` (사이즈별 cover, 슬라이더 없음)
  3. 캐릭터 일러스트 `drawImageContain` (X/Y/scale 슬라이더 적용)
  4. 게임 로고 `drawImageContain` (X/Y/scale 슬라이더 적용, default 좌측 상단)
  5. 캐릭터 설명 텍스트 (현재 언어, drop-shadow)
  6. 이름 프레임 PNG (사이즈별 자산 로드, `_imgCache` 활용)
  7. 캐릭터명 텍스트 — `createLinearGradient(top→bottom)` fillStyle (사용자 2색)
  8. 별 5개 (`star.png` 5번 반복, 자동 스케일·간격 계산)
  9. 속성/클래스 텍스트 — `{속성} | {클래스}` 구분자 (자동 폰트 축소)
  10. CTA 텍스트 — `PICKUP_CTA_MAP[lang]`, 흰 텍스트 + drop-shadow
- **FR-15**: DOM 미리보기 `renderPickupBanner(cfg)` — Canvas embed 형태로 단순화 (sd-showcase 패턴 준용, DOM/Canvas 이중 구현 회피)
- **FR-16**: 단건 다운로드 — `handleSingleDownload` `pickup` 분기 추가, `buildPickupCfg → prepPickupCfgImages → buildPickupCanvas → canvasToDataURL → buildPickupFilename`
- **FR-17**: 배치 ZIP — `buildBatchCfgs` `pickup` 분기 (selected sizes × 4 langs fan-out), 글로벌 ZIP 다운로드 흐름 재사용
- **FR-18**: 파일명 규칙 — `{prefix}_pickup_{lang}_{size}.{ext}` (sizeKey 매핑: `1x1` → `1080x1080`, `1200x628` → `1200x628`); slug 빈 문자열 시 `'pickup'` fallback (M-3 mitigation 패턴)

## Non-Functional Requirements (NFR)

- **NFR-01**: Canvas 기반 export (`USE_CANVAS_EXPORT=true` 동선 유지) — html-to-image 미사용
- **NFR-02**: 폰트 — 기존 `getFontFamilyForLang(lang)` 재사용 (Pretendard/Noto Sans JP/Noto Sans TC 자동 스왑) + `ensureFontsLoaded()` 사전 디코드 재사용
- **NFR-03**: 이미지 캐시 — `_imgCache` 재사용. 번들 PNG (frame×2 + star) 1회 디코드 → 8장 batch 모두 공유. 사용자 자산(logo + keyart + character) 1회 decode 후 4언어×2사이즈=8장 공유 (M-2 + bugfix 패턴 확장)
- **NFR-04**: 단일 HTML 정책 유지 — 외부 모듈/번들 도입 금지, 인라인 `<script>` + `<style>` 내 추가
- **NFR-05**: 번들 PNG 자산 분리 — `repo/assets/pickup/` 폴더 신설. KVR(`assets/keyvisual-review/`)와 동일 패턴. 자산 미제공 시 코드 placeholder fallback으로 개발 가능
- **NFR-06**: 성능 목표 — Single 미리보기 ≤500ms, Single 다운로드 ≤1초, Batch 8장 ZIP ≤2초 (기존 템플릿 동일 기준)

## Scenarios (SC)

- **SC-01**: 사용자가 헤더 셀렉터에서 "Pickup" 선택 → `s-size`에서 1x1+1200x628만 활성, 9:16 비활성. 단건/배치 패널이 Pickup 전용 UI로 전환
- **SC-02**: 사용자가 게임 로고/배경 키아트/캐릭터 PNG 3종 업로드 + ko 4 필드 입력 ("운명의 힘을 품은 구미호" / "미나" / "불" / "원거리") → 1080×1080 미리보기에 레퍼런스와 ±5% 오차 내 일치
- **SC-03**: 사용자가 1200×628로 전환 → 레이아웃 자동 재배치 (좌측 텍스트 영역 + 우측 캐릭터), 자산 3종 그대로 적용 (한 장 공용)
- **SC-04**: 사용자가 슬라이더 6개 (로고 X/Y/Scale, 캐릭터 X/Y/Scale) 조정 → 미리보기 실시간 반영, drop-shadow / 그라디언트 / 별 5개 위치 모두 일관 유지
- **SC-05**: 사용자가 캐릭터명 그라디언트 색상 picker 2개 변경 (예: 상=`#F5E6A1`, 하=`#B8860B`) → 캐릭터명 텍스트 fillStyle 그라디언트 즉시 반영
- **SC-06**: 언어 전환 (ko → en → ja → zh-TW) → 폰트 자동 변경 (Pretendard / Noto Sans JP / Noto Sans TC), CTA 텍스트가 `PICKUP_CTA_MAP`대로 변경, 4 텍스트 필드 입력값이 언어별로 독립 유지
- **SC-07**: 사용자가 ja에서 캐릭터명을 "미나" 대신 "ミナ"로 입력 → ja 출력에만 반영, ko/en/zh-TW 출력은 영향 없음
- **SC-08**: 캐릭터 설명/이름/속성 중 어느 한 텍스트가 프레임 내부 영역을 넘침 → `ctx.measureText` 기반 자동 폰트 축소로 1줄 fit (자동 줄바꿈은 별도 옵션 미지원, v1)
- **SC-09**: 배치 모드 1080×1080 + 1200×628 두 사이즈 체크 + 4언어 입력 → ZIP 다운로드 8장 (4언어 × 2사이즈), 파일명 `{prefix}_pickup_{lang}_{size}.png` 규칙 준수, 8장 모두 ≤2초 생성

## Risks (R)

- **R-01 (디자이너 자산 미도착)**: 번들 PNG (`name-frame-1x1.png`, `name-frame-1200x628.png`, `star.png`) 디자이너 미제공 시점에 코드 작업 진행 → 미리보기/다운로드가 깨진 이미지로 보일 수 있음. **완화**: `loadImg()` 실패 시 콘솔 경고 + 프레임은 흰색 stroke rect placeholder, 별은 ★ Unicode 텍스트 placeholder로 fallback 그려서 개발 진행 가능. 자산 도착 후 placeholder 자동 제거 (정상 PNG 우선 로드)
- **R-02 (다국어 텍스트 길이 차이)**: 캐릭터명/속성/클래스 다국어 길이 변동이 커서 (예: ko "원거리" 3자 vs en "Ranged" 6자) 프레임 내부 영역 초과 가능. **완화**: FR-13 자동 폰트 축소 (sd-showcase `fitSdsTitle` 패턴, 80%까지 단계 축소)
- **R-03 (캐릭터 일러스트 비율 왜곡)**: 1200×628 가로 비율에서 정사각 캐릭터 PNG가 부적합한 위치/스케일로 보일 수 있음 (1080×1080은 정사각이라 자연스러움). **완화**: 사이즈별 default `charY/charScale` 슬라이더 값을 `PICKUP_CANVAS_SPECS`에 분리 정의 (1200×628은 우측 영역 60% 사용, 1080×1080은 우측-중앙 80% 사용)
- **R-04 (단일 파일 비대화)**: 7,169 → 7,800라인 추정 (+631). **완화**: 큰 함수는 명명 분리(`buildPickupCanvas`, `prepPickupCfgImages` 등), 추후 모듈화 후보 (R-04 from sd-showcase 동일 기조)
- **R-05 (롤백)**: `TEMPLATE_KEYS`에서 `'pickup'` 제거 + `applyTemplateSwitch` 분기 + state.pickup + 신규 함수 5개 + UI 블록 + `repo/assets/pickup/` 폴더 삭제로 1커밋 롤백 가능. **완화**: 기능별 4 세션 커밋 분리 (Data / Renderer / Single-UI / Batch-UI)

---

## Impact Analysis

### Changed Resources

| Resource | Type | Change Description |
|----------|------|--------------------|
| `today-banner-designer.html` `TEMPLATE_KEYS` (~L1951 영역) | JS const | `'pickup'` 추가 |
| `today-banner-designer.html` (~L2200 KVR_LANG_PACK 다음) | JS const | `PICKUP_CTA_MAP`, `PICKUP_ASSETS`, `PICKUP_CANVAS_SPECS`, `PICKUP_DEFAULT` 신규 |
| `today-banner-designer.html` `state.single` (~L2495 영역) | JS state | `pickup` 필드 추가 (deepCopy `PICKUP_DEFAULT`) |
| `today-banner-designer.html` `state.batch` (~L2518 영역, KVR R13 다음) | JS state | `pickup` 필드 추가 (deepCopy `PICKUP_DEFAULT`) |
| `today-banner-designer.html` `renderBanner` (~L4321 영역) | JS function | `pickup` 분기 추가 (Canvas wrapper로 단순화) |
| `today-banner-designer.html` canvas dispatcher (~L4809 영역) | JS function | `pickup` 분기 추가 |
| `today-banner-designer.html` `applyTemplateSwitch` (~L5694 영역) | JS function | `pickup` 분기 추가 (사이즈 select 9x16 disabled 패턴, sd-showcase 준용) |
| `today-banner-designer.html` `handleSingleDownload` (~L6000 영역) | JS function | `pickup` 분기 추가 |
| `today-banner-designer.html` `renderBatchLangFields` (~L6491 영역) | JS function | `pickup` 분기 추가 (description textarea + name/element/class input × 4언어) |
| `today-banner-designer.html` `buildBatchCfgs` (~L6738 영역) | JS function | `pickup` 분기 추가 (selected sizes × 4 langs fan-out) |
| `today-banner-designer.html` `handleBatchExportZip` (~L7000 영역) | JS function | `pickup` 분기에서 사용자 자산 사전 디코드 추가 |
| `today-banner-designer.html` HTML body | DOM | `<option value="pickup">Pickup</option>` + 단건/배치 UI 블록 (`data-tmpl="pickup"`) |
| `today-banner-designer.html` `<style>` | CSS | `.tmpl-pickup` 사이즈별 레이아웃 (`.size-1x1`, `.size-1200x628`) ~50라인 |
| `repo/assets/pickup/name-frame-1x1.png` | PNG asset | 신규 (디자이너 제공) — border만, 내부 transparent |
| `repo/assets/pickup/name-frame-1200x628.png` | PNG asset | 신규 (디자이너 제공) — border만, 내부 transparent |
| `repo/assets/pickup/star.png` | PNG asset | 신규 (디자이너 제공) — 단일 별 PNG, 코드에서 5번 자동 스케일 |
| `CLAUDE.md` | doc | "현황" v1.8 항목 추가 (Session 1~4 진행 시점마다) |
| `README.md` | doc | Pickup 사용법 추가 (4개 언어 섹션) |

### Current Consumers (검증 대상)

| Resource | Operation | Impact |
|----------|-----------|--------|
| `TEMPLATE_KEYS` | iteration (UI dropdown render, `applyTemplateSwitch` 매칭) | None — append-only |
| `state.single` / `state.batch` | render, syncState, JSON serialize | None — 새 필드만 추가, 기존 필드 무영향 |
| `renderBanner` / canvas dispatcher | per-template branch | None — 새 분기만 추가 |
| `applyTemplateSwitch` | template switch UI sync | None — 새 분기만 추가, 기존 5 분기 변경 없음 |
| `handleSingleDownload` / `buildBatchCfgs` | export pipelines | None — 새 분기만 추가 |
| `renderBatchLangFields` | per-lang field render | None — 새 분기만 추가 |
| `_imgCache` + `updateStateImage` | image cache (M-2 fix) | 패턴 그대로 활용, 누수 방지 보장 |
| `LANG_PACK[lang]` | 언어 라벨 + 폰트 자동 스왑 | Read-only 재사용 |
| `getFontFamilyForLang(lang)` | Canvas 폰트 자동 선택 | Read-only 재사용 |
| `drawImageCover` / `drawImageContain` | 이미지 그리기 헬퍼 | Read-only 재사용 (배경=cover, 캐릭터/로고/프레임=contain) |

### Verification

- [ ] 기존 5 템플릿(today-tap, app-badge, appstore-screenshot, sd-showcase, keyvisual-review) 단건/배치 모두 회귀 0건
- [ ] `TEMPLATE_KEYS` iteration 코드 (헤더 `<select>` 옵션 렌더, `applyTemplateSwitch` 매칭)에서 `pickup` 정상 출력
- [ ] 자산 폴더 `repo/assets/pickup/` 비어 있을 때 placeholder fallback 정상 작동 (개발 가능 여부)
- [ ] 자산 도착 후 정상 PNG 로드 + placeholder 자동 제거
- [ ] `_imgCache` 자산 교체 반복 시 누수 0건 (logo/keyart/character × 단건/배치 = 6 슬롯 + 번들 3 PNG = 9 entries 유지)

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
| Rendering | DOM-only / Canvas-only / Both | **Canvas-only (DOM은 wrapper)** | sd-showcase v1.6 + KVR v1.7 패턴, 픽셀 일관성 |
| State | Vanilla object / Reactive lib | **Vanilla `state.single.pickup` + `state.batch.pickup`** | 기존 패턴 유지 (KVR R13 배치 자산 분리 패턴) |
| Image cache | per-render / shared `_imgCache` | **Shared `_imgCache` + `updateStateImage`** | M-2 패턴 일관 적용 |
| Bundled asset 전략 | inline base64 / external file | **External file (`assets/pickup/*.png`)** | KVR 패턴 일관, 자산 교체 용이 (디자이너 협업) |
| 자산 사이즈 정책 | 단일 PNG 자동 스케일 / 사이즈별 분리 | **이름 프레임은 사이즈별 분리, 별은 단일 PNG** | 사용자 결정 #6, #7 — 프레임은 비율 차이 큼, 별은 단순 |
| 사용자 자산 사이즈 정책 | 사이즈별 / 한 장 공용 | **한 장 공용** | today-tap 패턴, 사용자 입력 부담 절반 (사용자 결정 #12) |
| CTA 다국어 | 사용자 입력 / 코드 매핑 | **코드 고정 매핑** | 사용자 결정 #13, 입력 불필요 |
| 캐릭터명 색상 | 단일 색 / 그라디언트 2색 / 프리셋 | **그라디언트 2색 사용자 선택** | 사용자 결정 #18, 메탈릭 골드 톤 보존 + 게임별 톤 변경 가능 |
| 사용자 컨트롤 슬라이더 | 자동 / 미니멀 / 풀 커스터마이즈 | **6 슬라이더 (로고+캐릭터 X/Y/Scale)** | 사용자 결정 #19, 핵심 자유도만 노출 |

### Clean Architecture Approach

```
Single HTML 정책 유지

today-banner-designer.html (7,169 → 7,800라인 추정)
├─ <style>
│   ├─ 기존 5 템플릿 CSS
│   └─ .tmpl-pickup CSS (신규 ~50라인 — size-1x1, size-1200x628 분기)
├─ <body>
│   ├─ 헤더 <select> (기존 5 + pickup option)
│   ├─ 단건 모드 UI (기존 5 + data-tmpl="pickup" 블록 신규)
│   └─ 배치 모드 UI (기존 5 + data-tmpl="pickup" 블록 신규)
└─ <script>
    ├─ 상수 (LANG_PACK, ..., KVR_LANG_PACK, **PICKUP_CTA_MAP**, **PICKUP_ASSETS**,
    │   **PICKUP_CANVAS_SPECS**, **PICKUP_DEFAULT**)
    ├─ 헬퍼 (drawImageCover, drawImageContain, ensureFontsLoaded, _imgCache,
    │   updateStateImage, getFontFamilyForLang, fitSdsTitle 패턴 재사용)
    ├─ 빌더 (Today Tap × 2 + App Badge × 2 + App Store × 2 + SD Showcase × 5 +
    │   KVR × 5 + **Pickup × 5** [buildPickupCfg, prepPickupCfgImages,
    │   buildPickupCanvas, buildPickupBanner, buildPickupFilename])
    ├─ state (state.single + state.batch — 기존 + state.{single,batch}.pickup 추가)
    └─ 이벤트 (단건/배치 UI 바인딩 — 기존 + bindPickupSingleUI, bindPickupBatchUI)
```

---

## Convention Prerequisites

### 8.1 기존 프로젝트 컨벤션 확인

- [x] `CLAUDE.md` 정책 섹션 존재 (v1.5+ — Single+Batch 양쪽 의무, 4언어 기본, 픽셀 퍼펙트 등)
- [x] 단일 HTML 인라인 `<script>` + `<style>` 정책
- [x] `data-tmpl` / `data-tmpl-hide` 속성으로 UI 분기
- [x] `_imgCache` + `updateStateImage` 메모리 관리 패턴 (M-2 fix)
- [x] `drawImageContain` (M-4 fix) — Canvas stretch 0%
- [x] `repo/assets/{template-name}/` 번들 자산 패턴 (KVR)
- [x] `state.batch.{template}` 배치 자산 분리 (KVR R13)
- [ ] 신규 템플릿 추가 시 컨벤션 변경 없음 — 기존 패턴 그대로 적용

### 8.2 정의/검증할 컨벤션

| 항목 | 현재 상태 | 정의/검증할 내용 | 우선순위 |
|------|-----------|----------|:--------:|
| 사이즈 키 명명 | exists (`1x1`, `9x16`, `1200x628`) | 변경 없음 — `1x1`을 1080×1080으로 재사용 | High |
| state 필드 명명 | exists (per-template) | `state.single.pickup`, `state.batch.pickup` (KVR R13 패턴) | High |
| 함수 명명 | exists (`buildXxxCanvas`, `prepXxxCfgImages`) | `buildPickupCanvas`, `prepPickupCfgImages` 동일 패턴 | High |
| 자산 폴더 | exists (`assets/keyvisual-review/`) | `assets/pickup/` 신설 (KVR 패턴) | High |
| 사이즈별 자산 분리 | first-time (KVR은 단일 사이즈) | `name-frame-{1x1, 1200x628}.png` 명명 규칙 정립 | Medium |
| CTA 다국어 매핑 상수 | first-time | `PICKUP_CTA_MAP` 패턴 — 향후 다른 fixed-CTA 템플릿 재사용 가능 | Low |
| placeholder fallback | first-time | 번들 자산 누락 시 stroke rect + ★ Unicode fallback (개발용) | Medium |

### 8.3 환경 변수

해당 없음 — 단일 HTML 사내 툴, 환경 변수 없음.

---

## Implementation Order (Session-based)

`/pdca do pickup --scope module-{N}` 분할 가능.

| Session | Module | 범위 | 추정 라인 |
|---------|--------|------|-----------|
| **1** | `data-switch` | TEMPLATE_KEYS·상수(`PICKUP_CTA_MAP`, `PICKUP_ASSETS`, `PICKUP_CANVAS_SPECS`, `PICKUP_DEFAULT`)·state(`state.{single,batch}.pickup`)·`applyTemplateSwitch` 분기·헤더 `<option>`·자산 폴더 `repo/assets/pickup/` 생성 | ~80 |
| **2** | `canvas-renderer` | `buildPickupCfg`/`prepPickupCfgImages`/`buildPickupCanvas` (10단계 그리기)/`buildPickupBanner`/`buildPickupFilename` + `renderBanner`/canvas dispatcher 라우팅 + placeholder fallback (자산 누락 시) | ~280 |
| **3** | `single-ui` | `data-tmpl="pickup"` 단건 HTML 블록, 자산 dropzone 3개, 슬라이더 6개, 색상 picker 2개, 4언어 텍스트 4 필드 + 언어 스위처, state 바인딩 + `handleSingleDownload` 분기 | ~180 |
| **4** | `batch-ui-zip` | 배치 자산 dropzone 3개(별도 prefix `b-`), 배치 슬라이더 6개·picker 2개, `renderBatchLangFields` pickup 분기(4언어×4필드=16개), `buildBatchCfgs` pickup 분기, `handleBatchExportZip` 사전 디코드 | ~160 |

---

## 변경 파일

### 코드
- `today-banner-designer.html` (단일 파일, +700 라인 추정)

### 자산 (디자이너 제공)
- `repo/assets/pickup/name-frame-1x1.png` (신규)
- `repo/assets/pickup/name-frame-1200x628.png` (신규)
- `repo/assets/pickup/star.png` (신규)

### 문서
- `CLAUDE.md` — "현황" v1.8 항목 추가 (Session 1~4 진행 시점마다)
- `README.md` — Pickup 사용법 4언어 추가 섹션
- `docs/01-plan/features/pickup.plan.md` (이 문서)
- `docs/02-design/features/pickup.design.md` (다음 단계 — `/pdca design pickup`)
- `~/.claude/plans/pdca-plan-plus-twinkly-hellman.md` (Plan-Plus brainstorming 산출물, 백업 보존)

### 재사용한 기존 자산
- `loadCachedImage()`, `_imgCache`, `updateStateImage()` — 이미지 캐시 (M-2 fix)
- `drawImageContain()` — 캐릭터/로고/프레임 무 stretch (M-4 fix)
- `drawImageCover()` — 배경 키아트 cover 채움
- `prepCfgImages` 패턴 — `prepPickupCfgImages` 신규
- `setupDropzone()` 헬퍼 — 자산 3 single + 3 batch 드롭존
- `getFontFamilyForLang(lang)` — 다국어 폰트 자동 스왑
- `ensureFontsLoaded()` — Pretendard/Noto JP/Noto TC 사전 디코드
- `LANG_PACK[lang].label` — 언어 라벨
- `canvasToDataURL()` 글로벌 wrapper — export 형식
- `applyTemplateSwitch` 패턴 — sd-showcase 9:16 잠금 분기 참조 (1080×1080 + 1200×628 활성 / 9:16 비활성)
- `fitSdsTitle` (sd-showcase) — 자동 폰트 축소 패턴 참조 (캐릭터명/속성/클래스)
- `renderBatchLangFields` (today-tap/sd-showcase/appstore) — 배치 4언어 필드 자동 렌더 패턴

---

## Out of Scope (v1 명시 제외)

- ❌ 사용자 프리셋 저장 (텍스트, 자산, 또는 둘 다)
- ❌ 9:16 사이즈 (1080×1920)
- ❌ 별 개수 가변 (1~4★ 표시)
- ❌ 별 색상 사용자 변경 (PNG 고정 골드)
- ❌ 캐릭터명 단일 색 / 프리셋 그라디언트 (사용자 2색 선택만)
- ❌ 속성 옆 작은 아이콘 (🔥 / ⚪ 등)
- ❌ 배경 키아트 위치/크기 슬라이더
- ❌ 배경 어두움(dim) 슬라이더
- ❌ CTA/캐릭터명 폰트 크기 슬라이더 (자동 피팅만)
- ❌ 캐릭터 일러스트 자동 좌우반전 (sd-showcase 1200×628 패턴 미적용 — 단일 캐릭터)
- ❌ 다중 캐릭터 슬롯 (1인 픽업만)
- ❌ 캐릭터명 자동 줄바꿈 (1줄 + 자동 폰트 축소만)
- ❌ 다른 게임용 게임 로고 번들 (사용자 업로드만)
- ❌ 하단 copyright 자동 텍스트
- ❌ 우상단 게임 회사 로고

이상 15개 항목은 v1 완성 후 별도 PDCA cycle로 사용자 요청 시 개별 추가.

---

## Next Steps

1. [ ] 디자이너에게 자산 사양 전달:
   - `name-frame-1x1.png` (border만, 내부 transparent, 추천 ~800×220px)
   - `name-frame-1200x628.png` (border만, 내부 transparent, 추천 ~480×160px)
   - `star.png` (단일 별, 추천 ~80×80px, 코드에서 5번 자동 스케일·배치)
2. [ ] `/pdca design pickup` — 3 Architecture Options 비교 + 선택 + Design 문서 작성
3. [ ] `/pdca do pickup --scope data-switch` — Session 1 구현 시작 (자산 도착 전 placeholder fallback으로 진행 가능)
4. [ ] `/pdca do pickup --scope canvas-renderer` — Session 2
5. [ ] `/pdca do pickup --scope single-ui` — Session 3
6. [ ] `/pdca do pickup --scope batch-ui-zip` — Session 4
7. [ ] `/pdca analyze pickup` — Gap 분석 (gap-detector)
8. [ ] `/pdca report pickup` — 완료 리포트
