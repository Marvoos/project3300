import sys #importing sys to access arguments
import json #importing json to use json files

#function to load data
def load_data(file_name):
    input_dict = {}
    try:
        with open(file_name, "r") as input:
            data = input.read()
            input_dict = json.loads(data)#loading the data
    except FileNotFoundError:
        print("File was not found")
        exit()
    return input_dict

#function to provide output
def output_data(results): #assuming results is a dictionary
    output_data = json.dumps(results)
    print(output_data)

#All algorithm methods
def fifo(input_dict):
    results = {}
    #write fifo algorithm here
    return results

def sjf(input_dict):
    results = {}
    #write sjf algorithm here
    return results

def round_robin(input_dict):
    results = {}
    #write round robin algorithm here
    return results

def priority(input_dict):
    results = {}
    #write priority algorithm here
    return results

file_name = sys.argv[1] #the input filename

input_dict = load_data(file_name) #calling the function
results = {} #dict for results
if(input_dict["policy"].upper()=="FIFO"):
    results = fifo(input_dict)
elif(input_dict["policy"].upper()=="SJF"):
    results = sjf(input_dict)
elif(input_dict["policy"].upper()=="RR"):
    results = round_robin(input_dict)
elif(input_dict["policy"].upper()=="PRIORITY"):
    results = priority(input_dict)
else:
    print("It's not part of our policies")


output_data(results) #outputing data