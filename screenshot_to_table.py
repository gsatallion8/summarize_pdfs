import openai
import base64
import argparse
from pathlib import Path
from openai import OpenAI
from typing import Optional

client = OpenAI()

def encode_image_to_base64(image_path: str) -> str:
    """Encode an image to base64 for OpenAI API."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def extract_table_from_image(image_path: str, prompt: Optional[str] = None, model: str = "gpt-4o") -> str:
    """
    Extracts a table from a scanned image using OpenAI GPT-4o's vision capabilities.
    
    Args:
        image_path (str): Path to the image file (jpg, png).
        prompt (str, optional): Custom prompt for the model.
        model (str): Model to use (must support vision, e.g. gpt-4o).
    
    Returns:
        str: CSV-like string of the extracted table.
    """
    base64_image = encode_image_to_base64(image_path)

    if not prompt:
        prompt = (
            "You are a document analysis assistant. Extract any tables found in this image. "
            "Return the result in valid CSV format, without commentary or explanations."
        )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=2048,
    )

    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Extract tables from a scanned image using OpenAI GPT-4o.")
    parser.add_argument("image_path", help="Path to the input image (jpg, png, etc.)")
    parser.add_argument("output_path", help="Path to the output CSV file")
    parser.add_argument("--prompt", default=None, help="Custom prompt to override default table extraction prompt")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use (default: gpt-4o)")

    args = parser.parse_args()

    table_csv = extract_table_from_image(args.image_path, prompt=args.prompt, model=args.model)

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(table_csv)

    print(f"✅ Table extracted and saved to {output_path}")

if __name__ == "__main__":
    main()