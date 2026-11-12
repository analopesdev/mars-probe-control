import Rover from "./Rover.jsx";

const GAP = 4;
const LABEL_SPACE = 28;
const PADDING = 12;

function cellSizeFor(columns, rows) {
  return Math.max(28, Math.min(64, Math.floor(420 / Math.max(columns, rows))));
}

export default function Plateau3D({ probe, grid, rotation, tilt = 58, spin = -40 }) {
  const columns = grid.maxX + 1;
  const rows = grid.maxY + 1;
  const cell = cellSizeFor(columns, rows);
  const step = cell + GAP;

  const boardWidth = LABEL_SPACE + columns * step + PADDING;
  const boardHeight = PADDING + rows * step + LABEL_SPACE;

  const yValues = Array.from({ length: rows }, (_, i) => grid.maxY - i);
  const xValues = Array.from({ length: columns }, (_, i) => i);

  const centerX = LABEL_SPACE + probe.x * step + cell / 2;
  const centerY = PADDING + (grid.maxY - probe.y) * step + cell / 2;
  const roverScale = cell / 64;

  return (
    <div className="scene" role="img" aria-label={`Sonda em (${probe.x}, ${probe.y}) olhando para ${probe.direction}`}>
      <div
        className="board"
        style={{
          width: boardWidth,
          height: boardHeight,
          transform: `rotateX(${tilt}deg) rotateZ(${spin}deg)`,
        }}
      >
        <div className="board-side board-side--left" style={{ height: boardHeight }} />
        <div className="board-side board-side--front" style={{ width: boardWidth, top: boardHeight }} />

        <span className="compass" style={{ left: boardWidth / 2 - 6 }}>N</span>

        {yValues.map((y, row) => (
          <span key={`y${y}`} className="axis-label" style={{ left: 8, top: PADDING + row * step + cell / 2 - 8 }}>
            {y}
          </span>
        ))}
        {xValues.map((x) => (
          <span key={`x${x}`} className="axis-label" style={{ top: PADDING + rows * step + 4, left: LABEL_SPACE + x * step + cell / 2 - 4 }}>
            {x}
          </span>
        ))}

        <div
          className="cells"
          style={{
            left: LABEL_SPACE,
            top: PADDING,
            gridTemplateColumns: `repeat(${columns}, ${cell}px)`,
            gap: GAP,
          }}
        >
          {yValues.flatMap((y) =>
            xValues.map((x) => {
              const isHere = x === probe.x && y === probe.y;
              const shade = (x + y) % 2 === 0 ? "cell--dark" : "cell--light";
              return (
                <div
                  key={`${x},${y}`}
                  className={`cell ${shade} ${isHere ? "cell--current" : ""}`}
                  style={{ width: cell, height: cell }}
                />
              );
            }),
          )}
        </div>

        <div className="rover-shadow" style={{ left: centerX - 30 * roverScale, top: centerY - 30 * roverScale, width: 60 * roverScale, height: 60 * roverScale }} />

        <div
          className="rover"
          style={{
            left: centerX - 20,
            top: centerY - 24,
            transform: `translateZ(1px) rotateZ(${rotation}deg) scale(${roverScale})`,
          }}
        >
          <Rover />
        </div>
      </div>
    </div>
  );
}
