import os
import fitz  # PyMuPDF
from summarizer import Summarizer
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import warnings
from sklearn.exceptions import ConvergenceWarning
import pytesseract
from PIL import Image
import io

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        if not page_text.strip():  # If no text was extracted, try OCR
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            page_text = pytesseract.image_to_string(img)
        text += page_text
    return text

def summarize_text(text, num_sentences):
    model = Summarizer()
    summary = model(text, num_sentences=num_sentences)
    return summary

def extract_named_entities(text):
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    ner_results = nlp(text)
    
    entities = {}
    for result in ner_results:
        entity_type = result['entity']
        entity_value = result['word'].replace('##', '')
        if entity_type not in entities:
            entities[entity_type] = set()
        entities[entity_type].add(entity_value)
    
    return entities

def process_legal_document(pdf_path, num_sentences):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Generate summary
    summary = summarize_text(text, num_sentences)
    
    # Extract named entities
    entities = extract_named_entities(text)
    
    # Create output folder
    output_folder = "legal_document_analysis"
    os.makedirs(output_folder, exist_ok=True)
    
    # Get the base name of the PDF file without extension
    pdf_base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Save results to a text file with the same name as the PDF
    output_file = os.path.join(output_folder, f"{pdf_base_name}_analysis.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{num_sentences}-line Summary:\n")
        f.write(summary)
        f.write("\n\nNamed Entities:\n")
        for entity_type, entity_values in entities.items():
            f.write(f"{entity_type}: {', '.join(entity_values)}\n")
    
    return output_file

# Main execution
if __name__ == "__main__":
    pdf_path = input("Enter the path to the legal PDF file: ")
    num_sentences = int(input("Enter the number of sentences for summarization: "))
    output_file = process_legal_document(pdf_path, num_sentences)
    print(f"\nAnalysis results have been saved to: {os.path.abspath(output_file)}")
