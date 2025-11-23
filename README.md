# Rasterbator-style landing page

This repository contains a single Python script that serves a Rasterbator-inspired landing page and a working Rasterbator-style PDF generator.

The only dependency is Pillow for image processing:

```bash
pip install pillow
```

## Running the page

1. Start the server:
   ```bash
   python app.py
   ```
2. Open your browser to http://localhost:8000 to view the page.

## Creating a multi-page poster

1. Open the site and scroll to the "Try it now" section.
2. Upload a PNG or JPG image.
3. Choose how many columns and rows of paper you want, adjust page size (A4 or Letter), orientation, DPI, and margin.
4. Submit the form to download a ready-to-print multi-page PDF with one sheet per page.

Press `Ctrl+C` to stop the server.
