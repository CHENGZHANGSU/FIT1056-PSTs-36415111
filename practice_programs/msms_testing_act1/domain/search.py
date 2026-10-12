import unicodedata

def _norm(s):
    return unicodedata.normalize("NFKD", s).casefold()

def search_course(query, *, level = None, instrument = None, active_only = True, repo = None):
    q = _norm(query or "")
    items = repo.list_courses()
    results = []

    for c in items:
        if active_only and not c['active']:
            continue
        hay = _norm(c['title'] + " " + c.get("description", ""))
        if q and q not in hay:
            continue
        if level and c['level'] != level:
            continue
        if instrument and c['instrument'] != instrument:
            continue
        results.append(c)
    return sorted(results, key = lambda x:(x['title'].lower(), x['level']))