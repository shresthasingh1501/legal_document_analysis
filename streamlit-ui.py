import streamlit as st
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

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
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

def process_legal_document(pdf_file):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_file)
    
    # Generate summary
    summary = recursive_summarize(text)
    
    # Extract named entities
    entities = extract_named_entities(text)
    
    return summary, entities

# Streamlit App
st.title("Legal Document Summarizer")
st.write("Upload PDF documents to generate summaries and extract named entities.")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        summary, entities = process_legal_document(uploaded_file)
        
        st.write(f"**File:** {uploaded_file.name}")
        st.write(f"**Summary:** {summary}")
        
        st.write("**Named Entities:**")
        st.write(f"**Persons:** {', '.join(entities['PER'])}")
        st.write(f"**Organizations:** {', '.join(entities['ORG'])}")
        st.write(f"**Locations:** {', '.join(entities['LOC'])}")

st.write("Note: The analysis results are displayed above.")
