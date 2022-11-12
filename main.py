import Scanner
# sample file
str = """{ Sample program in TINY language –
computes factorial}
read x; {input an integer }
if 0 < x then { don’t compute if 
x <= 0 }
fact := 1;
repeat 
fact := (fact * x);
x := x - 1
until x = 0;
write fact { output factorial of x 
}
end """

print(Scanner.Scanner.generate_tokens(str))

