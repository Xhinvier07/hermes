from transformers import pipeline

print("Hermes - CLI Version")

print("Loading model...")
sentiment_analysis = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
print("Model loaded successfully.")

sentence = "I love using transformers library!"
result = sentiment_analysis(sentence)
print(f"Input Sentence: {sentence}")