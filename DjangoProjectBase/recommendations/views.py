from django.shortcuts import render
from movie.models import Movie
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import os


def recommend_movie(request):
    prompt = request.GET.get('prompt', '').strip()
    recommended_movie = None

    if prompt:
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        def get_embedding(text, model="text-embedding-3-small"):
            text = text.replace("\n", " ")
            response = client.embeddings.create(
                input=[text],
                model=model
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        movies = Movie.objects.exclude(description='')

        prompt_embedding = get_embedding(prompt)

        best_movie = None
        best_similarity = -1

        for movie in movies:
            try:
                movie_embedding = get_embedding(movie.description)
                similarity = cosine_similarity(prompt_embedding, movie_embedding)

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_movie = movie
            except Exception:
                continue

        recommended_movie = best_movie

    return render(request, 'recommendations/recommendations.html', {
        'prompt': prompt,
        'recommended_movie': recommended_movie,
    })