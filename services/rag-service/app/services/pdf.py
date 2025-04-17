from io import BytesIO

from pdfminer.high_level import extract_text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text content from a PDF byte stream.
    """
    with BytesIO(file_bytes) as file_stream:
        text = extract_text(file_stream)
    return text
