import sys
output_path = sys.argv[1]
output_file = ''
for input_path in sys.argv[2:]:
    with open(input_path, 'r') as f:
        output_file += f.read()
with open(output_path, 'w') as f:
    f.write(output_file)
