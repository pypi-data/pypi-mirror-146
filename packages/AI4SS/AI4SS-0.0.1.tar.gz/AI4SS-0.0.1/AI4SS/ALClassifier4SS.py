import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def ALClassifier4SS(X_train, X_test, y_train, y_test, data_unlabeled, NumEpochs, lower_prob_bound, upper_prob_bound,
          termination_threshold):
    # change X_train, X_tset, y_train, y_test to numpy arrays
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    # flatten y_train and y_test
    y_train = y_train.flatten()
    y_test = y_test.flatten()
    for epoch in range(NumEpochs):
        # build the svm model
        clf = SVC(probability=True)
        clf.fit(X_train, y_train)
        # test the model
        y_pred = clf.predict(X_test)
        # calculate the accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print('Epoch:', epoch, 'Test Accuracy:', accuracy)
        # if there is no more unlabeled data, break the loop
        if len(data_unlabeled) == 0:
            print('No more unlabeled data')
            break
        # predict the unlabeled data using predict_proba
        y_pred = clf.predict_proba(data_unlabeled)
        # find the index in y_pred that is between lower_bound and upper_bound
        index = np.where((y_pred[:, 1] > lower_prob_bound) & (y_pred[:, 1] < upper_prob_bound))
        # get the index of the unlabeled data
        index = index[0]
        # if the number of unlabeled data is less than the termination threshold, then break the loop
        if len(index) < termination_threshold:
            print('Number of uncertain data is less than the termination threshold')
            break
        print("All the index of the unlabeled data within the uncertain prob range is: ", index)
        print("-------------------------------------------------------")
        # randomly select termination_threshold number of them
        selected_index = np.random.choice(index, termination_threshold, replace=False)
        print("The selected index in this round is: ", selected_index)
        print("-------------------------------------------------------")
        manually_labeled = []
        unknow_index_list = []
        # randomly select termination_threshold number of the unlabeled data, print them iteratively and
        # ask the user to label them
        for i in range(termination_threshold):
            # print the entire row of the unlabeled data
            print("The uncertain data looks like:")
            tmp_index = selected_index[i]
            # print the entire row of the unlabeled data, column by column
            for j in range(len(data_unlabeled.columns)):
                print("Column Name:", data_unlabeled.columns[j], "Value:", data_unlabeled.iloc[tmp_index, j])
            # ask the user to label the data, the label must be 1 or 0
            label = input("Please label the data as 1 if it is a school "
                          "shooting or 0 if it is not, or enter 999 if you want to skip this data: ")
            # change the label to int
            label_str = str(label)
            # if the input is not 1 or 0, ask the user to input again
            while label_str != '1' and label_str != '0' and label_str != '999':
                label = input("Invalid input. Please label the data as 1 if it is a school "
                              "shooting or 0 if it is not, or enter 999 if you want to skip this data: ")
                label_str = str(label)
            print("The label is: " + label_str)
            # change back to int
            label = int(label)
            print("-------------------------------------------------------")
            # if the label is 999, then skip this data
            if label == 999:
                # add the index of this data to the list of the unknown index
                unknow_index_list.append(selected_index[i])
                continue
            # if the label is 1 or 0, then add it to the list
            else:
                manually_labeled.append(label)
        # remove all unknown_index from the selected_index
        selected_index = [ele for ele in selected_index if ele not in unknow_index_list]
        # add the manually labeled data to the training data
        X_add = data_unlabeled.iloc[selected_index]
        # change it to numpy array
        X_add = np.array(X_add)
        # add X_add to X_train
        X_train = np.concatenate((X_train, X_add), axis=0)
        # add the manually labeled data to the training data
        y_add = pd.Series(manually_labeled)
        # change it to numpy array
        y_add = np.array(y_add)
        # add y_add to y_train
        y_train = np.concatenate((y_train, y_add), axis=0)
        # delete the manually labeled data from the unlabeled data
        data_unlabeled = data_unlabeled.drop(selected_index)
        print("-------------------------------------------------------")
    return clf