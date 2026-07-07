#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Refresh Bio Followers
# @raycast.mode fullOutput
# @raycast.packageName CMDSPACE
# @raycast.icon 📊
# @raycast.description bio.cmdspace.work의 SNS 팔로워 수를 재수집해 assets/followers.json 갱신

# cmds-bio SNS 팔로워/구독자 수 갱신 스크립트 (헤드리스 실행 가능 — omnicontrol 스케줄러 대응)
#
# 사용법:
#   bash scripts/refresh-followers.sh                  # 5개 플랫폼 재수집 (LinkedIn 기존값 유지)
#   bash scripts/refresh-followers.sh --linkedin 1234  # LinkedIn 팔로워 수동 입력
#   bash scripts/refresh-followers.sh --linkedin-cmux  # cmux 브라우저(로그인 세션)로 LinkedIn 시도
#   bash scripts/refresh-followers.sh --deploy         # 갱신 후 vercel prod 배포까지 원샷
#   플래그 조합 가능: --linkedin-cmux --deploy
#
# 수집 경로 (모두 서버사이드 — 브라우저 클라이언트에서는 CORS/로그인월로 불가):
#   YouTube    : 채널 /about 페이지의 ytInitialData 내 subscriberCountText (플랫폼이 12.6K처럼 반올림)
#   X          : api.fxtwitter.com (비공식 프록시, 정확값)
#   Threads    : facebookexternalhit UA로 meta description의 "N Followers" (반올림)
#   Instagram  : web_profile_info 내부 API + x-ig-app-id 헤더 (정확값, 변경 취약)
#   GitHub     : 공식 REST API (정확값)
#   LinkedIn   : 익명 수집 불가(999/429 봇차단) — 수동(--linkedin N) 또는 cmux 로그인 세션(--linkedin-cmux)
#
# 실패한 플랫폼은 기존 값을 유지하므로 부분 실패에 안전.

set -uo pipefail
cd "$(dirname "$0")/.."

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
JSON="assets/followers.json"
LINKEDIN_URL="https://www.linkedin.com/in/yohan-koo-a1baa3138/"

LINKEDIN_MANUAL=""
USE_CMUX=false
DO_DEPLOY=false
while [ $# -gt 0 ]; do
    case "$1" in
        --linkedin) LINKEDIN_MANUAL="${2:-}"; shift 2 ;;
        --linkedin-cmux) USE_CMUX=true; shift ;;
        --deploy) DO_DEPLOY=true; shift ;;
        *) echo "알 수 없는 옵션: $1"; exit 1 ;;
    esac
done

fetch_youtube() {
    curl -s --max-time 20 -A "$UA" "https://www.youtube.com/@cmdspace/about" \
        | grep -o '"subscriberCountText":{"simpleText":"[^"]*"' \
        | head -1 | sed 's/.*"simpleText":"//; s/"$//; s/ subscribers//'
}

fetch_x() {
    curl -s --max-time 20 "https://api.fxtwitter.com/YohanKoo" \
        | python3 -c "import json,sys; print(json.load(sys.stdin)['user']['followers'])" 2>/dev/null
}

fetch_threads() {
    curl -s --max-time 20 -A "facebookexternalhit/1.1" "https://www.threads.com/@cmds_pace" \
        | grep -o 'content="[^"]*Followers' | head -1 \
        | sed 's/content="//; s/ Followers//'
}

fetch_instagram() {
    curl -s --max-time 20 -A "$UA" \
        -H "x-ig-app-id: 936619743392459" \
        "https://www.instagram.com/api/v1/users/web_profile_info/?username=cmds_pace" \
        | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['user']['edge_followed_by']['count'])" 2>/dev/null
}

fetch_github() {
    curl -s --max-time 20 "https://api.github.com/users/johnfkoo951" \
        | python3 -c "import json,sys; print(json.load(sys.stdin)['followers'])" 2>/dev/null
}

# cmux 네이티브 브라우저(WKWebView, 로그인 세션 공유)로 LinkedIn 팔로워 수집.
# cmux 앱이 실행 중이고 LinkedIn에 로그인된 세션이 있어야 성공. 실패 시 빈 문자열.
fetch_linkedin_cmux() {
    command -v cmux >/dev/null 2>&1 || return 0
    local out surface val
    out=$(cmux browser open "$LINKEDIN_URL" 2>/dev/null) || return 0
    surface=$(printf '%s' "$out" | grep -o 'surface=surface:[0-9]*' | cut -d= -f2)
    [ -n "$surface" ] || return 0
    sleep 7
    val=$(cmux browser --surface "$surface" eval \
        '(document.body.innerText.match(/([\d,.]+K?)\s*(followers|팔로워)/i)||[])[1]||""' 2>/dev/null | tr -d '" ')
    printf '%s' "$val"
}

YT=$(fetch_youtube)   || YT=""
XF=$(fetch_x)         || XF=""
TH=$(fetch_threads)   || TH=""
IG=$(fetch_instagram) || IG=""
GH=$(fetch_github)    || GH=""

LI="$LINKEDIN_MANUAL"
if [ -z "$LI" ] && [ "$USE_CMUX" = true ]; then
    LI=$(fetch_linkedin_cmux)
    [ -n "$LI" ] && echo "LinkedIn (cmux): $LI" || echo "LinkedIn (cmux): 실패 — 로그인 세션 확인 필요, 기존 값 유지"
fi

python3 - "$JSON" "$YT" "$XF" "$TH" "$IG" "$GH" "$LI" <<'PY'
import json, re, sys
from datetime import date

path, yt, xf, th, ig, gh, li = sys.argv[1:8]
data = json.load(open(path))

def parse_display(raw):
    """'12.6K' → (12600, '12.6K', approx=True) / '427' → (427, '427', False)"""
    raw = raw.strip().replace(",", "")
    if not raw:
        return None
    m = re.match(r"^([\d.]+)([KM]?)$", raw, re.I)
    if not m:
        return None
    num, suffix = float(m.group(1)), m.group(2).upper()
    if suffix == "K":
        return int(num * 1_000), raw if raw.upper().endswith("K") else f"{raw}K", True
    if suffix == "M":
        return int(num * 1_000_000), raw, True
    return int(num), f"{int(num):,}" if num >= 1000 else str(int(num)), False

updates = {"youtube": yt, "x": xf, "threads": th, "instagram": ig, "github": gh, "linkedin": li}
changed = []
for p in data["platforms"]:
    raw = updates.get(p["id"], "")
    parsed = parse_display(raw) if raw else None
    if parsed:
        old = p["count"]
        p["count"], p["display"], p["approx"] = parsed
        if old != p["count"]:
            changed.append(f"{p['label']}: {old} → {p['count']}")

data["asOf"] = date.today().isoformat()
json.dump(data, open(path, "w"), ensure_ascii=False, indent=2)
open(path, "a").write("\n")

total = sum(p["count"] for p in data["platforms"] if isinstance(p["count"], int))
print(f"✅ {path} 갱신 완료 (asOf {data['asOf']})")
print(f"   합계: {total:,}")
print("   변경:", "; ".join(changed) if changed else "없음")
PY

# ── index.html 정적 폴백 동기화 (no-JS/fetch 실패 시 노출되는 값) ──
# followers.json 을 진리 소스로: .social-count 폴백 숫자, aria-label/data-label 끝자리 수치,
# snsCaption 기준일(data-ko/data-en/텍스트)을 함께 치환해 이중 소스 드리프트를 막는다.
python3 - "$JSON" index.html <<'PY'
import json, re, sys

json_path, html_path = sys.argv[1:3]
data = json.load(open(json_path))
html = open(html_path, encoding="utf-8").read()
orig = html

for p in data["platforms"]:
    pid, disp = p["id"], p.get("display") or ""
    if not disp:
        continue
    # .social-count 폴백 텍스트
    html = re.sub(
        r'(data-sns="' + re.escape(pid) + r'"[^>]*>)[^<]*(</span>)',
        lambda m: m.group(1) + disp + m.group(2), html)
    # 해당 소셜 <a> 태그의 aria-label / data-label-ko / data-label-en 끝자리 수치
    def fix_anchor(m):
        tag = m.group(0)
        tag = re.sub(r'(aria-label="[^"]*?)[\d.,]+K?(")', r'\g<1>' + disp + r'\g<2>', tag)
        tag = re.sub(r'(data-label-ko="[^"]*?)[\d.,]+K?(")', r'\g<1>' + disp + r'\g<2>', tag)
        tag = re.sub(r'(data-label-en="[^"]*?)[\d.,]+K?(\s+(?:followers|subscribers)")', r'\g<1>' + disp + r'\g<2>', tag)
        return tag
    html = re.sub(r'<a class="social"[^>]*>(?=(?:(?!</a>).)*data-sns="' + re.escape(pid) + '")',
                  fix_anchor, html, flags=re.S)

# snsCaption 기준일 (data-ko · data-en · 폴백 텍스트)
as_of = data["asOf"]
html = re.sub(r'(SNS 팔로워·구독자 합계 · )\d{4}-\d{2}-\d{2}( 기준)', r'\g<1>' + as_of + r'\g<2>', html)
html = re.sub(r'(Combined followers &amp; subscribers · as of )\d{4}-\d{2}-\d{2}', r'\g<1>' + as_of, html)

if html != orig:
    open(html_path, "w", encoding="utf-8").write(html)
    print("✅ index.html 정적 폴백 동기화 완료 (social-count · aria-label · snsCaption)")
else:
    print("ℹ️  index.html 폴백은 이미 최신")
print("   ⚠️  YouTube 카드 문구('구독자 12.6K')와 게이트웨이 칩·푸터 날짜는 콘텐츠 변경 시 수동 갱신")
PY

if [ "$DO_DEPLOY" = true ]; then
    echo ""
    echo "🚀 프로덕션 배포 중..."
    vercel deploy --prod --yes --scope johnfkoo951s-projects
else
    echo ""
    echo "다음 단계: vercel deploy --prod --yes --scope johnfkoo951s-projects  (또는 --deploy 플래그)"
fi
