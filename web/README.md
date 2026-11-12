# Mars Mission Control 3D (frontend React)

Versão 3D do painel de controle das sondas, conectada aos três endpoints da API.
Usa só React e CSS 3D (`perspective`, `rotateX`, `preserve-3d`), sem bibliotecas de 3D.

## Como usar num projeto Vite

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

Copie a pasta `src/` deste pacote por cima da `src/` gerada (substitua o `App.jsx`)
e apague o `index.css` e o `App.css` do template, se não quiser os estilos padrão.

Crie um arquivo `.env` na pasta do frontend apontando para a API:

```
VITE_API_URL=http://localhost:8000
```

E rode:

```bash
npm run dev
```

Lembre de liberar o CORS no backend para a origem do Vite (`http://localhost:5173`).

## Contrato da API esperado

| Ação | Requisição | Resposta |
| --- | --- | --- |
| Lançar | `POST /probes` com `{ "x": 5, "y": 5, "direction": "NORTH" }` | `{ "id", "x", "y", "direction" }` |
| Mover | `POST /probes/{id}/commands` com `{ "commands": "MRM" }` | `{ "id", "x", "y", "direction" }` |
| Listar | `GET /probes` | `{ "probes": [ ... ] }` |

Erros: o front mostra o campo `detail` da resposta (o formato padrão do FastAPI).

Se a sua rota ou o nome do campo forem outros, ajuste só o arquivo `src/api.js`.

### Sobre o tamanho da grid

O contrato do enunciado não devolve o tamanho da grid. O front guarda o tamanho
enviado no lançamento (no `localStorage`). Se a API também devolver `grid_max_x` e
`grid_max_y`, o front usa esses valores, o que funciona mesmo depois de limpar o navegador.

## Estrutura

```
src/
├── api.js               chamadas aos três endpoints
├── directions.js        ordem da bússola e cálculo da rotação do rover
├── App.jsx              estado da tela e ligação entre os componentes
├── mars3d.css           estilos, incluindo a cena 3D
└── components/
    ├── LaunchForm.jsx    formulário de lançamento
    ├── ProbeList.jsx     lista de sondas (a frota)
    ├── Plateau3D.jsx     o planalto inclinado em 3D
    ├── Rover.jsx         o rover, feito de caixas 3D
    ├── CommandPanel.jsx  sequência de comandos e botões L, M, R
    └── MissionLog.jsx    histórico de envios, com os erros
```

## Como o 3D funciona

- O contêiner `.scene` tem `perspective`, que cria a profundidade.
- O planalto `.board` é inclinado com `rotateX(58deg) rotateZ(-40deg)`.
- Cada peça do rover é uma `Box`: cinco `div`s (quatro laterais e o topo)
  posicionadas com `rotateX`/`rotateY` dentro de um elemento com `transform-style: preserve-3d`.
- A direção é um `rotateZ` no rover. O ângulo é **acumulado** (+90 no R, -90 no L),
  para a animação nunca dar uma volta inteira ao contrário entre WEST e NORTH.
- O movimento é um `transition` em `left` e `top`.
