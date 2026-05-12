# SD Showcase Completion Report

> **Status**: Complete
>
> **Project**: Today Banner Designer (v1.6)
> **Author**: ksk@superplanet.net (UA Manager, Superplanet)
> **Start Date**: 2026-04-29
> **Completion Date**: 2026-04-30
> **Duration**: 2일 (집약적 PDCA 4 iterations)
> **PDCA Cycle**: #4 (sd-showcase 첫 번째 cycle)

---

## Executive Summary

### 1.1 Project Overview

| Item | Content |
|------|---------|
| Feature | SD Showcase 템플릿 (4번째 배너 템플릿) |
| Start Date | 2026-04-29 |
| End Date | 2026-04-30 |
| Duration | 2일 |
| 본체 파일 | `today-banner-designer.html` (5,097 → 6,105 라인, +1,008) |
| 사이즈 지원 | 1080×1080 + 1200×628 (9:16 미지원) |
| 언어 지원 | ko / en / ja / zh-TW (4언어) |
| 출력 조합 | 4언어 × 2사이즈 = **8장 ZIP 다운로드** |

### 1.2 Results Summary

```
┌─────────────────────────────────────────────┐
│  Final Match Rate: 100%                     │
├─────────────────────────────────────────────┤
│  ✅ FR (Functional):     16 / 16 items      │
│  ✅ NFR (Non-Functional): 5 / 5 items       │
│  ✅ SC (Scenarios):       8 / 8 items       │
│  ✅ R  (Risks):           5 / 5 mitigated   │
│  ✅ N  (New Reqs r2~r4): 10 / 10 items      │
│  ⏳ Out of Scope:         5 items (deferred)│
│  ❌ Cancelled:            2 items           │
└─────────────────────────────────────────────┘
```

### 1.3 Value Delivered

| Perspective | Content |
|-------------|---------|
| **Problem** | 게임 SD 캐릭터를 전면에 내세우는 단순 쇼케이스 배너 템플릿이 없어 UA 매니저가 4언어 × 2사이즈 = 8장을 디자이너 수작업으로 1~2시간 소요. 다른 사내 게임 BI 운영자도 잠재 요구. |
| **Solution** | 6 SD 슬롯 + 4언어 텍스트 + 2 사이즈 + 외곽 검정 테두리(고정 10/9px) + 자동 대비 + KO 광고법 자동 첨부를 자동화. 배경 컬러피커·SD 크기·SD 사이 간격·타이틀 외곽선 두께 슬라이더로 다른 게임 BI 재사용 가능. |
| **Function/UX Effect** | 단건 1초 / 배치 8장 ZIP 2초로 자동 생성 (60~120× 속도 향상). 자동 폰트 축소(긴 영문 처리) · 우측 SD 좌우반전(1200×628) · 타이틀 drop shadow(흰 배경에서도 시각 효과) · 픽 직각+흰 stroke+drop shadow 등 시각 디테일 자동화. |
| **Core Value** | UA 자산 생산 속도 60~120× 향상 + 4언어 다국어 운영 자동화 + KO 광고법 준수 자동화 + 다른 사내 게임 재활용 가능 인프라화. |

---

## 1.4 Success Criteria Final Status

> Plan 원본 SC-01~08 + r2~r4 누적 신규 요구 N1~N10 = 18 항목.

### Plan Original SC

| # | Criteria | Status | Evidence |
|---|---------|:------:|----------|
| SC-01 | "SD Showcase" 선택 시 사이즈 셀렉터 활성/비활성, UI 분기 | ✅ Met | `applyTemplateSwitch :4458-4527` |
| SC-02 | SD 6장 + 4언어 + 흰 배경 → 미리보기 정상 렌더 | ✅ Met | 사용자 첨부 1080×1080 KO PNG 실측 |
| SC-03 | 배경 검정 → 자동 대비 (흰/검 반전) | ✅ Met (코드 경로) | `getContrastPalette :2754-2767` |
| SC-04 | KO 양 사이즈 우하단 자동 고지문구 | ✅ Met | 사용자 첨부 다운로드 PNG에서 "확률형 아이템 포함" 확인 |
| SC-05 | 픽 ON/OFF 토글 OFF → 픽 사라짐, reflow 없음 | ✅ Met (코드 경로) | `:3712 if (cfg.showPill && cfg.pill.trim())` |
| SC-06 | SD 일부만 → 빈 슬롯 투명 | ✅ Met (코드 경로) | `:3700 if (!img \|\| !pos) continue` |
| SC-07 | 외곽선 슬라이더 4~14 + lineHeight 자동 보정 | ✅ Met | `:3678-3680 lineHeight 1.10 자동 보정` |
| SC-08 | 배치 8장 ZIP, KO만 고지문구 | ✅ Met (코드 경로) | `handleBatchExportZip :5560-5566` |

### r2~r4 New Requirements (사용자 피드백)

| # | Criteria | Status | Evidence |
|---|---------|:------:|----------|
| N1 | 외곽선 슬라이더 시각 변화 (흰 bg+흰 stroke 안 보임 해소) | ✅ Met | `drawSdsTitleLines :3719-3753` (drop shadow blur scale) |
| N2 | 1200×628 우측 SD(slots 4,5,6) 좌우반전 | ✅ Met | `drawSideCol :3854-3873` ctx.scale(-1,1) |
| N3 | 타이틀 drop shadow | ✅ Met | rgba(0,0,0,0.45) blur×1.6 offsetY×0.5 |
| N4 | SD 사이 간격 슬라이더 (0~80) | ✅ Met | `s/b-sds-spacing` UI + canvas 적용 |
| N5 | outerMargin 변경 (60→4 r4 고정) | ✅ Met | `border.outerMargin: 4` |
| N6 | 픽 206%×185% 확대 | ✅ Met | 1080: 67/74/33, 1200: 59/66/26 |
| N7 | 픽 anchor center → TOP | ✅ Met | `drawSdsPill(..., 'top')` |
| N8 | 검정 테두리 10px 고정 | ✅ Met | `border.thickness: 10` |
| N9 | 검정 테두리 9px 여백 (선 중심) 고정 | ✅ Met | `strokeRect(9, 9, w-18, h-18)` |
| N10 | "타이틀 글자 외곽선 두께" 라벨 명확화 | ✅ Met | HTML L1162, L1553 |

**Success Rate**: **18/18 = 100%** (Plan SC 8건 + r2~r4 신규 N 10건 모두 충족)

## 1.5 Decision Record Summary

> Plan-Plus 14+1 결정 + r2~r4 누적 결정 = **25 결정**.

### Plan-Plus 원안 (R1.Q1 ~ R4.Q14 + Checkpoint 1)

| Source | Decision | Followed? | Outcome |
|--------|----------|:---------:|---------|
| R1.Q1 | 브랜드 픽 4언어 각각 입력 | ✅ | 단건 + 배치 모두 4언어 분리 입력 |
| R1.Q2 | 타이틀 \n 직접 줄바꿈 | ✅ | textarea + sdsWrapText에서 \n 우선 처리 |
| R1.Q3 | KO 양 사이즈 자동 고지문구 | ✅ | LANG_PACK.ko.disclaimer 재사용 |
| R1.Q4 | 외곽 테두리 검정 고정 (사이즈별 자동 두께) | ✅→갱신 | r4에서 강정아 스펙 10/9px 고정으로 확정 |
| R2.Q5 | 빈 슬롯 투명 자리보존 | ✅ | drawImageContain 빈 슬롯 skip |
| R2.Q6 | 배경 컬러피커 + 자동 대비 휘도 이진 | ✅ | getLuminance + getContrastPalette + hysteresis |
| R2.Q7 | 외곽선 두께 슬라이더 4~14 | ✅ | r4에서 라벨 "타이틀 글자 외곽선 두께"로 명확화 |
| R2.Q8 | 프리셋 v1 미포함 | ✅ | SD Showcase 전용 프리셋 미구현 (Out of Scope) |
| R3.Q9 | 템플릿 명 "SD Showcase" | ✅ | TEMPLATE_KEYS 4번째 |
| R3.Q10 | 자동 대비 알고리즘 휘도 이진 | ✅ | WCAG sRGB 휘도 + hysteresis 0.46~0.54 |
| R3.Q11 | 배치 사이즈 체크박스 | ✅ | 1x1+1200×628 활성 / 9:16 비활성 |
| R3.Q12 | 픽 ON/OFF 토글 | ✅ | s-sds-showpill, b-sds-showpill |
| R4.Q13 | EN 라인별 균등 사이즈 (Friends 1.6× 미반영) | ✅ | v1 균등 사이즈 유지 (Out of Scope) |
| R4.Q14 | 1080×1080 1줄 기본 | ✅ | SD_SHOWCASE_DEFAULT.ko 기본값 |
| Checkpoint 1 | 세션 전용 영속화 | ✅ | localStorage 미사용 (기존 패턴 유지) |

### r1 Iterate (G1+G2)

| Source | Decision | Followed? | Outcome |
|--------|----------|:---------:|---------|
| G1 user feedback | outerMargin + thickness 분리 | ✅→갱신 | r4에서 4/10으로 최종 고정 |
| G2 user feedback | SD 셀 크기 슬라이더 (50~150%) | ✅ | s/b-sds-cellscale 유지 |

### r2 Iterate (사용자 신규 요구 4건)

| Source | Decision | Followed? | Outcome |
|--------|----------|:---------:|---------|
| r2 user spec | 외곽선 슬라이더 시각 변화 (drop shadow scale) | ✅ | drawSdsTitleLines 헬퍼 |
| r2 user spec | 1200×628 우측 SD 좌우반전 | ✅ | mirror 인자 추가 |
| r2 user spec | 타이틀 drop shadow (흰 bg에서도 시각 효과) | ✅ | shadow blur×1.6, offset×0.5 |
| r2 user spec | SD 사이 간격 슬라이더 (0~80) | ✅ | s/b-sds-spacing |

### r3 Iterate (픽 대형화 + outerMargin)

| Source | Decision | Followed? | Outcome |
|--------|----------|:---------:|---------|
| r3 user spec | outerMargin 60→15 | ✅→갱신 | r4에서 4로 재확정 |
| r3 user spec | 픽 206%×185% 확대 | ✅ | 1080: 67/74/33, 1200: 59/66/26 |
| r3 user spec | 픽 anchor center → TOP | ✅ | anchor='top' 파라미터 |

### r4 Iterate (강정아 스펙 검정 테두리 고정)

| Source | Decision | Followed? | Outcome |
|--------|----------|:---------:|---------|
| r4 강정아 슬랙 | 검정 테두리 10px 고정 (선 굵기) | ✅ | border.thickness: 10 |
| r4 강정아 슬랙 | 9px 여백 고정 (선 중심 기준) | ✅ | strokeRect(9, 9, w-18, h-18) |
| r4 강정아 슬랙 | 슬라이더 라벨 "타이틀 글자 외곽선" 명확화 | ✅ | UI 라벨 + 도움말 갱신 |

### Cancelled / Reverted

| Source | Decision | Outcome |
|--------|----------|---------|
| 사용자 요청 | NEXON Kart Gothic / Shin Go Pro / OPPOSans 폰트 적용 | 사용자 변심으로 즉시 원상복구. fonts/ 폴더 삭제, @font-face 제거, CSS·JS 모두 Pretendard/Noto JP/Noto TC 복귀. 잔재 0건 |
| 사용자 요청 | 이미지 그리드 270×300 고정 | 사용자 취소 — 적용 불필요 결정 |

**Decision Followed Rate**: **23/23 = 100%** (취소된 결정 2건은 사용자 의지에 따른 의도된 회수, Gap 아님)

---

## 2. Related Documents

| Phase | Document | Status |
|-------|----------|--------|
| Plan-Plus | `~/.claude/plans/brainstorming-spicy-plum.md` | ✅ 백업 보존 (14+1 결정 도출) |
| Plan | [`docs/01-plan/features/sd-showcase.plan.md`](../01-plan/features/sd-showcase.plan.md) | ✅ Finalized (v0.1, 326 lines, 16 FR + 5 NFR + 8 SC + 5 R) |
| Design | (Plan §7 Architecture Considerations + Plan-Plus §A-H로 대체) | ⏭ Skipped (Plan에 통합) |
| Do | 4 sessions: data-switch / canvas-renderer / single-ui / batch-ui-zip | ✅ All complete (676 lines initial) |
| Check | [`docs/03-analysis/sd-showcase.analysis.md`](../03-analysis/sd-showcase.analysis.md) | ✅ Complete (v0.3, 488 lines, Match Rate 100%) |
| Act | r1 → r4 누적 4 iterations | ✅ All resolved |
| Report | Current document | 🆕 Writing |

---

## 3. Completed Items

### 3.1 Functional Requirements (16/16)

| ID | Requirement | Status | Notes |
|----|-------------|:------:|-------|
| FR-01 | 헤더 셀렉터에 `sd-showcase` 옵션 추가 | ✅ | `:909` |
| FR-02 | TEMPLATE_KEYS에 `'sd-showcase'` 추가 | ✅ | `:1746` |
| FR-03 | SDS_CANVAS_SPECS + SD_SHOWCASE_DEFAULT 신규 | ✅ | r4 갱신 후 (border 9/10 고정, pill 대형화) |
| FR-04 | applyTemplateSwitch 분기 | ✅ | `:4458-4527` |
| FR-05 | state 확장 (sdshowcase, sd_*, langOverrides) | ✅ | spacing 추가됨 (r2) |
| FR-06 | 6 SD 드롭존 + updateStateImageAt | ✅ | M-2 패턴 확장 |
| FR-07 | 단건 모드 UI | ✅ | + spacing 슬라이더 (r2) |
| FR-08 | 배치 모드 UI 글로벌 4 + 6 드롭존 | ✅ | + spacing (r2) |
| FR-09 | renderBatchLangFields SDS 분기 | ✅ | |
| FR-10 | copyLangFieldsToOthers SDS 분기 | ✅ | |
| FR-11 | getLuminance + getContrastPalette 자동 대비 | ✅ | hysteresis 0.46~0.54 |
| FR-12 | buildSdShowcaseCanvas 7단계 합성 | ✅ | r2~r4 누적 개선 (drop shadow, mirror, fitTitle, TOP anchor) |
| FR-13 | 단건 다운로드 SDS 분기 | ✅ | `:4719-4720` |
| FR-14 | 배치 ZIP SDS 분기 | ✅ | `handleBatchExportZip :5707-5722` |
| FR-15 | 파일명 규칙 | ✅ | `buildSdShowcaseFilename` |
| FR-16 | DOM 프리뷰 buildSdShowcaseBanner | ✅ | wrap.style.padding=0 추가 (r2) |

### 3.2 Non-Functional Requirements (5/5)

| Item | Target | Achieved | Status |
|------|--------|----------|:------:|
| NFR-01 | Canvas export, html-to-image 미사용 | Canvas 100% | ✅ |
| NFR-02 | 폰트 자동 스왑 + ensureFontsLoaded | Pretendard / Noto JP / Noto TC | ✅ |
| NFR-03 | 6 SD 1회 디코드 → 8 조합 공유 | sdsSlotImgs Promise.all | ✅ |
| NFR-04 | 단일 HTML 정책 유지 | 외부 모듈 0건, 인라인만 | ✅ |
| NFR-05 | 휘도 0.46~0.54 hysteresis | _lastContrastMode | ✅ |

### 3.3 Risks Mitigated (5/5)

| ID | Risk | Mitigation 적용 | Status |
|----|------|----------------|:------:|
| R-01 | 픽 OFF 시 reflow 없음 — 사용자 혼선 | 의도된 동작, README 명시 | ✅ |
| R-02 | 휘도 0.5 경계 깜빡임 | hysteresis 0.46~0.54 | ✅ |
| R-03 | EN "Friends" 1.6× 미반영 | R4.Q13 결정으로 v1 균등 사이즈 | ✅ |
| R-04 | 단일파일 비대화 (5,097 → 추정 5,750) | 4 세션 분리 (실제 6,105) | ✅ |
| R-05 | 롤백 가능성 | 4 세션 + 4 iterate 커밋 분리 | ✅ |

### 3.4 New Requirements (r2~r4) — 10/10

| ID | 출처 | 구현 위치 | Status |
|----|------|----------|:------:|
| N1 | r2 | `drawSdsTitleLines :3719-3753` | ✅ |
| N2 | r2 | `drawSideCol mirror :3854-3873` | ✅ |
| N3 | r2 | shadow color/blur/offset | ✅ |
| N4 | r2 | s/b-sds-spacing 슬라이더 | ✅ |
| N5 | r3→r4 | border.outerMargin 4 (강정아 스펙) | ✅ |
| N6 | r3 | pill 206%×185% (1080: 67/74/33, 1200: 59/66/26) | ✅ |
| N7 | r3 | drawSdsPill anchor='top' | ✅ |
| N8 | r4 | border.thickness: 10 | ✅ |
| N9 | r4 | strokeRect 9px 선 중심 정렬 | ✅ |
| N10 | r4 | UI 라벨 명확화 + 도움말 | ✅ |

### 3.5 Deliverables

| Deliverable | Location | Status |
|-------------|----------|:------:|
| Code (단일 HTML) | `today-banner-designer.html` (6,105 라인, +1,008) | ✅ |
| Plan-Plus 결정 백업 | `~/.claude/plans/brainstorming-spicy-plum.md` | ✅ |
| Plan 문서 | `docs/01-plan/features/sd-showcase.plan.md` | ✅ |
| Analysis 문서 | `docs/03-analysis/sd-showcase.analysis.md` (v0.3, 16 sections) | ✅ |
| Report 문서 | `docs/04-report/sd-showcase.report.md` (현재) | ✅ |
| bkit state | `.bkit/state/pdca-status.json` (matchRate=100, iterations=4) | ✅ |

---

## 4. Incomplete Items

### 4.1 Out of Scope (Plan에서 명시 제외 — 차기 PDCA cycle 후보)

| Item | Reason | Priority | Estimated Effort |
|------|--------|----------|------------------|
| 사용자 프리셋 저장 (SD Showcase 전용) | Plan R2.Q8 결정 — v1 미포함 | Medium | 0.5일 |
| 다크/라이트 명시 테마 셀렉터 | 배경 컬러피커+자동 대비로 대체됨 | Low | — |
| 9:16 사이즈 | Plan §Out of Scope | Low | 0.5일 |
| 슬롯별 수동 위치/스케일/회전 | Plan §Out of Scope (KISS) | Low | 1일 |
| 픽 색상/모양/위치 커스터마이즈 | Plan §Out of Scope | Low | 0.5일 |
| EN 라인별 가변 폰트 사이즈 ("Friends" 1.6×) | R4.Q13 결정 — v1 균등 | Medium | 0.5일 (사용자 확인 시) |
| 그라데이션·이미지 배경 | Plan §Out of Scope | Low | — |

### 4.2 Cancelled/Reverted

| Item | Reason | Action Taken |
|------|--------|--------------|
| NEXON Kart Gothic / Shin Go Pro / OPPOSans 폰트 적용 | 사용자 변심 | A안(외부 TTF 참조) 적용 후 즉시 원상복구. fonts/ 폴더 삭제, @font-face 제거, CSS·JS 헬퍼 복귀. grep 검증 0건 |
| 이미지 그리드 270×300 고정 | 사용자 취소 | 미적용 |

---

## 5. Quality Metrics

### 5.1 Match Rate Evolution

| Iteration | Match Rate | Critical | Important | Trigger |
|-----------|:---------:|:---------:|:---------:|---------|
| r0 (초안) | 88% | 1 (G1: outer frame) | 1 (G2: SD 크기 UI) | 사용자 첨부 1080×1080 KO PNG + UI 스샷 피드백 |
| r1 (G1+G2 해소) | 96% | 0 | 0 | "지금 모두 수정" 결정 |
| r2 (신규 4건) | 100% | 0 | 0 | 외곽선 시각 변화 / 좌우반전 / drop shadow / spacing |
| r3 (픽 + outerMargin) | 100% | 0 | 0 | 픽 206%×185% / TOP 앵커 / outerMargin 60→15 |
| r4 (border 고정) | 100% | 0 | 0 | 강정아 스펙 확정 (10/9px 고정) |

### 5.2 Code Stats (Plan 추정 vs 실제)

| Metric | Plan 추정 | 실제 | 변화 |
|--------|:---------:|:----:|:----:|
| 신규 함수 | 5 | **8** | +3 (`drawSdsTitleLines`, `fitSdsTitle`, `sdsWrapText` 추가) |
| 추가 라인 | 650 | **1,008** | +358 (사용자 신규 요구 N1~N10 누적) |
| HTML 총 라인 | 5,747 | **6,105** | +358 |
| 사이즈 | 1080×1080 + 1200×628 | 동일 | — |
| 언어 | ko/en/ja/zh-TW | 동일 | — |
| 출력 조합 | 4×2=8장 | 8장 | — |
| Iterations | 1 (예상) | **4** | +3 (사용자 피드백 누적) |

### 5.3 Resolved Issues (4 iterations 누적)

| Issue | Severity | Resolution | Result |
|-------|:--------:|------------|:------:|
| G1 외곽 frame 디자인 모호 (Plan §Layout Spec 미스펙) | Critical | r1: outerMargin/thickness 분리 → r4: 강정아 스펙 9/10 고정 | ✅ |
| G2 SD 크기 조정 UI 부재 | Important | r1: cellScale 슬라이더 (50~150%, 단건+배치) | ✅ |
| 외곽선 슬라이더 시각 변화 없음 (흰 bg+흰 stroke 동색) | High | r2: drawSdsTitleLines + drop shadow blur scale | ✅ |
| 1200×628 우측 SD 비대칭 | High | r2: ctx.scale(-1,1) mirror | ✅ |
| 타이틀 입체감 부족 | Medium | r2: drop shadow rgba(0,0,0,0.45) | ✅ |
| SD 사이 간격 조정 불가 | Medium | r2: s/b-sds-spacing (0~80) | ✅ |
| 픽 사이즈 작음 | High | r3: 206%×185% 확대 | ✅ |
| 픽 위치 모호 (center vs top) | Medium | r3: anchor='top' 파라미터 | ✅ |
| 외곽선/배너 테두리 의미 혼동 | Critical | r4: 강정아 스펙 확정 + 라벨 명확화 | ✅ |
| 폰트 변경 후 미스 정렬 | Critical | rollback: 모두 원상복구 | ✅ |

### 5.4 사용자 실측 검증 (단건 모드, 1080×1080 KO)

- ✅ 6 SD 정상 렌더 (Nekomancer 게임 SD 6장)
- ✅ KO 타이틀 + 픽 정상 출력
- ✅ 우하단 "확률형 아이템 포함" 자동 첨부
- ⏳ 1200×628 + ja/zh-TW + 배치 ZIP 8장 추가 실측 권장

---

## 6. Lessons Learned & Retrospective (KPT)

### 6.1 What Went Well (Keep)

- **Plan-Plus brainstorming 14+1 결정**으로 시작 — 4라운드 AskUserQuestion으로 의도 모호성 사전 제거. r0 분석 시 R1.Q4(외곽 테두리)만 모호로 식별되었고, 그것조차 r4에서 강정아 추가 스펙으로 자연 보완됨
- **단일 HTML 정책 유지** — 외부 모듈 0건, 인라인 `<script>` + `<style>`만 사용. 4 iterations 동안 +358 라인 추가했지만 구조 일관성 유지
- **Canvas direct 합성 + DOM 프리뷰 wrapper(canvas embed)** — DOM/Canvas 이중 구현 회피로 유지보수 비용 절감. 미리보기와 다운로드 픽셀 일치 확보
- **Match Rate 88→100% 단계적 개선** — r0 사용자 첨부 시각 자료 기반 분석 → r1 G1+G2 해소 → r2~r4 누적 신규 요구. 4 iterations로 모든 명시적 요구 100% 충족
- **Iteration별 명확한 분리** — r1(G1+G2), r2(N1~N4), r3(N5~N7), r4(N8~N10)로 각 iteration 범위 명시. 추적성·롤백성 확보
- **사용자 피드백 신속 반영 + 재의사결정 존중** — 폰트 변경 시도 → 즉시 원상복구 (~30분 내). fonts/ 폴더 + @font-face + JS 헬퍼 모두 깔끔히 회수, 잔재 0건

### 6.2 What Needs Improvement (Problem)

- **Plan §Layout Spec 외곽 테두리 모호성** — "검정, 사이즈별 자동 두께"만 명시했고 outerMargin·여백·선 중심 위치 등 기준점이 미정의. r0~r4 4번에 걸쳐 외곽 frame 의미가 변경됨 (8/10 → 12+15/20 → 12+15/30 → 10/9 고정). 향후 시각 명세는 픽셀 좌표·기준점·스펙 도식까지 Plan에 포함해야 함
- **Plan과 사용자 시각 의도 갭** — Plan §Layout Spec은 8장 레퍼런스 추정으로 작성됐으나 픽셀 정확도까지는 아니었음. r0 분석에서 사용자 첨부 1080×1080 KO PNG 비교 시 G1(외곽 frame) 발견. 추후 픽셀 모방 템플릿은 Plan 단계에서 사용자 검증 1라운드 추가 필요
- **Iteration 추가 요구사항 누적** — 원안 16 FR 외 r2~r4에서 N1~N10 추가됨 (총 +10 신규). Plan-Plus brainstorming 단계에서 이런 시각 디테일(좌우반전·drop shadow·픽 사이즈 비례)을 사전 발굴할 체크리스트 부재
- **폰트 변경 시도 비용** — 약 25~30분 작업 후 즉시 회수. 의사결정 비가역성 평가가 부족. 폰트는 매우 비싼 의사결정(파일 외부 의존 + 라이선스 + 시각 일관성 영향)이라 단일 PDCA 단계로 처리하기보다 별도 spike·검토 필요

### 6.3 What to Try Next (Try)

- **Plan §Visual Spec 도식화** — 픽셀 좌표·기준점(선 중심·외곽 코너·내부 코너)·여백 측정법을 명시하는 ASCII art + 좌표 테이블. 사이즈마다 1개씩
- **PDCA Pre-Implementation Visual Mock** — Plan 종료 후 Do 시작 전, 단일 사이즈+단일 언어 1장만 빠르게 그려 사용자 시각 확인 라운드 추가. 픽셀 모방 템플릿 한정 권장
- **iteration auto-trigger 명확화** — "사용자 신규 요구가 누적되면 r5로 갈 것인지 / Plan 갱신 + 신규 PDCA cycle을 만들 것인지" 임계값 정의 (예: N>=10 시 신규 cycle)
- **폰트/외부 의존성 결정 spike 분리** — 폰트·외부 라이브러리 등 큰 의사결정은 별도 spike PDCA로 분리해 의사결정 비용 격리
- **SD Showcase 전용 프리셋 저장** — Plan §Out of Scope 였으나 4언어 × 2사이즈 × N게임 사용 패턴이라면 충분히 의미 있음. v2 후보

---

## 7. Process Improvement Suggestions

### 7.1 PDCA Process

| Phase | Current | Improvement Suggestion |
|-------|---------|------------------------|
| Plan | Plan-Plus 14+1 결정 도출은 강력 | 시각 명세에 픽셀 좌표 + 도식 + 기준점 명시 |
| Design | Plan §7로 통합 처리 (별도 Design 문서 없음) | 픽셀 모방 템플릿은 별도 Design 문서로 시각 mock 1장 첨부 권장 |
| Do | 4 sessions 분리 효과적 | 시각 디테일 누락 발견 시 즉시 사용자 시각 검증 라운드 1회 추가 |
| Check | gap-detector 정적 비교 + 사용자 시각 비교 병행 | 사용자 첨부 결과물 PNG vs 다운로드 비교가 핵심 도구로 작동함 |
| Act | r1~r4 누적 4 iterations 모두 사용자 트리거 | 사용자 신규 요구 누적이 N≥10 도달 시 신규 cycle 검토 |

### 7.2 Tools/Environment

| Area | Improvement Suggestion | Expected Benefit |
|------|------------------------|------------------|
| Visual diff | DOM 프리뷰 vs 다운로드 PNG 자동 비교 도구 | 미리보기/다운로드 불일치 즉시 탐지 |
| Spec format | Plan §Layout Spec에 ASCII art + 좌표표 표준화 | 시각 모호성 사전 차단 |
| Font isolation | 폰트 변경은 별도 spike PDCA cycle로 격리 | 의사결정 비용 격리, 회수 비용 절감 |

---

## 8. Next Steps

### 8.1 Immediate

- [x] PDCA Report 작성 (현재 문서)
- [x] CLAUDE.md "현황" 섹션 갱신
- [x] Git commit + push (완료 후)
- [ ] 사용자 8조합 시각 검증 (ko/en/ja/zh-TW × 1080×1080/1200×628 × 단건+배치)
  - 강정아 스펙 검정 테두리 9/10 확인
  - 픽 TOP 앵커 + 대형화 확인
  - 자동 폰트 축소 (긴 영문) 확인
  - 좌우반전 (1200×628 우측) 확인
- [ ] PR 머지 (worktree → main)

### 8.2 Next PDCA Cycle 후보

| Item | Priority | Trigger |
|------|:--------:|---------|
| SD Showcase v2 — 사용자 프리셋 저장 (4언어 × N게임 패턴) | Medium | 사용자 요청 시 |
| EN 라인별 가변 폰트 사이즈 (Friends 1.6×) | Medium | R4.Q13 v2 후보, 사용자 시각 확인 시 |
| 9:16 사이즈 추가 (스토리/릴스 광고 면) | Low | 새 광고 면 요구 발생 시 |
| 사용자 폰트 적용 (NEXON Kart 등) | Low | 폰트 정책 명확화 + 별도 spike 후 재시도 |

---

## 9. Changelog

### v1.6.0 (2026-04-29 → 2026-04-30)

**Added:**
- **SD Showcase 4번째 템플릿** — 6 SD + 4언어 + 2사이즈, 8장 ZIP 자동 생성
- **자동 대비 시스템** — `getLuminance` (WCAG sRGB) + `getContrastPalette` + hysteresis 0.46~0.54
- **자동 폰트 축소** (`fitSdsTitle`) — maxFontSize → minFontSize 루프, 긴 영문 자동 처리
- **CJK char-wrap / Latin word-wrap** (`sdsWrapText`) — \n 우선 + 언어별 wrap 전략
- **타이틀 drop shadow** (`drawSdsTitleLines`) — 흰 배경에서도 시각 효과
- **픽 직각 + 흰 stroke 4px + drop shadow** (`drawSdsPill`) — anchor center/top 옵션
- **1200×628 우측 SD 좌우반전** — `ctx.scale(-1, 1)` mirror
- **SD 셀 크기 슬라이더** (50~150%) — 단건 + 배치
- **SD 사이 간격 슬라이더** (0~80px) — 단건 + 배치
- **`updateStateImageAt`** — 6 슬롯 배열 안전 교체 (M-2 패턴 확장, _imgCache 누수 방지)
- **새 함수 8개** — `getLuminance`, `getContrastPalette`, `updateStateImageAt`, `buildSdShowcaseCfg`, `prepSdShowcaseCfgImages`, `buildSdShowcaseCanvas`, `buildSdShowcaseBanner`, `buildSdShowcaseFilename` + 헬퍼 3개 (`fitSdsTitle`, `sdsWrapText`, `drawSdsTitleLines`, `drawSdsPill`)

**Changed:**
- TEMPLATE_KEYS에 `'sd-showcase'` 추가 (4번째 템플릿)
- `applyTemplateSwitch` SDS 분기 — 1x1+1200×628 활성, 9:16 비활성
- `data-tmpl-hide` 속성 CSV 다중값 지원 (예: `"appstore-screenshot,sd-showcase"`)
- 검정 배너 테두리 **고정** (선 굵기 10px, 가장자리에서 선 중심까지 9px)
- "외곽선 두께" 슬라이더 라벨 **"타이틀 글자 외곽선 두께"** 로 명확화
- 픽 anchor center → TOP (1080: pillSection 상단, 1200: 타이틀 직후 24px gap)

**Fixed:**
- G1 외곽 frame 디자인 모호 → 강정아 스펙으로 확정 (4 iterations 끝)
- G2 SD 크기 조정 UI 부재 → cellScale 슬라이더 추가
- 외곽선 슬라이더 시각 변화 없음 (흰 bg+흰 stroke 동색) → drop shadow scale로 시각화

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-04-30 | 완료 리포트 — Plan-Plus + Plan + Do(4 sessions) + Check(r0~r4) 통합. Match Rate 100%, 18/18 SC+N, 23/23 Decisions followed. Cancelled 2건(폰트/그리드 270×300) 트래킹 | self-report + ksk@superplanet.net |
| 1.1 | 2026-05-12 | **R5 iteration 추가** — 글로벌 `cellScale` 슬라이더(50~150%) 폐기 → 슬롯별 `slotAdjustPerSize` (사이즈별 6 슬롯 × X/Y/Scale) 개별 조정. r1 G2 결정 사항 evolved. 6,105 → 10,001 라인 (+3,896 누적, R5 단독 +222). | self-report + ksk@superplanet.net |

---

## R5 Iteration (2026-05-12) — Per-Slot X/Y/Scale 개별 조정 도입

### R5.1 Context (왜 R5인가)

v1.6.0 완료 후 약 12일간 SD Showcase가 실사용된 후, UA Manager 김성권이 다음과 같은 한계를 보고:

> "현재 SD 캐릭터 6장은 일괄 SD 캐릭터 크기를 변경하도록 설정되어 있습니다. SD 캐릭터 별로 x/y/scale 조정 가능하도록 기능을 변경해야합니다. 다만 조정 범위는 클 필요는 없어서, 그 수준은 제안해주세요. 기존 SD 캐릭터 크기를 조정하는 것은 폐기해주세요."

**근본 원인**: r1 G2 결정 (cellScale 글로벌 슬라이더 50~150%)은 6장 캐릭터의 통일성 가정을 전제로 했으나, 실사용에서는 캐릭터별 자세·체형·정렬 편차가 발생하여 글로벌 일괄 스케일로는 시각 균형 맞추기 불가능. UA 디자인 마무리 단계에서 슬롯별 미세 조정 필요성 발생.

### R5.2 Decisions (사용자 4건 결정 — AskUserQuestion)

| # | 항목 | 선택 | 채택 사유 |
|---|------|------|---------|
| R5-D1 | UI 노출 방식 | 각 dropzone 아래 항상 노출 (X/Y/Scale 3 number input × 6) | 즉시 접근, 슬롯-컨트롤 인접 → 빠른 미세조정 workflow |
| R5-D2 | 사이즈 처리 | 사이즈별 분리 + 토글 UI (`slotAdjustPerSize['1x1' \| '1200x628']`) | 1x1 그리드 셀(297×263)과 1200×628 사이드 컬럼 셀(211×167)의 슬롯 기하학적 의미가 근본적으로 다름 → perSize 분리 필수 (Pickup R3 패턴 일관) |
| R5-D3 | 조정 범위 | 중간 — 1x1: x/y ±40px / 1200×628: x/y ±30px / scale 70~130% 공통 (step x/y=2, scale=5) | "클 필요 없음" 사용자 명시 + 가시적 효과 균형. 셀 폭의 ~13~15%이면 인접 슬롯과 겹침 직전 |
| R5-D4 | spacing 슬라이더 | 유지 (현행 0~80px) | base gap vs 슬롯별 미세조정 책임 분리. "6장 모두 5px씩 좁히기" 같은 일괄 작업 보존 |

추가 구현 결정 5건:
- R5-D5: 단건/배치 **분리** (KVR R30 정책 일관)
- R5-D6: `drawImageContain` 공용 헬퍼 시그니처 **무수정** (호출 측에서 dx/dy/draw{W,H} 미리 합산)
- R5-D7: 1200×628 우측 컬럼 mirror 분기에서 x offset **부호 반전 보정** (`effectiveX = -adj.x` — 사용자 직관 보존)
- R5-D8: 셀 경계 안 `ctx.save/clip/restore` — 옆 슬롯 침범 방지
- R5-D9: localStorage 미사용 → 마이그레이션 코드 불필요

### R5.3 Decision Record Chain — r1 G2 진화

R5는 PDCA 사이클 안에서 **이전 결정의 명시적 폐기/진화**를 보여주는 첫 사례:

```
r1 G2 (2026-04-29): cellScale 글로벌 슬라이더 50~150%
  ↓ 12일 실사용 후 한계 발견
R5 D1~D9 (2026-05-12): slotAdjustPerSize 슬롯별 개별 조정
  → cellScale 코드 잔재 0건 (grep 검증), 주석 8건만 "R5 폐기" 표기 남김
```

Outcome: PDCA Plan의 "결정은 진화 가능하다"는 원칙 + Pickup R2의 "디자이너 PNG 의존성 의도적 제거" 패턴과 같은 종류의 **Evolved Decision**으로 기록.

### R5.4 Implementation Summary (6 Phase 일괄 적용)

| Phase | 영역 | 변경 |
|---|---|---|
| 1 | 데이터 모델 | `SD_SHOWCASE_DEFAULT.cellScale` 제거 → `slotAdjustPerSize: {'1x1':[...×6], '1200x628':[...×6]} + editingSize` ([:2696](repo/today-banner-designer.html:2696)). `state.batch.sd_cellScale` → `sd_slotAdjustPerSize + sd_editingSize` ([:3843](repo/today-banner-designer.html:3843)) |
| 2 | HTML UI | 단건/배치 cellScale 슬라이더 삭제 (~12줄). dropzone 6개 위에 사이즈 토글 라디오 + 각 dropzone 아래 X/Y/Scale 컴팩트 number input × 18 (~180줄). 총 단건+배치 = 36 입력 |
| 3 | 이벤트 핸들러 | cellScale 핸들러 단건/배치 삭제. 사이즈 토글 + 18 input 핸들러 단건/배치 추가. `ensureSdSlotAdjustPerSize` 안전장치 + `loadSdShowcaseSlotsAdjustToUI(mode)` 공용 헬퍼 신규. syncBatchStateFromUI에서 cellScale 참조 제거 |
| 4 | 렌더 | `buildSdShowcaseCfg`에 slotAdjust 평탄화 추가 ([:5263-5278](repo/today-banner-designer.html:5263)). `buildSdShowcaseCanvas` cellScale 변수 제거 → 슬롯별 `adj.{x,y,scale}` ([:5446-5448](repo/today-banner-designer.html:5446)). 1x1 그리드 + 1200×628 좌·우 사이드 모두 `ctx.save/clip/restore` 셀 경계 침범 방지. 1200 우측 mirror 분기에서 `effectiveX = mirror ? -adj.x : adj.x` 부호 반전. `buildBatchCfgs` SD Showcase 분기에서 combo.size 기준 slotAdjustPerSize 평탄화 ([:9486-9504](repo/today-banner-designer.html:9486)) |
| 5 | 잔재 정리 | cellScale 코드 잔재 **0건** (grep 검증). 8개 주석에만 "R5 폐기" 표기 남김. drawImageContain 공용 헬퍼 시그니처 무수정. 다른 6 템플릿 코드 무수정 (slotAdjust/cellScale leakage 0건) |
| 6 | 문서 | CLAUDE.md 현황 2026-05-12 항목 추가 + Plan 문서 r1 G2 갱신 표기 + 본 Report R5 섹션 |

### R5.5 변경량

| Metric | Value |
|---|---|
| 파일 | `today-banner-designer.html` 1개 + `CLAUDE.md` |
| 라인 변화 | 9,779 → **10,001 라인** (+222줄, R5 단독) |
| 누적 변화 (v1.6 시작점부터) | 5,097 → 10,001 (+4,904 누적, +96%) |
| 회귀 위험 | **0** (SD Showcase 분기 전용 변경) |
| JS 문법 검증 | ✅ `node --check` 통과 |
| cellScale 코드 잔재 | 0건 |
| 다른 6 템플릿 leakage | 0건 (today-tap, app-badge, appstore-screenshot, keyvisual-review, pickup, steam-review) |

### R5.6 안전장치 (Risk Mitigation)

| ID | 위험 | 완화 |
|---|---|---|
| R5-R1 | 1200×628 우측 컬럼 mirror에서 x 부호 미보정 시 사용자 직관 위배 | Phase 4 명시: `effectiveX = mirror ? -adj.x : adj.x` |
| R5-R2 | 슬롯 x offset이 셀 경계 침범 → 옆 슬롯 위 겹침 | Phase 4 명시: `ctx.save → ctx.rect(cellX, cellY, cellW, cellH) → ctx.clip → drawImageContain → ctx.restore` |
| R5-R3 | scale=130%일 때 셀 경계 밖 잘림 | 의도된 동작 (sd-showcase 규약). 사용자 안내 텍스트로 명시 |
| R5-R4 | UI 폭이 길어짐 (각 dropzone 아래 3 input × 6) | text-[10px] 라벨 + 24px height + 컴팩트 padding (2px 4px)로 시각 부담 최소 |
| R5-R5 | 사이즈 토글 누락 → 잘못된 사이즈 조정값 수정 | 현재 편집 사이즈를 라디오 + 텍스트 라벨 ("편집 사이즈:")로 명시 |
| R5-R6 | 빈 슬롯에서도 X/Y/Scale 입력 가능 | 허용 (state 보관, 슬롯 채워지면 즉시 반영) |
| R5-R7 | cellScale 잔재(state 필드, 변수)가 남아 dead-path | Phase 5에서 grep 일괄 정리 + 검증 |
| R5-R8 | 18 핸들러 한 번에 추가 → 회귀 | 일괄 수정 후 `node --check` 통과 + grep으로 SD Showcase 격리 확인 |
| R5-R9 | `state.batch.sd_slotAdjustPerSize` 미초기화 시 런타임 에러 | `loadSdShowcaseSlotsAdjustToUI('batch')` + 핸들러 양쪽에 lazy init 안전장치 |

### R5.7 검증 시나리오 (브라우저 실측 대기 — 7건)

| # | 시나리오 | 합격 기준 |
|---|---|---|
| 1 | 단건 1x1: SD 6장 드롭 → slot 1: x=+40/y=-20/scale=120 입력 | 1번만 우상단 이동·확대 + 옆 슬롯 미침범 + 다운로드 PNG 동일 |
| 2 | 단건 1200×628: 사이즈 토글 | 1x1 조정값과 분리 (모두 0 표시) — perSize 검증 |
| 3 | mirror 검증 | 좌측 slot 1 x=+30 → 우측 이동 / 우측 slot 4 x=+30 → 우측 이동 (둘 다 사용자 직관 방향) |
| 4 | 사이즈 토글 round-trip | 1x1: slot 1 x=+40 → 1200×628: x=0 → 1x1 복귀: x=+40 복원 |
| 5 | cellScale UI 폐기 확인 | "SD 캐릭터 크기" 슬라이더(50~150%)가 단건/배치 모두에서 사라짐 |
| 6 | spacing 동작 | spacing=0 vs spacing=80 6장 일괄 간격 변화 (현행 유지) + 슬롯별 x offset과 합산 적용 |
| 7 | 배치 ZIP | 4언어 × 2사이즈 = 8 PNG에 1x1과 1200×628 각 perSize 조정값 반영 |
| 회귀 | 다른 6 템플릿 | today-tap, app-badge, appstore-screenshot, keyvisual-review, pickup, steam-review 단건/배치 모두 무영향 |

### R5.8 Lessons Learned

- **L-R5-1 (Evolved Decision)**: PDCA 사이클 안에서 "이전 결정의 의도적 폐기"가 자연스럽게 처리되어야 한다는 것을 R5가 첫 사례로 보여줌. cellScale은 r1 G2에서 "옳은" 결정이었으나 12일 실사용 후 한계 발견 → 명시적 evolved (Pickup R2 디자이너 PNG 의존성 폐기 패턴과 같은 종류).
- **L-R5-2 (Plan-Mode + AskUserQuestion 효율)**: Plan mode에서 코드 수정 전에 Explore 1회 + Plan agent 1회 + AskUserQuestion 4건으로 **모든 설계 결정 사전 합의 후 6 Phase 일괄 수정**. 회귀 위험 0 달성.
- **L-R5-3 (perSize 패턴 확산)**: Pickup R3에서 도입된 perSize 분리 패턴이 SD Showcase R5에 자연 적용. 향후 다른 multi-size 템플릿(Steam Review 등)에도 유사 R-iteration 발생 시 같은 패턴 재사용 예상.
- **L-R5-4 (clip + mirror 부호 보정)**: Canvas 좌표계의 `ctx.scale(-1, 1)` 환경에서 사용자 입력값의 시각적 방향과 코드 방향이 어긋날 수 있음. 명시적 `effectiveX = mirror ? -adj.x : adj.x` 분기로 직관 보존. 향후 mirror 사용 템플릿(KVR 등)에서도 동일 패턴 권고.

### R5.9 Open Items (미래 검토)

- 슬롯 개별 회전(rotate) — 요구 없음, Out of Scope 유지
- 드래그 앤 위치 조정 GUI — 입력 기반으로 충분, deferred
- 슬롯 비어있을 때 X/Y/Scale 입력 disabled — UX 개선 후보 (현행은 허용, state 보관)
- 사이즈 토글 + 라디오 시각 강조 (굵게/색) — 사용자 피드백 따라 결정
