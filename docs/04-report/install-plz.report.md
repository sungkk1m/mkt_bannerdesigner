# PDCA Report — Install Plz 템플릿 (v1.15)

**Feature**: install-plz
**Completed**: 2026-07-19 (1일 사이클: Plan → Design → Do → Check → Act-1)
**Author**: ksk@superplanet.net
**Docs**: `01-plan/features/install-plz.plan.md` · `02-design/features/install-plz.design.md` · `03-analysis/install-plz.analysis.md`

---

## Executive Summary

| 항목 | 값 |
|---|---|
| Feature | Install Plz — "설치 구걸" 밈 배너 (10번째 템플릿, key: `install-plz`) |
| 기간 | 2026-07-19 (당일 완료, Act-1 포함) |
| Match Rate | **100%** (FR 12/12 · NFR 4/4 · SC 6/6) |
| 변경 규모 | `today-banner-designer.html` +약 350라인 · `assets/install-plz/` 신규 9파일(플레이트 8 PNG + 생성 스크립트) |
| Iteration | 1회 (Act-1: 스케일 상한 150→250%, 실사용 피드백 당일 반영) |

### 1.3 Value Delivered (4관점, 실측 기준)

| 관점 | 실현된 가치 |
|---|---|
| **Problem** | 밈 폰트(두꺼운 외곽선 코믹체)가 툴 폰트 스택에 없어 텍스트 재현 불가 → 디자이너 수작업으로 4언어×2사이즈=8장 제작하던 밈 배너 |
| **Solution** | 레퍼런스 원본 픽셀을 추출한 텍스트 플레이트 8장 에셋화 — 폰트 렌더링 0%, 캔버스 출력 vs 플레이트 **8콤보 전수 maxDiff=0** 실측 |
| **Function/UX Effect** | SD 1장 업로드 → 배치 ZIP 8장 (실사용 검증: 사용자가 Lucky Seven SD로 8장 실제 생산 완료). 사이즈별 X/Y/Scale(50~250%) 미세 조정 |
| **Core Value** | 밈 포맷 재활용 인프라 — 신규 게임 SD 1장으로 8장 즉시 생산, 문구·폰트·KO 고지 위치 원본과 픽셀 동일. 새 레퍼런스 수령 시 `make_plates.py` 재실행으로 확장 가능 |

---

## Key Decisions & Outcomes

| 결정 (Plan/Design) | 준수 | 결과 |
|---|:---:|---|
| 텍스트 이미지화(플레이트) — 폰트 무변형 | ✅ | 캔버스 vs 플레이트 8콤보 maxDiff=0 → 레퍼런스 원본 픽셀 체인 완성 |
| 외부 에셋 방식 (pickup 패턴) | ✅ | HTML 비대화 없음 (+0KB), 에셋 총 ~800KB |
| SD 1장 공용 + 사이즈별 X/Y/Scale | ✅ | 실사용 산출물 8장 정상. Act-1에서 스케일 상한 250%로 확장 |
| 빈 슬롯 시작 (원본 엘프 미포함) | ✅ | SD 미업로드 시 플레이트만 렌더, 에러 0 |
| KO 고지문구 플레이트 내장 (별도 렌더 금지) | ✅ | KO 출력에만 원본 위치(우상단) 표시, 이중 표시 원천 차단 |
| 1200×628 = 원본 625 + 하단 3px 패딩 (무스케일) | ✅ | 텍스트 픽셀 1:1 보존 |

## Success Criteria Final Status: **9/9 Met**

플레이트 픽셀 정합 · 템플릿 전환/사이즈 잠금 · 언어별 플레이트 스왑 · 사이즈별 조정 독립 · KO 고지 원본 위치 · 배치 8장 · 빈 슬롯 안전 · 파일명 규칙 · 기존 9 템플릿 회귀 0 (상세 근거: analysis 문서)

## Act-1 Iteration 기록

- 실사용 피드백(당일): 세로로 긴 SD 소스가 contain-fit 시 작아 보임, 150% 상한 부족 → **단건/배치 스케일 슬라이더 max 250%** (양 사이즈 공통)
- 재검증: 250% 렌더 기하 픽셀 일치 확인

## Lessons Learned

1. **언어 간 픽셀 diff로 텍스트/캐릭터 분리** — 언어별로 다른 픽셀 = 텍스트, 동일 = 캐릭터. 단, 언어 간 겹치는 검정 획이 오탐을 만들어 언어별 개별 경계 측정 필요
2. **색상 채널 구분(blue-key)이 경계 함정 해결** — EN 하단 2줄이 물웅덩이와 행 겹침 → 파란(효과) vs 검정(텍스트) 분리로 경계 확정. 밈류 후속 템플릿에 재사용 가능한 기법
3. **레퍼런스 합성 흔적 주의** — 1080은 언어별 캐릭터 위치/크기가 달랐음(수작업 합성). "동일해 보이는" 레퍼런스도 사이즈·언어별 실측 필수
4. **contain-fit + 비정형 SD 비율** — 원본(587×570 정방형 근사) 기준 100%는 세로로 긴 소스에서 작아 보임 → 스케일 상한은 소스 비율 다양성을 감안해 넉넉히

## 산출물

- 코드: `today-banner-designer.html` (TEMPLATE_KEYS·상수·state·렌더 파이프라인 5함수·단건/배치 UI·스위치 분기)
- 에셋: `assets/install-plz/text-plate_{ko|en|ja|zh-TW}_{1x1|1200x628}.png` + `make_plates.py`
- 문서: PDCA 4종 + `CLAUDE.md` 현재 상태 v1.15
