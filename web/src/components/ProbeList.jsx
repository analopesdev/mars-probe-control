export default function ProbeList({ probes, grids, selectedId, onSelect }) {
  return (
    <section className="card">
      <h2><span className="index">02</span> Frota</h2>

      {probes.length === 0 && <p className="muted">Nenhuma sonda lançada ainda.</p>}

      {probes.map((probe) => {
        const grid = grids[probe.id];
        return (
          <button
            key={probe.id}
            type="button"
            className={probe.id === selectedId ? "probe-row probe-row--selected" : "probe-row"}
            onClick={() => onSelect(probe.id)}
          >
            <span>
              <span className="mono">{probe.id.slice(0, 8)}</span>
              <span className="muted small">{grid ? ` · grid ${grid.maxX} × ${grid.maxY}` : ""}</span>
            </span>
            <span className="mono">
              ({probe.x}, {probe.y}, {probe.direction})
            </span>
          </button>
        );
      })}
    </section>
  );
}
