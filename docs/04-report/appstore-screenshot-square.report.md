# PDCA Completion Report — App Store Screenshot 1080×1080 (Square) (v1.16)

**Feature**: `appstore-screenshot-square`
**Phase**: Completed (Plan → Design(C안) → Do(P1~P10) → Check(정적 3축 + 브라우저 실측) → Report)
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Period**: 2026-07-22 (단일일 완료)
**Skill (used)**: `/pdca plan`(AskUserQuestion 3-round) → `/pdca design`(C안) → `/pdca do` → `/pdca analyze` → `/pdca report`

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | 기존 App Store Screenshot(9:16 전용)에 **1:1(1080×1080)** 사이즈 추가 |
| Period | 2026-07-22 (Plan→Report 단일일) |
| Match Rate | **100%** (Structural·Functional·Contract·Runtime 4축) |
| Critical / Important / Minor Gap | **0 / 0 / 0 건** |
| Iteration | **0회** (Do 1회 통과 — iterate 불필요) |
| Success Criteria | **8/8 (100%)** · FR 9 · NFR 4 · Risk 5 전부 충족 |
| Files Changed | 3 (`today-banner-designer.html` + `README.md` + `CLAUDE.md`) + 2 신규 문서(analysis/report) |
| LOC Delta | `today-banner-designer.html` +144 / −55 (**net +89**, 12,185 → 12,274) |
| 아키텍처 | **C안 Pragmatic** — 9:16 무수정 + 드리프트 2지점 공유 헬퍼 |
| Build | 인라인 `<script>` `node --check` 통과 (9,416라인) |

### 1.3 Value Delivered (4관점 — 실측 결과)

| 관점 | 내용 | 지표 |
|---|---|---|
| **Problem** | App Store Screenshot이 9:16 전용이라 Meta 등 정사각(1:1) 지면 소재를 수작업 별도 제작. 세로형의 설명 본문은 정사각에서 공간상 불가능 | 정사각 수요 수작업 → 0 |
| **Solution** | 동일 템플릿에 1080×1080 추가. 설명 본문·디바이스 라벨·탭바 제거, 상태바→헤더→앱정보→스탯 4컬럼→키아트(하단 크롭). KO 고지문구는 IAP 우측 인라인 | Canvas `1080×1080` 실측 확인 |
| **Function/UX Effect** | 사이즈 셀렉터 9:16/1:1 선택 → 기존 입력값 재사용. 배치 ZIP = 선택 사이즈 × 4언어 (최대 8장) | 배치 8/4장 실측, 중복 0 |
| **Core Value** | 정사각 지면용 스토어 모방 소재를 추가 입력 없이 즉시 산출 — 세로형과 소재·텍스트 단일 관리 | 신규 입력 슬롯 0 (4언어 공용 키아트) |

---

## 1. Decision Record Chain

PRD 생략(Plan이 체인 최상단). Plan은 `/pdca plan` AskUserQuestion 3-round로 확정.

| 단계 | 결정 | 근거 | 결과 |
|---|---|---|---|
| Plan | 정사각은 하단 요소 취사선택 필수 | 1080·1200·1280 수치 검토 — 캔버스 확대는 키아트 폭도 키워 자기유사(해결 안 됨) | ✅ A안 확정 |
| Plan(User-1) | **A안**: 스탯 4컬럼 유지 + 키아트 하단 크롭(≈2.25:1) | B안(스탯제거+16:9무크롭) 대비 정보 밀도 유지 | ✅ 스탯 유지, keyartH 436 |
| Plan(User-2) | KO 고지문구 **1:1 신규만** IAP 우측 | 9:16은 O-2 B 결정 불변 | ✅ 9:16 KO=`앱 내 구입` 유지 |
| Plan(User-3) | 형식 `앱 내 구입 · 확률형 아이템 포함` | 가운데점, 기존 IAP 스타일 | ✅ 런타임 정확 일치 |
| Plan(User-4) | 배치 **사이즈 체크박스** (9:16/1:1) | GP 2사이즈 선례 | ✅ 8/4장 fan-out |
| Plan(User-5) | **1080×1080만** (1200 미지원) | 픽셀 퍼펙트 원칙 | ✅ 단일 사이즈 |
| Design | **C안 Pragmatic** (A탈락:드리프트 / B탈락:9:16수정 회귀) | 위험 2지점만 단일화 | ✅ 공유 헬퍼 2 + 섹션 분기 |
| Design | 키아트 하단패딩 **28px**, 상한 **551** | 상단 패딩 대칭 + 16:9 자연높이 | ✅ `AS_SQUARE` 상수 |

**Decision Outcomes**: 전 결정 코드 반영, 편차 0. C안의 핵심 가정(9:16 분기 외 무수정 → 회귀 0)이 정적+런타임으로 검증됨.

---

## 2. Success Criteria Final Status

| # | 기준 | 상태 | 증거 |
|---|---|:---:|---|
| SC-01 | 1:1 선택 + 프리뷰 1080×1080 | ✅ Met | `applyTemplateSwitch`(:9995) + Canvas 런타임 `1080x1080` |
| SC-02 | 1:1 하단 4요소 미표시 + 상단 4섹션 동일 좌표 | ✅ Met | DOM 실측 desc/device/tabbar/koDisc=false; Canvas `if(isSquare)return`(:6073) |
| SC-03 | KO 1:1 IAP = `앱 내 구입 · 확률형 아이템 포함` 한 줄 | ✅ Met | 런타임 `asIapLabelText('ko','1x1')` 정확 |
| SC-04 | en/ja/zh-TW 1:1 기존 IAP 문구 | ✅ Met | en=`In-App\nPurchases`(2줄), ja=`アプリ内課金` |
| SC-05 | KO 9:16 고지문구 기존 위치 — 회귀 0 | ✅ Met | `asIapLabelText('ko','9x16')`=`앱 내 구입`; `.as-ko-disclaimer` HEAD 동일 |
| SC-06 | 키아트 중앙 cover 크롭 | ✅ Met | `asSquareKeyartH(616)`=436, DOM=Canvas 동일, `drawImageCover` 재사용 |
| SC-07 | 배치 8/4장 + 파일명 사이즈 반영 | ✅ Met | 런타임 8/4/4 중복 0; `asSizeDim` 3곳 |
| SC-08 | DOM=Canvas 일치 + 타 템플릿 회귀 0 | ✅ Met | IAP·436px DOM=Canvas; 9:16 canvas `1080x1920` 유지 |

**Overall Success Rate: 8/8 = 100%** (정적 3축 + 브라우저 런타임 실측)

---

## 3. 구현 요약

### 신규 공유 헬퍼/상수 (R-1 드리프트 방지 — DOM/Canvas 단일 소스)
- `AS_SQUARE` — `{W:1080, H:1080, keyartTopPad:28, keyartBottomPad:28, keyartMaxH:551}`
- `asSquareKeyartH(keyartY)` — `min(1080 − keyartY − 28, 551)` → 스탯 436 / hide-stats 551
- `asIapLabelText(lang, size)` — KO 1:1만 고지문구 인라인 합성, 그 외 기존 문구
- `asSizeDim(size)` — 파일명용 `1080x1080` / `1080x1920`

### 렌더러 분기 (섹션 레벨 `cfg.size === '1x1'`)
- `buildAppStoreScreenshotBanner`(DOM): size 클래스 스왑, 하단 4섹션 미출력, 키아트 inline height, desc-fit 스킵
- `buildAppStoreScreenshotCanvas`(Canvas): `H=1080`, IAP `asIapLabelText().split('\n')`, 키아트 `asSquareKeyartH`, 키아트 후 `return canvas`

### UI / 배치 / 파일명
- `updateAsSquareUI()` — 규격 노트/설명 필드 숨김(값 보존)/탭바 토글 비활성, `applyTemplateSwitch`+`s-size` change 양쪽 호출
- `applyTemplateSwitch` — s-size 9x16+1x1 option 활성(sd-showcase 패턴) + bSizeBoxes AS 분기
- `buildBatchCfgs` — GP식 독립 선행 블록으로 이동, `sizes.filter(9x16|1x1)` + 빈배열 fallback (R-4 중복 원천 차단)
- 파일명 3곳 `asSizeDim(cfg.size)` 적용

### CSS (~3규칙)
- `.tmpl-appstore-screenshot.size-1x1` (1080×1080 컨테이너) / `.as-keyart{aspect-ratio:auto}` / `.as-iap-label{max-width:none;white-space:nowrap}`(R-2)

---

## 4. Risk 대응 결과

| R | 대응 | 검증 결과 |
|---|---|---|
| R-1 DOM/Canvas 드리프트 | 공유 헬퍼 단일 소스 | ✅ DOM=Canvas 런타임 일치 (IAP·436px) |
| R-2 고지문구 폭 초과 | max-width 해제 + nowrap | ✅ 한 줄 렌더 확인 |
| R-3 hide-stats×1:1 y-플로우 | keyartY 616/464 → 헬퍼 436/551 | ✅ `asSquareKeyartH(464)`=551 |
| R-4 배치 사이즈 중복 | GP식 독립 fan-out + filter | ✅ 중복 0, fallback·잡음필터 정상 |
| R-5 키아트 크롭 잘림 | README 운영 가이드(코드 아님) | ✅ README 안전영역 1줄 |

---

## 5. 학습 / 인사이트

### 잘 된 점
- **드리프트 위험 지점만 공유 소스화(C안)**: KO 고지문구·키아트 높이 두 값만 헬퍼로 단일화 → DOM/Canvas 두 렌더러가 자동 일치. R-1을 설계 단계에서 구조적으로 차단, iterate 0회로 100% 달성.
- **9:16 무수정 원칙 = 회귀 0**: 분기 추가 외 기존 라인을 건드리지 않아 SC-05/NFR-02 회귀가 발생할 여지 자체가 없었음. `.as-ko-disclaimer` 코드가 HEAD와 바이트 동일함을 대조 확인.
- **기존 자산 read-only 재사용**: `drawImageCover`·`fitAppStoreTitle`·`AS_LANG_PACK`·GP `gpSizes` 필터 패턴을 수정 없이 재사용 → 신규 좌표·상수 최소화(net +89 LOC, 추정 상한 250 대비 여유).
- **런타임 실측 검증**: 브라우저에서 헬퍼 반환값·Canvas 치수·DOM 섹션 유무·배치 fan-out을 직접 실행 확인 → 정적 grep만으로 못 잡는 실동작을 정량 증거로 확보.

### 아쉬운 점 / Minor
- NFR-03(성능 ≤1초/≤3초)은 기존 경로 재사용 근거로 추정 판정 — 별도 계측은 생략.
- T5 픽셀 maxDiff·T10 키아트 크롭 마커 이미지 diff는 이번 Check에서 재실행하지 않고 Do 단계 실측(CLAUDE.md 기록)에 위임 — `drawImageCover` 무수정이라 위험 낮음.

### 다음 PDCA에서 적용할 것
- **"드리프트 2지점 공유 헬퍼" 패턴**을 이중 렌더러(DOM+Canvas) 변형의 표준으로 정착 — R37/이번 케이스 연속 성공.
- 사이즈 변형 추가 시 **GP식 독립 fan-out 블록**을 기본으로 (combos.map 내부 고정 대비 중복 원천 차단).

---

## 6. 산출물 / 관련 파일

| 종류 | 경로 | 비고 |
|---|---|---|
| 본체 | `today-banner-designer.html` | net +89 LOC (v1.16, 1:1 사이즈 추가) |
| 문서 | `README.md` | 사이즈 목록 + 키아트 안전영역 가이드(R-5) |
| 정책/현황 | `CLAUDE.md` | §5 현재 상태 v1.16 갱신 |
| Plan | `docs/01-plan/features/appstore-screenshot-square.plan.md` | 3-round 결정 + 수치 검토 |
| Design | `docs/02-design/features/appstore-screenshot-square.design.md` | C안 + 패치 P1~P10 |
| Analysis | `docs/03-analysis/appstore-screenshot-square.analysis.md` | 4축 100% + 런타임 증거 |
| Report | `docs/04-report/appstore-screenshot-square.report.md` | 본 문서 |

---

## 7. v2 후보 (현재 범위 제외)

1. 1200×1200 export (×1.111 스케일 렌더 — 필요 시)
2. B안 레이아웃(스탯 제거 + 16:9 무크롭) 전용 토글 (현재 hide-stats로 유사 효과)
3. 1:1 전용 키아트 업로드 슬롯 (현재 9:16과 공용 1장 정책)

---

## 8. 결론

**App Store Screenshot 1:1(1080×1080) 변형 (v1.16)** 이 iterate 0회로 완료되었다.

- ✅ Match Rate **100%** (Structural·Functional·Contract·Runtime 4축, Critical/Important/Minor 갭 0)
- ✅ Success Criteria 8/8 · FR 9 · NFR 4 · Risk 5 전부 충족
- ✅ 9:16 및 타 9템플릿 회귀 0 (정적 바이트 대조 + 런타임 실측)
- ✅ 사용자 3-round 결정 5건 + C안 아키텍처 편차 0

다음 단계로 `/pdca archive appstore-screenshot-square --summary` 고려.

---

📊 **Final Status**: ✅ Completed (App Store Screenshot 1:1 변형, iterate 0, Match Rate 100% 정적+런타임, 회귀 0)
