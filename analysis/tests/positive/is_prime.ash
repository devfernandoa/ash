bool function is_prime(int n) {
    if (n <= 1) {
        return false;
    }
    for (i in 2..(n - 1)) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

let result: bool = is_prime(7);
echo(result);
