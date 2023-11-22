#os and sys are just libraries that allow me to manipulate with the enviroment on my machine
import os
import sys
#ive used heap because of its property to pop the smallest item off the heap, maintaining the heap invariant.
import heapq
#ive used json to convert dictionary to string to represent the Huffman Tree
import json

class Huffman:
    def __init__(self, path):
        #the path of the file
        self.path = path 
        #list of nodes
        self.nodes = []
        #dictionary of indexes related to nodes
        self.indexes = {}
        self.indexes_for_decompression = {}

    class Node:
        def __init__(self,char,freq):
            #characters that will be nodes of the tree
            self.char = char
            #frequency that is assigned to those characters
            self.freq = freq 
            #right and left attributes for making the tree
            self.right = None
            self.left = None

        #compare the 2 characters frequencies to build the correct Huffman tree (less then)
        def __lt__(self,char):
            return self.freq < char.freq

        #compare the 2 characters frequencies to build the correct Huffman tree (greater then)
        def __gt__(self,char):
            return self.freq > char.freq
        
        #compare the 2 characters frequencies to find out if 2 frequencies are equal
        def __eq__(self, char):
            if (char == None) or (not isinstance(char,Node)):
                return False
            return self.freq == char.freq

    #calculate frequency 
    def make_freq_dictionary(self, txt):
        #make a frequency dictinary
        freq = {}
        #look through the text
        for char in txt:
            #if some charachter is not in the frequency than its frequency is 0
            if not char in freq:
                freq[char] = 0 
            #otherwise calculate how many specific characters exist in the file
            freq[char] += 1
        #return the dictionary of characters and frequensies
        return freq

    #make a priority queue
    def make_nodes_queue(self, freq):
        #for every charater
        for index in freq:
            #build a node 
            node = self.Node(index, freq[index])
            #push it to a heap, and populate self.nodes
            heapq.heappush(self.nodes, node)

    #build a huffman tree 
    def build_tree(self):
        #for every node in the node queue
        while(len(self.nodes)>1):
            #we take 2 nodes with smallest frequencies 
            x = heapq.heappop(self.nodes)
            y = heapq.heappop(self.nodes)

            #we merge them together where x and y are children in the tree
            #process of making a HUFFMAN tree
            z = self.Node(None, x.freq + y.freq)
            z.left = x
            z.right = y

            #add the node z to the heap
            heapq.heappush(self.nodes, z)

    #make unique indexes for charachters
    def make_index(self, node, current_index):
        if node == None:
            return False
        if node.char != None:
            self.indexes[node.char] = current_index
            self.indexes_for_decompression[current_index] = node.char

        #recursion to make unique indexes for the nodes

        #left appends 0 to a nodes index
        self.make_index(node.left, current_index + "0")
        #right appends 1 to a nodes index
        self.make_index(node.right, current_index + "1")

    #make unique indexes for charachters
    def assign_index(self):
        #take a node from the heap
        root_node = heapq.heappop(self.nodes)
        #make an index variable
        root_index = ""
        #make the index for the root node
        self.make_index(root_node, root_index)
    
    #replace the characters with indexes
    def replace_text(self,txt):
        #make a varibale for encoded text 
        encoded_text = ""
        #for every charachter in the text 
        for char in txt:
            #append the node to the text
            encoded_text += self.indexes[char]
        #return the text
        return encoded_text

    #pad encoded text
    def standardise_encoded_text(self, encoded_text):
        #need to make length of indexes the same
        #to do that we add extra padding to the text

        #find out how much we need
        extra_padding = 8 - len(encoded_text) % 8 
        #add that to the text
        for i in range(0,extra_padding):
            encoded_text += "0"

        #use the correct foramtting
        padding_information = "{0:08b}".format(extra_padding)
        #add the padding inforamtion to the text
        encoded_text = padding_information + encoded_text
        return encoded_text

    #convert the text into bytes
    def convert_to_bytes(self, pad_encoded_text):
        #first we need the bytearray
        byts = bytearray()
        #for every string in our text 
        for i in range(0,len(pad_encoded_text), 8):
            #we find 1 byte 
            byte = pad_encoded_text[i:i+8]
            #covert to integer
            #and append it to our arraylist
            byts.append(int(byte,2))
        #return the arraylist
        return byts

    #compress the file 
    def compress(self):
        #get filename
        filename, file_extension = os.path.splitext(self.path)
        #give a different directory to store the bin and decopressed files
        flnm = filename.split("/")[-1]
        output_path = "compressed/" + flnm + ".bin"

        #try-except statment for handling errors
        try:
            #open the file with the correct path
            with open(self.path, 'r') as file, open (output_path, 'wb') as output:
                #get the text 
                txt = file.read()
                txt = txt.rstrip()

                #apply all additional functions in the correct order
                freq = self.make_freq_dictionary(txt)
                self.make_nodes_queue(freq)
                self.build_tree()
                self.assign_index()
                encoded_txt = self.replace_text(txt)
                pad_encoded_txt = self.standardise_encoded_text(encoded_txt)
                byte_file = self.convert_to_bytes(pad_encoded_txt)
                output.write(bytes(byte_file))

                #get the file with bytes in the end

            #return the output_path
            print("FILE SUCCESFULLY COMPRESSED")
            return output_path

        except :
            print("Could not compress the file")
            sys.exit()

    #remove padding from the binary text
    def remove_padding(self, bit_txt):
        #getting the padding inforamation from the original text
        padding_information = bit_txt[:8]
        #figuring out the extra padding of the text
        #converting it to integer
        extra_padding = int(padding_information,2)
        #we need the bit text, each 8 numbers for byte
        bit_txt = bit_txt[8:]
        #finaly get the encoded text of using the padding knowledge 
        #that we have
        encoded_txt = bit_txt[:-1*extra_padding]

        #return the text
        return encoded_txt

    #decode back the original file 
    def decode_text(self, txt):
        #make a varible for indexes of the charachters
        current_index = ""
        #make a varaible for the output of the text
        final_decoded_text = ""

        #for every bit in our text
        for bit in txt:
            #we get the current index
            current_index += bit
            #and if the index is in the dictionary of the indexes
            if current_index in self.indexes_for_decompression:
                #we assign the value of this index to a character
                char = self.indexes_for_decompression[current_index]
                #we populate the decoded text with characters 
                final_decoded_text += char
                #need to make index empty to continue the for loop
                current_index = ""

        #return the decoded text
        return final_decoded_text


    def decompress(self, path):
        #get filename
        filename, file_extension = os.path.splitext(self.path)
        #give a different directory to store the bin and decopressed files
        flnm = filename.split("/")[-1]
        output_path = "compressed/" + flnm + "_decompressed" + ".txt"

        #try-except statment for handling errors
        try:
            with open(path, 'rb') as file, open (output_path, 'w') as output:
                #make a variable for the bit text
                bit_txt = ""
                #read the text 1 byte by 1
                byte = file.read(1)
                #while byte has is greater than 0
                #keep reading the bytes
                while (len(byte)>0):
                    #find out the integer value of unicode 
                    byte = ord(byte)
                    #returns the binary representation of byte 
                    bits = bin(byte)[2:].rjust(8, '0')
                    #apped the text with the bits
                    bit_txt += bits
                    #read the next byte
                    byte = file.read(1) 

                #use our additional functions
                encoded_txt = self.remove_padding(bit_txt) 
                decoded_txt = self.decode_text(encoded_txt)

                #return the decoded text
                output.write(decoded_txt)

            #return the output_path
            print("FILE SUCCESFULLY DECOMPRESSED")
            return output_path

        except :
            print("Could not decompress the file")
            sys.exit()
    
    #the function to copy the Huffman Tree to a txt file
    def get_the_tree(self):
        #open the file 
        f = open("HuffmanTree.txt","w+")
        #converting the dictinary to string
        tree = json.dumps(self.indexes)
        #populate the text file
        f.write(tree)
    
      

