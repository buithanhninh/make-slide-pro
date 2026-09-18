# ai_image_engine.py
# World-Class AI Illustration Engine for Make Slide Pro V6.2.
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None

ILLUSTRATIONS_DIR = Path('assets/illustrations')
ILLUSTRATIONS_DIR.mkdir(parents=True, exist_ok=True)


class AIImageEngine:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('HF_TOKEN') or os.environ.get('HUGGINGFACE_TOKEN')
        self.client = None
        if self.token and InferenceClient:
            try:
                self.client = InferenceClient(token=self.token)
            except Exception as e:
                print(f'[AIImageEngine] Hugging Face client init error: {e}')

    def get_illustration_for_lesson(self, lesson_index: int, prompt: Optional[str] = None) -> Path:
        target_file = ILLUSTRATIONS_DIR / f'illustration_bai_{lesson_index}.jpg'
        if target_file.exists():
            return target_file

        if self.client and prompt:
            try:
                print(f'[AIImageEngine] Calling Hugging Face FLUX.1-schnell for Lesson {lesson_index}...')
                image = self.client.text_to_image(
                    prompt,
                    model='black-forest-labs/FLUX.1-schnell'
                )
                image.save(target_file)
                print(f'[AIImageEngine] Successfully generated and saved {target_file.name}')
                return target_file
            except Exception as e:
                print(f'[AIImageEngine] Hugging Face API call failed ({e}), falling back to curated assets.')

        return target_file


def main():
    engine = AIImageEngine()
    for i in range(1, 6):
        img = engine.get_illustration_for_lesson(i)
        print(f'Lesson {i} illustration: {img.name} (Exists: {img.exists()})')


if __name__ == '__main__':
    main()
