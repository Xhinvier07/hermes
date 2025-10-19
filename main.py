from transformers import pipeline
"""
    tabularisai/multilingual-sentiment-analysis (multilingual sentiment analysis model, 67M parameters, English, Spanish, French, German, Italian, Portuguese, Dutch, Malay, Telugu, Vietnamese, Chinese, Japanese, Korean, Turkish, Tagalog, Dutch, Russian, Arabic, Hindi)
    distilbert/distilbert-base-uncased-finetuned-sst-2-english (English sentiment analysis model, 0.1B parameters)
    j-hartmann/emotion-english-distilroberta-base (English emotion recognition model, )
    cardiffnlp/twitter-xlm-roberta-base-sentiment (multilingual sentiment analysis model, Arabic, English, French, German, Italian, Spanish, Portuguese)
    unitary/toxic-bert (English toxic comment classification model)
    ProsusAI/finbert (English financial sentiment analysis model)
"""

print("Hermes - CLI Version")
print("Loading model...")
sentiment_analysis = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis") # multilingual sentiment analysis model

print("Model loaded successfully.")


while True:
    sentence = input("Enter a sentence for sentiment analysis or q to exit: ")

    if sentence.lower() == 'q':
        print("=== EXITING ===")
        break

    result = sentiment_analysis(sentence, top_k=None) #top_k=None to get all labels

    print("=== RESULTS === \n")

    for item in result:
        print(f"Label: {item['label']}, Score: {item['score']:.4f}")
    
    print("="*20, "\n")
