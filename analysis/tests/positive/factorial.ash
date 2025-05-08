int function fact(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * fact(n - 1);
}

let result: int = fact(5);
echo(result);