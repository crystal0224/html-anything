---
name: html-anything
description: "입력(마크다운/노트/CSV/JSON/표/원시 텍스트)을 디자인된 ship-ready 단일 HTML 결과물로 변환. 78개 디자인 시스템 템플릿(슬라이드 덱·포스터·매거진 아티클·이력서·데이터 리포트/대시보드·문서·소셜 카드(샤오훙수/트윗)·Hyperframes 영상 프레임)을 골라 적용한다. 발표 슬라이드, 포스터, 원페이지 문서, 리포트, SNS 카드, 랜딩/프로토타입 화면, 영상 프레임을 '바로 공유 가능한 한 개 HTML 파일'로 만들고 싶을 때 사용. 트리거: 'HTML로 만들어줘', 'html-anything', '단일 HTML', 'ship-ready HTML', '슬라이드 HTML', '포스터로', '매거진 스타일로', '데이터 리포트 HTML', '카드뉴스', '샤오훙수/트윗 카드', '대시보드 HTML', 'Hyperframes/영상 프레임', '이 마크다운 디자인해서 HTML로', 'turn this into HTML', 'design this as a deck/poster/report'. 출처: nexu-io/html-anything (Apache-2.0) 포크의 템플릿 추출 — Claude Code와 Codex 양쪽에서 동작."
---

# html-anything — Agentic single-file HTML generator

마크다운/노트/표/JSON 같은 **초안 입력**을 받아, 78개 디자인 시스템 중 하나를 골라 **독자가 바로 보는 ship-ready 단일 HTML 파일**로 변환한다. 핵심 명제: *마크다운은 작성자용 초안, HTML이 최종형.* 웹앱(GUI) 없이 CLI 세션에서 직접 생성한다.

## 언제 무엇을 만드나 (surface 선택)

사용자 의도 → surface 매핑:

| 사용자가 원하는 것 | category | 대표 템플릿 |
|---|---|---|
| 발표 슬라이드 / 키노트 덱 | `slides` (22개) | `deck-swiss-international`, `deck-guizang-editorial`, `deck-open-slide-canvas` |
| 웹/SaaS 랜딩·프로토타입 화면 | `prototype` (8개) | `saas-landing`, `pricing-page`, `web-proto-editorial` |
| 지표 대시보드 | `dashboard` (8개) | 카탈로그 참조 |
| 데이터 리포트 | `data` / `finance` | `data-report`, `finance-report` |
| 긴 글/원페이지 문서·리포트 | `doc` (8개) | `doc-kami-parchment`, `exec-briefing-memo` |
| 매거진 아티클·블로그 | `article` (3개) | `article-magazine`, `blog-post` |
| 포스터 (세로 긴 이미지) | `poster` (5개) | `magazine-poster` |
| 소셜 카드 (샤오훙수/트윗/Reddit/Spotify) | `card` (7개) | `deck-xhs-post`, `social-carousel` |
| 영상 프레임 (Hyperframes/Remotion → mp4) | `video` (8개) | `frame-glitch-title`, `frame-logo-outro`, `vfx-text-cursor` |
| 모바일 앱 화면 | `mobile` (3개) | `mobile-app`, `mobile-onboarding` |
| 이력서 | `resume` | `resume` |

전체 78개 목록 + 한 줄 설명은 **[references/catalog.md](references/catalog.md)** 에 있다. surface가 정해지면 거기서 구체 템플릿을 고른다.

## 워크플로우

1. **의도 파악 → surface 결정.** 사용자가 "포스터로", "덱으로" 등 명시하면 그대로. 모호하면 위 표로 1차 좁히고, 후보가 여러 개면 카탈로그의 `★`(업스트림 추천) 우선 1~2개를 제시하고 사용자가 고르게 한다 (a/b/c).
2. **카탈로그에서 템플릿 선택.** `references/catalog.md`를 읽고 `scenario`(design/marketing/engineering/product/personal)와 톤으로 매칭.
3. **선택한 템플릿의 원본을 읽는다 (필수, 둘 다):**
   - `references/skills/<name>/SKILL.md` — 레이아웃 명세 + 하드 디자인 제약 (이게 프롬프트의 핵심)
   - `references/skills/<name>/example.html` — 실제 레퍼런스 출력. 구조·CSS 패턴을 그대로 따른다.
4. **사용자 실제 콘텐츠로 새 HTML 생성.** example.html의 **레이아웃·디자인 시스템은 유지**하되 내용만 사용자 데이터로 교체. 언어는 사용자 언어(한국어)로. 절대 placeholder/lorem/가짜 수치 금지 — 데이터가 부족하면 사용자에게 요청.
5. **단일 파일로 저장.** `<name>-<슬러그>.html` 형태. 작업 폴더 또는 사용자가 지정한 경로.
6. **시각 검증.** 생성 후 브라우저로 열어 확인 제안 (`open <file>` 또는 chromux/browser-harness). Crystal 부정사전(조잡/헐빈/딱딱/식상/오밀조밀) 자가 점검.

## 하드 제약 (모든 출력 공통 — 업스트림 anti-AI-slop 규율)

- **단일 파일**: CSS 인라인. 외부는 CDN만 허용 (Tailwind CDN, Google Fonts). 빌드 스텝 없이 더블클릭으로 열려야 함.
- **CJK-first 폰트 스택**: 한국어/중국어 콘텐츠면 CJK 폰트를 우선 지정 (예: Pretendard, Noto Sans KR을 앞에).
- **8px 베이스라인 그리드**: spacing·line-height를 8의 배수로.
- **명암비 ≥ 4.5** (WCAG AA). 본문 가독성 우선.
- **실데이터 강제**: 차트·표·인용은 사용자가 준 실제 값만. 모르면 비워두고 묻는다.
- **템플릿의 잠긴 레이아웃을 존중**: 각 SKILL.md가 "10 locked layouts" 식으로 버라이언트를 못박아 둠 — 임의 변형 말 것.

## 내보내기 (export) 옵션 안내

CLI에서는 `.html` 파일이 곧 결과물. 추가로 사용자에게 안내 가능:
- **WeChat/Zhihu 붙여넣기**: CSS를 juice로 인라인하면 재서식 없이 붙음 (업스트림 웹앱 기능 — 필요시 레포의 `next/` 앱 사용).
- **PNG 이미지** (트윗/샤오훙수): 브라우저에서 2× 스크린샷, 또는 chromux/browser-harness로 `screenshot`.
- **PDF** (덱): Chrome headless `--print-to-pdf` 또는 `regen-pdf` 스킬.
- **영상** (`video` 프레임): heygen-com/hyperframes 또는 Remotion에 넘겨 `.mp4` 렌더.

## 업스트림 동기화

템플릿 출처 = 포크 `~/html-anything` 의 `next/src/lib/templates/skills/`. 업스트림에서 새 템플릿을 받은 뒤:

```bash
cp -R ~/html-anything/next/src/lib/templates/skills/* ~/.claude/skills/html-anything/references/skills/
python3 ~/.claude/skills/html-anything/scripts/build_catalog.py   # catalog.md 재생성
```

Codex는 `~/.codex/skills/html-anything` → 이 디렉토리 심볼릭 링크이므로 자동 반영.
