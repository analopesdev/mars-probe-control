// Uma caixa 3D feita com divs: quatro laterais e o topo, montadas com rotateX e rotateY.
function Box({ left, top, width, depth, base, height, topColor, frontColor, sideColor }) {
  const face = { position: "absolute", boxSizing: "border-box" };

  return (
    <div
      style={{
        position: "absolute",
        left,
        top,
        width,
        height: depth,
        transformStyle: "preserve-3d",
        transform: `translateZ(${base}px)`,
      }}
    >
      <div style={{ ...face, left: 0, top: 0, width, height, transformOrigin: "top center", transform: "rotateX(90deg)", background: frontColor }} />
      <div style={{ ...face, left: 0, top: depth, width, height, transformOrigin: "top center", transform: "rotateX(90deg)", background: frontColor }} />
      <div style={{ ...face, left: 0, top: 0, width: height, height: depth, transformOrigin: "left center", transform: "rotateY(-90deg)", background: sideColor }} />
      <div style={{ ...face, left: width, top: 0, width: height, height: depth, transformOrigin: "left center", transform: "rotateY(-90deg)", background: sideColor }} />
      <div style={{ ...face, left: 0, top: 0, width, height: depth, transform: `translateZ(${height}px)`, background: topColor, borderRadius: 2 }} />
    </div>
  );
}

const WHEEL = { topColor: "#3a3a3a", frontColor: "#1f1f1f", sideColor: "#2a2a2a" };

// O rover tem 40 × 48 px e a frente (a câmera laranja) aponta para cima quando o ângulo é 0°.
export default function Rover({ accent = "#f97316" }) {
  return (
    <>
      <Box left={-6} top={4} width={10} depth={13} base={0} height={12} {...WHEEL} />
      <Box left={36} top={4} width={10} depth={13} base={0} height={12} {...WHEEL} />
      <Box left={-6} top={31} width={10} depth={13} base={0} height={12} {...WHEEL} />
      <Box left={36} top={31} width={10} depth={13} base={0} height={12} {...WHEEL} />

      <Box left={2} top={6} width={36} depth={38} base={7} height={14} topColor="#e7e2dc" frontColor="#a8a29e" sideColor="#c7c2bc" />
      <Box left={6} top={22} width={28} depth={18} base={21} height={1} topColor="#1e3a8a" frontColor="#1e3a8a" sideColor="#1e3a8a" />
      <Box left={16} top={6} width={8} depth={8} base={21} height={16} topColor="#d6d3d1" frontColor="#78716c" sideColor="#a8a29e" />
      <Box left={12} top={2} width={16} depth={10} base={37} height={7} topColor={accent} frontColor="#c2410c" sideColor="#ea580c" />
    </>
  );
}
