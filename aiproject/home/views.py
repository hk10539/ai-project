from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from PyPDF2 import PdfReader
import PyPDF2

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# =====================================================
# Helper Functions
# =====================================================

def validate_pdf(request):
    pdf = request.FILES.get('pdf')
    if not pdf or not pdf.name.endswith('.pdf'):
        return None
    return pdf


def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() or "" for page in reader.pages])


def chunk_text(text, size=500):
    return [text[i:i + size] for i in range(0, len(text), size)]


# =====================================================
# Load AI Models (once)
# =====================================================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS globals
faiss_index = None
stored_chunks = []


# =====================================================
# FAISS APIs
# =====================================================

@api_view(['POST'])
def build_faiss_index(request):
    global faiss_index, stored_chunks

    pdf_file = validate_pdf(request)
    if not pdf_file:
        return Response(
            {"error": "Please upload a valid PDF file"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Read and chunk PDF
    text = read_pdf(pdf_file)
    chunks = chunk_text(text)

    # Generate embeddings
    embeddings = embedding_model.encode(chunks)

    # Build FAISS index
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(np.array(embeddings))

    stored_chunks = chunks

    return Response(
        {
            "message": "FAISS index created successfully",
            "total_chunks": len(chunks),
            "embedding_dimension": dimension
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def semantic_search(request):
    query = request.data.get("query")

    if not query:
        return Response(
            {"error": "Query is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if faiss_index is None:
        return Response(
            {"error": "FAISS index not built yet"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Query embedding
    query_embedding = embedding_model.encode([query])

    # Search top 3 matches
    distances, indices = faiss_index.search(query_embedding, k=3)

    results = [stored_chunks[i] for i in indices[0]]

    return Response(
        {
            "query": query,
            "results": results
        },
        status=status.HTTP_200_OK
    )


# =====================================================
# Existing PDF APIs
# =====================================================

@api_view(['POST'])
def pdf_length(request):
    pdf_file = validate_pdf(request)
    if not pdf_file:
        return Response(
            {"error": "Please upload a valid PDF"},
            status=status.HTTP_400_BAD_REQUEST
        )

    reader = PdfReader(pdf_file)
    return Response(
        {"total_pages": len(reader.pages)},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def metadata(request):
    pdf_file = validate_pdf(request)
    if not pdf_file:
        return Response(
            {"error": "Please upload a valid PDF"},
            status=status.HTTP_400_BAD_REQUEST
        )

    reader = PdfReader(pdf_file)
    return Response(
        {"metadata": reader.metadata},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def readdata(request):
    pdf_file = validate_pdf(request)
    if not pdf_file:
        return Response(
            {"error": "Please upload a valid PDF"},
            status=status.HTTP_400_BAD_REQUEST
        )

    text = read_pdf(pdf_file)
    chunks = chunk_text(text)

    return Response(
        {
            "total_characters": len(text),
            "total_chunks": len(chunks),
            "sample_chunk": chunks[0] if chunks else ""
        },
        status=status.HTTP_200_OK
    )
