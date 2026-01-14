from pathlib import Path

from PyPDF2 import PdfReader


def read_pdf(filename) -> str:
    """
    Finds the PDF relative to this file's location and extracts text.
    :param filename: The name of the file (e.g., 'resume_kai.pdf')
    """
    # 1. Get the directory where THIS file is located
    current_dir = Path(__file__).resolve().parent

    # 2. Build the absolute path to the file
    pdf_path = current_dir.parent / "llm_prompts" / filename

    # 3. Safety Check: Does the file actually exist?
    if not pdf_path.exists():
        raise FileNotFoundError(f"Could not find PDF at: {pdf_path.absolute()}")

    # 4. Extract Text
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def read_text_file(filename) -> str:
    """
    Finds the text file relative to this file's location and reads its content.
    :param filename: The name of the file (e.g., 'summary.txt')
    """
    # 1. Get the directory where THIS file is located
    current_dir = Path(__file__).resolve().parent

    # 2. Build the absolute path to the file
    text_file_path = current_dir.parent / "llm_prompts" / filename

    # 3. Safety Check: Does the file actually exist?
    if not text_file_path.exists():
        raise FileNotFoundError(
            f"Could not find text file at: {text_file_path.absolute()}"
        )

    # 4. Read Content
    try:
        with open(text_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading text file: {str(e)}"
