import { useState } from "react";
import { DIRECTIONS } from "../directions.js";

export default function LaunchForm({ onLaunch }) {
  const [maxX, setMaxX] = useState(5);
  const [maxY, setMaxY] = useState(5);
  const [direction, setDirection] = useState("NORTH");

  function handleSubmit(event) {
    event.preventDefault();
    onLaunch(Number(maxX), Number(maxY), direction);
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2><span className="index">01</span> Lançamento</h2>

      <div className="row">
        <label>
          Grid máx. X
          <input type="number" min="1" value={maxX} onChange={(e) => setMaxX(e.target.value)} />
        </label>
        <label>
          Grid máx. Y
          <input type="number" min="1" value={maxY} onChange={(e) => setMaxY(e.target.value)} />
        </label>
      </div>

      <fieldset className="directions">
        <legend>Direção inicial</legend>
        {DIRECTIONS.map((option) => (
          <button
            key={option}
            type="button"
            className={option === direction ? "chip chip--active" : "chip"}
            onClick={() => setDirection(option)}
          >
            {option}
          </button>
        ))}
      </fieldset>

      <p className="muted small">A sonda sempre pousa em (0, 0).</p>
      <button type="submit" className="primary">Lançar sonda</button>
    </form>
  );
}
