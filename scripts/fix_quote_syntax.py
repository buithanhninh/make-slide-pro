# -*- coding: utf-8 -*-
import re
import ast
from pathlib import Path

def fix_file(file_path: Path):
    text = file_path.read_text(encoding='utf-8')
    lines = text.split('\n')
    fixed_lines = []
    for line in lines:
        stripped = line.strip()
        # Look for pattern: "key": "value with "inner quotes" and more"
        m = re.match(r'^(\s*)"([^"]+)"\s*:\s*"(.*)"\s*(,?)$', line)
        if m:
            indent, key, val, comma = m.groups()
            # If val contains unescaped double quotes, replace them with single quotes
            if '"' in val:
                val_fixed = val.replace('"', "'")
                fixed_line = f'{indent}"{key}": "{val_fixed}"{comma}'
                fixed_lines.append(fixed_line)
                continue
        # Also check for list elements: {"key": "val with "inner" quotes", ...}
        # In dict literals inside list: {"title": "...", "text": "..."}
        # We can replace internal quotes inside atom text or title
        # Let's handle patterns like {"title": "...", "text": "..."}
        fixed_lines.append(line)

    new_text = '\n'.join(fixed_lines)
    # If still has syntax error, let's locate exact line
    file_path.write_text(new_text, encoding='utf-8')
    try:
        ast.parse(new_text)
        print(f"SUCCESS: {file_path.name} is now valid Python!")
    except Exception as e:
        print(f"STILL ERROR in {file_path.name}: {e}")

for i in [3, 4, 5, 6]:
    fix_file(Path(f'scripts/course2_data_bai{i}.py'))
