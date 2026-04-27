# PDCA Plan — App Store Screenshot 템플릿 (v1.5)

**Feature**: appstore-screenshot
**Created**: 2026-04-25
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (recommended for future similar requests)**: `/plan-plus`

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | App Store Screenshot 템플릿 추가 |
| 시작 | 2026-04-25 |
| 본체 파일 | `today-banner-designer.html` (단일 HTML) |
| 변경 라인 | +1,216 (3,881 → 5,097) |
| FR | 11건 |
| NFR | 4건 |
| SC | 6건 |
| R | 3건 |

### Value Delivered (4관점)
| 관점 | 내용 |
|---|---|
| Problem | 9:16 ad creative 만들 때마다 디자이너가 App Store 스크린샷을 4개 언어 × N장 수동 제작. 다크/라이트·키아트·통계 수치까지 일일이 정렬해야 해 비효율 |
| Solution | 픽셀 퍼펙트 iOS App Store 페이지 모방 템플릿 — 키아트 1장 + 4언어 입력 + 1테마 선택 → Single export 1장 또는 Batch ZIP 4장 자동 생성 |
| Function UX Effect | 헤더 셀렉터에서 "App Store Screenshot" 선택 → 9:16 자동 잠금, 4언어 탭에서 가변 텍스트 입력, 토글 4종으로 통계·탭바·Get·IAP 표시/숨김, 다크/라이트 즉시 전환 |
| Core Value | UA 운영 워크플로우의 다국어 광고 소재 제작 시간 단축 + 일관된 픽셀 퍼펙트 출력 + 미디어별 검수 위험 분산 (탭바/Get 토글로 외관 조정) |

---

## Context

`today-banner-designer.html` (단일 HTML, v1.4)는 기존 2개 템플릿(`today-tap`, `app-badge`)을 제공한다. 사용자(Mobile Game UA Manager)가 첨부한 4개 언어 App Store 스크린샷(Underdark:Defense, ko/en/ja/zh-TW)을 픽셀 퍼펙트로 모방한 3번째 템플릿을 추가해 9:16 광고 소재 제작 시간을 단축하려 한다.

**스킬 매핑**: 추후 비슷한 요청은 `/plan-plus appstore-template` 으로 시작하면 자동 진행됨. 보조 — `bkit:phase-3-mockup`, `bkit:phase-5-design-system`, `superpowers:brainstorming`.

---

## 사용자 결정 요약 (확정 — 2026-04-25)

| 항목 | 결정 |
|---|---|
| Fidelity | 픽셀 퍼펙트 (Apple App Store 페이지 충실 재현) |
| 출력 해상도 | 1080 × 1920 (9:16 only, 기존 CANVAS_SPEC 재사용) |
| 언어 | EN / KO / JA / ZH-Hant (4종) |
| 테마 | 다크 또는 라이트 1개 선택 (per-design 단일 테마) |
| 키아트 | 1장 공용 (4언어 동일 이미지) |
| 통계 (평점·리뷰수·랭킹·개발자) | 입력필드 + 전체 영역 숨김 토글 |
| 하단 탭바 / Get / IAP 라벨 | 둘 다 표시 + 표시/숨김 토글 (개별) |
| 상태바 (시간·신호·Wi-Fi·배터리) | 고정값 (시간 9:41 — Apple 마케팅 관례) |
| 로케일 전용 컬럼 (KO 국내등급, JA 이벤트) | 제외, 4언어 모두 동일한 4컬럼 유지 |
| 디바이스 프레임 | 없음 (App Store 페이지 자체만 9:16 채움) |
| Export 모드 | Single + Batch 둘 다 (정책: 모든 신규 템플릿에 적용) |
| 자동 번역 | 안 함 (사용자가 4언어 직접 입력) |

---

## Functional Requirements (FR)

- **FR-1**: 헤더 템플릿 셀렉터(`#template-selector`)에 `appstore-screenshot` 옵션 추가 ✓
- **FR-2**: `TEMPLATE_KEYS` 배열에 `'appstore-screenshot'` 추가 + `.tmpl-appstore-screenshot` CSS 스코프 분리 ✓
- **FR-3**: `AS_LANG_PACK` 신규 — 4언어별 고정 라벨 (search/get/iap/more/4통계헤더/연령접미사/deviceLabel/tabs[5]) ✓
- **FR-4**: 9:16 한정 — `applyTemplateSwitch`에서 `s-size` disabled + 배치 사이즈 체크박스 자동 잠금 ✓
- **FR-5**: 사용자 입력 필드 (단건 모드 = 현재 언어 1개, 배치 모드 = 4언어 탭):
  - 공통 (언어 무관 1회): 키아트 이미지(`state.single.keyart` 재사용), 앱 아이콘(`state.single.icon` 재사용), 테마, 표시 토글 4종 ✓
  - 언어별 7개 슬롯: 앱 타이틀, 카테고리, 평점, 리뷰수, 랭킹, 개발자, 설명 본문 ✓
- **FR-6**: 픽셀 퍼펙트 8섹션 레이아웃 (위→아래):
  1. 상태바 (고정 9:41 + 신호 4 + Wi-Fi + 배터리)
  2. 헤더 (← + Search 라벨)
  3. 앱 정보 (아이콘 220×220 r50 + 타이틀 54px + 카테고리 28px + Get 32px + IAP 22px)
  4. 통계 4컬럼 (평점·연령4+·랭킹·개발자) — 숨김 토글 시 통째로 비표시
  5. 키아트 카드 (16:9, r28)
  6. "iPhone, iPad" + ⌄
  7. 설명 본문 (4줄 클램프 + more)
  8. 탭바 (Today/Games/Apps/Arcade/Search) — 숨김 토글 가능
  ✓
- **FR-7**: 다크/라이트 테마 — `data-theme="light|dark"` + CSS 변수 `--as-*` 11종 (`--as-bg`, `--as-text-primary`, `--as-text-secondary`, `--as-divider`, `--as-card-bg`, `--as-statusbar-icon`, `--as-cta-bg`, `--as-link`, `--as-tab-active`, `--as-tab-inactive`, `--as-stat-value`) ✓
- **FR-8**: 별점 — 5개 별 SVG (소수점 부분은 starH linearGradient로 부분 채움) + 옆에 숫자 ✓
- **FR-9**: Single export — 현재 화면(현재 언어 + 현재 테마) 1장 PNG 다운로드 ✓
- **FR-10**: Batch export — (4언어 × 선택된 1테마) = **4장 PNG ZIP**. 파일명: `{prefix}_appstore_{lang}_{theme}_1080x1920.{ext}` ✓
- **FR-11**: 상태 영속화 — `localStorage` 기존 `customPresets:v1` 재사용 (별도 namespace는 v2 후보) ✓ (deferred)

## Non-Functional Requirements (NFR)

- **NFR-1**: Canvas 기반 export (`USE_CANVAS_EXPORT = true` 동선 유지) — DOM-to-image 사용 안 함 ✓
- **NFR-2**: 폰트 — JP=Noto Sans JP, ZH-TW=Noto Sans TC, KO/EN=Pretendard. `ensureFontsLoaded()` 재사용 + `asFontFamily(lang)` 헬퍼 ✓
- **NFR-3**: 키아트 이미지 캐시 — `_imgCache` 재사용, batch 시 1회 디코드 → 4언어 재사용 ✓
- **NFR-4**: 단일 HTML 정책 유지 — 외부 모듈/번들 도입 금지, 인라인 `<script>` + `<style>` 내 추가 ✓

## Scenarios (SC)

- **SC-1**: 사용자가 템플릿 셀렉터에서 "App Store Screenshot" 선택 → 9:16 자동 잠금, 입력 패널이 새 필드로 전환 ✓
- **SC-2**: 키아트 1장 + 앱 아이콘 1장 업로드 + 다크 테마 선택 + 4언어 탭에서 각각 타이틀/설명/통계 입력 ✓
- **SC-3**: "이미지 다운로드" 클릭 → 1080×1920 PNG 1장 (현재 언어×테마) ✓
- **SC-4**: 배치 모드에서 "ZIP 일괄 다운로드" → 4장 PNG (EN/KO/JA/ZH-Hant 동일 다크 테마) ZIP ✓
- **SC-5**: "통계 영역" 토글 OFF → 4컬럼 통째 사라지고 키아트가 위로 이동 ✓
- **SC-6**: 라이트 테마로 전환 → 미리보기 + 모든 export 결과가 라이트로 갱신 ✓

## Risks (R)

- **R-1 (IP)**: Apple은 자사 UI 모방 광고를 일부 가이드라인에서 제한 가능. **완화**: Get 버튼·탭바 표시/숨김 토글로 외관 조정 가능. 광고 플랫폼 검수 시 반려 가능성을 사용자에게 README에 명시.
- **R-2 (단일파일 비대화)**: 387KB → 약 462KB로 증가. **완화**: 큰 함수는 별도 명명(`buildAppStoreScreenshotBanner`, `buildAppStoreScreenshotCanvas`), 추후 모듈화 검토.
- **R-3 (롤백)**: `TEMPLATE_KEYS`에서 신규 키 제거 + 관련 함수 삭제로 1커밋 롤백 가능. **완화**: 기능별 11단계로 커밋 분리 (CSS / HTML(Single) / HTML(Batch) / state / DOM 빌더 / Canvas 빌더 / Single 다운로드 / Batch ZIP / 토글 / 정책 / 문서).

---

## 변경 파일

### 코드
- `today-banner-designer.html` (단일 파일, +1,216 라인)

### 문서
- `CLAUDE.md` — "정책" 섹션 신규 + "현황" v1.5 항목 추가
- `docs/01-plan/features/appstore-screenshot.plan.md` (이 문서)

### 재사용한 기존 자산
- `loadCachedImage()`, `_imgCache`, `updateStateImage()` — 이미지 캐시
- `prepCfgImages` 패턴 — `prepAppStoreCfgImages` 신규 (icon + keyart + 18 SVG 사전 디코드)
- `ensureFontsLoaded()` — Pretendard/Noto JP/Noto TC 자동 로드
- `drawImageCover()` — 키아트·아이콘 cover fit
- `canvasToDataURL()` — PNG 변환
- `escapeHTML()` — XSS 방어
- JSZip — 배치 ZIP
- `data-lang` 속성 + 폰트 자동 스왑 (이미 동작)

---

## 신규 함수 / 상수

### Functions (10)
- `buildAppStoreScreenshotBanner(cfg)` — DOM 프리뷰 빌더 (8섹션)
- `buildAppStoreScreenshotCanvas(cfg)` — Canvas 직접 합성
- `prepAppStoreCfgImages(cfg)` — icon + keyart + 18 SVG 사전 디코드
- `buildAppStoreScreenshotCfg(stateObj)` — state.single → cfg 평탄화 (현재 언어 슬롯)
- `buildAppStoreFilename(s)` — `{prefix}_appstore_{lang}_{theme}_1080x1920.{ext}`
- `buildAsIconUrl(key, color)` — SVG 토큰 치환 → data:URL
- `asFontFamily(lang)` — 언어별 폰트 스택
- `asWrapText(ctx, text, maxWidth, maxLines)` — CJK 친화 줄바꿈, 4줄 클램프
- `syncSingleAppStoreFromUI()` — 단건 모드 입력 → state 동기화
- `loadAppStoreSlotToUI(lang)` — 언어 전환 시 슬롯 복원

### Constants (5)
- `AS_LANG_PACK` — 4언어 고정 라벨 (search/get/iap/more/통계헤더4/연령접미사/deviceLabel/tabs5)
- `AS_THEMES{dark, light}` — Canvas용 테마 팔레트 (CSS와 동일 hex)
- `AS_ICON_DEFS{18}` — Canvas용 inner SVG path (`__C__` 토큰)
- `AS_SVG{18}` — DOM용 wrapper SVG 문자열
- `APPSTORE_SCREENSHOT_DEFAULT` — 기본 state (theme + 4토글 + langs[4])

### State 확장
- `state.single.appstore = APPSTORE_SCREENSHOT_DEFAULT 깊은 복사`
- `state.batch.{as_theme, as_showStats, as_showTabbar, as_showCta, as_showIap}` (공통 설정)
- `state.batch.langOverrides[lang].{as_title, as_subtitle, as_description, as_rating, as_ratingCount, as_ranking, as_developer}` (기존 구조 통합)

---

## 검증 (Verification)

### 정적 (커밋 직후)
- [x] 인라인 `<script>` 추출 → `node --check` 통과 (5단계 모두)
- [ ] 브라우저에서 `today-banner-designer.html` 직접 열기 → 콘솔 에러 0
- [ ] 템플릿 셀렉터에 "App Store Screenshot" 선택 시 패널 전환 OK
- [ ] 4언어 탭 전환 시 폰트 정상 (Pretendard / Noto JP / Noto TC)
- [ ] 다크 ↔ 라이트 토글 시 색상 토큰 즉시 반영
- [ ] 통계 영역 숨김 토글 → 키아트가 자연스럽게 위로 이동

### 동적 (export)
- [ ] Single export → 1080×1920 PNG, 픽셀 정확도 (첨부 App Store 캡처 4장과 비교)
- [ ] Batch export → 4 PNG (EN/KO/JA/ZH-Hant) ZIP, 파일명 규격 일치
- [ ] 키아트 이미지 1번 업로드 → 4장 모두 동일 키아트 사용 (`_imgCache` 재사용 검증)
- [ ] 폰트 폴백 없음 — Canvas 출력에 Pretendard/Noto 정상 렌더 (한글·일본어·번체 모두)

### 회귀 (regression)
- [ ] 기존 `today-tap` 템플릿 정상 동작 (1:1 / 1200×628 / 9:16)
- [ ] 기존 `app-badge` 템플릿 정상 동작 (모든 사이즈)
- [ ] localStorage 기존 preset 호환 (충돌 없음)

### 시각 비교 (사용자 협업)
- 사용자가 첨부한 4개 스크린샷(Traditional Chinese, English, Japanese, Korean) vs 신규 템플릿 출력 1:1 비교 → 각 영역(상태바·헤더·앱정보·통계·키아트·설명·탭바) 일치 여부 체크리스트 작성

### 다음 단계 (구현 후)
- `/pdca analyze appstore-screenshot` — 갭 분석 (≥90% 목표)
- 갭 <90% → `/pdca iterate`
- 갭 ≥90% → `/simplify` → `/pdca report`

---

## 미해결 / v2 후보 (현재 범위 제외)
- 자동 번역 API 연동 (현 결정: 수동 입력)
- 키아트 언어별 오버라이드 (현 결정: 1장 공용)
- 디바이스 프레임(아이폰 베젤) (현 결정: 없음)
- 다크 + 라이트 동시 export (현 결정: 1테마/디자인)
- 한국 등급·일본 이벤트 등 로케일 전용 컬럼 (현 결정: 4컬럼 통일)
- localStorage 별도 namespace (`customPresets:appstore-screenshot:v1`) — 현재는 기존 시스템 재사용
- 픽셀 퍼펙트 미세 튜닝 (사용자 실측 후 캡처 비교 → 좌표 ±2~5px 보정)

이들은 사용자 실측 + Gap 분석 결과를 바탕으로 v2 PDCA에서 처리.
