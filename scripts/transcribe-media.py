from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_io import OutputSafetyError, assert_new_output, assert_regular_input_file, normalized_path, write_json_new


CRITICAL_TOKEN_PATTERN = re.compile(r"(?:\b\d[\d,.]*\b|\b\d+(?:\.\d+)?%|\$\s?[\d,.]+|€\s?[\d,.]+|₫\s?[\d,.]+|\b(?:19|20)\d{2}\b)")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def finite_number(value: Any, label: str) -> float:
    result = float(value)
    if not __import__("math").isfinite(result):
        raise ValueError(f"NON_FINITE_TRANSCRIPT_VALUE:{label}")
    return result


def critical_tokens(text: str) -> list[str]:
    return CRITICAL_TOKEN_PATTERN.findall(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe local audio/video for Make Slide Pro.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--language")
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_glossary(path: Path | None) -> str | None:
    if not path:
        return None
    safe_path = assert_regular_input_file(path, label="GLOSSARY_FILE")
    terms = [line.strip() for line in safe_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    return ", ".join(terms) if terms else None


def word_payload(word: Any) -> dict[str, object]:
    return {
        "start_ms": round(finite_number(word.start, "word.start") * 1000),
        "end_ms": round(finite_number(word.end, "word.end") * 1000),
        "word": str(word.word),
        "probability": None if getattr(word, "probability", None) is None else finite_number(word.probability, "word.probability"),
    }


def transcribe(args: argparse.Namespace) -> dict[str, object]:
    from faster_whisper import WhisperModel

    glossary = load_glossary(args.glossary)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(
        str(args.input),
        language=args.language,
        beam_size=args.beam_size,
        word_timestamps=True,
        vad_filter=True,
        condition_on_previous_text=True,
        hotwords=glossary,
    )
    serialized_segments: list[dict[str, object]] = []
    for segment in segments:
        text = str(segment.text).strip()
        words = [word_payload(word) for word in (segment.words or [])]
        flags: list[str] = []
        avg_logprob = finite_number(segment.avg_logprob, "segment.avg_logprob")
        no_speech_prob = finite_number(segment.no_speech_prob, "segment.no_speech_prob")
        compression_ratio = finite_number(segment.compression_ratio, "segment.compression_ratio")
        start_ms = round(finite_number(segment.start, "segment.start") * 1000)
        end_ms = round(finite_number(segment.end, "segment.end") * 1000)
        if avg_logprob < -1.0:
            flags.append("LOW_AVG_LOGPROB")
        if no_speech_prob > 0.6:
            flags.append("HIGH_NO_SPEECH_PROB")
        if compression_ratio > 2.4:
            flags.append("HIGH_COMPRESSION_RATIO")
        if critical_tokens(text):
            flags.append("CRITICAL_TOKEN_REVIEW")
        serialized_segments.append(
            {
                "segment_id": f"seg-{len(serialized_segments) + 1:05d}",
                "start_ms": start_ms,
                "end_ms": end_ms,
                "text": text,
                "avg_logprob": avg_logprob,
                "no_speech_prob": no_speech_prob,
                "compression_ratio": compression_ratio,
                "words": words,
                "critical_tokens": critical_tokens(text),
                "risk_flags": flags,
                "verification_state": "REVIEW_REQUIRED" if flags else "UNVERIFIED",
            }
        )
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_path": str(args.input.resolve()),
        "model": args.model,
        "device": args.device,
        "compute_type": args.compute_type,
        "language": getattr(info, "language", None),
        "language_probability": None if getattr(info, "language_probability", None) is None else finite_number(info.language_probability, "language_probability"),
        "duration_seconds": None if getattr(info, "duration", None) is None else finite_number(info.duration, "duration_seconds"),
        "segments": serialized_segments,
        "speaker_policy": "DO_NOT_ASSIGN_NAMES_WITHOUT_SEPARATE_DIARIZATION_EVIDENCE",
        "status": "REVIEW_REQUIRED" if any(item["risk_flags"] for item in serialized_segments) else "UNVERIFIED",
    }


def main() -> int:
    args = parse_args()
    input_path = normalized_path(args.input)
    output_path = normalized_path(args.output)
    glossary_path = normalized_path(args.glossary) if args.glossary else None
    if input_path == output_path or (glossary_path is not None and glossary_path == output_path):
        payload = {
            "schema_version": "1.0",
            "status": "BLOCKED",
            "error": "SOURCE_OUTPUT_PATH_COLLISION",
            "input_path": str(input_path),
            "output_path": str(output_path),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2
    try:
        input_path = assert_regular_input_file(input_path, label="INPUT_MEDIA")
        if args.beam_size <= 0:
            raise ValueError("INVALID_BEAM_SIZE")
        if glossary_path:
            glossary_path = assert_regular_input_file(glossary_path, label="GLOSSARY_FILE")
        output_path = assert_new_output(output_path, protected_paths=[input_path, *( [glossary_path] if glossary_path else [] )])
    except (OSError, OutputSafetyError, ValueError) as error:
        payload = {
            "schema_version": "1.0",
            "status": "BLOCKED",
            "input_path": str(input_path),
            "output_path": str(output_path),
            "error": str(error),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        try:
            write_json_new(payload, output_path)
        except (OSError, OutputSafetyError):
            pass
        return 2
    try:
        args.input = input_path
        args.output = output_path
        args.glossary = glossary_path
        input_hash_before = file_sha256(input_path)
        if args.dry_run:
            payload = {
                "schema_version": "1.0",
                "status": "DRY_RUN",
                "input_path": str(input_path),
                "input_sha256": input_hash_before,
                "model": args.model,
                "device": args.device,
                "compute_type": args.compute_type,
                "language": args.language,
                "would_use_vad": True,
                "would_emit_word_timestamps": True,
            }
        else:
            payload = transcribe(args)
            input_hash_after = file_sha256(input_path)
            payload["input_sha256"] = input_hash_before
            payload["input_sha256_after"] = input_hash_after
            if input_hash_before != input_hash_after:
                payload["status"] = "BLOCKED"
                payload["error"] = "INPUT_CHANGED_DURING_TRANSCRIPTION"
        write_json_new(payload, output_path)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if payload["status"] == "BLOCKED":
            return 2
        return 0 if payload["status"] == "DRY_RUN" else 3
    except (OSError, ImportError, RuntimeError, TypeError, ValueError) as error:
        payload = {
            "schema_version": "1.0",
            "status": "UNVERIFIED",
            "input_path": str(input_path),
            "output_path": str(output_path),
            "error": str(error),
        }
        try:
            write_json_new(payload, output_path)
        except (OSError, OutputSafetyError):
            pass
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
