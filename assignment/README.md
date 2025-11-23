# Relatório e Ferramental de Morfologia Matemática (base: `13_morphological_operators.ipynb`)

Este diretório entrega um roteiro completo para produzir o relatório em PDF e os artefatos experimentais do trabalho de **Morfologia Matemática**, tomando como referência o notebook `Python_OpenCV4/13_morphological_operators.ipynb`. Ele contém um script Python que lê fotografias reais (quando fornecidas) ou gera imagens sintéticas (pessoa, objeto e documento), extrai metadados técnicos, decompõe cada canal RGB, calcula histogramas e aplica operações morfológicas clássicas (erosão, dilatação, abertura, fechamento e gradiente).

## Estrutura
- `morphology_report.py`: script principal inspirado no notebook 13_morphological_operators, que carrega fotos ou cria imagens sintéticas, executa as operações e compila o PDF.
- `Relatorio_Morfologia_Matematica.md`: modelo técnico do relatório com todas as seções exigidas.
- `output/`: pasta gerada automaticamente com imagens intermediárias, gráficos e o PDF final (`relatorio_morfologia.pdf`).
- `input/`: opcional. Coloque aqui `pessoa.jpg/png`, `objeto.jpg/png` e `documento.jpg/png` para usar fotografias reais.

## Requisitos
- Python 3.11+
- Pacotes: `opencv-python-headless`, `numpy`, `matplotlib`

Instale-os com:
```bash
python -m pip install opencv-python-headless numpy matplotlib
```

## Uso rápido
Execute a partir da raiz do repositório:
```bash
python assignment/morphology_report.py
```
Os artefatos são gravados em `assignment/output/`.

### Usando fotos reais
1. Crie/abra a pasta `assignment/input/`.
2. Adicione arquivos nomeados `pessoa.jpg/png`, `objeto.jpg/png` e `documento.jpg/png` (BGR ou RGB). O script fará a leitura automática.
3. Rode normalmente o comando acima (ou com parâmetros adicionais). Se algum arquivo não existir, uma imagem sintética equivalente será gerada.

### Parâmetros principais
O script aceita ajustes para facilitar a experimentação das ferramentas de morfologia:
```bash
python assignment/morphology_report.py \
  --img-width 800 \
  --img-height 600 \
  --kernel-size 5 \
  --element rect \
  --input-dir assignment/input
```
- `--img-width` / `--img-height`: resolução das imagens sintéticas.
- `--kernel-size`: tamanho (ímpar) do elemento estruturante.
- `--element`: forma do elemento estruturante (`rect`, `ellipse` ou `cross`).
- `--input-dir`: diretório com as fotos reais (pessoa/objeto/documento) para substituir as versões sintéticas.

### Como testar as ferramentas de morfologia matemática
1. Gere os artefatos com o kernel padrão (5×5 retangular):
   ```bash
   python assignment/morphology_report.py
   ```
2. Varie o elemento estruturante para observar ganhos ou perdas de detalhe (erosão, dilatação, abertura, fechamento e gradiente são recalculados):
   ```bash
   python assignment/morphology_report.py --kernel-size 9 --element ellipse
   python assignment/morphology_report.py --kernel-size 3 --element cross
   ```
3. Compare as imagens `*_morfologia.png` (abertura, fechamento, gradiente) e os histogramas em `assignment/output/` para avaliar o efeito de cada parâmetro.
4. Consulte `relatorio_morfologia.pdf` para um resumo textual e visual das execuções.

## Observação sobre as imagens
- **Prioridade**: quando existirem fotos reais em `assignment/input/`, elas serão utilizadas e mencionadas no PDF.
- **Fallback**: se algum arquivo não existir, o script cria uma versão sintética em RGB de 8 bits por canal (24 bits) com gamut aproximado sRGB, respeitando tamanho, paleta e profundidade solicitados.
