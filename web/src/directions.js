// Ordem da bússola: girar para a direita = próxima da lista.
export const DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"];

// Ângulo do rover na tela para cada direção (0° = olhando para cima).
export function angleOf(direction) {
  return DIRECTIONS.indexOf(direction) * 90;
}

// Quanto girar o rover de uma direção para outra pelo caminho mais curto.
// Usamos o ângulo acumulado para a animação nunca dar uma volta inteira ao contrário
// (por exemplo, de WEST = 270° para NORTH = 0° o certo é girar +90°, não -270°).
export function rotationDelta(from, to) {
  const steps = (DIRECTIONS.indexOf(to) - DIRECTIONS.indexOf(from) + 4) % 4;
  if (steps === 3) return -90;
  return steps * 90;
}
