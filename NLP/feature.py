import csv
import numpy as np
import argparse

VECTOR_LEN = 300   # Length of glove vector
MAX_WORD_LEN = 64  # Max word length in dict.txt and glove_embeddings.txt

################################################################################
# We have provided you the functions for loading the tsv and txt files. Feel   #
# free to use them! No need to change them at all.                             #
################################################################################


def load_tsv_dataset(file):
    """
    Loads raw data and returns a tuple containing the reviews and their ratings.

    Parameters:
        file (str): File path to the dataset tsv file.

    Returns:
        An np.ndarray of shape N. N is the number of data points in the tsv file.
        Each element dataset[i] is a tuple (label, review), where the label is
        an integer (0 or 1) and the review is a string.
    """
    dataset = np.loadtxt(file, delimiter='\t', comments=None, encoding='utf-8',
                         dtype='l,O')
    return dataset


def load_feature_dictionary(file):
    """
    Creates a map of words to vectors using the file that has the glove
    embeddings.

    Parameters:
        file (str): File path to the glove embedding file.

    Returns:
        A dictionary indexed by words, returning the corresponding glove
        embedding np.ndarray.
    """
    glove_map = dict()
    with open(file, encoding='utf-8') as f:
        read_file = csv.reader(f, delimiter='\t')
        for row in read_file:
            word, embedding = row[0], row[1:]
            glove_map[word] = np.array(embedding, dtype=float)
    return glove_map

def output(data, embed):
    sOut = ""
    for i in range(len(data)):
        sOut += str("{:.6f}".format(data[i][0])) # label of review
        review = data[i][1] # review text
        splitWords = review.split() # split text into words
        # vecLen = np.shape(embed[splitWords[0]])[0] # get dim in embed
        vecLen = VECTOR_LEN
        zeroVec = np.zeros(vecLen)
        numWord = 0
        for i in range(len(splitWords)):
            if splitWords[i] in embed:
                zeroVec += embed[splitWords[i]]
                numWord += 1
        zeroVec /= numWord
        for i in range(vecLen):
            sOut += '\t' + str("{:.6f}".format(zeroVec[i]))
        sOut += '\n'
    return sOut




if __name__ == '__main__':
    # This takes care of command line argument parsing for you!
    # To access a specific argument, simply access args.<argument name>.
    # For example, to get the train_input path, you can use `args.train_input`.
    parser = argparse.ArgumentParser()
    parser.add_argument("train_input", type=str, help='path to training input .tsv file')
    parser.add_argument("validation_input", type=str, help='path to validation input .tsv file')
    parser.add_argument("test_input", type=str, help='path to the input .tsv file')
    parser.add_argument("feature_dictionary_in", type=str, 
                        help='path to the GloVe feature dictionary .txt file')
    parser.add_argument("train_out", type=str, 
                        help='path to output .tsv file to which the feature extractions on the training data should be written')
    parser.add_argument("validation_out", type=str, 
                        help='path to output .tsv file to which the feature extractions on the validation data should be written')
    parser.add_argument("test_out", type=str, 
                        help='path to output .tsv file to which the feature extractions on the test data should be written')
    args = parser.parse_args()

    trainData = load_tsv_dataset(args.train_input)
    validData = load_tsv_dataset(args.validation_input)
    testData = load_tsv_dataset(args.test_input)
    embed = load_feature_dictionary(args.feature_dictionary_in)
    outTrain = output(trainData, embed)
    with open(args.train_out, "w") as writeTrain:
        writeTrain.write(outTrain)

    outVal = output(validData, embed)
    with open(args.validation_out, "w") as writeVal:
        writeVal.write(outVal)

    outTest = output(testData, embed)
    with open(args.test_out, "w") as writeTest:
        writeTest.write(outTest)

    