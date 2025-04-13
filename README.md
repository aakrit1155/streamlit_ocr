# 📄 Streamlit OCR Application

This is a simple OCR (Optical Character Recognition) application built using **Streamlit**, **Tesseract OCR**, and **pdf2image**. The app allows users to upload images or PDF files and extracts text from them using OCR.

---

## 🚀 Features

- Extract text from **images** (PNG, JPG, BMP, TIFF).
- Extract text from **PDFs** (scanned or image-based).
- Preprocessing pipeline to enhance OCR accuracy.
- User-friendly interface with progress indicators.

---

## 🛠️ Prerequisites

Before running the project locally, ensure you have the following installed:

1. **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2. **Tesseract OCR**:
   - **Windows**: [Download Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
   - **Linux**: Install via package manager (e.g., `sudo apt install tesseract-ocr`)
   - **Mac**: Install via Homebrew (`brew install tesseract`)
3. **Poppler** (for PDF processing):
   - **Windows**: [Download Poppler](http://blog.alivate.com.au/poppler-windows/)
   - **Linux**: Install via package manager (e.g., `sudo apt install poppler-utils`)
   - **Mac**: Install via Homebrew (`brew install poppler`)

---

## 📦 Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aakrit1155/streamlit_ocr.git
   cd streamlit-ocr-app
