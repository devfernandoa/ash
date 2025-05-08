# Ash

Ash is a statically typed, minimalistic scripting language designed to simplify and replace complex Bash scripts.
It compiles natively to bash allowing you to run your scripts as a sh script.

## Features

- Static typing (`int`, `string`, `bool`)
- Clean, simple syntax
- Support for `for` and `while` loops
- Inline terminal command execution with `!`
- Built-in `echo` and `scan` functions

## Example

```ash
let name: string = read(string);

echo("Hello, " + name);

for (i in 0..5) {
    echo(i);
}

let ready: bool = true;

while (ready) {
    echo("Running...");
    ready = false;
}

!ls -la

```

## Usage

### Compile Ash source to Bash

From the root of the `analysis` directory:

```bash
python3 semantic/main.py <source.ash> <output.sh>
```

Example:

```bash
python3 semantic/main.py tests/positive/fibonacci.ash fibonacci.sh
```

This generates a Bash script and makes it executable.

### Run the generated Bash script

```bash
./fibonacci.sh
```

### Run all tests

```bash
cd analysis
chmod +x tests/run-tests.sh
./tests/run-tests.sh
```

This will compile and run all tests under `tests/positive/` and `tests/negative/`, comparing outputs and validating correctness.

## EBNF

The EBNF for the language is available on EBNF.txt
