import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes # To handle PDF files
import io # To handle byte streams
import os # To potentially check for Tesseract path if needed locally

# --- Configuration (Optional: Set Tesseract path if needed locally) ---
# On Streamlit Community Cloud, Tesseract should be discoverable if installed via packages.txt
# If running locally and Tesseract is not in your PATH, you might need to set this.
# Check common paths or where you installed it. Leave commented out for cloud deployment.
# Example paths:
# tesseract_path_linux = "/usr/bin/tesseract"
# tesseract_path_windows = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# if os.path.exists(tesseract_path_windows):
#     pytesseract.pytesseract.tesseract_cmd = tesseract_path_windows
# elif os.path.exists(tesseract_path_linux):
#      pytesseract.pytesseract.tesseract_cmd = tesseract_path_linux
# else:
#      # If not found in common paths, Streamlit will rely on PATH or packages.txt
#      pass


# --- Helper Functions ---

def perform_ocr_on_image(image_obj):
    """
    Performs OCR on a single PIL Image object.

    Args:
        image_obj (PIL.Image.Image): The image to process.

    Returns:
        str: The extracted text, or None if an error occurred.
    """
    try:
        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(image_obj)
        return text
    except pytesseract.TesseractNotFoundError:
        st.error(
            "Tesseract executable not found. \n"
            "**For Cloud Deployment:** Ensure 'tesseract-ocr' is in your packages.txt.\n"
            "**For Local Use:** Ensure Tesseract is installed and in your system's PATH, "
            "or set the path manually in the script."
            )
        return None
    except Exception as e:
        st.error(f"An error occurred during OCR processing: {e}")
        return None

def perform_ocr_on_pdf(pdf_bytes):
    """
    Converts PDF bytes to images and performs OCR on each page.

    Args:
        pdf_bytes (bytes): The byte content of the PDF file.

    Returns:
        str: The concatenated extracted text from all pages, or None if an error occurred.
    """
    extracted_text = ""
    try:
        # Convert PDF bytes to a list of PIL Image objects
        # poppler_path=None relies on poppler being in PATH or installed via packages.txt
        # On Streamlit Cloud, poppler-utils installed via packages.txt handles this.
        images = convert_from_bytes(pdf_bytes, poppler_path=None)

        if not images:
            st.warning("Could not extract any images from the PDF. The PDF might be empty, corrupted, or text-based (not scanned).")
            return None # Return None instead of empty string if no images found

        # Process each page (image)
        total_pages = len(images)
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, image in enumerate(images):
            page_num = i + 1
            status_text.text(f"Processing Page {page_num}/{total_pages}...")
            # Perform OCR on the image
            page_text = perform_ocr_on_image(image)
            if page_text: # Append text only if OCR was successful for the page
                extracted_text += f"--- Page {page_num} ---\n{page_text}\n\n"
            else:
                # Optionally note if a page failed OCR, or just skip
                extracted_text += f"--- Page {page_num} (OCR Failed or No Text Detected) ---\n\n"
            # Update progress bar
            progress_bar.progress((i + 1) / total_pages)

        status_text.text("PDF Processing Complete.")
        return extracted_text

    except ImportError:
         st.error("The 'pdf2image' or 'PIL' library is not installed. Please check your requirements.txt.")
         return None
    # Catch errors specifically related to pdf2image/poppler
    except (pdf2image.exceptions.PDFInfoNotInstalledError,
            pdf2image.exceptions.PDFPageCountError,
            pdf2image.exceptions.PDFSyntaxError,
            FileNotFoundError) as e: # FileNotFoundError can occur if poppler isn't found
         st.error(
             f"Error converting PDF to images: {e}\n"
             "**For Cloud Deployment:** Ensure 'poppler-utils' is in your packages.txt.\n"
             "**For Local Use:** Ensure Poppler is installed and in your system's PATH."
             )
         return None
    except Exception as e:
        st.error(f"An unexpected error occurred during PDF processing: {e}")
        return None

# --- Streamlit App UI ---

st.set_page_config(page_title="Simple OCR App", layout="wide")

st.title("📄 Simple OCR Application")
st.markdown("Upload an **Image** (PNG, JPG, BMP, TIFF) or a **PDF** file to extract text using Tesseract OCR.")

# 1. Choose file type
file_type = st.radio(
    "Select the type of file to upload:",
    ('Image', 'PDF'),
    horizontal=True,
    key='file_type_selection'
)

# 2. File Uploader - appears based on selection
uploaded_file = None
if file_type == 'Image':
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["png", "jpg", "jpeg", "bmp", "tiff"],
        key='image_uploader_widget'
    )
elif file_type == 'PDF':
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        key='pdf_uploader_widget'
    )

# 3. Process Button and Output Logic
if uploaded_file is not None:
    # Show a button to trigger processing
    if st.button(f"Process {file_type}", key='process_file_button'):
        extracted_text = None
        # Show spinner during processing
        with st.spinner(f'Processing {file_type}... This may take a moment.'):
            try:
                # Read the file bytes
                file_bytes = uploaded_file.getvalue()

                if file_type == 'Image':
                    # Convert image bytes to PIL Image object
                    image = Image.open(io.BytesIO(file_bytes))
                    # Display the uploaded image (optional, good for confirmation)
                    st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)
                    # Perform OCR
                    extracted_text = perform_ocr_on_image(image)

                elif file_type == 'PDF':
                    # Perform OCR on the PDF bytes
                    extracted_text = perform_ocr_on_pdf(file_bytes)

            except Exception as e:
                st.error(f"An error occurred before OCR could start: {e}")

        # Display the results
        if extracted_text is not None:
            st.subheader("Extracted Text:")
            st.text_area("Result", extracted_text, height=400, key='ocr_result_text_area')
        elif extracted_text == "": # Handle case where OCR ran but found nothing
             st.warning("OCR processing complete, but no text was detected in the file.")
        # If extracted_text is None, error messages were already shown by helper functions

else:
    st.info("Upload a file using the options above to enable processing.")

# --- Footer ---
st.markdown("---")
st.markdown("Powered by [Streamlit](https://streamlit.io/), [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), [pdf2image](https://github.com/Belval/pdf2image)")

