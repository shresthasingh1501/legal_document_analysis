# Legal Document Analysis

This repository contains scripts for analyzing legal documents in PDF format. The main functionalities include text extraction, summarization, named entity recognition (NER), and the ability to handle scanned documents using OCR. This project leverages various NLP models to provide comprehensive analysis of legal documents.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Analysis Script (analysis.py)](#analysis-script-analysispy)
  - [BERT OCR Script (bertocr.py)](#bert-ocr-script-bertocrpy)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Text Extraction**: Extracts text from PDF files, including OCR support for scanned documents.
- **Summarization**: Provides concise summaries of lengthy legal documents.
- **Named Entity Recognition (NER)**: Identifies and extracts named entities such as persons, organizations, and locations from the text.
- **Batch Processing**: Processes multiple PDF files in a directory, generating a comprehensive report.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/legal-doc-analysis.git
    cd legal-doc-analysis
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Analysis Script (analysis.py)

This script is designed to process a directory of legal PDF files, summarizing their content and extracting named entities.

1. Ensure you have the necessary model files downloaded for the summarization and NER tasks.
2. Run the script:

    ```bash
    python analysis.py
    ```

3. When prompted, enter the path to the directory containing the legal PDF files. The script will process each PDF in the directory, generate summaries, and extract named entities. The results will be saved to a CSV file in the same directory.

### BERT OCR Script (bertocr.py)

This script processes a single legal PDF file, with additional support for OCR to handle scanned documents.

1. Ensure you have Tesseract OCR installed and properly configured.
2. Run the script:

    ```bash
    python bertocr.py
    ```

3. When prompted, enter the path to the legal PDF file and the number of sentences for summarization. The script will extract text from the PDF, generate a summary, and extract named entities. The results will be saved to a text file in the `legal_document_analysis` folder.

## Requirements

- PyMuPDF
- bert-extractive-summarizer
- transformers
- torch
- sentence-transformers
- pytesseract
- Pillow
- scikit-learn
- streamlit

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any changes or improvements you would like to see.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

