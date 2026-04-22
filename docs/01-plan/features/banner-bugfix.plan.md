# Plan — banner-bugfix

- **Feature**: banner-bugfix
- **Date**: 2026-04-22
- **Status**: Plan
- **Owner**: 김성권 (UA Manager, ksk@superplanet.net)
- **Target**: `today-banner-designer.html` (Today Banner Designer v1.2 → v1.2.1)
- **Revision**: r2 (2026-04-22) — 부제 처리 추가 + Overflow Drop Shadow 기능 추가

---

## Executive Summary

실제 사용 중 발견된 레이아웃/UX 이슈 **6건** + 신규 기능 **1건**(Overflow Drop Shadow)을 해결/추가하여 UA팀 일상 제작 환경에서의 완성도와 표현력을 확보합니다. GitHub Pages 배포는 별도 트랙으로 분리합니다.

| 관점 | 내용 |
|------|------|
| **Problem** | 게임명·부제 `...` 또는 자동 줄바꿈으로 정보 손실, 고지문구 줄바꿈, 오버플로우 하단이 다크바/카드 밖으로 노출, Scale 상한(120%) 부족, 배치 모드에 미리보기 없음 + 속도 저하 — 6건의 UX 블로커 + 캐릭터 그림자 연출 부재로 평면적인 비주얼 |
| **Solution** | ① `.game-title`·`.game-subtitle` 동시 한 줄 강제 + 사이즈별 글자수 힌트 UI / ② `.banner-disclaimer` nowrap + 폰트·위치 재조정 / ③ Overflow wrap bottom을 darkbar 상단에 맞춤 / ④ Scale 슬라이더 max 120→150 / ⑤ 배치 모드 DOM 즉시 프리뷰 + 다운로드 시점에만 이미지 변환 / ⑥ Overflow `filter: drop-shadow()` 4-슬라이더(X/Y/Blur/Opacity) + 사이즈별 독립 저장, 기본 Off |
| **Function UX Effect** | 긴 제목·부제·고지문구도 시안에 온전히 표현. 캐릭터 연출(SD 튀어나옴)이 다크바에 침범하지 않고 의도대로 렌더. 배치 12장 생성 체감 속도 50-70% 개선. SD 캐릭터에 그림자를 추가하여 공간감 있는 비주얼 구현 |
| **Core Value** | UA팀이 "툴 제약 때문에 제작물을 버리는" 상황 제거. 레퍼런스(image 5) 수준 + **그림자 연출**까지 포함한 표현력을 모든 사이즈·언어 조합에서 확보 |

---

## Context Anchor

| 항목 | 내용 |
|------|------|
| **WHY** | 첨부된 실사용 결과물(6건)에서 레이아웃 파손·캐릭터 클립·속도 저하 확인 + 디자인 퀄리티 향상을 위한 그림자 연출 수요. UA 캠페인 집행 전 해소 필요 |
| **WHO** | 사내 UA팀 제작자 (Primary: 김성권) / 사용자: 로컬 브라우저에서 HTML 단일 파일을 여는 마케팅 담당자 |
| **RISK** | html-to-image 렌더 안정성 / DOM 프리뷰와 최종 이미지 간 미세 시각 차이 / 오버플로우 경계 변경 시 기존 프리셋 상호작용 / `filter: drop-shadow()`의 html-to-image 호환성 (일부 브라우저 캡처 시 누락 위험) |
| **SUCCESS** | 6개 이슈 모두 시각 검증 통과 + Drop Shadow 기능 4개 파라미터 정상 동작 + 배치 12장 렌더 시간 50%+ 단축 |
| **SCOPE** | `today-banner-designer.html` 내부 CSS/JS/HTML 수정만. 외부 호스팅·빌드 파이프라인 변경 없음 |

---

## 1. Requirements

### Functional Requirements

| ID | 내용 | 근거 이슈 |
|----|------|-----------|
| FR-01 | `.game-title`에서 `text-overflow: ellipsis` 및 `overflow: hidden` 제거. 한 줄 강제 유지(`white-space: nowrap`)는 유지하되 잘림 없이 전체 텍스트 표시. CTA 버튼 영역으로 침범 허용. | 이슈 1 |
| FR-02 | 단건/배치 모드 게임명 `<input>` 아래에 사이즈별 권장 글자수 힌트 텍스트 추가 (1:1 ~18자 / 9:16 ~15자 / 1200×628 ~14자 한글 기준). 현재 선택 사이즈에 따라 하이라이트 전환. | 이슈 1 |
| FR-03 | `.banner-disclaimer`에 `white-space: nowrap` 추가. 모든 사이즈에서 한 줄 유지. | 이슈 2 |
| FR-04 | 1:1 disclaimer `font-size` 20→16px, `right` 값 레퍼런스(image 5) 대비 현행 40px → 28-32px 범위로 미세 조정. 9:16/1200×628은 nowrap만 적용 후 육안 검증. | 이슈 2 |
| FR-05 | `.banner-overflow-wrap`의 `height` 계산식을 변경하여 bottom이 `.banner-darkbar` 상단과 정렬되도록 축소. (사이즈별 3건 개별 수정) | 이슈 3 |
| FR-06 | `#s-overflow-scale`, `#b-overflow-scale` 슬라이더 `max` 속성 120→150. 기본 프리셋(102~105%) 및 reset 로직은 그대로 유지. | 이슈 4 |
| FR-07 | 배치 모드 "일괄 생성" 클릭 시, 선택된 모든 조합의 banner DOM을 썸네일 그리드에 즉시 렌더(이미지 변환 없음). 사용자는 html-to-image 실행 없이 레이아웃/텍스트/오버플로우를 시각 확인 가능. | 이슈 5 |
| FR-08 | 이미지 변환은 다음 두 시점에만 실행: (a) 썸네일의 "개별 다운로드" 클릭 / (b) "ZIP 다운로드" 버튼 클릭. 즉시 프리뷰 단계에서는 `html-to-image` 호출 없음. | 이슈 5 |
| FR-09 | `waitForImages`의 `setTimeout(r, 80)` 대기를 제거하고 `img.decode()` 기반 대기로 교체(옵셔널: 지원 안 하는 브라우저는 onload 폴백). | 이슈 5 |
| FR-10 | `.game-subtitle`에도 `white-space: nowrap` 추가. `text-overflow` 지정 없음 상태 유지(잘림 없음). 부제가 공간을 넘으면 CTA 영역으로 침범 허용 (title과 동일 정책). | 이슈 7 (신규) |
| FR-11 | 부제 `<input>` 아래에도 사이즈별 권장 글자수 힌트 추가 (1:1 ~24자 / 9:16 ~20자 / 1200×628 ~22자 한글 기준, subtitle이 title보다 작은 폰트라 여유 더 있음). | 이슈 7 (신규) |
| FR-12 | **Overflow Drop Shadow 기능 추가**: `.banner-overflow-img`에 `filter: drop-shadow(Xpx Ypx BLURpx rgba(0,0,0,OPACITY))` 적용. 단건 모드와 배치 모드 모두 구현. | 신규 기능 |
| FR-13 | Drop Shadow UI: On/Off 토글 + 4개 슬라이더 (X: -20\~20px / Y: -20\~20px / Blur: 0\~40px / Opacity: 0\~100%). 단건 모드는 오버플로우 위치 조정 섹션 아래에, 배치 모드도 동일 위치에 추가. | 신규 기능 |
| FR-14 | 배치 모드 Drop Shadow는 **사이즈별 독립 저장** (기존 `overflowPerSize` 패턴과 동일). state에 `shadowPerSize[size] = { enabled, x, y, blur, opacity }` 구조 추가. | 신규 기능 |
| FR-15 | Drop Shadow **기본값은 Off**. 사용자가 토글을 켜야 파라미터 슬라이더가 활성화되고 실제 렌더에 반영됨. 기본 수치 프리셋: `{ x: 0, y: 8, blur: 16, opacity: 40 }`. | 신규 기능 |

### Non-Functional Requirements

| ID | 내용 |
|----|------|
| NFR-01 | 기존 단건 편집 모드는 동작 변경 없음 (게임명 스타일 제외) |
| NFR-02 | 최종 다운로드 이미지의 품질(pixelRatio, JPEG quality 0.95)는 변경하지 않음 |
| NFR-03 | 기존 Overflow 프리셋(`OVERFLOW_PRESETS`) 수치는 그대로 유지하여 기존 제작물 재현성 확보 |
| NFR-04 | 외부 CDN 의존(Tailwind, fonts, html-to-image, jszip) 추가·제거 없음 |
| NFR-05 | Drop Shadow Off 상태에서는 기존 제작물과 픽셀 동일(회귀 없음). 기본값 유지로 자동 적용되지 않음 |

---

## 2. Scope

### 포함
- `today-banner-designer.html` 내부 CSS 섹션 수정 (`.game-title`, `.banner-disclaimer`, `.banner-overflow-wrap`)
- HTML 섹션 수정 (입력 필드 주변 힌트 텍스트, 슬라이더 max 속성)
- JS 수정 (배치 생성 플로우 리팩터링, 이미지 변환 시점 분리)

### 제외 (별도 트랙)
- GitHub Pages 배포 세팅 (사용자 요청에 따라 추후 별도 진행 — 속도 개선 효과 없음 확인됨)
- 이전 코드 리뷰 지적 사항:
  - `slugify` Unicode 플래그 버그 (한글 파일명 손실)
  - CDN SRI 해시 누락
  - 배치 재진입 가드 부재
- 접근성 개선, 다크모드, i18n 확장

---

## 3. Success Criteria

| ID | 기준 | 검증 방법 |
|----|------|-----------|
| SC-01 | 게임명 20자 입력 시 ellipsis 없이 한 줄로 전체 표시 | 단건 모드에서 "Hardcore Leveling Warrior" 입력 후 1200×628 렌더 확인 |
| SC-02 | 게임명 입력란 아래 "권장 ~N자" 힌트 노출, 사이즈 변경 시 갱신 | 단건 모드에서 사이즈 토글하며 힌트 변화 확인 |
| SC-03 | "*확률형 아이템 포함" 고지문구가 1:1/9:16/1200×628 모두 한 줄로 표시 | 단건 모드 3개 사이즈 × 한국어로 각각 렌더 확인 |
| SC-04 | 오버플로우 캐릭터 하단이 다크바 영역에 진입하지 않음 | image 4 시나리오 재현: 세로 긴 SD 캐릭터 업로드 후 1:1 렌더, 다크바 영역에 캐릭터 시각 미노출 확인 |
| SC-05 | Overflow Scale 슬라이더가 150%까지 조정 가능 | 단건/배치 모드에서 슬라이더 우측 끝 150% 도달 확인 |
| SC-06 | 배치 "일괄 생성" 클릭 시 html-to-image 호출 없이 썸네일 그리드 즉시 표시 | 브라우저 DevTools Network/Performance로 이미지 변환 부재 확인 |
| SC-07 | 12장(3사이즈×4언어) ZIP 다운로드 시간이 기존 대비 50% 이상 단축 | 기존 소요 시간 측정 후 대비 |
| SC-08 | 기존 단건 모드 다운로드 결과물(PNG/JPEG)의 픽셀 차이 없음 (Drop Shadow Off 상태) | NFR-02 보존 확인 |
| SC-09 | 부제 "레전드 웹툰 게임" 입력 시 줄바꿈 없이 한 줄 표시, 입력란 아래 권장 글자수 힌트 노출 | 단건 모드 1:1 한국어 렌더 확인 |
| SC-10 | Overflow Drop Shadow 토글 On 시 캐릭터 외곽선을 따라 그림자 생성. 4개 슬라이더 조정 시 즉시 프리뷰 반영 | 단건 모드에서 토글 On → 슬라이더 조정 → 프리뷰 및 다운로드 이미지에 반영 확인 |
| SC-11 | 배치 모드에서 사이즈별 Drop Shadow 다른 값 저장 가능, 사이즈 드롭다운 전환 시 해당 사이즈 값으로 슬라이더 복원 | 배치 모드 1:1=On(강), 9:16=Off 설정 후 사이즈 전환/ZIP 출력으로 독립 저장 확인 |

---

## 4. Risks & Mitigations

| ID | 리스크 | 영향 | 대응 |
|----|--------|------|------|
| R-01 | 긴 게임명이 CTA 버튼 영역으로 침범 → 시각적 불량 | 중 | FR-02 힌트로 사용자에게 안내. 사용자 선택(질문 답변)에 따른 수용 |
| R-02 | DOM 프리뷰와 최종 변환 이미지 간 미세 차이 (폰트 로드 타이밍, CORS 이미지 처리) | 중 | 프리뷰 영역에 "참고용 프리뷰 · 최종 이미지는 다운로드 시 생성"고지 |
| R-03 | 오버플로우 하단 클립 변경 시 기존 프리셋 수치와 시각적 불일치 발생 가능 | 저 | 프리셋 수치 그대로 유지하되 렌더 후 3개 사이즈 각각 육안 검증. 필요 시 프리셋 미세 조정은 후속 |
| R-04 | `img.decode()` 미지원 구형 브라우저에서 프리뷰 오류 | 저 | 폴백: 기존 `onload` 방식. `if (img.decode) img.decode().catch(...); else awaitOnLoad(img);` |
| R-05 | `filter: drop-shadow()`가 html-to-image의 일부 캡처 모드에서 누락되거나 위치가 다르게 렌더될 가능성 | 중 | html-to-image 문서 확인 + 실제 1:1/9:16/1200×628 3가지 사이즈 × Shadow On 조합으로 다운로드 후 이미지에 그림자 반영 여부 검증. 이슈 발생 시 대체안: `::after` 복제 레이어 + `filter: blur()` |
| R-06 | 부제 한 줄 강제로 긴 부제가 CTA 버튼과 시각 간섭 | 저 | FR-11 힌트로 사용자 안내. title 정책과 동일하게 수용 |

---

## 5. Architecture Overview

```
today-banner-designer.html (단일 파일)
├── CSS
│   ├── .game-title              [FR-01]  ellipsis 제거, nowrap 유지
│   ├── .game-subtitle           [FR-10]  nowrap 추가 (신규)
│   ├── .banner-disclaimer       [FR-03,04] nowrap + 사이즈별 폰트/위치
│   ├── .banner-overflow-wrap    [FR-05]  height 축소로 darkbar 상단 정렬
│   └── .banner-overflow-img     [FR-12]  filter: drop-shadow() 동적 적용 (JS로 style 주입)
├── HTML
│   ├── #s-title / #s-subtitle   [FR-02,11]  글자수 힌트 추가 (title+subtitle)
│   ├── #b-title-{lang}, #b-subtitle-{lang}  [FR-02,11]  배치 모드도 힌트
│   ├── #s-overflow-scale        [FR-06]  max=150
│   ├── #b-overflow-scale        [FR-06]  max=150
│   ├── 단건 모드 Shadow 섹션    [FR-13]  On/Off 토글 + 4개 슬라이더 (X/Y/Blur/Opacity)
│   └── 배치 모드 Shadow 섹션    [FR-13]  동일 UI + 사이즈별 저장
└── JS
    ├── handleBatchGenerate      [FR-07,08] 2단계 분리 (프리뷰 → 변환)
    │   ├── renderBatchPreviewDOMs()  새 함수, 이미지 변환 없이 즉시
    │   └── exportBatchAsZip()        기존 로직을 별도 함수로 분리
    ├── waitForImages             [FR-09] img.decode() 전환
    ├── renderBanner()            [FR-12] cfg.shadow 파라미터로 overflow img에 filter 주입
    ├── state.single.shadow       [FR-13] { enabled, x, y, blur, opacity }
    ├── state.batch.shadowPerSize [FR-14] 3개 사이즈 독립 저장
    ├── bindSingleShadow()        [FR-13] 신규 이벤트 바인딩
    ├── bindBatchShadow()         [FR-13,14] 신규 이벤트 바인딩 + 사이즈 전환 로직
    └── SHADOW_DEFAULT            [FR-15] { enabled: false, x: 0, y: 8, blur: 16, opacity: 40 }
```

---

## 6. Implementation Order

1. **CSS 수정** (FR-01, FR-03, FR-04, FR-05, FR-10) — 국소, 빠른 검증 가능
2. **HTML max 속성 + 힌트 추가** (FR-02, FR-06, FR-11) — title + subtitle 힌트 UI
3. **JS 슬라이더 상한 150% 동기** (FR-06) — 라벨 업데이트 코드 `%` 기반이라 무변경 예상
4. **Drop Shadow 기능 추가** (FR-12 ~ FR-15)
   - 상태 구조: `state.single.shadow`, `state.batch.shadowPerSize` 정의
   - 단건 모드 UI: 사이드바에 Shadow 섹션 삽입 + 이벤트 바인딩
   - 배치 모드 UI: 사이즈별 편집 드롭다운과 연동 + 이벤트 바인딩
   - `renderBanner()`에서 `cfg.shadow` 수신하여 `filter: drop-shadow(...)` inline style 주입
5. **JS 배치 모드 리팩터링** (FR-07, FR-08, FR-09) — 가장 큰 변경
   - `handleBatchGenerate`를 두 단계로 분리
   - 썸네일 카드의 "개별 다운로드" 버튼에 변환 지연 로직 바인딩
   - ZIP 다운로드 버튼은 모든 조합 변환 후 ZIP 생성
6. **검증** — 7개 이슈 + Drop Shadow 시나리오 재현 + 12장 배치 속도 측정 + Shadow가 html-to-image 출력에 반영되는지 확인

---

## 7. Critical Files

| 파일 | 변경 영역 (예상 라인) |
|------|---------------------|
| `today-banner-designer.html` | **CSS**: 205-213 (.game-title), 215 (.game-subtitle), 228-236 (.banner-disclaimer), 156-183 (.banner-overflow-wrap) |
| `today-banner-designer.html` | **HTML**: 449-452 (s-title/subtitle 힌트), 471-479 (s-drop-overflow), 490-508 (Shadow 섹션 신규 삽입), 505 (s-overflow-scale max), 593-620 (배치 입력/오버플로우), 622-649 (배치 Shadow 섹션 신규 삽입), 647 (b-overflow-scale max) |
| `today-banner-designer.html` | **JS**: 719-766 (state + SHADOW_DEFAULT 신규), 771-820 (renderBanner — shadow 적용 로직 추가), 958-1017 (bindSingleMode — Shadow 바인딩 추가), 1118-1168 (bindBatchMode — Shadow 바인딩 추가), 1099-1105 (waitForImages), 1291-1370 (handleBatchGenerate) |

---

## 8. Verification Plan

1. **기능 검증** (브라우저)
   - 단건 모드: 긴 제목("Hardcore Leveling Warrior") → 한 줄 표시 + 힌트 노출
   - 단건 모드: 긴 부제("레전드 웹툰 게임") → 한 줄 표시 + 힌트 노출
   - 단건 모드: 한국어 고지문구 → 1:1/9:16/1200×628 모두 한 줄
   - 단건 모드: 세로 긴 SD 캐릭터 업로드 → 다크바에 침범 없음
   - 단건 모드: Scale 슬라이더 150%까지 드래그 가능
   - 단건 모드: Drop Shadow 토글 On → 슬라이더 조정 → 프리뷰 즉시 반영 → 다운로드 이미지에 그림자 포함
   - 배치 모드: 2x2x2 조합(2사이즈×2언어) 클릭 → 썸네일 즉시 표시
   - 배치 모드: 개별 다운로드 버튼 → 변환 후 단일 PNG 저장
   - 배치 모드: ZIP 다운로드 → 모든 조합 변환 완료 후 ZIP
   - 배치 모드: 1:1=Shadow On(강), 9:16=Off 설정 후 ZIP 출력 → 사이즈별 독립 적용 확인

2. **성능 측정**
   - 3사이즈 × 4언어 = 12장 조건 설정
   - DevTools Performance 탭으로 이전 버전 vs 신버전 기록 비교
   - ZIP 완료까지 경과 시간 wall-clock 기록

3. **회귀 검증**
   - 이전 버전에서 만든 제작물(첨부 이미지 3, 4, 5)과 동일 입력으로 렌더 후 시각 비교
   - `OVERFLOW_PRESETS` 값 동일 확인

---

## 9. Out of Scope (명시적 제외)

- GitHub Pages 배포 (사용자 결정: 나중에 별도 진행)
- `slugify` 한글 처리 버그 수정 (이전 코드 리뷰 건, 별도 트랙)
- CDN SRI 해시 추가 (이전 코드 리뷰 건, 별도 트랙)
- 배치 재진입 가드 (이전 코드 리뷰 건, 별도 트랙)
- 새 사이즈·언어 추가
- 반응형 모바일 UI 개선

---

## 10. Next Step

사용자 승인 후 `/pdca design banner-bugfix`로 Design 단계 진행, 또는 바로 코드 수정 지시.
(수정 대상이 단일 파일 내 국소 변경이므로 Design 단계 생략하고 바로 Do로 넘어가도 무방)
