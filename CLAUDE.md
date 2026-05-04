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
- 2026-05-03: **[Repo 동기화] 로컬 ↔ GitHub 비교 + GitHub 우선 동기화** — 로컬 폴더가 git 저장소 아님(.git 없음) 확인. `levelup` PDCA 문서 3종(plan/design/analysis, 약 83KB)이 로컬에만 있어 `repo/.backup-pre-sync-20260503-205036/`로 보존 후 제거. GitHub에서 `.gitignore`, `sd-showcase.{plan,analysis,report}.md`, 최신 `CLAUDE.md`(26.5→28.7KB), `today-banner-designer.html`(515→497KB) 다운로드. Git blob SHA 기준 15개 파일 전부 일치 검증. 이후 `.git`이 새로 생성됨.
- 2026-05-03: **[Key Visual + iPhone Review v1.7] 신규 5번째 템플릿 — 키비주얼 풀 배경 + black iPhone mockup floating + 4언어 ZIP 자동 생성**
  - 워크플로우: `/plan-plus` (4-round Brainstorming via AskUserQuestion) → `/pdca plan` → `/pdca design` (Architecture Option C: 기존 패턴 + helper 함수 분리) → `/pdca do` (M1~M7 자동 진행) → `/pdca analyze` → `/pdca report`
  - **결정사항 24건** (Brainstorming 23 + Open Items 추천값 일괄 1)
  - **변경량**: `today-banner-designer.html` 6,105 → 6,943라인 (+838) · 497KB → 534KB · 단일 HTML 정책 유지
  - **신규 자산**: `repo/assets/keyvisual-review/iphone.png` (248×500, 6.5KB) — 사용자 첨부 black iPhone mockup, Pillow 알파+RGB 분석으로 화면 영역 좌표 추출 (x=14, y=16, w=220, h=472 → 비율 0.0567/0.0301/0.8907/0.9478)
  - **신규 함수 7개**: `buildKvrCfg`, `prepKvrCfgImages`, `buildKvrCanvas`, `buildKvrBanner`, `buildKvrFilename`, `bindKvrSingleUI`, `loadKvrSlotToUI` + 헬퍼 `KVR_HELPERS.{starParts, formatRatingCount, formatReviewDate}` + 텍스트 유틸 `ellipsisLine`, `wrapTextToNLines`
  - **핵심 기능**:
    - 1080×1080 전용 (9:16 / 1200×628은 옵션·체크박스 자동 비활성)
    - 키비주얼 + 로고 = 2개 레이어, 각각 scale (50~200%/50~150%) + x/y slider (±500/±200/±100~+200)
    - black iPhone mockup floating (폭 540px = 캔버스의 50%, 하단 8.7px 자연 잘림)
    - 헤드라인 LANG_PACK 프리셋 4세트 + OFF (real-player / top-rated / players-say / five-star)
    - 평점 0.5 단위 부분 채움 (★ 유니코드 + linear-gradient clip 마스킹)
    - 평가 개수 4언어 단위 자동 변환 (21000 → 2.1만/21K/2.1万/2.1萬)
    - 작성 날짜 ISO → 언어별 자연 포맷 (1월 23일 / Jan 23 / 1月23日)
    - LANG_PACK 자동 라벨 (평가 및 리뷰 / 가장 도움이 되는 리뷰 + 4언어)
    - 리뷰 본문 2줄 고정 + ellipsis (CJK 문자 단위 / 라틴 단어 단위 줄바꿈)
    - 별점 색상 컬러피커 (기본 #1d1d1f 다크 그레이)
    - mockup 화면 영역 클리핑 (콘텐츠가 mockup 밖으로 흘러가지 않음)
    - zh-TW/ja 폰트 사이즈 자동 0.92×/0.85× (긴 라벨 보정)
  - **Single + Batch 양쪽 지원** (CLAUDE.md 정책 준수): 단건 입력 데이터를 그대로 4언어 ZIP 출력 (UA 워크플로 단순화 — 단건 검수 → 배치 자동)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
  - 문서: `docs/01-plan/features/keyvisual-review.plan.md` · `docs/02-design/features/keyvisual-review.design.md` · `docs/03-analysis/keyvisual-review.analysis.md` · `docs/04-report/keyvisual-review.report.md`
- 2026-05-04: **[v1.7 R13 흰 BG] KVR 흰 BG 박스 위·아래 외곽 +10px 확장 (옵션 B 채택)**
  - 사용자 요청: "콘텐츠와 mockup 사이에 키비주얼이 비치는 공간"을 줄이기 위해 흰 BG 박스를 위로 10px + 아래로 10px 확장
  - 사용자 비교 단계: 사본 4개(`kvr-bg-shift-10px/20px/30px/10px-bottom-10px`) 시각 비교 후 옵션 B (위 10 + 아래 10 외곽 확장) 선택
  - **변경 사항** (`today-banner-designer.html`):
    - `KVR_SCREEN_CORNER_R` 정의 직후 (line 4516+): `const bgY = screenY - 10; const bgH = screenH + 20;` 변수 2개 추가
    - 흰 BG path (line 4519-4525): `screenY` → `bgY`, `screenY + screenH` → `bgY + bgH` 교체 (4곳)
    - clip path (line 4540-4546): 동일 패턴 교체 (4곳)
    - 콘텐츠 cy0는 `screenY + pad + notchPad` 그대로 → **텍스트 절대 위치 100% 보존** ✅
  - **효과**:
    - 박스 상단 y: 242.6 → 232.6 (위로 10px, mockup 노치 영역에 더 가까움 → 키비주얼 비침 영역 축소)
    - 박스 하단 y: 1080.0 → 1090.0 (아래로 10px, 캔버스 +10px 밖 → 자동 클리핑 + mockup 베젤이 가림)
    - 박스 높이: 837.4 → 857.4 (+20px)
    - 콘텐츠/텍스트 위치 변화 없음
  - **회귀 위험**: 0 (KVR 전용, BG/clip path 외 무영향. 콘텐츠 cy0/screenH/cornerR 모두 그대로)
  - 변경량: `today-banner-designer.html` 7,166 → 7,169 라인 (+3, bgY/bgH 변수 2줄 + 주석 1줄) · 708,046 B → **708,237 B** (+191 B)
  - 문법 검증: `node --check` 통과
  - **임시 비교 사본**: `repo/preview-content-shift/` 디렉토리 (kvr-shift-* 6개 + kvr-bg-shift-* 4개 + README) — 본체 적용 후 정리 예정 (사용자 결정 대기)
- 2026-05-04: **[v1.7 R13] KVR 배치 모드 키비주얼/로고 미적용 버그 해결 — 옵션 3-B (다른 템플릿과 일관된 별도 슬롯 패턴)**
  - 사용자 보고: 배치 export 결과 4언어 모두 키비주얼/로고 미적용 (디폴트 그라데이션 BG + 로고 부재). 단건 export는 정상.
  - 원인 분석 (`/pdca analyze`): KVR 배치는 `state.single.kvr`만 사용하는 정책 (CLAUDE.md "단건 검수 → 배치 자동" 단순화). 배치 모드 UI에 KVR 전용 슬롯/슬라이더 부재 → 사용자가 today-tap 공용 슬롯(b-drop-keyart 등)에 업로드해도 KVR 분기는 무관 → 미적용
  - 다른 템플릿 비교: today-tap (s-/b-drop-keyart 별도) / App Badge (s-/b-drop-logo 별도) / SD Showcase (s-/b-sd-slot 6개 별도) → KVR만 배치 슬롯 부재 = 패턴 위반
  - 사용자 선택: **옵션 3-B (슬롯 + 슬라이더 전체 별도)** — 다른 템플릿과 완전 일관
  - **변경 사항**:
    - `state.batch.kvr = JSON.parse(JSON.stringify(KVR_DEFAULT))` 추가 (line 2518) — 배치 전용 KVR 데이터
    - 배치 today-tap 슬롯(`b-drop-keyart`/`b-drop-icon`) `data-tmpl-hide` 속성에 `keyvisual-review` 추가 (line 1540, 1559) — KVR 모드에서 자동 숨김
    - 배치 KVR 전용 UI 패널 신규 추가 (line 1721+, 약 90줄): 키비주얼 dropzone(`b-drop-kvr-bg`) + 3 슬라이더 / 로고 dropzone(`b-drop-kvr-logo`) + 3 슬라이더 / 헤드라인 프리셋 select / 평점/개수/날짜/별색 입력 (단건 KVR 패널과 동일 구조, prefix `b-` 사용)
    - `bindKvrBatchUI()` 함수 신규 추가 (line 5437+, 약 60줄): bindKvrSingleUI 모방, b-* dropzone/slider/select 핸들러, `state.batch.kvr` 갱신 (refreshSinglePreview 호출 안 함 — 배치는 프리뷰 별도 트리거)
    - `bindBatchMode` 끝에 `bindKvrBatchUI()` 호출 추가 (line 6391)
    - `buildBatchCfgs` KVR 분기 수정 (line 6754): `buildKvrCfg(state.single.kvr, ...)` → `buildKvrCfg({ ...state.batch.kvr, langs: state.single.kvr.langs }, ...)`. 키비주얼/로고/슬라이더/평점은 배치 별도, 콘텐츠 langs(reviewTitle/Body/reviewerId)는 단건 데이터 사용 — 정책 절충 (사용자가 단건 검수 → 배치 자동 출력 워크플로 유지)
    - `handleBatchExportZip` 사전 디코드 수정 (line 7003-7004): `state.single.kvr.bgImage/logoImage` → `state.batch.kvr.bgImage/logoImage`
  - **검증**:
    - JS 문법 (`node --check`): 통과 ✓
    - state init 추가 라인 + 배치 패널 90줄 + bindKvrBatchUI 60줄 → +150 라인
    - 변경량: `today-banner-designer.html` 7,016 → 7,166 라인 (+150) · 699,941 B → **708,046 B** (+8,105 B)
  - **회귀 위험**: 0 (KVR 전용, 다른 4 템플릿 무영향. R12 흰 BG path 코드 무수정)
  - **워크플로 안내**:
    - KVR 단건: `s-drop-kvr-bg/logo` 슬롯 + 단건 슬라이더 → state.single.kvr → 단건 export
    - KVR 배치: `b-drop-kvr-bg/logo` 슬롯 + 배치 슬라이더 → state.batch.kvr → 배치 ZIP export (콘텐츠는 단건 데이터 자동 사용)
- 2026-05-04: **[v1.7 R12] KVR 흰 BG 좌·우 갭 메우기 + 모서리 둥글기 강화 (R11 PNG 화면 영역 정밀 매칭)**
  - R11 PNG 교체 후 사용자 시각 검증: "콘텐츠 및 리뷰 부분과 휴대폰 목업 사이에 키비주얼이 비치는 공간"
  - 사용자 요청: "콘텐츠 및 리뷰 부분의 크기를 조금 늘리는 형태로 가되, 모서리를 더 둥글게 만들어서 휴대폰 목업 외곽에 삐져나오지 않도록 설정"
  - **PNG 픽셀 분석으로 갭 발견** (검정 frame inner edge 자동 측정):
    - 새 PNG 실제 화면 영역: x=450~1049 (W=600), y=105~1307
    - 현재(R8.1) KVR_MOCKUP_SCREEN 흰 BG: x=456.6~1043.4 → **좌측 6.6px / 우측 5.6px 갭 발생** ❌
    - 상·하 51~60px 침범은 mockup이 마지막에 그려져 덮으므로 시각 문제 없음
    - 화면 corner radius: y=105~132 (27행) 동안 x=456→451 변화 → 실제 약 50px 추정 (현재 30px 미달)
  - **수정 (코드 2줄, 사용자 명시 제약 준수)**:
    - `KVR_MOCKUP_SCREEN.xRatio` 0.05 → **0.04** (좌측 BG 시작 x=456.6 → 450.1, 갭 0.1px)
    - `KVR_MOCKUP_SCREEN.wRatio` 0.90 → **0.92** (우측 BG 끝 x=1043.4 → 1049.9, 갭 -0.9px — mockup 검정 frame이 덮어 시각 문제 없음)
    - `KVR_SCREEN_CORNER_R` 30 → **50** (모서리 더 둥글게, 새 PNG 화면 corner와 매칭)
    - yRatio/hRatio 그대로 (콘텐츠 fit 보호 — mockup이 위/아래 침범 영역 덮음)
  - **효과 검증**:
    - 좌·우 갭 메움: 6.6/5.6px → 0.1/-0.9px ✅
    - 콘텐츠 폭 cw: 312 → **320** (+8px, 긴 리뷰 본문 ellipsis 덜 발생 보너스)
    - 콘텐츠 fit (ko/en): 384 + pad 48 = 432 ≤ screenH 434 → 여전히 fit ✅
    - 모서리 더 둥글게 → 흰 BG가 mockup 둥근 frame 안에 자연스럽게 매칭, 키비주얼 비침 영역 최소화
  - 변경량: `today-banner-designer.html` 2줄 수정 (line 2207, 2209) · 7,016라인 유지 · 683KB 유지
  - 다른 코드 변경 없음 (KVR_MOCKUP_BODY/PATH/SOURCE_TOP_RATIO + 그리기 로직 모두 그대로)
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
- 2026-05-04: **[v1.7 R11] KVR mockup PNG 신규 디자인으로 교체 (CITYPNG.COM iPhone 17 Portrait Mockup)**
  - 사용자 요청: "현재 iPhone 목업으로 설정되어 있는 PNG를 첨부한 PNG로 교체. 마찬가지로 상단 부분만 나오도록 동일하게 크기를 조정. 그 외의 설정은 코드를 건드리지 말 것."
  - 사용자 결정 (3건):
    1. 색상 처리: **원본 그대로** (라벤더 베젤 + 검정 frame + 검정 노치 — 일부 반투명 그대로)
    2. PNG 사이즈: **1500×1500 다운스케일** (기존 패턴 유지, base64 인라인 효율)
    3. 워터마크: **옵션 A** (KVR_MOCKUP_BODY 좌표로 자동 제외 — drawImage source rect가 워터마크 영역 자름)
  - 시각화 비교: 옵션 A vs 옵션 B 캔버스 결과물 픽셀 차이 = **0** (시각적 완전 동일) → 옵션 A로 충분 확인 후 선택
  - **새 PNG 변환** (Pillow + LANCZOS):
    - 원본: `[CITYPNG.COM]iPhone 17 Portrait Mockup - 4000x4000.png` (484.9KB, RGBA)
    - 다운스케일: 1500×1500 LANCZOS → `iphone-clean-1500.png` (117.1KB)
    - PNG 자체 가공 없음 (옵션 A 결정에 따름)
  - **자동 추출된 정확한 좌표** (1500×1500):
    - body bbox: x=424~1075 (W=652), y=20~1367 (H=1348)
    - 워터마크 영역: y=1391~1445 (8,317 opaque pixels — body 좌표로 자동 제외됨)
  - **수정 코드 (사용자 명시 제약 준수 — 최소 변경)**:
    - `KVR_MOCKUP_PATH` (line 2200): base64 갱신 (50,812 → 159,932 chars)
    - `KVR_MOCKUP_BODY` (line 2204): x=425→**424**, y=21→**20**, w=650→**652**, h=1346→**1348**
    - 그 외 모든 설정 변경 없음 (KVR_MOCKUP_SCREEN, KVR_MOCKUP_SOURCE_TOP_RATIO=0.55, R8 layering, R9 둥근 모서리 path, R10 notchPad/baseCy 모두 그대로)
  - **새 좌표 효과** (R9 SOURCE_TOP_RATIO=0.55 그대로):
    - srcH_visible = 1348 × 0.55 = 741.4
    - mockupH = 400 × (741.4 / 652) = **455.0** (R10.2: 455.6, ±1px 차이 — 시각적 동일)
    - mockupY = 1080 - 455 = **625** (R10.2: 624.4)
    - 콘텐츠 fit: 384 + 48 (pad) = 432 ≤ screenH ≈ 434 → ✅ 여전히 fit
  - 변경량: `today-banner-designer.html` 7,016라인 유지 · 554.7KB → **661.2KB** (+106.5KB, base64 증가)
  - 회귀 위험: 0 (KVR PNG 자산 + body 좌표만 교체)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
  - 새 PNG 자산: `repo/assets/keyvisual-review/iphone-clean-1500.png` (117.1KB)
- 2026-05-04: **[v1.7 R10.2] KVR PNG 베젤 + 노치 + 카메라 모두 PURE BLACK 통일 (사용자 명확한 의도 확인)**
  - R10.1 적용 후 사용자 추가 명확화: "휴대폰 목업의 카메라가 있는 중앙 부분과 외곽 부분을 검정색으로 칠해줘"
  - 사용자 의도: mockup의 **카메라 중앙(노치) + 외곽 베젤 전체**를 모두 BLACK으로 → 레퍼런스 이미지처럼 강한 대비
  - **PNG v4 변환** (Pillow + numpy):
    - 변환 조건: `alpha > 30 AND avg_RGB >= 50` → RGB(0,0,0) + alpha=255 강제
    - 처리 대상: 26,171 픽셀 (라벤더 베젤 RGB(148,139,152) + AA 가장자리)
    - 노치/카메라(R10.1에서 이미 검정)는 자동 보존 (avg<50 조건으로 제외 → 영향 없음)
    - 화면 영역(alpha=0) 무영향
  - **변환 결과**:
    - 베젤 RGB (148, 139, 152) → **(0, 0, 0)** ✅
    - 모든 불투명 픽셀 RGB 평균 (120, 116, 123) → **(0, 0, 0)** ✅
    - 화면 영역 alpha=0 그대로 유지 (400,000 픽셀 무변경) ✅
  - **새 PNG**: `iphone-purple-1500-transparent-v4.png` (92.2→37.2KB, -55KB) — 모든 픽셀이 검정 단일 색이라 PNG 압축 효율 극대화
  - **base64 갱신**: 125,878 → 50,834 chars (HTML -73.3KB)
  - 다른 코드 변경 없음 (PNG asset만 교체)
  - 변경량: `today-banner-designer.html` 7,014라인 유지 · 628.0KB → **554.7KB** (-73.3KB)
  - 회귀 위험: 0 (KVR PNG 자산만 교체)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
- 2026-05-04: **[v1.7 R10.1] KVR PNG 노치/카메라 PURE BLACK 강제 (R10 alpha 부스트 후 잔여 lavender 혼합 제거)**
  - R10 적용 후 사용자 시각 검증에서 노치/카메라가 여전히 흐릿/연한 색으로 보임 (라벤더 anti-aliasing edge 잔존)
  - 사용자 결정 (B 옵션 선택): 베젤 라벤더 유지, 노치/카메라만 솔리드 검정 + AA 가장자리도 검정으로 수렴
  - **PNG v3 변환** (Pillow + numpy):
    - 변환 조건: `(R+G+B)/3 < 100 AND alpha > 30` → RGB(0,0,0) + alpha=255 강제
    - 처리 대상: 16,637 픽셀 (노치 본체 + 카메라 도트 + AA 가장자리 혼합)
    - 변환 전 노치 RGB 평균: (2, 2, 6) → 변환 후: **(0, 0, 0)** ✅ 순수 검정
    - 베젤 영향 0: RGB(148, 139, 152) 라벤더 그대로, alpha 253 유지 ✅
  - **새 PNG**: `iphone-purple-1500-transparent-v3.png` (100.1→92.2KB, -7.9KB)
  - **base64 갱신**: 136,682 → 125,878 chars (HTML -10.6KB)
  - 다른 코드 변경 없음 (코드 0줄 수정, PNG asset만 교체)
  - 변경량: `today-banner-designer.html` 7,014라인 유지 · 638.4KB → **628.0KB** (-10.4KB)
  - 회귀 위험: 0 (KVR PNG 자산만 교체)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
- 2026-05-04: **[v1.7 R10] KVR PNG 노치/카메라 alpha 부스트 + 콘텐츠 노치 회피 padding + 로고 mockup 바로 상단 (사용자 레퍼런스 매칭)**
  - 사용자 R9 시각 검증 후 추가 요청 3건:
    1. mockup 테두리/카메라가 투명하게 처리됨 → 검정·퍼플 색상으로 복원
    2. 평가/리뷰 콘텐츠가 mockup 카메라 이후부터 시작
    3. 게임 로고 디폴트 위치 → mockup 바로 상단
  - 사용자 명시 제약: "요청한 내용 외의 것들은 절대 수정하지 마세요"
  - **PNG 진단** (Pillow + numpy):
    - 베젤 (라벤더 RGB 163,153,167): alpha 평균 247 ✅
    - **노치 검정 (RGB ~0,0,0)**: alpha 평균 **143/255 (56%)** ❌ 반투명
    - 카메라 도트 (RGB 37,35,90): alpha 평균 143 ❌ 반투명
    - 원인: 원본 PNG (배경 제거 서비스)가 노치/카메라에 anti-aliasing partial alpha 처리 → mockup이 콘텐츠 위에 그려져도 56% 투명도로 비쳐보임
  - **수정**:
    - **A. PNG alpha 부스트** (사용자 결정: 검정 계열만): RGB<100 & alpha>30 픽셀(13,702개)을 alpha=255로 강제 → `iphone-purple-1500-transparent-v2.png` (109.4→100.1KB) → base64 인라인 갱신 (149,438→136,682 chars, HTML -12.5KB)
    - **B. 콘텐츠 노치 회피**: `cy0 = screenY + pad + notchPad` (R9: `screenY + pad`) — `notchPad = 50` 신규 상수 추가. 노치 끝(canvas y=661) 아래 cy0=719에서 콘텐츠 시작 → 노치와 안 겹침 ✅
    - **C. 로고 디폴트 위치**: `baseCy = mockupY - 16 - drawH/2` (R8: `140 + drawH/2` 고정 위치) → mockup 상단으로부터 16px 간격으로 자동 배치 (drawH 100 가정 시 baseCy=558, drawY=508, 로고 하단 = mockupY-16 = 608)
  - **새 좌표** (R10): mockupY=624, mockupH=456 (R9 동일), cy0=719 (노치 회피), 콘텐츠 끝 1046, screenBottom 1080.0 → 9.9px 여유 ✅
  - **다른 요소 무변경** (사용자 제약 준수): SOURCE_TOP_RATIO=0.55 그대로, 흰 BG/clip 둥근 path 그대로, 헤드라인 fs=44/y=80 그대로, 폰트 사이즈 그대로
  - 변경량: `today-banner-designer.html` 7,012 → 7,014라인 (+2, notchPad 1줄 + 주석 1줄, 그 외 in-place 수정) · 673.1KB → **638.4KB** (-34.7KB, PNG 변환 후 alpha=255 픽셀이 PNG 압축 효율 ↑)
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
- 2026-05-04: **[v1.7 R9] KVR 흰 BG 상단 둥근 모서리 + mockup 길이 축소 + 하단 fit (사용자 레퍼런스 매칭)**
  - 사용자 R8.1 시각 검증 후 추가 요청 3건:
    1. mockup 화면 영역 흰 직사각형의 모서리를 mockup에 맞춰 잘리게 (둥근 모서리)
    2. mockup 길이가 너무 김 → 콘텐츠에 맞춰 상단만 남기고 줄임
    3. 줄어든 mockup을 배너 하단에 fit
  - 사용자 명시 제약: "요청한 내용 외의 것들은 절대 수정하지 마세요"
  - 사용자 레퍼런스 이미지 분석:
    - 표시 범위: iPhone body 상단 ~55% (노치 + 카메라 + 화면 콘텐츠 전체)
    - 컷 위치: 리뷰 본문 2번째 줄(`...들어가는...`) 직후 평평하게 cut
    - 시각: 화면 모서리 상단 둥글게, 하단은 베젤 없이 평평한 가로 cut 라인 → 캔버스 하단과 일치
  - **수정**:
    - **A**: `KVR_MOCKUP_SOURCE_TOP_RATIO` 1.0 → **0.55** (레퍼런스 매칭, body 상단 55%만 표시 — 노치+화면)
    - **B**: 흰 BG `ctx.fillRect()` → **상단 2개 모서리 둥글게(30px), 하단 2개 직각** path (`moveTo`/`lineTo`/`quadraticCurveTo` 명시 작성, 신규 helper 없음)
    - **C**: 콘텐츠 `ctx.rect()` clip → 위와 동일한 path (시각 일관성)
    - 신규 상수: `KVR_SCREEN_CORNER_R = 30`
    - **모서리 적용 위치**: 상단 2개만 둥글게 — mockup cut 라인이 캔버스 하단과 일치하므로 하단을 둥글게 하면 키비주얼이 보이는 작은 삼각 gap 발생 → 상단만 둥글게로 자연스러운 mockup screen 표현
  - **새 좌표** (R9): mockupH 828→**456**, mockupY 252→**624** (위쪽 키비주얼 영역 +372px 확장), screenY=645, screenH=435, screenBottom=1080.0 (캔버스 하단 정확 일치)
  - **콘텐츠 fit**: 384(콘텐츠) + 48(pad) = 432 ≤ 435 → ✅ 3px 여유 (tight but valid)
  - **다른 요소 무변경** (사용자 제약 준수): 로고 baseW=240/baseCy=140+, 헤드라인 fs=44/y=80 모두 R8 그대로
  - 변경량: `today-banner-designer.html` 6,996 → 7,012라인 (+16, fillRect 1줄 → path 12줄, clip rect 1줄 → path 9줄, 상수 1줄) · 671.5KB → **673.1KB** (+1.6KB)
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
  - 미세 조정 옵션: 콘텐츠가 너무 tight하면 SOURCE_TOP_RATIO 0.55 → 0.58 (mockupH 481, screenH 459, 27px 여유) 가능
- 2026-05-04: **[v1.7 R8.1] KVR PNG "Background Removed" 워터마크 제거 (body 좌표 정밀화)**
  - R8 적용 후 사용자 스크린샷 검증에서 발견:
    - mockup 하단에 "Background Removed" 검정 텍스트가 워터마크로 보임 → PNG 원본에 박혀있던 워터마크 (배경 제거 무료 서비스 자동 삽입 추정)
    - 분석: PNG 행별 검사 → iPhone body 실제 끝은 y=1367 (베젤 마지막 행), 그 아래 y=1370~1390는 투명, **y=1400~1430에 검정 "Background Removed" 텍스트**
    - 원래 `KVR_MOCKUP_BODY.h=1425`는 워터마크 영역까지 잘못 포함 (body 끝 y=21+1425=1446)
  - **수정**:
    - `KVR_MOCKUP_BODY.h` 1425 → **1346** (실제 body 끝 y=21+1346=1367, 워터마크 영역 source rect 제외)
    - `KVR_MOCKUP_SCREEN.hRatio` 0.92 → **0.974** (새 body 끝까지 화면 영역 확장 — 0.92*1425/1346 = 0.974)
    - 다른 코드 변경 없음 (mockupW/SCREEN.xRatio/yRatio/wRatio/SOURCE_TOP_RATIO 모두 R8 그대로)
  - **새 좌표** (R8.1): mockupH ≈ 828.3 (R8: 877.3), mockupY ≈ 251.7 (R8: 202.7), 위쪽 영역 252px (R8: 203px) — 키비주얼 영역 약간 확장 (보너스 효과)
  - screenY ≈ 272, screenH ≈ 807, 콘텐츠 384 + pad 48 = 432 → 375px 여유 ✅
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: `node --check` 통과
- 2026-05-04: **[v1.7 R8] KVR mockup 레이어 "맨 앞" + 투명 화면 PNG + body 100% 표시 (사용자 잔여 이슈 3건 일괄 해결)**
  - 사용자 디버그 컨텍스트 보고 (R7 적용 후에도 잔여):
    1. iPhone mockup이 소재 하단에 약간 떼어져 있어 어색
    2. 평가/리뷰 컨텐츠가 자꾸 mockup 레이어 대비 맨 앞에 위치 → mockup이 맨 앞에 보여야
    3. mockup 카메라/프레임 외 내부는 흰색(평가/리뷰 흰색과 동일)으로
  - 근본 진단: 3건 모두 하나의 결정(rendering order + 화면 PNG opaque)이 만든 연쇄 효과
    - ① "떼어진" 인상: SOURCE_TOP_RATIO=0.42로 iPhone body 상단 42%만 표시 → 하단 베젤·홈인디케이터 잘려서 mockup이 화면 중간에서 끊긴 듯 보임
    - ② "콘텐츠가 앞에": buildKvrCanvas 그리기 순서가 [2] mockup → [6] 콘텐츠 → 사실상 콘텐츠가 mockup 위에 그려짐
    - ③ 흰색 일치: 현재 PNG 화면 opaque 흰색 + 별도 fillRect 흰색 → mockup이 콘텐츠보다 뒤라 의미 없음
  - **수정 (A+B+C 결합)**:
    - **A. PNG 변환** (Pillow + numpy): `iphone-purple-1500-whitescreen.png`의 흰 화면 픽셀(R>240 G>240 B>240 alpha>200, 2.75% 픽셀)을 alpha=0 (투명)으로 변환 → `iphone-purple-1500-transparent.png` (109.4KB) → base64 인라인 (149,438 chars, R7 대비 -284 chars)
    - **B. body 100% 표시**: `KVR_MOCKUP_SOURCE_TOP_RATIO` 0.42 → **1.0** (상단 노치+카메라 + 화면 + 하단 베젤·홈인디케이터 전체)
    - **C. 그리기 순서 재배치** (`buildKvrCanvas`):
      - 변경 전: [1] bg → [2] mockup → [3] 로고 → [4] 헤드라인 → [5] 흰 fillRect → [6] 콘텐츠
      - 변경 후: [1] bg → [2] 로고 → [3] 헤드라인 → [4] 흰 fillRect → [5] 콘텐츠(clip) → [6] **mockup PNG 마지막** (투명 화면이라 콘텐츠 그대로 보임, 베젤·카메라가 콘텐츠 위로 보임)
    - **mockupW** 540 → **400** (body 100% + 캔버스 안 fit)
    - **새 좌표**: mockupH ≈ 877.3, mockupY ≈ 202.7 (위쪽 ~203px), screenY ≈ 224.6, screenH ≈ 807.1 (콘텐츠 432 + 375px 여유)
    - **로고 디폴트**: baseW 320→**240**, baseCy `200+drawH/2`→**`140+drawH/2`** (mockupY=203 침범 방지)
    - **헤드라인 디폴트**: fontSize 56→**44**, y 280→**80** (위쪽 영역 안 자연스러운 배치)
  - **레이어 검증**: PNG 화면 영역 transparent → mockup [6]에서 마지막에 그려도 콘텐츠를 덮지 않고 베젤·노치·카메라·하단 홈인디케이터만 콘텐츠 위로 보임 → 사용자 요구 "mockup 맨 앞" 충족 ✅
  - **하단 fit**: SOURCE_TOP_RATIO=1.0 → iPhone body 100% 표시 → 하단 베젤·홈인디케이터까지 보여 "떼어진" 인상 제거 ✅
  - **흰색 일치**: 화면 영역 fillRect `#ffffff` + 콘텐츠(평점·리뷰) 흰 BG = 동일 톤 ✅
  - 변경량: `today-banner-designer.html` 6,992 → 6,996라인 (+4) · 663KB → **671.5KB** (+8.5KB, R8 [6] mockup drawing 추가 + 코멘트)
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: 인라인 `<script>` 추출 → `node --check` 통과
- 2026-05-04: **[v1.7 R7] KVR mockup 화면 흰색 PNG + 하단 캔버스 끝 fit + 로고 디폴트 안전 위치 (to-be 레퍼런스 매칭)**
  - 사용자 to-be 레퍼런스 이미지(첨부) 분석:
    - mockup 화면 = **흰색** (콘텐츠 흰 배경과 동일 톤)
    - mockup 하단 = 캔버스 끝과 자연스럽게 이어짐 (gap 없음)
    - mockup 상단 노치/Dynamic Island/카메라 명확히 보임
    - 베젤 라벤더/메탈 (보라톤 그대로)
  - **변경 사항**:
    1. **PNG 변환** (Pillow + numpy): `iphone-purple-1500.png`의 검정 화면 영역(R<30 G<30 B<30 alpha>200, 2.6% 픽셀)을 흰색(255,255,255,255)으로 일괄 변환 → `iphone-purple-1500-whitescreen.png` (112KB, 6.4% 압축)
    2. **base64 인라인 갱신**: `KVR_MOCKUP_PATH`를 새 PNG의 base64로 교체 (149,749 chars, HTML 10KB 감소)
    3. **mockupBottomMargin 30 → 0**: mockup 하단 = 캔버스 끝 (이슈: "iPhone mockup이 소재 하단에 약간 떼어져 있어 어색")
    4. **`KVR_MOCKUP_SCREEN.yRatio` 0.04 → 0.025**: 노치 ↔ 콘텐츠 padding 좁힘 (자연스러운 mockup 시각)
    5. **로고 baseCy** `336+drawH/2` → **`200+drawH/2`** (drawY=200, mockupY=582 침범 방지, 위쪽 안전 위치)
  - 새 좌표:
    - mockupY=582.5, mockupH=497.5, screen 끝 y=1080 (캔버스 끝과 정확히 일치) ✅
    - screenY=612.1, screenH=467.9 → 콘텐츠 384 + pad 48 = 432 → 36px 여유 ✅
    - 위쪽 키비주얼+로고 영역 582px (R6의 552 → R7 582)
    - 베젤 좌우 27px / 상단 30px / 하단 0px (mockup 하단 = 캔버스 끝)
  - **레이어 순서 검증**: 콘텐츠는 SCREEN clip 영역 안에서만 그려져 mockup 베젤 위로 안 넘어감. mockup PNG 화면이 흰색이라 콘텐츠가 흰 화면 위에 자연스럽게 표시. mockup 베젤(보라+노치+카메라)이 PNG 단계에서 그려져 시각적으로 mockup이 콘텐츠 frame 역할 ✅
  - **흰 박스 fillRect 유지**: PNG 변환 잔여 검정 픽셀 보호 + 반투명 검정 영역(antialiasing)도 흰색으로 덮음
  - 변경량: `today-banner-designer.html` 6,992라인 유지 · 697KB → **663KB** (-34KB, base64 차이 + 마진 코드 제거)
  - 백업: `today-banner-designer.html.bak-r7` (sed 안전 마진)
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: `node --check` 통과
- 2026-05-04: **[v1.7 R6] KVR mockup 베젤 시각화 + 키비주얼 슬라이더 3배 확장**
  - 사용자 추가 보고:
    1. 콘텐츠가 mockup을 침범하는 것처럼 보임 (R5 적용 후에도 mockup 베젤이 너무 얇아 휴대폰 frame이 시각적으로 사라짐)
    2. 키비주얼 슬라이더 범위가 부족 — 3배 이상 확장 필요
  - **근본 원인 진단 (이슈 1)**: `KVR_MOCKUP_SCREEN`의 베젤 비율(xRatio=0.0185, yRatio=0.0056)이 너무 얇아 흰 박스가 mockup의 96%를 덮음 → mockup의 보라/검정 베젤이 시각적으로 사라짐 → 사용자에게 "콘텐츠만 floating, mockup 침범" 같은 인상 발생
  - **수정 (이슈 1)**:
    - `KVR_MOCKUP_SCREEN` 베젤 두껍게: xRatio 0.0185→**0.05**, yRatio 0.0056→**0.04**, wRatio 0.9631→**0.90**, hRatio 0.9825→**0.92**
    - 좌우 베젤 10px→**27px** / 상단 2.2px→**47px** (시각적으로 명확한 휴대폰 frame)
    - SCREEN 좁힘에 맞춰 `KVR_MOCKUP_SOURCE_TOP_RATIO` 0.34→**0.42** (콘텐츠 384 + 여유 66 fit)
    - mockupY 계산에 `mockupBottomMargin = 30` 추가 → 캔버스 하단 30px가 키비주얼 영역(휴대폰 floating 효과 + 하단 베젤 시각화)
    - 새 좌표: mockupH=497.5, mockupY=552.5, screenY=600, screenH=450, 콘텐츠 끝 y=984 → screen 끝 1050 (66px 여유) → 캔버스 끝 1080 (mockup 하단 30px 키비주얼 보임)
    - mockup PNG의 검정 화면 영역(0.0185, 0.0056, 0.9631, 0.9825)이 흰 박스(0.05, 0.04, 0.90, 0.92)보다 큼 → 흰 박스 가장자리 좌우 22px / 상단 18px에 검정 픽셀 보임 → 보라 베젤 + 검정 frame + 흰 화면 = 휴대폰 같은 시각 ✅
  - **수정 (이슈 2)**: 키비주얼 슬라이더 (line 1199, 1203, 1207)
    - 크기: max 200 → **600** (3배)
    - 좌우: ±500 step 5 → **±1500 step 10** (3배)
    - 상하: ±500 step 5 → **±1500 step 10** (3배)
  - 변경량: `today-banner-designer.html` 6,991 → 6,992라인 (mockupBottomMargin 1줄 추가) · 697KB 유지
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: `node --check` 통과
  - 검정 외곽선 사용자 답변 (R5 결정 사항 유지): 미리보기 전용 안전장치, PNG 미반영 — 의도된 동작
- 2026-05-03: **[v1.7 R5] KVR mockup 정밀 fit + 로고 디폴트 위치 + 검정 외곽선 검증**
  - 사용자 추가 4건 요청 (R4 적용 후 검증):
    1. 로고 디폴트 위치 → 헤드라인 ↔ mockup 사이로 이동
    2. mockup 크기 → 콘텐츠 잘리지 않을 정도로 정밀 축소
    3. 평점 콘텐츠 mockup 침범 방지
    4. 키비주얼 침범 방지 검정 외곽선/테두리 — 실제 PNG 반영 여부 검증
  - **콘텐츠 누적 높이 측정** (코드 분석): pad24 + 헤더40 + 평점116 + 부제44 + 제목36 + 메타42 + 본문58 + pad24 = **384px (ko/en)** / 372px (ja/zh-TW)
  - **타겟 screenH ≈ 400** (콘텐츠 384 + 16px 여유) → `KVR_MOCKUP_SOURCE_TOP_RATIO` 0.50 → **0.34**
  - 새 수치: srcH_visible=484.5, mockupH=402.5, mockupY=677.5, screenH=395.8, 콘텐츠 끝 y=1068 → 캔버스 끝 1080 (12px 여유)
  - 위쪽 키비주얼+로고 영역 488px → **677px (62.7%)** ↑
  - **로고 baseCy** `40 + drawH/2` → `336 + drawH/2` (헤드라인 끝 312 + 24px gap → mockup 시작 677 사이 위치)
  - **검정 외곽선 검증 결과** (코드 미수정, 의도된 동작 확인):
    - 미리보기 영역 검정 padding = `.preview-frame` 부모 컨테이너 + `buildKvrBanner` wrap의 `background:#000` (line 4660, async canvas 로딩 placeholder)
    - 실제 PNG 출력 = `buildKvrCanvas`가 1080×1080 캔버스에 키비주얼 풀 cover로 그림 → **검정 외곽선 PNG에 반영 안 됨** ✅
    - 결론: 미리보기 안전장치(키비주얼 누락 시 검정 fallback). 정상 동작
  - 변경량: `today-banner-designer.html` 6,990 → 6,991라인 (주석 1줄 추가) · 697KB 유지
  - 회귀 위험: 0 (KVR 전용)
  - 문법 검증: `node --check` 통과
- 2026-05-03: **[v1.7 R4] KVR UX 정리 + mockup 추가 축소 (B2)**
  - 사용자 실측 후 추가 이슈 2건 + UX 1건 일괄 수정 (코드 미수정 정밀 리뷰 → 결정 → 수정 순)
  - **이슈 A 수정 (Critical)**: KVR 모드에서 today-tap 공용 `s-drop-keyart` / `s-drop-icon` 슬롯이 노출되어 사용자가 거기에 업로드해도 미리보기 무반응 (state.single.keyart/icon은 KVR 렌더가 안 읽음)
    - line 1298 wrapper의 `data-tmpl-hide="sd-showcase"` → `"sd-showcase,keyvisual-review"` 1줄 변경
    - 결과: KVR 단건 패널의 슬롯 4개 → 2개로 정리 (KVR 전용 키비주얼+로고만 노출)
  - **이슈 B 수정 (B2 옵션)**: mockup이 캔버스 68% (~734px) 차지 → 키비주얼 영역 부족
    - `KVR_MOCKUP_SOURCE_TOP_RATIO` 0.62 → 0.50 (1줄 변경)
    - 새 계산: srcH_visible = 712.5 (vs 883.5), mockupH ≈ 592 (vs 734), mockupY ≈ 488 (vs 346)
    - 효과: 위쪽 키비주얼+로고 영역 346px(32%) → 488px(45%) 확장
  - **UX 수정**: 헤드라인 디폴트 ON(`real-player`) → OFF (와이어프레임 의도 일치)
    - `KVR_DEFAULT.headlinePreset` `'real-player'` → `'off'` (line 2136)
    - `buildKvrCfg` fallback `'real-player'` → `'off'` (line 4295)
    - `bindKvrSingleUI` fallback `'real-player'` → `'off'` (line 5333)
  - **결정 기록 (사용자 즉답)**: 1=Yes / 2=B2 / 3=축소 / 4=현재 유지(별점+개수 인라인) / 5=현재 유지("가장 도움이 되는 리뷰" 라벨) / 6=헤드라인 OFF
  - 안내 텍스트 갱신: "iPhone mockup은 캔버스 폭 50% (540px), body 상단 50%만 표시 → mockup 높이 ≈ 592px (캔버스 하단 정렬) · 헤드라인 기본 OFF"
  - 변경량: `today-banner-designer.html` 6,990라인 유지 · 697KB 유지 (텍스트 치환만)
  - 회귀 위험: 0 (KVR 전용 변경, mockup 외 영향 없음)
  - 문법 검증: `node --check` 통과
- 2026-05-03: **[v1.7 R3] KVR 송오브블루 스타일 레이아웃 — purple iPhone PNG body 상단 62% + drawImage 9-인자**
  - 배경: R2 fix(mockup 폭 540→400)에도 사용자가 송오브블루 스타일에 더 가까운 디자인 요청 → 사용자 명시 사양에 따라 R3 적용
  - 사양 (사용자 직접 지시):
    1. purple PNG (4000×4000) → 1500×1500 다운스케일 후 base64 인라인
    2. body의 62%만 표시 (송오브블루 스타일)
    3. drawImage 9-인자 source rect 사용
    4. 그리기 순서 유지 (배경→mockup→로고→헤드라인→클립+콘텐츠)
  - PNG 분석 (Pillow + numpy):
    - Body bbox (1500×1500): x=425..1074 (W=650), y=21..1445 (H=1425), 종횡비 0.456
    - Screen 검출: 검은색 화면 (RGB<30) 영역 — body 상대 비율 (1.85%, 0.56%, 96.31%, 98.25%)
    - **purple iPhone PNG의 화면이 검은색**이라 흰 배경 박스를 destination 위에 그린 후 콘텐츠 추가
  - 신규 상수: `KVR_MOCKUP_BODY = {x:425, y:21, w:650, h:1425}`, `KVR_MOCKUP_SOURCE_TOP_RATIO = 0.62`
  - 갱신: `KVR_MOCKUP_PATH` (purple base64, 156KB), `KVR_MOCKUP_SCREEN` (purple PNG body 비율로 재계산)
  - `buildKvrCanvas` [2] mockup: `ctx.drawImage(img, 425, 21, 650, 883.5, 270, 346, 540, 734)` 9-인자
  - `buildKvrCanvas` [5] 화면 영역: source rect 안 visible screen 비율로 재계산 (`scYR_dst = scYR / SOURCE_TOP_RATIO`, `scHR_dst = min(scHR, SOURCE_TOP_RATIO-scYR)/SOURCE_TOP_RATIO`)
  - 폰트 사이즈 R1 수준으로 복원 (mockup 폭 540으로 다시 커짐): 헤더 26 / 평점 88 / 별 26+14 / 부제 22 / 리뷰 24 / 본문 20 / 메타 16
  - 헤드라인 위치 220 → 280 (mockup 시작 y=346 위)
  - padding 32 → 24 (콘텐츠 영역 활용도 ↑)
  - 변경량: `today-banner-designer.html` 6,956 → 6,990라인 (+34) · 543KB → 697KB (+154KB, purple base64 인라인)
  - 회귀 위험: 0 (KVR 전용 변경)
  - 문법 검증: `node --check` 통과
  - 좌표 검증: 위쪽 346px (키비주얼+로고+헤드라인), 하단 734px (mockup 송오브블루 스타일)
- 2026-05-03: **[v1.7 hotfix] file:// 프로토콜 KVR mockup 로드 실패 수정 (분석/수정/검증)**
  - 증상: 사용자가 `open today-banner-designer.html` (file://)로 열었을 때 KVR 단건 미리보기에서 mockup 미표시 + 배치 결과 4장 모두 `Failed to execute 'drawImage'... HTMLImageElement is in 'broken' state` 에러
  - 근본 원인 ①: `loadCachedImage`(line 3050)의 `img.crossOrigin='anonymous'` 설정이 file:// 프로토콜에서 외부 PNG(`assets/keyvisual-review/iphone.png`) 로드 시 Chrome unique-origin 정책으로 차단 → broken state
  - 근본 원인 ②: broken state Image가 `_imgCache.set(dataURL, img)`로 캐시에 저장되어 이후 모든 호출이 같은 broken 객체 반환 (cascade failure)
  - 왜 v1.7에서만: 기존 4템플릿은 모두 base64 dataURL(BADGE_ASSETS, AS_SVG, 사용자 업로드)이라 file:// 영향 없음. KVR이 첫 외부 PNG 사용
  - 수정 A: `KVR_MOCKUP_PATH` 상수를 `'assets/keyvisual-review/iphone.png'` → base64 dataURL로 인라인 (~8.7KB) → file://+HTTP 모두 작동 + 다른 템플릿 패턴 일치
  - 수정 D: `loadCachedImage`에 broken state 검출 강화 — `decode()` reject 또는 `naturalWidth==0`일 때 `console.warn` + `null` 반환 (캐시 미저장). 호출자는 null fallback 처리
  - 변경량: `today-banner-designer.html` 6,943 → 6,956라인 (+13) · 534KB → 543KB (+9KB)
  - 회귀 위험: 0 — KVR_MOCKUP_PATH는 KVR 전용, loadCachedImage 변경은 정상 케이스 무영향(broken case는 어차피 그리기 실패)
  - 문법 검증: `node --check` 통과
  - 자산 파일 `assets/keyvisual-review/iphone.png`는 보존 (소스 추적성)
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
