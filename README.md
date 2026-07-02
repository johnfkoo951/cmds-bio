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

# 2) 배포
vercel deploy --prod --yes --scope johnfkoo951s-projects
```

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
│   ├── obsidian-professional-note-cover.jpg # 출판 도서 표지
│   ├── cmds-logo-round.png       # 이전 원형 로고 보존
│   └── og-bio.png                # 1200×630 공유 카드 이미지
├── vercel.json         # cleanUrls 설정
├── .vercelignore       # docs·README 는 배포 제외 (개인정보 보호)
└── docs/               # 로컬 작업 문서 (공개 배포 안 됨)
    ├── 01-overview.md       # 구조·디자인 토큰
    ├── 02-profile.md        # 프로필·연락처·SNS (source of truth)
    ├── 03-content-guide.md  # 링크/소셜/바이오 편집법
    ├── 04-deployment.md     # 배포·도메인·DNS
    └── 05-search-visibility.md # SEO·GEO·AEO 검색 노출성 체크
```

## ⚠️ 개인정보 주의

`docs/02-profile.md` 에는 **모바일 번호·카톡 참여코드** 등 비공개 정보가 들어 있습니다.
- `.vercelignore` 로 배포에서 제외되어 `bio.cmdspace.work/docs/*` 로 공개되지 않습니다.
- 이 폴더를 GitHub 에 push 한다면 **private 레포**로 하거나 `docs/` 를 `.gitignore` 하세요.

## 링크 허브 업데이트

- 웹 표시: `index.html` 의 “커맨드스페이스 게이트웨이” 섹션
- 프로젝트 데이터: `assets/bio-links.json`
- 메인 볼트 원본 노트: `/Users/yohankoo/Local Obsidian_MBP/CMDSPACE_Local_MBP/70. Outputs/71. Published/bio-cmdspace-work-link-hub.md`
- `cmdspace.work`와 `bio.cmdspace.work`는 같은 링크 자산을 공유하므로, 링크 변경 시 두 사이트를 같이 확인합니다.
