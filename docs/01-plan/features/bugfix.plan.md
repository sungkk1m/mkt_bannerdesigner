# Plan — bugfix (Canvas 직접 합성 + Overflow 확장)

- **Feature**: bugfix
- **Date**: 2026-04-22 (r1/r2), 2026-04-22 (**r3 확장**)
- **Status**: Plan (r3)
- **Owner**: 김성권 (UA Manager, ksk@superplanet.net)
- **Target**: `today-banner-designer.html` (Today Banner Designer v1.2 → v1.3)
- **Related**: `banner-bugfix` (완료, Gap 97%)
- **r3 범위**: 실사용 중 발견된 이슈 5건 — (1) 일본어 게임명 CTA 침범 (2) 게임명↔부제 간격 (3) 배치 기본 규격 (4) 배치 기본 언어 (5) 사용자 프리셋 저장

---

## Executive Summary

이전 `banner-bugfix`에서 도입한 `img.decode()`는 **대기 로직**만 개선했지 **변환 자체**(html-to-image)는 그대로였음. 사용자 실측 결과 체감 속도 개선 미미. 본 Plan은 **html-to-image 자체를 제거**하고 Canvas 2D API로 직접 그리는 방식으로 근본 해결. 동시에 오버플로우 조작 범위를 Scale 200%, X/Y ±80%로 확장하여 표현력을 확보.

| 관점 | 내용 |
|------|------|
| **Problem** | ① 배치 8장(1200×628 + 1080×1080 × 4언어) 다운로드가 브라우저 실측상 여전히 느림 — `html-to-image` 라이브러리의 DOM→SVG→Canvas 변환 파이프가 절대 병목 ② Overflow Scale 150% 상한과 X ±30% / Y ±15% 오프셋이 실제 제작물(Scale 상향된 SD)에서 부족 |
| **Solution** | ① **Canvas 직접 합성** — `<canvas>` API로 배경·카드·키아트·오버플로우·drop-shadow·다크바·아이콘·텍스트 모두 수동 drawImage/fillText. html-to-image 경로 대체. 병렬화·OffscreenCanvas 여지도 확보 ② Scale max 150→**200**, X/Y offset 각 ±**80%**로 확장. wrap `clip-path: inset(-9999px -9999px 0 -9999px)`로 **하단만 클립**해 자유도 최대 + darkbar 침범 방지 |
| **Function UX Effect** | 배치 8장 기준 **20~30초 → 1~2초**(10-30배 체감 속도 개선). 대형 SD 캐릭터·극단 오프셋 연출 가능. 단건 다운로드도 즉시 반응 |
| **Core Value** | 배치 생산성 병목 해소. UA 캠페인 대량 소재 제작이 "커피 한 잔 기다림"에서 "즉시"로 전환. 이전 `banner-bugfix`에서 약속했으나 미달성했던 SC-07 성능 목표를 진짜 달성 |

### r3 추가 요약 (실사용 이슈 5건)

| 관점 | 내용 |
|------|------|
| **Problem** | ① 일본어 게임명(`ソードマスターストーリー`)이 CTA 영역 침범 ② 게임명↔부제 상하 간격 2px로 너무 좁아 붙어 보임 ③ 배치 기본 규격 `1:1+9:16`은 실무에서 `1:1+1200x628`이 더 빈번 ④ 배치 기본 언어 `ko+en`에서 매번 ja/zh-TW 체크 번거로움 ⑤ 자주 쓰는 게임명/부제 조합을 매번 재입력 |
| **Solution** | ① `[data-lang="ja"]` selector로 title/subtitle 0.85배 고정 축소 (CSS 6 rule + Canvas 1 함수) ② `.darkbar-text gap` 2→4px + Canvas `lineGap` 2→4 전 사이즈 통일 ③ HTML `checked`·state 기본값 변경 ④ 4개 언어 모두 기본 checked ⑤ localStorage 기반 사용자 프리셋 (title/subtitle/cta/disclaimer 4필드, `prompt()` 저장, confirm 덮어쓰기, 🗑 삭제) |
| **Function UX Effect** | 일본어 overflow 제거 · 타이포 가독성 향상 · 1-클릭 최적 프리셋 선택 · 반복 입력 0회 달성 |
| **Core Value** | 일본어 시장 광고 품질 확보 + 반복 작업 제거 → 배너 1건 평균 제작 시간 추가 단축 |

| 항목 | 내용 |
|------|------|
| **WHY** | 이전 feature의 SC-07(50%+ 단축)이 실측상 미달성. html-to-image가 근본 병목임을 확인. Overflow 범위는 실사용 중 부족 판명 |
| **WHO** | 사내 UA팀 제작자 (Primary: 김성권) |
| **RISK** | Canvas 재현도(픽셀 레벨 미세 차이) / 폰트 로드 타이밍 / Canvas `shadowXXX`와 CSS `filter: drop-shadow()` 블러 해석 차이 / 다국어 폰트 fallback |
| **SUCCESS** | 배치 8장 ≤ 2초 + Canvas 출력물이 기존 시각 품질과 유사 + Overflow 확장 범위 정상 조작 |
| **SCOPE** | `today-banner-designer.html` 내부만. 외부 의존·빌드 파이프라인·배포 방식 무변경 |

---

## 1. Requirements

### Functional Requirements

| ID | 내용 | 근거 이슈 |
|----|------|-----------|
| FR-01 | **Canvas 직접 합성 함수 `buildBannerCanvas(cfg)` 구현** — HTMLCanvasElement를 반환. html-to-image 호출 제거 | 이슈 1 |
| FR-02 | Canvas가 재현해야 하는 요소: (a) 배너 흰색 배경 + border-radius 0 (b) Today 워드마크(italic, 크기·여백 사이즈별) (c) 프로필 아이콘 — 1200×628 전용, 파란 원+SVG 사람 아이콘 (d) 카드 rounded rectangle clip → 키아트 `drawImage` (object-fit cover) (e) 오버플로우 이미지 + drop-shadow (f) 다크바(border-radius 하단, rgba 97% 검정) (g) 아이콘 이미지 rounded (h) 게임명·부제 nowrap 텍스트 (i) CTA rounded 보더+텍스트 (j) 고지문구 nowrap 텍스트 | 이슈 1 |
| FR-03 | **사이즈별 설정 테이블 `CANVAS_SPECS`** — 현재 CSS에 흩어진 수치(padding, header font/size, card radius, darkbar height·padding, icon size, title/subtitle font, cta size, disclaimer font/position 등)를 JS 상수로 이관. 1:1/9:16/1200×628 3개 사이즈별 | 이슈 1 |
| FR-04 | **폰트 로드 확보** — Pretendard(한/영), Noto Sans JP, Noto Sans TC를 Canvas 그리기 전 `document.fonts.load('weight size family')`로 사전 로드 대기. 누락 시 Canvas `fillText`가 시스템 fallback 폰트로 그림 → 다국어 품질 손상 방지 | 이슈 1 |
| FR-05 | Overflow drop-shadow는 Canvas `ctx.shadowOffsetX/Y`, `ctx.shadowBlur`, `ctx.shadowColor = rgba(0,0,0, opacity)`로 재현. 투명 PNG 외곽선을 따라 자동 그림자 생성 (drawImage 특성) | 이슈 1 |
| FR-06 | **`handleBatchExportZip`, `downloadBatchItem`, `handleSingleDownload` 모두 Canvas 경로로 전환** — html-to-image `bannerToImage()` 호출 제거 | 이슈 1 |
| FR-07 | **프리뷰(handleBatchPreview, refreshSinglePreview) 경로는 현행 DOM 방식 유지** — Canvas는 "출력(다운로드)" 전용. 프리뷰는 실시간성·간편성 우선 | 이슈 1 |
| FR-08 | `html-to-image` CDN은 **일단 유지** (주석만 "미사용, 롤백 대비" 표시). 검증 완료 후 별도 PDCA에서 제거 | 이슈 1 (방어적) |
| FR-09 | **Overflow Scale 슬라이더 max 150 → 200** (단건: `#s-overflow-scale`, 배치: `#b-overflow-scale`) | 이슈 2 |
| FR-10 | **Overflow X 오프셋 min/max -30~30 → -80~80** (단건: `#s-overflow-x`, 배치: `#b-overflow-x`) | 이슈 2 |
| FR-11 | **Overflow Y 오프셋 min/max -15~15 → -80~80** (단건: `#s-overflow-y`, 배치: `#b-overflow-y`) | 이슈 2 |
| FR-12 | **`.banner-overflow-wrap`에 `clip-path: inset(-9999px -9999px 0 -9999px)` 적용** — 상·좌·우 무한 자유, 하단(= darkbar 상단 = wrap의 bottom 경계)만 클립 | 이슈 2 |
| FR-13 | **`transform`을 wrap에서 img로 이동** — wrap은 위치 고정, img가 내부에서 translate/scale. wrap의 clip-path가 정상 작동하도록. Canvas 버전도 img 기준 transform 수치 사용 | 이슈 2 |
| **FR-14** | **일본어 title/subtitle 0.85배 고정 축소 (CSS)** — `.banner[data-lang="ja"].size-1x1 .game-title { font-size: 36px }` 형태로 사이즈별 6 rule 추가 (1:1 42→36, 24→20 · 9:16 56→48, 32→27 · 1200x628 30→26, 17→14. 모두 반올림 정수) | r3 이슈 1 |
| **FR-15** | **일본어 title/subtitle 0.85배 고정 축소 (Canvas)** — `getTitleScaleByLang(lang)` 신규 함수 (`lang==='ja' ? 0.85 : 1`) · `buildBannerCanvas`에서 `titleFS = Math.round(spec.title.fontSize * scale)`, `subFS = Math.round(spec.subtitle.fontSize * scale)` 적용 | r3 이슈 1 |
| **FR-16** | **title↔subtitle 상하 간격 2→4px 통일 (CSS)** — `.darkbar-text { gap: 2px }` → `gap: 4px` · 사이즈별 분기 없이 공통 적용 | r3 이슈 2 |
| **FR-17** | **title↔subtitle 상하 간격 2→4px 통일 (Canvas)** — `buildBannerCanvas` 내 `const lineGap = 2` → `const lineGap = 4` | r3 이슈 2 |
| **FR-18** | **배치 규격 기본 체크박스 재배치** — HTML에서 9:16 `checked`/`selected` 제거, 1200x628에 추가 · `state.batch.sizes` 초기값 `['1x1', '9x16']` → `['1x1', '1200x628']` | r3 이슈 3 |
| **FR-19** | **배치 언어 기본 체크박스 4개 전체 체크** — HTML에서 ja, zh-TW도 `checked`/`selected` 부여 · `state.batch.langs` 초기값 `['ko', 'en']` → `['ko', 'en', 'ja', 'zh-TW']` | r3 이슈 4 |
| **FR-20** | **사용자 프리셋 localStorage 저장/로드** — key `todayBannerDesigner:customPresets:v1` · 스키마 `{ presets: [{ id, name, createdAt, updatedAt, data: {ko,en,ja,zh-TW}: {title, subtitle, cta, disclaimer} }] }` · 이미지 제외 | r3 이슈 5 |
| **FR-21** | **저장 버튼 UI** — 단건 탭 `#s-download` 바로 위에 `[💾 프리셋 저장]` (`#s-save-preset`) · 배치 탭 `#b-preview` 바로 위에 `[💾 프리셋 저장 (4개 언어 스냅샷)]` (`#b-save-preset`) · 클릭 시 `prompt()`로 이름 입력 | r3 이슈 5 |
| **FR-22** | **프리셋 목록 UI** — 단건: `샘플 프리셋` 영역 아래에 `내 프리셋` grid (버튼 + × 삭제) · 배치: `#b-preset` select에 `<optgroup label="샘플">`/`<optgroup label="내 프리셋">` 병합 + 옆에 `[🗑 삭제]` 버튼 | r3 이슈 5 |
| **FR-23** | **중복 이름 처리 + 삭제 확인** — 같은 이름 저장 시 `confirm()`으로 덮어쓰기 여부 질의 · 삭제 시 `confirm()`으로 최종 확인 | r3 이슈 5 |
| **FR-24** | **단건↔배치 프리셋 상호운용** — 단건 저장 시 현재 언어 slot만 값, 나머지 3개 언어는 빈 문자열 · 단건에서 로드 시 현재 선택 언어의 값으로 복원 · 배치 저장 시 4개 언어 전체 스냅샷 · 배치에서 로드 시 `langOverrides` 전체 복원 + `renderBatchLangFields()` 재렌더 | r3 이슈 5 |
| **FR-25** | **localStorage 실패 방어** — `getCustomPresets`/`saveCustomPresets`에 `try/catch` · 차단/쿼타 초과 시 alert 안내하고 기본 앱 동작은 정상 유지 | r3 이슈 5 (방어적) |

### Non-Functional Requirements

| ID | 내용 |
|----|------|
| NFR-01 | Canvas 출력물의 시각 품질이 사용자 육안 기준 기존 html-to-image 결과물과 "유사" 수준 (픽셀 단위 완벽 일치 아님) |
| NFR-02 | 단건 모드 프리뷰, Shadow UI, hints, 언어 전환 등 기존 UX 무변경 |
| NFR-03 | 기존 배치 프리뷰 동작(HTML DOM scale) 무변경 |
| NFR-04 | Overflow 프리셋 수치(`OVERFLOW_PRESETS`) 무변경 — 기존 제작물 재현성 유지 |
| NFR-05 | 저장된 사용자 오프셋 값이 확장된 범위 밖으로 벗어나지 않음 (현재 ±30/±15/105 → 확장 ±80/±80/200 모두 안전) |
| NFR-06 | 외부 CDN 의존 추가·제거 없음 (FR-08에 따라 html-to-image는 미사용 상태로만 유지) |
| **NFR-07** | r3 변경은 한/영/번체 렌더 결과에 영향 없음 — 일본어 선택 시에만 폰트 축소 적용 (FR-14/15), gap 변경은 전 언어 공통이라 시각 일관성 유지 |
| **NFR-08** | 기존 하드코딩 PRESETS (`underdark`, `necomancer`)는 r3 이후에도 정상 동작 · 사용자 프리셋과 optgroup으로 분리 표시 |
| **NFR-09** | 저장된 프리셋 스키마는 `CP_KEY`에 `:v1` 버전 접미사 포함 · 향후 스키마 변경 시 `:v2` 신설 + 마이그레이션 |

---

## 2. Scope

### 포함
- Canvas 직접 합성 함수 + 사이즈별 설정 테이블 추가
- `handleSingleDownload`, `handleBatchExportZip`, `downloadBatchItem` 경로 교체
- Overflow slider 3개(Scale/X/Y) 범위 확장
- `.banner-overflow-wrap` clip-path + transform 이동
- **(r3)** 일본어 폰트 0.85배 축소 (CSS + Canvas)
- **(r3)** title↔subtitle 간격 2→4px 통일 (CSS + Canvas)
- **(r3)** 배치 기본 규격 `1:1+1200x628`, 기본 언어 4개 전체 체크
- **(r3)** localStorage 기반 사용자 프리셋 저장/로드/삭제

### 제외 (별도 트랙)
- GitHub Pages 배포
- html-to-image 라이브러리 CDN **제거** (검증 안정화 후)
- 이전 코드리뷰 잔존 3건 (slugify/SRI/재진입 가드)
- 새 사이즈·언어·기능 추가
- 단건 모드 프리뷰 및 Shadow UI 재설계

---

## 3. Success Criteria

| ID | 기준 | 검증 방법 |
|----|------|-----------|
| SC-01 | 배치 8장(1200×628 + 1080×1080 × 4언어) ZIP 다운로드 ≤ 2초 | DevTools Performance + `Date.now()` 로깅으로 벽시계 측정 |
| SC-02 | 단건 다운로드 1장 ≤ 0.5초 | 동일 측정 |
| SC-03 | Canvas 출력물이 기존 결과물과 시각적으로 유사 | 동일 입력으로 두 경로 비교 (html-to-image 임시 토글로 검증 가능) — 사용자 육안 승인 |
| SC-04 | 다국어(한/영/일/번체) 텍스트 정상 렌더 | 4언어 각각 렌더 후 글자 깨짐·fallback 없음 확인 |
| SC-05 | Overflow Scale 200% 조정 가능 | 슬라이더 우측 끝 200% 도달 확인 |
| SC-06 | Overflow X/Y ±80% 조정 가능 | 슬라이더 양 끝 ±80 도달 확인 |
| SC-07 | 극단 오프셋(예: Scale 200% + Y +80%)에서도 오버플로우가 darkbar 영역에 침범하지 않음 | DOM 프리뷰 + Canvas 출력 모두 darkbar 위에서 clip 확인 |
| SC-08 | 상·좌·우 방향으로는 overflow wrap 경계를 넘어 자유롭게 이동 | 음수 X/Y로 wrap 상단·좌우 바깥까지 표시 확인 (단 banner 자체 `overflow: hidden`에 의해 최종 클립) |
| SC-09 | Drop Shadow가 Canvas 경로에서도 정상 작동 | Shadow On + 슬라이더 조정 → 다운로드 이미지에 그림자 포함 확인 |
| SC-10 | 단건/배치 프리뷰 동작 무변경 | 기존 UI 상호작용 회귀 없음 |
| **SC-11** | 일본어 선택 + `ソードマスターストーリー` 입력 시 1x1/9:16/1200x628 세 사이즈 모두 title이 CTA 영역 침범 없이 한 줄 표시 | 프리뷰 육안 + Canvas 다운로드 PNG 확인 |
| **SC-12** | 한/영/번체 선택 시 폰트 크기 기존과 동일 (42/56/30, 24/32/17) | 3개 언어 각각 단건 프리뷰 측정 |
| **SC-13** | 전 사이즈 프리뷰에서 title↔subtitle 간격 2→4px로 체감되게 벌어짐 | 육안 Before/After 비교 |
| **SC-14** | Canvas 다운로드 PNG의 title↔subtitle 간격도 DOM 프리뷰와 일치 | 프리뷰 vs 다운로드 이미지 비교 |
| **SC-15** | 배치 탭 최초 진입 시 1:1 + 1200x628만 체크, 9:16 unchecked | UI 확인 |
| **SC-16** | 배치 탭 최초 진입 시 ko/en/ja/zh-TW 4개 모두 체크, `b-lang-fields`에 4개 언어 입력란 렌더 | UI 확인 |
| **SC-17** | 프리셋 저장 → 새로고침 → 저장된 프리셋이 UI 목록에 표시되고 클릭 시 입력값 복원 | localStorage 검사 + 실제 복원 확인 |
| **SC-18** | 같은 이름 저장 시 confirm 팝업 + OK 시 덮어쓰기, 취소 시 변경 없음 | 시나리오 실행 |
| **SC-19** | 🗑 삭제 시 confirm 팝업 + OK 시 목록에서 제거 + localStorage도 반영 | 시나리오 실행 |
| **SC-20** | 기존 하드코딩 `underdark`/`necomancer` 프리셋 r3 이후에도 정상 적용 | 기존 버튼 클릭 테스트 |

---

## 4. Risks & Mitigations

| ID | 리스크 | 영향 | 대응 |
|----|--------|------|------|
| R-01 | Canvas rounded clip으로 카드·다크바 radius 재현 시 픽셀 수준 미세 차이 | 중 | `ctx.roundRect()` (Chrome 98+/Safari 16+/Firefox 131+ 지원) 사용. 미지원 브라우저 드물지만 polyfill path(arc/lineTo 조합) 보조 |
| R-02 | 폰트 로드 전 Canvas 그리기 → fallback 폰트 사용 | 높음 | `await Promise.all([document.fonts.load('900 italic 120px Pretendard'), ...])` 3종 명시 대기 |
| R-03 | Canvas `shadowXXX`와 CSS `filter: drop-shadow()` 블러 반경 해석 미세 차이 | 저 | 블러 값 그대로 사용 + 육안 검증. 차이 크면 상수 보정 (예: 블러 × 1.1) |
| R-04 | 투명 PNG 오버플로우의 drop-shadow가 Canvas에서 정확히 외곽선 따라가지 않을 가능성 | 저 | `drawImage`는 투명 영역을 알파 0으로 처리 → `ctx.shadowXXX`가 자동으로 알파 기반 그림자 생성. 표준 동작이라 정상 작동 예상 |
| R-05 | 다국어 폰트 CDN 차단 환경에서 fallback → Canvas 텍스트도 시스템 폰트 | 저 | `document.fonts.load()` reject 시 경고 메시지만 표시하고 그대로 진행. 기존 html-to-image 방식과 동일 한계 |
| R-06 | Overflow 범위 확장 후 기존 제작물과 프리셋 복원 시 의도치 않은 이동 | 저 | 프리셋(`OVERFLOW_PRESETS`) 값 그대로 유지(NFR-04). 기존 저장값도 확장 범위 내 안전(NFR-05) |
| R-07 | wrap `clip-path` 변경 + transform 이동 시 기존 Shadow filter 적용 위치 달라질 가능성 | 중 | Shadow는 img 자체에 `filter: drop-shadow()`. wrap 이동과 무관하게 img에 적용됨. Canvas 경로도 img 기준 계산이라 일관. 회귀 테스트 필수 |
| R-08 | Canvas 단일 구현으로 배치 통합 완료 후 문제 발견 시 롤백 어려움 | 중 | FR-08에 따라 html-to-image CDN은 유지. 전환 함수를 플래그로 분기 가능하도록 구조화 (예: `USE_CANVAS_EXPORT = true` 상수) → 급할 때 false로 되돌려 html-to-image 경로 복구 가능 |
| **R-09** | r3 CSS `.banner[data-lang="ja"]` selector가 기존 `.banner[data-lang="ja"] { font-family }` rule과 specificity 충돌 | 저 | 신규 rule은 child selector `.game-title`/`.game-subtitle`까지 포함이라 더 specific. 충돌 없음 |
| **R-10** | r3 gap 4px로 `textBlockH` 증가 → darkbar 세로 중앙 정렬 이동 | 저 | Canvas 측 `textBlockY = darkbarY + (db.height - textBlockH)/2`는 동적 계산이라 자동 보정. CSS는 flex align-items로 동적 처리 |
| **R-11** | r3 localStorage 차단 환경 (시크릿 모드, 일부 ITP 설정) | 저 | FR-25의 try/catch로 프리셋 기능만 비활성. 기본 앱 동작 정상 |
| **R-12** | r3 저장된 프리셋 마이그레이션 (스키마 버전업) | 저 | NFR-09의 `:v1` 접미사로 향후 v2 신설 + 마이그레이션 가능 |
| **R-13** | r3 기본값 변경(Item 3/4) 으로 기존 사용자 습관 적응 비용 | 저 | 사내 툴 1명(김성권) 운영, 즉시 안내 가능 |

---

## 5. Architecture Overview

```
today-banner-designer.html
├── CSS
│   └── .banner-overflow-wrap          [FR-12]  clip-path: inset(-9999px -9999px 0 -9999px)
├── HTML
│   ├── #s-overflow-x / y / scale      [FR-09,10,11]  range 속성 확장
│   └── #b-overflow-x / y / scale      [FR-09,10,11]  동일
└── JS
    ├── CANVAS_SPECS[size]             [FR-03]  사이즈별 수치 상수
    ├── ensureFontsLoaded()            [FR-04]  Pretendard/Noto JP/TC 사전 로드
    ├── buildBannerCanvas(cfg)         [FR-01,02,05]  핵심 합성 함수
    │   ├── drawBackground()
    │   ├── drawTodayHeader()
    │   ├── drawProfileIcon()          (1200×628 only)
    │   ├── drawCard()                  (rounded clip + 키아트 drawImage)
    │   ├── drawOverflow()              (shadow 포함, img transform 수치 반영)
    │   ├── drawDarkbar()               (rounded bottom, rgba 배경)
    │   ├── drawAppIcon()
    │   ├── drawGameTitle()             (nowrap, measureText)
    │   ├── drawGameSubtitle()          (nowrap, measureText)
    │   ├── drawCTA()                   (rounded rect border + fillText)
    │   └── drawDisclaimer()            (nowrap, 사이즈별 폰트/위치)
    ├── canvasToDataURL(canvas, format, quality)
    ├── handleSingleDownload()         [FR-06]  → buildBannerCanvas 경로
    ├── handleBatchExportZip()         [FR-06]  → buildBannerCanvas 경로
    ├── downloadBatchItem()            [FR-06]  → buildBannerCanvas 경로
    ├── renderBanner()                 [FR-13]  transform을 wrap → img로 이동
    └── USE_CANVAS_EXPORT = true       [R-08]   플래그로 롤백 여지
```

### r3 추가 아키텍처

```
today-banner-designer.html
├── CSS
│   ├── .banner[data-lang="ja"].size-1x1 .game-title/.game-subtitle    [FR-14]  6 rule
│   ├── .banner[data-lang="ja"].size-9x16 .game-title/.game-subtitle   [FR-14]
│   ├── .banner[data-lang="ja"].size-1200x628 .game-title/.game-subtitle [FR-14]
│   └── .darkbar-text { gap: 4px }                                     [FR-16]
├── HTML
│   ├── batch size checkboxes (9x16 unchecked, 1200x628 checked)       [FR-18]
│   ├── batch lang checkboxes (ja, zh-TW checked)                      [FR-19]
│   ├── #s-save-preset + #s-custom-preset-list                         [FR-21/22]
│   ├── #b-save-preset + #b-preset optgroup + #b-delete-preset         [FR-21/22]
└── JS
    ├── getTitleScaleByLang(lang)                                      [FR-15]
    ├── buildBannerCanvas title/subtitle fontSize × scale, lineGap=4   [FR-15/17]
    ├── state.batch.sizes: ['1x1', '1200x628']                         [FR-18]
    ├── state.batch.langs: ['ko', 'en', 'ja', 'zh-TW']                 [FR-19]
    ├── CP_KEY, CP_LANGS                                                [FR-20]
    ├── getCustomPresets / saveCustomPresets                            [FR-20/25]
    ├── emptyLangSlot / makePresetDataFromSingle / FromBatch            [FR-24]
    ├── savePresetFlow(source)                                          [FR-21/23]
    ├── applyPresetToSingle / applyPresetToBatch                        [FR-24]
    ├── deletePreset(id)                                                [FR-23]
    └── renderPresetListUI()                                            [FR-22]
```

---

## 6. Implementation Order

1. **CANVAS_SPECS 테이블 정의** (FR-03) — CSS 수치를 JS 상수로 이관. 1회 만들면 재활용
2. **ensureFontsLoaded() 유틸** (FR-04) — 3종 폰트 weight/size 조합 load 대기
3. **buildBannerCanvas() 골격** (FR-01) — 배경·카드·키아트만 먼저. 검증 쉬운 단위부터
4. **텍스트 draw 함수들** (FR-02) — Today, 게임명/부제 (measureText 기반 nowrap), CTA, 고지문구
5. **오버플로우 + drop-shadow** (FR-02/05) — shadowXXX 설정 후 drawImage
6. **다크바·아이콘·프로필 아이콘** (FR-02) — rounded clip 재사용, 1200×628 전용 로직
7. **handleSingleDownload + handleBatchExportZip + downloadBatchItem 경로 전환** (FR-06) — 한 함수씩 교체, 각 단계 검증
8. **CSS clip-path 적용** (FR-12) — overflow-wrap 속성 변경
9. **renderBanner transform 이동** (FR-13) — wrap → img, DOM 프리뷰 회귀 확인
10. **Overflow 슬라이더 범위 확장** (FR-09/10/11) — max 속성만 변경
11. **검증** — SC 전 항목 확인 (8장 2초 측정이 핵심)

### r3 구현 순서

12. **Item 3/4 먼저** (FR-18/19, XS 난이도) — HTML checkbox + state 기본값. 리스크 최소 지점부터
13. **Item 2** (FR-16/17, S 난이도) — CSS gap 2→4 + Canvas lineGap 2→4. 전 사이즈 공통
14. **Item 1** (FR-14/15, M 난이도) — CSS ja selector 6 rule + `getTitleScaleByLang` 함수 + Canvas 적용. DOM↔Canvas 결과 일치 확인
15. **Item 5** (FR-20~25, L 난이도) — localStorage 유틸 → 저장 함수 → UI 버튼 → 로드 로직 → 삭제 → `renderPresetListUI`
16. **통합 검증** — SC-11~20 전체 확인 + 기존 SC-01~10 회귀 없음

---

## 7. Critical Files

| 파일 | 변경 영역 |
|------|---------|
| `today-banner-designer.html` | **CSS**: `.banner-overflow-wrap` (157-184) — clip-path 추가 |
| `today-banner-designer.html` | **HTML**: `#s-overflow-x/y/scale`, `#b-overflow-x/y/scale` slider `min`/`max` 속성 변경 (단건 라인 ~498-507, 배치 ~640-649) |
| `today-banner-designer.html` | **JS 추가**: CANVAS_SPECS, ensureFontsLoaded, buildBannerCanvas + draw* 서브루틴 (신규 ~200-300 LOC, 기존 `renderBanner` 섹션 근처에 배치) |
| `today-banner-designer.html` | **JS 수정**: `renderBanner` (870-830 근처, overflow 처리 부분) — wrap.style.transform 제거, img.style.transform으로 이동 |
| `today-banner-designer.html` | **JS 수정**: `handleSingleDownload` (~1073-1097), `handleBatchExportZip` (~1607-1653), `downloadBatchItem` (~1580-1604) — bannerToImage 대신 buildBannerCanvas 호출 |
| `today-banner-designer.html` | **r3 CSS**: line 72-74/94-96/117-119 근처 ja selector 6 rule 추가 (FR-14) · line 205 `.darkbar-text gap: 2→4px` (FR-16) |
| `today-banner-designer.html` | **r3 HTML**: line 552-570 단건 프리셋/저장 UI (FR-21/22) · line 599-601 규격 체크박스 재배치 (FR-18) · line 608-611 언어 체크박스 4개 모두 checked (FR-19) · line 616-625 배치 select optgroup + 삭제 버튼 (FR-22) · line 738 근처 저장 버튼 (FR-21) |
| `today-banner-designer.html` | **r3 JS 추가**: line 817 직후 `CP_KEY`, `CP_LANGS`, 8개 프리셋 함수 (FR-20/22/23/24/25) · line 1121-1125 직후 `getTitleScaleByLang` (FR-15) |
| `today-banner-designer.html` | **r3 JS 수정**: line 837-838 state 기본값 (FR-18/19) · line 1323-1341 title/subtitle fontSize × scale + lineGap (FR-15/17) · `bindSingle`/`bindBatchMode` 이벤트 핸들러 추가 (FR-21/22/23) · DOMContentLoaded에서 `renderPresetListUI()` 호출 |

---

## 8. Verification Plan

1. **기능 검증** (브라우저 수동)
   - 단건 모드: 한국어 "언더다크 : 디펜스" + 1:1 → PNG 다운로드 → 기존 결과와 시각 비교
   - 단건 모드: 일본어 "レベル上げ!" + 9:16 → Noto Sans JP 폰트 적용 확인
   - 단건 모드: 번체 "熱練戰士" + 1:1 → Noto Sans TC 폰트 적용 확인
   - 단건 모드: Overflow 이미지 업로드 + Scale 200%, X +80, Y +80 → darkbar 침범 없음, 상·좌·우 자유 이동 확인
   - 단건 모드: Drop Shadow On → 출력 이미지에 그림자 포함 확인
   - 배치 모드: 1200×628 + 1080×1080 × 4언어 = 8장 프리뷰 생성 → 즉시 표시 (무변경 확인)
   - 배치 모드: ZIP 다운로드 → **실측 시간 측정**
   - 개별 다운로드 버튼 → 단일 PNG 저장 즉시

2. **성능 측정** (SC-01 핵심)
   - `console.time('batch-export')` / `console.timeEnd` 추가(임시) 또는 DevTools Performance 레코딩
   - Before: 현재 html-to-image 버전 기준 측정
   - After: Canvas 버전 측정
   - Target: **≤ 2초** (가급적), 최소 ≤ 5초

3. **회귀 검증**
   - `banner-bugfix` 시나리오(Plan r2) 전부 재실행 — 게임명·부제 한 줄 / 고지문구 한 줄 / 오버플로우 하단 클립 / Shadow 4슬라이더 등
   - 기존 `OVERFLOW_PRESETS` 적용 시 시각 결과 동일

4. **롤백 여부 판단**
   - Canvas 출력 시각 품질이 요구 수준 미달이면 `USE_CANVAS_EXPORT = false`로 전환 → html-to-image 경로 복구

### r3 검증 시나리오 (SC-11~20)

| Item | 시나리오 |
|------|---------|
| 1 (FR-14/15) | 단건·배치 모두 일본어 선택 + `ソードマスターストーリー` / `陰キャ女子は一途属性` 입력 → 1x1/9:16/1200x628 세 사이즈에서 title이 CTA 영역 침범 없음 · 다운로드 PNG에서도 동일 |
| 1 회귀 | 한국어 `언더다크 : 디펜스`·영어 `Underdark: Defense`·번체 `熱練戰士` 각각 → 폰트 크기 기존과 동일 |
| 2 (FR-16/17) | 프리뷰에서 세 사이즈 모두 title↔subtitle 간격이 기존 대비 확실히 벌어짐 (2→4px) · 다운로드 PNG에서도 동일 |
| 3 (FR-18) | 배치 탭 최초 진입 시 `1:1 + 1200x628`만 체크 · `9:16` unchecked · 프리뷰 생성 시 2개 조합만 렌더 |
| 4 (FR-19) | 배치 탭 최초 진입 시 4개 언어 모두 체크 · `#b-lang-fields` 영역에 4개 입력 블록 표시 |
| 5a (FR-20/21/24) | 단건 ko 입력 → `[💾 프리셋 저장]` → 이름 "테스트1" → 저장 → 새로고침 → `내 프리셋` 목록에서 클릭 → ko 필드 복원 |
| 5b (FR-20/21/22/24) | 배치 4개 언어 전체 입력 → `[💾 프리셋 저장 (4개 언어 스냅샷)]` → 이름 "테스트2" → 저장 → 새로고침 → `#b-preset` "내 프리셋" optgroup에서 선택 → "모든 언어에 적용" → 4개 언어 입력란 복원 |
| 5c (FR-23) | 같은 이름 재저장 → confirm 팝업 → OK → 덮어쓰기 성공 (목록에 중복 없음) · 취소 → 변경 없음 |
| 5d (FR-22/23) | 단건 × 또는 배치 🗑 → confirm → 목록에서 사라짐 + localStorage에서도 제거 |
| 5e (NFR-08) | 기존 `언더다크 샘플`, `네코맨서 샘플` 버튼 및 배치 `샘플` optgroup의 `underdark`/`necomancer`도 여전히 정상 동작 |
| 5f (FR-25) | (옵션) localStorage 차단된 시크릿 브라우저에서 프리셋 저장 시도 → alert 안내 + 앱 나머지 기능 정상 |

---

## 9. Out of Scope

- GitHub Pages 배포 (이전 Plan에서 이미 "추후 별도" 결정)
- `html-to-image` CDN 제거 (본 Plan에서는 유지, 검증 안정화 후 별도)
- `slugify` 한글 처리 버그 / CDN SRI 해시 / 배치 재진입 가드 (이전 코드리뷰 건, 별도 트랙)
- 새 사이즈·언어·디자인 요소 추가
- 반응형 모바일 UI 개선

---

## 10. Next Step

사용자 승인 후 `/pdca do bugfix`로 구현 착수, 또는 바로 "일괄 구현" 지시.
단일 파일 국소 변경이 아니라 **신규 함수군(~250 LOC) 추가 + 출력 경로 3곳 교체**이므로 Design 단계를 거칠지 여부는 선택사항. 구현 구조가 위에 명시되어 있어 생략 가능.

**r3 기준 현재 상태**: r2 구현은 완료(Check 100%) · r3는 Plan 확정만 완료, **코드 미수정**. 사용자의 `/pdca do bugfix` 지시 대기 중.
