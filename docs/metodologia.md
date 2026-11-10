# Metodologia de preparação dos dados

## Objetivo

Preparar as bases pluviométrica, geotécnica e hidrológica para análises exploratórias e visualizações do StormWatch, preservando a rastreabilidade das informações.

## Etapas

1. **Ingestão:** leitura dos três CSVs em `data/raw/` sem alterar a origem.
2. **Padronização:** normalização de datas, números decimais, nomes de colunas e metadados.
3. **Validação:** verificação de campos obrigatórios, datas, coordenadas, valores numéricos e chaves duplicadas.
4. **Tratamento:** sentinelas documentadas tornam-se ausentes no campo analítico; valor original e status permanecem disponíveis.
5. **Integração espacial:** cálculo da distância geodésica entre estações e classificação da correspondência como exata ou aproximada.
6. **Integração temporal:** associação por estação e timestamp idênticos; não há preenchimento, interpolação nem aproximação temporal automática.
7. **Relato:** geração de relatório JSON com contagens, regras e limitações.

## Interpretação responsável

- `-1000` nos sensores de umidade é tratado como sentinela, não como umidade física.
- Nível hidrológico `35` é sinalizado para investigação; não é descartado automaticamente.
- Uma estação próxima não é necessariamente representativa do mesmo microterritório. Correspondências aproximadas exigem validação.
- Sem unidades e limiares oficiais, o pipeline não cria classes de risco.
- A janela temporal recebida é histórica (janeiro de 2026), não monitoramento em tempo real.
