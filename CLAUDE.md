# CLAUDE.md — Today Banner Designer

이 파일은 **이 프로젝트 고유 규칙 + 작업 규율**만 담는다.
역할·커뮤니케이션(한/영)·자율성 경계·free-tier 기본값은 전역 `~/.claude/CLAUDE.md`가 이미 규정하므로 여기서 중복하지 않는다.

---

## 1. 작업 규율

- **Think before coding**: 가정은 명시한다. 모호하면 추측하지 말고 멈춰서 묻는다. 해석이 갈리면 임의로 하나 고르지 말고 제시한다.
- **Surgical changes**: 요청과 직접 연결된 라인만 수정. 인접 코드·주석·포맷을 임의로 "개선"하지 않는다. 안 깨진 건 리팩터링하지 않는다. 기존 스타일을 따른다. 내 변경이 만든 orphan만 정리한다.
- **Goal-driven**: 작업 전 성공 기준을 정하고, 끝나면 그 기준으로 검증한다 ("동작하게" 같은 약한 기준 금지).
- **Simplicity**: 요청 범위만. 추측성 추상화·설정·불필요한 방어코드 금지.

## 2. 절대 하지 말 것

- 내 허락 없이 파일 삭제 금지
- 모르면 추측하지 말고 반드시 묻기
- 작업 중간에 임의로 다른 방향으로 바꾸지 말 것

## 3. 정책 (모든 신규 템플릿에 적용 — v1.5+)

- **Single 모드 + Batch 모드 양쪽 지원 의무**: 모든 신규 템플릿은 단건 export(현재 화면 1장)와 배치 export(언어/사이즈/테마 조합 ZIP) 둘 다 제공해야 한다. 다국어 UA 운영 워크플로우 요구사항이며, 새 템플릿 PR은 양쪽 동작을 검증한다.
- **다국어 4종 기본**: ko / en / ja / zh-TW LANG_PACK 확장이 디폴트. 일부 템플릿이 별도 LANG_PACK(예: AS_LANG_PACK)을 둘 수 있으나 동일한 4언어 키를 쓴다.
- **언어별 폰트 자동 스왑**: Pretendard(ko/en) / Noto Sans JP(ja) / Noto Sans TC(zh-TW). `data-lang` 속성 + CSS 셀렉터 + Canvas의 `getFontFamilyForLang/asFontFamily`로 일관 적용.
- **사용자 결정 (2026-04-25, App Store Screenshot 기준)**:
  - 자동 번역 도입 안 함 → 4언어 직접 입력
  - 픽셀 퍼펙트 모방 → 외관은 실 App Store 페이지 충실 재현
  - 테마는 디자인 1개당 1테마 (다크 또는 라이트 단일) — Batch ZIP은 4언어 × 1테마 = 4장
  - 키아트는 4언어 공용 (1장 업로드)
  - 디바이스 프레임(베젤) 미포함 → App Store 페이지 자체만 9:16 채움
  - 로케일 전용 컬럼(한국 등급/이벤트 등)은 4컬럼으로 통일

## 4. 프로젝트 개요

- **본체**: `today-banner-designer.html` (단일 HTML 사내 툴, Apple "Today" 스타일 광고 배너 생성)
- **문서**: `README.md` / PDCA 문서는 `docs/01-plan ~ 04-report`
- **담당**: UA Manager 김성권 (ksk@superplanet.net)
- **repo**: https://github.com/sungkk1m/mkt_bannerdesigner (main)

## 5. 현재 상태  (갱신 시 덮어쓰기 — 누적 금지, 5~10줄 이내)

- 템플릿 11종: today-tap, app-badge, sd-showcase, keyvisual-review, pickup, steam-review, ask-me-anything, appstore-screenshot, google-play-screenshot, install-plz, chalkboard
- 최신 작업: **chalkboard (v1.19)** — 칠판 배경(사이즈별 data URL 인라인 — file://에서도 로드, 원본 `assets/chalkboard/bg_{1x1,1200x628}.webp`) + 리본/헤드라인([대괄호] 강조)/타이틀/본문/낙서/CTA 언어별 입력 + 캐릭터·로고 1장 공용. 1080×1080 + 1200×628, 캐릭터·로고·타이틀 위치/크기는 `adjPerSize` 사이즈별 저장, 소재컨셉 `칠판`. 칠판 글씨 = 온글잎 하루치 개구리체(`assets/chalkboard/*.ttf`, FontFace 로드) — 가나·한자 미포함이라 ja/zh-TW는 Noto 대체
- 직전 작업: **filename-rule (v1.18, `feature/filename-rule` 브랜치)** — 전 템플릿 파일명을 실무 규칙 `{언어}_{타이틀}_{소재컨셉}_{가로x세로}.{ext}`로 통일 (예: `한_SMS_투데이탭_1080x1080.png`). 언어 토큰 한/영/일/번, 소재컨셉 10종(투데이탭/앱아이콘/앱스토어/SD쇼케이스/아이폰리뷰/픽업/스팀리뷰/무물보/구글플레이/설치구걸), 테마는 괄호 병기 `구글플레이(다크)`, 규격은 scale 반영 실제 픽셀, 타이틀 미입력 시 `TITLE`
- 구조: `buildAssetFilename()` 중앙 함수 1개가 유일한 파일명 조립 지점 (구 빌더 10개 + asSizeDim + slugify 제거). 단건 `#s-title-code` 입력 신설, 배치 `#b-prefix` 재사용. 신규 템플릿은 `CONCEPT_TOKEN`에 1줄 추가하면 규칙 자동 상속
- 검증: **실측 완료(2026-08-27)** — 산출물 88장 전수 PASS (파일명 패턴·규격=실제픽셀·중복 0·GP 16장 충돌 0). main 머지 대기 (상세: `docs/01-plan/features/filename-rule.plan.md` §11)
- ⚠️ **툴은 반드시 HTTP로 열 것** (`python -m http.server` 등). `file://`로 열면 `crossOrigin='anonymous'` 탓에 `assets/*.png` 경로 참조 에셋이 CORS 차단돼 로드 실패 → install-plz 백지, pickup 프레임·별이 fallback 드로잉으로 대체됨 (인라인 data URL 에셋은 무영향). 근본 수정 미착수
- 참고: 구 store-listing v1.5 미커밋 553줄은 git stash 보존 (`backup: stale store-listing v1.5 work ...`)
- 4언어(ko/en/ja/zh-TW) × Single+Batch 전 템플릿 지원

## 6. 이력·히스토리 참조 규칙  ★

- 과거 PDCA 상세(Plan/Design/Analysis/Report)와 결정 근거는 `docs/01-plan ~ 04-report`, `.bkit/audit/`, git history에 보존돼 있다. **CLAUDE.md에 날짜별 누적 로그를 쌓지 말 것.**
- 과거 맥락이 필요하면 그때 해당 `docs/` 파일만 on-demand로 연다 (이 파일에 미리 복사해두지 않는다).
- "현재 상태"(섹션 5)는 갱신 시 **append가 아니라 덮어쓰기** — 오래된 항목은 지우고 최신만 유지한다.
- 버그·이슈는 재발 방지에 꼭 필요한 핵심만 짧게. 상세 재현/수정 내역은 해당 PDCA 문서·커밋에 둔다.
