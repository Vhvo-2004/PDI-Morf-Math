# Relatório de Morfologia Matemática (base: `Python_OpenCV4/13_morphological_operators.ipynb`)

## Capa
- **Título da atividade:** Processamento Digital de Imagens com Morfologia Matemática
- **Nome do aluno:** _Preencha aqui_
- **Curso e disciplina:** _Preencha aqui_
- **Nome do professor:** _Preencha aqui_
- **Instituição:** _Preencha aqui_
- **Data:** _Preencha aqui_

## Resumo
Este documento integra referencial teórico e experimentos realizados com o script `assignment/morphology_report.py`, derivado do notebook `13_morphological_operators.ipynb`. Três imagens (fotos reais quando disponíveis, ou versões sintéticas) — pessoa, objeto e documento — são processadas em RGB 8 bits, decompostas nos canais R, G e B, têm seus histogramas calculados e recebem as operações de erosão, dilatação, abertura, fechamento e gradiente morfológico. Os resultados evidenciam o impacto do elemento estruturante na separação de objetos, remoção de ruído, preenchimento de lacunas e realce de contornos.

## Sumário
1. [Introdução](#1-introdução)  
2. [Referencial Teórico](#2-referencial-teórico)  
3. [Metodologia](#3-metodologia)  
4. [Resultados e Discussão](#4-resultados-e-discussão)  
5. [Conclusão](#5-conclusão)  
6. [Referências](#referências)  
7. [Apêndices ou Anexos](#apêndices-ou-anexos)

## 1. Introdução
A morfologia matemática manipula formas em imagens por meio de elementos estruturantes. Neste trabalho, seguindo o roteiro do notebook `13_morphological_operators.ipynb`, aplica-se o tema a imagens coloridas (fotos reais ou equivalentes sintéticas), observando como erosão, dilatação, abertura, fechamento e gradiente alteram regiões homogêneas e bordas. O processamento digital de imagens é fundamental em inspeção industrial, OCR e biometria, pois permite remover ruídos, preencher falhas e destacar transições relevantes.

## 2. Referencial Teórico
- **Erosão:** remove pixels nas bordas, separando objetos conectados (como as moedas no notebook base) e suavizando contornos.
- **Dilatação:** adiciona pixels às bordas, reparando quebras e preenchendo intrusões.
- **Abertura (erosão seguida de dilatação):** remove estruturas pequenas e ruídos impulsivos, preservando formas maiores.
- **Fechamento (dilatação seguida de erosão):** preenche lacunas e suaviza depressões em objetos.
- **Gradiente morfológico (dilatação − erosão):** destaca contornos e transições de intensidade.
- **Elementos estruturantes:** retangulares, elípticos ou em cruz. O tamanho controla o nível de suavização; formas elípticas tendem a preservar contornos arredondados, enquanto cruz enfatiza direções ortogonais.
- **Espaço de cor:** operações aplicadas em escala de cinza para consistência entre canais, evitando artefatos cromáticos; histogramas por canal ajudam a entender a distribuição de intensidades antes e depois das operações.

## 3. Metodologia
1. **Fotografias reais (preferencial) ou sintéticas:**
   - Aplique fotos autorais nomeadas `pessoa.jpg/png`, `objeto.jpg/png` e `documento.jpg/png` em `assignment/input/`; o script as lê automaticamente.
   - Se ausentes, cria versões sintéticas: avatar vetorial, composição geométrica e documento com ruído aditivo para simular digitalização.
2. **Especificações técnicas:** RGB de 8 bits por canal (24 bits), gamut aproximado sRGB; resolução padrão 800×600 px (ajustável por linha de comando).
3. **Ferramentas:** Python 3.11+, OpenCV (`opencv-python-headless`), NumPy e Matplotlib. Execução via `python assignment/morphology_report.py`.
4. **Procedimentos:** carregar/gerar as três imagens; decompor em canais R, G e B; histogramas de 256 níveis; conversão para escala de cinza; aplicação de erosão, dilatação, abertura, fechamento e gradiente com elemento estruturante configurável; exportação de imagens e PDF para `assignment/output/`.
5. **Algoritmo:**
   - Criação ou leitura do elemento estruturante (`cv2.getStructuringElement`) com forma e tamanho parametrizáveis.
   - Processamento morfológico em escala de cinza: `cv2.erode`, `cv2.dilate` e `cv2.morphologyEx` com códigos `MORPH_OPEN`, `MORPH_CLOSE` e `MORPH_GRADIENT`.
   - Persistência de resultados (RGB original, canais, histogramas e composições morfológicas) para análise e inserção automática no PDF.

## 4. Resultados e Discussão
- **Histogramas e decomposição RGB:** os picos de intensidade refletem predominância de cores (tons de pele para a pessoa, azuis/marrons no objeto, altos valores para o fundo do documento). A decomposição evidencia quais canais são mais afetados pelas operações.
- **Efeito do elemento estruturante:**
  - Erosão separa formas conectadas e suprime detalhes finos; dilatação repara quebras.
  - Abertura reduz ruídos pontuais e remove pequenos traços no documento.
  - Fechamento preenche lacunas, mantendo contornos maiores e consolidando regiões da figura da pessoa.
  - Gradiente realça bordas e permite observar o contorno de letras, membros e arestas geométricas.
- **Análise paramétrica:** aumentar o `kernel-size` amplia a suavização e reduz detalhes; escolher `ellipse` tende a preservar curvas, enquanto `cross` privilegia detalhes ortogonais. A avaliação deve considerar o equilíbrio entre remoção de ruído e preservação de informação.

## 5. Conclusão
As operações de erosão, dilatação, abertura, fechamento e gradiente, aplicadas com elementos estruturantes configuráveis, demonstram capacidade de limpeza e realce em imagens coloridas tratadas em escala de cinza. Ajustar tamanho e forma do kernel permite controlar o compromisso entre suavização e preservação de contornos. Futuras extensões podem incluir top-hat/black-hat, processamento por canal, reconstrução morfológica e integração com limiarização adaptativa para pipelines de OCR.

## Referências
- Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson.  
- Soille, P. (2003). *Morphological Image Analysis: Principles and Applications* (2nd ed.). Springer.  
- Dougherty, E. R., & Lotufo, R. A. (2003). *Hands-On Morphological Image Processing*. SPIE.  
- OpenCV. (2024). *Morphological Operations* — https://docs.opencv.org

## Apêndices ou Anexos
- **Código-fonte comentado:** `assignment/morphology_report.py` (gera ou lê imagens, histogramas, morfologia e PDF).
- **Imagens utilizadas:** fotos reais em `assignment/input/` quando presentes; caso contrário, versões sintéticas salvas em `assignment/output/`.
- **Gráficos adicionais:** histogramas e composições morfológicas exportadas na mesma pasta.
