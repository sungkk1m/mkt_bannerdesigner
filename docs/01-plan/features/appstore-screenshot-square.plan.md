# PDCA Plan — App Store Screenshot 1080×1080 (Square) 변형

**Feature**: `appstore-screenshot-square`
**Created**: 2026-07-22
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/pdca plan` (AskUserQuestion 3-round — 레이아웃 시각 비교 포함)
**References**:
- `docs/01-plan/features/appstore-screenshot.plan.md` (베이스 템플릿 v1.5)
- Google Play Screenshot v1.11 (2사이즈 지원 선례 — `gpSizes` 필터 패턴)
- ko-disclaimer-policy O-2 B (KO 고지문구 세로형 위치 결정 — 유지)

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | App Store Screenshot 정사각(1080×1080) 사이즈 추가 |
| 시작 | 2026-07-22 |
| 본체 파일 | `today-banner-designer.html` (단일 HTML, 현행 ~12,185 라인 → 추정 +200~250) |
| 사이즈 | 기존 9:16 (1080×1920) 유지 + **1:1 (1080×1080) 신규** |
| 언어 | ko / en / ja / zh-TW (4개 고정, 기존 AS_LANG_PACK 그대로) |
| FR | 9건 |
| NFR | 4건 |
| SC | 8건 |
| R | 5건 |
| 결정사항 | 5건 (AskUserQuestion 3-round) |
| Implementation | 1~2 sessions |

### Value Delivered (4관점)

| 관점 | 내용 |
|---|---|
| **Problem** | App Store Screenshot 템플릿이 9:16(1080×1920) 전용이라 Meta 등 정사각(1:1) 지면에 쓸 소재를 별도 제작해야 함. 세로형의 설명 본문 영역은 정사각에서는 공간상 불가능 |
| **Solution** | 동일 템플릿에 1080×1080 사이즈 추가. 설명 본문·디바이스 라벨·탭바를 제거하고 상태바→헤더→앱정보→스탯 4컬럼→키아트(하단 크롭)로 구성. KO 고지문구는 "앱 내 구입" 우측에 인라인 표기 |
| **Function/UX Effect** | 사이즈 셀렉터에서 9:16/1:1 선택 → 기존 입력값 그대로 재사용(설명 본문만 1:1에서 미사용). 배치 ZIP = 선택 사이즈 × 4언어 (최대 8장) |
| **Core Value** | 정사각 지면용 스토어 모방 소재를 추가 입력 없이 즉시 산출 — 세로형과 소재·텍스트 단일 관리 |

---

## Context Anchor

> Auto-generated from Executive Summary. Propagated to Design/Do documents for context continuity.

| Key | Value |
|-----|-------|
| **WHY** | 정사각(1:1) 광고 지면용 App Store 모방 소재가 없어 세로형만으로 UA 운영 — 1080×1080 수요를 수작업으로 커버 중 |
| **WHO** | UA Manager (사내 마케팅) — 기존 appstore-screenshot 사용자 그대로 |
| **RISK** | DOM/Canvas 이중 렌더 불일치(R-1); KO 고지문구 폭 초과(R-2); hide-stats 토글과 1:1 y-플로우 상호작용(R-3); 배치 사이즈 중복 생성(R-4); 키아트 상하 크롭으로 핵심 비주얼 잘림(R-5) |
| **SUCCESS** | 1:1 단건/배치 정상 export; KO 1:1 고지문구 "앱 내 구입 · 확률형 아이템 포함" 한 줄; 9:16 출력 기존과 픽셀 동일(회귀 0); DOM 프리뷰 = Canvas export 일치 |
| **SCOPE** | Session 1: CSS + DOM/Canvas 1:1 분기 + KO 고지문구 / Session 2: 사이즈 셀렉터 + 배치 + 검증 |

---

## 검토 경위 (구현 가능성 분석 — 2026-07-22)

**초기 요청**: "설명 본문을 제거한 형태로 1080×1080 생성이 가능한지" → **가능하나 설명 본문 제거만으로는 부족**함을 수치로 확인:

| 캔버스 | 상단 스택 (상태바80+헤더78+앱정보278+스탯152) | 키아트 16:9 (패딩 28 포함) | 합계 | 판정 |
|---|---|---|---|---|
| 1080×1080 | 588 | 551+28 = 579 | 1,167 | **87px 초과** |
| 1200×1200 (검토) | 588 | 619+28 = 647 | 1,235 | **35px 초과** — 캔버스 확대는 키아트 폭도 키우므로 해결 안 됨 (자기유사) |
| 1280×1280 (참고) | 588 | 664+28 | 1,280 | 딱 맞으나 UI 절대크기가 상대적으로 작아져 픽셀 퍼펙트 원칙 위배 |

→ 정사각인 이상 하단 요소 취사선택 필수. 사용자에게 A안(스탯 유지+키아트 크롭)/B안(스탯 제거+16:9 무크롭) 시각 비교 제시 후 **A안 확정**.

---

## 사용자 결정 요약 (확정 — 2026-07-22, AskUserQuestion 3-round)

| # | 항목 | 결정 |
|---|------|------|
| 1 | 1:1 하단 구성 | **A안: 스탯 4컬럼 유지 + 키아트 하단 크롭** (≈2.1~2.2:1 표시, 중앙 cover 크롭). 설명 본문·디바이스 라벨·탭바 제거 |
| 2 | KO 고지문구 적용 범위 | **1:1 신규만** IAP 우측 표기. 세로형 9:16은 현행 유지 (description 본문 끝 — ko-disclaimer-policy O-2 B 결정 불변) |
| 3 | 고지문구 표기 형식 | **`앱 내 구입 · 확률형 아이템 포함`** (가운데점 구분, 22px, 보조 텍스트 색상 — 기존 IAP 라벨과 동일 스타일) |
| 4 | 배치 export 조합 | **사이즈 체크박스** (9:16 / 1:1) × 4언어 × 1테마 — Google Play 템플릿 패턴. 둘 다 선택 시 8장, 하나만 선택 시 4장 |
| 5 | 정사각 사이즈 | **1080×1080만** (1200×1200 미지원 — 위 검토 경위 참조. 필요 시 추후 ×1.111 스케일 렌더로 확장 가능) |

---

## Confirmed Spec — 1:1 레이아웃 (Canvas 절대좌표 기준)

9:16과 **동일 좌표·동일 크기**로 상단을 유지하고, 하단만 다르다 (픽셀 퍼펙트 원칙 유지):

| 섹션 | Y 범위 | 9:16 대비 |
|---|---|---|
| [1] 상태바 | 0–80 | 동일 |
| [2] 헤더 (‹ 검색) | 80–158 | 동일 |
| [3] 앱 정보 (아이콘 242 + 타이틀/CTA행) | 158–436 | 동일. **KO만 IAP 라벨 = `앱 내 구입 · 확률형 아이템 포함`** |
| [4] 스탯 4컬럼 | 440–588 | 동일 |
| [5] 키아트 | 616 (588+28) – 하단 | **높이 ~440–464px로 상하 중앙 크롭** (16:9 원본의 세로 80~84% 표시). 하단 여백 0~24px는 Design 단계 확정 |
| [6] 디바이스 라벨 | — | **제거** |
| [7] 설명 본문 + more | — | **제거** |
| [7.1] KO 고지문구 (description 끝) | — | **제거** (IAP 우측으로 대체) |
| [8] 탭바 | — | **제거** |

**KO 고지문구 상세**:
- 1:1 + `lang==='ko'` 조건에서만: IAP 라벨 텍스트를 `pack.iap + ' · ' + (LANG_PACK.ko.disclaimer 선행 `*` 제거)` 로 합성
- DOM `.as-iap-label`의 `max-width: 260px` 제약은 1:1 KO에서 해제 필요 (가용 폭 ~520px, 예상 문자열 폭 ~350px — 한 줄 수용 확인)
- en/ja/zh-TW는 기존 IAP 문구만 (koDisclaimer 없음 — 기존 정책 동일)
- 9:16은 코드 경로 무수정 (회귀 0 원칙)

---

## Functional Requirements (FR)

| ID | 내용 |
|---|---|
| FR-01 | `s-size` 셀렉터: appstore-screenshot 선택 시 9x16 + 1x1 두 옵션 활성 (기존: 9x16 고정 `disabled` → 해제, `applyTemplateSwitch` 분기 수정) |
| FR-02 | CSS `.banner.tmpl-appstore-screenshot.size-1x1` (1080×1080) 추가 + 1:1 전용 섹션 숨김 (description / ko-disclaimer / device / tabbar) |
| FR-03 | `buildAppStoreScreenshotBanner(cfg)` size 분기 — 1x1: 제거 섹션 미출력, 키아트 높이 고정 + `object-fit: cover` 상하 크롭 |
| FR-04 | `buildAppStoreScreenshotCanvas(cfg)` size 분기 — H=1080, 섹션 [6][7][7.1][8] 스킵, 키아트 `drawImageCover` 크롭 (기존 헬퍼 재사용) |
| FR-05 | KO 1:1 고지문구: IAP 라벨 `앱 내 구입 · 확률형 아이템 포함` (DOM + Canvas 동일 로직, 9:16 무변경) |
| FR-06 | 배치 사이즈 체크박스: appstore 선택 시 9x16 + 1x1 활성 (GP `bSizeBoxes` 패턴), `buildBatchCfgs` AS 분기의 `size: '9x16'` 고정 제거 → `combo.size` 사용 + GP식 사이즈 필터(9x16/1x1 외 제외, 중복 방지) |
| FR-07 | 파일명: 기존 규칙 `{prefix}_{size}_{lang}.png` 그대로 (`cfg.size`가 1x1이면 자동 반영 — 신규 코드 불필요, 검증만) |
| FR-08 | 단건 UI: 1x1 선택 시 설명 본문 textarea(`s-as-description`) 숨김 (9:16 복귀 시 복원, 입력값은 보존). 배치 UI의 description 필드는 유지 (9:16 겸용) |
| FR-09 | 기존 토글(스탯/탭바/CTA/IAP) 동작 유지 — 1x1에서 탭바 토글은 무의미(항상 미표시)하므로 비활성 또는 무시. hide-stats 시 Canvas y-플로우로 키아트 영역이 늘어나는 동작은 허용 (16:9 무크롭에 근접 — B안 유사 효과) |

---

## Non-Functional Requirements (NFR)

| ID | 내용 |
|---|---|
| NFR-01 | 단일 HTML 정책 유지 (외부 파일·자산 추가 0) |
| NFR-02 | 기존 9템플릿 + appstore 9:16 회귀 0 — 9:16 코드 경로는 분기 추가 외 무수정 |
| NFR-03 | 단건 ≤1초 / 배치 8장 ZIP ≤3초 (기존 기준 유지) |
| NFR-04 | `node --check` 인라인 JS 문법 검증 통과 |

---

## Success Criteria (SC)

| ID | 내용 | 측정 |
|---|---|---|
| SC-01 | s-size에서 1x1 선택 가능, 프리뷰 1080×1080 렌더 | DOM 검사 |
| SC-02 | 1:1에 설명 본문·디바이스 라벨·탭바·(구)KO 고지문구 미표시, 상태바~스탯은 9:16과 동일 좌표 | 프리뷰 + export 비교 |
| SC-03 | KO 1:1 IAP 라벨 = `앱 내 구입 · 확률형 아이템 포함` 한 줄 (줄바꿈·잘림 없음) | 4언어 export 검증 |
| SC-04 | en/ja/zh-TW 1:1은 기존 IAP 문구만 표시 | 동상 |
| SC-05 | KO 9:16 고지문구 기존 위치(description 끝) 그대로 — 회귀 0 | 9:16 export 비교 |
| SC-06 | 키아트 중앙 cover 크롭 (좌우 무손실, 상하 대칭 크롭) | 기준 이미지로 픽셀 확인 |
| SC-07 | 배치: 9x16+1x1 체크 → 8장 ZIP, 1x1만 → 4장, 파일명에 사이즈 정확 반영 | 실제 ZIP 검증 |
| SC-08 | DOM 프리뷰 vs Canvas export 시각 일치 + 기존 템플릿 회귀 0 | 브라우저 실측 (install-plz 방식) |

---

## Risks (R)

| ID | 리스크 | 대응 |
|---|---|---|
| R-1 | DOM/Canvas 이중 렌더 불일치 (1:1 분기가 한쪽만 반영) | 분기 상수(키아트 높이·고지문구 조립)를 공통 헬퍼/상수로 단일화 — 기존 R37(`fitAppStoreDescription`) 패턴 |
| R-2 | KO 고지문구 폭 초과 (CTA 버튼 폭 가변 → 가용 폭 축소) | max-width 해제 + 폭 실측. 초과 시 fallback: 고지문구만 둘째 줄 |
| R-3 | hide-stats 토글 시 1:1 y-플로우 변동 | Canvas는 이미 y-플로우 구조 — 키아트 높이를 "잔여 공간" 기반으로 계산해 자연 대응. DOM도 flex 기반 동일 확인 |
| R-4 | `buildBatchCfgs` AS 분기가 size 고정이라 2사이즈 선택 시 중복 4장 생성 | GP `gpSizes` 필터 패턴 이식 (`sizes.filter(s => s==='9x16'||s==='1x1')`, 빈 배열 시 9x16 fallback) |
| R-5 | 키아트 상하 ~8~10% 크롭으로 소재 핵심 비주얼 잘림 | 운영 가이드: 키아트 상하 10%는 안전 영역 외로 취급 (README 한 줄 추가) — 코드 대응 아님 |

---

## Reused Existing Functions (재사용 우선)

| 헬퍼 | 용도 |
|---|---|
| `drawImageCover(ctx, img, x, y, w, h)` | 키아트 중앙 크롭 (Canvas) — 이미 사용 중, 높이만 변경 |
| `fitAppStoreTitle` / `asFontFamily` | 타이틀 auto-fit / 언어별 폰트 — 무수정 재사용 |
| `AS_LANG_PACK` / `LANG_PACK.ko.disclaimer` | IAP 문구 + 고지문구 소스 — 상수 추가 없음 |
| GP `gpSizes` 필터 (line ~11571) | 배치 사이즈 필터 패턴 이식 |
| `applyTemplateSwitch` sd-showcase 분기 | 사이즈 옵션 부분 활성 패턴 (option 단위 disabled) |

---

## Implementation Sequencing (1~2 sessions)

1. **Session 1 — renderer** (~150 라인): CSS `.size-1x1` + DOM 빌더 분기 + Canvas 빌더 분기 + KO 고지문구 합성 로직
2. **Session 2 — ui-batch-verify** (~80 라인): `applyTemplateSwitch` 사이즈 잠금 해제 + 배치 체크박스/`buildBatchCfgs` 필터 + description 필드 토글 + 브라우저 실측 검증

각 세션 종료 시 `node --check` 문법 검증.

---

## Out of Scope

- 1200×1200 export (검토 후 제외 — 필요 시 ×1.111 스케일 렌더로 후속 확장)
- B안 레이아웃(스탯 제거 + 16:9 무크롭) 전용 토글 — 단, hide-stats 토글의 자연 y-플로우로 유사 효과 허용
- 세로형(9:16) KO 고지문구 위치 변경 — O-2 B 결정 유지
- 키아트 1:1 전용 별도 업로드 슬롯 (4언어 공용 1장 정책 유지, 9:16과도 공용)
- 테마 확장 (디자인 1개당 1테마 정책 유지)

---

## Critical Files

- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/today-banner-designer.html` — 유일한 수정 대상
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/CLAUDE.md` — 완료 시 "현재 상태" 섹션 갱신
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/docs/01-plan/features/appstore-screenshot-square.plan.md` — 본 plan
- `/Users/sungkkim/Desktop/mkt_bannerdesigner/repo/docs/02-design/features/appstore-screenshot-square.design.md` — 다음 phase
