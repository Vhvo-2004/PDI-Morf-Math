# Relatorio de Morfologia Matematica

Este diretório contém o script `morphology_report.py`, que gera imagens sintéticas (pessoa, objeto e documento), decompõe cada uma nos canais RGB, calcula histogramas e aplica operações morfológicas (abertura, fechamento e gradiente). Os resultados são exportados como imagens e reunidos em um relatório PDF.

## Requisitos
- Python 3.11+
- Bibliotecas: `opencv-python-headless`, `numpy` e `matplotlib`

Em ambientes sem acesso à internet, instale os pacotes a partir de um espelho local ou de arquivos `.whl` pré-baixados.

## Uso
Execute o script a partir da raiz do repositório:

```bash
python assignment/morphology_report.py
```

Os arquivos gerados serão gravados em `assignment/output/`, incluindo as imagens intermediárias e o PDF `relatorio_morfologia.pdf`.

## Observação sobre as imagens
As "fotografias" são ilustrações sintéticas criadas com primitivas gráficas do OpenCV para respeitar a restrição de não capturar fotos reais neste ambiente. Elas preservam as características técnicas solicitadas (canais RGB de 8 bits, gamut aproximado sRGB) e servem para demonstrar o fluxo de processamento morfológico.
