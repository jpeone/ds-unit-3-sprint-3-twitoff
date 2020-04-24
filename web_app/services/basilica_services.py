import basilica
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BASILICA_API_KEY')

conn = basilica.Connection(api_key)
print(type(conn))

embedding = conn.embed_sentence('hey this is a cool tweet', model='twitter')
print(embedding)

tweets = ['Hello world', 'artificial intelligence', 'another tweet']
embeddings = conn.embed_sentences(tweets, model= 'twitter')
for embed in embeddings:
    print('----------')
    print(embed)