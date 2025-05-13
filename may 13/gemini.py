#import libray
import google.generativeai as genai

#Set gemini API
api_key='AIzaSyA7GvK4bWznhjrIuqvOXRdrjbIvEosZY0Y'
genai.configure(api_key=api_key)
#Load gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate text
def generate_text(prompt):
    return model.generate_content(prompt).text

# Function to summarize text
def text_summarization(text):
    return model.generate_content(f'Summarize this: {text}').text

# Function to answer question
def question_answering(context, question):
    return model.generate_content(f'Question: {question} Context: {context}').text

# Function to analyze sentiment
def sentiment_analysis(text):
    return model.generate_content(f"What is the sentiment of the following text: {text}").text

# Function to translate text to another language
def text_translation(text, target_language):
    return model.generate_content(f'Translate this text to {target_language}: {text}').text


# Run all functions
prompt = "The quick brown fox"
print("Generated Text:")
print(generate_text(prompt))
print()

text = "The quick brown fox jumps over the lazy dog"
print("Summarized:")
print(text_summarization(text))
print()

context = "The quick brown fox jumps over the lazy dog"
question = "What does the fox jump over?"
print("Answer:")
print(question_answering(context, question))
print()

print("Sentiment:")
print(sentiment_analysis(text))
print()

target_language = "es"  
print("Translated to Spanish:")
print(text_translation(text, target_language))