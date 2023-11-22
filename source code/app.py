import sys
#import the Huffman Algorithm
from huffman import Huffman

#ask the user to input file path
print("Please enter the path to the file for compression (with .txt)")
path = input()

#make an object of the Huffman Class
hffmn = Huffman(path)

#simple interface for the user 
flag = 0
while flag == 0:
    print("Enter 'compress' to compress the file, or enter 'decompress' to decompress the file")
    print("Enter 'exit' to exit")
    user_in = input()
    if user_in == "compress":
        #compress the file 
        out = hffmn.compress()
        #make the Huffman Tree of the text 
        hffmn.get_the_tree()
        flag = 0
    elif user_in == "decompress":
        #decompress the file 
        hffmn.decompress(out)
        flag = 0
    elif user_in == "exit":
        #exit from the system
        sys.exit()
    