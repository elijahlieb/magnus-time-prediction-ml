from sklearn.model_selection import train_test_split

# Function to split Train and Test 
def split_TrainTest(df, target, list_features):

    X = df[list_features]
    y = df[target]

    # Split train/test
    return train_test_split(X, y, test_size=0.2, random_state=42)