import subprocess
import sys
import os
from parser import AshParser  # Your working Python compiler

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <source.ash> <output.sh>")
        sys.exit(1)

    source = sys.argv[1]
    output = sys.argv[2]

    # ✅ Step 1: Syntax check using Flex/Bison
    with open(source, 'r') as src_file:
        result = subprocess.run(["./ash"], stdin=src_file, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Syntax error:")
        print(result.stderr or result.stdout)
        sys.exit(1)

    print("✅ Syntax OK — continuing with compilation...")

    # ✅ Step 2: Compile using your Python AST → Bash generator
    with open(source) as f:
        code = f.read()

    try:
        ast = AshParser(code).parse()
        bash_code = ast.generate()

        with open(output, "w") as out_file:
            out_file.write("#!/bin/bash\n" + bash_code)

        os.chmod(output, 0o755)
        print(f"✅ Compilation successful. Output written to {output}")
    except Exception as e:
        print("❌ Semantic or generation error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
