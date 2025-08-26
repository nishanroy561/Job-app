import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { fetchJobs } from "../lib/api";
import Pagination from "../components/pagination";

const DEFAULT_PAGE_SIZE = 20;
const AUTO_REFRESH_MS = 60_000;

export default function Jobs() {
  const [params, setParams] = useSearchParams();
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const q = useMemo(() => ({
    title: params.get("title") || "",
    location: params.get("location") || "",
    source: params.get("source") || "",
    page: Math.max(1, parseInt(params.get("page") || "1", 10)),
    pageSize: Math.min(100, Math.max(5, parseInt(params.get("limit") || DEFAULT_PAGE_SIZE, 10))),
  }), [params]);

  const setParamsPatch = useCallback((patch) => {
    const next = new URLSearchParams(params);
    for (const k of ["title","location","source"]) {
      if (patch[k] !== undefined) { if (!patch[k]) next.delete(k); else next.set(k, patch[k]); }
    }
    if (patch.page !== undefined) next.set("page", String(patch.page));
    if (patch.pageSize !== undefined) next.set("limit", String(patch.pageSize));
    setParams(next, { replace: true });
  }, [params, setParams]);

  // Debounce filters
  const debounceRef = useRef(0);
  const setFilter = (patch) => {
    clearTimeout(debounceRef.current);
    debounceRef.current = window.setTimeout(() => {
      setParamsPatch({ ...patch, page: 1 });
    }, 250);
  };

  async function loadPage() {
    setLoading(true); setErr("");
    try {
      const offset = (q.page - 1) * q.pageSize;
      const res = await fetchJobs({ title: q.title, location: q.location, source: q.source, limit: q.pageSize, offset });
      setItems(res.items || []);
      setTotal(res.total || 0);
    } catch {
      setErr("Failed to load jobs");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadPage(); }, [q.title, q.location, q.source, q.page, q.pageSize]); // eslint-disable-line

  useEffect(() => {
    const id = setInterval(() => { loadPage(); }, AUTO_REFRESH_MS);
    return () => clearInterval(id);
  }, [q.title, q.location, q.source, q.page, q.pageSize]); // eslint-disable-line

  return (
    <>
      {/* Sticky Header */}
      <div className="header">
        <div className="header-inner">
          <div className="brand">CareerForge</div>
          <span className="badge">Live feed</span>
          <div className="badge">Total: {total}</div>
          <div className="row" style={{ marginLeft: "auto" }}>
            <select
              value={q.pageSize}
              onChange={(e)=> setParamsPatch({ pageSize: parseInt(e.target.value,10), page: 1 })}
            >
              {[10,20,30,50,100].map(s => <option key={s} value={s}>{s}/page</option>)}
            </select>
            <button className="button" onClick={loadPage}>Refresh</button>
          </div>
        </div>
      </div>

      <div className="container">
        {/* Filters */}
        <div className="row" style={{ marginBottom: 10, flexWrap: "wrap" }}>
          <input
            placeholder="Title e.g. Python"
            defaultValue={q.title}
            onChange={(e)=> setFilter({ title: e.target.value })}
            style={{ flex: 1, minWidth: 180 }}
          />
          <input
            placeholder="Location e.g. India"
            defaultValue={q.location}
            onChange={(e)=> setFilter({ location: e.target.value })}
            style={{ flex: 1, minWidth: 180 }}
          />
          <input
            placeholder="Source e.g. linkedin"
            defaultValue={q.source}
            onChange={(e)=> setFilter({ source: e.target.value })}
            style={{ width: 180 }}
          />
          <button className="button"
            onClick={()=> setParamsPatch({ title:"", location:"", source:"", page:1 })}
          >Clear</button>
        </div>

        {/* Status */}
        <div className="row" style={{ justifyContent: "space-between", marginBottom: 8 }}>
          <div className="muted">{loading ? "Loading…" : `Found ${total} jobs`}</div>
          {err && <div className="error">{err}</div>}
        </div>

        {/* Results */}
        {loading ? (
          <div className="grid">
            {Array.from({ length: Math.min(8, q.pageSize) }).map((_, i) => (
              <div key={i} className="skeleton">
                <div className="bar" style={{ width: "60%" }} />
                <div className="bar small" />
                <div className="bar small" style={{ width: "25%" }} />
              </div>
            ))}
          </div>
        ) : items.length === 0 ? (
          <div className="empty">No jobs match your filters.</div>
        ) : (
          <div className="grid">
            {items.map((job, i) => (
              <a key={`${job.source || "src"}:${job.id || job.url || i}`} className="card" href={job.url} target="_blank" rel="noreferrer">
                <h3>{job.title}</h3>
                <div className="meta">{job.company} • {job.location}</div>
                <div className="submeta">
                  <span className="pill">{job.source || "source"}</span>
                  {job.employment_type && <span className="pill ok">{job.employment_type}</span>}
                  {job.date_posted && <span className="pill">{job.date_posted}</span>}
                </div>
              </a>
            ))}
          </div>
        )}

        {/* Pagination */}
        <Pagination
          total={total}
          page={q.page}
          pageSize={q.pageSize}
          onPageChange={(p)=> setParamsPatch({ page: p })}
        />
      </div>
    </>
  );
}
