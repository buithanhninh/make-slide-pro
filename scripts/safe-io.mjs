import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

const MAX_JSON_INPUT_BYTES = 64 * 1024 * 1024;

export class JsonInputError extends Error {
  constructor(message) {
    super(message);
    this.name = "JsonInputError";
  }
}

export class InputPathError extends JsonInputError {
  constructor(message) {
    super(message);
    this.name = "InputPathError";
  }
}

export function normalizedPath(value) {
  return path.resolve(value);
}

export function pathIsWithin(value, directory) {
  const candidate = normalizedPath(value);
  const root = normalizedPath(directory);
  const relative = path.relative(root, candidate);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function comparisonKey(value) {
  const normalized = normalizedPath(value);
  return process.platform === "win32" ? normalized.toLowerCase() : normalized;
}

async function assertNoReparseOutputAncestors(output) {
  let current = path.dirname(normalizedPath(output));
  const ancestors = [];
  while (true) {
    ancestors.push(current);
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  for (const ancestor of ancestors.reverse()) {
    try {
      const metadata = await fs.lstat(ancestor);
      if (metadata.isSymbolicLink()) {
        throw new Error(`OUTPUT_PARENT_REPARSE_POINT:${ancestor}`);
      }
      if (process.platform === "win32") {
        const canonical = await fs.realpath(ancestor);
        if (comparisonKey(canonical) !== comparisonKey(ancestor)) {
          throw new Error(`OUTPUT_PARENT_REPARSE_POINT:${ancestor}`);
        }
      }
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
}

async function assertNoReparseInputComponents(input) {
  let current = normalizedPath(input);
  const components = [];
  while (true) {
    components.push(current);
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  for (const component of components.reverse()) {
    try {
      const metadata = await fs.lstat(component);
      if (metadata.isSymbolicLink()) {
        throw new InputPathError(`INPUT_REPARSE_POINT_NOT_ALLOWED:${component}`);
      }
      if (process.platform === "win32") {
        const canonical = await fs.realpath(component);
        if (comparisonKey(canonical) !== comparisonKey(component)) {
          throw new InputPathError(`INPUT_REPARSE_POINT_NOT_ALLOWED:${component}`);
        }
      }
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
}

export async function assertRegularInputFile(input, label = "INPUT") {
  const resolvedInput = normalizedPath(input);
  await assertNoReparseInputComponents(resolvedInput);
  let metadata;
  try {
    metadata = await fs.lstat(resolvedInput);
  } catch (error) {
    if (error?.code === "ENOENT") {
      throw new InputPathError(`${label}_MISSING:${resolvedInput}`);
    }
    throw error;
  }
  if (!metadata.isFile()) {
    throw new InputPathError(`${label}_NOT_REGULAR_FILE:${resolvedInput}`);
  }
  return resolvedInput;
}

async function assertOutputAbsent(output) {
  try {
    await fs.lstat(output);
    throw new Error(`OUTPUT_ALREADY_EXISTS:${output}`);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
}

function assertNoDuplicateJsonProperties(text) {
  let index = 0;
  const skipWhitespace = () => {
    while (/\s/u.test(text[index] ?? "")) index += 1;
  };
  const parseString = () => {
    const start = index;
    index += 1;
    let escaped = false;
    while (index < text.length) {
      const character = text[index];
      index += 1;
      if (escaped) {
        escaped = false;
      } else if (character === "\\") {
        escaped = true;
      } else if (character === '"') {
        return JSON.parse(text.slice(start, index));
      }
    }
    throw new JsonInputError("INVALID_JSON:UNTERMINATED_STRING");
  };
  const parseValue = () => {
    skipWhitespace();
    if (text[index] === "{") {
      parseObject();
    } else if (text[index] === "[") {
      parseArray();
    } else if (text[index] === '"') {
      parseString();
    } else {
      while (index < text.length && !/[\s,}\]]/u.test(text[index])) index += 1;
    }
    skipWhitespace();
  };
  const parseObject = () => {
    const seen = new Set();
    index += 1;
    skipWhitespace();
    if (text[index] === "}") {
      index += 1;
      return;
    }
    while (index < text.length) {
      const key = parseString();
      const normalizedKey = key.toLowerCase();
      if (seen.has(normalizedKey)) {
        throw new JsonInputError(`DUPLICATE_JSON_PROPERTY:${key}`);
      }
      seen.add(normalizedKey);
      skipWhitespace();
      index += 1;
      parseValue();
      if (text[index] === "}") {
        index += 1;
        return;
      }
      index += 1;
      skipWhitespace();
    }
  };
  const parseArray = () => {
    index += 1;
    skipWhitespace();
    if (text[index] === "]") {
      index += 1;
      return;
    }
    while (index < text.length) {
      parseValue();
      if (text[index] === "]") {
        index += 1;
        return;
      }
      index += 1;
      skipWhitespace();
    }
  };
  parseValue();
}

export function parseJsonStrict(text) {
  const normalizedText = text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  let payload;
  try {
    payload = JSON.parse(normalizedText);
  } catch (error) {
    throw new JsonInputError(`INVALID_JSON:${error.message}`);
  }
  assertNoDuplicateJsonProperties(normalizedText);
  return payload;
}

export async function loadJsonStrict(input) {
  const resolvedInput = await assertRegularInputFile(input, "JSON");
  const inputSize = (await fs.stat(resolvedInput)).size;
  if (inputSize > MAX_JSON_INPUT_BYTES) {
    throw new JsonInputError(`JSON_INPUT_TOO_LARGE:${inputSize}:limit=${MAX_JSON_INPUT_BYTES}`);
  }
  return parseJsonStrict(await fs.readFile(resolvedInput, "utf8"));
}

export async function assertNewOutput(output, { protectedPaths = [], protectedDirectories = [] } = {}) {
  const resolvedOutput = normalizedPath(output);
  await assertNoReparseOutputAncestors(resolvedOutput);
  for (const protectedPath of protectedPaths) {
    if (resolvedOutput.toLowerCase() === normalizedPath(protectedPath).toLowerCase()) {
      throw new Error(`OUTPUT_PATH_COLLISION:${resolvedOutput}`);
    }
  }
  for (const protectedDirectory of protectedDirectories) {
    if (pathIsWithin(resolvedOutput, protectedDirectory)) {
      throw new Error(`OUTPUT_INSIDE_INPUT_DIRECTORY:${resolvedOutput}`);
    }
  }
  await assertOutputAbsent(resolvedOutput);
  return resolvedOutput;
}

export async function writeJsonNew(payload, output) {
  const resolvedOutput = await assertNewOutput(output);
  await assertNoReparseOutputAncestors(resolvedOutput);
  await fs.mkdir(path.dirname(resolvedOutput), { recursive: true });
  await assertNoReparseOutputAncestors(resolvedOutput);
  await assertOutputAbsent(resolvedOutput);
  const temporaryPath = path.join(
    path.dirname(resolvedOutput),
    `.${path.basename(resolvedOutput)}.tmp-${crypto.randomUUID().replaceAll("-", "")}`,
  );
  const text = `${JSON.stringify(payload, null, 2)}\n`;
  try {
    await fs.writeFile(temporaryPath, text, { encoding: "utf8", flag: "wx" });
    await assertNoReparseOutputAncestors(resolvedOutput);
    await assertOutputAbsent(resolvedOutput);
    await fs.link(temporaryPath, resolvedOutput);
  } finally {
    await fs.rm(temporaryPath, { force: true });
  }
  return resolvedOutput;
}
