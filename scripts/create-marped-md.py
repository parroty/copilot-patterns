import os
import re
import yaml
from pprint import pprint

# Define the root directory of the contents
ROOT_DIR = 'contents/ja'

# Define section input patterns as a constant
SECTION_PATTERNS = [
    ('title', r'## (.+?)\n(?=### Description)'),
    ('description', r'### Description\n\n(.*?)(###|####|\Z)'),
    ('example', r'#### Example\n\n(.*?)(###|\Z)'),
    ('exercise', r'### Exercise\n\n(.*?)(###|\Z)'),
    ('checklist', r'### Checklist for Further Learning\n\n(.*?)(###|\Z)'),
]

# Define section output config as a constant
SECTION_CONFIG = {
    'title': {"class": "title", "footer_prefix": "GitHub Copilot Patterns", "header": "", "title": "{name}"},
    'description': {"class": "description", "footer_prefix": "GitHub Copilot Patterns", "header": "", "title": "Description"},
    'example': {"class": "example", "footer_prefix": "GitHub Copilot Patterns", "header": "", "title": "Example"},
    'exercise': {"class": "exercise", "footer_prefix": "GitHub Copilot Patterns", "header": "", "title": "Exercise"},
    'checklist': {"class": "checklist", "footer_prefix": "GitHub Copilot Patterns", "header": "", "title": "Checklist for Further Learning"}
}

def _extract_section(pattern, content):
    """Helper function to extract a section using a given pattern."""
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None

def extract_sections(content):
    """ Extracts sections from the provided content using predefined patterns."""
    return {name: _extract_section(pattern, content) for name, pattern in SECTION_PATTERNS if _extract_section(pattern, content)}

def extract_yaml(content):
    """ Extracts YAML content from the provided string."""
    pattern = r'---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}

def read_file_content(file_path):
    """Read the content of the given file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_file_content(content):
    """Parse sections and YAML content from the given file content."""
    sections = extract_sections(content)
    meta = extract_yaml(content)
    meta["short-description"] = meta.get("description", "")
    return {**meta, **sections}

def read_and_parse_files(directory):
    """Read and parse markdown files from the specified directory."""
    parsed_contents = []

    for subdir, _, files in os.walk(directory):
        if subdir != directory:  # process only root directory contents
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(subdir, file)
                    content = read_file_content(file_path)
                    parsed_contents.append(parse_file_content(content))
    return parsed_contents

def extract_hint_content(hint):
    """Extract the content inside a specific hint tag and format it."""
    pattern = r'{% hint style="info" %}\n(.*?)\n{% endhint %}'
    match = re.search(pattern, hint, re.DOTALL)
    if match:
        return '> ' + '\n> '.join(match.group(1).strip().split('\n'))
    return None

def clean_content(content, section):
    target_content = content[section]
    """Clean and transform the given content."""
    # Modify image links to a simpler markdown format
    target_content = re.sub(r'\[<img src="(.*?)">\]\(.*?\)', r'![](\1)', target_content)
    # Remove the first line
    if section == "title":
        target_content = re.sub(r'^.*?\n', '', target_content)
        # Extract content from a specific hint tag
        hint_content = extract_hint_content(target_content)
        # Remove the original hint tag and its content
        target_content = re.sub(r'{% hint style="info" %}.*?{% endhint %}', '', target_content, flags=re.DOTALL)
        # Append the formatted hint content, if it exists
        if hint_content:
            target_content += '\n\n' + hint_content
    return target_content.strip()


def format_marp_section(class_name, footer_prefix, header, title, content, section, name):
    
    # Customize Functions Mapping
    customize_functions = {
        "title": customize_title_section
    }
    
    content[section] = clean_content(content, section)
    customize_func = customize_functions.get(section, customize_default_section)
    content_section = customize_func(content, section, title)
    
    header_elements = {
        "_class": f"{class_name}",
        "_footer": f"{footer_prefix} - {name}",
        "_header": header
    }
    
    header_section = "<!-- \n"
    for key, value in header_elements.items():
        header_section += f"{key}: \"{value}\"\n"
    header_section += "-->\n"

    return header_section + content_section

def convert_to_marp(parsed_contents):
    """Convert the parsed contents to Marp format."""
    marp_content = ""
    for content in parsed_contents:
        name = content["name"]
        for section, config in SECTION_CONFIG.items():
            if section in content and content[section]:
                title = config["title"].format(name=name)
                marp_content += format_marp_section(config["class"], config["footer_prefix"], config["header"], title, content, section, name)
    return marp_content


def customize_title_section(content, section, category):
    cleaned_content = f"{content['short-description']}\n\n{content[section]}"
    return f"## {category}\n\n{cleaned_content}\n\n---\n"

def customize_default_section(content, section, category):
    cleaned_content = f"## {content['name']}\n\n{content[section]}"

    # Insert title to the second line of cleaned_content
    content_section = cleaned_content.split("\n", 1)
    content_section.insert(1, f"\n\n### {category}\n\n")
    return "".join(content_section) + "\n\n---\n"

def main():
    contents = read_and_parse_files(ROOT_DIR)
    # Add marp_content to scripts/base-docs.md and save it as ./output_marp.md
    with open("scripts/base-docs.md", "r", encoding="utf-8") as f:
        base_docs = f.read()
        marp_content = base_docs + convert_to_marp(contents)
    with open("output_marp.md", "w", encoding="utf-8") as f:
        f.write(marp_content)

if __name__ == '__main__':
    main()
