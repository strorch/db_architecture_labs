import os
import tempfile
import webbrowser

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn import tree
import graphviz

def open_image_in_browser(file_path, title='no title'):
    abs_file_path = os.path.abspath(file_path)
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(f'<!DOCTYPE html><html><head><title>{title}</title></head><body>')
        f.write(f'<img src="file://{abs_file_path}" alt="Image"/>')
        f.write('</body></html>')
        html_file_path = f.name

        webbrowser.open('file://' + html_file_path)

def main():
    file_path = 'results/train_set.csv'
    tree_params = {'max_depth': 3}

    pd.set_option('display.max_rows',None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width',1000)

    print('reading {} ...'.format(file_path))
    df = pd.read_csv(file_path)

    print('analyzing dataset ...')
    preview = df.head()
    print(preview)

    print('analyzing columns with features ...')
    feature_columns = [col for col in df.columns if col != 'Result']

    for col in df.columns:
        print(df[col].describe())

    print('correlation analysis ...')
    correlation = df.corr()
    print(correlation)
    sns.set(font_scale=0.5)
    sns.heatmap(correlation, annot=True)
    plt.title('Heat map')
    plt.savefig('results/heatmap.png', dpi=150, bbox_inches='tight', pad_inches=0.5)
    open_image_in_browser('results/heatmap.png', 'features heatmap')

    print('preparing train set ...')
    X = df[feature_columns]
    y = df['Result']

    print('splitting train and test set ...')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    print('training the model {} ...'.format(tree_params))
    model = tree.DecisionTreeClassifier()
    model.set_params(**tree_params)
    model.fit(X_train, y_train)

    print('validating the model:')
    y_pred = model.predict(X_test)


    # Compute the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    cm_normalized = cm.astype('float') / cm.sum()
    cm_percentage = cm_normalized * 100
    # Convert each number in the confusion matrix to a string with a percentage symbol
    cm_percentage_str = np.array([["{0:.2f}%".format(value) for value in row] for row in cm_percentage])

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm_percentage, annot=cm_percentage_str, fmt='')
    plt.xlabel('Predicted')
    plt.ylabel('Truth')
    plt.title('Confusion Matrix ({})'.format(tree_params))
    plt.savefig('results/confusion_matrix.png', dpi=150, bbox_inches='tight', pad_inches=0.5)
    open_image_in_browser('results/confusion_matrix.png', 'confusion matrix({})'.format(tree_params))

    print(f"    Confusion matrix: [[FN, FP], [TN, TP]] =  {cm}")

    accuracy = accuracy_score(y_test, y_pred)
    print(f"    Accuracy: (TP + TN) / (ALL) = {accuracy * 100:.2f}%")

    precision = precision_score(y_test, y_pred)
    print(f"    Precision: TP / (TP + FP) = {precision * 100:.2f}%")

    recall = recall_score(y_test, y_pred)
    print(f"    Recall: TP / (TP + FN) = {recall * 100:.2f}%")

    f1 = f1_score(y_test, y_pred)
    print(f"    F1: 2 * (Precision * Recall) / (Precision + Recall) = {f1 * 100:.2f}%")

    dot_data = tree.export_graphviz(model, out_file=None,
                                    feature_names=['Play_music', 'Play_video_games', 'Like_sports', 'Like_cooking', 'Handsome', 'Generous', 'Rich', 'Married', 'Age'],
                                    class_names=['no', 'yes'],
                                    filled=True, rounded=True,
                                    special_characters=True,
                                    leaves_parallel=False)

    graph = graphviz.Source(dot_data)
    graph.render("results/decision_tree", format='png')
    open_image_in_browser('results/decision_tree.png', 'decision tree({})'.format(tree_params))


if __name__ == "__main__":
   main()