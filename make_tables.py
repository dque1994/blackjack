__author__ = 'miller'
__guy_who_looked_over_Jims_shoulder_and_also_wrote_some_cool_stuff__ = 'que'

######################## THIS MODULE READS IN DATA FROM .TXT FILES SO THEY CAN BE USED AS ARRAYS #######################

####### EVERY FUNCTION WILL BE PREFACED WITH A BASIC DESCRIPTION AS WELL AS THE ARGUMENTS AND THE RETURN VALUE #########
import csv

#Function parses data from a tab-delimited .txt file
#ARGS: tab-delimited .txt file
#RETURN: array of data
def read_table_file(file):
    table = []

    f = open(file,'r')
    g = csv.reader(f,delimiter='\t')
    for line in g:

        table_line = []
        for element in line:

            number_test = float(element)
            if number_test <= 0:
                table_line.append(False)
            else:
                table_line.append(True)
        table.append(table_line)

    return table
