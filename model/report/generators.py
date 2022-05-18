from pathlib import Path


def generate_html_file(file_path: Path, fulfilled_template: str):
    with file_path.open(mode='w') as file:
        file.write(fulfilled_template)
