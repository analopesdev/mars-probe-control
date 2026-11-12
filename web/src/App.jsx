import { useEffect, useState } from "react";
import { launchProbe, listProbes, moveProbe } from "./api.js";
import { angleOf, rotationDelta } from "./directions.js";
import LaunchForm from "./components/LaunchForm.jsx";
import ProbeList from "./components/ProbeList.jsx";
import Plateau3D from "./components/Plateau3D.jsx";
import CommandPanel from "./components/CommandPanel.jsx";
import MissionLog from "./components/MissionLog.jsx";
import "./mars3d.css";

const GRIDS_KEY = "mars-probe-grids";

function gridFrom(probe, fallback) {
  if (probe.grid_max_x !== undefined) {
    return { maxX: probe.grid_max_x, maxY: probe.grid_max_y };
  }
  return fallback;
}

function loadSavedGrids() {
  try {
    return JSON.parse(localStorage.getItem(GRIDS_KEY)) ?? {};
  } catch {
    return {};
  }
}

function saveGrids(grids) {
  try {
    localStorage.setItem(GRIDS_KEY, JSON.stringify(grids));
  } catch {
  }
}

let nextLogId = 0;

export default function App() {
  const [probes, setProbes] = useState([]);
  const [grids, setGrids] = useState(loadSavedGrids);
  const [rotations, setRotations] = useState({});
  const [selectedId, setSelectedId] = useState(null);
  const [log, setLog] = useState([]);
  const [busy, setBusy] = useState(false);

  const selected = probes.find((probe) => probe.id === selectedId);
  const selectedGrid = selected ? gridFrom(selected, grids[selected.id]) : null;

  useEffect(() => {
    listProbes()
      .then((list) => {
        setProbes(list);
        setRotations(Object.fromEntries(list.map((p) => [p.id, angleOf(p.direction)])));
        if (list.length > 0) setSelectedId(list[0].id);
      })
      .catch((error) => addLog(`Não foi possível carregar as sondas: ${error.message}`, false));
  }, []);

  useEffect(() => saveGrids(grids), [grids]);

  function addLog(text, ok) {
    nextLogId += 1;
    setLog((current) => [{ id: nextLogId, text, ok }, ...current].slice(0, 8));
  }

  async function handleLaunch(maxX, maxY, direction) {
    setBusy(true);
    try {
      const probe = await launchProbe(maxX, maxY, direction);
      setProbes((current) => [...current, probe]);
      setGrids((current) => ({ ...current, [probe.id]: { maxX, maxY } }));
      setRotations((current) => ({ ...current, [probe.id]: angleOf(probe.direction) }));
      setSelectedId(probe.id);
      addLog(`Sonda ${probe.id.slice(0, 8)} lançada em (0, 0, ${probe.direction})`, true);
    } catch (error) {
      addLog(`Lançamento recusado: ${error.message}`, false);
    } finally {
      setBusy(false);
    }
  }

  async function handleSend(commands) {
    if (!selected) return;
    setBusy(true);
    try {
      const moved = await moveProbe(selected.id, commands);
      setRotations((current) => ({
        ...current,
        [moved.id]: (current[moved.id] ?? angleOf(selected.direction)) + rotationDelta(selected.direction, moved.direction),
      }));
      setProbes((current) => current.map((probe) => (probe.id === moved.id ? { ...probe, ...moved } : probe)));
      addLog(`${commands} → (${moved.x}, ${moved.y}, ${moved.direction})`, true);
    } catch (error) {
      addLog(`${commands} → ${error.message}`, false);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="page">
      <header className="header">
        <div>
          <h1>Mars Mission Control</h1>
          <p className="muted">
            {selected ? `Sonda ${selected.id.slice(0, 8)} · grid ${selectedGrid?.maxX ?? "?"} × ${selectedGrid?.maxY ?? "?"}` : "Nenhuma sonda em operação"}
          </p>
        </div>

        {selected && (
          <div className="telemetry">
            <div><span>X</span><strong>{selected.x}</strong></div>
            <div><span>Y</span><strong>{selected.y}</strong></div>
            <div><span>Direção</span><strong className="accent">{selected.direction}</strong></div>
          </div>
        )}
      </header>

      <div className="layout">
        <aside className="sidebar">
          <LaunchForm onLaunch={handleLaunch} />
          <ProbeList probes={probes} grids={grids} selectedId={selectedId} onSelect={setSelectedId} />
        </aside>

        <section className="content">
          <div className="card card--scene">
            {selected && selectedGrid ? (
              <Plateau3D probe={selected} grid={selectedGrid} rotation={rotations[selected.id] ?? 0} />
            ) : (
              <p className="muted empty">
                {selected
                  ? "Não sei o tamanho da grid desta sonda. Faça a API devolver grid_max_x e grid_max_y."
                  : "Nenhuma sonda selecionada."}
              </p>
            )}
          </div>

          <div className="row row--wrap">
            <CommandPanel onSend={handleSend} disabled={!selected || busy} />
            <MissionLog entries={log} />
          </div>
        </section>
      </div>
    </main>
  );
}
