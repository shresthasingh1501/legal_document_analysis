import os
import fitz  # PyMuPDF
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

def summarize_text(text, max_length=512, min_length=30):
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

def chunk_text(text, chunk_size=512):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def recursive_summarize(text, chunk_size=300, max_length=512, min_length=30):
    if len(text.split()) <= chunk_size:
        return summarize_text(text, max_length, min_length)

    chunks = chunk_text(text, chunk_size)
    summaries = [summarize_text(chunk, max_length, min_length) for chunk in chunks]
    combined_summary = ' '.join(summaries)
    return recursive_summarize(combined_summary, chunk_size, max_length, min_length)

def extract_named_entities(text):
    ner_results = ner_pipeline(text)
    
    entities = {'PER': set(), 'ORG': set(), 'LOC': set(), 'MISC': set()}
    for result in ner_results:
        entity_type = result['entity'].split('-')[-1]
        entity_value = result['word'].replace('##', '')
        if entity_type in entities:
            entities[entity_type].add(entity_value)
    
    return entities

def process_legal_document(pdf_path):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Generate summary
    summary = recursive_summarize(text)
    
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
        f.write("Summary:\n")
        f.write(summary)
        f.write("\n\nNamed Entities:\n")
        for entity_type, entity_values in entities.items():
            f.write(f"{entity_type}: {', '.join(entity_values)}\n")
    
    return output_file

# Main execution
if __name__ == "__main__":
    pdf_path = input("Enter the path to the legal PDF file: ")
    output_file = process_legal_document(pdf_path)
    print(f"\nAnalysis results have been saved to: {os.path.abspath(output_file)}")
