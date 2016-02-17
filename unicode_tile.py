
import sys

# U+1F000 ~ U+1F003
# U+1F004 ~ U+1F006

# U+1F007 ~ U+1F00F
# U+1F010 ~ U+1F018
# U+1F019 ~ U+1F021

codes = [0x1F000, 0x1F001, 0x1F002, 0x1F003, 0x1F004, 0x1F005, 0x1F006]
numbers = [[0x1F007+i+e*9 for i in range(0,9)] for e in range(0,3)]

print(numbers)
for code in codes:
	sys.stdout.buffer.write(chr(code).encode("utf-8"))
	print()

for x in numbers:
	for code in x:
		sys.stdout.buffer.write(chr(code).encode("utf-8"))
		print()

		