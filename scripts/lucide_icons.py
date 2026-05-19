"""
Icônes Lucide (SVG) pour les présentations PowerPoint.
https://lucide.dev/icons

Télécharge les SVG depuis lucide-static (unpkg), applique la couleur d'accent
et rasterise en PNG via rsvg-convert (librsvg).
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from pptx.dml.color import RGBColor

LUCIDE_VERSION = "0.469.0"
LUCIDE_CDN = f"https://unpkg.com/lucide-static@{LUCIDE_VERSION}/icons/{{name}}.svg"

_REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = _REPO_ROOT / "assets" / "icons" / "cache"


def rgb_to_hex(color: RGBColor) -> str:
    """Convertit un RGBColor python-pptx en #RRGGBB."""
    if hasattr(color, "rgb"):
        val = color.rgb
        if isinstance(val, int):
            return f"#{val:06X}"
        s = str(val).lstrip("#")
        return f"#{s.upper()}"
    # python-pptx 1.x : RGBColor se comporte comme un tuple (R, G, B)
    return f"#{int(color[0]):02X}{int(color[1]):02X}{int(color[2]):02X}"


def _fetch_svg(name: str) -> str:
    name = name.strip().lower().replace("_", "-")
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError(f"Nom d'icône Lucide invalide: {name!r}")
    url = LUCIDE_CDN.format(name=name)
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"Icône Lucide introuvable: {name} (https://lucide.dev/icons/{name})") from e
        raise


def _colorize_svg(svg: str, hex_color: str) -> str:
    hex_color = hex_color if hex_color.startswith("#") else f"#{hex_color}"
    svg = svg.replace("currentColor", hex_color)
    svg = re.sub(r'stroke="(?!none)[^"]*"', f'stroke="{hex_color}"', svg)
    svg = re.sub(r'fill="currentColor"', f'fill="{hex_color}"', svg)
    return svg


def _rsvg_convert(svg_path: Path, png_path: Path, size_px: int) -> None:
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        raise RuntimeError(
            "rsvg-convert introuvable. Installez librsvg (ex. brew install librsvg) "
            "pour afficher les icônes Lucide dans les présentations."
        )
    subprocess.run(
        [rsvg, "-w", str(size_px), "-h", str(size_px), str(svg_path), "-o", str(png_path)],
        check=True,
        capture_output=True,
    )


def render_icon_png(name: str, color: RGBColor, size_px: int = 48) -> Path:
    """
    Retourne le chemin d'un PNG en cache pour l'icône Lucide demandée.
    """
    hex_color = rgb_to_hex(color).lstrip("#").upper()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{name}_{hex_color}_{size_px}.png"
    if cache_path.exists():
        return cache_path

    svg = _colorize_svg(_fetch_svg(name), f"#{hex_color}")
    with tempfile.TemporaryDirectory() as tmp:
        svg_path = Path(tmp) / f"{name}.svg"
        png_path = Path(tmp) / f"{name}.png"
        svg_path.write_text(svg, encoding="utf-8")
        _rsvg_convert(svg_path, png_path, size_px)
        cache_path.write_bytes(png_path.read_bytes())
    return cache_path
