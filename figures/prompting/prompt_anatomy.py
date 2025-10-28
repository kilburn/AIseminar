# Improved, larger, more legible version of the diagram

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# --- Configuration ---
WIDTH, HEIGHT = 3200, 1200  # Bigger canvas
BACKGROUND_COLOR = (255, 255, 255, 0)  # Transparent background (RGBA)
LINE_COLOR = "#FFFFFF"  # White strokes (good on dark slides)
BOX_COLOR = (255, 255, 255, 0)  # Transparent boxes
FONT_COLOR = "#FFFFFF"  # White text
PADDING = 120  # More breathing room
BOX_WIDTH, BOX_HEIGHT = 520, 340  # Larger boxes
ARROW_SIZE = 40  # Bigger arrows
FONT_SIZE_TITLE = 92  # Main title
FONT_SIZE_BOX_TITLE = 72  # Box title
FONT_SIZE_SUB = 56  # Box subtitle
STROKE_WIDTH = 6  # Thicker lines for visibility
DOT_RADIUS = 12

# --- Fonts ---
def load_font(preferred, size):
    for f in preferred:
        try:
            return ImageFont.truetype(f, size)
        except IOError:
            continue
    return ImageFont.load_default()

font_main_title = load_font(
    ["DejaVuSans.ttf", "Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    FONT_SIZE_TITLE,
)
font_box_title = load_font(
    ["DejaVuSans.ttf", "Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    FONT_SIZE_BOX_TITLE,
)
font_sub = load_font(
    ["DejaVuSans.ttf", "Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    FONT_SIZE_SUB,
)

# --- Diagram Data ---
PROMPT_STEPS = [
    ("Examples", "guide desired output"),
    ("Additional Information", "background context"),
    ("Role", "model's persona"),
    ("Directive", "clear instructions"),
    ("Output Formatting", "structure of response"),
]

# Helper: draw centered text (with optional wrapping)
def draw_centered_text(draw, text, center_x, top_y, font, max_width=None, line_spacing=8):
    lines = [text]
    if max_width is not None:
        # rough wrap based on character width
        avg_char_w = max(font.getlength("A"), 1)
        est_chars_per_line = max(int(max_width / (avg_char_w * 0.8)), 1)
        lines = textwrap.wrap(text, width=est_chars_per_line)
    # compute block height
    heights = []
    widths = []
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        widths.append(w)
        heights.append(h)
    total_h = sum(heights) + line_spacing * (len(lines)-1)
    y = top_y
    # draw lines centered
    for i, line in enumerate(lines):
        w = widths[i]
        h = heights[i]
        x = center_x - w/2
        draw.text((x, y), line, font=font, fill=FONT_COLOR)
        y += h + line_spacing
    return total_h

# --- Image Setup ---
img = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND_COLOR)
draw = ImageDraw.Draw(img)

# --- Title & separator ---
TITLE = "Recommended Order for Prompts"
bbox_title = draw.textbbox((0,0), TITLE, font=font_main_title)
title_w = bbox_title[2] - bbox_title[0]
title_x = (WIDTH - title_w)//2
title_y = 80
draw.text((title_x, title_y), TITLE, font=font_main_title, fill=FONT_COLOR)
sep_y = title_y + (bbox_title[3]-bbox_title[1]) + 40
draw.line([(PADDING, sep_y), (WIDTH - PADDING, sep_y)], fill=LINE_COLOR, width=STROKE_WIDTH)

# --- Layout calculations ---
num_steps = len(PROMPT_STEPS)
available_w = WIDTH - 2*PADDING
spacing = (available_w - num_steps*BOX_WIDTH) / (num_steps - 1)
top_y_boxes = int(sep_y + 120)
center_y = top_y_boxes + BOX_HEIGHT//2

box_centers = []

# --- Draw boxes ---
for i, (title, subtitle) in enumerate(PROMPT_STEPS):
    x1 = int(PADDING + i*(BOX_WIDTH + spacing))
    y1 = top_y_boxes
    x2 = x1 + BOX_WIDTH
    y2 = y1 + BOX_HEIGHT
    cx = (x1 + x2)//2
    cy = (y1 + y2)//2
    box_centers.append((cx, cy))

    # Box
    draw.rectangle([x1, y1, x2, y2], outline=LINE_COLOR, width=STROKE_WIDTH, fill=BOX_COLOR)

    # Dot
    draw.ellipse([x1 + 24 - DOT_RADIUS, y1 + 28 - DOT_RADIUS, x1 + 24 + DOT_RADIUS, y1 + 28 + DOT_RADIUS], fill=LINE_COLOR)

    # Text
    title_block_h = draw_centered_text(draw, title, cx, y1 + 48, font_box_title, max_width=BOX_WIDTH - 48, line_spacing=10)
    _ = draw_centered_text(draw, subtitle, cx, y1 + 48 + title_block_h + 24, font_sub, max_width=BOX_WIDTH - 64, line_spacing=8)

    # Arrows (to next)
    if i < num_steps - 1:
        nx1 = int(PADDING + (i+1)*(BOX_WIDTH + spacing))
        line_y = cy
        draw.line([(x2, line_y), (nx1, line_y)], fill=LINE_COLOR, width=STROKE_WIDTH)
        tip_x = nx1
        draw.polygon([(tip_x, line_y),
                      (tip_x - ARROW_SIZE, line_y - ARROW_SIZE/2),
                      (tip_x - ARROW_SIZE, line_y + ARROW_SIZE/2)], fill=LINE_COLOR)

# --- Save ---
out_path = "figures/prompting/prompt_anatomy.png"
img.save(out_path)
out_path
