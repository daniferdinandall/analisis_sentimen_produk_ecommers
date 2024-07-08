import os
import pandas as pd
import csv

# Path untuk file lexicon positive dan negative
positive_lexicon_file = 'preprocessing/lexicon_dictionary/positive.csv'
negative_lexicon_file = 'preprocessing/lexicon_dictionary/negative.csv'

# Membaca lexicon positive
lexicon_positive = {}
with open(positive_lexicon_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        lexicon_positive[row[0]] = int(row[1])

# Membaca lexicon negative
lexicon_negative = {}
with open(negative_lexicon_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        lexicon_negative[row[0]] = int(row[1])

# Membaca hasil preprocessing dari file CSV
preprocessed_file = 'preprocessing/dataset/Aerostreet5_steming.csv'
df = pd.read_csv(preprocessed_file)

# Function untuk melakukan labeling berdasarkan lexicon
def label_sentiment(text):
    if isinstance(text, str):  # Check if text is a string
        sentiment_score = 0
        
        # Cek kata-kata dengan spasi terlebih dahulu
        for phrase in lexicon_positive:
            if phrase in text:
                sentiment_score += lexicon_positive[phrase]
        
        for phrase in lexicon_negative:
            if phrase in text:
                sentiment_score += lexicon_negative[phrase]
        
        # Split dan cek kata-kata satu per satu
        tokens = text.split()
        for token in tokens:
            if token in lexicon_positive:
                sentiment_score += lexicon_positive[token]
            elif token in lexicon_negative:
                sentiment_score += lexicon_negative[token]
        
        if sentiment_score > 0:
            return 'Puas'
        elif sentiment_score < 0:
            return 'Tidak Puas'
        else:
            return 'Neutral'
    return 'Neutral'

# Mengganti NaN dengan string kosong ''
df['Ulasan'] = df['Ulasan'].fillna('')

# Melabeli setiap ulasan dalam dataframe
df['Label'] = df['Ulasan'].apply(label_sentiment)

# Menyimpan dataframe yang sudah dilabeli ke dalam file CSV di dalam folder 'label'
folder_name = 'label'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

output_file = os.path.join(folder_name, 'Aerostreet5_labeled.csv')
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"Labeling selesai. Data yang telah dilabeli disimpan dalam file '{output_file}'.")
