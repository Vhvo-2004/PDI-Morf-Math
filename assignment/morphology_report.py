"""Demonstra morfologia matemática com base no notebook 13_morphological_operators.

Pipeline:
- Carrega fotografias reais (pessoa, objeto e documento) de um diretório indicado ou gera
  equivalentes sintéticos quando ausentes, mantendo especificações RGB de 24 bits.
- Coleta metadados técnicos: resolução, paleta e gamut aproximado.
- Decompõe em canais RGB, gera histogramas de 256 níveis.
- Aplica erosão, dilatação, abertura, fechamento e gradiente morfológico com elemento
  estruturante configurável, seguindo as operações do notebook base.
- Exporta PNGs intermediários e monta um relatório em PDF.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
INPUT_DIR = Path(__file__).resolve().parent / "input"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class ImageArtifact:
    """Mantém a imagem, metadados e caminhos de persistência."""

    name: str
    image: np.ndarray
    path: Path
    metadata: Dict[str, str]
    channel_paths: Dict[str, Path]
    histogram_path: Path
    morphology_paths: Dict[str, Path]


def generate_person_image(width: int, height: int) -> np.ndarray:
    """Cria um avatar estilizado para simular uma fotografia de pessoa."""

    img = np.full((height, width, 3), 255, dtype=np.uint8)
    cv2.putText(img, "Pessoa (sintetica)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (60, 60, 60), 2, cv2.LINE_AA)
    center = (width // 2, height // 2 - 40)
    head_radius = max(40, min(width, height) // 10)
    torso_w, torso_h = head_radius, head_radius * 2

    cv2.circle(img, (center[0], center[1] - head_radius - 10), head_radius, (40, 120, 220), -1)
    cv2.rectangle(img, (center[0] - torso_w, center[1] - 20), (center[0] + torso_w, center[1] + torso_h), (60, 160, 60), -1)

    leg_len = torso_h + head_radius
    arm_len = torso_w * 2
    cv2.line(img, (center[0] - torso_w, center[1] + torso_h), (center[0] - torso_w - 20, center[1] + leg_len), (50, 90, 170), 14)
    cv2.line(img, (center[0] + torso_w, center[1] + torso_h), (center[0] + torso_w + 20, center[1] + leg_len), (50, 90, 170), 14)
    cv2.line(img, (center[0] - torso_w, center[1] + 10), (center[0] - torso_w - arm_len, center[1] - 30), (50, 90, 170), 12)
    cv2.line(img, (center[0] + torso_w, center[1] + 10), (center[0] + torso_w + arm_len, center[1] - 30), (50, 90, 170), 12)

    cv2.circle(img, (center[0] - head_radius // 3, center[1] - head_radius - 20), 8, (255, 255, 255), -1)
    cv2.circle(img, (center[0] + head_radius // 3, center[1] - head_radius - 20), 8, (255, 255, 255), -1)
    cv2.ellipse(img, (center[0], center[1] - head_radius + 5), (head_radius // 2, head_radius // 4), 0, 0, 180, (240, 240, 240), -1)
    return img


def generate_object_image(width: int, height: int) -> np.ndarray:
    """Cria uma composição geométrica para simular um objeto tridimensional."""

    img = np.full((height, width, 3), 240, dtype=np.uint8)
    cv2.putText(img, "Objeto sintetico", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 60, 100), 2, cv2.LINE_AA)

    rect_w, rect_h = width // 5, height // 3
    rect_x, rect_y = width // 4, height // 3
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (180, 80, 30), -1)
    cv2.rectangle(img, (rect_x + 15, rect_y + 15), (rect_x + rect_w - 15, rect_y + rect_h // 2), (210, 120, 80), -1)
    cv2.rectangle(img, (rect_x + 15, rect_y + rect_h // 2 + 10), (rect_x + rect_w - 15, rect_y + rect_h - 15), (130, 60, 20), -1)

    radius = min(width, height) // 6
    center = (int(width * 0.65), int(height * 0.55))
    cv2.circle(img, center, radius, (60, 150, 220), -1)
    cv2.circle(img, center, radius - 30, (200, 230, 255), -1)
    cv2.line(img, (center[0], center[1] - radius), (center[0], center[1] - radius - 80), (30, 90, 160), 12)
    cv2.line(img, (center[0], center[1] - radius - 80), (center[0] - 40, center[1] - radius - 120), (30, 90, 160), 12)
    cv2.line(img, (center[0], center[1] - radius - 80), (center[0] + 40, center[1] - radius - 120), (30, 90, 160), 12)
    return img


def generate_document_image(width: int, height: int) -> np.ndarray:
    """Cria um documento com texto e campos, adicionando ruído leve."""

    img = np.full((height, width, 3), 255, dtype=np.uint8)
    margin_x, margin_y = width // 12, height // 20
    cv2.rectangle(img, (margin_x, margin_y), (width - margin_x, height - margin_y), (220, 220, 220), 2)
    cv2.putText(img, "Documento sintetico", (margin_x + 10, margin_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 3, cv2.LINE_AA)

    linhas = [
        "Aluno: Exemplo",
        "Curso: PDI",
        "Professor: Sintetico",
        "Instituicao: OpenAI",
        "Assinatura: ____________",
        "Data: 2024-05-10",
    ]
    for i, linha in enumerate(linhas):
        cv2.putText(img, linha, (margin_x + 10, margin_y + 110 + i * 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (30, 30, 30), 2, cv2.LINE_AA)

    box_w, box_h = (width - 2 * margin_x - 40) // 2, 60
    for row in range(5):
        for col in range(2):
            x1 = margin_x + 10 + col * (box_w + 40)
            y1 = margin_y + 350 + row * 80
            x2, y2 = x1 + box_w, y1 + box_h
            cv2.rectangle(img, (x1, y1), (x2, y2), (140, 140, 140), 2)
            cv2.putText(img, f"Campo {row * 2 + col + 1}", (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 2, cv2.LINE_AA)

    noise = np.random.randint(0, 25, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    return img


def save_image(name: str, image: np.ndarray) -> Path:
    path = OUTPUT_DIR / name
    cv2.imwrite(str(path), image)
    return path


def image_metadata(name: str, image: np.ndarray, source: str) -> Dict[str, str]:
    height, width, channels = image.shape
    return {
        "nome": name,
        "dimensoes": f"{width}x{height}",
        "canais": str(channels),
        "profundidade_bits": f"{8 * channels} bits (total)",
        "paleta": "RGB 24 bits",
        "gamut": "sRGB aproximado (inteiros 0-255)",
        "fonte": source,
    }


def load_or_generate(name: str, generator, width: int, height: int, input_dir: Path) -> Tuple[np.ndarray, str]:
    """Tenta carregar uma foto real do diretório informado; gera sintética se não encontrar."""

    extensions = (".png", ".jpg", ".jpeg", ".bmp")
    for ext in extensions:
        candidate = input_dir / f"{name}{ext}"
        if candidate.exists():
            image = cv2.imread(str(candidate))
            if image is None:
                break
            if image.ndim == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            return image, f"foto real ({candidate.name})"

    return generator(width, height), "sintética (gerada pelo script)"


def decompose_rgb(name: str, image: np.ndarray) -> Tuple[Dict[str, Path], Dict[str, Tuple[np.ndarray, np.ndarray]]]:
    """Separa canais e retorna caminhos e histogramas (256 bins)."""

    b, g, r = cv2.split(image)
    channels = {"B": b, "G": g, "R": r}
    channel_paths: Dict[str, Path] = {}
    histograms: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}

    for channel_name, channel_data in channels.items():
        stacked = cv2.merge([
            channel_data if channel_name == "B" else np.zeros_like(channel_data),
            channel_data if channel_name == "G" else np.zeros_like(channel_data),
            channel_data if channel_name == "R" else np.zeros_like(channel_data),
        ])
        channel_paths[channel_name] = save_image(f"{name}_{channel_name}.png", stacked)

        hist, bins = np.histogram(channel_data.flatten(), 256, [0, 256])
        histograms[channel_name] = (hist, bins)

    return channel_paths, histograms


def plot_histograms(name: str, histograms: Dict[str, Tuple[np.ndarray, np.ndarray]]) -> Path:
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    colors = {"B": "blue", "G": "green", "R": "red"}
    for channel_name, (hist, _) in histograms.items():
        ax.plot(hist, color=colors[channel_name], label=f"Canal {channel_name}")
    ax.set_title(f"Histograma RGB - {name}")
    ax.set_xlabel("Intensidade")
    ax.set_ylabel("Pixels")
    ax.legend()
    fig.tight_layout()
    path = OUTPUT_DIR / f"{name}_histograma.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def build_structuring_element(element: str, size: int) -> np.ndarray:
    shape_map = {
        "rect": cv2.MORPH_RECT,
        "ellipse": cv2.MORPH_ELLIPSE,
        "cross": cv2.MORPH_CROSS,
    }
    if element not in shape_map:
        raise ValueError(f"Elemento estruturante invalido: {element}")
    return cv2.getStructuringElement(shape_map[element], (size, size))


def morphological_process(name: str, image: np.ndarray, kernel: np.ndarray) -> Dict[str, Path]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    operations = {
        "erosao": lambda img: cv2.erode(img, kernel, iterations=1),
        "dilatacao": lambda img: cv2.dilate(img, kernel, iterations=1),
        "abertura": lambda img: cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel),
        "fechamento": lambda img: cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel),
        "gradiente": lambda img: cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel),
    }
    paths: Dict[str, Path] = {}
    results: Dict[str, np.ndarray] = {}

    for op_name, fn in operations.items():
        processed = fn(gray)
        path = save_image(f"{name}_{op_name}.png", processed)
        paths[op_name] = path
        results[op_name] = processed

    combined = cv2.merge(
        [results.get("erosao"), results.get("dilatacao"), results.get("gradiente")]
    )
    paths["combinado"] = save_image(f"{name}_morfologia.png", combined)
    return paths


def add_text_page(pdf: PdfPages, title: str, body: str) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis("off")
    plt.text(0.5, 0.92, title, ha="center", va="center", fontsize=18, fontweight="bold")
    plt.text(0.05, 0.85, body, ha="left", va="top", fontsize=11)
    pdf.savefig(fig)
    plt.close(fig)


def add_image_grid(pdf: PdfPages, title: str, images: Iterable[Tuple[str, Path]]) -> None:
    images = list(images)
    fig, axes = plt.subplots(1, len(images), figsize=(8.27, 11.69))
    if len(images) == 1:
        axes = [axes]
    fig.suptitle(title, fontsize=16)
    for ax, (legend, path) in zip(axes, images):
        img = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
        ax.imshow(img, cmap="gray")
        ax.axis("off")
        ax.set_title(legend, fontsize=10)
    pdf.savefig(fig)
    plt.close(fig)


def create_report(artifacts: List[ImageArtifact], kernel_size: int, element: str) -> Path:
    report_path = OUTPUT_DIR / "relatorio_morfologia.pdf"
    with PdfPages(report_path) as pdf:
        add_text_page(
            pdf,
            "Capa",
            "Titulo: Estudo de Morfologia Matematica (base: 13_morphological_operators.ipynb)\n"
            "Aluno: (preencher)\n"
            "Curso/Disciplina: PDI\n"
            "Professor: (preencher)\n"
            "Instituicao: (preencher)\n"
            "Data: (preencher)",
        )

        add_text_page(
            pdf,
            "Resumo",
            "Objetivo: reproduzir as operações do notebook 13_morphological_operators em fotos reais"
            " (ou versões sintéticas), com erosão, dilatação, abertura, fechamento e gradiente.\n"
            "Metodologia: leitura ou síntese das imagens (pessoa, objeto, documento), canais RGB,"
            " histogramas, conversão para escala de cinza e aplicação das operações com elemento"
            f" estruturante {element} de tamanho {kernel_size}.\n"
            "Resultados: separação de objetos, preenchimento de falhas e realce de bordas.",
        )

        add_text_page(
            pdf,
            "Sumario",
            "1. Introducao\n2. Referencial Teorico\n3. Metodologia\n4. Resultados e Discussao\n"
            "5. Conclusao\nReferencias\nApendices",
        )

        add_text_page(
            pdf,
            "1. Introducao",
            "Morfologia matematica manipula formas via elementos estruturantes. Operacoes basicas"
            " (erosao, dilatacao, abertura, fechamento, gradiente) permitem limpar ruido, separar"
            " objetos conectados e realcar bordas em imagens coloridas convertidas para escala de"
            " cinza, conforme explorado no notebook 13_morphological_operators.",
        )

        add_text_page(
            pdf,
            "2. Referencial Teorico",
            "Erosao e dilatacao sao operacoes fundamentais. Abertura = erosao + dilatacao;"
            " Fechamento = dilatacao + erosao; Gradiente = dilatacao - erosao. A forma e o tamanho"
            " do elemento estruturante controlam o nivel de suavizacao e preservacao de contornos.",
        )

        metodologia = [
            "3. Metodologia",
            "Fonte das imagens: fotos reais em assignment/input/ (pessoa.jpg/png, objeto.jpg/png, documento.jpg/png) ou",
            " versoes sinteticas quando ausentes, garantindo RGB 24 bits e gamut sRGB aproximado.",
            f"Elemento estruturante: {element}, tamanho {kernel_size} (cv2.getStructuringElement).",
            "Procedimentos: carregar/gerar imagens, decompor canais, histogramas 256 bins,",
            " aplicar erosao, dilatacao, abertura, fechamento e gradiente em escala de cinza;",
            " salvar evidencias e montar PDF.",
            "Metadados:",
        ]
        for art in artifacts:
            metodologia.append(
                f"- {art.metadata['nome']}: {art.metadata['dimensoes']} px, paleta {art.metadata['paleta']}, "
                f"gamut {art.metadata['gamut']}, origem {art.metadata['fonte']}"
            )
        add_text_page(pdf, "\n".join(metodologia[:1]), "\n".join(metodologia[1:]))

        add_text_page(
            pdf,
            "4. Resultados e Discussao",
            "Histogramas mostram distribuicoes distintas (tons de pele, fundos claros e cores"
            " frias). Erosao e dilatacao seguem o notebook base para separar ou preencher formas;"
            " abertura remove ruido do documento; fechamento consolida regioes no avatar;"
            " gradiente destaca contornos no objeto e no texto. Variar o kernel altera a relacao"
            " entre suavizacao e preservacao de detalhes.",
        )

        add_text_page(
            pdf,
            "5. Conclusao",
            "Operacoes morfologicas simples, parametrizadas por forma e tamanho do kernel,"
            " sao eficazes para limpar e realcar estruturas. Trabalhos futuros: top-hat/black-hat,"
            " processar canais individualmente, seguir demais exemplos do 13_morphological_operators",
            " (reconstrucao, gradientes internos/externos) e integrar OCR.",
        )

        add_text_page(
            pdf,
            "Referencias",
            "Gonzalez & Woods (2018) - Digital Image Processing\n"
            "Soille (2003) - Morphological Image Analysis\n"
            "Dougherty & Lotufo (2003) - Hands-On Morphological Image Processing\n"
            "OpenCV Documentation",
        )

        for art in artifacts:
            add_image_grid(
                pdf,
                f"RGB e histogramas - {art.name}",
                [
                    ("Original", art.path),
                    ("Histogramas RGB", art.histogram_path),
                ],
            )
            add_image_grid(
                pdf,
                f"Canais RGB - {art.name}",
                [(f"Canal {ch}", path) for ch, path in art.channel_paths.items()],
            )
            add_image_grid(
                pdf,
                f"Morfologia - {art.name}",
                [
                    ("Erosao", art.morphology_paths["erosao"]),
                    ("Dilatacao", art.morphology_paths["dilatacao"]),
                    ("Abertura", art.morphology_paths["abertura"]),
                    ("Fechamento", art.morphology_paths["fechamento"]),
                    ("Gradiente", art.morphology_paths["gradiente"]),
                    ("Combinado", art.morphology_paths["combinado"]),
                ],
            )

        add_text_page(
            pdf,
            "Apendice - Codigo",
            "O script morphology_report.py gera imagens sinteticas, histogramas e aplica"
            " operacoes morfologicas. Artefatos sao armazenados em assignment/output/",
        )
    return report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demonstra morfologia matematica com OpenCV")
    parser.add_argument("--img-width", type=int, default=800, help="Largura das imagens sinteticas (px)")
    parser.add_argument("--img-height", type=int, default=600, help="Altura das imagens sinteticas (px)")
    parser.add_argument("--kernel-size", type=int, default=5, help="Tamanho do elemento estruturante (impar)")
    parser.add_argument("--element", type=str, default="rect", choices=["rect", "ellipse", "cross"], help="Forma do elemento estruturante")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=INPUT_DIR,
        help="Diretorio com fotos reais (pessoa.*, objeto.*, documento.*); se vazio, gera imagens sinteticas",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    kernel_size = args.kernel_size if args.kernel_size % 2 == 1 else args.kernel_size + 1
    kernel = build_structuring_element(args.element, kernel_size)

    generators = {
        "pessoa": generate_person_image,
        "objeto": generate_object_image,
        "documento": generate_document_image,
    }

    artifacts: List[ImageArtifact] = []
    for name, generator in generators.items():
        image, source = load_or_generate(name, generator, args.img_width, args.img_height, args.input_dir)
        original_path = save_image(f"{name}.png", image)
        meta = image_metadata(name, image, source)

        channel_paths, histograms = decompose_rgb(name, image)
        histogram_path = plot_histograms(name, histograms)
        morphology_paths = morphological_process(name, image, kernel)

        artifacts.append(
            ImageArtifact(
                name=name,
                image=image,
                path=original_path,
                metadata=meta,
                channel_paths=channel_paths,
                histogram_path=histogram_path,
                morphology_paths=morphology_paths,
            )
        )

    report_path = create_report(artifacts, kernel_size, args.element)
    print(f"Relatorio gerado em: {report_path}")
    print("Imagens e histogramas: assignment/output/")
    print(f"Kernel: {args.element} de tamanho {kernel_size}")
    print(f"Fonte das imagens: {args.input_dir} (usa sinteticas se vazio)")


if __name__ == "__main__":
    main()
