# cmds-bio — 구요한 Link-in-Bio

구요한 (Yohan Koo · 커맨드스페이스) 개인 **링크인바이오** 페이지.
litt.ly / Linktree 를 대체하는 self-hosted 한 페이지짜리 정적 사이트.

- **Live** — https://bio.cmdspace.work
- **Vercel** — 프로젝트 `cmds-bio` (scope: `johnfkoo951s-projects`)
- **스택** — 순수 `index.html` 1개 (인라인 CSS/JS, 빌드 없음) + `assets/` 로고·대표사진·갤러리

## Quick start

```bash
cd /Users/yohankoo/DEV/cmds-bio

# 1) 편집 — index.html 만 고치면 됨
#    (링크/소셜/바이오/색상 전부 이 파일 안에)
#    콘텐츠 변경 시 신선도 날짜 2곳 갱신: 게이트웨이 칩 + 푸터 <time id="pageUpdated">

# 2) (선택) SNS 팔로워 수 재수집 — assets/followers.json 갱신
bash scripts/refresh-followers.sh

# 3) 배포
vercel deploy --prod --yes --scope johnfkoo951s-projects
```

## SNS 집계 자동 갱신 (헤드리스 — omnicontrol 스케줄러용)

```bash
# 권장: 순수 셸 원샷 (수집 → JSON 갱신 → prod 배포)
cd /Users/yohankoo/DEV/cmds-bio && bash scripts/refresh-followers.sh --deploy

# LinkedIn 포함 (cmux 앱 실행 중 + LinkedIn 로그인 세션 필요)
cd /Users/yohankoo/DEV/cmds-bio && bash scripts/refresh-followers.sh --linkedin-cmux --deploy

# LinkedIn 수동 입력
bash scripts/refresh-followers.sh --linkedin 1234

# Claude 경유 (HTML 폴백 동기화·worklog 기록까지 위임)
cd /Users/yohankoo/DEV/cmds-bio && claude -p "/bio-sns-refresh" --dangerously-skip-permissions
```

- LinkedIn은 익명 수집이 차단(999/429)되어 수동 입력 또는 cmux 로그인 세션 경유만 가능.
- 실패한 플랫폼은 기존 값 유지 — 부분 실패에 안전. 상세 절차는 `.claude/skills/bio-sns-refresh/SKILL.md`.

## 연결 프로젝트 — cmdspace.work (`/Users/yohankoo/DEV/cmdspace-main`)

두 사이트는 프로필 직함·대표 수치·링크 자산을 공유하는 **연결 프로젝트**다.

| 공유 정보 | bio 위치 | cmdspace.work 위치 |
|---|---|---|
| 직함 (겸임교수·KIRD 객원교수) | index.html identity + docs/02-profile.md | index.html Operator 섹션 |
| 활동 450+ / 노트 10,000+ / LG 900명 | index.html 크레덴셜 리스트 | data/activities.csv(동적) + 정적 카피 |
| 링크 자산 | index.html + assets/bio-links.json | Ecosystem hub 카드 |
| Last updated 표기 | 게이트웨이 칩 + 푸터 `<time>` | footer (CSV 최신 레코드 날짜) |

**한쪽에서 위 정보를 바꾸면 반드시 다른 쪽도 확인·갱신할 것.** 이력 기록: 이 레포 `docs/06-worklog.md` ↔ cmdspace-main `README.md`의 연결 프로젝트 섹션.

## 폴더 구조

```
cmds-bio/
├── index.html          # 페이지 본체 (프로필·소셜·링크·툴바 전부)
├── assets/
│   ├── cmds-icon-black.png       # clean PNG 로고 (favicon/light)
│   ├── cmds-icon-white.png       # clean PNG 로고 (hero/dark)
│   ├── cmds-lockup-black.png     # CMDSPACE lockup
│   ├── cmds-lockup-white.png     # CMDSPACE lockup dark
│   ├── profile-yohan.jpg         # 대표사진 portrait
│   ├── profile-yohan-square.jpg  # 대표사진 square crop
│   ├── profile-yohan-headshot.jpg # 히어로용 얼굴 중심 crop
│   ├── gallery/                  # cmdspace.work 현장 갤러리 24장 WebP
│   ├── gallery.json              # 갤러리 원본 메타데이터
│   ├── bio-links.json            # 링크 허브 데이터 원본(JSON)
│   ├── followers.json            # SNS 팔로워 수 + asOf (페이지가 fetch, 스크립트로 갱신)
│   ├── obsidian-professional-note-cover.jpg # 출판 도서 표지
│   ├── cmds-logo-round.png       # 이전 원형 로고 보존
│   └── og-bio.png                # 1200×630 공유 카드 이미지
├── vercel.json         # cleanUrls 설정
├── .vercelignore       # docs·README·scripts·미참조 이미지 배포 제외
├── scripts/
│   └── refresh-followers.sh # SNS 팔로워 재수집 → followers.json 갱신
└── docs/               # 로컬 작업 문서 (공개 배포 안 됨)
    ├── 01-overview.md       # 구조·디자인 토큰
    ├── 02-profile.md        # 프로필·연락처·SNS (source of truth)
    ├── 03-content-guide.md  # 링크/소셜/바이오 편집법
    ├── 04-deployment.md     # 배포·도메인·DNS
    ├── 05-search-visibility.md # SEO·GEO·AEO 검색 노출성 체크
    └── 06-worklog.md        # 작업 로그 (감사 결과·변경 이력·후속 TODO)
```

## ⚠️ 개인정보 주의

`docs/` 폴더(내부 작업 문서·프로필 source of truth)는 비공개 정보를 포함할 수 있어 **git에서 제외**되어 있습니다.
- `.gitignore` 로 커밋 제외 (로컬 전용 — 2026-07-04 히스토리에서도 완전 제거), `.vercelignore` 로 배포 제외.
- 이 레포는 public입니다 — 새 민감정보는 반드시 `docs/` 안에만 두세요.

## 따라 만들기 (Fork 가이드)

이 레포는 litt.ly/Linktree를 대체하는 self-hosted 링크인바이오의 실제 운영 예시입니다. 포크 후:
1. `index.html`의 프로필·링크·색상 토큰(`:root` CSS 변수) 교체, `assets/` 이미지 교체
2. `scripts/refresh-followers.sh`의 SNS 핸들을 본인 계정으로 수정 → `assets/followers.json` 자동 갱신
3. Vercel(또는 아무 정적 호스팅)에 배포 — 빌드 없음, 파일 그대로

## 링크 허브 업데이트

- 웹 표시: `index.html` 의 “커맨드스페이스 게이트웨이” 섹션
- 프로젝트 데이터: `assets/bio-links.json`
- 메인 볼트 원본 노트: `/Users/yohankoo/Local Obsidian_MBP/CMDSPACE_Local_MBP/70. Outputs/71. Published/bio-cmdspace-work-link-hub.md`
- `cmdspace.work`와 `bio.cmdspace.work`는 같은 링크 자산을 공유하므로, 링크 변경 시 두 사이트를 같이 확인합니다.
