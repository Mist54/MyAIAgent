import os
from Core.config import NOTE_DIR
from .summarizer import summarize
from datetime import datetime
import re


def generate_filename(title: str, content: str) -> str:
    # Get current date in yyyyMMdd format
    date_str = datetime.now().strftime("%Y%m%d")
    # Extract the first few words from the content (e.g., first sentence or meaningful words)
    content_preview = " ".join(content.split()[:2])  # Get the first 2 words
    content_preview = content_preview.strip().replace(" ", "_")  # Replace spaces with underscores

    # Combine date and preview to generate the filename
    filename = f"{date_str}_Summary_{content_preview}.txt"
    return filename


def clean_up_summary(summary: str) -> str:
    # Remove incomplete sentences or trailing words like "AIs"
    summary = summary.strip()

    # Remove trailing incomplete words like "AIs"
    summary = re.sub(r'\b[A-Za-z]{1,3}\b$', '', summary)

    # Clean any trailing punctuation issues
    summary = re.sub(r'\s+[.,;!?]', '', summary)  # Remove extra spaces before punctuation

    # Ensure the summary ends with proper punctuation
    if summary and not any(summary.rstrip().endswith(p) for p in ['.', '!', '?']):
        summary = summary.rstrip() + '.'

    # Clean up potential issues with bullet points
    if '\n' in summary:
        # Fix numbered list items without proper spacing
        summary = re.sub(r'(\n\d+\.)\s*', r'\1 ', summary)

        # Ensure each bullet point ends with proper punctuation
        lines = summary.split('\n')
        for i in range(len(lines)):
            line = lines[i].strip()
            if line and not any(line.endswith(p) for p in ['.', '!', '?']):
                lines[i] = line + '.'
        summary = '\n'.join(lines)

    return summary.strip()


def save_note(title: str, content: str, key_points=None) -> str:
    if not os.path.exists(NOTE_DIR):
        try:
            os.makedirs(NOTE_DIR)
        except Exception as e:
            print(f"Error creating directory {NOTE_DIR}: {e}")
            return ""

    try:
        filename = generate_filename(title, content)  # Generate dynamic filename
        filepath = os.path.join(NOTE_DIR, filename)

        # Generate summary with error handling
        try:
            summary = summarize(content, key_points=key_points)
            clean_summary = clean_up_summary(summary)
        except Exception as e:
            print(f"Error generating summary: {e}")
            clean_summary = "Error generating summary."

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=== Original Content ===\n")
            f.write(content.strip())
            f.write("\n\n=== Summary ===\n")
            f.write(clean_summary)

            # If key points were requested, add a section header
            if key_points and "1." in clean_summary:
                f.write("\n\n=== Key Points ===\n")
                # Extract just the key points - they're already in the summary
                # But we add this section for clarity

        return filepath
    except Exception as e:
        print(f"Error saving note: {e}")
        return ""


def summarize_note(filepath: str, key_points=None) -> str:
    try:
        if not os.path.exists(filepath):
            return f"Error: File not found at {filepath}"

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Handle key points separately if requested
        if key_points:
            # Check if content already has key points section
            if "=== Key Points ===" in content:
                key_points_section = content.split("=== Key Points ===", 1)[1].strip()
                if key_points_section:
                    return key_points_section

            # Extract the original content to generate key points from
            if "=== Original Content ===" in content:
                original_content = content.split("=== Original Content ===", 1)[1]
                if "===" in original_content:
                    original_content = original_content.split("===", 1)[0].strip()
                return summarize(original_content, key_points=key_points)
            else:
                # If no original content section, use the whole file
                return summarize(content, key_points=key_points)
        else:
            # Standard behavior - get existing summary if available
            if "=== Summary ===" in content:
                summary_section = content.split("=== Summary ===", 1)[1]
                # Stop at the next section if there is one
                if "===" in summary_section:
                    summary_section = summary_section.split("===", 1)[0]
                return summary_section.strip()
            else:
                # Generate a new summary
                return summarize(content)
    except Exception as e:
        return f"Error reading or summarizing note: {e}"