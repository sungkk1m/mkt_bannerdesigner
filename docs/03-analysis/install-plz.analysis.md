# PDCA Analysis — Install Plz 템플릿 (v1.15)

**Feature**: install-plz
**Date**: 2026-07-19
**Plan/Design Ref**: `docs/01-plan/features/install-plz.plan.md` / `docs/02-design/features/install-plz.design.md`

---

## Context Anchor

| Key | Value |
|-----|-------|
| **WHY** | 밈 폰트가 툴 폰트 스택에 없음 → 레퍼런스 원본 픽셀 플레이트만이 "폰트 아예 변경 없이"를 만족 |
| **SUCCESS** | 8장 텍스트 픽셀 원본 동일, 캐릭터 잔여물 0, Single+Batch 동작, 기존 9 템플릿 회귀 0 |

## Match Rate: **100%** (FR 12/12 · NFR 4/4 · SC 6/6)

### 검증 방법
- 정적: FR별 코드 구현 확인 (구현 세션 내 직접 작성·배선)
- 런타임: 브라우저 실측 (localhost:8123 static server, in-page JS 계측 + 스크린샷)

### Success Criteria 평가

| SC | 결과 | 근거 (실측) |
|---|---|---|
| 플레이트 픽셀 정합 (NFR-02) | ✅ | **8/8 콤보 캔버스 vs 플레이트 에셋 maxDiff=0** (in-browser getImageData 전수 비교). 플레이트↔레퍼런스는 생성 단계에서 파티션 재조립 diff=0 검증 → 텍스트 = 원본 픽셀 체인 완성 |
| SC-01 템플릿 전환/사이즈 잠금 | ✅ | 1x1·1200x628 활성 / 9x16·4x5 비활성 (single select + batch 체크박스 모두) |
| SC-02 SD 합성 + 언어 전환 플레이트 스왑 | ✅ | KO 1x1 / JA 1x1 / JA 1200x628 스크린샷 — 레퍼런스와 동일 배치 재현 |
| SC-03 사이즈별 X/Y/Scale 독립 | ✅ | 1x1 x=50, 1200x628 x=-30 동시 저장 확인 (slotAdjustPerSize) |
| SC-04 KO 고지문구 원본 위치 | ✅ | KO 1200x628 캔버스 (1050,8)-(1192,40) 영역 dark px 359 검출, 타 언어 0. 렌더러에 별도 고지 코드 없음 (이중 표시 원천 차단) |
| SC-05 배치 8장 | ✅ | buildBatchCfgs → 8 cfgs (언어별 플레이트 경로 정확), b-preview 8 썸네일 캔버스 1080×1080 ×4 + 1200×628 ×4, 온스크린 aspect 1.00/1.91 |
| SC-06 SD 미업로드 안전 | ✅ | 플레이트만 렌더, 에러 없음 |
| 파일명 규칙 | ✅ | `installplz_ko_1080x1080.png` / `installplz_zh-TW_1200x628.jpg` / 배치 `{prefix}_installplz_{lang}_{dim}` |
| 회귀 0건 | ✅ | 10개 템플릿 전환 sweep — 전 템플릿 프리뷰 렌더 정상, today-tap 복귀 시 사이즈 옵션 복원, **콘솔 에러 0** |

### 발견/처리한 이슈 (구현 중 수정)

| # | 이슈 | 처리 |
|---|---|---|
| 1 | EN 1080 하단 텍스트 2줄("PLEASE TRY"/"OUR GAME") 중 1줄이 초기 경계값(Y2=919)에서 잘림 | blue-mask(물웅덩이) vs black(텍스트) 색상 구분 재측정 → Y2=823 확정 |
| 2 | 1200x628 텍스트 크롭에 물웅덩이 좌측 끝 파란 조각 침범 | blue-key 정리(B−R>50 && B>140 → 흰색) — 텍스트는 검/흰/빨/회색이라 무영향 |
| 3 | 레퍼런스 1200×628이 실제 1200×625 | 하단 3px 흰 패딩 (무스케일 — 텍스트 픽셀 1:1 보존) |
| 4 | 1080 캐릭터가 언어별 위치/크기 상이 (수작업 합성 흔적) | 언어별 개별 크롭 경계값 적용, SD 기본 박스는 사이즈별 단일 스펙(587×570) |

### 잔여 리스크 (수용)

- 배치 그리드 썸네일의 브라우저 페인트 지연이 스크린샷에 간헐 포착 — DOM/캔버스 실측은 전부 정상, 다운로드 산출물 무관 (기존 템플릿 공통 프리뷰 특성)
- `file://` 직접 열기 시 이 템플릿 export 불가 (외부 에셋 canvas taint) — pickup과 동일 제약, static server 운용 중

## Act-1 Iteration (2026-07-19, 실사용 피드백)

- **피드백**: 실제 배치 산출물(`banner_banners (22)` — Lucky Seven SD) 확인 결과, 세로로 긴 SD 소스는 contain-fit 시 작아 보이는데 스케일 상한 150%로는 부족
- **수정**: 단건(`s-ip-scale`)·배치(`b-ip-scale`) 스케일 슬라이더 max 150 → **250** (양 사이즈 공통, step 5 유지)
- **재검증**: 100×100 테스트 SD를 250%로 렌더 → 예상 기하(1425×1425 drawn box, 캔버스 전체 커버)와 픽셀 일치. 스케일 경로에 별도 클램프 없음 확인
- **참고**: 검증 중 Claude 내장 브라우저 팬에서 `img.decode()` 프라미스가 hang되는 환경 이슈 발견 (페이지 리로드 후 발생, 새 탭으로 해소) — 툴 코드/실사용 Chrome과 무관

## 결론

Match Rate 100% (Act-1 반영 완료) — `/pdca report install-plz` 진행 가능.
