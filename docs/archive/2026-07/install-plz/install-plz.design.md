# PDCA Design — Install Plz 템플릿 (v1.15)

**Feature**: install-plz
**Created**: 2026-07-19
**Plan Ref**: `docs/01-plan/features/install-plz.plan.md`

---

## Context Anchor

| Key | Value |
|-----|-------|
| **WHY** | 밈 폰트가 툴 폰트 스택에 없음 → 레퍼런스 원본 픽셀 추출(플레이트)만이 "폰트 아예 변경 없이"를 만족 |
| **WHO** | UA Manager — SD 1장 교체로 4언어×2사이즈 8장 재생산 |
| **RISK** | 문구 고정(의도됨) / 외부 에셋 canvas taint(file:// 미지원, pickup과 동일) / 플레이트 경계값은 이 레퍼런스 전용 |
| **SUCCESS** | 8장 텍스트 픽셀 원본 동일, 캐릭터 잔여물 0, Single+Batch 동작, 기존 9 템플릿 회귀 0 |
| **SCOPE** | Do-1 에셋 / Do-2 코드 (아키텍처: 기존 최신 템플릿 패턴 준수 — Pragmatic) |

## Architecture 선택

기존 코드베이스에 확립된 템플릿 추가 패턴이 유일한 합리적 구조라 3안 비교 생략 (Option C — Pragmatic 자동 선택):
**pickup/steam-review 패턴** = `state.single.installplz` + `state.batch.installplz` 노드, `buildInstallPlzCfg(stateNode, lang, size)` 공용 cfg 빌더, 외부 에셋 + `loadCachedImage`.

---

## 1. 에셋 스펙 (Do-1)

### 1.1 파일 구성 — `assets/install-plz/`

| 파일 | 크기 | 내용 |
|---|---|---|
| `text-plate_{ko\|en\|ja\|zh-TW}_1x1.png` | 1080×1080 | 텍스트 플레이트 (흰 배경 + 원본 텍스트 크롭) |
| `text-plate_{ko\|en\|ja\|zh-TW}_1200x628.png` | 1200×628 | 〃 (원본 625 + 하단 3px 흰 패딩) |
| `make_plates.py` | — | 생성 스크립트 보존 (R-04: 새 레퍼런스 시 재실행) |

### 1.2 플레이트 생성 파라미터 (사전 검증 확정값)

**1080×1080** — 상단 밴드 `[0..Y1)` + 하단 밴드 `[Y2..1080)` 크롭, 나머지 흰색:

| lang | Y1 | Y2 | 비고 |
|---|---|---|---|
| ko | 212 | 811 | 고지문구(y15-29) 상단 밴드에 자연 포함 |
| en | 252 | 823 | 하단 2줄("PLEASE TRY"+"OUR GAME") 모두 포함 |
| ja | 245 | 823 | |
| zh-TW | 245 | 823 | |

**1200×628** — 좌측 텍스트 rect `[0..X1) × [0..553)` 크롭:

| lang | X1 | 추가 처리 |
|---|---|---|
| ko | 631 | 고지문구 스탬프: 원본 `(1050,8)-(1192,40)` → 동일 좌표 |
| en | 612 | |
| ja | 624 | |
| zh-TW | 549 | |

**공통 후처리**: blue-key 정리 — `B-R>50 && B>140` 픽셀을 흰색으로 (물방울/웅덩이 파편 제거, 텍스트는 검정/흰/빨강/회색이라 무영향). KO 고지문구 스탬프는 blue-key **이후** 적용.

## 2. Canvas 좌표 스펙

```js
const INSTALL_PLZ_CANVAS_SPECS = {
  '1x1':      { w: 1080, h: 1080, sd: { x: 258, y: 240, w: 587, h: 570 } },
  '1200x628': { w: 1200, h: 628,  sd: { x: 609, y: 25,  w: 587, h: 570 } },
};
```
- `sd` = 원본 레퍼런스의 캐릭터 배치 rect (두 사이즈 모두 587×570 실측) → SD 기본 박스
- `INSTALL_PLZ_ASSETS[lang][sizeKey]` = 플레이트 경로 매핑

## 3. State / Default

```js
const INSTALL_PLZ_DEFAULT = {
  sdImage: null,                       // SD 1장 공용 (data URL)
  slotAdjustPerSize: {                 // 사이즈별 X/Y/Scale (sd-showcase R5 패턴, 슬롯 1개)
    '1x1':      { x: 0, y: 0, scale: 100 },
    '1200x628': { x: 0, y: 0, scale: 100 },
  },
  editingSize: '1x1',
};
// state.single.installplz / state.batch.installplz = deep copy
```
슬라이더 범위: X/Y ±250px (step 5), Scale 50~**250**% (step 5) — SD 박스(587×570)가 캔버스 대비 크므로 sd-showcase(±40)보다 넓게. (R1 iterate: 세로로 긴 SD 소스가 contain-fit 시 작아 보임 → 상한 150→250 확장, 양 사이즈 공통)

## 4. 렌더 파이프라인 (FR-08)

```
buildInstallPlzCfg(stateNode, lang, size)
  → { template, size, lang, sdImage, adj: {x,y,scale}, plateSrc: INSTALL_PLZ_ASSETS[lang][size] }
prepInstallPlzCfgImages(cfg)
  → { ...cfg, _plateImg, _sdImg }        // loadCachedImage ×2 (배치 시 캐시 hit)
buildInstallPlzCanvas(cfg)
  ① fillRect 흰색 (플레이트 로드 실패 방어)
  ② drawImage(_plateImg, 0, 0)           // 무스케일 — 픽셀 정합 (NFR-02)
  ③ SD: s=scale/100; bw=sd.w*s; bh=sd.h*s;
     bx=sd.x+adj.x+(sd.w-bw)/2; by=sd.y+adj.y+(sd.h-bh)/2;
     drawImageContain(ctx, _sdImg, bx, by, bw, bh)   // null이면 skip (SC-06)
```
- 레이어: 플레이트 → SD (SD가 위 — 스케일 업 시 텍스트 위로 올라올 수 있으나 사용자 조정 영역)
- 텍스트/고지문구/폰트 렌더링 **없음** (플레이트 내장) — `ensureFontsLoaded` 불필요하나 파이프라인 일관성 위해 호출 유지
- DOM 프리뷰: `buildInstallPlzBanner(cfg)` — canvas embed wrapper (buildSdShowcaseBanner 패턴)
- 파일명: `installplz_{lang}_{1080x1080|1200x628}.{ext}` (`buildInstallPlzFilename`)

## 5. UI 설계

### 5.1 단건 (data-tmpl="install-plz")
- SD 드롭존 1개 `#s-ip-sd` (setupDropzone + updateStateImage)
- 편집 사이즈 라디오 `s-ip-editsize` (1×1 / 1200×628) — sd-showcase 패턴
- X/Y/Scale 슬라이더 3개 `#s-ip-{x,y,scale}` + 값 라벨 — 편집 사이즈의 adj에 바인딩
- 안내문: "텍스트·고지문구는 레퍼런스 원본 이미지 고정 (편집 불가)"

### 5.2 배치 (data-tmpl="install-plz")
- 글로벌: SD 드롭존 `#b-ip-sd` + 편집 사이즈 라디오 + X/Y/Scale 슬라이더 (state.batch.installplz)
- `renderBatchLangFields` 분기: 언어별 입력 필드 없음 — 안내 문구만 렌더 (FR-11)
- `buildBatchCfgs` 분기: `buildInstallPlzCfg(state.batch.installplz, combo.lang, combo.size)` — 선택 사이즈 × 4언어

### 5.3 템플릿 스위치 (FR-04)
- 헤더 `<option value="install-plz">Install Plz</option>` (10번째)
- `applyTemplateSwitch`: 1x1+1200x628 활성 / 9x16 비활성 (steam-review 분기와 동일 로직의 신규 else-if)
- 배치 사이즈 체크박스: 1x1+1200x628 체크·활성, 나머지 비활성
- `data-tmpl-hide` 목록 4곳에 `install-plz` 추가 (today-tap 전용 필드 숨김)
- 프리뷰 메타 라벨맵 + 배치 라벨맵에 'Install Plz' 추가

## 6. 변경 지점 매핑 (Do-2)

| 위치 (v1.14 기준) | 변경 |
|---|---|
| L925 부근 헤더 select | option 추가 |
| L1121 부근 단건 패널 | data-tmpl="install-plz" 블록 신규 |
| L2108 부근 배치 패널 | data-tmpl="install-plz" 블록 신규 |
| L1743/1749/1992/2011 data-tmpl-hide | install-plz 추가 |
| L2788 TEMPLATE_KEYS | 'install-plz' 추가 |
| L3600 부근 상수 영역 | INSTALL_PLZ_ASSETS/SPECS/DEFAULT 신규 |
| L4447/4523 state init | single.installplz / batch.installplz 추가 |
| renderBanner (L4881 부근) | install-plz 분기 → buildInstallPlzBanner |
| L6980 부근 | buildInstallPlzCfg/prep/Canvas/Banner/Filename 신규 (~120라인) |
| buildBannerCanvas (L7954 부근) | 분기 추가 |
| 단건 UI 바인딩 (L8283 부근) | s-ip-* 바인딩 + loadInstallPlzToUI |
| 배치 UI 바인딩 (L8942 부근) | b-ip-* 바인딩 |
| applyTemplateSwitch (L9647/9727) | 사이즈 잠금 분기 + UI 로드 훅 |
| refreshSinglePreview (L10036) | cfg 분기 + 라벨맵 |
| handleSingleDownload (L10102) | 파일명 + canvas 경로 분기 |
| renderBatchLangFields (L10852) | isIp 안내문 분기 |
| buildBatchCfgs (L11247) | isIp cfg 분기 |
| 배치 canvas 루프 (L11632) | isIp prep 분기 |

## 7. Test Plan (Check)

1. Single: 4언어 × 2사이즈 = 8조합 프리뷰 렌더 + 플레이트 스왑 확인 (콘솔 에러 0)
2. Single: SD 업로드 → 합성 표시, X/Y/Scale 사이즈별 독립 반영, 다운로드 파일명 규칙
3. Single: SD 미업로드 다운로드 → 플레이트만 (에러 없음)
4. Batch: 2사이즈+4언어 ZIP 8장, KO 2장만 고지문구(플레이트 내장분) 확인
5. 픽셀 정합: 다운로드 PNG의 텍스트 영역 vs 원본 레퍼런스 diff = 0 (Python 검증)
6. 회귀: 기존 9 템플릿 프리뷰 + 단건 다운로드 정상, 9:16/4:5 잠금 로직 상호 오염 없음

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-07-19 | 최초 — 검증 확정값 기반 에셋/좌표/파이프라인/UI 설계 |
