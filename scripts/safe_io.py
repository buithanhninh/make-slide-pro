from __future__ import annotations

import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Any, Iterable

MAX_JSON_INPUT_BYTES = 64 * 1024 * 1024


class OutputSafetyError(ValueError):
    pass


class JsonInputError(ValueError):
    pass


class InputSafetyError(JsonInputError):
    pass


def normalized_path(path: Path | str) -> Path:
    return Path(os.path.abspath(os.path.expanduser(os.fspath(path))))


def _canonical_path(path: Path | str) -> Path:
    return normalized_path(path).resolve(strict=False)


def _comparison_key(path: Path | str) -> str:
    return os.path.normcase(os.fspath(normalized_path(path)))


def _path_is_within(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def _is_reparse_or_symlink(path: Path) -> bool:
    metadata = os.lstat(path)
    if stat.S_ISLNK(metadata.st_mode):
        return True
    attributes = getattr(metadata, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)
    return bool(attributes & reparse_flag)


def _assert_no_reparse_output_ancestors(output: Path | str) -> None:
    current = normalized_path(output).parent
    ancestors: list[Path] = []
    while True:
        ancestors.append(current)
        if current == current.parent:
            break
        current = current.parent
    for ancestor in reversed(ancestors):
        try:
            if _is_reparse_or_symlink(ancestor):
                raise OutputSafetyError(f"OUTPUT_PARENT_REPARSE_POINT:{ancestor}")
        except FileNotFoundError:
            continue


def _assert_no_reparse_input_components(input_path: Path | str) -> None:
    current = normalized_path(input_path)
    components: list[Path] = []
    while True:
        components.append(current)
        if current == current.parent:
            break
        current = current.parent
    for component in reversed(components):
        try:
            if _is_reparse_or_symlink(component):
                raise InputSafetyError(f"INPUT_REPARSE_POINT_NOT_ALLOWED:{component}")
        except FileNotFoundError:
            continue


def assert_regular_input_file(path: Path | str, *, label: str = "INPUT") -> Path:
    candidate = normalized_path(path)
    _assert_no_reparse_input_components(candidate)
    try:
        metadata = os.lstat(candidate)
    except FileNotFoundError as error:
        raise InputSafetyError(f"{label}_MISSING:{candidate}") from error
    if not stat.S_ISREG(metadata.st_mode):
        raise InputSafetyError(f"{label}_NOT_REGULAR_FILE:{candidate}")
    return candidate


def assert_safe_input_directory(path: Path | str, *, label: str = "INPUT_DIRECTORY") -> Path:
    candidate = normalized_path(path)
    _assert_no_reparse_input_components(candidate)
    try:
        metadata = os.lstat(candidate)
    except FileNotFoundError as error:
        raise InputSafetyError(f"{label}_MISSING:{candidate}") from error
    if not stat.S_ISDIR(metadata.st_mode):
        raise InputSafetyError(f"{label}_NOT_DIRECTORY:{candidate}")
    return candidate


def _assert_output_absent(output: Path) -> None:
    if os.path.lexists(output):
        raise OutputSafetyError(f"OUTPUT_ALREADY_EXISTS:{output}")


def path_is_within(path: Path | str, directory: Path | str) -> bool:
    lexical_candidate = normalized_path(path)
    lexical_root = normalized_path(directory)
    if _path_is_within(lexical_candidate, lexical_root):
        return True
    return _path_is_within(_canonical_path(path), _canonical_path(directory))


def assert_new_output(
    output: Path | str,
    *,
    protected_paths: Iterable[Path | str] = (),
    protected_directories: Iterable[Path | str] = (),
) -> Path:
    resolved_output = normalized_path(output)
    _assert_no_reparse_output_ancestors(resolved_output)
    for protected_path in protected_paths:
        if (
            _comparison_key(resolved_output) == _comparison_key(protected_path)
            or _comparison_key(_canonical_path(resolved_output))
            == _comparison_key(_canonical_path(protected_path))
        ):
            raise OutputSafetyError(f"OUTPUT_PATH_COLLISION:{resolved_output}")
    for protected_directory in protected_directories:
        if path_is_within(resolved_output, protected_directory):
            raise OutputSafetyError(f"OUTPUT_INSIDE_INPUT_DIRECTORY:{resolved_output}")
    _assert_output_absent(resolved_output)
    return resolved_output


def load_json_strict(path: Path | str) -> Any:
    def reject_constant(value: str) -> None:
        raise JsonInputError(f"NON_FINITE_JSON_NUMBER:{value}")

    def reject_duplicate_properties(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        seen: set[str] = set()
        for key, value in pairs:
            normalized_key = key.casefold()
            if normalized_key in seen:
                raise JsonInputError(f"DUPLICATE_JSON_PROPERTY:{key}")
            seen.add(normalized_key)
            result[key] = value
        return result

    resolved_path = assert_regular_input_file(path, label="JSON")
    input_size = resolved_path.stat().st_size
    if input_size > MAX_JSON_INPUT_BYTES:
        raise JsonInputError(
            f"JSON_INPUT_TOO_LARGE:{input_size}:limit={MAX_JSON_INPUT_BYTES}"
        )
    try:
        return json.loads(
            resolved_path.read_text(encoding="utf-8-sig"),
            object_pairs_hook=reject_duplicate_properties,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise JsonInputError(f"INVALID_JSON:{error.msg}:line={error.lineno}:column={error.colno}") from error


def write_json_new(payload: Any, output: Path | str) -> Path:
    resolved_output = assert_new_output(output)
    _assert_no_reparse_output_ancestors(resolved_output)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    _assert_no_reparse_output_ancestors(resolved_output)
    _assert_output_absent(resolved_output)
    text = json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        dir=resolved_output.parent,
        prefix=f".{resolved_output.name}.tmp-",
        text=True,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        _assert_no_reparse_output_ancestors(resolved_output)
        _assert_output_absent(resolved_output)
        if os.name == "nt":
            os.rename(temporary_path, resolved_output)
        else:
            os.link(temporary_path, resolved_output)
            temporary_path.unlink()
    finally:
        temporary_path.unlink(missing_ok=True)
    return resolved_output
