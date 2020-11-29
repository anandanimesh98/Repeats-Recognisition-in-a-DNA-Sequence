with open('sequence.fasta', 'r') as f:
    f.readline()
    data = f.read()
data = ''.join(data.split())
with open('data1.txt', 'w') as f:
    f.write(data)