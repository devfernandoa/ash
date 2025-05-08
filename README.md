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

## EBNF

The EBNF for the language is available on EBNF.txt

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

## Installation

If you just want to use the Ash compiler, a prebuilt binary is available:

```
./build/dist/ashc
```

You can compile Ash code using:

```bash
./build/dist/ashc <source.ash> <output.sh>
```

Make sure the binary has execute permission:

```bash
chmod +x ./build/dist/ashc
```

If you wish to install it globally, you can copy the binary to a directory in your `PATH`, such as `/usr/local/bin`:

```bash
sudo cp ./build/dist/ashc /usr/local/bin/ashc
```

Then you can run it from anywhere:

```bash
ashc <source.ash> <output.sh>
```

## Building from Source

If you want to build the Ash compiler from source, you'll need Python 3 and `pyinstaller`.

### Install pyinstaller

```bash
pip install pyinstaller
```

### Build the CLI tool

From inside the `analysis/semantic` directory, run:

```bash
pyinstaller --onefile -n ashc main.py
```

This will generate the binary in:

```
./build/dist/ashc
```

You can then use `ashc` like:

```bash
./build/dist/ashc mycode.ash out.sh
./out.sh
```
