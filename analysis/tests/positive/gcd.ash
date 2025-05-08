int function gcd(int a, int b) {
    while (b != 0) {
        let temp: int = b;
        b = a % b;
        a = temp;
    }
    return a;
}

let result: int = gcd(48, 18);
echo(result);