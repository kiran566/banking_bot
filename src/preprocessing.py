import nltk
import string
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
def preprocess_text(text: str) -> str:
    """
    Clean and preprocess input text:
    - Lowercase
    - Tokenize
    - Remove punctuation
    - Lemmatize
    - Remove non-alphanumeric tokens
    """

    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)


    tokens = nltk.word_tokenize(text)

    # Remove punctuation & lemmatize
    cleaned_tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in string.punctuation and word.isalnum() and word not in stop_words
    ]

    return " ".join(cleaned_tokens)


# For testing purpose
if __name__ == "__main__":
    sample = "How can I OPEN a Current Account for a Proprietorship?"
    print(preprocess_text(sample))
