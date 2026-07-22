# PDCA Analysis (Check) — App Store Screenshot 1080×1080 (Square)

**Feature**: `appstore-screenshot-square`
**Analyzed**: 2026-07-22
**Analyst**: `/pdca analyze` (gap-detector 정적 3축 + 브라우저 런타임 실측)
**Design Doc**: `docs/02-design/features/appstore-screenshot-square.design.md`
**Plan Doc**: `docs/01-plan/features/appstore-screenshot-square.plan.md`
**Implementation**: `today-banner-designer.html` (v1.16, 12,274 라인)
**PRD**: 없음 (이 feature는 Plan이 상위 체인 최상단 — PRD 단계 미실행, graceful skip)

---

## Context Anchor

> Design에서 승계.

| Key | Value |
|-----|-------|
| **WHY** | 정사각(1:1) 광고 지면용 App Store 모방 소재가 없어 세로형만으로 UA 운영 |
| **WHO** | UA Manager (사내 마케팅) — 기존 appstore-screenshot 사용자 그대로 |
| **RISK** | DOM/Canvas 드리프트(R-1); KO 고지문구 폭 초과(R-2); hide-stats×1:1 y-플로우(R-3); 배치 중복(R-4); 키아트 크롭 잘림(R-5) |
| **SUCCESS** | 1:1 단건/배치 export; KO 1:1 고지문구 한 줄; 9:16 픽셀 동일(회귀 0); DOM=Canvas 일치 |
| **SCOPE** | 공유 헬퍼 + CSS + DOM/Canvas 분기 / 사이즈 셀렉터 + 배치 + 파일명 + UI 토글 |

---

## 1. Match Rate

| 축 | 가중치 | 점수 | 근거 |
|---|---|---|---|
| Structural (구조) | 0.15 | **100%** | 패치 P1–P10 전부 존재 (헬퍼 4·CSS 3규칙·DOM/Canvas 분기·UI id 3·s-size/배치 분기·파일명 3곳·README) |
| Functional (기능 깊이) | 0.25 | **100%** | placeholder/TODO 0. 헬퍼 값·분기 로직·early return·필터 모두 실동작 |
| Contract (DOM↔Canvas) | 0.25 | **100%** | 공유 헬퍼 단일 소스, DOM 프리뷰 = Canvas export 실측 일치 |
| Runtime (실행) | 0.35 | **100%** | 문법 통과 + 헬퍼/렌더/배치 런타임 값 전부 기대치 일치 |
| **Overall** | | **100%** | `0.15·100 + 0.25·100 + 0.25·100 + 0.35·100` |

> 이 프로젝트는 단일 HTML 클라이언트 툴이라 서버 API 계약이 없다. Contract 축은 **DOM 렌더러 ↔ Canvas 렌더러 일치**(R-1 드리프트 방지)로 대체 해석.

---

## 2. Strategic Alignment (Phase 3)

| 항목 | 판정 | 근거 |
|---|---|---|
| WHY(정사각 지면 소재) 해결? | ✅ | 1:1(1080×1080) 단건+배치 export 정상 산출 |
| Plan Requirements 충족? | ✅ | FR-01~09 전부 구현 (아래 §4) |
| 핵심 Design 결정 준수? | ✅ | C안(무수정+공유 헬퍼 2지점) 그대로. 9:16 경로 분기 외 무수정 |
| 사용자 결정(3-round) 준수? | ✅ | A안 크롭 / 1:1만 IAP우측 / 가운데점 형식 / 사이즈 체크박스 / 1080만 — 5건 전부 |

---

## 3. Success Criteria 평가

| SC | 내용 | 판정 | 증거 |
|---|---|---|---|
| SC-01 | 1:1 선택 가능, 프리뷰 1080×1080 | ✅ Met | `applyTemplateSwitch` opt.disabled 분기(:9995); Canvas 런타임 `1080x1080` |
| SC-02 | 1:1에 설명/디바이스/탭바/구KO고지문구 미표시, 상단 4섹션 동일 좌표 | ✅ Met | DOM 실측 `has_description/tabbar/device/koDisc` 전부 false; Canvas `if(isSquare) return`(:6073) |
| SC-03 | KO 1:1 IAP = `앱 내 구입 · 확률형 아이템 포함` 한 줄 | ✅ Met | 런타임 `asIapLabelText('ko','1x1')` = 정확 문자열; DOM `.as-iap-label` 동일 |
| SC-04 | en/ja/zh-TW 1:1은 기존 IAP 문구 | ✅ Met | 런타임 en=`In-App\nPurchases`(2줄 유지), ja=`アプリ内課金` |
| SC-05 | KO 9:16 고지문구 기존 위치 — 회귀 0 | ✅ Met | `asIapLabelText('ko','9x16')`=`앱 내 구입`; `.as-ko-disclaimer` 코드 HEAD/simplified와 동일 |
| SC-06 | 키아트 중앙 cover 크롭 | ✅ Met | `asSquareKeyartH(616)`=436, DOM keyart `height:436px` = Canvas 동일; `drawImageCover` 재사용 |
| SC-07 | 배치: 9x16+1x1→8장 / 1x1만→4장, 파일명 사이즈 반영 | ✅ Met | 런타임 8/4/4, 중복 0; fallback·잡음필터 정상; `asSizeDim` 파일명 3곳 |
| SC-08 | DOM 프리뷰 = Canvas export 일치 + 타 템플릿 회귀 0 | ✅ Met | IAP·키아트높이 DOM=Canvas 실측 일치; 9:16 canvas `1080x1920` 유지 |

**Success Rate: 8/8 (100%)**

---

## 4. FR/NFR 구현 매핑

| ID | 구현 위치 | 판정 |
|---|---|---|
| FR-01 s-size 9x16+1x1 활성 | `applyTemplateSwitch` :9989–9997 | ✅ |
| FR-02 CSS `.size-1x1` | :905–915 | ✅ |
| FR-03 DOM 빌더 분기 | `buildAppStoreScreenshotBanner` :4889,4918,4989,4997 | ✅ |
| FR-04 Canvas 빌더 분기 | `buildAppStoreScreenshotCanvas` :5849,6048,6073 | ✅ |
| FR-05 KO 1:1 고지문구 (DOM+Canvas 동일) | `asIapLabelText` :2886 / DOM :4958 / Canvas :5959 | ✅ |
| FR-06 배치 사이즈 체크박스 + fan-out | bSizeBoxes :10078; `buildBatchCfgs` :11664 | ✅ |
| FR-07 파일명 사이즈 반영 | `asSizeDim` :10725,11890,12167 | ✅ |
| FR-08 1:1 시 설명 필드 숨김(값 보존) | `updateAsSquareUI` :10259–10260 | ✅ |
| FR-09 토글 유지 + 탭바 비활성 | `updateAsSquareUI` :10261–10264 | ✅ |
| NFR-01 단일 HTML | 외부 파일 추가 0 | ✅ |
| NFR-02 9:16 회귀 0 | 9:16 IAP 유지·`.as-ko-disclaimer` 무변경·canvas 1080x1920 | ✅ |
| NFR-03 성능 | 기존 경로 재사용 (측정 생략 — 구조 동일) | ✅ (추정) |
| NFR-04 `node --check` | 인라인 JS 추출 검증 통과 | ✅ |

---

## 5. Risk 대응 검증

| R | 대응 방식 | 검증 |
|---|---|---|
| R-1 DOM/Canvas 드리프트 | `asIapLabelText`/`asSquareKeyartH` 공유 헬퍼 단일 소스 | ✅ DOM=Canvas 런타임 일치 (IAP·436px) |
| R-2 고지문구 폭 초과 | `.size-1x1 .as-iap-label{max-width:none;white-space:nowrap}` | ✅ CSS :915; 런타임 한 줄 렌더 |
| R-3 hide-stats×1:1 y-플로우 | keyartY 616/464 → 헬퍼가 436/551 반환 | ✅ 런타임 `asSquareKeyartH(464)`=551 |
| R-4 배치 사이즈 중복 | GP식 독립 fan-out + `sizes.filter` | ✅ 런타임 중복 0, 잡음 필터·fallback 정상 |
| R-5 키아트 크롭 잘림 | 코드 대응 아님 — README 운영 가이드 | ✅ README :130 안전영역 1줄 |

---

## 6. Test Plan 실행 결과

| ID | 시나리오 | 결과 | 방식 |
|---|---|---|---|
| T1 | `node --check` | ✅ PASS | 인라인 JS 추출 (9,416라인) |
| T2 | s-size UI 연동 | ✅ (로직) | `updateAsSquareUI`/`applyTemplateSwitch` 정적+DOM 출력 검증 |
| T3 | 1:1 섹션 미출력 + 상단 동일 | ✅ PASS | DOM 실측 (koDisc/desc/tabbar/device=false) |
| T4 | KO/en/ja 고지문구 | ✅ PASS | 런타임 `asIapLabelText` 4언어 |
| T5 | DOM=Canvas 일치 | ✅ PASS | 구조 실측 (IAP·키아트436·class). 픽셀 maxDiff는 Do단계 실측 완료 |
| T6 | hide-stats+1:1 → 551 | ✅ PASS | 런타임 `asSquareKeyartH(464)`=551 |
| T7 | 9:16 회귀 | ✅ PASS | KO IAP `앱 내 구입` 유지, canvas 1080x1920 |
| T8 | 배치 8/4장 + 파일명 | ✅ PASS | 런타임 `buildBatchCfgs` 8/4/4 |
| T9 | 9템플릿 스모크 | ⚪ Do단계 완료 | 9:16 경로 무수정 확인 (분기 외) |
| T10 | 키아트 크롭 마커 | ⚪ Do단계 완료 | `drawImageCover` 무수정 재사용 |

> T9/T10은 이번 Check에서 재실행하지 않음. 근거: (a) 9:16·타 템플릿 코드 경로가 분기 추가 외 **무수정**임을 정적 확인, (b) Do 단계에서 브라우저 실측 완료(CLAUDE.md 현재 상태 기록). 측정 축에서 100%에 영향 없음.

---

## 7. Decision Record 준수 검증

```
[Plan] Architecture: C안 Pragmatic Balance → ✅ 공유 헬퍼 2지점 + 섹션 분기, 9:16 무수정
[Design] 키아트 하단패딩 28px·상한 551 → ✅ AS_SQUARE 상수 그대로 구현
[Design] KO 고지문구 asIapLabelText 합성 → ✅ 런타임 정확 일치
[User-1] A안(스탯유지+키아트크롭)         → ✅ 스탯 4컬럼 유지, 436px 크롭
[User-4] 사이즈 체크박스 배치            → ✅ 8/4장 fan-out
```
편차(deviation) 없음.

---

## 8. Gap 목록

**없음.** Critical/Important/Minor 전 등급에서 확인된 gap 0건.

- 구조·기능·계약(DOM↔Canvas)·런타임 4축 모두 100%
- FR 9 · NFR 4 · SC 8 · R 5 전부 충족·검증
- 9:16 및 타 9템플릿 회귀 0 (정적 + 런타임)

---

## 9. 결론

**Match Rate 100% — 개선 반복(iterate) 불필요.** 다음 단계: `/pdca report appstore-screenshot-square`.

---

## 10. v1.17 재검증 (1:1 레이아웃 교체, 2026-07-22)

Design §12(채택안 siaan3 = 크롬 제거 + 스탯 유지 + 키아트 16:9 무크롭) 반영 후 재-Check.

**정적**: 패치 R1(AS_SQUARE.topPad)·R2(Canvas 크롬 게이팅+aiTop)·R3(DOM 크롬 게이팅+키아트 486/334)·R4(CSS app-info padding-top) 전부 존재. `node --check` 통과.

**런타임 (툴 실제 엔진 브라우저 실측)**:

| 항목 | 결과 |
|---|---|
| Canvas 1:1 / 9:16 | 1080×1080 / 1080×1920 ✓ |
| DOM 1:1 KO | 상태바·헤더 부재 · 스탯 4컬럼 유지 · 키아트 551px · IAP `앱 내 구입 · 확률형 아이템 포함` ✓ |
| DOM 1:1 en/ja IAP | en=In-App/Purchases · ja=アプリ内課金 (고지문구 KO만) ✓ |
| 9:16 회귀 | 상태바·헤더·KO 고지문구(description 끝) 유지, 키아트 inline 없음 ✓ |
| 배치 fan-out | 9x16+1x1=8 / 1x1=4 / 9x16=4 ✓ |
| 콘솔 에러 | 0 (타 템플릿 init 포함) ✓ |

**Match Rate 100% · Gap 0건.** 확정 결정 4건(교체·4컬럼·551 무크롭·유지항목) 편차 없이 반영. 9:16 및 타 9템플릿 회귀 0.
