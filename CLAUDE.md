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

## 정책 (모든 신규 템플릿에 적용 — v1.5+)

- **Single 모드 + Batch 모드 양쪽 지원 의무**: 모든 신규 템플릿은 단건 export(현재 화면 1장)와 배치 export(언어/사이즈/테마 조합 ZIP) 둘 다 제공해야 한다. 이는 다국어 UA 운영 워크플로우 요구사항이며, 새 템플릿 PR은 양쪽 동작을 검증해야 한다.
- **다국어 4종 기본**: ko / en / ja / zh-TW 4개 언어 LANG_PACK 확장이 디폴트. 일부 템플릿이 별도 LANG_PACK(예: AS_LANG_PACK)을 둘 수 있으나, 동일한 4언어 키를 사용한다.
- **언어별 폰트 자동 스왑**: Pretendard(ko/en) / Noto Sans JP(ja) / Noto Sans TC(zh-TW). `data-lang` 속성 + CSS 셀렉터 + Canvas의 `getFontFamilyForLang/asFontFamily`로 일관 적용.
- **사용자 결정 (2026-04-25, v1.5 App Store Screenshot 기준)**:
  - 자동 번역 도입 안 함 → 4언어 직접 입력
  - 픽셀 퍼펙트 모방 → 외관은 실 App Store 페이지 충실 재현
  - 테마는 디자인 1개당 1테마 (다크 또는 라이트 단일 선택) — Batch ZIP은 4언어 × 1테마 = 4장
  - 키아트는 4언어 공용 (1장 업로드)
  - 디바이스 프레임(베젤) 미포함 → App Store 페이지 자체만 9:16 채움
  - 한국 등급/이벤트 같은 로케일 전용 컬럼은 통일 (4컬럼 유지)

---

## 프로젝트 개요

- **이름**: Today Banner Designer (v1.2)
- **유형**: 단일 HTML 사내 툴 (Apple "Today" 스타일 광고 배너 자동 생성)
- **본체**: `today-banner-designer.html`
- **문서**: `README.md`
- **담당**: UA Manager 김성권 (ksk@superplanet.net)
- **원격 repo**: https://github.com/sungkk1m/mkt_bannerdesigner (main branch, HTTPS/OAuth 인증)

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
- 2026-04-23: **GitHub 원격 등록 완료** — `origin/main` upstream 설정. 초기 커밋 `289a68c`에 v1.2 본체 + PDCA r1~r4 + Review 15건 포함 (8 files, 3638 insertions). `.bkit/`·`.claude/settings.local.json`은 `.gitignore`로 제외. 인증은 Git Credential Manager OAuth device flow로 자동 처리됨.
- 2026-04-24: **[App Badge v1.4 r5] 헤드라인 영역 오버플로우 클리핑 예외처리**
  - 잠재적 클리핑 3곳 모두 해제:
    1. `.ab-headline` 공통: `overflow: visible` 명시 (기본값이지만 안전장치)
    2. `.size-1x1 .ab-headline`: `height: 95px; display: flex; align-items/justify-content: center` 제거 → `top: 287.5px + transform: translateY(-50%)` (텍스트 높이가 95를 넘어도 상·하 양방향으로 자연 확장)
    3. `.banner.tmpl-app-badge`: `overflow: hidden` → `overflow: visible` (DOM 프리뷰에서 banner 경계 밖 텍스트/그림자 표시 허용. 배경 이미지는 자체 `object-fit: cover + inset: 0`으로 bounded)
  - Canvas `buildAppBadgeCanvas` 헤드라인 verticalCenter 로직: `Math.max(0, (boxH - blockH) / 2)` → `(boxH - blockH) / 2` (음수 허용 = DOM translateY(-50%) 동작과 정확히 일치, boxH 초과 시 위로도 확장)
  - 영향 범위: 1:1 사이즈만 CSS 변경, 9:16 / 1200×628은 기존 layout 보존. Canvas 변경은 모든 사이즈 공통이나 verticalCenter 플래그가 1:1에만 있어 실질적으로 1:1만 영향
  - 문법 검증: `node --check` 통과
- 2026-04-24: **[App Badge v1.4 r4] 1:1 뱃지 그룹 명시적 중앙정렬 + Drop Shadow inner→outer 확정**
  - 뱃지 그룹: `.size-1x1 .ab-badges` `left:50%+translateX(-50%)`(shrink-to-content + 중앙 이동) → `left:0; right:0; width:100%; justify-content:center` 로 전환 (flex 컨테이너 전체 너비 + 명시적 중앙정렬). `flex-shrink:0` 추가해 이미지 의도치 않은 축소 방지
  - Drop Shadow 이슈 원인: `background-clip:text` + `color:transparent` 조합에서 `text-shadow`가 일부 브라우저에서 글리프 내부로 클리핑 → **inner-shadow 같은 시각 효과**
  - 수정 (DOM): `.fx-drop-shadow .ab-headline` `text-shadow` → **`filter: drop-shadow(0 8px 16px rgba(0,0,0,0.7))`** 요소 렌더 후 외부 projection이라 그라데이션과 무관하게 outer 보장
  - 수정 (로고): `filter: drop-shadow` 값 `0 6px 14px/.55` → `0 10px 20px/.7` 강화
  - 수정 (Canvas): `HEADLINE_FX['drop-shadow'].shadow` color/blur/offsetY `rgba(.55)/24/12` → `rgba(.7)/32/16` 강화 (Canvas는 원래 outer지만 프리뷰와 시각 균일 맞춤)
  - 문법 검증: `node --check` 통과
- 2026-04-24: **[App Badge v1.4 r3] 1:1 뱃지 aspect 보존 + 실제 40px gap**
  - 원인 진단: 기존 1:1 뱃지가 고정 354×100 박스에 강제 렌더 → SVG 원본(appstore 3.231:1=323w, googleplay 3.375:1=338w)이 가로 +9~10% stretch · CSS flex-gap 40은 박스 기준이라 실제 뱃지 사이 시각적 공백이 31~62px로 불규칙
  - 수정 1 (CSS `.size-1x1 .ab-badges img`): `width:354 height:100` → `height:100 width:auto` + 컨테이너 `align-items:center` (뱃지 원본 비율 보존, flex gap 40이 실제 뱃지 엣지 간 거리로 작동)
  - 수정 2 (Canvas `APP_BADGE_CANVAS_SPECS['1x1'].badges`): `fitByHeight:true` 플래그 추가 · `buildAppBadgeCanvas` 뱃지 렌더 분기에서 fitByHeight일 때 각 이미지 `naturalWidth/naturalHeight`로 w 계산 → `totalW = gpW + asW + gap`으로 centerX 기준 startX 재계산 → 실제 40px 간격 보장
  - 9:16 / 1200×628은 기존 고정 w 유지 (1:1만 변경)
  - 문법 검증: `node --check` 통과
- 2026-04-24: **[App Badge v1.4 r2] 1:1 헤드라인 fontSize 110 + 한국어 사전예약 뱃지 교체**
  - 1:1 headline fontSize 72 → **110** (CSS + Canvas 동기) · boxH=95 유지 (verticalCenter 로직으로 overflow 시에도 시각적 balance 유지)
  - 하단 뱃지 중앙 정렬 + gap 40 (기존 값 재확인, 변경 없음)
  - 한국어 사전예약 뱃지 교체: `BADGE_ASSETS.appStore.preregister.ko` · `BADGE_ASSETS.googlePlay.preregister.ko` 를 사용자 제공 SVG 2종 (`~/Downloads/ko_appstore_pre.svg` / `ko_googleplay_pre.svg`) 의 base64 data URI로 덮어쓰기 (두 파일 모두 svg+xml 타입 통일)
  - 교체 라인: L1295 (appStore) · L1309 (googlePlay) — 공백·trailing comma 보존 정규식 기반 in-place 치환
  - 문법 검증: `node --check` 통과
- 2026-04-24: **[App Badge v1.4] 1:1 사용자 지정 그리드 + 신규 시각 효과 3종**
  - 1:1 그리드 (top→bot): margin 40 / logo 160h / gap 40 / text 95 / gap 40 / icon 515×515 / gap 50 / badge 100h (gap 40) / margin 40
  - 아이콘 좌표: left=282 (1080-515)/2 · badge w=354 h=100 · logo maxH=160 maxW=900 · headline fontSize 72 (vertical-center in 95h box)
  - CSS+Canvas 동기 수정 (`.size-1x1`, `APP_BADGE_CANVAS_SPECS['1x1']`), Canvas에 `verticalCenter`+`boxH` 신규 필드 + 계산 로직 추가
  - 신규 효과 1: **앱 아이콘 Outglow** — `iconGlowColor` + `iconGlowEnabled`, CSS `has-icon-glow` 토글 클래스 + box-shadow 2중, Canvas는 아이콘 clip 전에 컬러 레이어 2회 stacked fill로 재현
  - 신규 효과 2: **헤드라인 그라데이션** — `headlineGradColor` + `headlineGradEnabled`, CSS `has-head-grad` + `-webkit-background-clip: text`, Canvas는 라인별 `createLinearGradient(y, y+fs)` 흰색→지정컬러
  - 신규 효과 3: **로고 Drop Shadow** — 모든 사이즈 공통, CSS `filter: drop-shadow(0 6px 14px rgba(0,0,0,.55))` + Canvas `shadowColor/Blur/OffsetY` drawImage 시 적용
  - UI: 단건·배치 양쪽에 체크박스 + 컬러 피커 2쌍 (헤드라인 그라데이션 / 아이콘 outglow)
  - 수정 파일: `today-banner-designer.html` 1개 · state 필드 8개 신규 (single.app_badge × 4 + batch × 4) · 이벤트 핸들러 8개 신규
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
- 2026-04-23: **[App Badge v1.3] 신규 템플릿 "App Badge & Icon" 추가 + r3a~r3h 레이아웃 이터레이션** — 헤더 드롭다운으로 Today Tap ↔ App Badge 전환. 3사이즈(1:1 / 9:16 / 1200×628) × 4언어(ko/en/ja/zh-TW) × 2상태(download / preregister) 지원. 공식 스토어 뱃지 16개 base64 인라인(Apple 8 SVG + Google 8 PNG). 주요 상수/함수: `BADGE_ASSETS`, `APP_BADGE_CANVAS_SPECS`, `HEADLINE_PRESETS` + `HEADLINE_PRESETS_1200`(1200×628 전용 2줄 버전), `HEADLINE_FX`(4종 효과), `buildAppBadgeBanner`(DOM) · `buildAppBadgeCanvas`(Canvas). 레이아웃 이터레이션: **r3a** 사이즈별 기본 / **r3b** 1:1 아이콘 550 + 뱃지 중앙 / **r3c** 1200×628 2줄 헤드라인 도입 / **r3d** 로고 텍스트영역 중심 / **r3e** 헤드라인·로고 가운데 정렬(중심 x=338, 뱃지 2종 중점) + 첫줄 0.72× / **r3f** JA+download 전용 line2 축소(108px, firstLineScale 0.87) — `data-preset` 속성 + Canvas `overrides['download:ja']` / **r3g** 로고 상향(maxH 175) / **r3h** 로고 `bottomY` 앵커로 전환(가로비율 다른 로고라도 헤드라인과 일정 간격 유지). `.gitignore`에 `Apple badge/` · `Google badge/` · `_inject_badges.py` 추가(원본 에셋·일회성 스크립트 커밋 제외). 뱃지 스트레치 진단: `drawImage` 5-인자가 박스에 강제 맞춤 → JA 뱃지 원본 2.72:1이 박스 3.57:1에서 +31% 늘어남. 수정은 사용자 선택 대기.
- 2026-04-23: **[Code Review] 전체 품질 리뷰 완료** — `today-banner-designer.html` 3291라인 · 374KB 기준. Critical 0건 · Major 4건(M-1 CDN SRI 미적용 / M-2 `_imgCache` 무제한 누적 / M-3 slugify CJK 소실(기존 B-03) / M-4 스토어 뱃지 Canvas 스트레치) · Minor 7건 · Info 3건. Score 78/100. 긍정: XSS 방어(escapeHTML 일관), 에러 경계, localStorage 방어, 폰트 사전로드, 이미지 캐시 최적화 모두 충실.
- 2026-04-23: **[M-4 수정 완료 — 실측 OK]** `today-banner-designer.html` Canvas 뱃지 스트레치 해소. **변경**: `drawImageCover` 옆에 `drawImageContain(ctx, img, x, y, w, h)` 헬퍼 신규 추가 (`naturalWidth/Height` → `Math.min(w/iw, h/ih)` → 중앙 정렬 `drawImage`). `buildAppBadgeCanvas` [7] 섹션의 Google Play·App Store 뱃지 `ctx.drawImage` 5-인자 호출 2곳을 `drawImageContain`으로 교체. **효과**: JA +31% / KO +10% 스트레치 → **0%**. DOM `object-fit: contain` 프리뷰와 다운로드 PNG 100% 일치. 실측 확인 조합: 1200×628 + JA·ZH-TW, 1:1 + ZH-TW (캡처 3장 — 뱃지 문자·사과 아이콘 원형 유지 확인). 박스 치수·주변 좌표 불변이라 회귀 0. 권장 `drawImageContain`을 택함(Option 1). M-1~M-3은 후속 트랙 대기.
- 2026-04-23: **[M-2 수정 완료 — 실측 OK]** `_imgCache` 메모리 누수 해소 (Option A: 정밀 무효화). **변경**: `_imgCache` 정의 직후 `updateStateImage(stateObj, prop, newDataURL)` 헬퍼 신규 추가 (이전 dataURL이 있으면 `_imgCache.delete(prev)` 후 state 갱신). 이미지 state를 바꾸는 7개 드롭존 콜백(`s-drop-keyart/overflow/icon`, `b-drop-keyart/overflow/icon/logo`)의 `state.xxx.yyy = dataURL` 호출을 `updateStateImage(state.xxx, 'yyy', dataURL)`로 일괄 교체. **효과**: 드롭존 교체 시마다 이전 dataURL의 Map key(base64 문자열) + 디코딩 Image가 즉시 회수됨. 사용자 실측: 키아트 A→B→C 연속 교체해도 `_imgCache.size`가 **1로 유지** 확인(기존엔 3으로 증가했을 것). 🗑 제거 경로도 자동 커버(`onFile(null)` → `updateStateImage(..., null)`). 배치 ZIP 12장 성능(캐시 히트 기반 1회 decode) 불변. 변경량 +19/-7 라인. M-1·M-3은 후속 트랙 대기.
- 2026-04-25: **[App Store Screenshot v1.5] 신규 3번째 템플릿 "App Store Screenshot" 추가 (픽셀 퍼펙트 iOS App Store 모방, 9:16 1080×1920 전용)**
  - 헤더 드롭다운 추가: `Today Tap` / `App Badge & Icon` / **`App Store Screenshot`** (TEMPLATE_KEYS 3개로 확장)
  - 8개 섹션 레이아웃 (DOM + Canvas 동기): 상태바(고정 9:41/신호/Wi-Fi/배터리) → 헤더(뒤로+검색) → 앱 정보(아이콘 220×220 r50 + 타이틀+카테고리+Get+IAP) → 통계 4컬럼(평점·연령·랭킹·개발자, ★별점 SVG) → 키아트 카드(16:9 r28) → 디바이스 라벨(iPhone+iPad 아이콘+chevron) → 설명 본문(4줄 클램프 + more 링크) → 하단 탭바(5개: Today/Games/Apps/Arcade/Search)
  - 다크/라이트 테마 (per-design 단일 테마): `data-theme="dark|light"` + `--as-*` CSS 변수 11종 + JS `AS_THEMES{dark,light}` 팔레트 (CSS와 동일 hex)
  - 4언어 고정 라벨 새 LANG_PACK: `AS_LANG_PACK[ko|en|ja|zh-TW]` (search/get/iap/more/4통계헤더/연령접미사/deviceLabel/탭5개)
  - 4언어 가변 텍스트 (사용자 직접 입력, 자동 번역 X): 타이틀/카테고리/설명/평점/리뷰수/랭킹/개발자 — 단건은 현재 언어 슬롯 표시, 배치는 4언어 전체 입력란 자동 렌더
  - 표시/숨김 토글 4종 (전 언어 공통): 통계 영역 / 하단 탭바 / Get 버튼 / IAP 라벨 (CSS `.hide-stats|tabbar|cta|iap` + cta+iap 양쪽 OFF면 cta-row 자동 collapse)
  - 키아트 1장 공용 (4언어 동일 이미지, `state.batch.keyart` 재사용)
  - SVG 아이콘 18종 (canvas용 inner path + `__C__` 토큰 치환): 신호 4바/Wi-Fi/배터리/back chevron/별3종(F/H/E)/ranking/developer/iPhone/iPad/chevronDown/탭5개. `buildAsIconUrl(key, color)` → data:URL → `loadCachedImage` 캐시 활용
  - Single 모드 export 분기: `handleSingleDownload` → `buildAppStoreScreenshotCfg` → `prepAppStoreCfgImages` → `buildAppStoreScreenshotCanvas` → `canvasToDataURL` → `buildAppStoreFilename` (`{prefix}_appstore_{lang}_{theme}_1080x1920.{ext}`)
  - Batch 모드 export 분기: `buildBatchCfgs` → `appstore-screenshot` 분기 (size 항상 9x16) → `handleBatchExportZip` 루프 → 4언어 × 1테마 = 4장 ZIP
  - 9:16 자동 잠금: `applyTemplateSwitch`에서 `appstore-screenshot` 선택 시 `#s-size` disabled + 배치 사이즈 체크박스 9:16만 체크/나머지 disabled
  - `data-tmpl-hide` 속성 신규 (역방향 토글): 고지문구 input은 appstore-screenshot 모드에서 자동 숨김
  - 신규 함수: `buildAppStoreScreenshotBanner`(DOM) · `buildAppStoreScreenshotCanvas`(Canvas) · `prepAppStoreCfgImages` · `buildAppStoreScreenshotCfg` · `buildAppStoreFilename` · `buildAsIconUrl` · `asFontFamily` · `asWrapText`(CJK 친화 줄바꿈, 4줄 클램프) · `syncSingleAppStoreFromUI` · `loadAppStoreSlotToUI`
  - 신규 상수: `AS_LANG_PACK` · `AS_THEMES{dark,light}` · `AS_ICON_DEFS{18종}` · `AS_SVG{18종 wrapper}` · `APPSTORE_SCREENSHOT_DEFAULT`(theme + 4토글 + langs[ko|en|ja|zh-TW] 슬롯)
  - state 확장: `state.single.appstore = APPSTORE_SCREENSHOT_DEFAULT 깊은 복사` · `state.batch.{as_theme, as_showStats, as_showTabbar, as_showCta, as_showIap}` · `state.batch.langOverrides[lang].{as_title, as_subtitle, as_description, as_rating, as_ratingCount, as_ranking, as_developer}` (기존 langOverrides에 통합)
  - HTML 컨트롤 패널 신규: 단건(`data-tmpl="appstore-screenshot"` 블록 1개, 테마+규격(고정)+가변텍스트3+통계4+토글4) · 배치(공통 설정 블록 + `renderBatchLangFields` appstore 분기 4×7필드)
  - 정책 추가 (CLAUDE.md): "모든 신규 템플릿은 Single+Batch 양쪽 지원 의무" + "다국어 4종 기본" + "테마 1개/디자인" + "키아트 4언어 공용" + "픽셀 퍼펙트 모방"
  - PDCA Plan 문서: `docs/01-plan/features/appstore-screenshot.plan.md` (FR-1~11, NFR-1~4, SC-1~6, R-1~3 + 미해결 v2 후보 5건)
  - 변경량: `today-banner-designer.html` 3,881 → 5,097라인 (+1,216) · 387KB → 추정 462KB
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과 (5단계 모두)
  - 상태: 코드 구현 완료. 사용자 브라우저 실측 + 시각 비교(첨부 4스샷 vs 출력) 후 `/pdca analyze appstore-screenshot` Gap 분석 대기
- 2026-04-29~30: **[SD Showcase v1.6] 신규 4번째 템플릿 — 6 SD + 4언어 + 2사이즈 (1080×1080 + 1200×628), 8장 ZIP 자동 생성 PDCA 완주**
  - 워크플로우: `/plan-plus` (14+1 결정) → `/pdca plan` → `/pdca do` × 4 sessions → `/pdca analyze` (r0~r4) → `/pdca report`
  - 4 sessions: data-switch / canvas-renderer / single-ui / batch-ui-zip
  - 4 iterations: r1(G1+G2 해소) → r2(N1~N4) → r3(N5~N7) → r4(강정아 스펙 N8~N10)
  - **Match Rate: r0 88% → r1 96% → r4 100%**. Critical/Important/Minor Gap 0건
  - **Plan SC: 8/8 + 신규 N: 10/10 = 18/18 충족 (100%)**, Decisions Followed 23/23 (100%)
  - **변경량**: `today-banner-designer.html` 5,097 → 6,105라인 (+1,008) · 단일 HTML 정책 유지
  - **신규 함수 12개**: `getLuminance`, `getContrastPalette`, `updateStateImageAt`, `buildSdShowcaseCfg`, `prepSdShowcaseCfgImages`, `buildSdShowcaseCanvas`, `buildSdShowcaseBanner`, `buildSdShowcaseFilename`, `fitSdsTitle`, `sdsWrapText`, `drawSdsTitleLines`, `drawSdsPill`
  - **핵심 기능**:
    - SD 6장 슬롯 (3×2 그리드 1080 / 좌·우 사이드 컬럼 1200)
    - 4언어 타이틀 + 픽 자동 입력, KO 양 사이즈 "확률형 아이템 포함" 자동 첨부
    - 자동 폰트 축소 (긴 영문 처리), CJK char-wrap / Latin word-wrap (\n 우선)
    - 자동 대비 (휘도 이진 + hysteresis 0.46~0.54)
    - 1200×628 우측 SD 자동 좌우반전 (`ctx.scale(-1,1)`)
    - 픽 직각 + 흰 stroke 4px + drop shadow + TOP 앵커
    - 타이틀 drop shadow (slider와 비례 스케일링)
    - 검정 배너 테두리 **고정** (선 굵기 10px / 가장자리에서 선 중심까지 9px, 강정아 스펙)
    - SD 셀 크기 슬라이더 (50~150%) + SD 사이 간격 슬라이더 (0~80px)
    - 배경 컬러피커 + 자동 대비
  - **취소된 결정**: NEXON Kart Gothic / Shin Go Pro / OPPOSans 폰트 적용 시도 (사용자 변심으로 즉시 원상복구, 잔재 0건) · 이미지 그리드 270×300 고정 (사용자 취소)
  - 문서: `docs/01-plan/features/sd-showcase.plan.md` · `docs/03-analysis/sd-showcase.analysis.md` (v0.3, 16 sections) · `docs/04-report/sd-showcase.report.md` (v1.0)

## 히스토리

_(에러·이슈 발생 시 날짜·요약·대응 기록)_

- 2026-04-22: **[B-01] 배치 프리셋 적용 미반영 (Critical)**
  - 원인: `renderBatchLangFields`가 `existing`(현 DOM 값) 스냅샷을 우선하여 `state.batch.langOverrides` 무시 → `applyCustomPresetToBatch`가 state만 수정하고 DOM 미갱신 상태에서 재렌더 호출 시 프리셋 값 누락. status message만 "적용됨" 표시되는 silent failure.
  - 대응: `applyCustomPresetToBatch` 내부 CP_LANGS forEach에 DOM input 직접 쓰기 블록 추가. 재렌더 시 existing 스냅샷이 방금 쓴 프리셋 값을 담도록 함. `renderBatchLangFields` 로직은 회귀 회피 위해 미변경.
