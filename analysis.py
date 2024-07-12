import os
import fitz  # PyMuPDF
import csv
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForTokenClassification
import warnings
from sklearn.exceptions import ConvergenceWarning

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# Summarization pipeline setup
model_name = "shresthasingh/my_awesome_billsum_model"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# NER pipeline setup
ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        text += page_text
    return text

def summarize_text(text, min_length=30):
    return summarizer(text, min_length=min_length, do_sample=False)[0]['summary_text']

def chunk_text(text, chunk_size=512):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def recursive_summarize(text, chunk_size=300, min_length=30):
    if len(text.split()) <= chunk_size:
        return summarize_text(text, min_length)

    chunks = chunk_text(text, chunk_size)
    summaries = [summarize_text(chunk, min_length) for chunk in chunks]
    combined_summary = ' '.join(summaries)
    return recursive_summarize(combined_summary, chunk_size, min_length)

def extract_named_entities(text, chunk_size=256):
    chunks = chunk_text(text, chunk_size)
    entities = {'PER': set(), 'ORG': set(), 'LOC': set()}
    
    for chunk in chunks:
        ner_results = ner_pipeline(chunk)
        for result in ner_results:
            entity_type = result['entity'].split('-')[-1]
            if entity_type in entities:
                entity_value = result['word'].replace('##', '')
                entities[entity_type].add(entity_value)
    
    return entities

def process_legal_document(pdf_path):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Generate summary
    summary = recursive_summarize(text)
    
    # Extract named entities
    entities = extract_named_entities(text)
    
    return summary, entities

def process_directory(directory_path):
    output_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            summary, entities = process_legal_document(pdf_path)
            persons = ', '.join(entities['PER'])
            organizations = ', '.join(entities['ORG'])
            locations = ', '.join(entities['LOC'])
            output_data.append([filename, summary, persons, organizations, locations])
    
    output_csv = os.path.join(directory_path, "legal_document_analysis.csv")
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["File name", "File Summary", "Persons of Interest", "Organizations of Interest", "Locations of Interest"])
        for data in output_data:
            writer.writerow(data)
    
    print(f"\nAnalysis results have been saved to: {os.path.abspath(output_csv)}")

# Main execution
if __name__ == "__main__":
    directory_path = input("Enter the path to the directory containing legal PDF files: ")
    process_directory(directory_path)

