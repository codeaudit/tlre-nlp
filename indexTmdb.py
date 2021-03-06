import pysolr


def indexableMovies(filename='tmdb_enriched_deduped.json'):
    """ Generates TMDB movies, similar to how ES Bulk indexing
        uses a generator to generate bulk index/update actions """
    from tmdbMovies import tmdbMovies
    for movieId, tmdbMovie in tmdbMovies(filename):
        print("Indexing %s" % movieId)
        try:
            releaseDate = None
            if 'release_date' in tmdbMovie and len(tmdbMovie['release_date']) > 0:
                releaseDate = tmdbMovie['release_date'] + 'T00:00:00Z'

            yield {'id': movieId,
                   'title': tmdbMovie['title'],
                   'overview': tmdbMovie['overview'],
                   'tagline': tmdbMovie['tagline'],
                   'directors': [director['name'] for director in tmdbMovie['directors']],
                   'cast': [castMember['name'] for castMember in tmdbMovie['cast']],
                   'genres': [genre['name'] for genre in tmdbMovie['genres']],
                   'release_date': releaseDate,
                   'vote_average': tmdbMovie['vote_average'] if 'vote_average' in tmdbMovie else None,
                   'vote_count': int(tmdbMovie['vote_count']) if 'vote_count' in tmdbMovie else None,
                   'location': tmdbMovie['location'] if 'location' in tmdbMovie else [],
                   'location_city': tmdbMovie['location_city'] if 'location_city' in tmdbMovie else [],
                   'location_state': tmdbMovie['location_state'] if 'location_state' in tmdbMovie else [],
                   'location_country': tmdbMovie['location_country'] if 'location_country' in tmdbMovie else [],                   
                   }
        except KeyError as k: # Ignore any movies missing these attributes
            print(k)
            continue


if __name__ == "__main__":
    solr = pysolr.Solr('http://localhost:8983/solr/tmdb', timeout=100)
    solr.add(indexableMovies(filename='tmdb_enriched_deduped.json'))
