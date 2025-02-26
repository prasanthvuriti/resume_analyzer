from django.db import models

class JobDescription(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Resume(models.Model):
    file = models.FileField(upload_to="resumes/", verbose_name="Resume File", help_text="Upload a PDF or DOCX file.")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis_result = models.TextField(blank=True, null=True, help_text="Stores resume analysis results.")  # Store analysis results

    def __str__(self):
        return self.file.name