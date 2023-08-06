import math

def init_string_swap(n, init_string):
    for i in range(0, len(init_string), 2 ** (n + 1)):
        for j in range(i + (2 ** (n - 1)), i + 2 ** (n)):
            index_1 = j
            index_2 = j + (2 ** (n - 1))
            init_string[index_1], init_string[index_2] = init_string[index_2], init_string[index_1]

def swap_down(index_in, list_in, init_string_original):
    list_in[index_in], list_in[index_in -
                               1] = list_in[index_in - 1], list_in[index_in]
    init_string_swap(index_in, init_string_original)

def match_by_swapping(list_original, list_altered, init_string_original):
    init_string_copy = init_string_original.copy()
    list_original_copy = list_original.copy()
    for num in list_altered:
        index_original = list_original_copy.index(num)
        index_altered = list_altered.index(num)
        if index_original == index_altered:
            pass
        else:
            num_swaps = index_original - index_altered
            for i in range(num_swaps):
                swap_down(index_original - i, list_original_copy,
                          init_string_copy)
    return init_string_copy

def resize_lut(init_string_to_resize, new_size):
    original_size = math.log(len(init_string_to_resize), 2)
    init_string_copy = init_string_to_resize.copy()
    while original_size != new_size:
        init_string_copy = init_string_copy + init_string_copy
        original_size = original_size + 1
    return init_string_copy

def listToString(init_string_list_form):
    binaryStringForm = ""
    for element in init_string_list_form:
        if element == '0':
            binaryStringForm = binaryStringForm + '0'
        else:
            binaryStringForm = binaryStringForm + '1'
    return binaryStringForm

def binStringToList(init_string_string_form):
    binarylistForm = []
    for element in init_string_string_form:
        if element == "0":
            binarylistForm.append('0')
        else:
            binarylistForm.append('1')
    return binarylistForm

def binaryStringToHexString(init_binary_string_form):
    hexString = "0x"
    for i in range(0, len(init_binary_string_form), 4):
        if init_binary_string_form[i:i+4] == '0000':
            hexString = hexString + '0'
        elif init_binary_string_form[i:i+4] == '0001':
            hexString = hexString + '1'
        elif init_binary_string_form[i:i+4] == '0010':
            hexString = hexString + '2'
        elif init_binary_string_form[i:i+4] == '0011':
            hexString = hexString + '3'
        elif init_binary_string_form[i:i+4] == '0100':
            hexString = hexString + '4'
        elif init_binary_string_form[i:i+4] == '0101':
            hexString = hexString + '5'
        elif init_binary_string_form[i:i+4] == '0110':
            hexString = hexString + '6'
        elif init_binary_string_form[i:i+4] == '0111':
            hexString = hexString + '7'
        elif init_binary_string_form[i:i+4] == '1000':
            hexString = hexString + '8'
        elif init_binary_string_form[i:i+4] == '1001':
            hexString = hexString + '9'
        elif init_binary_string_form[i:i+4] == '1010':
            hexString = hexString + 'A'
        elif init_binary_string_form[i:i+4] == '1011':
            hexString = hexString + 'B'
        elif init_binary_string_form[i:i+4] == '1100':
            hexString = hexString + 'C'
        elif init_binary_string_form[i:i+4] == '1101':
            hexString = hexString + 'D'
        elif init_binary_string_form[i:i+4] == '1110':
            hexString = hexString + 'E'
        elif init_binary_string_form[i:i+4] == '1111':
            hexString = hexString + 'F'
    return hexString

def hexStringToBinary(initStringHexForm):
    initStringCopy = ""
    binaryString = ""
    if initStringHexForm[:2] == "0x":
        initStringCopy = initStringHexForm[2:]
    else:
        initStringCopy = initStringHexForm
    for c in initStringCopy:
        if c == '0':
            binaryString = binaryString + '0000'
        elif c == '1':
            binaryString = binaryString + '0001'
        elif c == '2':
            binaryString = binaryString + '0010'
        elif c == '3':
            binaryString = binaryString + '0011'
        elif c == '4':
            binaryString = binaryString + '0100'
        elif c == '5':
            binaryString = binaryString + '0101'
        elif c == '6':
            binaryString = binaryString + '0110'
        elif c == '7':
            binaryString = binaryString + '0111'
        elif c == '8':
            binaryString = binaryString + '1000'
        elif c == '9':
            binaryString = binaryString + '1001'
        elif c == 'A':
            binaryString = binaryString + '1010'
        elif c == 'B':
            binaryString = binaryString + '1011'
        elif c == 'C':
            binaryString = binaryString + '1100'
        elif c == 'D':
            binaryString = binaryString + '1101'
        elif c == 'E':
            binaryString = binaryString + '1110'
        elif c == 'F':
            binaryString = binaryString + '1111'
    return binaryString

def rapidWriteL2PtoAbcdefList(hm):
    strManipDict = {}
    strManipDict["[A1]"] = "a"
    strManipDict["[A2]"] = "b"
    strManipDict["[A3]"] = "c"
    strManipDict["[A4]"] = "d"
    strManipDict["[A5]"] = "e"
    strManipDict["[A6]"] = "f"

    ins = ["I0", "I1", "I2", "I3", "I4", "I5"]

    newMapping = []

    for i in ins:
        newMapping.append(strManipDict[str(hm[i])])

    return newMapping

def fullConversion(hm, initString):
    list_a = rapidWriteL2PtoAbcdefList(hm)
    list_b = ['a', 'b', 'c', 'd', 'e', 'f'] # Original Order

    a = hexStringToBinary(initString)  # Init string as shown by rapidwright
    b = binStringToList(a)

    new_init = match_by_swapping(list_a, list_b, b)
    c = listToString(new_init)
    d = binaryStringToHexString(c)
    
    return d

def getInit(filePath):
    mapping = [15, 31, 14, 30, 13, 29, 12, 28,
            63, 47, 62, 46, 61, 45, 60, 44,
            11, 27, 10, 26,  9, 25,  8, 24,
            59, 43, 58, 42, 57, 41, 56, 40,
            7, 23,  6, 22,  5, 21,  4, 20,
            55, 39, 54, 38, 53, 37, 52, 36,
            3, 19,  2, 18,  1, 17,  0, 16,
            51, 35, 50, 34, 49, 33, 48, 32]


    initString = b''

    with open(filePath, "rb") as f:
        #byte = f.read(105399)
        byte = f.read(0x19BB7)
        byte0 = f.read(2)
        initString = initString + byte
        byte = f.read(0x19D4A - 0x19BB7 - 1)
        byte1 = f.read(2)
        initString = initString + byte
        byte = f.read(0x19D4A - 0x19BB7 - 1)
        byte2 = f.read(2)
        initString = initString + byte
        byte = f.read(0x19D4A - 0x19BB7 - 1)
        byte3 = f.read(2)
        initString = initString + byte
        #print("As read in: ", byte0, byte1, byte2, byte3)
        # print(initString)

    initStringList = []
    byteset = [byte0, byte1, byte2, byte3]
    #byteset = [initString]
    fullBytesRightOrder = byte3 + byte2 + byte1 + byte0

    for i in range(64):
        mask = 1 << i
        val = (int.from_bytes(fullBytesRightOrder, "big") & mask)
        if val == 0:
            initStringList.append(0)
        else:
            initStringList.append(1)
    #print("---", initStringList)

    initStringListString = ""
    for a in initStringList:
        initStringListString = initStringListString + str(a)
    #print("Converted to bits: ", initStringListString)

    orderedInit = []
    for index in mapping:
        orderedInit.append(initStringList[index])

    orderedInitsss = ""
    for a in orderedInit:
        orderedInitsss = orderedInitsss + str(a)
    #print("Reordered:         ", orderedInitsss)

    flipped = orderedInitsss[::-1]
    #print("flipped: ", flipped)

    finalHexInit = binaryStringToHexString(flipped)
    #print("final Hex Init: ", finalHexInit)
    return finalHexInit



"""
def main():
    list_a = ['d', 'e', 'c', 'f', 'b', 'a'] # New Order
    #list_a = ['a', 'b']
    list_b = ['a', 'b', 'c', 'd', 'e', 'f'] # Original Order
    #init_string = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    #               31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]

    intstring = "0xFFFFFFFF90000000"        # Init string as shown by rapidwright
    a = hexStringToBinary(intstring)
    b = binStringToList(a)

    #print(init_string)
    #print(list_a)
    new_init = match_by_swapping(list_a, list_b, b)
    print(new_init)
    c = listToString(new_init)
    print(c)
    d = binaryStringToHexString(c)
    print(intstring)
    print("VVVVVVVVVVVVVVV")
    print(d)      # As it appears in the bitstream
    #print(new_init)


if __name__ == "__main__":
    "This is executed when run from the command line "
    main()

"""