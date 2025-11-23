# Relatório de Morfologia Matemática

## Capa
- **Título da atividade:** Processamento Digital de Imagens com Morfologia Matemática
- **Nome do aluno:** _Preencha aqui_
- **Curso e disciplina:** _Preencha aqui_
- **Nome do professor:** _Preencha aqui_
- **Instituição:** _Preencha aqui_
- **Data:** _Preencha aqui_

## Resumo
Este relatório apresenta um estudo de morfologia matemática aplicada ao processamento digital de imagens. Foi construída uma base sintética com três fotografias (pessoa, objeto e documento) geradas pelo script `assignment/morphology_report.py`, que decompoe cada imagem em canais RGB, calcula histogramas e aplica operações de abertura, fechamento e gradiente. Os resultados experimentais demonstram como operações morfológicas alteram estruturas e texturas, preservando ou removendo detalhes conforme o elemento estruturante utilizado.

## Sumário
1. [Introdução](#1-introdução)
2. [Referencial Teórico](#2-referencial-teórico)
3. [Metodologia](#3-metodologia)
4. [Resultados e Discussão](#4-resultados-e-discussão)
5. [Conclusão](#5-conclusão)
6. [Referências](#referências)
7. [Apêndices ou Anexos](#apêndices-ou-anexos)

## 1. Introdução
A morfologia matemática oferece um conjunto de operações que manipulam formas em imagens por meio de elementos estruturantes. Neste trabalho, o objetivo é ilustrar como abertura, fechamento e gradiente podem realçar bordas, remover ruído e modificar contrastes em imagens coloridas. O processamento digital de imagens viabiliza análises automatizadas em áreas como inspeção industrial, biometria e digitalização de documentos, justificando o estudo das transformações morfológicas básicas.

## 2. Referencial Teórico
- **Conceitos fundamentais:** Abertura (erosão seguida de dilatação) para remover pequenas estruturas; fechamento (dilatação seguida de erosão) para preencher lacunas; gradiente morfológico (diferença entre dilatação e erosão) para realçar contornos. Em imagens RGB, as operações são aplicadas canal a canal ou sobre representações derivadas (ex.: escala de cinza).
- **Fundamentos matemáticos:** Operações definidas sobre conjuntos; elemento estruturante modela vizinhanças; uso de convoluções discretas para aplicar as transformações canalizadas.
- **Trabalhos relacionados:** Aplicações comuns incluem filtragem de ruído impulsivo, segmentação de caracteres e realce de bordas em pipelines de OCR e visão industrial.

## 3. Metodologia
1. **Fotografias sintéticas:**
   - **Pessoa:** Avatar estilizado com fundo uniforme para simular retrato.
   - **Objeto:** Figura geométrica com sombras leves para simular tridimensionalidade.
   - **Documento:** Página com texto e caixas para simular campos preenchidos.
2. **Especificações técnicas:** Imagens em cores (RGB), 8 bits por canal (24 bits totais), gamut aproximado sRGB; resolução padrão de 640×480 pixels, podendo ser ajustada pelo parâmetro `img_size` no script.
3. **Ferramentas:** Python 3.11+, OpenCV (`opencv-python-headless`), NumPy e Matplotlib. Execução pelo comando `python assignment/morphology_report.py` a partir da raiz do repositório.
4. **Procedimentos:**
   - Geração das três imagens com primitivas do OpenCV.
   - Decomposição de cada imagem em canais R, G e B.
   - Cálculo e plotagem dos histogramas de intensidade para cada canal.
   - Aplicação das operações morfológicas (abertura, fechamento e gradiente) em cada imagem.
   - Exportação das imagens intermediárias e finais para `assignment/output/`.
5. **Algoritmo principal:** Para cada imagem, os canais são processados individualmente com um elemento estruturante retangular (tamanho configurável). As operações são implementadas via `cv2.morphologyEx` com códigos `MORPH_OPEN`, `MORPH_CLOSE` e `MORPH_GRADIENT`, garantindo a mesma estruturação nos três canais para manter a consistência cromática.

## 4. Resultados e Discussão
- **Histogramas e decomposição RGB:** Os histogramas refletem a distribuição de intensidades em cada canal, permitindo observar predominâncias de cores (ex.: tons de pele na imagem da pessoa ou fundo claro no documento). A decomposição visual dos canais ajuda a identificar quais cores são mais afetadas pelas operações morfológicas.
- **Aplicação das operações:**
  - **Abertura:** Suaviza ruídos e remove pequenos detalhes, útil para limpar fundos.
  - **Fechamento:** Preenche lacunas e reforça regiões sólidas, preservando contornos maiores.
  - **Gradiente:** Destaca bordas e transições de intensidade, facilitando segmentação.
- **Análise:** Comparando imagens originais e processadas, nota-se redução de ruído em fundos homogêneos após abertura, fechamento de pequenas falhas em caracteres do documento e realce de bordas no gradiente. A escolha do tamanho do elemento estruturante influencia diretamente a quantidade de detalhes preservados ou removidos.

## 5. Conclusão
As operações morfológicas demonstradas evidenciam a utilidade de abertura, fechamento e gradiente para manipular formas e texturas em imagens coloridas. A abordagem canal a canal preserva a consistência cromática enquanto modifica a estrutura de acordo com o elemento estruturante. Trabalhos futuros podem explorar elementos estruturantes personalizados, pipelines de segmentação e integração com algoritmos de OCR.

## Referências
- Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson.
- Soille, P. (2003). *Morphological Image Analysis: Principles and Applications* (2nd ed.). Springer.
- Dougherty, E. R., & Lotufo, R. A. (2003). *Hands-On Morphological Image Processing*. SPIE.

## Apêndices ou Anexos
- **Código-fonte comentado:** Ver `assignment/morphology_report.py` para geração das imagens, histogramas e operações morfológicas.
- **Imagens utilizadas:** Geradas automaticamente em `assignment/output/` ao executar o script.
- **Gráficos adicionais:** Histogramas por canal são exportados junto às figuras de decomposição e operações morfológicas.
