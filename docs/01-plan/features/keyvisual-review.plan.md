# PDCA Plan — Key Visual + iPhone Review 템플릿 (v1.7)

**Feature**: `keyvisual-review`
**Created**: 2026-05-03
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Skill (used)**: `/plan-plus` → `/pdca plan` (brainstorming via 4 rounds of AskUserQuestion)
**Upstream Doc**: `~/.claude/plans/https-github-com-sungkk1m-mkt-bannerdesi-dynamic-eich.md`

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | Key Visual + iPhone Review 템플릿 (5번째 템플릿) |
| 시작 | 2026-05-03 |
| 본체 파일 | `today-banner-designer.html` (단일 HTML, 6,105 → 추정 6,800라인) |
| 사이즈 | **1080×1080 (1차)** · 9:16/1200×628은 CSS 자리만 열어둠 (disabled) |
| 언어 | ko / en / ja / zh-TW (4개 고정) |
| FR | 12건 |
| NFR | 5건 |
| SC | 8건 |
| R | 6건 |
| 결정사항 | 17건 (Brainstorming 4-round + Open Items 추천값 일괄) |
| Implementation | ~3 sessions (~700라인 추가 + assets 1 PNG) |

### Value Delivered (4관점)

| 관점 | 내용 |
|---|---|
| **Problem** | 게임 광고에서 "리얼 유저 리뷰/평점" 패턴은 신뢰도와 CTR에 강력한 트리거지만, 현재 4언어×1사이즈=4장 생산을 디자이너 외주/수작업에 의존. 앱스토어 캡처 → 텍스트 옮기기 → mockup 합성 → 4언어 번역까지 1~2시간 |
| **Solution** | 키비주얼(배경) + 로고 + iPhone mockup floating + 평점/리뷰 화면을 자동화한 5번째 템플릿. 평점·평가 개수·날짜는 1회 입력 → 단위·포맷이 4언어 자동 변환. 헤드라인은 LANG_PACK 프리셋 선택만으로 즉시 4언어 |
| **Function/UX Effect** | 헤더 드롭다운 "Key Visual + Review" → 1080×1080 자동 활성, 키비주얼/로고 업로드 + scale/x/y slider, 평점·개수·날짜·언어별 리뷰 입력 → 단건 1초 / 배치 4장 ZIP 1.5초. 별점 0.5 단위 자동 채움(4.6→★★★★½), 평가 개수 단위 ko `2.1만` / en `21K` / ja `2.1万` / zh-TW `2.1萬` 자동 |
| **Core Value** | UA 자산 생산 속도 60~120× 향상 + 4언어 운영 자동화 + 앱스토어 신뢰도 모티브 표준화 + 다른 사내 게임 즉시 재활용 가능 |

---

## Context Anchor

> Auto-generated from Executive Summary. Propagated to Design/Do documents for context continuity.

| Key | Value |
|-----|-------|
| **WHY** | 게임 광고에서 평점·리뷰 신뢰도 트리거 자동화 부재 — 디자이너가 4언어×1사이즈=4장 매번 수작업, 앱스토어 캡처 옮기기 시간 소요 큼 |
| **WHO** | UA Manager (사내 마케팅), 잠재적으로 다른 사내 게임 BI 마케터 (게임별 키비주얼만 교체하면 재활용) |
| **RISK** | mockup 화면 영역 좌표 부정확 시 콘텐츠 잘림 (R-1); 별점 0.5 단위 부분 채움 시각 미세 차이 (R-2); 평가 개수 zh-TW `萬` 변환 (R-3); zh-TW 긴 라벨 mockup 좌우 padding 초과 (R-4); 헤드라인 LANG_PACK 비활성화 시 레이아웃 reflow (R-5); 단일 HTML 6,800라인 시 브라우저 로딩 미세 영향 (R-6) |
| **SUCCESS** | 단건 ≤1초, 배치 4장 ZIP ≤2초; 4언어 LANG_PACK 라벨 정확; 별점 5케이스(4.0/4.3/4.5/4.8/5.0) 정밀; 평가 개수 4케이스 단위 변환 정확; 기존 4템플릿 회귀 없음 |
| **SCOPE** | Session 1: PDCA plan + mockup 좌표 분석 / Session 2: PDCA design + 3안 선택 / Session 3: CSS+UI+JS 구현 + ZIP export / Session 4: 검증 + 회귀 + analysis/report |

---

## Context

`today-banner-designer.html`(단일 HTML, v1.6 — SD Showcase 추가 후 6,105라인)는 기존 4개 템플릿(`today-tap`, `app-badge`, `appstore-screenshot`, `sd-showcase`)을 제공한다. 사용자(Mobile Game UA Manager)가 첨부한 5장의 레퍼런스(black iPhone mockup, 와이어프레임 스토리보드, 송오브블루 광고 예시, 앱스토어 평점/리뷰 캡처)를 토대로 **키비주얼이 배경 전체를 덮고 가운데에 black iPhone mockup이 floating되어 그 안에 앱스토어 스타일 평점/리뷰 화면을 보여주는 5번째 템플릿**을 추가한다.

기존 4개 템플릿이 모두 "특정 광고 면(Today Tap 셀, 앱 정보 카드, App Store 스샷, SD 라인업 쇼케이스)"을 모방하는 데 집중된 반면, **Key Visual + Review는 앱스토어 평점/리뷰 페이지의 사회적 증거(social proof)를 게임 키비주얼과 결합**하는 새로운 광고 패턴을 자동화한다. mockup·평점·별점·리뷰는 게임마다 동일 구조이고 키비주얼만 교체하면 즉시 재활용 가능한 형태로 설계한다.

**스킬 매핑**: 추후 비슷한 요청은 `/plan-plus keyvisual-review-v2`로 시작. 보조 — `bkit:phase-3-mockup`(레이아웃 검증), `bkit:phase-5-design-system`(LANG_PACK 일관성).

---

## 사용자 결정 요약 (확정 — 2026-05-03, Brainstorming 4 rounds + Open Items 추천값 일괄)

| # | 항목 | 결정 |
|---|------|------|
| 1 | 템플릿 이름 (헤더 드롭다운) | **"Key Visual + Review"** (key: `keyvisual-review`) |
| 2 | 사이즈 | **1080×1080 우선** (CSS는 9:16/1200×628 자리 비워둠, disabled) |
| 3 | 언어 | ko / en / ja / zh-TW (4개 고정 + 기존 LANG_PACK 폰트 자동 스왑 차용) |
| 4 | 레이아웃 구조 | 배경 전체 = 키비주얼 / 가운데 black iPhone mockup floating |
| 5 | 키비주얼 입력 | 단일 이미지 업로드, scale 50–200%, x/y ±500px |
| 6 | 로고 슬롯 | 키비주얼 위에 별도, 폭 320px 권장, scale 50–150%, x ±200, y -100~+200 |
| 7 | 헤드라인 텍스트 | 키비주얼 위 별도, **4언어 LANG_PACK 프리셋 4세트** + 비활성화 옵션 (비어도 프리뷰 가능) |
| 8 | iPhone mockup | **black iPhone 한 종류만**, 첨부 PNG (사용자 제공) → `repo/assets/keyvisual-review/iphone.png` |
| 9 | mockup 화면 좌표 | PNG 알파 채널 분석으로 자동 추출 → 사용자 검수 |
| 10 | mockup 안 콘텐츠 padding | **32px** (화면 가장자리에서 띄우는 거리) |
| 11 | 평점 박스 디자인 | 앱스토어 자연 흐름 (외곽선/카드 분리 없음) |
| 12 | 평점 표기 | 숫자만 크게 (예: `4.8`, ~120px bold) |
| 13 | 별점 표시 정밀도 | **0.5 단위 부분 채움** (4.6 → ★★★★½, 4.8 → 반올림 5개) |
| 14 | 별점 색상 | 앱스토어 톤 다크 그레이 `#1d1d1f` (사용자 컬러 픽 가능) |
| 15 | "평가 및 리뷰 >" 화살표 | **유지** (앱스토어 모티브) |
| 16 | 부제목 "가장 도움이 되는 리뷰" | **필요 + LANG_PACK 자동** |
| 17 | 평가 총 개수 | **숫자만 공통 입력** + 단위 LANG_PACK 자동 (`21000` → ko `2.1만개의 평가` / en `21K Ratings` / ja `2.1万件の評価` / zh-TW `2.1萬個評價`) |
| 18 | 작성 날짜 | **ISO 입력** → 언어별 자연 표기 자동 (ko `1월 23일`, en `Jan 23`, ja `1月23日`, zh-TW `1月23日`) |
| 19 | 리뷰 카드 개수 | **1개 고정** (와이어프레임) |
| 20 | 리뷰 카드 필드 | 제목, 별점, 날짜, 아이디, 본문 (인물 썸네일 불필요) |
| 21 | 본문 줄 수 | **2줄 고정 + ellipsis(`…`)** |
| 22 | 데이터 입력 UX | **언어별 탭 폼 직접 입력** (공통: 평점/개수/날짜, 언어별: 제목/본문/아이디) |
| 23 | ZIP export | 1080×1080 × 4언어 = **4장 동시 출력** |
| 24 | mockup 자산 보관 | **별도 파일** `repo/assets/keyvisual-review/iphone.png` (HTML inline base64 안 함) |

---

## Functional Requirements (FR)

| # | 요구사항 |
|---|---|
| **FR-1** | 신규 템플릿 `keyvisual-review`를 헤더 드롭다운에 5번째 옵션으로 추가하고, 선택 시 1080×1080 자동 활성·9:16/1200×628 옵션은 disabled |
| **FR-2** | 키비주얼 + 로고 = 2개 레이어. 각각 이미지 업로드 + scale slider + x slider + y slider 제공 |
| **FR-3** | black iPhone mockup이 캔버스 가운데에 floating. 폭 ≈540px, 캔버스 세로 중앙 약간 아래. mockup PNG 알파 채널 분석으로 화면 영역 자동 매핑 |
| **FR-4** | mockup 안 화면(스크린)에 padding 32px로 평점 영역 + 부제목 + 리뷰 카드 1개를 자연 흐름으로 표시 |
| **FR-5** | 평점 영역 = 헤더 "평가 및 리뷰 >" + 평점 숫자(`4.8`, ~120px bold) + 별점 5개(0.5 단위 부분 채움) + 평가 개수 단위 LANG_PACK |
| **FR-6** | 부제목 "가장 도움이 되는 리뷰" 1줄, LANG_PACK 자동 번역 |
| **FR-7** | 리뷰 카드 1개 = 제목(1줄) + 메타 행(별점·날짜·아이디) + 본문(2줄 고정 + ellipsis) |
| **FR-8** | 헤드라인 영역 = 키비주얼 위 별도 텍스트, LANG_PACK 프리셋 4세트 select + 비활성화(빈 값) 가능. 비활성화 시 mockup 위 여백만 남고 reflow 없음 |
| **FR-9** | 데이터 입력: 공통 입력 박스(평점·평가 개수·날짜) 1개 + 언어별 탭(ko/en/ja/zh-TW) 4개 (각 탭에 리뷰 제목·본문·아이디) |
| **FR-10** | 별점 0.5 단위 부분 채움 헬퍼 `renderStars(rating: number)`: 4.0→★★★★☆ / 4.3→★★★★☆ / 4.5→★★★★½ / 4.8→★★★★★ / 5.0→★★★★★ |
| **FR-11** | 평가 개수 LANG_PACK 변환 헬퍼 `formatRatingCount(num: number, lang: string)`: 1500/21000/215000 케이스에서 ko `1.5천/2.1만/21.5만` · en `1.5K/21K/215K` · ja `1500/2.1万/21.5万` · zh-TW `1500/2.1萬/21.5萬` |
| **FR-12** | ZIP export: 사용자가 활성 언어 체크박스 선택 후 "다운로드 ZIP" → 1080×1080 × 선택된 언어 수만큼 PNG 생성 + ZIP 묶음 |

## Non-Functional Requirements (NFR)

| # | 요구사항 |
|---|---|
| **NFR-1** | 기존 4템플릿(today-tap, app-badge, appstore-screenshot, sd-showcase) 회귀 없음 (CSS 셀렉터 충돌 없음, JS 분기 추가만) |
| **NFR-2** | 단일 HTML 파일 패턴 유지. 신규 자산은 `repo/assets/keyvisual-review/iphone.png` 1개만 추가 |
| **NFR-3** | 프리뷰 응답 시간: 입력 변경 → 렌더링 ≤500ms |
| **NFR-4** | ZIP 4장 출력 ≤2초 (html2canvas 기존 사용 패턴 동일) |
| **NFR-5** | 신규 코드 라인 ≤700라인 추가 (CSS ≤300, HTML ≤200, JS ≤200) |

## Success Criteria (SC)

| # | 검증 항목 | 합격 기준 |
|---|---|---|
| **SC-1** | 4언어 LANG_PACK 라벨 정확도 | 헤더 / 부제목 / 평가 개수 단위 / 헤드라인 프리셋 / 날짜 포맷이 ko/en/ja/zh-TW 4언어로 정확히 변환 |
| **SC-2** | 별점 정밀도 | 4.0 / 4.3 / 4.5 / 4.8 / 5.0 입력 시 별 5개 채움 패턴 정확 |
| **SC-3** | 평가 개수 LANG_PACK 변환 | 100 / 1500 / 21000 / 215000 케이스에서 4언어 단위 변환 정확 |
| **SC-4** | 키비주얼/로고 slider | scale·x·y 3개 slider 모두 정상 동작, mockup 가리지 않음 |
| **SC-5** | 헤드라인 비활성화 | 비활성화 시 정상 렌더링 (reflow 없음, 빈 자리만 남음) |
| **SC-6** | 기존 4템플릿 회귀 없음 | 4개 템플릿 각각 ko/en/ja/zh-TW × 활성 사이즈 모두 정상 출력 |
| **SC-7** | ZIP 4장 출력 시간 | 1080×1080 × 4언어 ZIP 묶음 ≤2초 |
| **SC-8** | mockup 화면 영역 정확도 | 첨부 black iPhone PNG에서 추출한 좌표로 콘텐츠가 잘리지 않고 정확히 들어감 (zh-TW 긴 라벨 포함) |

## Risks & Mitigations

| # | 위험 | 완화 |
|---|---|---|
| **R-1** | mockup PNG 알파 채널 분석 부정확 → 콘텐츠 잘림/오프셋 | 자동 추출 좌표를 사용자에게 보고하고 시각 검수 단계 추가; CSS 변수로 분리해 후속 미세 조정 가능 |
| **R-2** | 별점 0.5 단위 부분 채움이 폰트/유니코드 환경에 따라 시각 차이 | linear-gradient 기반 div + ★ 유니코드 마스크 또는 SVG 사용; 5케이스 전부 시각 검증 |
| **R-3** | zh-TW 평가 개수 `萬` 변환 (10,000 단위) 정확도 | 단위 변환 로직 (`Math.floor(n/10000) + 萬`) 4케이스 케이스 테스트 |
| **R-4** | zh-TW 긴 라벨이 mockup 좌우 padding 초과 | `font-size`를 zh-TW에서 0.92× 자동 축소 (기존 ja 시스템과 동일 패턴), 또는 `letter-spacing` 미세 조정 |
| **R-5** | 헤드라인 LANG_PACK 비활성화 시 레이아웃 reflow | `min-height` 고정으로 빈 자리 보존, mockup 위치 변동 없음 |
| **R-6** | 단일 HTML이 6,800라인을 넘으면 브라우저 초기 로딩 미세 영향 | 신규 자산은 외부 PNG로 분리 (base64 inline 안 함). 향후 v2.0에서 모듈 분리 검토 |

## Implementation Phases

| Phase | Session | 범위 | 산출물 | 시간 추정 |
|---|---|---|---|---|
| **1** | Session 1 | PDCA plan 문서 작성 + assets 디렉토리 + mockup PNG 좌표 분석 | 본 문서 + `repo/assets/keyvisual-review/iphone.png` + 좌표 보고 | ~30분 |
| **2** | Session 2 | PDCA design 문서 작성 (Architecture 3안 비교 + 사용자 선택) | `docs/02-design/features/keyvisual-review.design.md` | ~30분 |
| **3** | Session 3 | CSS 클래스 추가 + 입력 폼 UI + JS LANG_PACK + helper 함수 + 렌더링 분기 | `today-banner-designer.html` 수정 (~500라인) | ~60분 |
| **4** | Session 4 | ZIP export 분기 + 검증 + 회귀 테스트 + analysis/report | 검증 결과 + `docs/03-analysis/keyvisual-review.analysis.md` + `docs/04-report/keyvisual-review.report.md` | ~45분 |

총 estimated: ~2.5~3시간 (단발 세션 가능, 분할도 가능)

## Open Items (Plan 승인 후 추가 결정)

> 모두 **추천값 일괄 적용**으로 사용자 결정 완료 (2026-05-03). 구현 후 시각 검수에서 미세 조정 가능.

| # | 항목 | 추천값 (적용 확정) |
|---|---|---|
| 1 | internal key / 표시명 | `keyvisual-review` / "Key Visual + Review" |
| 2 | 로고 슬롯 기본값 | 폭 320px, scale 50–150%, x ±200, y -100~+200 |
| 3 | 헤드라인 프리셋 4세트 | ① Real Player Reviews / 유저 리얼 후기 / プレイヤーの本音レビュー / 玩家真實評價 ② Top Rated / 최고 평점 / 高評価 / 高評價 ③ What Players Say / 유저들이 말하는 / プレイヤーの声 / 玩家評語 ④ 5-Star Reviews / 5점 리뷰 모음 / 5つ星レビュー / 5星評論 |
| 4 | mockup 안 콘텐츠 padding | 32px |
| 5 | 별점 색상 | `#1d1d1f` (앱스토어 다크 그레이) — 사용자 컬러 픽 가능 |
| 6 | "평가 및 리뷰 >" 화살표 | 유지 |
| 7 | mockup 자산 위치 | `repo/assets/keyvisual-review/iphone.png` |

## 다음 단계

1. **사용자 black iPhone PNG 첨부** → `repo/assets/keyvisual-review/iphone.png`로 저장
2. **mockup 좌표 자동 추출** → CSS 변수 (`--kvr-screen-x/y/w/h`) 정의 → 사용자 검수
3. **PDCA design 문서 작성** → Architecture 3안 비교 → 사용자 선택
4. **구현 + 검증** → analysis/report → GitHub push
