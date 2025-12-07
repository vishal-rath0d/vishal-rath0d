#!/usr/bin/env python3
"""
Direct GIF generator - renders terminal animation from scratch
No SVG, no white space, exact dimensions
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
FPS = 60
CHAR_SPEED = 0.1
LINE_SPEED = 0.3
BLINK_TIME = 20
CLEAR_SPEED = 0.1

# Colors - higher contrast for readability
BG_COLOR = (25, 25, 25)        # Slightly darker
HEADER_BG = (45, 45, 45)
PROMPT_COLOR = (230, 200, 220)  # Brighter pink
TEXT_COLOR = (240, 240, 240)   # Brighter text
KEY_COLOR = (230, 200, 220)    # Brighter pink
VALUE_COLOR = (200, 210, 230)  # Brighter blue
DOT_RED = (255, 95, 87)
DOT_YELLOW = (254, 188, 46)
DOT_GREEN = (40, 200, 64)

# Layout - bigger for readability
WIDTH = 1000               # Wider
HEADER_HEIGHT = 45
LEFT_MARGIN = 25
LINE_HEIGHT = 24          # More spacing
PROMPT_Y_START = 80
FONT_SIZE = 18            # Bigger font!


def load_font(size=FONT_SIZE):
    """Load highest quality monospace font available"""
    font_paths = [
        # Try JetBrains Mono first (best quality)
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
        "/Library/Fonts/Courier New.ttf",
        "/System/Library/Fonts/Monaco.dfont",
        "/System/Library/Fonts/Menlo.ttc",
        # Fallbacks
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "C:\\Windows\\Fonts\\consola.ttf",  # Windows
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue

    # Last resort - but still better than default
    return ImageFont.load_default()


def draw_header(draw, width):
    """Draw macOS-style header"""
    draw.rectangle([0, 0, width, HEADER_HEIGHT], fill=HEADER_BG)
    # Dots - slightly bigger for clarity
    draw.ellipse([14, 14, 28, 28], fill=DOT_RED)
    draw.ellipse([36, 14, 50, 28], fill=DOT_YELLOW)
    draw.ellipse([58, 14, 72, 28], fill=DOT_GREEN)


def draw_text_high_quality(draw, pos, text, color, font):
    """Draw text with antialiasing for better quality"""
    # PIL automatically uses antialiasing for TrueType fonts
    draw.text(pos, text, fill=color, font=font)


def main():
    # Read YAML
    with open('profile.yaml', 'r') as f:
        lines = [line.rstrip() for line in f.read().strip().split('\n')]

    # Calculate exact height needed
    content_height = PROMPT_Y_START + (len(lines) + 3) * LINE_HEIGHT + 50
    height = HEADER_HEIGHT + content_height

    print(f"🎬 Generating GIF directly (no SVG)...")
    print(f"   Size: {WIDTH}x{height}px (EXACT fit, no white space)")
    print(f"   Lines: {len(lines)}, FPS: {FPS}")

    # Calculate timeline
    command = "cat profile.yaml"
    cmd_time = len(command) * CHAR_SPEED
    yaml_start = cmd_time + 0.5
    yaml_end = yaml_start + len(lines) * LINE_SPEED
    duration = yaml_end + BLINK_TIME + 3

    total_frames = int(duration * FPS)
    print(f"   Frames: {total_frames}, Duration: {duration:.1f}s\n")

    font = load_font()
    frames = []

    print("📸 Rendering frames...")
    for frame_num in range(total_frames):
        t = frame_num / FPS

        # Create frame
        img = Image.new('RGB', (WIDTH, height), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw header
        draw_header(draw, WIDTH)

        # Draw prompt line
        y = HEADER_HEIGHT + PROMPT_Y_START
        draw_text_high_quality(draw, (LEFT_MARGIN, y),
                               "➜ ", PROMPT_COLOR, font)

        # Type command
        if t < cmd_time:
            chars_typed = int(t / CHAR_SPEED)
            draw_text_high_quality(
                draw, (55, y), command[:chars_typed], PROMPT_COLOR, font)
        elif t >= cmd_time:
            draw_text_high_quality(draw, (55, y), command, PROMPT_COLOR, font)

        # Show YAML lines
        if t >= yaml_start:
            y_pos = HEADER_HEIGHT + PROMPT_Y_START + LINE_HEIGHT * 2
            lines_to_show = int((t - yaml_start) / LINE_SPEED)

            for i, line in enumerate(lines[:lines_to_show + 1]):
                indent = len(line) - len(line.lstrip())
                x_pos = LEFT_MARGIN + indent * 10  # More indent spacing
                content = line.lstrip()

                # Color based on content
                if ':' in content and not content.startswith('-'):
                    parts = content.split(':', 1)
                    draw_text_high_quality(
                        draw, (x_pos, y_pos), parts[0] + ':', KEY_COLOR, font)
                    if len(parts) > 1:
                        key_width = font.getbbox(parts[0] + ':')[2]
                        draw_text_high_quality(
                            draw, (x_pos + key_width, y_pos), parts[1], VALUE_COLOR, font)
                else:
                    draw_text_high_quality(
                        draw, (x_pos, y_pos), content, VALUE_COLOR, font)

                y_pos += LINE_HEIGHT

        frames.append(img)

        if (frame_num + 1) % 100 == 0 or frame_num == total_frames - 1:
            print(
                f"   {((frame_num + 1) / total_frames * 100):.0f}% done ({frame_num + 1}/{total_frames})")

    print("\n💾 Saving GIF...")
    frames[0].save(
        'terminal.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=int(1000/FPS),
        loop=0
    )

    size_mb = os.path.getsize('terminal.gif') / (1024 * 1024)
    print(f"\n✅ Done! terminal.gif")
    print(f"   Size: {size_mb:.2f} MB ({WIDTH}x{height}px)")
    print(f"   Duration: {duration:.1f}s, Loops: infinite")
    print(f"   NO white space - exact fit!")


if __name__ == '__main__':
    main()
