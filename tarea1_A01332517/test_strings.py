from myregex import email, phone_number, hexadecimal

assert email("abdul@tec.mx") == True
assert email("abdultec.mx") == False
assert email("bastian.baltasar.bux@fantasia.com.mx") == True
assert email("bastian.baltasar.bux@fantasia..com.mx") == False
assert email("@hsbc.com") == False
assert email("example@com.") == False

assert phone_number("+1 (52) 55 4433 2211") == True
assert phone_number("+1(52)5544332211") == True
assert phone_number("+1(52)554432211") == False
assert phone_number("5544332211") == True

assert hexadecimal("hexadecimal") == False
assert hexadecimal("0x0f0fab34") == True
assert hexadecimal("0x0f0fah34") == False
assert hexadecimal("0a0f0fa134") == False
assert hexadecimal("0x0F0FAB34") == True