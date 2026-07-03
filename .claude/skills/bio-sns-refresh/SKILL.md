---
name: bio-sns-refresh
description: bio.cmdspace.work의 SNS 팔로워·구독자 수를 재수집해 followers.json을 갱신하고 프로덕션 배포까지 수행. 사용자가 "SNS 집계 업데이트", "팔로워 수 갱신", "bio 팔로워 리프레시", "/bio-sns-refresh"를 요청하거나 omnicontrol 스케줄러가 헤드리스로 호출할 때 사용.
---

# bio-sns-refresh

bio.cmdspace.work (레포 `/Users/yohankoo/DEV/cmds-bio`)의 SNS 팔로워 집계를 갱신하는 스킬.

## 헤드리스 호출 (omnicontrol 스케줄러용)

```bash
# 권장 — Claude 불필요, 순수 셸 (가장 싸고 빠름)
cd /Users/yohankoo/DEV/cmds-bio && bash scripts/refresh-followers.sh --deploy

# LinkedIn 포함 (cmux 앱 실행 중 + LinkedIn 로그인 세션 필요)
cd /Users/yohankoo/DEV/cmds-bio && bash scripts/refresh-followers.sh --linkedin-cmux --deploy

# Claude 경유 (검증·문서 갱신까지 맡기고 싶을 때)
cd /Users/yohankoo/DEV/cmds-bio && claude -p "/bio-sns-refresh" --dangerously-skip-permissions
```

## 절차 (Claude가 실행할 때)

1. `bash scripts/refresh-followers.sh` 실행 (cmux CLI가 있고 cmux 앱이 실행 중이면 `--linkedin-cmux` 추가).
2. 출력의 "변경" 라인 확인:
   - 변경 없음 → 배포 불필요, 종료 보고.
   - 변경 있음 → 3단계로.
3. 큰 변동(플랫폼별 ±20% 이상 또는 합계 천 단위 변화) 시 `index.html`의 구운 폴백도 동기화:
   - `#snsTotal` 정적 텍스트 (예: `16,000+`)
   - 각 `.social-count` 정적 텍스트와 소셜 앵커의 `aria-label`/`data-label-ko`/`data-label-en`
   - YouTube 링크 카드 설명의 "구독자 N" (`data-desc-ko/en` + `.link-sub`)
   - `#snsCaption`의 기준일 (data-ko/data-en 포함)
4. `git add -A && git commit` (메시지: "SNS 집계 갱신 YYYY-MM-DD") 후
   `vercel deploy --prod --yes --scope johnfkoo951s-projects`.
5. 라이브 검증: `curl -s https://bio.cmdspace.work/assets/followers.json | python3 -m json.tool | head`.
6. 변동 내역을 `docs/06-worklog.md`에 한 줄 추가.

## LinkedIn 주의

- 익명 수집 불가 (999/429 봇차단). 두 가지 경로만 유효:
  - `--linkedin N` 수동 입력
  - `--linkedin-cmux` — cmux 네이티브 브라우저의 로그인 세션 이용 (세션 없으면 조용히 기존 값 유지)
- 실패해도 스크립트는 안전하게 기존 값을 유지한다. 실패 시 사용자에게 "cmux에서 LinkedIn 로그인 후 재실행"을 안내.

## 관련 파일

- 데이터: `assets/followers.json` (asOf 포함 — 페이지가 same-origin fetch)
- 스크립트: `scripts/refresh-followers.sh`
- 기록: `docs/06-worklog.md` · 연결 프로젝트: `/Users/yohankoo/DEV/cmdspace-main` (cmdspace.work)
