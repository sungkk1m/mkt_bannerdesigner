# PDCA Plan — Install Plz 템플릿 (v1.15)

**Feature**: install-plz
**Created**: 2026-07-19
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/pdca plan`
**Reference**: `~/Downloads/{한|영|일|번}_UD_설치구걸_{1080x1080|1200x628}.png` (8장, 2026-07-19 수령)

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | Install Plz 템플릿 추가 (10번째 템플릿) — "설치 구걸" 밈 배너 |
| 시작 | 2026-07-19 |
| 본체 파일 | `today-banner-designer.html` (11,828라인) + `assets/install-plz/` (신규 8 PNG) |
| 사이즈 | 1200×628 + 1080×1080 (9:16 미지원) |
| 언어 | en / ko / ja / zh-TW (4개, 레퍼런스 8장 전부 확보 완료) |
| 핵심 방식 | **텍스트 이미지화(플레이트)** — 레퍼런스 원본 픽셀 그대로 추출, 폰트 렌더링 0% |
| FR | 12건 |
| NFR | 4건 |
| SC | 6건 |
| R | 4건 |

### Value Delivered (4관점)

| 관점 | 내용 |
|---|---|
| **Problem** | "이 광고 돈냈어요" 밈 형식 배너의 SD 캐릭터만 게임별로 교체해 재활용하고 싶으나, 특수 밈 폰트(외곽선 스타일)가 툴 폰트 스택에 없어 텍스트 재현 불가. 디자이너 수작업으로 4언어×2사이즈=8장 제작 |
| **Solution** | 레퍼런스에서 텍스트 영역을 픽셀 그대로 잘라낸 "텍스트 플레이트" 8장을 에셋화. 사용자는 SD 1장만 업로드 → 8장 자동 생성. 폰트 완전 무변형 |
| **Function/UX Effect** | 헤더 셀렉터 "Install Plz" → SD 드롭존 1개 + 사이즈별 X/Y/Scale 조정 → Single 1장 / Batch ZIP 8장. KO 고지문구는 플레이트에 원본 위치 그대로 포함 (별도 렌더 없음) |
| **Core Value** | 밈 포맷 재활용 인프라화 — 신규 게임 SD 1장으로 8장 즉시 생산, 폰트/문구/고지 위치 원본과 픽셀 동일 |

---

## Context Anchor

| Key | Value |
|-----|-------|
| **WHY** | 밈 폰트(두꺼운 외곽선 코믹체)가 툴 폰트 스택(Pretendard/Noto)에 없음 → 텍스트를 폰트로 재현 불가. 원본 픽셀 추출만이 "아예 변경 없이"를 만족 |
| **WHO** | UA Manager — Underdark:Defense 및 향후 타 게임 SD 교체 재활용 |
| **RISK** | 레퍼런스 1200×628이 실제 1200×625 (하단 3px 흰 패딩으로 대응); EN 1080 텍스트-캐릭터 간극 8px로 타이트 (검증 완료); 향후 문구 수정 불가(원본 고정) — 의도된 제약 |
| **SUCCESS** | 8장 플레이트에 캐릭터 잔여물 0 + 텍스트 잘림 0 (픽셀 검증 완료); 원본 재조립 시 육안 동일; Single/Batch 양쪽 동작; 기존 9 템플릿 회귀 0건 |
| **SCOPE** | Do-1: 플레이트 에셋 생성 / Do-2: 템플릿 구현 (데이터+렌더러+단건 UI+배치 UI) |

---

## 사전 검증 결과 (Feasibility — 2026-07-19 완료) ★

사용자 요청 5번 "폰트를 이미지화해서 그대로 넣어주는 것이 가능한지 검증" → **가능 확정**.

| 검증 항목 | 방법 | 결과 |
|---|---|---|
| 텍스트/캐릭터 분리 | 4언어 픽셀 diff (언어 간 동일 픽셀 = 캐릭터, 상이 = 텍스트) | 분리 가능 |
| 1080×1080 밴드 경계 | 언어별 상/하단 텍스트 밴드 y 측정 (blue-mask로 물방울/웅덩이 vs 검정 텍스트 색상 구분) | ko Y1=212/Y2=811, en Y1=252/Y2=823, ja·zh Y1=245/Y2=823 |
| EN 1080 하단 2줄 함정 | "PLEASE TRY"(y831~)가 웅덩이(~y820)와 12px 간극 | Y2=823으로 두 줄 모두 보존 |
| 1200×628 좌우 경계 | 텍스트 우단 (ko 627 / en 608 / ja 620 / zh 545) vs 캐릭터 좌단 (x604, 물방울) | 컬럼 겹침 → 세로 크롭(y≤553) + blue-key 정리로 해결 |
| KO 고지문구 | 1080: 상단 밴드에 자연 포함. 1200: 우상단 (1050,8)-(1192,40) 별도 스탬프 — 타 언어 동일 영역 dark px 0 확인 | 원본 위치 그대로 보존 |
| 재조립 무결성 | 플레이트 + 캐릭터 크롭 파티션 재조립 vs 원본 max diff = 0 | 통과 |
| 원본 캐릭터 규격 | 두 사이즈 모두 정확히 587×570 동일 크기 배치 (1080: (258,240) / 1200: (609,25)) | SD 1장 공용 구조 타당 |

검증 스크립트: scratchpad `analyze_refs*.py`, `make_plates*.py` (세션 산출물, 최종본은 Do-1에서 repo에 보존)

---

## 사용자 결정 요약 (확정 — 2026-07-19 Checkpoint)

| # | 항목 | 결정 |
|---|------|------|
| 1 | 템플릿 이름 | **"Install Plz"** (key: `install-plz`, 하이픈 컨벤션) |
| 2 | 사이즈 | 1200×628 + 1080×1080 (레퍼런스 그대로) |
| 3 | 텍스트 | **플레이트(이미지) 고정 — 편집 UI 없음**, 폰트 무변형 |
| 4 | SD 미업로드 기본 표시 | **빈 슬롯** (원본 엘프 캐릭터 에셋 미포함) |
| 5 | 에셋 저장 | **외부 파일** `assets/install-plz/` (pickup 패턴) — 폰트 보존은 저장 방식과 무관함 확인 |
| 6 | SD 업로드 | **1장 공용** (4언어×2사이즈 전체 적용) |
| 7 | SD 조정 | **사이즈별 X/Y/Scale** (sd-showcase `slotAdjustPerSize` 패턴, 슬롯 1개) |
| 8 | KO 고지문구 | 플레이트에 원본 위치 그대로 포함 (1080 우상단 / 1200 우상단) — 툴의 자동 고지 렌더 **비활성** (이중 표시 방지) |
| 9 | 1200×628 출력 | 원본 625 높이 → **하단 3px 흰 패딩** (스케일 변형 없음) |

---

## Functional Requirements (FR)

- **FR-01**: 헤더 템플릿 셀렉터에 `install-plz` 옵션 추가 (10번째) + `TEMPLATE_KEYS` 확장
- **FR-02**: 에셋 8장 — `assets/install-plz/text-plate_{ko|en|ja|zh-TW}_{1x1|1200x628}.png` (1x1=1080×1080, 1200x628=1200×628 패딩 완료본)
- **FR-03**: 상수 `INSTALL_PLZ_ASSETS` (플레이트 경로 매핑) + `INSTALL_PLZ_CANVAS_SPECS` (SD 기본 박스: 1x1 → (258,240,587,570) / 1200x628 → (609,25,587,570)) + `INSTALL_PLZ_DEFAULT`
- **FR-04**: `applyTemplateSwitch` 분기 — 1x1 + 1200x628 활성, 9x16 비활성 (sd-showcase 패턴)
- **FR-05**: state 확장 — `state.single.installplz {sdImage, slotAdjustPerSize}` + `state.batch.ip_sdImage, ip_slotAdjustPerSize`
- **FR-06**: SD 드롭존 (단건 `#s-ip-sd`, 배치 `#b-ip-sd`) — `setupDropzone` + `updateStateImage` 재사용
- **FR-07**: 사이즈별 X/Y/Scale 슬라이더 (단건/배치 각각, 편집 사이즈 토글 포함 — sd-showcase R5 UI 패턴, 슬롯 1개 단순화)
- **FR-08**: Canvas 렌더러 `buildInstallPlzCanvas(cfg)` — ① 흰 배경 fillRect ② 플레이트 drawImage(0,0) ③ SD `drawImageContain`(기본 박스 + x/y/scale 보정). 텍스트/고지 렌더 없음
- **FR-09**: 단건 다운로드 분기 — 파일명 `{prefix}_installplz_{lang}_{size}.{ext}`
- **FR-10**: 배치 ZIP — 선택 사이즈 × 4언어 fan-out (최대 8장), SD 1장 + 플레이트 8장 `_imgCache` 공유
- **FR-11**: `renderBatchLangFields` 분기 — 언어별 입력 필드 없음, "텍스트는 레퍼런스 원본 고정(이미지)" 안내 표시
- **FR-12**: KO 자동 고지문구 렌더 로직에서 `install-plz` 제외 (플레이트 내장이므로 이중 표시 방지)

## Non-Functional Requirements (NFR)

- **NFR-01**: 플레이트에 캐릭터 잔여물 0px / 텍스트 손실 0px (사전 검증 경계값 사용)
- **NFR-02**: Canvas export 픽셀 정합 — 플레이트는 무스케일 drawImage(원본 해상도 = 캔버스 해상도)
- **NFR-03**: `_imgCache` 재사용 — 배치 시 플레이트 8장 + SD 1장 각 1회 디코드
- **NFR-04**: 단일 HTML 정책 유지 (에셋만 외부, 코드는 인라인)

## Scenarios (SC)

- **SC-01**: "Install Plz" 선택 → 1x1/1200x628만 활성, SD 드롭존 + X/Y/Scale UI 표시, 텍스트 입력 UI 없음
- **SC-02**: SD 업로드 → 미리보기에 플레이트 텍스트 + SD 합성 표시, 언어 전환 시 플레이트 스왑
- **SC-03**: X/Y/Scale 조정 → 사이즈별 독립 반영 (1x1 조정이 1200x628에 영향 없음)
- **SC-04**: KO 선택 → 고지문구가 원본 위치(우상단)에 표시, 타 언어 미표시. 별도 고지 렌더 없음
- **SC-05**: 배치 2사이즈 + 4언어 → ZIP 8장, 각 장의 텍스트가 해당 언어/사이즈 레퍼런스와 픽셀 동일
- **SC-06**: SD 미업로드 → 텍스트 플레이트만 렌더 (빈 슬롯, 에러 없음)

## Risks (R)

- **R-01 (문구 고정)**: 텍스트 수정 불가 — 의도된 제약. 문구 변경 필요 시 새 레퍼런스 수령 → 플레이트 재생성 (Do-1 스크립트 재실행)
- **R-02 (외부 에셋 의존)**: `file://` 직접 열기 시 이 템플릿 export 불가 (canvas taint) — pickup과 동일 제약, static server 사용 중이라 영향 없음
- **R-03 (EN 플레이트 용량)**: EN 원본 JPEG 노이즈로 216~240KB (타 언어 3~4배) — 총 1.1MB 수준, 허용
- **R-04 (레퍼런스 좌표 하드코딩)**: 플레이트 생성 경계값이 이 레퍼런스 전용 — 새 밈 템플릿엔 재검증 필요. 생성 스크립트를 `assets/install-plz/`에 보존해 재사용

---

## Implementation Order

| Session | Module | 범위 |
|---------|--------|------|
| **Do-1** | `plate-assets` | 생성 스크립트 최종화 → `assets/install-plz/` 8 PNG + 스크립트 보존 |
| **Do-2** | `template-code` | FR-01~FR-12 (데이터/스위치 → 렌더러 → 단건 UI → 배치 UI) |
| **Check** | `verify` | 브라우저 실측 (single 8조합 + batch ZIP + 회귀) |

## Out of Scope (v1 명시 제외)

- ❌ 텍스트 편집 / 폰트 렌더링 (플레이트 고정이 핵심 요구)
- ❌ 원본 엘프 캐릭터 기본 표시 (사용자 결정 #4)
- ❌ 9:16 사이즈
- ❌ SD 회전/반전, 다중 SD 슬롯
- ❌ 언어별 SD 개별 업로드
- ❌ 다크 테마 (레퍼런스 = 흰 배경 단일)

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-07-19 | 최초 작성 — 사전 픽셀 검증 완료(가능 확정), 사용자 결정 9건 반영 | ksk@superplanet.net |
