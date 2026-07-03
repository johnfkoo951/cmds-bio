#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Refresh Bio Followers
# @raycast.mode fullOutput
# @raycast.packageName CMDSPACE
# @raycast.icon 📊
# @raycast.description bio.cmdspace.work의 SNS 팔로워 수를 재수집해 assets/followers.json 갱신

# cmds-bio SNS 팔로워/구독자 수 갱신 스크립트
# 사용법: bash scripts/refresh-followers.sh   (이후 vercel deploy --prod 로 배포)
#
# 수집 경로 (모두 서버사이드 curl — 브라우저에서는 CORS/로그인월로 불가):
#   YouTube    : 채널 /about 페이지의 ytInitialData 내 subscriberCountText (플랫폼이 12.6K처럼 반올림)
#   X          : api.fxtwitter.com (비공식 프록시, 정확값)
#   Threads    : facebookexternalhit UA로 meta description의 "N Followers" (반올림)
#   Instagram  : web_profile_info 내부 API + x-ig-app-id 헤더 (정확값, 변경 취약)
#   GitHub     : 공식 REST API (정확값)
#   LinkedIn   : 공개 API 없음 — 기존 값 유지 (수동 관리)
#
# 실패한 플랫폼은 기존 값을 유지하므로 부분 실패에 안전.

set -uo pipefail
cd "$(dirname "$0")/.."

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
JSON="assets/followers.json"

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

YT=$(fetch_youtube)   || YT=""
XF=$(fetch_x)         || XF=""
TH=$(fetch_threads)   || TH=""
IG=$(fetch_instagram) || IG=""
GH=$(fetch_github)    || GH=""

python3 - "$JSON" "$YT" "$XF" "$TH" "$IG" "$GH" <<'PY'
import json, re, sys
from datetime import date

path, yt, xf, th, ig, gh = sys.argv[1:7]
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

updates = {"youtube": yt, "x": xf, "threads": th, "instagram": ig, "github": gh}
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
print(f"   합계: {total:,} (LinkedIn 제외)")
print("   변경:", "; ".join(changed) if changed else "없음")
print("   ⚠️  index.html에 구운 폴백 숫자·aria-label·YouTube 카드 문구는 수동 확인 권장")
PY

echo ""
echo "다음 단계: vercel deploy --prod --yes --scope johnfkoo951s-projects"
