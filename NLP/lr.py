import numpy as np
import argparse
import csv
import copy

def sigmoid(x : np.ndarray):
    """
    Implementation of the sigmoid function.

    Parameters:
        x (np.ndarray): Input np.ndarray.

    Returns:
        An np.ndarray after applying the sigmoid function element-wise to the
        input.
    """
    e = np.exp(x)
    return e / (1 + e)


def train(
    theta : np.ndarray, # shape (D,) where D is feature dim
    X : np.ndarray,     # shape (N, D) where N is num of examples
    y : np.ndarray,     # shape (N,)
    num_epoch : int, 
    learning_rate : float
) -> tuple:
    # TODO: Implement `train` using vectorization
    b = 0.0
    xDim = np.shape(X)[0] # number of examples
    wVec = theta # 0 vector initialized
    nll = []
    nll.append([])
    nll.append([])
    for j in range(num_epoch):
        for i in range(xDim):
            xVec = X[i]
            prob = sigmoid(np.dot(wVec.T, xVec)+b)
            yVec = y[i]
            pointGradX = np.dot(xVec, prob-yVec)
            pointGradB = prob-yVec
            wVec = wVec - learning_rate*pointGradX # update weight vector
            b = b - learning_rate*pointGradB # update intercept term
        nllVal = -np.mean(yVec * np.log(prob) + (1 - yVec) * np.log(1 - prob))
        nll[1].append(nllVal)
        nll[0].append(j)
    return (wVec, b, nll)


def predict(
    theta : np.ndarray,
    X : np.ndarray,
    b : float
) -> np.ndarray:
    # TODO: Implement `predict` using vectorization
    preds = []
    prob = sigmoid(np.dot(X, theta) + b)
    for p in prob:
        if p >= 0.5:
            preds.append(1)
        else:
            preds.append(0)
    return preds


def compute_error(
    y_pred : np.ndarray, 
    y : np.ndarray
) -> float:
    # TODO: Implement `compute_error` using vectorization)
    errCount = 0
    total = len(y)
    for i in range(len(y)):
        if y[i] != y_pred[i]:
            errCount += 1
    return errCount/total

def read_tsv(file):
    with open(file, "r") as file2read:
        reader = csv.reader(file2read, delimiter="\t")
        data = [row for row in reader]
    x = []
    y = []
    new = copy.deepcopy(data)
    floatList = [[float(element) for element in row] for row in new]
    for row in range(len(data)):
        y.append(floatList[row][0])
        x.append(floatList[row][1:])
    return (x, y)


if __name__ == '__main__':
    # This takes care of command line argument parsing for you!
    # To access a specific argument, simply access args.<argument name>.
    # For example, to get the learning rate, you can use `args.learning_rate`.
    parser = argparse.ArgumentParser()
    parser.add_argument("train_input", type=str, help='path to formatted training data')
    parser.add_argument("validation_input", type=str, help='path to formatted validation data')
    parser.add_argument("test_input", type=str, help='path to formatted test data')
    parser.add_argument("train_out", type=str, help='file to write train predictions to')
    parser.add_argument("test_out", type=str, help='file to write test predictions to')
    parser.add_argument("metrics_out", type=str, help='file to write metrics to')
    parser.add_argument("num_epoch", type=int, 
                        help='number of epochs of stochastic gradient descent to run')
    parser.add_argument("learning_rate", type=float,
                        help='learning rate for stochastic gradient descent')
    parser.add_argument("nll_out", type=str,
                        help='learning rate for stochastic gradient descent')
    
    args = parser.parse_args()
    trainData = read_tsv(args.train_input)
    weightVec = train(np.zeros(len(trainData[0][0])),trainData[0], trainData[1],args.num_epoch, args.learning_rate)
    weightVec1 = train(np.zeros(len(trainData[0][0])),trainData[0], trainData[1],args.num_epoch, 0.01)
    weightVec2 = train(np.zeros(len(trainData[0][0])),trainData[0], trainData[1],args.num_epoch, 0.001)
    predTrain = predict(weightVec[0], trainData[0], weightVec[1])
    errTrain = compute_error(predTrain, trainData[1])
    print(errTrain)
    
    validData = read_tsv(args.validation_input)
    weightVecVal = train(np.zeros(len(validData[0][0])),validData[0], validData[1],args.num_epoch, args.learning_rate)
    predValid = predict(weightVec[0], validData[0], weightVec[1])
    testData = read_tsv(args.test_input)
    predTest = predict(weightVec[0], testData[0], weightVec[1])
    errTest = compute_error(predTest, testData[1])
    print(errTest)

    with open(args.train_out, "w") as writeTrain:
        for i in range(len(predTrain)):
            writeTrain.write(str(predTrain[i])+'\n')

    with open(args.test_out, "w") as writeTest:
        for i in range(len(predTest)):
            writeTest.write(str(predTest[i])+'\n')

    with open(args.metrics_out, "w") as met:
        met.write(f'error(train): {str("{:.6f}".format(errTrain))}\nerror(test): {str("{:.6f}".format(errTest))}')

    
    # with open(args.nll_out, "w") as nll_t:
    #     nll_t.write("no. epochs" + '\t' + "avg. training neg log likelihood" + '\t' + "avg. validation neg log likelihood" + '\n')
    #     for i in range(len(weightVec[2][0])):
    #         nll_t.write(str(weightVec[2][0][i]+1) + '\t' + str(weightVec[2][1][i]) + '\t' + str(weightVecVal[2][1][i]) + '\n')
    
    with open(args.nll_out, "w") as nll_t:
        nll_t.write("no. epochs" + '\t' + "neg log likelihood with rate as 0.1" + '\t' + "neg log likelihood with rate as 0.01" + '\t' + "neg log likelihood with rate as 0.001" + '\n')
        for i in range(len(weightVec[2][0])):
            nll_t.write(str(weightVec[2][0][i]+1) + '\t' + str(weightVec[2][1][i]) + '\t' + str(weightVec1[2][1][i]) + '\t' + str(weightVec2[2][1][i]) + '\n')
    
