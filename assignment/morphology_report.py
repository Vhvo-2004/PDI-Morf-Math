import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
import textwrap

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_person_image():
    image = np.full((600, 800, 3), 255, dtype=np.uint8)
    cv2.putText(image, "Pessoa (sintetica)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2, cv2.LINE_AA)
    center = (400, 250)
    cv2.circle(image, (center[0], center[1] - 80), 60, (40, 120, 220), -1)  # head
    cv2.rectangle(image, (center[0] - 60, center[1] - 30), (center[0] + 60, center[1] + 130), (60, 160, 60), -1)  # torso
    cv2.line(image, (center[0] - 60, center[1] + 130), (center[0] - 120, center[1] + 250), (50, 90, 170), 18)  # left leg
    cv2.line(image, (center[0] + 60, center[1] + 130), (center[0] + 120, center[1] + 250), (50, 90, 170), 18)  # right leg
    cv2.line(image, (center[0] - 60, center[1] + 10), (center[0] - 180, center[1] - 40), (50, 90, 170), 16)  # left arm
    cv2.line(image, (center[0] + 60, center[1] + 10), (center[0] + 180, center[1] - 40), (50, 90, 170), 16)  # right arm
    cv2.circle(image, (center[0] - 20, center[1] - 90), 10, (255, 255, 255), -1)  # left eye
    cv2.circle(image, (center[0] + 20, center[1] - 90), 10, (255, 255, 255), -1)  # right eye
    cv2.ellipse(image, (center[0], center[1] - 60), (20, 10), 0, 0, 180, (240, 240, 240), -1)  # smile
    return image


def generate_object_image():
    image = np.full((600, 800, 3), 240, dtype=np.uint8)
    cv2.putText(image, "Objeto sintetico", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 60, 100), 2, cv2.LINE_AA)
    cv2.rectangle(image, (200, 200), (380, 420), (180, 80, 30), -1)  # box
    cv2.rectangle(image, (210, 210), (370, 330), (210, 120, 80), -1)
    cv2.rectangle(image, (210, 340), (370, 410), (130, 60, 20), -1)
    cv2.circle(image, (520, 310), 100, (60, 150, 220), -1)  # sphere
    cv2.circle(image, (520, 310), 70, (200, 230, 255), -1)
    cv2.line(image, (520, 210), (520, 110), (30, 90, 160), 12)  # stand
    cv2.line(image, (520, 110), (480, 70), (30, 90, 160), 12)
    cv2.line(image, (520, 110), (560, 70), (30, 90, 160), 12)
    return image


def generate_document_image():
    image = np.full((1000, 700, 3), 255, dtype=np.uint8)
    cv2.rectangle(image, (40, 40), (660, 960), (230, 230, 230), 2)
    cv2.putText(image, "Documento sintetico", (70, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
    for i, line in enumerate([
        "Aluno: Exemplo", "Curso: PDI", "Professor: Sintetico", "Instituicao: OpenAI",
        "Assinatura: ____________", "Data: 2024-05-10"
    ]):
        cv2.putText(image, line, (70, 150 + i * 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (30, 30, 30), 2, cv2.LINE_AA)
    for row in range(5):
        for col in range(2):
            top_left = (70 + col * 300, 500 + row * 90)
            bottom_right = (330 + col * 300, 560 + row * 90)
            cv2.rectangle(image, top_left, bottom_right, (120, 120, 120), 2)
            cv2.putText(image, f"Campo {row * 2 + col + 1}", (top_left[0] + 10, top_left[1] + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 2, cv2.LINE_AA)
    noise = np.random.randint(0, 25, image.shape, dtype=np.uint8)
    image = cv2.add(image, noise)
    return image


def save_image(name: str, image: np.ndarray):
    path = OUTPUT_DIR / name
    cv2.imwrite(str(path), image)
    return path


def image_metadata(name: str, image: np.ndarray):
    height, width, channels = image.shape
    depth_bits = 8 * channels
    metadata = {
        "nome": name,
        "dimensoes": f"{width}x{height}",
        "canais": channels,
        "profundidade_bits": depth_bits,
        "gamut": "sRGB aproximado (cores inteiras de 0-255)",
        "paleta": "RGB 24 bits"
    }
    return metadata


def decompose_rgb(name: str, image: np.ndarray):
    b, g, r = cv2.split(image)
    channels = {"B": b, "G": g, "R": r}
    channel_paths = {}
    for channel_name, channel_data in channels.items():
        stacked = cv2.merge([
            channel_data if channel_name == "B" else np.zeros_like(channel_data),
            channel_data if channel_name == "G" else np.zeros_like(channel_data),
            channel_data if channel_name == "R" else np.zeros_like(channel_data),
        ])
        path = save_image(f"{name}_{channel_name}.png", stacked)
        channel_paths[channel_name] = path
    histograms = {}
    for channel_name, channel_data in channels.items():
        hist, bins = np.histogram(channel_data.flatten(), 256, [0, 256])
        histograms[channel_name] = (hist, bins)
    return channel_paths, histograms


def plot_histograms(name: str, histograms):
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    colors = {"B": "blue", "G": "green", "R": "red"}
    for channel_name, (hist, bins) in histograms.items():
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


def morphological_process(name: str, image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opened = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    combined = cv2.merge([opened, closed, gradient])
    path = save_image(f"{name}_morfologia.png", combined)
    return path, {"abertura": opened, "fechamento": closed, "gradiente": gradient}


def wrap_text(text, width=90):
    return "\n".join(textwrap.wrap(text, width=width))


def add_text_page(pdf: PdfPages, title: str, body: str):
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis('off')
    plt.text(0.5, 0.9, title, ha='center', va='center', fontsize=18, fontweight='bold')
    plt.text(0.05, 0.82, wrap_text(body, 100), ha='left', va='top', fontsize=11)
    pdf.savefig(fig)
    plt.close(fig)


def add_image_page(pdf: PdfPages, title: str, image_paths):
    fig, axes = plt.subplots(1, len(image_paths), figsize=(8.27, 11.69))
    if len(image_paths) == 1:
        axes = [axes]
    fig.suptitle(title, fontsize=16)
    for ax, path in zip(axes, image_paths):
        img = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(path.name, fontsize=10)
    pdf.savefig(fig)
    plt.close(fig)


def create_report(metadata_list, hist_paths, morph_paths):
    report_path = OUTPUT_DIR / "relatorio_morfologia.pdf"
    with PdfPages(report_path) as pdf:
        add_text_page(pdf, "Capa",
                      "Titulo: Estudo de Morfologia Matematica\n"
                      "Aluno: Estudante Exemplo\n"
                      "Curso/Disciplina: PDI\n"
                      "Professor: Sintetico\n"
                      "Instituicao: OpenAI Demo\n"
                      "Data: 2024-05-10")

        add_text_page(pdf, "Resumo",
                      "Objetivo: investigar operacoes morfologicas (abertura, fechamento e gradiente) em imagens"
                      " sinteticas capturando pessoa, objeto e documento. Metodologia: geracao de imagens com"
                      " OpenCV, decomposicao em canais RGB, histogramas e aplicacao das operacoes. Resultados:"
                      " melhoria na homogeneidade de regioes apos abertura/fechamento e realce de contornos"
                      " via gradiente.")

        add_text_page(pdf, "Sumario",
                      "1. Introducao\n2. Referencial Teorico\n3. Metodologia\n4. Resultados e Discussao\n5. Conclusao\nReferencias\nApendices")

        add_text_page(pdf, "1. Introducao",
                      "Morfologia matematica utiliza operacoes baseadas em elementos estruturantes para analisar"
                      " formas. Nesta atividade o tema e aplicado a imagens coloridas, destacando o uso de"
                      " abertura, fechamento e gradiente morfologico para limpeza de ruido e realce de bordas.")

        add_text_page(pdf, "2. Referencial Teorico",
                      "A abertura (erosao seguida de dilatacao) remove detalhes pequenos, o fechamento (dilatacao"
                      " seguida de erosao) preenche lacunas, e o gradiente morfologico calcula a diferenca entre"
                      " dilatacao e erosao evidenciando bordas. Estruturantes retangulares 5x5 foram usados para"
                      " preservar estruturas maiores enquanto suavizam ruido fino.")

        metodologia = "3. Metodologia\nImagens sinteticas geradas em 24 bits, gamut sRGB aproximado. Cada foto"
        for meta in metadata_list:
            metodologia += f"\n- {meta['nome']}: {meta['dimensoes']} pixels, paleta {meta['paleta']}, " \
                            f"gamut {meta['gamut']}."
        metodologia += "\nProcedimentos: decomposicao de canais RGB, histogramas com 256 bins e aplicacao"
        metodologia += " de abertura, fechamento e gradiente em escala de cinza."
        add_text_page(pdf, "3. Metodologia", metodologia)

        add_text_page(pdf, "4. Resultados e Discussao",
                      "Os histogramas mostram distribuicao distinta de cores: a pessoa sintetica tem tons"
                      " de pele simulados concentrados em R e G; o objeto exibe picos em azuis e marrons; o"
                      " documento apresenta predominancia de altas intensidades devido ao fundo branco."
                      " A abertura reduziu ruido no documento, o fechamento suavizou sombras na pessoa e o"
                      " gradiente realcou contornos em todas as imagens.")

        add_text_page(pdf, "5. Conclusao",
                      "Operacoes morfologicas simples melhoraram a legibilidade das imagens sinteticas e"
                      " facilitaram a segmentacao de bordas. Dificuldades: restricao a imagens sinteticas."
                      " Como aprimoramento, testar estruturantes elipticos e combinacoes com limiarizacao.")

        add_text_page(pdf, "Referencias",
                      "Soille, P. Morphological Image Analysis. Serra, J. Image Analysis and Mathematical"
                      " Morphology. OpenCV Documentation.")

        for meta, hist_path, morph_path in zip(metadata_list, hist_paths, morph_paths):
            add_image_page(pdf, f"RGB e morfologia - {meta['nome']}", [meta['path'], hist_path, morph_path])

        add_text_page(pdf, "Apêndice - Codigo",
                      "O script morphology_report.py gera imagens sinteticas, decomposicao RGB, histogramas,"
                      " aplica morfologia e monta este PDF.")

    return report_path


def main():
    images = {
        "pessoa": generate_person_image(),
        "objeto": generate_object_image(),
        "documento": generate_document_image(),
    }

    metadata_list = []
    hist_paths = []
    morph_paths = []

    for name, image in images.items():
        path = save_image(f"{name}.png", image)
        meta = image_metadata(name, image)
        meta["path"] = path
        metadata_list.append(meta)

        channel_paths, histograms = decompose_rgb(name, image)
        hist_path = plot_histograms(name, histograms)
        hist_paths.append(hist_path)

        morph_path, _ = morphological_process(name, image)
        morph_paths.append(morph_path)

    report_path = create_report(metadata_list, hist_paths, morph_paths)
    print(f"Relatorio gerado em: {report_path}")


if __name__ == "__main__":
    main()
