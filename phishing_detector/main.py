
#imports
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SequentialFeatureSelector

#loads the dataset
dataset = pd.read_csv("phishing_detector/datasets/dataset_export_full_11k.csv")

#validation for dataset loading, will print a sample line
print("Dataset loaded successfully; sample line:")
print(dataset.sample(1))

#aligns dataset columns with string variables to train SVM using
labelsColumn = dataset.columns[1]
messagesColumn = dataset.columns[2]

labels = dataset[labelsColumn].astype(str)
messages = dataset[messagesColumn].astype(str)

#train/test split
xTrain, xTest, yTrain, yTest = train_test_split(
    messages,
    labels,
    test_size=0.2,             
    random_state=42,
    stratify=labels             
)

#vectorises message so it is readable to SVM
vectoriser = TfidfVectorizer(

    #changes all characters to lowercase, allows SVM to read "Hello" and "hello" as the same
    lowercase=True,

    #ignores unimportant words
    stop_words="english",

    ngram_range=(1, 2),
    min_df=1
)

xTrainVector = vectoriser.fit_transform(xTrain)
xTestVector = vectoriser.transform(xTest)

#svm training
svm = LinearSVC(class_weight="balanced")
svm.fit(xTrainVector, yTrain)

suspiciousWords = vectoriser.get_feature_names_out()
svmWeights = svm.coef_[0]

#debug message
print("\nModel training complete")

#message prediction 
def predictMessage(messageInput: str):

    #vectorises message
    vectorisedMessage = vectoriser.transform([messageInput])
    
    #evaluates message and returns a prediction
    prediction = svm.predict(vectorisedMessage)[0]
    return prediction

#returns a sorted list of the most suspicious parts of the message the AI picked up on
def getSuspiciousWords(messageInput, top_n=5):

    #vectorises message
    vectorisedMessage = vectoriser.transform([messageInput])
    featureIndexes = vectorisedMessage.nonzero()[1]

    sortedList = []

    for idx in featureIndexes:
        word = suspiciousWords[idx]
        weight = svmWeights[idx]
        sortedList.append((word, weight))

    #will sort by how impactful they are into final decision
    sortedList = sorted(
        sortedList,
        key=lambda x: abs(x[1]),
        reverse=True
    )

    return sortedList[:top_n]

#provides explanation to the user if the message is deemed spam
def explainMessage(messageInput, prediction):

    suspiciousWords = getSuspiciousWords(messageInput)

    #displays suspicious words and weight attached to them
    words = [
        f"{word} (weight {weight:.2f})"
        for word, weight in suspiciousWords
    ]

    #lists all suspicious words
    if prediction.lower() == "spam":
        explanation = (
            "The phrases used such as "f"{', '.join(words)} are commonly used within malicious messages, indicating this is spam.\n"
        )
    else:
        explanation = (
            "This message does not contain any phrases commonly used in spam messages, indicating it is likely a real message.\n"
        )
    
    return explanation

#loop for error checking
while True:

    #user must give permisson for application to read messages
    userConfirmation = input("Do you give permission for this application to read your WhatsApp messages (y/n): ")

    #user confirms permission
    if userConfirmation.lower() == "y":

        #while loop for user input
        while True:

            #input message
            userInput = input("Enter a message to evaluate or 'q' to quit: ")

            #quit
            if userInput.lower() == "q":
                print("Quitting program...")
                quit()

            #outputs prediction
            output = predictMessage(userInput)

            #outputs
            print("\n///////////////////////////////////////////// Message Evaluation /////////////////////////////////////////////\n")
            print(userInput + "\n")
            
            #prints explanation if spam
            if output == "spam":
                print(f"Prediction:\nThis message is likely spam. It is advised to not respond. \n")
                explanation = explainMessage(userInput, output)
                print("Explanation\n" + explanation)

            #if message is safe
            else:
                print("Prediction:\nThis message is likely safe to respond to. \n")
                explanation = explainMessage(userInput, output)
                print("Explanation:\n" + explanation)
                
    #user denies permission
    elif userConfirmation.lower() == "n":

        print("Quitting program...")
        quit()

    #error handling
    else :
        print("Invalid response, please try again: ")
