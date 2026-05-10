# PDCA Plan — Steam Review 템플릿 (v1.9)

**Feature**: `steam-review`
**Created**: 2026-05-10
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/plan-plus` (`superpowers:brainstorming` 4-round AskUserQuestion) → `/pdca plan`
**Upstream Doc**: `~/.claude/plans/plan-plus-brainstorming-let-s-logical-puddle.md`
**References**:
- `docs/01-plan/features/keyvisual-review.plan.md` (베이스 패턴)
- `docs/01-plan/features/pickup.plan.md` (다중 사이즈 처리 패턴)

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | Steam Review 템플릿 (7번째 템플릿) |
| 시작 | 2026-05-10 |
| 본체 파일 | `today-banner-designer.html` (단일 HTML, 현행 ~8,437 라인 → 추정 ~9,290 라인) |
| 사이즈 | **1080×1080 + 1200×628** (9:16 미지원) |
| 언어 | ko / en / ja / zh-TW (4개 고정) |
| FR | 18건 |
| NFR | 6건 |
| SC | 9건 |
| R | 7건 |
| 결정사항 | 8건 (Brainstorming AskUserQuestion 4-round) |
| Implementation | ~4 sessions (~855 라인 추가 + assets 5 PNG → base64 인라인) |

### Value Delivered (4관점)

| 관점 | 내용 |
|---|---|
| **Problem** | Steam 스토어 분위기의 "리뷰 + 평가" 광고 패턴은 신뢰도와 CTR에 매우 효과적이지만, 현재 4언어 × 2사이즈 = 8장을 매번 디자이너에게 의뢰해야 함. 기존 KVR 템플릿(앱스토어 모티브)과는 별개로, **Steam 특유의 다크 블루 톤 + 추천/플레이시간 카드 UI**가 필요함 |
| **Solution** | 7번째 템플릿 `steam-review`. 키비주얼 1장 업로드(전 언어 공유) + 게임 타이틀·설명·태그 5종·리뷰 본문 4종을 4언어 각자 입력 → 1080×1080(리뷰 3장)·1200×628(리뷰 4장) 자동 fan-out. 평가 라벨/플레이시간/리뷰어 아이콘은 언어별 하드코딩으로 일관성 보장 |
| **Function/UX Effect** | 헤더 드롭다운 "Steam Review" → 1080×1080·1200×628 자동 활성, 키비주얼 업로드 + scale/x/y slider → 4언어 텍스트 입력 → 단건 1초 / 배치 8장 ZIP ~3초. 한국어 4번째 태그 디폴트 = `확률형 아이템 포함`(규제 대응) 자동 채움. 리뷰어 4명(파란머리·기사·핑크·코기) 고정 + 슬롯별 고정 플레이시간(56.9/4.8/6.4/203.4 hrs) |
| **Core Value** | UA 자산 생산 속도 60×↑ + Steam-스타일 브랜딩 즉시 활용 + 한국 규제 대응 자동화 + 다른 게임 즉시 재활용(키비주얼만 교체). 6번째 템플릿 후 7번째로 templating 시스템 검증 |

---

## Context Anchor

> Auto-generated from Executive Summary. Propagated to Design/Do documents for context continuity.

| Key | Value |
|-----|-------|
| **WHY** | Steam 스토어 분위기 "리뷰 + 추천" 광고 패턴 자동화 부재 — UA 매니저가 4언어 × 2사이즈 = 8장 매번 외주, 평가 라벨/플레이시간 일관성 깨지기 쉬움, 한국 규제 태그(확률형 아이템 포함) 누락 위험 |
| **WHO** | UA Manager (사내 마케팅), 잠재적으로 다른 사내 게임 BI 마케터 (게임별 키비주얼+텍스트만 교체하면 재활용) |
| **RISK** | CJK 텍스트 래핑 실패 (R1); 긴 태그 wrap 시 reviews 영역 침범 (R2, 4탭 통일로 위험 감소); zh-TW reviews[3] 누락 (R3); 폰트 폴백 (R4); Batch ZIP 8장 무거움 (R5); 키비주얼 비율 불일치 (R6); Steam 색상 토큰 정확도 (R7) |
| **SUCCESS** | 단건 ≤1초, 배치 8장 ZIP ≤3초; 4언어 평가/플레이시간 라벨 정확; 한국어 4번째 태그 디폴트 자동 채움 (`확률형 아이템 포함`); 1080×1080 reviews[1,2,3] / 1200×628 reviews[0,1,2,3] 정확 렌더; 사용자 첨부 8장 스크린샷과 시각 90%+ 일치; 기존 6템플릿 회귀 0 |
| **SCOPE** | Session 1: data-switch (constants + state init + 자산 추출/임베딩) / Session 2: canvas-renderer (cfg/canvas/banner) / Session 3: single-ui (HTML 패널 + bind + lang switch) / Session 4: batch-ui-zip (배치 UI + ZIP) |

---

## Context

`today-banner-designer.html`(단일 HTML, v1.8 + KVR R28 — 현행 ~8,437라인)는 6개 템플릿(`today-tap`, `app-badge`, `appstore-screenshot`, `sd-showcase`, `keyvisual-review`, `pickup`)을 제공한다. 사용자(Mobile Game UA Manager)가 첨부한 8장의 레퍼런스(영어/한국어/일본어/번체 × 1080×1080·1200×628 — 각 언어로 실제 생성된 Steam-스타일 광고 배너)를 토대로 **Steam 스토어 페이지의 리뷰 카드 + 게임 정보 hero 영역을 결합한 7번째 템플릿**을 추가한다.

기존 KVR은 앱스토어(iOS) 모티브의 단일 mockup floating 패턴이라면, **Steam Review는 Steam 스토어의 "최근 리뷰" + "스토어 페이지 hero" 결합**으로, 게이머의 사회적 증거 + 게임 본질(키비주얼·태그·설명)을 한 화면에 통합한다. 4명의 가상 리뷰어 아이콘 + 슬롯별 고정 플레이시간을 통해 **광고임에도 자연스러운 리뷰 페이지 인상**을 준다.

**스킬 매핑**: 추후 비슷한 요청은 `/plan-plus steam-review-v2` 로 시작. 보조 — `bkit:phase-3-mockup`(레이아웃 검증), `bkit:phase-5-design-system`(언어별 LANG_PACK 일관성).

---

## 사용자 결정 요약 (확정 — 2026-05-10, 4-round AskUserQuestion)

| # | 항목 | 결정 |
|---|------|------|
| 1 | 템플릿 이름 (헤더 드롭다운) | **"Steam Review"** (key: `steam-review`) |
| 2 | 사이즈 | **1080×1080 + 1200×628** 양쪽 지원 (`9x16` 미지원) |
| 3 | 언어 | ko / en / ja / zh-TW (4개 고정 + 기존 LANG_PACK 폰트 자동 스왑 차용) |
| 4 | 리뷰 슬롯 데이터 모델 | **공유 4슬롯**. `1x1`은 reviews[1,2,3] 만 렌더, `1200x628`은 reviews[0,1,2,3] 모두 렌더 |
| 5 | 평가 라벨 + 플레이시간 처리 | **언어별 하드코딩, 편집 불가**. en=Recommended/`X.X hrs on record`, ko=추천/`기록상 X.X시간`, ja=おすすめ/`プレイタイムX.X時間`, zh-TW=推薦/`總時數X.X小時` |
| 6 | 게임 태그 개수 | **모든 언어 4칸 통일** (빈 칸 자동 hide). **한국어 4번째 슬롯 디폴트 = `확률형 아이템 포함`** (한국 규제 대응, "지금 플레이"보다 우선). 5탭 분리 사양은 R-2 좌표 침범 위험 회피 위해 4탭으로 단순화 (사용자 결정, 2026-05-10 Session 1 시작 시점) |
| 7 | 모드 | **Single + Batch 양쪽 지원** (CLAUDE.md 정책 준수, KVR/pickup 패턴 일관) |
| 8 | 디자인 자산 소스 | 사용자 제공 8장 스크린샷 그대로 차용 → 리뷰어 아이콘 4 + 따봉 아이콘 1 추출 → base64 임베딩 |

---

## Confirmed Spec

| 항목 | 결정 |
|---|---|
| 베이스 패턴 | `keyvisual-review` 구조 + `pickup` 의 다중 사이즈 처리 |
| 키비주얼 | 1장만 업로드 → 전 언어 공유. x/y/scale 슬라이더 |
| 슬롯-아이콘 매핑 (고정) | slot 0 = 파란머리 소녀 (56.9 hrs) / slot 1 = 녹색머리 기사 (4.8 hrs) / slot 2 = 분홍머리 소녀 (6.4 hrs) / slot 3 = 코기 (203.4 hrs) |
| 편집 가능 (언어별) | 게임 타이틀, 게임 설명, 태그×5, 리뷰 본문×4 |
| 하드코딩 (편집 불가) | 배경색(#1b2838 Steam 다크 블루 + #16202d 카드), 평가 라벨, 플레이시간 포맷, 슬롯별 시간, 리뷰어 아이콘×4, 따봉 아이콘, 별 아이콘(회색 데코) |
| 별 아이콘 | 회색 fill 비활성 데코로 고정 (노란 채움 미지원, Out of Scope) |
| 부정 평가 카드 | 미지원 (모두 추천 카드. Out of Scope) |
| 리뷰어 ID/이름 | 미표시 (Steam 스크린샷에 없음. KVR과 다른 점) |

---

## Architecture (선택안: Pragmatic Balance)

KVR + pickup 의 검증된 패턴을 그대로 미러링한다. 새 모듈/파일 분리 없이 단일 HTML 파일 정책을 유지한다.

### 파일 변경 대상 (단 1개)
- `repo/today-banner-designer.html` (~8,437 → ~9,290 라인, +853)

### 신규 추가 코드 블록 (~855 라인)

| 블록 | 위치 (insert near) | 분량 |
|---|---|---|
| `STEAM_REVIEW_DEFAULT` 상수 | KVR_HELPERS 직후 (~line 2570) | ~25 |
| `STEAM_REVIEW_ASSETS` (base64 5종) | 같은 위치 | ~10 + base64 페이로드 (~33KB) |
| `STEAM_REVIEW_PLAYTIMES` / `STEAM_REVIEW_LANG_PACK` | 같은 위치 | ~20 |
| `STEAM_REVIEW_CANVAS_SPECS` (사이즈별 좌표) | 같은 위치 | ~30 |
| `buildSteamReviewCfg(stateNode, lang, size, mode='batch')` | KVR cfg 빌더 옆 (~line 5400) — pickup R5 mode 인자 패턴 차용 | ~50 |
| `prepSteamReviewCfgImages(cfg)` | 같은 위치 | ~40 |
| `buildSteamReviewCanvas(cfg)` (사이즈 분기 통합) | 같은 위치 | ~250 |
| `buildSteamReviewBanner(cfg)` | 같은 위치 | ~30 |
| `buildSteamReviewFilename(cfg, prefix, ext)` | 같은 위치 | ~10 |
| `STEAM_REVIEW_HELPERS` (drawTagPill / drawReviewCard / wrapDescription / filterTags / measureTagBlock) | 같은 위치 | ~120 |
| `bindSteamReviewSingleUI()` + `loadSteamReviewSlotToUI(lang)` | KVR bind 옆 (~line 6450) | ~80 |
| `bindSteamReviewBatchUI()` | 배치 bind 영역 (~line 7800) | ~60 |
| Single HTML 컨트롤 패널 `<div data-tmpl="steam-review">` | KVR 패널 직후 (~line 1330) | ~75 |
| Batch HTML 컨트롤 패널 + `renderBatchLangFields` 분기 | pickup 배치 직후 (~line 2100) | ~70 |

### 기존 코드 수정 지점 (~25 라인, 패치 20개)

| # | 위치 | 작업 |
|---|---|---|
| 1 | `#template-selector` dropdown | `<option value="steam-review">Steam Review</option>` 추가 |
| 2 | `TEMPLATE_KEYS` 배열 | `'steam-review'` 추가 |
| 3 | `tmplLabelMap` | `'steam-review': 'Steam Review'` 추가 |
| 4 | `state.single` init | `steam: JSON.parse(JSON.stringify(STEAM_REVIEW_DEFAULT))` |
| 5 | `state.batch` init | 동일 |
| 6 | `renderBanner` dispatch | `'steam-review' → buildSteamReviewBanner(cfg)` 분기 |
| 7 | `buildBannerCanvas` dispatcher | `buildSteamReviewCanvas(cfg)` 분기 |
| 8 | `applyTemplateSwitch` | `9x16` 비활성화 + `loadSteamReviewSlotToUI(state.single.lang)` 호출 (sd-showcase/pickup 패턴) |
| 9 | scattered `data-tmpl-hide` 속성들 | `,steam-review` 추가 |
| 10 | `refreshSinglePreview` | `buildSteamReviewCfg(state.single.steam, lang, size, 'single')` 분기 |
| 11 | `handleSingleDownload` | steam-review 다운로드 분기 (mode='single') |
| 12 | lang change 핸들러 | `loadSteamReviewSlotToUI(lang)` 호출 |
| 13 | `bindSingleMode` 끝 | `bindSteamReviewSingleUI()` 호출 |
| 14 | `bindBatchMode` 끝 | `bindSteamReviewBatchUI()` 호출 |
| 15 | `syncBatchStateFromUI` | per-lang 필드 + 공통 keyvisual sync 로직 |
| 16 | `renderBatchLangFields` | `isSteam` 분기 (4언어 × {title, description, tags×5, reviews×4} 입력) |
| 17 | `copyLangFieldsToOthers` | steam-review 복사 로직 |
| 18 | `buildBatchCfgs` | `(size, lang)` 팬아웃 (mode='batch' default) |
| 19 | `downloadBatchItem` | steam-review canvas 분기 |
| 20 | `handleBatchExportZip` | keyvisual 1회 디코드 + 8장 캔버스 루프 (KVR R5 패턴) |

---

## Canvas Layout (사이즈별 좌표·드로잉 순서)

### 공통 사전처리
1. 배경 채우기 (`#1b2838` Steam 다크 블루)
2. 키비주얼: `kvBox` 영역에 `cover` 핏 + 사용자 scale/X/Y 변환 + 4px 라운드 클리핑

### `1x1` (1080×1080) — slots [1, 2, 3] 렌더
- `heroBox`: x=20, y=20, w=1040, h=340
  - `kvBox`: 40,40 / 520×300 (2:1 비율)
  - 타이틀: 580,60 / w=480 / 42pt 흰색
  - 설명: 580,120 / w=480 / 18pt `#c6d4df` / 3-line clamp
  - 태그: 580,240+ / wrap-flow / pill (radius 3px, `rgba(102,159,209,0.18)` 배경, `#a3cfe3` 텍스트, 14pt)
- `reviewsArea`: 20,380 / w=1040 / h≈680
  - 카드 3장 세로 스택, gap=14 → 각 카드 ~217px
  - 카드 = `#16202d` BG + 아이콘(84×84 라운드) + 따봉(26×26) + 평가라벨(굵게 22pt) + 본문(2-line clamp 18pt) + 시간(meta 14pt)

### `1200x628` — slots [0, 1, 2, 3] 렌더
- `heroBox` 좌측: 20,20 / 560×588
  - `kvBox`: 40,40 / 540×270
  - 타이틀: 40,330 / w=520 / 34pt 흰색
  - 설명: 40,380 / w=520 / 16pt
  - 태그: 40,480 / wrap-flow / 13pt
- `reviewsArea` 우측: 600,20 / 580×588
  - 카드 4장 세로 스택, gap=8 → 각 카드 ~141px
  - 카드 폰트는 1x1 보다 작음 (titleFs=16, bodyFs=18, metaFs=12)

**슬롯-아이콘 고정 매핑:**
- slot 0 = 파란머리 소녀, 56.9 hrs (1200×628 첫 카드, 1x1 미사용)
- slot 1 = 녹색머리 기사, 4.8 hrs
- slot 2 = 분홍머리 소녀, 6.4 hrs
- slot 3 = 코기, 203.4 hrs

---

## Functional Requirements (FR)

| ID | 내용 |
|---|---|
| FR-01 | 헤더 드롭다운에 "Steam Review" 옵션 추가, 선택 시 단건/배치 컨트롤 패널이 자동 전환 |
| FR-02 | 사이즈 셀렉터에서 `1x1` (1080×1080) / `1200x628` 선택 가능, `9x16` 자동 비활성화 |
| FR-03 | 언어 셀렉터에서 ko/en/ja/zh-TW 4개 선택 가능, 폰트 자동 스왑 |
| FR-04 | 키비주얼 1장 업로드 (전 언어 공유), scale 50–600% / X ±1500 / Y ±1500 슬라이더 |
| FR-05 | 게임 타이틀 입력 (언어별, 단일 input) |
| FR-06 | 게임 설명 입력 (언어별, textarea, 3-line clamp) |
| FR-07 | 게임 태그 4칸 입력 (언어별, 빈 칸 자동 hide). 모든 언어 동일 4칸 |
| FR-08 | 한국어 디폴트 4번째 태그 = `확률형 아이템 포함` 자동 pre-fill (한국 규제 대응) |
| FR-09 | 리뷰 본문 4칸 입력 (언어별, textarea, 2-line clamp) |
| FR-10 | 평가 라벨 자동 출력 (en=Recommended, ko=추천, ja=おすすめ, zh-TW=推薦) — 편집 불가 |
| FR-11 | 플레이시간 포맷 자동 출력 (언어별 + 슬롯별 56.9/4.8/6.4/203.4) — 편집 불가 |
| FR-12 | 사이즈별 리뷰 슬롯 표시: `1x1` = reviews[1,2,3] / `1200x628` = reviews[0,1,2,3] |
| FR-13 | 리뷰어 아이콘 4종 + 따봉 아이콘 base64 임베딩, 캔버스에 PNG 그리기 |
| FR-14 | 별 아이콘 회색 데코 (`#5c7080` fill, 비활성 무드) — 모든 카드 동일 |
| FR-15 | Single 모드 PNG 다운로드 (`{prefix}_steam_{lang}_{size}.png`) |
| FR-16 | Batch 모드 8장 ZIP (4 lang × 2 size, 키비주얼 1회 디코드 공유) |
| FR-17 | 언어 전환 시 입력 필드 자동 복원 (다른 템플릿 패턴 일관) |
| FR-18 | `buildSteamReviewCfg`에 `mode` 파라미터 (`'single'` / `'batch'`) — pickup R5 패턴 (단건/배치 perSize 분리 회피) |

---

## Non-Functional Requirements (NFR)

| ID | 내용 |
|---|---|
| NFR-01 | 단일 HTML 정책 유지 (외부 파일 의존성 추가 0개) |
| NFR-02 | 단건 export ≤1초 (KVR 단건 1초 이내 기준) |
| NFR-03 | 배치 ZIP 8장 ≤3초 (KVR 4장 1.5초 × 2 사이즈 + 키비주얼 1회 디코드 공유) |
| NFR-04 | base64 자산 추가 ~33KB (HTML 변경량 +35KB 이내) |
| NFR-05 | 기존 6템플릿 회귀 0 (steam-review 분기 외 무수정) |
| NFR-06 | `node --check` 인라인 JS 문법 검증 통과 |

---

## Success Criteria (SC)

| ID | 내용 | 측정 |
|---|---|---|
| SC-01 | `template-selector` 드롭다운에 "Steam Review" 노출 + 선택 시 컨트롤 패널 자동 전환 | DOM 검사 |
| SC-02 | 4언어 텍스트 슬롯 저장·복원 정확 | 언어 전환 5회 reload, diff 0 |
| SC-03 | 키비주얼 1장 → 4언어 동일 적용, scale/x/y 슬라이더 즉시 미리보기 반영 | 슬라이더 조작 + 4언어 출력 비교 |
| SC-04 | 사이즈별 리뷰 슬롯 정확: `1x1` reviews[1,2,3] / `1200x628` reviews[0,1,2,3] | 단건 export 2장 비교 |
| SC-05 | 평가 라벨 + 플레이시간 언어별 하드코딩 정확, 편집 불가 | 4언어 출력 검증 + 입력 필드 부재 확인 |
| SC-06 | 한국어 4번째 태그 디폴트 자동 pre-fill (`확률형 아이템 포함`) | 새 페이지 로드 → 한국어 선택 → 태그 input 4번째 = `확률형 아이템 포함` 확인 |
| SC-07 | Single PNG 다운로드 + Batch 8장 ZIP 정상 동작 | 실제 다운로드 + 파일 검증 |
| SC-08 | 사용자 첨부 8장 스크린샷과 시각 90%+ 일치 (색상, 폰트 크기, 카드 레이아웃) | 사용자 시각 비교 |
| SC-09 | 기존 6템플릿 회귀 0 | 6템플릿 단건/배치 export 정상 |

---

## Risks (R)

| ID | 리스크 | 대응 |
|---|---|---|
| R-1 | CJK 텍스트 래핑 실패 | 기존 `wrapTextToNLines` 재사용. ja/zh-TW = 글자 단위, en/ko = 단어 단위 |
| R-2 | 긴 태그 wrap 시 1x1 reviews 영역 침범 가능 (4탭 통일로 위험 감소) | 태그 블록 `measureTagBlock`로 사전 측정 → `reviewsArea.y` 동적 계산 안전장치 유지 (하드코딩 금지) |
| R-3 | zh-TW reviews[3] 사용자 미입력 시 1200×628에서 빈 카드 | 빈 본문이라도 카드 프레임 + 아이콘 + 평가라벨 + 플레이시간까지 렌더 (Steam UI 일관성) |
| R-4 | 폰트 폴백 (Pretendard/Noto Sans JP/Noto Sans TC) | `getFontFamilyForLang` 그대로. 한국어 pill 14pt에서 줄바꿈 검증 필수 |
| R-5 | Batch ZIP 8장 / 게임 무거움 | 키비주얼 + 5 자산 1회 디코드 후 size×lang 8조합 캔버스 루프 (KVR R5 패턴) |
| R-6 | 키비주얼 비율 불일치 (1:1, 16:9 등 다양) | scale 50–600% 폭넓게 허용 + X/Y ±1500 (KVR R6 와 동일) |
| R-7 | Steam 색상 토큰 정확도 (스크린샷 픽셀 ↔ 코드 hex) | 스크린샷에서 Preview 픽셀-피킹 1회 → `STEAM_REVIEW_CANVAS_SPECS` 에 락인 |

---

## Reused Existing Functions (재사용 우선)

새로 만들지 말고 기존 헬퍼를 재사용한다:

| 헬퍼 | 위치 (대략) | 용도 |
|---|---|---|
| `setupDropzone(zoneId, onFile)` | line ~6059 | 키비주얼 업로드 |
| `bindKvrSlider(elId, labelId, prop, suffix)` 패턴 | line ~6362 | scale/x/y 슬라이더 (steam 버전 복제) |
| `loadCachedImage(url)` | (KVR이 사용) | 이미지 캐시 디코드 |
| `fileToDataURL(file)` | (setupDropzone 내부) | 파일→base64 |
| `getFontFamilyForLang(lang)` | (KVR canvas 사용) | CJK 폰트 폴백 |
| `wrapTextToNLines` | line ~4516 | 텍스트 래핑 |
| `_imgCache` 패턴 | (handleBatchExportZip 내부) | batch ZIP 생성 시 키비주얼 1회 디코드 공유 |
| `updateStateImage(stateObj, prop, dataURL)` | (M-2 도입) | dataURL 교체 시 캐시 무효화 |

---

## Asset Acquisition (구현 전 사전작업)

5개 PNG 아이콘을 사용자 제공 8장 스크린샷에서 추출 → 압축 → base64 임베딩.

| 자산 | 추출 소스 | 크롭 가이드 |
|---|---|---|
| Reviewer slot 0 (파란머리 소녀) | 1200×628 (어떤 언어든) — 우측 첫 카드 | 정사각 ~64×64, 128×128로 export |
| Reviewer slot 1 (녹색머리 기사) | 1080×1080 EN — 첫 카드 | 84×84 → 168×168 |
| Reviewer slot 2 (분홍머리 소녀) | 1080×1080 EN — 두번째 카드 | 동일 |
| Reviewer slot 3 (코기) | 1080×1080 EN — 세번째 카드 | 동일 |
| Thumbs-up (블루 따봉) | 1200×628 어떤 카드든 | 26×26 → 64×64 |

**워크플로:** Preview/Figma 크롭 → tinypng 80% 압축 → `base64 -i icon.png` → `STEAM_REVIEW_ASSETS` 에 paste. 합산 ~33KB base64 (KVR mockup 117KB 대비 작음).

---

## Implementation Sequencing (4 sessions)

`pickup` 의 4-session 분할을 미러링:

1. **Session 1 — data-switch** (~220 라인): 상수 4종, 레지스트리, state init, 자산 추출 + base64 임베딩
2. **Session 2 — canvas-renderer** (~380 라인): cfg/prep/canvas/banner/filename + dispatch
3. **Session 3 — single-ui** (~155 라인): HTML 패널 + bind + loadSlotToUI + handleSingleDownload 분기
4. **Session 4 — batch-ui-zip** (~125 라인): batch HTML + renderBatchLangFields + sync + buildBatchCfgs + ZIP 분기

각 세션 종료 시 `node --check` 로 인라인 `<script>` 문법 검증.

---

## Verification (구현 완료 후 검증)

1. **문법 검증**: `node --check` 로 인라인 JS 검증
2. **기능 검증**: `repo/today-banner-designer.html` 을 브라우저로 열어 다음 시나리오 수동 테스트
   - Steam Review 선택 → 키비주얼 업로드 → 4개 언어 텍스트 입력 → `1x1` 다운로드
   - 사이즈 `1200x628` 으로 토글 → reviews[0] 슬롯이 새로 등장하는지 확인
   - 한국어 선택 → 5번째 태그가 디폴트로 차있는지 확인
   - Batch 탭 → 4-language 패널에 텍스트 채움 → ZIP 익스포트 (8장)
   - 한국어 5탭이 1x1 에서 줄바꿈해도 리뷰 영역과 겹치지 않는지 확인 (R-2 검증)
3. **시각 비교**: 사용자 제공 8장 스크린샷과 출력 PNG 를 나란히 놓고 색상·여백·폰트 크기 차이 1차 점검
4. **PDCA Check 단계**: `/pdca analyze steam-review` 로 gap-detector 자동 검증 (목표 matchRate ≥ 90%)

---

## Out of Scope (v1.9에서 제외)

- 진정한 CSV-bulk batch (10개 게임 × 4lang × 2size = 80장 자동) — 현재는 4-language 패널 방식만. 향후 v2 후보
- `9x16` (1080×1920) 사이즈 지원
- 부정 평가(Not Recommended) 카드
- 별 아이콘 활성화(노란색 채우기) — 현재는 회색 데코로 고정
- 리뷰어 ID/이름 표시 (KVR 과 달리 Steam 스크린샷에 없음)
- 사용자 정의 리뷰어 아이콘 업로드
- 평가 라벨/플레이시간 사용자 편집

---

## Critical Files

- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/today-banner-designer.html` — 유일한 수정 대상
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/CLAUDE.md` — PDCA phase 진행 시 "현황" 섹션 갱신
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/docs/01-plan/features/steam-review.plan.md` — 본 plan
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/docs/02-design/features/steam-review.design.md` — 다음 phase
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/assets/steam-review/` (선택) — 추출한 PNG 원본 보관 (base64 임베딩 후에도 원본 유지 권장)
