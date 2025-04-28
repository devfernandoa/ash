# Ash

Ash is a statically typed, minimalistic scripting language designed to simplify and replace complex Bash scripts.

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
