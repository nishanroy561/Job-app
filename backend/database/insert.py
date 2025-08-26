from database.db import jobs_collection
from websites.internships import fetch_internships
from websites.linkdin import fetch_linkedin
from api import JOB_KEY  # keep your key here

def _pick(*vals, default=None):
    for v in vals:
        if v is None: 
            continue
        if isinstance(v, str) and not v.strip():
            continue
        if isinstance(v, (list, dict)) and len(v) == 0:
            continue
        return v
    return default

def _as_list(payload, keys=("jobs", "data", "results", "items")):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in keys:
            v = payload.get(k)
            if isinstance(v, list):
                return v
        return [payload]  # single object fallback
    return []

def _coalesce_location(raw):
    loc = raw.get("location")
    if loc:
        return loc
    derived = raw.get("locations_derived")
    if isinstance(derived, list) and derived:
        return ", ".join(derived)
    # last resort: try city/region/country style fields
    city = _pick(raw.get("city"), raw.get("addressLocality"))
    region = _pick(raw.get("region"), raw.get("addressRegion"))
    country = _pick(raw.get("country"), raw.get("addressCountry"))
    parts = [p for p in (city, region, country) if p]
    return ", ".join(parts) if parts else "Remote/Unknown"

def normalize_job(raw: dict, source: str):
    # ids vary by API
    jid = _pick(raw.get("id"), raw.get("job_id"), raw.get("jobId"), raw.get("jobid"))
    title = _pick(raw.get("title"), raw.get("job_title"), raw.get("position"), default="N/A")
    company = _pick(raw.get("organization"), raw.get("company"), raw.get("employer_name"), raw.get("company_name"), default="N/A")
    et = raw.get("employment_type")
    if isinstance(et, list):
        et = et[0] if et else None
    url = _pick(raw.get("url"), raw.get("job_url"), raw.get("apply_link"), raw.get("link"), default="#")
    date_posted = _pick(raw.get("date_posted"), raw.get("job_posted_at_datetime_utc"), raw.get("posted_at"))
    logo = _pick(raw.get("organization_logo"), raw.get("company_logo"))

    return {
        "source_id": f"{source}:{jid}" if jid else None,  # unique across sources
        "id": jid,
        "title": title,
        "company": company,
        "location": _coalesce_location(raw),
        "employment_type": et,
        "url": url,
        "date_posted": date_posted,
        "source": source,
        "logo": logo,
        "raw": raw,
    }

def store_jobs():
    # ensure unique index once (safe to call multiple times)
    try:
        jobs_collection.create_index("source_id", unique=True)
    except Exception:
        pass

    print("🔄 Fetching jobs from APIs...")

    # Internships API (often returns a LIST)
    try:
        internships_payload = fetch_internships(JOB_KEY)
        internships = _as_list(internships_payload)
        c = 0
        for r in internships:
            doc = normalize_job(r, "internships")
            if not doc["source_id"]:
                continue
            jobs_collection.update_one({"source_id": doc["source_id"]}, {"$set": doc}, upsert=True)
            c += 1
        print(f"✅ Stored {c} internships")
    except Exception as e:
        print("⚠️ Internship fetch failed:", e)

    # LinkedIn API (sometimes LIST, sometimes { jobs: [...] })
    try:
        linkedin_payload = fetch_linkedin(JOB_KEY)
        linkedin_jobs = _as_list(linkedin_payload)
        c = 0
        for r in linkedin_jobs:
            doc = normalize_job(r, "linkedin")
            if not doc["source_id"]:
                continue
            jobs_collection.update_one({"source_id": doc["source_id"]}, {"$set": doc}, upsert=True)
            c += 1
        print(f"✅ Stored {c} LinkedIn jobs")
    except Exception as e:
        print("⚠️ LinkedIn fetch failed:", e)

    print("🎉 Job sync completed!")

if __name__ == "__main__":
    store_jobs()
