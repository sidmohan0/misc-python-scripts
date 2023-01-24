import csv
import openai
import pickle

def serialize_embedding(filepath, identifier):
    # Set the OpenAI API key
    openai.api_key = "your_api_key_here"

    # Read the CSV file
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['user'] == identifier:
                # Get the embedding for the message
                embedding = openai.Embedding.create(
                    engine="text-embedding-ada-002",
                    prompt=row['message']
                )

                # Serialize the embedding using pickle
                serialized_embedding = pickle.dumps(embedding.embedding)
                row['serialized_embedding'] = serialized_embedding

    # Write the updated rows to the CSV file
    with open(filepath, 'w') as csvfile:
        fieldnames = ['date', 'user', 'message', 'serialized_embedding']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow(row)

def deserialize_embedding(filepath, identifier):
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['user'] == identifier:
                deserialized_embedding = pickle.loads(row['serialized_embedding'].encode())
                return deserialized_embedding
