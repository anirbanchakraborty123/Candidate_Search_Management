from django.db.models import Q, Count
from .models import Candidate

def search_candidates(query: str):
    """ 
        Search candidates by their name based on a given query and
        returns a list of candidates sorted by relevancy 
    """
    
    # Split the query into individual words
    all_query_words = query.split()

    # Exact match
    exact_matches = Candidate.objects.filter(name__iexact=query)

    # Partial match
    # We need to build a query that checks if any word in the query appears in the candidate's name
    partial_match_filter = Q()
    for word in all_query_words:
        partial_match_filter |= Q(name__icontains=word)
    
    # Get candidates who partially match the query, excluding the exact match ones
    partial_matches = Candidate.objects.filter(partial_match_filter).exclude(name__iexact=query)

    # Annotate with the number of matching words
    # Annotate the partial matches with the number of overlapping words from the query
    for word in all_query_words:
        partial_matches = partial_matches.annotate(
            matching_word_count=Count('name', filter=Q(name__icontains=word))
        )
    
    # Order the partial matches by the number of matching words
    partial_matches = partial_matches.order_by('-matching_word_count')

    # Combine the exact matches and the ordered partial matches
    results = exact_matches.union(partial_matches)

    return results
