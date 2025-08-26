import sys
from database.db import jobs_collection
from collections import defaultdict
from urllib.parse import urlparse

def url_key(u: str) -> str:
    """Normalize URL to host+path (ignore query params, case-insensitive)."""
    if not u or u == "#":
        return ""
    try:
        p = urlparse(u)
        return (p.netloc.lower() + p.path.rstrip("/"))
    except Exception:
        return u.lower().strip()

def find_url_duplicates(min_group_size=2):
    groups = defaultdict(list)
    for job in jobs_collection.find({}, {"_id": 1, "url": 1, "title": 1, "company": 1, "source": 1}):
        key = url_key(job.get("url"))
        if key:
            groups[key].append(job)
    # return only groups with duplicates
    return [(k, v) for k, v in groups.items() if len(v) >= min_group_size]

def delete_url_duplicates(dup_groups):
    deleted_total = 0
    for key, docs in dup_groups:
        # keep the first doc, delete others
        keep_id = docs[0]["_id"]
        dup_ids = [d["_id"] for d in docs[1:]]
        if dup_ids:
            res = jobs_collection.delete_many({"_id": {"$in": dup_ids}})
            print(f"🔴 Deleted {res.deleted_count} duplicates for URL={key} (kept {keep_id})")
            deleted_total += res.deleted_count
    print(f"\n✅ Total deleted: {deleted_total}")

if __name__ == "__main__":
    dup_groups = find_url_duplicates()
    print(f"Found {len(dup_groups)} duplicate URL groups")

    if len(sys.argv) > 1 and sys.argv[1] == "--delete":
        delete_url_duplicates(dup_groups)
    else:
        # just preview duplicates
        for i, (key, docs) in enumerate(dup_groups, 1):
            print(f"\n[{i}] {key} (count={len(docs)})")
            for d in docs:
                print(f"  - {d.get('title')} @ {d.get('company')} [{d.get('source')}] _id={d['_id']}")
        print("\nℹ️ Run with `python debug.py --delete` to actually remove duplicates")
