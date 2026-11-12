import { useState } from "react";

export default function CommandPanel({ onSend, disabled }) {
  const [sequence, setSequence] = useState("");

  function send(commands) {
    const cleaned = commands.trim().toUpperCase();
    if (!cleaned) return;
    onSend(cleaned);
    setSequence("");
  }

  function handleSubmit(event) {
    event.preventDefault();
    send(sequence);
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2><span className="index">03</span> Comandos</h2>

      <div className="row row--end">
        <label className="grow">
          Sequência (M, L, R)
          <input
            className="mono sequence"
            value={sequence}
            onChange={(e) => setSequence(e.target.value)}
            placeholder="MRM"
          />
        </label>
        <button type="submit" className="primary" disabled={disabled}>Enviar</button>
      </div>

      <div className="row">
        <button type="button" className="key" aria-label="Girar à esquerda" onClick={() => send("L")} disabled={disabled}>L</button>
        <button type="button" className="key" aria-label="Mover para frente" onClick={() => send("M")} disabled={disabled}>M</button>
        <button type="button" className="key" aria-label="Girar à direita" onClick={() => send("R")} disabled={disabled}>R</button>
      </div>
    </form>
  );
}
