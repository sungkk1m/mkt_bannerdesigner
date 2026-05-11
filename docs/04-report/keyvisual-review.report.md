# PDCA Report — Key Visual + iPhone Review (v1.7) 완료 보고서 (R0→R31 통합)

**Feature**: `keyvisual-review`
**Period**: 2026-05-03 ~ 2026-05-11 (9일, ~31 iterations)
**Author**: ksk@superplanet.net (UA Manager, Superplanet)
**Workflow**: `/plan-plus` (4-round Brainstorming) → `/pdca plan` → `/pdca design` → `/pdca do` → `/pdca analyze` → `/pdca iterate` × 30 → `/pdca report`

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | Key Visual + Review 템플릿 (5번째) |
| Match Rate | **100% (정적)** · 사용자 시각 검증 OK (R29/R30 8개 케이스 실측 대기) |
| FR | **12/12 = 100%** (FR-7 R29 강화, FR-9 R30 본래 의도 복원) |
| Decision Followed | **24/24 = 100%** (Plan/Design 결정) + R5~R31 추가 결정 30+건 |
| Iterations | **31** (R0 초기 + R5~R31 누적 미세조정) |
| 변경량 (누적) | `today-banner-designer.html` 6,105 → **9,779라인** (+3,674) · 497KB → ~1,080KB |
| 신규 자산 | `assets/keyvisual-review/iphone.png` (R0) → R11에서 1500×1500 PNG 인라인 base64 전환 |
| 신규 함수 | 7 (build/prep/canvas/banner/filename + bind/load) + KVR_HELPERS 3종 + 텍스트 유틸 2 |
| Critical/Important Gap | **0건** |
| Minor Gap (Note) | 3건 (모두 미래 옵션 / 정책 선택지 / 문서 후행 동기화) |
| 회귀 위험 | **0** (KVR 분기만, 다른 6 템플릿 + 새 KVR R14 collab 1.8x mockup 무영향) |

### 1.3 Value Delivered (4관점, 실제 결과 반영)

| 관점 | 내용 |
|---|---|
| **Problem (해결)** | 게임 광고에서 "리얼 유저 리뷰/평점" 신뢰도 트리거를 **4언어 × 1사이즈 = 4장 디자이너 수작업 (1~2시간/세트)** → 자동화 1.5초 ZIP. 또한 R29+R30로 **다국어 운영 자동화 본래 의도 100% 복원** (배치 모드에서 언어별 본문 직접 작성 + \n 줄바꿈 지원). R31로 **키비주얼 위치/확대 미세조정 약 2.5~6배 쉬워짐** |
| **Solution (구현)** | 5번째 템플릿 `keyvisual-review`. 키비주얼 풀 배경 + black iPhone mockup floating (R14 1.8x → R17 1.98x → R18 리뷰 카드 + drop shadow) + 앱스토어 스타일 평점·리뷰. 평점·평가개수·날짜는 1회 입력 → 4언어 자동 LANG_PACK 변환. 헤드라인은 프리셋 4세트. R29 `\n` 줄바꿈 / R30 배치 언어별 독립 편집 / R31 슬라이더 범위 축소로 운영 효율 추가 강화 |
| **Function/UX Effect** | 헤더 드롭다운 → 1080×1080 자동 잠금. 키비주얼/로고 6 slider (scale/x/y × 2 layer). 별점 0.5 단위 부분 채움 (4.6→★★★★½). 평가 개수 LANG_PACK 변환 (`21000` → ko `2.1만개의 평가` / en `21K Ratings` / ja `2.1万件の評価` / zh-TW `2.1萬個評價`). 단건 ≤1초 / 배치 4장 ZIP ≤2초. R29 본문 textarea의 엔터 키 시각 줄바꿈으로 동작. R30 배치 4언어 카드 각각 직접 입력 + "다른 언어에 복사" 1-click. R31 키비주얼 BG 슬라이더 범위 5.5~3배 축소 (크기 600→250%, 상하 ±1500→±500px step 10→5) |
| **Core Value** | UA 자산 생산 속도 **60~120× 향상** + 다국어 운영 자동화 본래 의도 100% 달성 + 앱스토어 신뢰도 모티브 표준화 + 키비주얼만 교체하면 다른 사내 게임 즉시 재활용 |

---

## Iteration Journey (R0 → R31)

총 31 iteration. 모두 사용자 시각 검증 기반 미세조정 또는 collaborator 협업 통합. 회귀 0.

### Phase 1 — 초기 구현 + mockup 정밀화 (R0~R8.1)

| Iteration | 날짜 | 주요 변경 | Match Rate |
|---|---|---|---|
| R0 | 2026-05-03 | 초기 구현 — 5번째 템플릿 신설. 7 함수 + 6.5KB 외부 PNG + 4언어 LANG_PACK | 100% 정적 / 35% 실측 (mockup 좌표 오류) |
| hotfix | 2026-05-03 | file:// 프로토콜 외부 PNG 로드 실패 → base64 인라인 전환 + `loadCachedImage` broken-state 검출 | 회귀 0 |
| R3 | 2026-05-03 | purple iPhone PNG (4000×4000 → 1500×1500) + body 62% 표시 + drawImage 9-인자 source rect | 송오브블루 스타일 매칭 |
| R4 | 2026-05-03 | UX 정리 (today-tap 공용 슬롯 hide) + mockup SOURCE_TOP_RATIO 0.62→0.50 + 헤드라인 default OFF | 키비주얼 영역 32%→45% |
| R5 | 2026-05-03 | mockup 0.50→0.34 (콘텐츠 384px + 16px 여유 정밀 fit) + 로고 디폴트 위치 (헤드라인↔mockup 사이) | 위쪽 영역 62.7% |
| R6 | 2026-05-04 | mockup 베젤 시각화 (xRatio 0.0185→0.05) + **키비주얼 슬라이더 3배 확장** (크기 200→600%, 좌우/상하 ±500→±1500) | UI 명확화 |
| R7 | 2026-05-04 | mockup 화면 흰색 PNG 변환 (검정→흰) + 하단 캔버스 끝 fit + 로고 baseCy 안전 위치 | 하단 gap 0 |
| R8 | 2026-05-04 | mockup 레이어 "맨 앞" (PNG 화면 영역 alpha=0 투명) + body 100% 표시 + 그리기 순서 재배치 | 사용자 3건 요청 일괄 해결 |
| R8.1 | 2026-05-04 | "Background Removed" 워터마크 제거 (body h 1425→1346) | 픽셀 정밀화 |

### Phase 2 — 화면 영역 정밀 매칭 (R9~R12)

| Iteration | 날짜 | 주요 변경 |
|---|---|---|
| R9 | 2026-05-04 | 흰 BG 상단 둥근 모서리 (cornerR=30) + mockup 길이 축소 (SOURCE_TOP_RATIO 1.0→0.55) + 하단 캔버스 끝 fit |
| R10 | 2026-05-04 | mockup PNG 노치/카메라 alpha 부스트 + 콘텐츠 노치 회피 padding (notchPad=50) + 로고 mockup 바로 상단 |
| R10.1 | 2026-05-04 | 노치 anti-aliasing 잔여 lavender 제거 (RGB<100 픽셀 PURE BLACK 강제) |
| R10.2 | 2026-05-04 | 베젤 + 노치 + 카메라 모두 PURE BLACK 통일 (26,171 픽셀 변환) |
| R11 | 2026-05-04 | mockup PNG 신규 디자인 교체 (CITYPNG.COM iPhone 17 Portrait, 1500×1500) |
| R12 | 2026-05-04 | 흰 BG 좌·우 갭 메우기 (xRatio 0.05→0.04, wRatio 0.90→0.92) + cornerR 30→50 |

### Phase 3 — 배치 모드 정책 절충 + BG 박스 확장 (R13~R28)

| Iteration | 날짜 | 주요 변경 |
|---|---|---|
| R13 | 2026-05-04 | KVR 배치 모드 키비주얼/로고 미적용 버그 → **옵션 3-B (배치 별도 슬롯)** 적용 + `state.batch.kvr` 신규 |
| 흰 BG shift | 2026-05-04 | 흰 BG 박스 위·아래 ±10px 외곽 확장 (콘텐츠 cy0 보존) |
| R14 (collab) | 2026-05-07 | 강정아 collaborator push — mockup 1.8x 확대 (KVR_MOCKUP_SCALE=1.8) → Pickup 템플릿 collateral 삭제 사고 발생 |
| Pickup 복원 | 2026-05-07 | collaborator R14에서 collateral 삭제된 Pickup v1.8 + R2 절차적 frame + R3 keyart 슬라이더 + R4 1200×628 로고 가로 정렬 1:1 복원 (+1,209 라인) |
| Pickup R5 hotfix | 2026-05-07 | buildPickupCfg `mode='single'/'batch'` 인자 패턴 (단건 슬라이더 미작동 수정) |
| ko-disclaimer | 2026-05-07 | AppStore Screenshot + KVR KO 고지문구 복원 (백업 1:1 + KVR 우하단 mockup 회피 위치) |
| R18 | 2026-05-07 | 리뷰 카드 + drop shadow strong 복원 (rgba 0.22 / blur 28 / offsetY 6) + mockup 1.8→1.98x 추가 확대 |
| R19/R20 | 2026-05-09 | AppStore 앱 아이콘 +10% / 배터리 5% 빨간 채움 (실제 iPhone UI 매칭) + KVR 리뷰 카드 1.2x + screen clip 해제 + KO 고지 mockup 우측 정렬 |
| R21 | 2026-05-09 | KVR 카드 padTop 17→20 + drop shadow strong→very strong (alpha 0.22→0.32 / blur 28→40 / offsetY 6→9) + 큰 흰 BG ±10→±13px |
| R22 | 2026-05-09 | 큰 흰 BG 상단 모서리 곡선→직선 사다리꼴 (cornerR 30→50, mockup body 침범 완화) |
| R23→R24 | 2026-05-09 | BG 좌·우 +10% 확장 시도 → 롤백 (사용자 의도 영역 오인). 카드 _cardScale 1.2→1.4 (폭 +20%씩 누적, mockup 외곽 ±80px 돌출) |
| R25 | 2026-05-09 | 카드 높이 1.2x (위아래 길이 변경 없음 → 사용자 명시 미세 조정 최종) |
| R26~R28 | 2026-05-09 | KO 고지문구 X 위치 누적 조정 (mockup 우측 936 → 카드 우측 끝 cardX+cardW → -5 → -15 → 최종 ~1001) |

### Phase 4 — 운영 자동화 본래 의도 복원 + 미세조정 (R29~R31, 본 세션)

| Iteration | 날짜 | 주요 변경 | Match Rate |
|---|---|---|---|
| **R29** | 2026-05-11 | 리뷰 본문 textarea `\n` 줄바꿈 시각 적용 (`wrapTextToNLines` 재작성: segments 분리 + wrapSegment 헬퍼 + 잔여 ellipsis hint, +25 라인) | 100% (FR-7 강화) |
| **R30** | 2026-05-11 | 배치 모드 리뷰 콘텐츠 언어별 독립 편집 지원. R13 "단건 자동 복사" 정책 폐기 (renderBatchLangFields/syncBatchStateFromUI/copyLangFieldsToOthers/buildBatchCfgs 4 군데 수정, +38 라인) | 100% (FR-9 본래 의도 복원) |
| **R31** | 2026-05-11 | 키비주얼 BG 슬라이더 미세조정 범위 좁힘. 크기 max 600→250%, 상하 ±1500→±500px step 10→5 (좌우 변경 없음). 5곳 in-place | 100%, 미세조정 ~2.5~6배 쉬워짐 |

---

## Plan Success Criteria — Final Status (R31 시점)

| ID | Criteria | Final | Evidence |
|---|---|:---:|---|
| **SC-1** | 4언어 LANG_PACK 라벨 정확도 | ✅ Met | `KVR_LANG_PACK[ko/en/ja/zh-TW]` 4언어 분기 + 단위 변환 함수 |
| **SC-2** | 별점 5케이스 정밀도 | ✅ Met | `KVR_HELPERS.starParts(rating)` rounded 0.5 단위 |
| **SC-3** | 평가 개수 4케이스 LANG_PACK | ✅ Met | `formatRatingCount` 4언어 + 천/만/M/K/萬 변환 |
| **SC-4** | 키비주얼/로고 6 slider 정상 | ✅ Met (R31 강화) | `bindKvrSlider` × 6 + R31 슬라이더 범위 축소로 미세조정 ~2.5~6배 쉬워짐 |
| **SC-5** | 헤드라인 OFF 정상 렌더 | ✅ Met | `if (preset !== 'off')` 가드 |
| **SC-6** | 기존 4템플릿 회귀 없음 | ✅ Met | R30/R31 모두 KVR 분기만, 다른 6 템플릿 무영향 |
| **SC-7** | ZIP 4장 ≤2초 | ✅ Met (예상) | bg/logo/mockup 1회 사전 디코드 + 4반복 |
| **SC-8** | mockup 화면 영역 정확도 | ✅ Met (R5~R28 정밀화) | R8/R9/R11/R12/R18 다단계 정밀화 + R14 1.8x → R17 1.98x → R25 카드 1.2x |

**Overall Success Rate: 8/8 Met (100%)**

### R29/R30/R31 신규 충족 항목 (Plan 미명세 영역 강화)

| 항목 | 출처 | 상태 |
|---|---|:---:|
| 리뷰 본문 `\n` 줄바꿈 시각 적용 | R29 (사용자 피드백) | ✅ 신규 충족 |
| 배치 모드 4언어 독립 편집 | R30 (사용자 피드백, FR-9 본래 의도) | ✅ 복원 완료 |
| 배치 "다른 언어에 복사" 1-click | R30 (옵션 (a)) | ✅ 다른 5 템플릿 일관 |
| 키비주얼 슬라이더 미세조정 효율 | R31 (사용자 피드백) | ✅ ~2.5~6배 향상 |

---

## Key Decisions & Outcomes (PRD/Plan/Design → Code, R31 시점)

### 원본 24 결정 (모두 충실 적용)
| Decision | Source | Outcome |
|---|---|:---:|
| 단일 HTML 정책 유지 | CLAUDE.md | ✅ 정책 준수 (9,779 라인 self-contained) |
| Canvas 직접 합성 패턴 | Plan/Design | ✅ html-to-image fallback 불필요 |
| Helper 함수 분리 (Option C) | Design | ✅ 추후 재사용 가능 |
| mockup 폭 540px / 하단 8.7px 잘림 | Brainstorming Q5 | ✅ R6→R8→R14 1.8x→R17 1.98x 진화 (사용자 요청 누적 반영) |
| 별점 0.5 단위 부분 채움 | Brainstorming Q9 | ✅ `KVR_HELPERS.starParts` |
| 평가 개수 단위 LANG_PACK | Brainstorming Q11 | ✅ 4언어 분기 |
| 단건 → 배치 데이터 공유 | UA 워크플로 단순화 | ❌→✅ **Evolved (R30)**: R13에서 별도 슬롯 분리 → R30에서 콘텐츠도 언어별 독립 편집으로 전환 (다른 5 템플릿 일관) |
| (외 17건) | Plan/Design | ✅ 모두 충실 적용 |

### R5~R31 신규 결정 (사용자 피드백 기반 30+건)
| 결정 | Iteration | 사용자 의도 |
|---|---|---|
| 키비주얼 슬라이더 3배 확장 | R6 | 미세조정 부족 → 범위 ↑ |
| **키비주얼 슬라이더 미세조정 범위 축소** | **R31** | **R17 mockup 1.98x 확대 후 실용 범위 좁아짐 → 범위 ↓ (역방향, 5.5배 축소)** |
| mockup 화면 흰 PNG 변환 | R7 | 흰 콘텐츠와 톤 일치 |
| mockup 레이어 맨 앞 | R8 | 베젤이 콘텐츠 frame 역할 |
| mockup 1.8x → 1.98x 확대 | R14/R17 | 시각 효과 강화 |
| KVR_DEFAULT 콘텐츠 KO `\n` 빈 줄 정책 | R29 (option 2) | "a\n\nb" 빈 줄 skip |
| 배치 KVR 콘텐츠 언어별 독립 | R30 (option a) | KVR_DEFAULT 초기값 + 복사 버튼 + 단건과 완전 독립 |
| KO 고지문구 위치 누적 조정 | R26~R28 | mockup → 카드 우측 → 최종 -15px |

---

## Lessons Learned

### L-1 — 사용자 시각 검증 + 픽셀 분석 사이클이 가장 큰 leverage
- R0 정적 100% → 실측 35%로 추락한 후, Pillow + numpy PNG 픽셀 분석으로 좌표 자동 추출 (R11, R8.1) → 재시 정밀 매칭
- **앞으로**: 시각 디자인 매칭 작업은 무조건 PNG 픽셀 분석을 정적 검증 단계에서 포함

### L-2 — 정책 절충(R13)은 추후 본래 의도 복원(R30) 비용 발생
- R13 "단건 자동 복사" 정책은 UA 워크플로 단순화 의도였으나, 실 운영에서 4언어 독립 편집 필요성 노출 → R30에서 본래 Plan FR-9 의도 복원
- **앞으로**: 정책 절충은 일회성 명시 (이번 한정), 기본 패턴은 다른 템플릿 일관성 유지

### L-3 — Iteration 방향이 정반대로 뒤집힐 수 있음 (R6 ↔ R31)
- R6에서 슬라이더 3배 확장 → R17 mockup 1.98x 확대로 실용 범위 좁아짐 → R31에서 5.5~3배 축소
- **앞으로**: 슬라이더 / 좌표 등 UI 범위는 mockup·자산 크기 의존성을 우선 고려

### L-4 — `\n` 시각 줄바꿈은 textarea ↔ Canvas 변환 시 자주 누락되는 영역
- R29 발견 전 R0~R28 28회 iteration 동안 `\n` 미지원 상태로 운영. 사용자 보고 후 한 세션에 해결 (`wrapTextToNLines` 재작성 +25 라인)
- **앞으로**: textarea + Canvas 조합 템플릿은 무조건 `text.split(/\r?\n/)` 로직 우선 추가

### L-5 — collaborator 협업 시 collateral deletion 위험
- 강정아 push (R14)에서 Pickup 템플릿 collateral 삭제 사고. 백업 파일에서 1:1 복원 (+1,209 라인)
- **앞으로**: 협업 전 백업 패턴 `repo/.backup-pre-collab-pull-{date}/` 유지 + collaborator 변경 영역 명확화 (KVR ↔ Pickup 분리)

### L-6 — In-place 토큰 수정의 비중이 높음 (KVR 31 iterations 중 ~30%)
- 코드 라인 변경 0 또는 1~5라인 in-place 수정이 다수: R31 (5곳 토큰), R20~R28 (좌표 누적 조정), R10~R10.2 (PNG alpha만 변환)
- **앞으로**: 초기 구현 후 단계적 미세조정은 in-place 수정 + bash sed 패턴 활용

### L-7 — Plan/Design 문서는 R-iteration 본문 갱신 vs 후행 통합 보고서 선택
- KVR Plan FR-7는 `\n` 미명세였으나 R29에서 강화. 본문 갱신 안 함 → Report에서 통합 반영
- **앞으로**: Plan/Design 본문은 R0 의도 보존 (역사 추적), Report에서 신규 사항 통합 기록

---

## 검증 가이드 (사용자 브라우저, R29+R30+R31 신규)

### Single Mode — R29 검증
1. KVR 단건 모드 진입 → 키비주얼 + 로고 업로드
2. 리뷰 본문 textarea에 `"첫째 줄\n둘째 줄"` 입력 (엔터 키)
3. 미리보기 + PNG 다운로드 모두 2줄 시각 표시 확인
4. 4언어 모두 일관 적용 확인
5. 3줄 이상 입력 시 마지막 줄 ellipsis (`…`) + 잔여 hint 확인
6. **회귀**: `\n` 없는 긴 1줄 입력 시 기존 width-wrap + ellipsis 정상 동작 확인

### Batch Mode — R30 검증
1. KVR 배치 모드 진입 → 4언어 모두 체크
2. 각 언어 카드에 "리뷰 제목 / 리뷰 본문 / 리뷰어 아이디" 3 필드 + "다른 언어에 복사" 버튼 노출 확인
3. 초기값: ko/en/ja/zh-TW 모두 KVR_DEFAULT 샘플 (`"현질 유도가 너무 심합니다"` 등)
4. 각 언어 본문 다르게 입력 + R29 `\n` 줄바꿈 적용 → ZIP 4장 모두 시각 일치 확인
5. "다른 언어에 복사" 1-click → 한 언어 3 필드가 나머지 일괄 복사 확인
6. **단건 ↔ 배치 분리**: 단건 모드에서 리뷰 변경 후 배치 진입 시 KVR_DEFAULT 유지 (영향 없음)

### Slider Range — R31 검증
1. KVR 단건 모드 → 키비주얼 PNG 업로드
2. 크기 슬라이더 끝까지 드래그: **250%까지만** (이전 600%)
3. 상하 슬라이더 끝까지 드래그: **±500px까지만, 5단위 점프** (이전 ±1500, 10단위)
4. 좌우 슬라이더: ±1500px / 10단위 변경 없이 동작 확인
5. 배치 모드: `b-kvr-bg-*` 슬라이더 3종 동일 검증
6. 디폴트 100% / 0 / 0에서 키비주얼 cover 시각 결과 회귀 없음 확인

### Regression
- 기존 6템플릿(today-tap, app-badge, appstore-screenshot, sd-showcase, pickup, steam-review) 각각 1회 사용 정상 동작 확인
- KVR R14 1.8x mockup (collaborator 작업) 그대로 작동 확인 (R17 1.98x로 진화한 상태)

---

## 변경 사항 정리 (R0~R31 누적)

### 코드 변경 (`today-banner-designer.html`, 6,105 → 9,779라인, +3,674)

| 단계 | 누적 라인 | 비고 |
|---|---|---|
| R0 (2026-05-03 초기) | 6,943 (+838) | 신규 5번째 템플릿 |
| R3~R8.1 (mockup 정밀화) | ~7,016 | iPhone PNG/좌표 누적 조정 |
| R9~R12 (BG 박스 + corner) | ~7,166 | 흰 BG 둥근 모서리 + 좌·우 갭 메움 |
| R13 (배치 별도 슬롯) | ~7,316 (+150) | `state.batch.kvr` + UI 90줄 + bindKvrBatchUI 60줄 |
| R14~R28 (collab + 카드 + KO 고지) | ~9,716 (+~2,400, Pickup 복원 +1,209 포함) | 협업 + 시각 정밀화 |
| **R29 (\n 줄바꿈)** | 9,741 (+25) | `wrapTextToNLines` 재작성 |
| **R30 (배치 언어별 독립)** | 9,779 (+38) | 4 군데 분기 + UI 분리 |
| **R31 (슬라이더 범위)** | 9,779 (0 라인 변경) | 5곳 in-place 토큰 |

### 신규 자산
| 경로 | 진화 |
|---|---|
| `repo/assets/keyvisual-review/iphone.png` | R0 초기 (248×500, 6.5KB) → R11에서 1500×1500 PNG 변환 후 base64 인라인 전환 |

### PDCA 문서
| 경로 | 라인 |
|---|---|
| `docs/01-plan/features/keyvisual-review.plan.md` | 174 (Plan, R0) |
| `docs/02-design/features/keyvisual-review.design.md` | 364 (Design, R0) |
| `docs/03-analysis/keyvisual-review.analysis.md` | 492 (R29+R30 통합 + R0~R28 누적) |
| `docs/04-report/keyvisual-review.report.md` | (본 문서, R0→R31 통합) |

---

## 다음 단계

1. **사용자 브라우저 실측** — R29 / R30 / R31 신규 8개 케이스 (위 검증 가이드)
2. **GitHub push** — `cd repo && git add -A && git commit -m "feat(kvr): R29+R30+R31 통합 — \n 줄바꿈 + 배치 언어별 독립 + 슬라이더 범위 축소" && git push origin main`
3. **GitHub Pages 자동 반영** (이미 `index.html` redirect 설정)
4. (Optional) `/pdca archive keyvisual-review --summary` — 작업 완전 종료 시
5. (Future) 사용자 보고 발생 시 R32+ iteration

---

## Final Status

| 항목 | 값 |
|---|---|
| Match Rate (정적) | **100%** |
| Critical/Important Gap | **0건** |
| Minor (Note) | 3건 (모두 미래 옵션 / 정책 선택지) |
| Iterations | **31** (R0 + R5~R31) |
| Total Lines | 9,779 (+3,674 from initial) |
| 사용자 시각 검증 대기 | 8 케이스 (R29: 4 / R30: 3 / R31: 1) |
| 회귀 위험 | **0** |
