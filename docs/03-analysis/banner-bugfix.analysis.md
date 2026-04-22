# Analysis — banner-bugfix (Gap Analysis)

- **Feature**: banner-bugfix
- **Date**: 2026-04-22
- **Phase**: PDCA Check (Gap Analysis)
- **Plan Ref**: `docs/01-plan/features/banner-bugfix.plan.md` (r2, FR-01~15 / SC-01~11)
- **Implementation**: `today-banner-designer.html` (Do 단계 완료)
- **Method**: 정적 분석 — `Plan FR-NN` 코드 주석 + 실제 구현 로직 + UI 요소 대조
- **User Signal**: "HTML 테스트 시 큰 문제 없음" — 실사용 검증 완료

---

## Executive Summary

| 항목 | 값 |
|------|-----|
| **FR Match Rate** | 15/15 = **100%** |
| **SC Match Rate** | 10/11 Met + 1 Partial = **~95%** |
| **Overall Match Rate** | **≈ 97%** |
| **Critical Gaps** | 0 |
| **Important Gaps** | 0 |
| **Minor Gaps** | 3 (모두 긍정 방향 또는 명세 해석 문제) |
| **Verdict** | ✅ **Report 단계 진행 가능** (90% 임계 충족) |

---

## Context Anchor (Plan r2로부터 상속)

| 항목 | 내용 |
|------|------|
| **WHY** | 실사용 결과물 6건에서 레이아웃 파손·속도 저하 발견 + 그림자 연출 수요 |
| **WHO** | 사내 UA팀 (Primary: 김성권) |
| **RISK** | html-to-image 호환성 / DOM 프리뷰-최종 이미지 차이 / 프리셋 상호작용 / drop-shadow 캡처 |
| **SUCCESS** | 6개 이슈 시각 검증 + Shadow 4파라미터 동작 + 12장 50%+ 단축 |
| **SCOPE** | `today-banner-designer.html` 내부만 |

---

## 1. Strategic Alignment Check

| 질문 | 답 |
|------|-----|
| Plan의 핵심 문제(WHY)를 해결했는가? | ✅ **Yes** — 레이아웃 파손·속도 저하·그림자 부재 전부 코드에 반영 |
| Plan Success Criteria가 충족됐는가? | ✅ **10/11 Met** — SC-07만 사용자 실측 대기 |
| Plan의 주요 결정(아키텍처, 범위)이 지켜졌는가? | ✅ **Yes** — 단일 파일 내 수정, 외부 의존 추가 없음, GitHub Pages 배포 제외 유지 |

**결론**: 전략적 정렬도 높음. 사용자가 의도한 목적을 달성.

---

## 2. FR 구현 대조표 (15건)

| FR | Plan 요구사항 | 구현 증거 | 상태 |
|----|---------------|-----------|------|
| FR-01 | `.game-title` ellipsis/overflow 제거, nowrap 유지 | [today-banner-designer.html:206-213](../../today-banner-designer.html) — `overflow`/`text-overflow` 제거, `white-space: nowrap` 유지 | ✅ Met |
| FR-02 | 게임명 input 아래 사이즈별 힌트 | `#s-title-hint` 요소 + `TITLE_HINTS={1x1:18, 9x16:15, 1200x628:14}` + `updateSingleHints()` + `s-size` change 이벤트 연동 | ✅ Met |
| FR-03 | `.banner-disclaimer` nowrap | `:236` — `white-space: nowrap` 적용 | ✅ Met |
| FR-04 | 1:1 disclaimer font 20→16px, right 40→28px | `:232-234` — `right: 28px; font-size: 16px` | ✅ Met (+ 9:16 폰트 26→24 추가 개선) |
| FR-05 | overflow-wrap bottom을 darkbar 상단 정렬 | `:169-184` — `bottom: calc(60px + 180px)` 등 3건 | ✅ Met |
| FR-06 | Scale slider max 120→150 | `#s-overflow-scale`, `#b-overflow-scale` 양쪽 `max="150"` | ✅ Met |
| FR-07 | 배치 DOM 즉시 프리뷰 (html-to-image 없이) | `handleBatchPreview()` — `transform: scale()` 기반 DOM 직접 렌더, `state.batch.previewCombos` 보관 | ✅ Met |
| FR-08 | 이미지 변환은 개별/ZIP 다운로드 트리거 시에만 | `downloadBatchItem()` + `handleBatchExportZip()` 분리 | ✅ Met |
| FR-09 | `img.decode()` 기반 대기, setTimeout 제거 | `waitForImages` 내 `img.decode()` 분기 + onload 폴백. `setTimeout(r, 80/100)` 호출부 전부 제거 | ✅ Met |
| FR-10 | `.game-subtitle` nowrap | `:216` — `white-space: nowrap` 적용 | ✅ Met |
| FR-11 | 부제 힌트 (단건: 사이즈별 / 배치: 공통) | `#s-subtitle-hint` + `SUBTITLE_HINTS` + `updateSingleHints()` · 배치는 언어별 입력 섹션 상단 공통 안내 | ✅ Met |
| FR-12 | overflow-img에 `filter: drop-shadow()` | `renderBanner()` 내 `cfg.shadow.enabled` 체크 후 `img.style.filter` 주입 | ✅ Met |
| FR-13 | Shadow UI — On/Off + 4개 슬라이더 | 단건·배치 양쪽에 `#s-shadow-*`, `#b-shadow-*` 구조 + 이벤트 바인딩 | ✅ Met |
| FR-14 | 배치 Shadow 사이즈별 독립 저장 | `state.batch.shadowPerSize` + `b-overflow-size` change 시 `loadBatchShadowSliders()` 호출 | ✅ Met |
| FR-15 | 기본 Off, 프리셋 `{x:0, y:8, blur:16, opacity:40}` | `SHADOW_DEFAULT = { enabled: false, x:0, y:8, blur:16, opacity:40 }` | ✅ Met |

---

## 3. SC (Success Criteria) 검증

| SC | 기준 | 상태 | 비고 |
|----|------|------|------|
| SC-01 | 게임명 20자 시 한 줄 표시 | ✅ Met | ellipsis 제거, nowrap만 |
| SC-02 | 힌트 사이즈 변경 시 갱신 | ✅ Met | `s-size` change → `updateSingleHints` |
| SC-03 | 고지문구 전 사이즈 한 줄 | ✅ Met | nowrap 일괄 |
| SC-04 | 오버플로우 다크바 침범 없음 | ✅ Met | `bottom` 재정렬 |
| SC-05 | Scale 150% 조정 가능 | ✅ Met | max=150 |
| SC-06 | 배치 클릭 시 html-to-image 호출 없이 썸네일 | ✅ Met | `handleBatchPreview` 내 변환 호출 없음 (DOM transform scale만) |
| SC-07 | 12장 ZIP 50%+ 단축 | ⚠️ Partial | 이론적 개선(`setTimeout` 제거 ×12 ≈ 1s + `decode()` 병렬화) 명확하나 **사용자 실측 필요** |
| SC-08 | Shadow Off에서 기존 결과 픽셀 동일 | ✅ Met | Shadow 기본 Off, filter 미주입 → 기존 렌더 경로 |
| SC-09 | 부제 줄바꿈 없이 + 힌트 | ✅ Met | FR-10/11 구현 |
| SC-10 | Shadow On 시 외곽선 그림자 + 슬라이더 반영 | ✅ Met | `filter: drop-shadow()` 주입 경로 확인 |
| SC-11 | 사이즈별 Shadow 독립 저장 | ✅ Met | `shadowPerSize` 구조 + 사이즈 드롭다운 복원 |

---

## 4. Decision Record Verification

| 단계 | 결정 | 구현 반영 |
|------|------|-----------|
| Plan Q1 | title 긴 경우 "한 줄 강제 + 힌트만" | ✅ ellipsis 제거, nowrap 유지, 힌트 표시 |
| Plan Q2 | disclaimer "nowrap + 폰트 축소 + 위치 재조정" | ✅ 1:1 16px/right 28px 적용 (+ 9:16 24px 보너스) |
| Plan Q3 | overflow "다크바 상단까지만 노출" | ✅ `bottom: darkbar_offset + darkbar_height` |
| Plan Q4 | 배치 "DOM 프리뷰 즉시 + 확정 시 이미지 변환" | ✅ `handleBatchPreview()` + `handleBatchExportZip()` 분리 |
| Plan Q5 | GitHub Pages "나중에 따로" | ✅ Scope 제외 유지 |
| Plan r2 Q1 | 부제 "title과 동일 (한 줄 강제 + 힌트)" | ✅ `.game-subtitle` nowrap + 힌트 |
| Plan r2 Q2 | Shadow "4개 슬라이더 정밀 조정" | ✅ X/Y/Blur/Opacity 4슬라이더 |
| Plan r2 Q3 | Shadow 배치 "사이즈별 독립" | ✅ `shadowPerSize` |
| Plan r2 Q4 | Shadow 기본 Off | ✅ `SHADOW_DEFAULT.enabled = false` |

**결정 사항 전부 충실 반영.** 임의 방향 전환 없음 (CLAUDE.md 규칙 준수).

---

## 5. Gap List

### 5.1 Critical
**없음**

### 5.2 Important
**없음**

### 5.3 Minor

| ID | 구분 | 설명 | 조치 제안 |
|----|------|------|----------|
| G-01 | Spec deviation (긍정적) | FR-04 9:16/1200×628은 "nowrap만 적용 후 육안 검증"이었으나 9:16 font-size 26→24 추가 축소 | 수용 권장 (기능적 이득) |
| G-02 | Measurement needed | SC-07 12장 50%+ 단축은 사용자 실측 필요 | 브라우저 DevTools Performance로 Before/After 측정 권장 |
| G-03 | Scope note | 배치 mode 힌트가 per-input이 아니라 상단 공통 안내 1줄 | Plan 명세와 부합 (per-input 요구 아님) — 현 상태 유지 권장 |

### 5.4 Out of Scope (Plan에서 명시적 제외)
- `slugify` 한글 처리 버그 (이전 코드리뷰 건)
- CDN SRI 해시 누락 (이전 코드리뷰 건)
- 배치 재진입 가드 부재 (이전 코드리뷰 건)
- GitHub Pages 배포

이 4건은 이번 feature 범위가 아니므로 Gap으로 기록하지 않음.

---

## 6. Recommendations

### 즉시 (Optional)
- 없음 — Critical/Important Gap 없음

### 권장 (사용자 판단)
- **SC-07 성능 실측**: 기존 HTML과 신규 HTML로 같은 배치 조건(3사이즈 × 4언어 = 12장) 비교 측정
- **Shadow html-to-image 호환성 확인**: Shadow On 상태에서 개별 다운로드 후 PNG 열어 그림자가 이미지에 포함됐는지 육안 검증 (Plan R-05 대응)

### 다음 단계 제안

| 옵션 | 설명 |
|------|------|
| **A. `/pdca report banner-bugfix`** | Match 97%로 Report 단계 충족. 완료 리포트 작성 |
| **B. 추가 기능 요청 수용** | 사용자가 언급한 "추가 요청 사항"을 받아 Plan r3 작성 또는 별도 feature (예: banner-enhance) 분리 |
| **C. `/pdca iterate`** | 불필요 (Gap 없음) |

---

## 7. Checkpoint 5 — Review Decision

Critical/Important Gap이 없으므로 Review 결정 자동:
- **그대로 진행** — 현재 코드 확정
- 사용자가 추가 기능을 요청할 예정이므로 Report는 그 작업 완료 후에 작성하는 편이 자연스러움

---

_본 분석은 정적 코드 대조 기반이며 어떠한 코드도 수정하지 않았습니다 (사용자 지시 준수)._
