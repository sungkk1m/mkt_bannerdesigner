# Plan: filename-rule — 실무 소재 이름규칙 자동 적용

> PDCA Plan Plus (r2) · 2026-08-26 · 담당: 김성권 (ksk@superplanet.net)
> 대상: `today-banner-designer.html` (origin/main = 6f7b7f5, v1.17 / 10개 템플릿 기준)
> 상태: **구현 완료** (`feature/filename-rule` 브랜치). Q1~Q3 사용자 결정 반영, node 단위 테스트 14케이스 + GP 충돌 검사 PASS. 브라우저 실측 대기.

---

## Executive Summary

| 관점 | 내용 |
|------|------|
| **Problem** | 툴이 저장하는 파일명(`prefix_1x1_ko.png`, 템플릿별 제각각 10종 패턴)이 실무 소재 이름규칙(`언어_타이틀_소재컨셉_규격`, 예: `한_SMS_투데이탭_1080x1080.png`)과 달라 다운로드 후 매번 수동 rename이 발생한다. |
| **Solution** | 타이틀 영문명(SMS, SODA 등)만 입력하면 언어 토큰(한/영/일/번)·소재컨셉(투데이탭 등 10종)·실제 픽셀 규격이 자동 조합되는 중앙 파일명 함수 1개로 10개 템플릿 전체를 통일한다. |
| **Function UX Effect** | 단건·배치·ZIP 모든 다운로드 경로에서 rename 0회. 배치 ZIP을 풀면 그대로 Google Drive 소재 폴더에 업로드 가능한 파일명이 나온다. |
| **Core Value** | 소재 산출→업로드 파이프라인의 마지막 수동 단계 제거. 신규 템플릿 추가 시 CONCEPT_TOKEN 1줄만 추가하면 규칙이 자동 상속된다. |

## Context Anchor

| 항목 | 내용 |
|------|------|
| **WHY** | 다운로드 파일명이 실무 규칙과 달라 전 소재 수동 rename 중 |
| **WHO** | UA 마케터 (본인 + 팀, Google Drive 소재 폴더 공유) |
| **RISK** | GP 다크+라이트 동시 배치 시 테마 미구분 → ZIP 내 파일명 충돌로 절반 유실 (R-02, Critical) |
| **SUCCESS** | 10개 템플릿 × 단건/배치/ZIP 전 경로에서 `언어_타이틀_소재컨셉_규격.ext` 자동 생성, 충돌 0 |
| **SCOPE** | `today-banner-designer.html` 1개 파일. 상수 3개 + 중앙 함수 1개 + 호출부 ~14곳 + 입력 UI 1개 |

---

## 1. 검증 결과 (Feasibility — 사용자 요청: "가능한지 검증만")

**결론: 가능하다.** 파일명이 만들어지는 지점을 전수 조사한 결과 아래 14곳이 전부이며, 모두 한 함수로 수렴시킬 수 있는 구조다.

### 1.1 현재 파일명 생성 지점 전수 조사 (origin/main 6f7b7f5 기준)

| # | 템플릿 | 단건 모드 현재 형식 | 배치 모드 현재 형식 |
|---|--------|--------------------|--------------------|
| 1 | today-tap | `{slug(게임명)}_{size}_{lang}` | `{b.prefix}_{size}_{lang}` |
| 2 | app-badge | `{slug(헤드라인1줄)}_app-badge_{size}_{lang}` | `{b.prefix}_app-badge_{size}_{lang}` |
| 3 | appstore-screenshot | `{slug(타이틀)}_appstore_{lang}_{theme}_{dim}` | `{b.prefix}_appstore_{lang}_{theme}_{dim}` |
| 4 | sd-showcase | `{prefix}_sdshowcase_{lang}_{dim}` | `{b.prefix}_sdshowcase_{lang}_{dim}` |
| 5 | keyvisual-review | `{prefix}_keyvisual-review_{lang}_1080x1080` | 동일 패턴 |
| 6 | pickup | `{prefix}_pickup_{lang}_{dim}` | 동일 패턴 |
| 7 | steam-review | `{prefix}_steam-review_{lang}_{dim}` | 동일 패턴 |
| 8 | ask-me-anything | `{prefix}_ama_{lang}_1080x1920` | 동일 패턴 |
| 9 | google-play-screenshot | `{prefix}_google-play-screenshot_{lang}_{theme}_{dim}` | 동일 패턴 |
| 10 | install-plz | `installplz_{lang}_{dim}` (prefix 없음, 하드코딩) | `{b.prefix}_installplz_{lang}_{dim}` |

- 단건: 템플릿별 빌더 함수 10개 (`buildFilename`, `buildAppBadgeFilename`, `buildAppStoreFilename`, `buildSdShowcaseFilename`, `buildKvrFilename`, `buildPickupFilename`, `buildSteamReviewFilename`, `buildAmaFilename`, `buildGooglePlayScreenshotFilename`, `buildInstallPlzFilename`) — `handleSingleDownload` 내 분기에서 호출 (tip 기준 L10515~10590)
- 배치: `downloadBatchItem`(L11893~) / `handleBatchExportZip`(L12170~) 인라인 삼항 체인 2곳 + html-to-image fallback 1곳 (L12210) + ZIP 파일명 `{b.prefix}_banners.zip` 1곳
- 단건 prefix 출처가 제각각: 템플릿별 텍스트 필드(게임명/헤드라인/리뷰제목/캐릭터명/부제 등)를 `slugify` — **소문자 강제 + 한글 소실(기존 B-03/M-3 이슈)**. 신규 규칙에서는 전용 입력으로 대체되어 이 이슈 자체가 소멸한다.

### 1.2 신규 이름규칙 (실무 규칙, 캡처본 근거)

```
{언어토큰}_{타이틀영문명}_{소재컨셉}_{가로x세로}.{ext}
예: 한_SMS_투데이탭_1080x1080.png · 번_SODA_앱스토어_1080x1920.png
```

**언어 토큰** (FR-01): `ko→한` · `en→영` · `ja→일` · `zh-TW→번`

**소재컨셉 토큰** (FR-02, 사용자 확정):

| 템플릿 키 | 소재컨셉 | 템플릿 키 | 소재컨셉 |
|-----------|---------|-----------|---------|
| today-tap | 투데이탭 | pickup | 픽업 |
| app-badge | 앱아이콘 | steam-review | 스팀리뷰 |
| appstore-screenshot | 앱스토어 | ask-me-anything | 무물보 |
| sd-showcase | SD쇼케이스 | google-play-screenshot | 구글플레이 |
| keyvisual-review | 아이폰리뷰 | install-plz | 설치구걸 |

**규격 토큰** (FR-03): 기존 코드의 사이즈 해석 로직 재사용 — `1x1→1080x1080`, `9x16→1080x1920`, `1200x628→1200x628`, GP `4x5→1080x1350`, KVR 고정 `1080x1080`, AMA 고정 `1080x1920`. 전부 코드에 이미 존재하므로 신규 계산 불필요.

### 1.3 기술 검증 완료 항목

| 항목 | 결과 |
|------|------|
| 한글 파일명 브라우저 다운로드 (`a.download`) | 가능. 모든 모던 브라우저 유니코드 지원 |
| 한글 파일명 ZIP (JSZip) | 가능. JSZip이 UTF-8 플래그 기록, Windows 10 탐색기 정상 해제 (구형 압축 유틸만 주의 — R-01) |
| 대문자 보존 (SMS, SODA) | 가능. 단, 기존 `slugify`는 소문자 강제이므로 prefix에는 slugify 대신 전용 sanitize 사용 (FR-09) |
| 소재컨셉 한글 토큰 | 가능. 고정 상수라 sanitize 불필요 |
| 모든 템플릿 적용 | 가능. 생성 지점 14곳 전수 확인, 누락 경로 없음 |

---

## 2. 대안 비교 (Plan Plus — Alternatives)

| 안 | 내용 | 평가 |
|----|------|------|
| **A안 (권장)** | 중앙 함수 `buildAssetFilename({template, lang, size, prefix, theme, ext})` 1개 + 토큰 상수 3개. 기존 빌더 10개와 인라인 체인을 전부 위임/교체 | 규칙이 한 곳에 존재. 신규 템플릿은 CONCEPT_TOKEN 1줄. 코드 순감소(-10 함수) |
| B안 | 기존 빌더 10개를 각각 신규 형식으로 수정 | 변경은 국소적이나 중복 10곳 존치 → 규칙 재변경 시 같은 작업 반복 |
| C안 | 다운로드 직전 기존 파일명을 정규식으로 rename | 템플릿별 예외(theme, 고정 사이즈)에 취약, 디버깅 어려움. 비권장 |

**결정: A안.** (B-01류 silent failure를 만든 원인이 "같은 로직의 복제"였음 — 동일 실수 재발 방지)

## 3. YAGNI 제외 항목

- 토큰 순서/구분자 커스터마이징 UI — 규칙은 팀 고정 규칙이므로 불필요
- 언어 토큰 사용자 편집 — 불필요
- 파일명 실시간 미리보기 위젯 — 선택(구현 시 status 한 줄로 충분), 이번 범위 제외

---

## 4. Functional Requirements

| FR | 내용 |
|----|------|
| FR-01 | `LANG_TOKEN` 상수: `{ko:'한', en:'영', ja:'일', 'zh-TW':'번'}` |
| FR-02 | `CONCEPT_TOKEN` 상수: §1.2 표의 10개 매핑 |
| FR-03 | 규격 해석: 템플릿×사이즈 키 → `가로x세로` 문자열 (기존 sizeMap/asSizeDim 로직 통합) |
| FR-04 | 중앙 함수 `buildAssetFilename()` — 유일한 파일명 조립 지점 |
| FR-05 | 단건 모드: `handleSingleDownload` 분기 10곳을 중앙 함수 호출로 교체 (기존 빌더 10개 제거 또는 위임) |
| FR-06 | 배치 모드: `downloadBatchItem` + `handleBatchExportZip` 인라인 체인 2곳 + fallback 1곳 교체 |
| FR-07 | 단건 모드에 "타이틀 영문명" 전역 입력 신설 (`#s-title-code`, `state.single.titleCode`) — 포맷/해상도 셀렉트 옆 배치 |
| FR-08 | 배치 `#b-prefix` 라벨·placeholder 변경: "타이틀 영문명 (예: SMS)" — 기존 input 재사용 |
| FR-09 | prefix sanitize: trim + 공백 제거 + 금지문자(`\/:*?"<>|`) 제거 + **대소문자 보존** + 빈 값 fallback (Q2) |
| FR-10 | 테마 구분: google-play-screenshot은 다크+라이트 **동시 생성**이므로 파일명에 테마 토큰 필수 (Q1 결정 반영). appstore-screenshot도 동일 규칙 적용 |
| FR-11 | 배치 ZIP 파일명: `{타이틀}_{소재컨셉}.zip` (예: `SMS_투데이탭.zip`) |
| FR-12 | install-plz 하드코딩(`installplz_`) 제거 → 공통 규칙 편입 |

## 5. Success Criteria

| SC | 내용 |
|----|------|
| SC-01 | 10개 템플릿 각각 단건 다운로드 시 `언어_타이틀_소재컨셉_규격.ext` 형식 (예: `한_SMS_투데이탭_1080x1080.png`) |
| SC-02 | 배치 ZIP 내 전 조합이 신규 규칙, 파일명 충돌 0 (특히 GP 다크/라이트 8~16장 전수 존재) |
| SC-03 | 4개 언어 토큰 정확 매핑 (한/영/일/번) |
| SC-04 | 타이틀 대문자 보존 (`SMS`→`SMS`, `soda`→`soda` 입력 그대로) |
| SC-05 | Windows 10 탐색기에서 ZIP 해제 시 한글 파일명 정상 표시 |
| SC-06 | 타이틀 미입력 시에도 다운로드 실패 없음 (fallback 동작) |

## 6. Risks

| R | 내용 | 대응 |
|---|------|------|
| R-01 | 구형 압축 유틸(구버전 알집 등)에서 ZIP 내 한글 파일명 깨짐 가능 | 낮음. Windows 10 기본 탐색기·반디집·최신 알집은 UTF-8 플래그 지원. 실측 1회로 확인 |
| R-02 | **(Critical 제약)** GP 배치는 dark+light 동시 fan-out (`buildBatchCfgs` L11655) — 테마 토큰 없으면 ZIP 내 동일 파일명으로 절반 유실 | FR-10 필수 반영. Q1에서 표기 방식만 결정 |
| R-03 | **로컬 저장소 불일치**: 로컬 main(c7610e3)이 origin/main(6f7b7f5)보다 28커밋 뒤 + 미커밋 553줄(구 store-listing v1.5, origin/main의 appstore-screenshot으로 대체된 작업으로 추정) | 구현 전 origin/main 동기화 필수. 미커밋분 처리(스태시/폐기)는 **사용자 승인 후** 진행 (프로젝트 규칙: 허락 없이 삭제 금지) |
| R-04 | 프리셋·localStorage에 저장된 기존 `b-prefix` 값('banner' 등)이 그대로 타이틀 자리에 노출 | placeholder 갱신 + 빈 값 fallback으로 흡수 |

## 7. Open Questions — 사용자 결정 완료 (2026-08-26)

| Q | 질문 | **결정** |
|---|------|--------|
| **Q1** | GP(및 앱스토어) 테마 토큰 표기 | **소재컨셉에 괄호 병기: `앱스토어(다크)` / `구글플레이(라이트)`** — `_` 구분자 남발 금지 (사용자 지정) |
| **Q2** | 타이틀 미입력 시 fallback 문자열 | **`TITLE`** (권장안 채택) |
| **Q3** | 2x(레티나) 다운로드 시 규격 토큰 | **실제 픽셀** (예: 2x 1:1 → `2160x2160`, 권장안 채택) |

- 추가 결정: 로컬 저장소는 origin/main(6f7b7f5)으로 동기화 완료. 기존 미커밋 553줄(구 store-listing v1.5)은 **stash 보존** (`backup: stale store-listing v1.5 work ...`). 구현은 `feature/filename-rule` 브랜치 — 사용자 실측 후 main 머지/PR 진행 예정.

## 8. 구현 규모 추정

- 수정 파일: `today-banner-designer.html` 1개
- 신규: 상수 2~3개 + 중앙 함수 1개 + 단건 입력 UI 1개 (~60줄)
- 교체: 단건 빌더 호출 10곳, 배치 인라인 체인 2곳, fallback 1곳, ZIP명 1곳 (~-80/+40줄)
- 순 diff 약 ±150줄, 기존 렌더링·Canvas 로직 무접촉 (파일명 계층만 변경 → 회귀 리스크 낮음)

## 9. 다음 단계

1. ~~사용자: Q1~Q3 결정 + R-03 승인~~ → 완료 (2026-08-26)
2. ~~구현~~ → 완료 (`feature/filename-rule`, 소규모 변경이라 Design 단계 생략하고 Plan→Do 직행)
3. 사용자 브라우저 실측: 단건 10템플릿 + 배치 ZIP(특히 GP 다크/라이트 8장 전수) + Windows ZIP 해제 한글 확인 (SC-01~06)
4. 실측 통과 시 사용자가 main 머지 또는 PR

## 10. 구현 결과 요약 (Do — 2026-08-26)

- 신규: `LANG_TOKEN` / `CONCEPT_TOKEN` / `THEMED_TEMPLATES` / `THEME_TOKEN` 상수 + `sanitizeTitleCode()` + `assetDim()` + `buildAssetFilename()` (FR-01~04)
- 교체: 단건 `handleSingleDownload` 분기 → 중앙 호출 1개 (FR-05) · 배치 `downloadBatchItem`/`handleBatchExportZip`/fallback 3곳 (FR-06) · ZIP명 `{타이틀}_{소재컨셉}.zip` (FR-11)
- 제거: 구 빌더 10개(`buildFilename`, `buildAppBadgeFilename`, `buildAppStoreFilename`, `buildSdShowcaseFilename`, `buildKvrFilename`, `buildPickupFilename`, `buildSteamReviewFilename`, `buildAmaFilename`, `buildGooglePlayScreenshotFilename`, `buildInstallPlzFilename`) + `asSizeDim` + `slugify` (전부 참조 0 확인 후 제거)
- UI: 단건 `#s-title-code` 입력 신설(FR-07, 프리뷰 재렌더 없이 state만 갱신) · 배치 `#b-prefix` 라벨/placeholder/힌트 갱신(FR-08) · `state.batch.prefix` 기본값 `'banner'` → `''`
- 부수 수정(기존 불일치 해소): 배치 개별 다운로드에 install-plz 분기 부재 → 중앙 함수로 자동 해소 · 배치 ZIP에 steam-review 분기 부재 → 동일 해소
- 검증: `node --check` 통과(1,064,386 chars) · 단위 테스트 14케이스 + GP 다크/라이트 충돌 검사 PASS (`한_SMS_투데이탭_1080x1080.png` / `번_SODA_앱스토어(라이트)_1080x1920.png` / `영_TITLE_설치구걸_2400x1256.png` 등)
