export default function Pagination({ total, page, pageSize, onPageChange }) {
  const totalPages = Math.max(1, Math.ceil((total || 0) / pageSize));
  const btn = (p, label = p, disabled = false, active = false) => (
    <button
      key={`${label}`}
      className={`page-btn ${active ? "active" : ""}`}
      onClick={() => onPageChange(p)}
      disabled={disabled || active}
    >
      {label}
    </button>
  );

  const pages = [];
  const start = Math.max(1, page - 2);
  const end = Math.min(totalPages, start + 4);

  pages.push(btn(page - 1, "Prev", page <= 1));
  if (start > 1) { pages.push(btn(1)); if (start > 2) pages.push(<span key="pre">…</span>); }
  for (let p = start; p <= end; p++) pages.push(btn(p, p, false, p === page));
  if (end < totalPages) { if (end < totalPages - 1) pages.push(<span key="post">…</span>); pages.push(btn(totalPages)); }
  pages.push(btn(page + 1, "Next", page >= totalPages));

  return <div className="pagination">{pages}</div>;
}
