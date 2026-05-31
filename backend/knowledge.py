import os
os.environ["DOCLING_DEVICE"] = "cpu"

from docling.document_converter import DocumentConverter

def build_knowledge_base():
    converter = DocumentConverter()
    result = converter.convert("1304.1672v2.pdf")
    
    text = result.document.export_to_markdown()
    
    chunks = []
    paragraphs = text.split('\n\n')
    for p in paragraphs:
        if len(p.strip()) > 100:
            chunks.append(p.strip())
    
    return chunks

def get_relevant_chunks(chunks, query_terms):
    relevant = []
    for chunk in chunks:
        if any(term.lower() in chunk.lower() for term in query_terms):
            relevant.append(chunk)
    return relevant[:3]

if __name__ == "__main__":
    print("Building knowledge base from TORCS manual...")
    chunks = build_knowledge_base()
    print(f"Extracted {len(chunks)} chunks")
    print("\nSample chunk:")
    print(chunks[0])