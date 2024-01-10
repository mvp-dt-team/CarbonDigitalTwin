filename_in = 'g75-92.csv'
filename_out = 'g75-92_.csv'
with open(filename_in, 'r', encoding='utf8') as infile, open(filename_out, 'w', encoding='utf8') as outfile:
    count = 0
    for row in infile.readlines():
        if count == 0:
            count = 1
            outfile.write(row)
            continue
        clear = row.split(',')
        if float(clear[1]) < 2.01:
            outfile.write(row)