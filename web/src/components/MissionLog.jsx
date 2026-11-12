export default function MissionLog({ entries }) {
  return (
    <section className="card card--dark">
      <h2><span className="index">04</span> Registro</h2>

      {entries.length === 0 && <p className="muted">Os comandos enviados aparecem aqui.</p>}

      <ul className="log">
        {entries.map((entry) => (
          <li key={entry.id} className={entry.ok ? "log--ok" : "log--error"}>
            {entry.text}
          </li>
        ))}
      </ul>
    </section>
  );
}
