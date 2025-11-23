from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from textwrap import dedent
from email import policy
from email.parser import BytesParser

HOST = "localhost"
PORT = 8000


def parse_multipart_form(body: bytes, content_type: str):
    """Parse a multipart/form-data body into fields and files.

    Returns a tuple of (fields, files) where `fields` maps field names to text
    values and `files` maps field names to a dict containing filename and
    content bytes.
    """

    # Prefix with a synthetic header block so BytesParser can understand the
    # multipart payload.
    parser = BytesParser(policy=policy.default)
    message = parser.parsebytes(f"Content-Type: {content_type}\r\n\r\n".encode() + body)

    fields = {}
    files = {}

    for part in message.iter_parts():
        if part.get_content_disposition() != "form-data":
            continue

        name = part.get_param("name", header="content-disposition")
        filename = part.get_param("filename", header="content-disposition")

        if filename:
            files[name] = {"filename": filename, "content": part.get_payload(decode=True)}
        else:
            fields[name] = part.get_content()

    return fields, files


def build_page() -> str:
    """Return the HTML content for the Rasterbator-style landing page."""
    return dedent(
        """
        <!DOCTYPE html>
        <html lang=\"en\">
        <head>
            <meta charset=\"UTF-8\" />
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
            <title>Rasterbator Reimagined</title>
            <style>
                :root {
                    color-scheme: light dark;
                    --accent: #ff2c55;
                    --bg: #0d0d0f;
                    --panel: #151519;
                    --text: #e9e9ed;
                    --muted: #b6b7be;
                    --card: #1f1f24;
                }
                * { box-sizing: border-box; }
                body {
                    margin: 0;
                    font-family: \"Inter\", system-ui, -apple-system, sans-serif;
                    background: radial-gradient(circle at 20% 20%, rgba(255,44,85,0.18), transparent 30%),
                                radial-gradient(circle at 80% 0%, rgba(85,100,255,0.14), transparent 25%),
                                var(--bg);
                    color: var(--text);
                }
                header {
                    position: sticky;
                    top: 0;
                    backdrop-filter: blur(12px);
                    background: rgba(13,13,15,0.75);
                    border-bottom: 1px solid #262631;
                    z-index: 10;
                }
                .nav {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    max-width: 1100px;
                    margin: 0 auto;
                    padding: 14px 20px;
                }
                .brand {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    font-weight: 700;
                    letter-spacing: 0.4px;
                }
                .brand span {
                    color: var(--accent);
                }
                .nav-links {
                    display: flex;
                    gap: 18px;
                    color: var(--muted);
                    font-size: 14px;
                }
                .nav-links a { color: inherit; text-decoration: none; }
                .hero {
                    max-width: 1100px;
                    margin: 60px auto;
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                    gap: 32px;
                    padding: 0 20px;
                    align-items: center;
                }
                .hero-card {
                    background: linear-gradient(145deg, rgba(31,31,36,0.8), rgba(27,27,31,0.7));
                    border: 1px solid #242632;
                    border-radius: 18px;
                    padding: 28px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
                }
                .hero h1 {
                    font-size: clamp(34px, 5vw, 52px);
                    margin: 0 0 16px;
                }
                .hero p {
                    color: var(--muted);
                    font-size: 16px;
                    line-height: 1.6;
                }
                .cta-buttons {
                    display: flex;
                    gap: 12px;
                    margin-top: 18px;
                    flex-wrap: wrap;
                }
                .btn {
                    padding: 12px 18px;
                    border-radius: 10px;
                    border: 1px solid transparent;
                    cursor: pointer;
                    font-weight: 700;
                    text-decoration: none;
                    transition: transform 120ms ease, box-shadow 120ms ease;
                }
                .btn:hover { transform: translateY(-1px); }
                .btn-primary {
                    background: var(--accent);
                    color: #fff;
                    box-shadow: 0 10px 30px rgba(255,44,85,0.35);
                }
                .btn-secondary {
                    background: #1f1f24;
                    color: var(--text);
                    border-color: #2c2c35;
                }
                .hero-visual {
                    background: radial-gradient(circle at 30% 20%, rgba(255,44,85,0.2), transparent 45%),
                                radial-gradient(circle at 80% 0%, rgba(85,100,255,0.2), transparent 35%),
                                var(--card);
                    border: 1px solid #272733;
                    border-radius: 16px;
                    padding: 24px;
                    position: relative;
                    overflow: hidden;
                    min-height: 320px;
                }
                .hero-visual .grid {
                    display: grid;
                    grid-template-columns: repeat(6, 1fr);
                    gap: 6px;
                }
                .hero-visual .cell {
                    padding-top: 100%;
                    border-radius: 6px;
                    position: relative;
                    overflow: hidden;
                    background: linear-gradient(135deg, rgba(255,44,85,0.7), rgba(85,100,255,0.7));
                }
                .hero-visual .cell::after {
                    content: \"\";
                    position: absolute;
                    inset: 0;
                    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.6), transparent 45%);
                }
                .hero-visual .badge {
                    position: absolute;
                    bottom: 16px;
                    right: 16px;
                    background: rgba(12,12,15,0.8);
                    border: 1px solid #31313d;
                    padding: 10px 14px;
                    border-radius: 10px;
                    font-size: 14px;
                    color: var(--muted);
                }
                section {
                    max-width: 1100px;
                    margin: 0 auto 60px;
                    padding: 0 20px;
                }
                .live-preview {
                    background: linear-gradient(145deg, rgba(31,31,36,0.7), rgba(27,27,31,0.6));
                    border: 1px dashed #2c2c35;
                }
                .preview-box {
                    position: relative;
                    width: 100%;
                    aspect-ratio: 3 / 2;
                    min-height: 260px;
                    display: grid;
                    place-items: stretch;
                    background: radial-gradient(circle at 40% 30%, rgba(255,44,85,0.12), transparent 45%),
                                radial-gradient(circle at 70% 70%, rgba(85,100,255,0.1), transparent 40%),
                                #0e0e13;
                    border: 1px solid #262631;
                    border-radius: 12px;
                    overflow: hidden;
                }
                .preview-box canvas {
                    width: 100%;
                    height: 100%;
                    display: block;
                    position: absolute;
                    inset: 0;
                }
                .preview-placeholder {
                    position: absolute;
                    inset: 0;
                    display: grid;
                    place-items: center;
                    color: var(--muted);
                    font-size: 15px;
                    letter-spacing: 0.3px;
                    background: linear-gradient(145deg, rgba(31,31,36,0.4), rgba(27,27,31,0.3));
                    z-index: 1;
                }
                .preview-meta {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 10px;
                    font-size: 14px;
                    color: var(--muted);
                    margin-top: 10px;
                }
                .preview-meta strong { color: var(--text); }
                .preview-note {
                    color: var(--muted);
                    font-size: 13px;
                    margin-top: 12px;
                    line-height: 1.4;
                }
                .section-title {
                    display: flex;
                    align-items: baseline;
                    gap: 10px;
                    margin-bottom: 22px;
                }
                .section-title span { color: var(--accent); font-weight: 700; }
                .feature-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                    gap: 18px;
                }
                .card {
                    background: var(--card);
                    border: 1px solid #242632;
                    border-radius: 14px;
                    padding: 18px;
                    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
                }
                .card h3 { margin-top: 0; margin-bottom: 10px; }
                .card p { color: var(--muted); line-height: 1.5; }
                .steps {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 16px;
                }
                .step-number {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 32px;
                    height: 32px;
                    border-radius: 10px;
                    background: rgba(255,44,85,0.12);
                    color: var(--accent);
                    font-weight: 800;
                    margin-bottom: 10px;
                }
                .faq {
                    display: grid;
                    gap: 12px;
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                }
                .faq-item {
                    background: #17171c;
                    border: 1px solid #242632;
                    border-radius: 12px;
                    padding: 16px;
                }
                footer {
                    padding: 24px 20px 60px;
                    text-align: center;
                    color: var(--muted);
                }
                @media (max-width: 640px) {
                    .nav-links { display: none; }
                    .hero { margin-top: 30px; }
                }
            </style>
        </head>
        <body>
            <header>
                <div class=\"nav\">
                    <div class=\"brand\">
                        <svg width=\"28\" height=\"28\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">
                            <circle cx=\"12\" cy=\"12\" r=\"10\" stroke=\"var(--accent)\" stroke-width=\"2\" />
                            <path d=\"M12 4V12L17 15\" stroke=\"var(--accent)\" stroke-width=\"2\" stroke-linecap=\"round\" />
                        </svg>
                        <span>Rasterbator</span> Reimagined
                    </div>
                    <div class=\"nav-links\">
                        <a href=\"#how\">How it works</a>
                        <a href=\"#features\">Features</a>
                        <a href=\"#faq\">FAQ</a>
                    </div>
                </div>
            </header>

            <div class=\"hero\">
                <div class=\"hero-card\">
                    <div class=\"pill\" style=\"color: var(--muted); letter-spacing: 1px; font-weight: 700; font-size: 13px;\">CREATE. PRINT. AMAZE.</div>
                    <h1>Turn any image into massive wall art.</h1>
                    <p>Upload an image, choose your paper size and margins, and generate a ready-to-print PDF that transforms your photo into multi-page poster mosaics.</p>
                    <div class=\"cta-buttons\">
                        <a class=\"btn btn-primary\" href=\"#rasterbate\">Rasterbate an image</a>
                        <a class=\"btn btn-secondary\" href=\"#features\">See how it works</a>
                    </div>
                    <p style=\"margin-top: 16px; color: var(--muted);\">100% free • No install required • Works in your browser</p>
                </div>
                <div class=\"hero-visual\" aria-hidden=\"true\">
                    <div class=\"grid\">
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                        <div class=\"cell\"></div>
                    </div>
                    <div class=\"badge\">Poster size: 5x4 A4 sheets</div>
                </div>
            </div>

            <section id=\"rasterbate\" style=\"margin-top: 20px;\">
                <div class=\"section-title\"><span>Try it now</span><h2>Create a multi-page PDF from your image</h2></div>
                <div class=\"card\" style=\"display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; align-items: start;\">
                    <div>
                        <form id=\"raster-form\" action=\"/rasterbate\" method=\"post\" enctype=\"multipart/form-data\" target=\"_blank\" style=\"display: grid; gap: 12px;\">
                            <label style=\"display: grid; gap: 6px; font-weight: 600;\">
                                Select image (PNG/JPG)
                                <input required type=\"file\" name=\"image\" accept=\"image/png, image/jpeg\" style=\"padding: 10px; border-radius: 10px; border: 1px solid #2c2c35; background: #111118;\" />
                            </label>
                            <div style=\"display: grid; gap: 10px; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));\">
                                <label style=\"display: grid; gap: 6px; font-weight: 600;\">
                                    Columns
                                    <input required type=\"number\" name=\"columns\" value=\"3\" min=\"1\" max=\"10\" style=\"padding: 10px; border-radius: 10px; border: 1px solid #2c2c35; background: #111118; color: var(--text);\" />
                                </label>
                                <label style=\"display: grid; gap: 6px; font-weight: 600;\">
                                    Rows
                                    <input required type=\"number\" name=\"rows\" value=\"3\" min=\"1\" max=\"10\" style=\"padding: 10px; border-radius: 10px; border: 1px solid #2c2c35; background: #111118; color: var(--text);\" />
                                </label>
                                <label style=\"display: grid; gap: 6px; font-weight: 600;\">
                                    Margin (mm)
                                    <input type=\"number\" step=\"1\" name=\"margin\" value=\"10\" min=\"0\" max=\"40\" style=\"padding: 10px; border-radius: 10px; border: 1px solid #2c2c35; background: #111118; color: var(--text);\" />
                                </label>
                                <label style=\"display: grid; gap: 6px; font-weight: 600;\">
                                    DPI
                                    <input type=\"number\" step=\"50\" name=\"dpi\" value=\"300\" min=\"150\" max=\"600\" style=\"padding: 10px; border-radius: 10px; border: 1px solid #2c2c35; background: #111118; color: var(--text);\" />
                                </label>
                            </div>
                            <label style=\"display: grid; gap: 6px; font-weight: 600;\">
                                Page size
                                <select name=\"page_size\" style=\"padding: 10px; border-radius: 10px; border: 1px solid #2c2c35; background: #111118; color: var(--text);\">
                                    <option value=\"A4\" selected>A4 (210 x 297 mm)</option>
                                    <option value=\"Letter\">Letter (8.5 x 11 in)</option>
                                </select>
                            </label>
                            <label style=\"display: grid; gap: 6px; font-weight: 600;\">
                                Orientation
                                <select name=\"orientation\" style=\"padding: 10px; border-radius: 10px; border: 1px solid #2c2c35; background: #111118; color: var(--text);\">
                                    <option value=\"portrait\" selected>Portrait</option>
                                    <option value=\"landscape\">Landscape</option>
                                </select>
                            </label>
                            <p style=\"color: var(--muted); font-size: 14px; margin: 0;\">Submit to download a ready-to-print PDF. Each sheet will be a separate page in the PDF.</p>
                            <button class=\"btn btn-primary\" type=\"submit\">Generate PDF</button>
                        </form>
                    </div>
                    <div class=\"card live-preview\">
                        <h3 style=\"margin-top: 0;\">Live preview</h3>
                        <p class=\"preview-note\">See exactly how your image will split across pages. The grid updates instantly when you change columns, rows, margins, orientation, or page size.</p>
                        <div id=\"preview-box\" class=\"preview-box\">
                            <canvas id=\"preview-canvas\" aria-label=\"Poster grid preview\"></canvas>
                            <div id=\"preview-placeholder\" class=\"preview-placeholder\">Upload an image to preview the cuts</div>
                        </div>
                        <div class=\"preview-meta\">
                            <span id=\"grid-label\"><strong>Grid</strong>: 3 × 3</span>
                            <span id=\"page-label\">A4 portrait • 10 mm margin</span>
                        </div>
                    </div>
                </div>
            </section>

            <section id=\"how\">
                <div class=\"section-title\"><span>How it works</span><h2>From image to poster in minutes</h2></div>
                <div class=\"steps\">
                    <div class=\"card\">
                        <div class=\"step-number\">1</div>
                        <h3>Upload your image</h3>
                        <p>Select a PNG, JPG, or GIF—high-resolution photos give the best results.</p>
                    </div>
                    <div class=\"card\">
                        <div class=\"step-number\">2</div>
                        <h3>Choose layout</h3>
                        <p>Pick portrait or landscape, set paper size, and adjust margins to match your printer.</p>
                    </div>
                    <div class=\"card\">
                        <div class=\"step-number\">3</div>
                        <h3>Generate PDF</h3>
                        <p>Download a tiled PDF that splits the image into perfectly aligned pages.</p>
                    </div>
                </div>
            </section>

            <section id=\"features\">
                <div class=\"section-title\"><span>Features</span><h2>Precise controls for perfect posters</h2></div>
                <div class=\"feature-grid\">
                    <div class=\"card\">
                        <h3>Smart resizing</h3>
                        <p>Scale your image to any wall size while keeping crisp detail and balanced margins.</p>
                    </div>
                    <div class=\"card\">
                        <h3>Pixel, line, or dot styles</h3>
                        <p>Experiment with classic halftone dots, grid-based pixels, or minimalist line art.</p>
                    </div>
                    <div class=\"card\">
                        <h3>Color or monochrome</h3>
                        <p>Switch between vibrant color output and high-contrast black-and-white looks.</p>
                    </div>
                    <div class=\"card\">
                        <h3>Instant previews</h3>
                        <p>Review your poster layout before you print so you know exactly what you'll get.</p>
                    </div>
                </div>
            </section>

            <section>
                <div class=\"section-title\"><span>Why people love it</span><h2>Make a statement on any wall</h2></div>
                <div class=\"feature-grid\">
                    <div class=\"card\">
                        <h3>Budget friendly</h3>
                        <p>Create oversized art with regular home printers and everyday paper.</p>
                    </div>
                    <div class=\"card\">
                        <h3>Anyone can do it</h3>
                        <p>No design degree needed—just pick an image and follow the prompts.</p>
                    </div>
                    <div class=\"card\">
                        <h3>Perfect alignment</h3>
                        <p>Built-in margins and print guides make taping panels together painless.</p>
                    </div>
                </div>
            </section>

            <section id=\"faq\">
                <div class=\"section-title\"><span>FAQ</span><h2>Common questions</h2></div>
                <div class=\"faq\">
                    <div class=\"faq-item\">
                        <h3>Do I need to install anything?</h3>
                        <p>No, the experience is entirely browser-based. Generate your PDF online and print locally.</p>
                    </div>
                    <div class=\"faq-item\">
                        <h3>What paper sizes are supported?</h3>
                        <p>Works great with A4, A3, Letter, Legal, and Tabloid. Custom sizes are supported, too.</p>
                    </div>
                    <div class=\"faq-item\">
                        <h3>Does it handle very large images?</h3>
                        <p>High-resolution images are recommended. The generator automatically scales to fit the chosen layout.</p>
                    </div>
                    <div class=\"faq-item\">
                        <h3>Is there a watermark?</h3>
                        <p>No watermarks are added. Your finished PDF is clean and ready to print or share.</p>
                    </div>
                </div>
            </section>

            <footer>
                Crafted in Python to showcase a Rasterbator-inspired layout. Enjoy turning your photos into striking wall posters.
            </footer>
            <script>
                (() => {
                    const form = document.getElementById("raster-form");
                    const fileInput = form.querySelector('input[name="image"]');
                    const columnsInput = form.querySelector('input[name="columns"]');
                    const rowsInput = form.querySelector('input[name="rows"]');
                    const marginInput = form.querySelector('input[name="margin"]');
                    const dpiInput = form.querySelector('input[name="dpi"]');
                    const pageSizeSelect = form.querySelector('select[name="page_size"]');
                    const orientationSelect = form.querySelector('select[name="orientation"]');
                    const previewCanvas = document.getElementById("preview-canvas");
                    const previewBox = document.getElementById("preview-box");
                    const placeholder = document.getElementById("preview-placeholder");
                    const gridLabel = document.getElementById("grid-label");
                    const pageLabel = document.getElementById("page-label");

                    const PAGE_SIZES = {
                        A4: [210, 297],
                        Letter: [215.9, 279.4],
                    };

                    let loadedImage = null;

                    function clampNumber(value, fallback, min = 1) {
                        const num = Number.parseFloat(value);
                        if (Number.isNaN(num)) return fallback;
                        return Math.max(min, num);
                    }

                    function updateLabels(columns, rows, pageSize, orientation, margin, dpi, footprintCols, footprintRows) {
                        gridLabel.textContent = `Grid: ${columns} × ${rows}`;
                        const footprint = `${footprintCols.toFixed(1)} × ${footprintRows.toFixed(1)} pages at ${dpi} DPI`;
                        pageLabel.textContent = `${pageSize} ${orientation} • ${margin} mm margin • ${footprint}`;
                    }

                    function renderPreview() {
                        const columns = clampNumber(columnsInput.value, 3);
                        const rows = clampNumber(rowsInput.value, 3);
                        const margin = Math.max(0, Number.parseFloat(marginInput.value) || 0);
                        const dpi = clampNumber(dpiInput.value, 300, 72);
                        const pageSize = pageSizeSelect.value in PAGE_SIZES ? pageSizeSelect.value : "A4";
                        const orientation = orientationSelect.value === "landscape" ? "landscape" : "portrait";

                        const size = PAGE_SIZES[pageSize];
                        let [pageW, pageH] = size;
                        if (orientation === "landscape") {
                            [pageW, pageH] = [pageH, pageW];
                        }

                        const tileW = pageW - margin * 2;
                        const tileH = pageH - margin * 2;

                        if (tileW <= 0 || tileH <= 0 || !loadedImage) {
                            const ctx = previewCanvas.getContext("2d");
                            const boxRect = previewBox.getBoundingClientRect();
                            if (!boxRect.width || !boxRect.height) {
                                requestAnimationFrame(renderPreview);
                                return;
                            }
                            previewCanvas.width = boxRect.width;
                            previewCanvas.height = boxRect.height;
                            ctx.clearRect(0, 0, previewCanvas.width, previewCanvas.height);
                            placeholder.style.display = "grid";
                            placeholder.textContent = "Upload an image to preview the cuts";
                            return;
                        }

                        const targetWpx = tileW * columns * (dpi / 25.4);
                        const targetHpx = tileH * rows * (dpi / 25.4);
                        const cropWpx = Math.min(loadedImage.width, targetWpx);
                        const cropHpx = Math.min(loadedImage.height, targetHpx);
                        const footprintCols = cropWpx / (tileW * (dpi / 25.4));
                        const footprintRows = cropHpx / (tileH * (dpi / 25.4));
                        updateLabels(columns, rows, pageSize, orientation, margin, dpi, footprintCols, footprintRows);

                        const totalW = pageW * columns;
                        const totalH = pageH * rows;
                        previewBox.style.aspectRatio = `${totalW} / ${totalH}`;

                        const boxRect = previewBox.getBoundingClientRect();
                        if (!boxRect.width || !boxRect.height) {
                            requestAnimationFrame(renderPreview);
                            return;
                        }
                        const dpr = window.devicePixelRatio || 1;
                        previewCanvas.width = boxRect.width * dpr;
                        previewCanvas.height = boxRect.height * dpr;

                        const ctx = previewCanvas.getContext("2d");
                        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
                        ctx.clearRect(0, 0, boxRect.width, boxRect.height);

                        placeholder.style.display = "none";

                        const scaleToBox = Math.min(boxRect.width / totalW, boxRect.height / totalH);
                        const mosaicW = totalW * scaleToBox;
                        const mosaicH = totalH * scaleToBox;
                        const offsetX = (boxRect.width - mosaicW) / 2;
                        const offsetY = (boxRect.height - mosaicH) / 2;

                        ctx.fillStyle = "#0f0f15";
                        ctx.fillRect(offsetX - 12, offsetY - 12, mosaicW + 24, mosaicH + 24);

                        const cropLeftPx = Math.max(0, (loadedImage.width - cropWpx) / 2);
                        const cropTopPx = Math.max(0, (loadedImage.height - cropHpx) / 2);
                        const artOffsetWmm = ((tileW * columns) - (cropWpx / (dpi / 25.4))) / 2;
                        const artOffsetHmm = ((tileH * rows) - (cropHpx / (dpi / 25.4))) / 2;

                        for (let row = 0; row < rows; row += 1) {
                            for (let col = 0; col < columns; col += 1) {
                                const pageX = offsetX + col * pageW * scaleToBox;
                                const pageY = offsetY + row * pageH * scaleToBox;
                                const tileX = pageX + margin * scaleToBox;
                                const tileY = pageY + margin * scaleToBox;
                                const tileDisplayW = tileW * scaleToBox;
                                const tileDisplayH = tileH * scaleToBox;

                                ctx.fillStyle = "#181822";
                                ctx.fillRect(pageX, pageY, pageW * scaleToBox, pageH * scaleToBox);

                                const imageStartXmm = artOffsetWmm + col * tileW + margin - margin;
                                const imageStartYmm = artOffsetHmm + row * tileH + margin - margin;
                                const imageEndXmm = imageStartXmm + (cropWpx / (dpi / 25.4));
                                const imageEndYmm = imageStartYmm + (cropHpx / (dpi / 25.4));

                                const tileStartXmm = col * pageW + margin;
                                const tileStartYmm = row * pageH + margin;
                                const tileEndXmm = tileStartXmm + tileW;
                                const tileEndYmm = tileStartYmm + tileH;

                                const drawStartXmm = Math.max(tileStartXmm, imageStartXmm);
                                const drawStartYmm = Math.max(tileStartYmm, imageStartYmm);
                                const drawEndXmm = Math.min(tileEndXmm, imageEndXmm);
                                const drawEndYmm = Math.min(tileEndYmm, imageEndYmm);

                                if (drawEndXmm > drawStartXmm && drawEndYmm > drawStartYmm) {
                                    const srcX = cropLeftPx + ((drawStartXmm - imageStartXmm) / (cropWpx / (dpi / 25.4))) * cropWpx;
                                    const srcY = cropTopPx + ((drawStartYmm - imageStartYmm) / (cropHpx / (dpi / 25.4))) * cropHpx;
                                    const srcW = ((drawEndXmm - drawStartXmm) / (cropWpx / (dpi / 25.4))) * cropWpx;
                                    const srcH = ((drawEndYmm - drawStartYmm) / (cropHpx / (dpi / 25.4))) * cropHpx;

                                    ctx.drawImage(
                                        loadedImage,
                                        srcX,
                                        srcY,
                                        srcW,
                                        srcH,
                                        offsetX + (drawStartXmm) * scaleToBox,
                                        offsetY + (drawStartYmm) * scaleToBox,
                                        (drawEndXmm - drawStartXmm) * scaleToBox,
                                        (drawEndYmm - drawStartYmm) * scaleToBox,
                                    );
                                }

                                ctx.strokeStyle = "rgba(255,255,255,0.22)";
                                ctx.lineWidth = 1.5;
                                ctx.setLineDash([6, 6]);
                                ctx.strokeRect(pageX, pageY, pageW * scaleToBox, pageH * scaleToBox);
                                ctx.setLineDash([]);
                            }
                        }

                        ctx.strokeStyle = "rgba(255, 44, 85, 0.5)";
                        ctx.lineWidth = 2;
                        for (let c = 1; c < columns; c += 1) {
                            const x = offsetX + c * pageW * scaleToBox;
                            ctx.beginPath();
                            ctx.moveTo(x, offsetY);
                            ctx.lineTo(x, offsetY + mosaicH);
                            ctx.stroke();
                        }
                        for (let r = 1; r < rows; r += 1) {
                            const y = offsetY + r * pageH * scaleToBox;
                            ctx.beginPath();
                            ctx.moveTo(offsetX, y);
                            ctx.lineTo(offsetX + mosaicW, y);
                            ctx.stroke();
                        }
                    }

                    fileInput.addEventListener("change", () => {
                        const [file] = fileInput.files || [];
                        if (!file) {
                            loadedImage = null;
                            renderPreview();
                            return;
                        }

                        placeholder.style.display = "grid";
                        placeholder.textContent = "Loading preview...";

                        const reader = new FileReader();
                        reader.onload = () => {
                            const img = new Image();
                            img.onload = () => {
                                loadedImage = img;
                                renderPreview();
                                placeholder.textContent = "";
                            };
                            img.src = reader.result;
                        };
                        reader.readAsDataURL(file);
                    });

                    [columnsInput, rowsInput, marginInput, dpiInput, pageSizeSelect, orientationSelect].forEach((input) => {
                        input.addEventListener("input", renderPreview);
                        input.addEventListener("change", renderPreview);
                    });

                    window.addEventListener("resize", () => requestAnimationFrame(renderPreview));

                    renderPreview();
                })();
            </script>
        </body>
        </html>
        """
    )


PAGE_SIZES_MM = {
    "A4": (210.0, 297.0),
    "Letter": (215.9, 279.4),
}


def mm_to_px(mm: float, dpi: int) -> int:
    return int(round(mm / 25.4 * dpi))


def rasterbate_image(
    image_bytes: bytes,
    columns: int,
    rows: int,
    page_size: str,
    orientation: str,
    margin_mm: float,
    dpi: int,
) -> BytesIO:
    try:
        from PIL import Image  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
        raise ImportError(
            "Pillow is required to rasterbate images. Please install it with `pip install pillow`."
        ) from exc

    if columns < 1 or rows < 1:
        raise ValueError("Columns and rows must be positive integers.")
    if margin_mm < 0:
        raise ValueError("Margin cannot be negative.")
    if dpi < 72:
        raise ValueError("DPI must be at least 72.")

    if page_size not in PAGE_SIZES_MM:
        raise ValueError("Unsupported page size.")

    orientation = orientation.lower()
    if orientation not in {"portrait", "landscape"}:
        raise ValueError("Orientation must be portrait or landscape.")

    width_mm, height_mm = PAGE_SIZES_MM[page_size]
    if orientation == "landscape":
        width_mm, height_mm = height_mm, width_mm

    page_w_px = mm_to_px(width_mm, dpi)
    page_h_px = mm_to_px(height_mm, dpi)
    margin_px = mm_to_px(margin_mm, dpi)

    if margin_px * 2 >= page_w_px or margin_px * 2 >= page_h_px:
        raise ValueError("Margin too large for the selected page size.")

    tile_w = page_w_px - 2 * margin_px
    tile_h = page_h_px - 2 * margin_px

    target_w = tile_w * columns
    target_h = tile_h * rows

    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Preserve the original resolution: no downscaling. We only crop to the
    # available poster area or center the image if it is smaller than the grid.
    crop_w = min(image.width, target_w)
    crop_h = min(image.height, target_h)
    left = max(0, (image.width - crop_w) // 2)
    top = max(0, (image.height - crop_h) // 2)
    cover = image.crop((left, top, left + crop_w, top + crop_h))

    mosaic = Image.new("RGB", (target_w, target_h), "white")
    offset_x = (target_w - crop_w) // 2
    offset_y = (target_h - crop_h) // 2
    mosaic.paste(cover, (offset_x, offset_y))

    pages = []
    for row in range(rows):
        for col in range(columns):
            crop_box = (
                col * tile_w,
                row * tile_h,
                (col + 1) * tile_w,
                (row + 1) * tile_h,
            )
            tile = mosaic.crop(crop_box)
            page = Image.new("RGB", (page_w_px, page_h_px), "white")
            page.paste(tile, (margin_px, margin_px))
            pages.append(page)

    output = BytesIO()
    pages[0].save(output, format="PDF", save_all=True, append_images=pages[1:], resolution=dpi)
    output.seek(0)
    return output


class RasterbatorHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - name required by BaseHTTPRequestHandler
        page = build_page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self) -> None:  # noqa: N802 - name required by BaseHTTPRequestHandler
        if self.path != "/rasterbate":
            self.send_error(404, "Not Found")
            return

        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("multipart/form-data"):
            self.send_error(400, "Expected multipart/form-data")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            self.send_error(400, "Missing request body")
            return

        body = self.rfile.read(content_length)
        try:
            fields, files = parse_multipart_form(body, content_type)
        except Exception as exc:  # pylint: disable=broad-except
            self.send_error(400, f"Failed to parse form data: {exc}")
            return

        if "image" not in files:
            self.send_error(400, "Image upload is required")
            return

        try:
            columns = int(fields.get("columns", "3"))
            rows = int(fields.get("rows", "3"))
            margin_mm = float(fields.get("margin", "10"))
            dpi = int(fields.get("dpi", "300"))
            page_size = fields.get("page_size", "A4")
            orientation = fields.get("orientation", "portrait")

            image_bytes = files["image"]["content"]
            pdf = rasterbate_image(
                image_bytes=image_bytes,
                columns=columns,
                rows=rows,
                page_size=page_size,
                orientation=orientation,
                margin_mm=margin_mm,
                dpi=dpi,
            )
        except Exception as exc:  # pylint: disable=broad-except
            self.send_error(400, f"Failed to rasterbate image: {exc}")
            return

        pdf_bytes = pdf.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.send_header("Content-Disposition", "attachment; filename=poster.pdf")
        self.end_headers()
        self.wfile.write(pdf_bytes)

    def log_message(self, format: str, *args) -> None:  # noqa: A003 - inherits name from base class
        return  # Silence default console logging for cleaner output


def main() -> None:
    server = HTTPServer((HOST, PORT), RasterbatorHandler)
    print(f"Rasterbator-style site running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
