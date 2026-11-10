# Dicionário de dados — preencher e validar

Este documento deve ser completado com os metadados oficiais dos provedores. Não inferir unidades ou significados apenas pelo nome da coluna.

| Campo padronizado | Descrição | Unidade | Observação |
|---|---|---|---|
| `municipio` | Município associado à estação | — | Conforme arquivo de origem |
| `codEstacao` | Identificador da estação | — | Chave de referência |
| `uf` | Unidade federativa | — | |
| `nomeEstacao` | Nome da estação | — | |
| `latitude`, `longitude` | Coordenadas da estação | graus decimais | Validar datum e precisão com o provedor |
| `datahora` | Data/hora da observação | — | Fuso não informado na origem |
| `sensor` | Identificador/tipo do sensor, quando aplicável | — | Confirmar semântica com provedor |
| `valorMedida` | Valor numérico padronizado | A confirmar | Não atribuir unidade sem documentação |
| `valorMedida_original` | Texto da medição original | — | Rastreabilidade |
| `status_qualidade` | Resultado das regras de qualidade | — | Ex.: válido, sentinela, revisar |
| `origem` | Base de origem | — | Pluviométrica, geotécnica ou hidrológica |

## Pendências de metadados

- Unidade da precipitação em cada arquivo e intervalo de acumulação.
- Unidade e referência do nível hidrológico, incluindo significado do valor 35.
- Unidade e escala dos sensores de umidade por profundidade.
- Fuso horário, convenção de horário e frequência esperada de cada sensor.
- Limites oficiais de alerta e fonte responsável por sua definição.
