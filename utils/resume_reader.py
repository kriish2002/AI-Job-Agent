import os
from pypdf import PdfReader


class ResumeReader:

    def __init__(self, file_path="resume.pdf"):
        self.file_path = file_path

    def read(self):

        if not os.path.exists(self.file_path):
            print("❌ Resume file not found")
            return ""

        try:

            reader = PdfReader(self.file_path)

            resume_text = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    resume_text += text + "\n"

            print(
                f"📄 Resume Loaded : "
                f"{len(resume_text)} characters"
            )

            return resume_text

        except Exception as e:

            print(f"❌ Resume Read Error : {e}")
            return ""