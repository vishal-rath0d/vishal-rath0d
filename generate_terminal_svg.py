#!/usr/bin/env python3
"""
Clean terminal SVG generator - dynamic YAML reading
Reads profile.yaml and displays it exactly as written
"""
import html

# ============================================
# CONFIGURATION - Edit these values as needed
# ============================================

# Animation Timing
CHAR_SPEED = 0.1          # seconds per character when typing
LINE_SPEED = 0.3          # seconds per line when revealing YAML
BLINK_TIME = 20           # seconds cursor blinks at end
CLEAR_SPEED = 0.1         # seconds per character when typing "clear"

# SVG Dimensions
SVG_WIDTH = 900
SVG_HEIGHT = 650

# Colors (Pink theme from Daria's README)
COLOR_PROMPT = "#D9BED1"      # Pink for prompt and cursor
COLOR_TEXT = "#E6E6E6"        # Light gray for general text
COLOR_KEY = "#D9BED1"         # Pink for YAML keys
COLOR_VALUE = "#B8C5D6"       # Light blue for YAML values
COLOR_BG = "#1E1E1E"          # Dark background
COLOR_HEADER_BG = "#2D2D2D"   # Header bar background
COLOR_RED_DOT = "#FF5F57"     # macOS red button
COLOR_YELLOW_DOT = "#FEBC2E"  # macOS yellow button
COLOR_GREEN_DOT = "#28C840"   # macOS green button

# Layout & Spacing
LEFT_MARGIN = 20              # Left margin for all text
PROMPT_WIDTH = 50             # X position after prompt (for command text)
INDENT_PX_PER_SPACE = 7       # Pixels per space for indentation
LINE_HEIGHT = 20              # Vertical spacing between lines
YAML_START_Y = 100            # Y position where YAML content starts
PROMPT_Y = 70                 # Y position of command prompt

# Text Content
COMMAND = "kubectl get engineer vishal-rathod -o yaml"
CLEAR_COMMAND = "clear"
TERMINAL_TITLE = "vishal@devops-engineer ~ % bash"
YAML_FILE = "profile.yaml"

# Font
FONT_FAMILY = "JetBrains Mono"
FONT_SIZE = 14
TITLE_FONT_SIZE = 13

# Read YAML file directly (as text, not parsed)
with open(YAML_FILE, 'r') as f:
    yaml_content = f.read()

# Split into lines for display
lines = yaml_content.strip().split('\n')

# Calculate timeline
cmd_time = len(COMMAND) * CHAR_SPEED
yaml_start = cmd_time + 0.5
yaml_end = yaml_start + (len(lines) * LINE_SPEED)
blink_end = yaml_end + BLINK_TIME
clear_start = blink_end + 0.5
clear_type_time = 5 * CLEAR_SPEED
clear_typed = clear_start + clear_type_time
clear_execute = clear_typed + 0.3
loop_time = clear_execute + 0.5

print(
    f"Timeline: cmd={cmd_time:.1f}s, yaml={yaml_end-yaml_start:.1f}s ({len(lines)} lines), total={loop_time:.1f}s")

# ============================================
# MAIN SCRIPT - No need to edit below
# ============================================

# Read YAML file directly (as text, not parsed)
with open(YAML_FILE, 'r') as f:
    yaml_content = f.read()

# Split into lines for display
lines = yaml_content.strip().split('\n')

# Calculate required SVG height dynamically - tight fit!
# Formula: header(40) + prompt(70) + yaml_content + bottom_prompt(40) + minimal_padding(30)
required_height = 40 + 70 + (len(lines) * LINE_HEIGHT) + 40 + 30
svg_height = required_height  # Use EXACT required height, no extra padding

# Calculate timeline
cmd_time = len(COMMAND) * CHAR_SPEED
yaml_start = cmd_time + 0.5
yaml_end = yaml_start + (len(lines) * LINE_SPEED)
blink_end = yaml_end + BLINK_TIME
clear_start = blink_end + 0.5
clear_type_time = len(CLEAR_COMMAND) * CLEAR_SPEED
clear_typed = clear_start + clear_type_time
clear_execute = clear_typed + 0.3
loop_time = clear_execute + 0.5

print(
    f"Timeline: cmd={cmd_time:.1f}s, yaml={yaml_end-yaml_start:.1f}s ({len(lines)} lines), total={loop_time:.1f}s")
print(f"SVG Height: {svg_height}px (content requires {required_height}px)")

# SVG Generation
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {svg_height}" width="{SVG_WIDTH}" height="{svg_height}">
<style>
@import url('https://fonts.googleapis.com/css2?family={FONT_FAMILY.replace(" ", "+")}:wght@400;600&amp;display=swap');
* {{ font-family: '{FONT_FAMILY}', monospace; font-size: {FONT_SIZE}px; }}
.prompt {{ fill: {COLOR_PROMPT}; }}
.text {{ fill: {COLOR_TEXT}; }}
.key {{ fill: {COLOR_KEY}; }}
.val {{ fill: {COLOR_VALUE}; }}
@keyframes blink {{ 0%,49% {{opacity:1;}} 50%,100% {{opacity:0;}} }}
.cursor {{ animation: blink 0.8s infinite; }}
</style>

<rect width="{SVG_WIDTH}" height="{svg_height}" fill="{COLOR_BG}" rx="8"/>
<rect width="{SVG_WIDTH}" height="40" fill="{COLOR_HEADER_BG}" rx="8"/>
<circle cx="20" cy="20" r="6" fill="{COLOR_RED_DOT}"/>
<circle cx="40" cy="20" r="6" fill="{COLOR_YELLOW_DOT}"/>
<circle cx="60" cy="20" r="6" fill="{COLOR_GREEN_DOT}"/>
<text x="{SVG_WIDTH//2}" y="25" fill="{COLOR_PROMPT}" font-size="{TITLE_FONT_SIZE}" text-anchor="middle" font-weight="600">{TERMINAL_TITLE}</text>

<g id="terminal">
'''

# LINE 1: Prompt + Command typing
svg += f'<text x="{LEFT_MARGIN}" y="{PROMPT_Y}" class="text">'
svg += '<tspan class="prompt">➜ </tspan>'

# Type each character progressively - each frame at SAME position
for i in range(1, len(COMMAND) + 1):
    t_start = (i-1) * CHAR_SPEED
    t_end = i * CHAR_SPEED
    text = html.escape(COMMAND[:i])

    # Each tspan appears at the same x position (right after prompt)
    svg += f'''<tspan x="{PROMPT_WIDTH}" opacity="0">
  <set attributeName="opacity" to="1" begin="{t_start}s"/>
  <set attributeName="opacity" to="0" begin="{t_end}s"/>
  {text}
</tspan>'''

# Final complete command (stays visible after typing)
svg += f'''<tspan x="{PROMPT_WIDTH}" opacity="0">
  <set attributeName="opacity" to="1" begin="{cmd_time}s"/>
  {html.escape(COMMAND)}
</tspan>'''

# NO cursor here - in real terminal, cursor disappears when you press Enter
svg += '</text>\n\n'

# YAML Content - each line appears separately
y = YAML_START_Y
for idx, line in enumerate(lines):
    t = yaml_start + (idx * LINE_SPEED)

    # Calculate indentation (count leading spaces)
    indent_spaces = len(line) - len(line.lstrip())
    x_pos = LEFT_MARGIN + (indent_spaces * INDENT_PX_PER_SPACE)

    # Get the actual content (without leading spaces)
    content = line.lstrip()
    escaped = html.escape(content)

    svg += f'<text x="{x_pos}" y="{y}" class="text" opacity="0">'
    svg += f'<set attributeName="opacity" to="1" begin="{t}s"/>'

    # Syntax highlighting: detect key:value pairs
    if ':' in content and not content.strip().startswith('-'):
        parts = content.split(':', 1)
        key = html.escape(parts[0])
        val = html.escape(parts[1]) if len(parts) > 1 else ''
        svg += f'<tspan class="key">{key}:</tspan>'
        if val:
            svg += f'<tspan class="val">{val}</tspan>'
    else:
        # List items or plain text
        svg += f'<tspan class="val">{escaped}</tspan>'

    svg += '</text>\n'
    y += LINE_HEIGHT

# Blinking cursor at end
svg += f'\n<text x="{LEFT_MARGIN}" y="{y + LINE_HEIGHT}" class="text" opacity="0">'
svg += f'<set attributeName="opacity" to="1" begin="{yaml_end}s"/>'
# Commenting out blink end so cursor stays visible
# svg += f'<set attributeName="opacity" to="0" begin="{blink_end}s"/>'
svg += '<tspan class="prompt">➜ </tspan>'
svg += '<tspan class="prompt cursor">█</tspan>'
svg += '</text>\n\n'

# COMMENTED OUT: "clear" command - keeps terminal content visible
# # "clear" command - typed character by character
# svg += f'<text x="{LEFT_MARGIN}" y="{y + LINE_HEIGHT}" class="text">'
# svg += f'<tspan class="prompt" opacity="0">'
# svg += f'<set attributeName="opacity" to="1" begin="{clear_start}s"/>'
# svg += '➜ </tspan>'
#
# # Type "clear" character by character
# for i in range(1, len(CLEAR_COMMAND) + 1):
#     t_start = clear_start + ((i-1) * CLEAR_SPEED)
#     t_end = clear_start + (i * CLEAR_SPEED)
#     text = html.escape(CLEAR_COMMAND[:i])
#
#     svg += f'<tspan x="{PROMPT_WIDTH}" opacity="0">'
#     svg += f'<set attributeName="opacity" to="1" begin="{t_start}s"/>'
#     svg += f'<set attributeName="opacity" to="0" begin="{t_end}s"/>'
#     svg += f'{text}</tspan>'
#
# # Final "clear" text
# svg += f'<tspan x="{PROMPT_WIDTH}" opacity="0">'
# svg += f'<set attributeName="opacity" to="1" begin="{clear_typed}s"/>'
# svg += f'{html.escape(CLEAR_COMMAND)}</tspan>'
# svg += '</text>\n\n'
#
# # Execute clear - hide everything after a brief pause
# clear_execute = clear_typed + 0.3
#
# svg += f'''
# <!-- Hide all content when clear executes -->
# <set attributeName="opacity" to="0" begin="{clear_execute}s" targetElement="terminal"/>
# '''

svg += '''
</g>

<script type="text/javascript"><![CDATA[
  (function() {
    var svg = document.querySelector('svg');
    setTimeout(function() {
      svg.setCurrentTime(0);
      setInterval(function() { svg.setCurrentTime(0); }, ''' + str(int(loop_time * 1000)) + ''');
    }, ''' + str(int(loop_time * 1000)) + ''');
  })();
]]></script>
</svg>'''

# Write
with open('terminal.svg', 'w') as f:
    f.write(svg)

print("Generated terminal.svg")
