import collections
import string
import re
import argparse, sys, getopt


#read input file - reference https://machinelearningmastery.com/clean-text-machine-learning-python/
def file_in(input_file):
    try:
        with open(input_file, errors='ignore') as my_file:
            text = my_file.read()
            words = text.split()
            words = [word.lower() for word in words]
            table = str.maketrans('', '', string.punctuation)
            stripped = [w.translate(table) for w in words]
            final_list = regex(stripped)
            return final_list
    except FileNotFoundError:
        print("Unable to locate input file")



# This method is only used when reading the file
def regex(word_list):
    clean_list = []
    for i in word_list:
        clean = re.sub('\d', "", i)
        clean_list.append(clean)

    clean_list = list(filter(None, clean_list))
    return clean_list


# refrence https://stackoverflow.com/questions/27466350/recursive-python-function-to-count-occurrences-of-an-element-in-a-list
def recsiveCount(words,key):
    if not words:
        return 0

    if words[0] == key:
        return 1 + recsiveCount(words[1:], key)
    else:
        return 0 + recsiveCount(words[1:],key)




def count_all(words,solution = {}):
    if not words:
        return solution;
    elif(len(words) == 0):
        return solution
    else:
        key = words[0]
        value = recsiveCount(words,key)
        if key not in solution:
            solution.update({key:value})
        words.pop(0)
        count_all(words)
    return solution


#used only to display answer
def printK(my_dict, k,output):
    my_dict = sorted(my_dict.items(), key=lambda x:x[1], reverse=True)
    my_dict = collections.OrderedDict(my_dict)
    freq_list = my_dict.values()
    freq_list = list(freq_list)
    i = 0
    with open(output, "w") as out_f:

        for key, value in my_dict.items():
            if(k == 0):
                break
            else:
                if(i < len(freq_list)-1):

                    if(value == freq_list[i+1]):
                        k = k
                    else:
                        k -= 1
                print(key,value)
                out_f.write(key + " " + str(value) + '\n')
                i += 1


def main():
    sys.setrecursionlimit(3050)
    parser = argparse.ArgumentParser(description= "topksearch")
    parser.add_argument('input', help="input=input.txt;k=n;output=output.txt")
    args = parser.parse_args()
    parseArgument = args.input.split(';')
    finalArguments = []
    if not parseArgument:
        print("Please run using correct format")
    else:
        #Used only to parse arguments
        for argument in parseArgument:
            clean_arg = argument.split('=')
            finalArguments.append(clean_arg)
        try:
            input_file = finalArguments[0][1]
            output_file = finalArguments[2][1]
            k = finalArguments[1][1]
        except IndexError:
            print("Correctly enter the input parameters type -h for help")
            print("input=input.txt;k=2;ouput=topkword.txt")
            return 0
        all_words = file_in(input_file)
        if not all_words:
            print("Text file is empty")
            with open(output_file, 'a') as out_f:
                pass
        else:
            try:
                sol = count_all(all_words)
                printK(sol,abs(int(k)),output_file)
            except ValueError:
                print("No k found")


if __name__ == "__main__":
    main()
