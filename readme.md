# Legal Document Analysis

This Python script, `analysis.py`, extracts text from legal PDFs, summarizes the content, and extracts named entities. It uses various libraries including PyMuPDF for PDF text extraction, PyTesseract for OCR, and Transformers for Named Entity Recognition (NER).

## Features

- **Text Extraction**: Extracts text from PDF files, including OCR for scanned images.
- **Text Summarization**: Provides a concise summary of the document.
- **Named Entity Recognition (NER)**: Identifies and categorizes entities in the text.

## Prerequisites

Ensure you have the following installed:

- Python 3.6 or higher
- Pip (Python package installer)

## Installation

1. Clone this repository or download the `analysis.py` script and `requirements.txt` file.

    ```bash
    git clone https://github.com/yourusername/legal-document-analysis.git
    cd legal-document-analysis
    ```

2. Install the required Python packages using the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

3. Install Tesseract OCR:
    - **Windows**: Download and install from [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
    - **macOS**: Install via Homebrew with `brew install tesseract`.
    - **Linux**: Install via your package manager, e.g., `sudo apt-get install tesseract-ocr`.

## Usage

1. Run the script:

    ```bash
    python analysis.py
    ```

2. When prompted, enter the path to the legal PDF file and the number of sentences for the summary.

    ```
    Enter the path to the legal PDF file: /path/to/your/document.pdf
    Enter the number of sentences for summarization: 5
    ```

3. The script will create a folder named `legal_document_analysis` and save the results to a file named `document_analysis.txt` (where `document` is the name of your PDF file without the extension).

## Example Output


