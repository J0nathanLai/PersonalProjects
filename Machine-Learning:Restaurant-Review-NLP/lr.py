import numpy as np
import argparse
import csv
import copy
import matplotlib.pyplot as plt

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
    X = np.array(X)
    y = np.array(y)
    b = 0.0
    xDim = np.shape(X)[0] # number of examples
    wVec = theta # 0 vector initialized
    nll = [[], []] 
    for j in range(num_epoch):
        for i in range(xDim):
            xVec = X[i]
            prob = sigmoid(np.dot(wVec.T, xVec)+b)
            yVec = y[i]
            pointGradX = np.dot(xVec, prob-yVec)
            pointGradB = prob-yVec
            wVec = wVec - learning_rate*pointGradX # update weight vector
            b = b - learning_rate*pointGradB # update intercept term
        # Compute full-batch training NLL
        probs_train = sigmoid(np.dot(X, wVec) + b)
        train_loss = -np.mean(y * np.log(probs_train) + (1 - y) * np.log(1 - probs_train))
        nll[0].append(j)
        nll[1].append(train_loss)
    return wVec, b, nll


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
    
    args = parser.parse_args()
    trainData = read_tsv(args.train_input)
    weightVec = train(np.zeros(len(trainData[0][0])),trainData[0], trainData[1],args.num_epoch, args.learning_rate)
    weightVec1 = train(np.zeros(len(trainData[0][0])),trainData[0], trainData[1],args.num_epoch, 0.01)
    weightVec2 = train(np.zeros(len(trainData[0][0])),trainData[0], trainData[1],args.num_epoch, 0.001)
    predTrain = predict(weightVec[0], trainData[0], weightVec[1])
    errTrain = compute_error(predTrain, trainData[1])
    
    validData = read_tsv(args.validation_input)
    weightVecVal = train(np.zeros(len(validData[0][0])),validData[0], validData[1],args.num_epoch, args.learning_rate)
    predValid = predict(weightVec[0], validData[0], weightVec[1])
    testData = read_tsv(args.test_input)
    predTest = predict(weightVec[0], testData[0], weightVec[1])
    errTest = compute_error(predTest, testData[1])

    with open(args.train_out, "w") as writeTrain:
        for i in range(len(predTrain)):
            writeTrain.write(str(predTrain[i])+'\n')

    with open(args.test_out, "w") as writeTest:
        for i in range(len(predTest)):
            writeTest.write(str(predTest[i])+'\n')

    with open(args.metrics_out, "w") as met:
        met.write(f'error(train): {str("{:.6f}".format(errTrain))}\nerror(test): {str("{:.6f}".format(errTest))}')

    # Run training and store weights and NLLs
    trainData = read_tsv(args.train_input)
    validData = read_tsv(args.validation_input)

    # Train model and get training NLL
    weightVec = train(
        np.zeros(len(trainData[0][0])), 
        trainData[0], 
        trainData[1], 
        args.num_epoch, 
        args.learning_rate
    )
    # Extract training NLL from weightVec
    nll_train = weightVec[2]  # [epochs], [NLLs]

    # Recompute validation NLLs epoch-by-epoch using saved weights
    X_val = np.array(validData[0])
    y_val = np.array(validData[1])
    X_train = np.array(trainData[0])
    y_train = np.array(trainData[1])
    theta = np.zeros(X_train.shape[1])
    b = 0.0
    val_nll = [[], []]

    # Re-run training epoch-by-epoch again to log validation NLLs
    for j in range(args.num_epoch):
        for i in range(len(X_train)):
            xVec = X_train[i]
            y_i = y_train[i]
            prob = sigmoid(np.dot(theta.T, xVec) + b)
            grad_w = xVec * (prob - y_i)
            grad_b = prob - y_i
            theta -= args.learning_rate * grad_w
            b -= args.learning_rate * grad_b

        # Validation NLL at this epoch
        probs_val = sigmoid(np.dot(X_val, theta) + b)
        eps = 1e-8
        val_loss = -np.mean(y_val * np.log(probs_val + eps) + (1 - y_val) * np.log(1 - probs_val + eps))
        val_nll[0].append(j + 1)
        val_nll[1].append(val_loss)
    
    plt.figure(figsize=(10, 6))
    plt.plot(nll_train[0], nll_train[1], label="Training NLL", linewidth=2)
    plt.plot(val_nll[0], val_nll[1], label="Validation NLL", linewidth=2)
    plt.xlabel("Epoch")
    plt.ylabel("Average Negative Log-Likelihood")
    plt.title("Training vs Validation NLL over Epochs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("q8.1.png")
    plt.close()

    learning_rates = [1e-1, 1e-2, 1e-3]
    colors = ['red', 'blue', 'green']
    X_train = trainData[0]
    y_train = trainData[1]

    plt.figure(figsize=(10, 6))
    for lr, color in zip(learning_rates, colors):
        theta_init = np.zeros(len(X_train[0]))
        _, _, nll = train(theta_init, X_train, y_train, args.num_epoch, lr)
        plt.plot(nll[0], nll[1], label=f"η = {lr}", color=color, linewidth=2)

    plt.xlabel("Epoch")
    plt.ylabel("Average Negative Log-Likelihood")
    plt.title("Training NLL over Epochs for Different Learning Rates")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("q8.4.png")
    plt.close()
