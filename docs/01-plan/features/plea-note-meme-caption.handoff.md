# Handoff — 손글씨 플리(plea-note) · 밈 캡션(meme-caption) 템플릿 + 4:5 규격

> **용도**: claude.ai 리서치 세션 → Claude Code 이관 문서. Claude Code는 이 문서를 입력으로 `/plan-plus` → `/pdca plan`을 진행한다.
> 이 문서는 **Plan 이전 브리프**다. 결정사항 표의 "확인 필요" 항목은 Plan 단계에서 사용자에게 먼저 묻는다 (CLAUDE.md §1·§2).
>
> - 작성: 2026-11-09 · 요청자: ksk@superplanet.net
> - 대상 파일: `today-banner-designer.html` (단일 HTML)
> - 신규 템플릿 2종 → 13·14번째 템플릿

---

## 1. 배경 (왜 만드는가)

2026-11-09 경쟁사 레퍼런스 리서치(CookApps 「카드 오브 데몬슬레이어」, Meta 광고 115건 · US/TW)에서
기존 12종 템플릿으로 재현이 안 되는 이미지 포맷 2종이 확인됐다.

| 레퍼런스 포맷 | 경쟁사 운영 | 기존 템플릿과의 관계 |
|---|---|---|
| **손글씨 플리 노트** — 흰 배경 + 손글씨 호소 카피("I really, really made a fun card roguelike game. **Please try it once!!**") + 빨간 강조·물결 밑줄 + 마스코트·카드 소품 + "Download Now" 말풍선 CTA | US·TW **공통 메인 컨셉** (동일 포맷 현지화) | `install-plz`와 컨셉 유사하나 install-plz는 **텍스트 플레이트 고정(편집 불가)**. 문구 편집형이 없음 |
| **밈 캡션** — 키아트 풀블리드 + 상단/하단 굵은 흰 글씨·검은 외곽선("YOU JUST ACTIVATED / MY TRAP CARD") | US | 해당 템플릿 없음 |

- 레퍼런스 원본은 비공개 Drive에만 있다: `내 드라이브 > 레퍼런스 서치 모음 > 261109_카드오브데몬슬레이어(쿡앱스)`
  - 손글씨 플리: `Meta_CoDS_1522620356342175_deck.jpg`(US), `Meta_CoDS_2433273020746443_deck.jpg`(TW), `Meta_CoDS_953716527441641_deck.jpg`(US, 쿠폰코드 변형)
  - 밈 캡션: `Meta_CoDS_1094080630272192_deck.jpg`(US)
- ⚠️ **경쟁사 소재 이미지를 이 저장소(public, GitHub Pages)에 커밋하지 말 것.** 시각 확인이 필요하면 사용자에게 로컬 경로로 받는다.
- 레퍼런스 소재는 전부 **4:5(1080×1350)** — Meta 피드 표준. 그래서 4:5를 신규 템플릿 기본 규격으로 넣는다.

---

## 2. 범위

### In scope
1. 신규 템플릿 `plea-note` (손글씨 플리) — 1:1 + **4:5**
2. 신규 템플릿 `meme-caption` (밈 캡션) — 1:1 + **4:5**
3. 두 템플릿 모두 **ko / en / ja / zh-TW** × **Single + Batch** (CLAUDE.md §3 정책)
4. 파일명 규칙 상속: `CONCEPT_TOKEN` 2줄 + `assetDim()` 분기 2개
5. README · CLAUDE.md §5(현재 상태, 덮어쓰기) 갱신

### Out of scope (v1)
- 기존 12종 템플릿에 4:5 추가 → 결정 D2
- 9:16 · 1200×628 지원 (신규 2종) → v2 후보
- 자동 번역 (정책상 도입 안 함 — 4언어 직접 입력)

---

## 3. 결정사항

| # | 항목 | 기본안 (이 문서 기준) | 상태 |
|---|---|---|---|
| D1 | 손글씨 플리를 **신규 템플릿**으로 vs **install-plz의 "손글씨 모드"** | 신규 템플릿 `plea-note`. 이유: install-plz는 "원본 플레이트 고정·폰트 무변형"이 설계 전제(design §1~2)라 모드 추가 시 분기 복잡도↑, Surgical changes 원칙상 기존 템플릿 무수정이 안전 | **확인 필요** |
| D2 | 4:5를 신규 2종에만 vs 기존 템플릿에도 | 신규 2종에만. `SIZE_PACK['4x5']`는 이미 존재(v1.11 GP 전용) → 재사용 | **확인 필요** |
| D3 | 손글씨 폰트 (4언어) | §6.1 후보표 기준, Google Fonts 가용성·글리프 커버리지 실측 후 확정 | **검증 필요** |
| D4 | 밈 폰트 (4언어) | §6.2 후보표 기준, 동일 검증 | **검증 필요** |
| D5 | KO 확률형 아이템 고지문구 | 기존 템플릿과 동일하게 KO만 토글 제공 (기본 OFF) | 기본안 |
| D6 | 소재컨셉 토큰 | `plea-note: '손글씨플리'`, `meme-caption: '밈캡션'` | 기본안 |

---

## 4. 템플릿 A — `plea-note` (손글씨 플리)

### 4.1 구성 요소
| 요소 | 입력 | 언어별 | 비고 |
|---|---|---|---|
| 본문(호소 카피) | 멀티라인 textarea | ✅ | `[ ]` = 빨간색 강조, `{ }` = 빨간 물결 밑줄 (chalkboard의 `[대괄호]` 강조 규칙과 일관) |
| 꼬리말 | 1줄 (예: `Please... :'(`) | ✅ | 본문 아래 우측 정렬, 작은 크기 |
| 쿠폰 코드 | 1줄 (예: `WELCOMEGIFT`), 비우면 미표시 | 공용 | 따옴표로 감싸 크게 (`'WELCOMEGIFT'`) |
| CTA 말풍선 | 1줄 | ✅ | 연두 필(`#D9F2B4`) + 검은 손그림 테두리 + 마우스 커서 아이콘(캔버스 드로잉) |
| 캐릭터 | 투명 PNG 1장 | 공용 | 위치/크기 `adjPerSize` |
| 소품(카드 등) | 투명 PNG 1장, 선택 | 공용 | 위치/크기 `adjPerSize` |
| 낙서 효과선 | 토글 (기본 ON) | 공용 | 캐릭터 주변 `\\ //` 손그림 강조선, 캔버스 드로잉 |
| 배경 | 흰색 고정 `#FFFFFF` | — | |

### 4.2 레이아웃 (`PLEA_NOTE_CANVAS`, chalkboard `CHALKBOARD_CANVAS` 패턴)
```
'4x5' (1080×1350):
  body:       { x: 70, y: 80, maxW: 940, fsMax: 84, fsMin: 44, lineH: 1.28 }   // 자동 축소
  tail:       { right: 70, gapTop: 18, fs: 40 }
  coupon:     { cx: 540, gapTop: 40, fs: 96 }                                  // 있을 때만, 본문 아래
  artZone:    { x: 40, y: 620, w: 1000, h: 560 }                               // 캐릭터+소품 contain
  cta:        { cx: 560, cy: 1215, h: 96, padX: 56, minW: 380, fs: 46 }
  disclaimer: { right: 24, baseline: 1338, fs: 20 }
'1x1' (1080×1080):
  body:       { x: 60, y: 60, maxW: 960, fsMax: 72, fsMin: 40, lineH: 1.26 }
  tail:       { right: 60, gapTop: 14, fs: 34 }
  coupon:     { cx: 540, gapTop: 30, fs: 80 }
  artZone:    { x: 40, y: 500, w: 1000, h: 440 }
  cta:        { cx: 560, cy: 990, h: 84, padX: 48, minW: 340, fs: 40 }
  disclaimer: { right: 22, baseline: 1068, fs: 20 }
```
- 본문이 길어 `artZone`을 침범하면: 폰트 축소 → `fsMin` 도달 시 `artZone.y`를 아래로 밀고 artZone 높이를 줄인다 (텍스트 우선).
- 위 수치는 레퍼런스 실측 비율 환산 초안. Design 단계에서 실렌더 보고 조정.

### 4.3 기본 카피 (`PLEA_NOTE_DEFAULT.langs` — 사용자가 수정)
| lang | body | tail | cta |
|---|---|---|---|
| ko | `정말 {진심으로} 만든\n카드 로그라이크 게임이에요.\n[딱 한 번만 해주세요!!]` | `제발요… ㅠㅠ` | `지금 설치` |
| en | `We {really, really} made\na fun card roguelike game.\n[Please try it once!!]` | `Please… :'(` | `Download Now` |
| ja | `{本気で}作った\nカードローグライクです。\n[一回だけ遊んでください!!]` | `お願い…(；；)` | `今すぐインストール` |
| zh-TW | `這是我們{認真}做的\n卡牌肉鴿遊戲\n[拜託你玩一次吧!!]` | `拜託了… Q_Q` | `立即安裝` |

---

## 5. 템플릿 B — `meme-caption` (밈 캡션)

### 5.1 구성 요소
| 요소 | 입력 | 언어별 | 비고 |
|---|---|---|---|
| 배경 키아트 | 이미지 1장 | 공용 | cover-fit + 초점 X/Y 슬라이더(`adjPerSize`) |
| 상단 텍스트 | 1~2줄 | ✅ | 흰 글씨 + 검은 외곽선 |
| 하단 텍스트 | 1~2줄 | ✅ | 동일 |
| 대문자 변환 | 토글 (기본 ON, **en만 적용**) | — | ko/ja/zh-TW 무시 |
| 가독 그라데이션 | 토글 (기본 OFF) | 공용 | 상·하단 검정 30%→0% 띠 |
| 로고 | 투명 PNG, 선택 | 공용 | 하단 텍스트와 겹치지 않는 우하단 소형 |

### 5.2 렌더 규칙
- 텍스트: `fillStyle #FFFFFF`, `strokeStyle #000000`, `lineWidth = fs × 0.14`, `lineJoin = 'round'`, **stroke 먼저 → fill** (외곽선이 글자 안쪽을 먹지 않게)
- 자동 축소: 줄당 `maxW = W − 2×margin`에 맞을 때까지 축소, 2줄 초과 시 줄바꿈 후 재축소
```
'4x5':  { margin: 44, top: { y: 40 },  bottom: { yFromBottom: 40 }, fsMax: 128, fsMin: 56 }
'1x1':  { margin: 40, top: { y: 32 },  bottom: { yFromBottom: 32 }, fsMax: 116, fsMin: 52 }
```

### 5.3 기본 카피
| lang | top | bottom |
|---|---|---|
| ko | `딱 한 판만 하려다가` | `새벽 3시` |
| en | `ME AFTER "ONE MORE RUN"` | `AT 3 AM` |
| ja | `あと1回だけのつもりが` | `気づけば朝` |
| zh-TW | `本來只想再玩一局` | `結果天亮了` |

---

## 6. 폰트 (D3·D4 — 실측 검증 후 확정)

기존 규칙: `getFontFamilyForLang()` + `data-lang` + Canvas 폰트 스왑. 신규 폰트는 chalkboard처럼 `FontFace` 로드 후 렌더 (`document.fonts.load` 완료 대기 필수 — 배치 첫 장 폴백 폰트 렌더 방지).

### 6.1 손글씨 (plea-note)
| lang | 1순위 후보 | 대안 | 비고 |
|---|---|---|---|
| ko / en | 온글잎 하루치 개구리체 (`assets/chalkboard/OwnglyphHaruchiFrog-Rg.ttf`, **기존 에셋 재사용**) | Nanum Pen Script / Gaegu | 한글+라틴 포함 확인됨(chalkboard) |
| ja | Yomogi | Klee One / Zen Kurenaido | 가나+상용 한자 커버리지 확인 |
| zh-TW | LXGW WenKai TC | Noto Sans TC (폴백) | 번체 상용자 커버리지 확인 |

### 6.2 밈 (meme-caption)
| lang | 1순위 후보 | 대안 |
|---|---|---|
| en | Anton | Bebas Neue |
| ko | Black Han Sans | Do Hyeon |
| ja | Dela Gothic One | Noto Sans JP 900 |
| zh-TW | Noto Sans TC 900 | — |

**검증 방법**: 4언어 기본 카피 전 글자를 각 폰트로 렌더 → 두부(□) 0개 확인. 미포함 시 대안으로 교체하고 Plan에 기록.

---

## 7. 구현 가이드 (기존 코드 기준 포인트)

| 작업 | 위치 (2026-11-09 main 기준 대략) | 내용 |
|---|---|---|
| 템플릿 등록 | `<option value=…>` (L937~948), `TEMPLATE_KEYS` (L3194), `tmplLabelMap` (L11703) | `plea-note`, `meme-caption` 추가 |
| 규격 | `SIZE_PACK['4x5']` (L3320) | 이미 존재 — 주석에 신규 템플릿 사용 명시만 |
| 파일명 | `CONCEPT_TOKEN` (L11922), `assetDim()` (L11946) | 토큰 2줄 + 분기 `(size === '4x5') ? [1080,1350] : [1080,1080]` |
| 상수 | chalkboard 상수 블록(L4515~) 다음 | `PLEA_NOTE_CANVAS / _DEFAULT`, `MEME_CAPTION_CANVAS / _DEFAULT` |
| 렌더 | `buildChalkboardCfg / Canvas / Banner` (L8596 / 8856 / 8935) 패턴 복제 | `build{PleaNote,MemeCaption}{Cfg,Canvas,Banner}` |
| UI | `data-tmpl="chalkboard"` 단건·배치 패널 패턴 | 언어별 입력 + 공용 이미지 슬롯 + 사이즈별 위치 슬라이더 |
| 템플릿 전환 | L11270, L11370, L11452 (install-plz/chalkboard 분기) | 신규 2종 분기 추가 |
| 사이즈 선택 | 단건/배치 사이즈 체크박스 | 신규 2종 선택 시 `1x1`·`4x5`만 노출 (GP의 4x5 노출 로직 참고) |

---

## 8. 성공 기준 (Goal-driven — 완료 시 이 기준으로 검증)

| # | 기준 | 검증 방법 |
|---|---|---|
| SC-1 | 각 템플릿 Single export 1장이 지정 규격과 실제 픽셀 일치 (1080×1080 / 1080×1350) | PIL로 파일 크기 확인 |
| SC-2 | Batch: 4언어 × 2규격 = **템플릿당 8장**, ZIP 내 중복 0 | ZIP 목록 검사 |
| SC-3 | 파일명 `{한/영/일/번}_{제목코드}_{손글씨플리\|밈캡션}_{WxH}.png` | 정규식 검사 |
| SC-4 | 4언어 기본 카피 렌더 시 두부(□) 0, 폴백 폰트 렌더 0 (배치 첫 장 포함) | 8장 육안 + 폰트 로드 대기 확인 |
| SC-5 | 텍스트 오버플로 0 — 짧은/긴/아주 긴 카피 3세트 × 4언어 × 2규격 | 캔버스 밖·영역 침범 없음 |
| SC-6 | 밈 외곽선 가독성: 밝은·어두운 배경 각 1장에서 판독 가능 | 육안 |
| SC-7 | `[ ]` 강조·`{ }` 물결 밑줄이 줄바꿈 경계에서도 정상 | 경계 케이스 카피 렌더 |
| SC-8 | **기존 12종 회귀 없음**: today-tap·install-plz·google-play-screenshot(4x5 포함) 산출물 파일명·픽셀 규격 변경 전과 동일 | 변경 전후 샘플 비교 |
| SC-9 | HTTP로 열어 정상 동작 (`python -m http.server`) | CLAUDE.md §5 주의사항 |

---

## 9. Claude Code 시작 프롬프트 (복사해서 사용)

```
docs/01-plan/features/plea-note-meme-caption.handoff.md 를 읽고,
CLAUDE.md 규칙에 따라 /plan-plus → /pdca plan 으로 Plan 문서를 만들어줘.
먼저 §3 결정사항 중 "확인 필요"(D1, D2)를 나에게 질문하고,
D3·D4 폰트는 Google Fonts에서 4언어 기본 카피 글리프 커버리지를 실측해서 제안해줘.
구현은 Plan 승인 후 템플릿 A(plea-note) → B(meme-caption) 순서로 진행.
```
