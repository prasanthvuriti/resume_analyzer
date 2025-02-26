import os
import nltk
import traceback
from nltk.tokenize import word_tokenize
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import JobDescription, Resume
import PyPDF2
import docx

# Download necessary NLTK data (Only downloads once)

# Set file size limit (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += (page.extract_text() or "") + " "
    except Exception as e:
        text = f"Error reading PDF: {str(e)}"
    return text.strip() or "No readable text found in PDF."

def extract_text_from_docx(docx_path):
    text = []
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text.append(para.text)
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
    return " ".join(text)


import logging

# Configure logging
logger = logging.getLogger(__name__)

def analyze_resume(request):
    """Handles resume upload and comparison with job descriptions."""
    try:
        if request.method == "POST":
            # Ensure a resume file is uploaded
            if "resume" not in request.FILES or not request.FILES["resume"]:
                return render(request, "upload.html", {"error_message": "Please select a resume file to upload."})

            uploaded_file = request.FILES["resume"]

            # Validate file size
            if uploaded_file.size > MAX_FILE_SIZE:
                return render(request, "error.html", {"message": "File size exceeds 5MB limit."})

            # Save file temporarily in media/resumes/
            fs = FileSystemStorage(location="media/resumes/")
            file_path = fs.save(uploaded_file.name, uploaded_file)
            file_full_path = fs.path(file_path)

            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(file_full_path)
            elif uploaded_file.name.endswith(".docx"):
                resume_text = extract_text_from_docx(file_full_path)
            else:
                fs.delete(file_path)
                file_extension = uploaded_file.name.split('.')[-1]  # Extract file extension
                error_message = f"Unsupported file format: .{file_extension.upper()}. Please upload a PDF or DOCX file."
                return render(request, "error.html", {"message": error_message})


            # Retrieve job descriptions from database
            job_descriptions = JobDescription.objects.all()
            if not job_descriptions.exists():
                return render(request, "upload.html", {"error_message": "No job descriptions available. Please add one."})

            # Analyze Resume vs. Job Descriptions
            suggestions = []
            resume_tokens = set(word_tokenize(resume_text.lower()))

            for job in job_descriptions:
                job_tokens = set(word_tokenize(job.description.lower()))
                matched_words = job_tokens & resume_tokens
                match_percentage = (len(matched_words) / len(job_tokens)) * 100 if job_tokens else 0
                missing_skills = list(job_tokens - resume_tokens)[:10]

                suggestions.append({
                    "job_title": job.title,
                    "match_percentage": round(match_percentage, 2),
                    "missing_skills": missing_skills
                })

            fs.delete(file_path)  # Delete resume after processing

            return render(request, "result.html", {"suggestions": suggestions})

        return render(request, "upload.html")

    except Exception as e:
        logger.error("Error processing resume", exc_info=True)  # Log errors instead of printing them
        return render(request, "error.html", {"message": "An error occurred while processing the resume."})


# Resume Upload Page
def upload_resume(request):
    return render(request, "upload.html")

# Homepage
def home(request):
    return render(request, "Resume_Analyzer.html")  # Ensure correct filename
