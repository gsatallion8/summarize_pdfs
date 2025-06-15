import os
import openai
from pathlib import Path
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")

def load_text_files(text_folder: Path) -> List[Path]:
    return list(text_folder.glob("*.txt"))

def read_text(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def summarize_text(text: str, model="gpt-4", max_tokens=300) -> str:
    prompt = (
        "Summarize the following document in concise, clear bullet points. "
        "Highlight key ideas, events, and any critical information:\n\n"
        f"{text}"
    )

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.5,
    )
    return response["choices"][0]["message"]["content"]

def summarize_folder(text_folder: str, output_summary_file: str):
    text_files = load_text_files(Path(text_folder))
    combined_summary = []

    for text_file in text_files:
        print(f"Summarizing: {text_file.name}")
        text = read_text(text_file)
        summary = summarize_text(text)
        combined_summary.append(f"## Summary of {text_file.name}\n{summary}\n")

    with open(output_summary_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(combined_summary))

    print(f"\nSummaries saved to {output_summary_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Summarize all .txt files in a folder using GPT.")
    parser.add_argument("text_folder", help="Folder with .txt files")
    parser.add_argument("output_summary_file", help="Path to save the combined summary")

    args = parser.parse_args()
    summarize_folder(args.text_folder, args.output_summary_file)
