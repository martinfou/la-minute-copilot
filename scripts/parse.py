#!/usr/bin/env python3
"""
Parser PowerPoint pour La minute Copilot.
Lit un fichier JSON de contenu et génère un .pptx.

Usage:
    python3 parse.py presentations/ep01-outlook.json
    python3 parse.py presentations/ep01-outlook.json -o mon_fichier.pptx
"""

import json, sys, os, argparse
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Constantes de design ──
BLUE = RGBColor(0x00, 0x78, 0xD4)
DARK = RGBColor(0x2B, 0x2B, 0x2B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x6B, 0x6B, 0x6B)
LIGHT_BG = RGBColor(0xF0, 0xF4, 0xF8)
GREEN = RGBColor(0x10, 0xB9, 0x81)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
CARD_BORDER = RGBColor(0xE0, 0xE0, 0xE0)
FOOTER_BLUE = RGBColor(0xAA, 0xD4, 0xF0)
BONUS_BG = RGBColor(0xFF, 0xF3, 0xCD)
BONUS_TEXT = RGBColor(0x85, 0x6E, 0x04)

PALETTE = {
    'blue': BLUE,
    'green': GREEN,
    'amber': AMBER,
}

TITLE_SIZE = 32
SUBTITLE_SIZE = 18
CARD_TITLE_SIZE = 18
BODY_SIZE = 13
SMALL_SIZE = 14

def add_bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, size=18, bold=False, color=DARK, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = 'Calibri'
    p.alignment = align
    return tf

def add_multiline(slide, left, top, width, height, lines, size=13, color=DARK):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = 'Calibri'
        p.space_after = Pt(4)
    return tf

def add_card(slide, left, top, width, height, card_data):
    """Dessine une carte avec fond blanc, bordure et contenu."""
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = CARD_BORDER

    accent = PALETTE.get(card_data.get('color', 'blue'), BLUE)
    add_textbox(slide, left + 0.3, top + 0.2, width - 0.6, 0.5,
                f"{card_data['icon']} {card_data['title']}", size=CARD_TITLE_SIZE, bold=True, color=accent)
    add_multiline(slide, left + 0.3, top + 0.7, width - 0.6, height - 1.0,
                  card_data.get('lines', []), size=BODY_SIZE, color=DARK)

def generate(json_path, output_path=None):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    for slide_data in data['slides']:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide_type = slide_data.get('type', '')

        if slide_type == 'title':
            add_bg(slide, BLUE)
            add_textbox(slide, 1, 2.0, 11, 1.2, slide_data['title'], size=48, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
            add_textbox(slide, 1, 3.2, 11, 0.8, slide_data.get('subtitle', ''), size=28, color=FOOTER_BLUE, align=PP_ALIGN.CENTER)
            add_textbox(slide, 1, 4.5, 11, 0.6, slide_data.get('footer', ''), size=16, color=FOOTER_BLUE, align=PP_ALIGN.CENTER)

        elif slide_type == 'tips':
            add_bg(slide, WHITE)
            add_textbox(slide, 0.5, 0.3, 12, 0.7, slide_data['title'], size=TITLE_SIZE, bold=True, color=DARK)
            add_textbox(slide, 0.5, 1.0, 12, 0.5, slide_data.get('subtitle', ''), size=SUBTITLE_SIZE, color=GRAY)

            cards = slide_data.get('cards', [])
            n = len(cards)
            if n == 2:
                widths = [6.0, 6.0]
            elif n == 3:
                widths = [4.0, 4.0, 4.0]
            else:
                widths = [12.0 / n] * n

            x = 0.5
            for i, card in enumerate(cards):
                add_card(slide, x, 1.7, widths[i] - 0.2, 5.2, card)
                x += widths[i] + 0.2

        elif slide_type == 'bonus':
            add_bg(slide, LIGHT_BG)
            add_textbox(slide, 0.5, 0.3, 12, 0.7, slide_data['title'], size=TITLE_SIZE, bold=True, color=DARK)

            cards = slide_data.get('cards', [])
            n = len(cards)
            width = (12.0 / n) - 0.3
            x = 0.5
            for card in cards:
                add_card(slide, x, 1.3, width, 5.5, card)
                x += width + 0.3

        elif slide_type == 'summary':
            add_bg(slide, BLUE)
            add_textbox(slide, 1, 1.0, 11, 0.8, slide_data['title'], size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

            cards = slide_data.get('cards', [])
            n = len(cards)
            card_w = 3.8
            gap = (11 - n * card_w) / (n + 1)
            x = 0.5 + gap
            for card in cards:
                shape = slide.shapes.add_shape(1, Inches(x), Inches(2.2), Inches(card_w), Inches(2.5))
                shape.fill.solid()
                shape.fill.fore_color.rgb = WHITE
                shape.line.color.rgb = FOOTER_BLUE
                add_textbox(slide, x + 0.3, 2.4, card_w - 0.6, 0.6,
                            f"{card['icon']} {card['title']}", size=22, bold=True, color=DARK, align=PP_ALIGN.CENTER)
                add_textbox(slide, x + 0.3, 3.2, card_w - 0.6, 1.0,
                            card.get('desc', ''), size=16, color=GRAY, align=PP_ALIGN.CENTER)
                x += card_w + gap

            bonus_text = slide_data.get('bonus', '')
            if bonus_text:
                shape = slide.shapes.add_shape(1, Inches(3.5), Inches(5.2), Inches(6.3), Inches(1.2))
                shape.fill.solid()
                shape.fill.fore_color.rgb = BONUS_BG
                shape.line.color.rgb = RGBColor(0xFF, 0xE0, 0x82)
                add_textbox(slide, 3.7, 5.4, 5.9, 0.6, bonus_text, size=16, bold=True, color=BONUS_TEXT, align=PP_ALIGN.CENTER)

            footer = slide_data.get('footer', '')
            if footer:
                add_textbox(slide, 1, 6.7, 11, 0.5, footer, size=14, color=FOOTER_BLUE, align=PP_ALIGN.CENTER)

    # Sauvegarde
    if not output_path:
        basename = os.path.splitext(os.path.basename(json_path))[0]
        output_path = os.path.join(os.path.dirname(json_path), f"{basename}.pptx")

    prs.save(output_path)
    print(f"✅ Présentation générée: {output_path}")
    print(f"   Diapositives: {len(prs.slides)}")
    print(f"   Taille: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Génère un PowerPoint from JSON')
    parser.add_argument('json', help='Fichier JSON des slides')
    parser.add_argument('-o', '--output', help='Fichier .pptx de sortie')
    args = parser.parse_args()
    generate(args.json, args.output)
