# CLAUDE.md — Today Banner Designer 프로젝트 규칙

Claude Code가 이 프로젝트에서 작업할 때 반드시 참고할 지침입니다.
작업 지시를 받을 때, 에러·이슈가 발생했을 때마다 "현황 / 히스토리" 섹션을 간결하게 업데이트하세요 (컨텍스트 꼬이지 않도록 주의).

---

## 절대 하지 말아야 할 것들

- 내 허락 없이 파일 삭제하지 말 것
- 모르면 추측하지 말고 반드시 물어볼 것
- 작업 중간에 임의로 다른 방향으로 바꾸지 말 것

## 해야 할 것들

- 작업을 지시받을 때, 이 문서의 "현황" 섹션을 간결하게 갱신
- 에러·이슈 발생 시, 이 문서의 "히스토리" 섹션에 원인·대응을 간결하게 기록
- 두 섹션 모두 누적 시 **간결함 우선** (컨텍스트 꼬이지 않게, 오래된 항목은 요약/정리)

---

## 프로젝트 개요

- **이름**: Today Banner Designer (v1.2)
- **유형**: 단일 HTML 사내 툴 (Apple "Today" 스타일 광고 배너 자동 생성)
- **본체**: `today-banner-designer.html`
- **문서**: `README.md`
- **담당**: UA Manager 김성권 (ksk@superplanet.net)

## 현황

_(작업 지시 시 최신 상태로 갱신)_

- 2026-04-22: CLAUDE.md 초기 생성, 프로젝트 규칙 정의
- 2026-04-22: 코드 리뷰 완료 (Verdict: Request Minor Changes) — 상세는 `~/.claude/plans/rosy-tickling-tide.md`
  - 우선 수정 권장: slugify 한글 손실(line 1108), 배치 재진입 가드(line 1291), CDN SRI 누락
- 2026-04-22: **[PDCA Plan] banner-bugfix** (r1) — 실사용 발견 이슈 5건 + GitHub Pages 별도 트랙
  - 문서: `docs/01-plan/features/banner-bugfix.plan.md`
  - 범위(초기): 게임명 ellipsis 제거 + 글자수 힌트 / 고지문구 nowrap+폰트·위치 / 오버플로우 darkbar 상단 클립 / Scale max 150% / 배치 DOM 프리뷰 즉시 + 다운로드 시점에만 이미지 변환
- 2026-04-22: **[PDCA Plan] banner-bugfix** (r2) — 부제 처리 + Drop Shadow 기능 추가
  - 부제도 title과 동일 정책(nowrap + 힌트) — FR-10/11
  - Overflow Drop Shadow 기능 신규 추가 — FR-12\~15 (filter: drop-shadow, 4개 슬라이더, 사이즈별 독립 저장, 기본 Off)
- 2026-04-22: **[PDCA Do] banner-bugfix** — 일괄 구현 완료
  - CSS: game-title ellipsis 제거(FR-01), game-subtitle nowrap 추가(FR-10), disclaimer nowrap+1:1 폰트·위치 조정(FR-03/04), overflow-wrap bottom을 darkbar 상단 정렬(FR-05)
  - HTML: title/subtitle 힌트(FR-02/11), Scale max 120→150(FR-06), Shadow UI 단건·배치 양쪽 추가(FR-13), 배치 버튼 분리(프리뷰/ZIP, FR-07/08)
  - JS: SHADOW_DEFAULT + state.single.shadow + state.batch.shadowPerSize, renderBanner에 filter: drop-shadow() 주입, bindSingle/BatchMode Shadow 이벤트, waitForImages를 img.decode()로 전환(FR-09), handleBatchPreview + handleBatchExportZip + downloadBatchItem 2단계 분리
- 2026-04-22: **[PDCA Check] banner-bugfix** — Gap 분석 완료
  - 문서: `docs/03-analysis/banner-bugfix.analysis.md`
  - Match Rate: **≈ 97%** (FR 15/15 = 100%, SC 10/11 Met + 1 Partial)
  - Critical/Important Gap: **0건**. Minor 3건 (모두 긍정 방향/명세 해석)
  - SC-07 속도 50%+ 단축은 사용자 실측에서 **미달성 확인** → 후속 feature(bugfix)로 이관
- 2026-04-22: **[PDCA Plan] bugfix** — Canvas 직접 합성 + Overflow 확장
  - 문서: `docs/01-plan/features/bugfix.plan.md`
  - 범위: ① html-to-image 제거, Canvas 2D API 직접 합성으로 배치 8장 ≤ 2초 목표 ② Overflow Scale max 150→200, X/Y 오프셋 각 ±80% 확장 + wrap `clip-path`로 다크바 하단 침범 방지 (상·좌·우 자유)
  - 결정: Option A (Canvas 직접 합성) 선정
- 2026-04-22: **[PDCA Do] bugfix** — 일괄 구현 완료
  - CSS: `.banner-overflow-wrap`에 `clip-path: inset(-9999px -9999px 0 -9999px)` (FR-12)
  - HTML: 단건/배치 Overflow slider 6개 범위 확장 (Scale 200, X/Y ±80) (FR-09/10/11)
  - JS renderBanner: `transform`을 wrap → img로 이동 (FR-13). wrap 고정 + clip-path 정상 작동
  - JS 신규: `CANVAS_SPECS[size]` 사이즈별 레이아웃 테이블 (3 사이즈) · `roundRect()` polyfill · `loadCachedImage`(data URL decode 1회 캐시) · `prepCfgImages` · `ensureFontsLoaded`(Pretendard·Noto JP·Noto TC 3종 × weight 조합 사전 로드) · `getFontFamilyForLang`(언어별 폰트 스택) · `drawImageCover`(object-fit:cover 재현) · `buildBannerCanvas(cfg)`(11단계 수동 합성: 배경/Today 헤더/프로필 아이콘/카드 rounded clip+키아트/오버플로우 + drop-shadow + 하단 clip/다크바 rgba/앱 아이콘/CTA measure+rounded/game-title·subtitle nowrap/disclaimer) · `canvasToDataURL(canvas, format, quality)`
  - JS 경로 교체: `handleSingleDownload`, `downloadBatchItem`, `handleBatchExportZip` 모두 `USE_CANVAS_EXPORT=true`일 때 Canvas 경로 사용. batch ZIP은 이미지 3종을 **1회만 decode 후 모든 조합 공유**로 추가 최적화. 모든 경로에 `performance.now()` 측정 로깅 추가
  - Fallback: `USE_CANVAS_EXPORT=false`로 변경 시 기존 html-to-image 경로 즉시 복구 (Plan R-08)
- 2026-04-22: **[PDCA Check] bugfix** — Gap 분석 완료
  - 문서: `docs/03-analysis/bugfix.analysis.md`
  - Match Rate: **100%** (FR 13/13, SC 10/10) — 사용자 브라우저 실측 "문제 전혀 없고 정상 구현" 확인
  - Critical/Important/Minor Gap: **0건**
  - 참고: I-01~I-03(메모리·letterSpacing 호환성·프로필 아이콘 근사) 관찰 기록 — Gap 아님, 미래 개선 후보
  - 상태: 사용자 **추가 작업 요청 대기** (Report는 추가 작업 완료 후 통합)
- 2026-04-22: **[PDCA Plan] bugfix (r3)** — 실사용 이슈 5건 Plan 확정 (코드 미수정)
  - 문서: `docs/01-plan/features/bugfix.plan.md` (r2 보존 + r3 확장 병합)
  - 이슈: (1) 일본어 게임명 CTA 침범 (2) 게임명↔부제 간격 2px 과소 (3) 배치 기본 규격 (4) 배치 기본 언어 (5) 프리셋 저장 기능 부재
  - 결정: Item1 **A안 (일본어 0.85배 고정)** · Item2 **전 사이즈 공통 4px** · Item3 `1:1+1200x628` · Item4 4개 언어 전체 · Item5 **β안** (title/subtitle/cta/disclaimer) + **I안** (`prompt()`) + **X안** (`confirm()` 덮어쓰기)
  - 추가 명세: FR-14~25, SC-11~20, R-09~13, NFR-07~09
  - 수정 대상: `today-banner-designer.html` 1개 파일 · 신규 함수 8개(프리셋) + 1개(getTitleScaleByLang)
- 2026-04-22: **[PDCA Do] bugfix (r3)** — 일괄 구현 완료
  - CSS: `.darkbar-text { gap: 4px }` (FR-16) · `.banner[data-lang="ja"]` title/subtitle 6 rule 추가 (FR-14, 42→36/24→20, 56→48/32→27, 30→26/17→14)
  - HTML 배치 체크박스: 9:16 unchecked → 1200x628 checked (FR-18) · ja/zh-TW 모두 checked (FR-19)
  - HTML 단건: 샘플 프리셋 아래 `내 프리셋` 영역 + `#s-save-preset` 버튼 (FR-21/22) · 다운로드 버튼 바로 위 배치
  - HTML 배치: `#b-preset`에 `<optgroup label="샘플">`/`<optgroup id="b-custom-preset-optgroup">` 분리 + `#b-delete-preset` 🗑 버튼 (FR-22) · 프리뷰 바로 위 `#b-save-preset` 버튼 (FR-21)
  - JS 신규: `getTitleScaleByLang(lang)` (FR-15) · `CP_KEY`, `CP_LANGS` 상수 · `getCustomPresets`/`saveCustomPresets` try-catch 방어 (FR-20/25) · `makePresetDataFromSingle`/`FromBatch`/`emptyLangSlot` · `savePresetFlow(source)` (prompt → 중복 체크 confirm → localStorage 쓰기, FR-21/23) · `deletePresetById(id)` confirm (FR-23) · `applyCustomPresetToSingle`/`ToBatch` (FR-24) · `renderPresetListUI()` 단건 그리드 + 배치 optgroup 동시 렌더
  - JS Canvas 수정: `buildBannerCanvas` 내 `titleFS = Math.round(spec.title.fontSize * titleScale)`, `subFS = Math.round(spec.subtitle.fontSize * titleScale)`, `lineGap = 4` (FR-15/17)
  - JS 이벤트: `bindSingleMode`에 `#s-save-preset` click → `savePresetFlow('single')` · `bindBatchMode`에 `#b-save-preset` click → `savePresetFlow('batch')` + `#b-delete-preset` click → `deletePresetById` · `applyBatchPreset` 확장 (`custom:<id>` 분기 추가, 샘플 프리셋 경로 보존, FR-24)
  - JS 초기화: `DOMContentLoaded`에 `renderPresetListUI()` 호출 추가
  - `state.batch.sizes: ['1x1', '1200x628']` · `state.batch.langs: ['ko', 'en', 'ja', 'zh-TW']` (FR-18/19)
  - 정적 검증: 34개 FR/NFR 마커 중 33개 정규식 일치 (1개는 메시지 문구 표현 차이로 false negative, 실제 코드 정상)
  - 상태: 코드 구현 완료. 사용자 브라우저 실측 + `/pdca analyze bugfix` Gap 분석 대기
- 2026-04-22: **[PDCA Check] bugfix (r3)** — Gap 분석 완료 (브라우저 실측 전, 정적 대조만)
  - 문서: `docs/03-analysis/bugfix.analysis.md` (기존 r2 100% 분석 보존 + r3 섹션 9~16 추가 병합)
  - r3 FR Match Rate: **12/12 = 100%** (FR-14~25 모두 정적 증거 라인 번호 확보)
  - r3 SC 평가: **7 Met + 3 Partial "Code-Ready"** (실측 전 보수적 평가) — SC-11 일본어 overflow 육안 / SC-13 gap 체감 주관 / SC-17 프리셋 저장→복원 end-to-end가 실측 필요 항목
  - Decision Record 준수: Q1 A안(고정 0.85배) / Q2 공통 4px / Q3 β안(4필드) / Q4 I+X안(prompt + confirm) **4건 모두 충실 반영**
  - Critical/Important/Minor Gap: **0건** (정적 기준)
  - 회귀 체크: r2 FR-01~13 모두 무영향 (title/subtitle 영역만 수정, 11단계 Canvas 합성 구조 보존)
  - 통합 Match Rate: r2 100% 실측 확인 + r3 100% 정적 = **25/25 FR Met + 17/20 SC 확정 + 3 실측 대기**
  - 상태: 사용자 브라우저 실측 후 `/pdca report bugfix` 작성 권장 (r2+r3 통합 리포트)
- 2026-04-22: **[Review] 코드 리뷰 & 분석 (읽기 전용)** — 버그·엣지 케이스 15건 도출
  - 문서: `~/.claude/plans/claude-enchanted-giraffe.md`
  - Critical 1건(B-01 배치 프리셋 적용 실패) · High 2건(B-02 Canvas 텍스트 CTA 침범, B-03 slugify CJK 소실) · Medium 5건 · Low 6건 · Info 1건
  - 사용자 실측으로 B-01 재현 확인 → 최소 스코프 수정 착수
- 2026-04-22: **[bugfix r4] B-01 Critical 수정 완료 (실측 OK)** — `applyCustomPresetToBatch`에 DOM input 직접 갱신 블록 추가 (9줄). 배치 프리셋 적용 end-to-end 정상화 **브라우저 실측 확인**. 다른 코드는 미변경. 남은 B-02~B-15는 후속 트랙 대기.

## 히스토리

_(에러·이슈 발생 시 날짜·요약·대응 기록)_

- 2026-04-22: **[B-01] 배치 프리셋 적용 미반영 (Critical)**
  - 원인: `renderBatchLangFields`가 `existing`(현 DOM 값) 스냅샷을 우선하여 `state.batch.langOverrides` 무시 → `applyCustomPresetToBatch`가 state만 수정하고 DOM 미갱신 상태에서 재렌더 호출 시 프리셋 값 누락. status message만 "적용됨" 표시되는 silent failure.
  - 대응: `applyCustomPresetToBatch` 내부 CP_LANGS forEach에 DOM input 직접 쓰기 블록 추가. 재렌더 시 existing 스냅샷이 방금 쓴 프리셋 값을 담도록 함. `renderBatchLangFields` 로직은 회귀 회피 위해 미변경.
