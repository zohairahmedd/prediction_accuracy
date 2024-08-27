import csv
import argparse

def main():
    """
    take command line arguments input for the paths of both the csv files

    arguments:
        none
    """
    parser = argparse.ArgumentParser(description='calculating APR for a model.') # necessary for implementing command-line
    parser.add_argument('--input_model_predictions', '-imp', type=str, help='path csv file with predictions') # adds argument input_model_predictions to the parser
    parser.add_argument('--input_groundtruth', '-ig', type=str, help='path to csv file with ground truth values') # adds argument input_groundtruth to the parser

    args = parser.parse_args() # allows us to use the arguments in the parser (args.argument_name)

    apr_calculations(args.input_model_predictions, args.input_groundtruth) 

def apr_calculations(input_model_predictions, input_groundtruth):
    """
    calculate accuracy, precision, and recall using predicted & groundtruth values

    arguments:
        input_model_predictions (str): path to csv of model predictions
        input_groundtruth (str): path to csv of groundtruth values
    """

    TP_RC, FP_RC, TN_RC, FN_RC = 0,0,0,0
    TP_LC, FP_LC, TN_LC, FN_LC = 0,0,0,0

    RCornea = []
    LCornea = []

    with open(input_model_predictions, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            RCornea.append(int(float(row[1]) == 0))  
            LCornea.append(int(float(row[2]) == 0)) 

    RCornea_binary = [] 
    LCornea_binary = []

    with open(input_groundtruth, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            RCornea_binary.append(int(row[1]))
            LCornea_binary.append(int(row[2]))

    for r_binary, r_value in zip(RCornea_binary, RCornea):
        if r_binary == 1 and r_value == 1:
            TP_RC += 1
        elif r_binary == 1 and r_value == 0:
            FP_RC += 1
        elif r_binary == 0 and r_value == 0:
            TN_RC += 1
        elif r_binary == 0 and r_value == 1:
            FN_RC += 1

    for l_binary, l_value in zip(LCornea_binary, LCornea):
        if l_binary == 1 and l_value == 1:
            TP_LC += 1
        elif l_binary == 1 and l_value == 0:
            FP_LC += 1
        elif l_binary == 0 and l_value == 0:
            TN_LC += 1
        elif l_binary == 0 and l_value == 1:
            FN_LC += 1

    accuracy_RC = round((TP_RC + TN_RC) / (TP_RC + FP_RC + FN_RC + TN_RC), 2) if (TP_RC + FP_RC + FN_RC + TN_RC) > 0 else 0
    precision_RC = round(TP_RC / (TP_RC + FP_RC), 2) if (TP_RC + FP_RC) > 0 else 0
    recall_RC = round(TP_RC / (TP_RC + FN_RC), 2) if (TP_RC + FN_RC) > 0 else 0

    accuracy_LC = round((TP_LC + TN_LC) / (TP_LC + FP_LC + FN_LC + TN_LC), 2) if (TP_LC + FP_LC + FN_LC + TN_LC) > 0 else 0
    precision_LC = round(TP_LC / (TP_LC + FP_LC), 2) if (TP_LC + FP_LC) > 0 else 0
    recall_LC = round(TP_LC / (TP_LC + FN_LC), 2) if (TP_LC + FN_LC) > 0 else 0

    print(f"Right Cornea | Accuracy: {accuracy_RC}, Precision: {precision_RC}, Recall: {recall_RC}")
    print(f"Left Cornea | Accuracy: {accuracy_LC}, Precision: {precision_LC}, Recall: {recall_LC}")

if __name__ == '__main__':
    main()