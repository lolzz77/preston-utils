hex_string = input("Enter a hexadecimal string: ")

# Convert hexadecimal string to bytes
hex_bytes = bytes.fromhex(hex_string)

# Convert bytes to ASCII string
ascii_string = hex_bytes.decode('ASCII')

print("The ASCII representation of", hex_string, "is:", ascii_string)
