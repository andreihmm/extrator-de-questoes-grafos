from typing import List
import re
import PyPDF2


def extrair_texto_pdf(pdf_file: str) -> str:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            if content:
                content = content.replace('\t', ' ')
                content = content.strip()
                textosEntreAsteriscos = r'\*.*?\*'
                content = re.sub(textosEntreAsteriscos, '', content)
                pdf_text.append(content)
        
        full_text = '\n\n'.join(pdf_text)

        full_text = re.sub(
            r'(\d{1,3}\s*Direito)(?=\s*[A-Z])',
            r'\1\n\n',
            full_text
        )
        return full_text
