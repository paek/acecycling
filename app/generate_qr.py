"""Generate a QR code for ACE Cycling app download with app icon in center."""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw
import os

# ── Config ──
URL = "http://acecycling.acegame.com/app/index.html"
ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "icons", "ace_cycling_2st.png")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "qr_code_app_download.png")

# ── Generate QR code ──
qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo overlay
    box_size=20,
    border=4,
)
qr.add_data(URL)
qr.make(fit=True)

# Create styled QR code with rounded modules
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer()
).convert("RGBA")

qr_w, qr_h = img.size

# ── Load and prepare app icon ──
icon = Image.open(ICON_PATH).convert("RGBA")

# Size the icon to ~22% of QR code width
logo_size = int(qr_w * 0.24)
icon = icon.resize((logo_size, logo_size), Image.LANCZOS)

# Create circular mask for rounded icon
mask = Image.new("L", (logo_size, logo_size), 0)
mask_draw = ImageDraw.Draw(mask)
corner_r = int(logo_size * 0.22)  # App-icon-style rounded corners
mask_draw.rounded_rectangle([0, 0, logo_size - 1, logo_size - 1], radius=corner_r, fill=255)

# White background padding behind the icon
pad = 12
bg_size = logo_size + pad * 2
bg = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 255))
bg.paste(icon, (pad, pad), mask)

# ── Composite onto QR code ──
pos = ((qr_w - bg_size) // 2, (qr_h - bg_size) // 2)
img.paste(bg, pos, bg)

# ── Save ──
final = img.convert("RGB")
final.save(OUTPUT_PATH, "PNG", dpi=(300, 300))
print(f"✅ QR code saved: {OUTPUT_PATH}")
print(f"   Size: {final.size[0]}x{final.size[1]}px")
print(f"   URL:  {URL}")
print(f"   Icon: {os.path.basename(ICON_PATH)}")
