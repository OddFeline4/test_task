import csv
def load_data(full_file,head_file,output_file):
    with open(full_file) as input_file, open(head_file) as input_head,\
            open(output_file,'w') as output_file:
        reader = csv.DictReader(input_file)
        writer = [str([exp['GUID'],exp['Timestamp'],
                   exp['OuterIP'],exp['NgToken']]).replace('[','(').replace(']',')') for exp in reader]
        data_string = ',\n'.join(writer)
        head_string = input_head.read()
        output_file.write(head_string)
        output_file.write(data_string)


