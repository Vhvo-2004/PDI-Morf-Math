# Relatório e Ferramental de Morfologia Matemática

Este diretório entrega um roteiro completo para produzir o relatório em PDF e os artefatos experimentais do trabalho de **Morfologia Matemática**. Ele contém um script Python que gera imagens sintéticas (pessoa, objeto e documento), extrai metadados técnicos, decompõe cada canal RGB, calcula histogramas e aplica operações morfológicas clássicas.

## Estrutura
- `morphology_report.py`: script principal que cria as imagens sintéticas, executa as operações e compila o PDF.
- `Relatorio_Morfologia_Matematica.md`: modelo técnico do relatório com todas as seções exigidas.
- `output/`: pasta gerada automaticamente com imagens intermediárias, gráficos e o PDF final (`relatorio_morfologia.pdf`).

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

### Parâmetros principais
O script aceita ajustes para facilitar a experimentação das ferramentas de morfologia:
```bash
python assignment/morphology_report.py \
  --img-width 800 \
  --img-height 600 \
  --kernel-size 5 \
  --element rect
```
- `--img-width` / `--img-height`: resolução das imagens sintéticas.
- `--kernel-size`: tamanho (ímpar) do elemento estruturante.
- `--element`: forma do elemento estruturante (`rect`, `ellipse` ou `cross`).

### Como testar as operações morfológicas
1. Gere os artefatos com o kernel padrão (5×5 retangular):
   ```bash
   python assignment/morphology_report.py
   ```
2. Varie o elemento estruturante para observar ganhos ou perdas de detalhe:
   ```bash
   python assignment/morphology_report.py --kernel-size 9 --element ellipse
   python assignment/morphology_report.py --kernel-size 3 --element cross
   ```
3. Compare as imagens `*_morfologia.png` (abertura, fechamento, gradiente) e os histogramas em `assignment/output/` para avaliar o efeito de cada parâmetro.
4. Consulte `relatorio_morfologia.pdf` para um resumo textual e visual das execuções.

## Observação sobre as imagens
As "fotografias" são sintetizadas com primitivas do OpenCV para contornar restrições de captura real. Cada imagem é gerada em RGB de 8 bits por canal (24 bits) com gamut aproximado sRGB, mantendo as especificações solicitadas (tamanho, paleta e profundidade) para fins didáticos e reprodutíveis.
