from transformers import pipeline
import textwrap
import re

# Single summarizer pipeline
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")


def chunk_text(text: str, max_chunk_size: int = 1000) -> list[str]:
    return textwrap.wrap(text, width=max_chunk_size, break_long_words=False, break_on_hyphens=False)


def summarize(text: str, max_length=150, min_length=40, key_points=None) -> str:
    if not text.strip():
        return "Empty input"

    if key_points is not None:
        if not isinstance(key_points, int) or key_points <= 0:
            return "Error: key_points should be a positive integer."

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        if not chunk.strip():
            continue

        length = len(chunk.split())
        max_len = min(max_length, max(20, int(length * 0.8)))
        min_len = min(min_length, max(5, int(length * 0.4)))

        if length < 10:
            summaries.append(chunk)
            continue

        try:
            result = summarizer_pipeline(
                chunk,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )
            summary_text = result[0]["summary_text"].strip()
            if summary_text:
                summaries.append(summary_text)

        except Exception as e:
            print(f"Error summarizing chunk: {e}")
            summaries.append(chunk)

    combined_text = " ".join(summaries).strip()

    if key_points and combined_text:
        try:
            bullet_markers = r'(?:^|\n)(?:•|-|\*|\d+\.)\s*'

            # If bullet markers are present, split by them
            if re.search(bullet_markers, combined_text):
                bullets = re.split(bullet_markers, combined_text)
            else:
                bullets = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', combined_text)

            bullets = [b.strip() for b in bullets if b.strip()]
            bullets = bullets[:key_points]

            formatted_points = []
            for i, point in enumerate(bullets):
                if not any(point.endswith(p) for p in ['.', '!', '?']):
                    point += '.'
                formatted_points.append(f"{i + 1}. {point}")

            return "\n".join(formatted_points)

        except Exception as e:
            print(f"Error formatting key points: {e}")
            return combined_text

    return combined_text
