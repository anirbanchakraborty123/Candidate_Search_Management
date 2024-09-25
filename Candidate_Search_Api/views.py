from django.db.models import Case, When, Value, IntegerField, Count, Q, F
from .models import Candidate

def search_candidates(query: str):
    """ 
        Search candidates by their name based on a given query and
        returns a list of candidates sorted by relevancy 
    """
    # Split the query into individual words for partial matching
    query_words = query.split()

    # Exact match first
    exact_match = Q(name__iexact=query)
    
    # Partial match on any of the words
    partial_match = Q()
    for word in query_words:
        partial_match |= Q(name__icontains=word)
    
    # Annotate the queryset with the count of matched search terms and order by that count
    candidates = Candidate.objects.filter(partial_match).annotate(
        exact_match=Case(
            When(exact_match, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
           ),
        match_count=Count('id', filter=Q(name__icontains=query_words[0]))  # Initialize with the first term
    )
    
    # Iterate through the rest of the search terms to annotate match_count
    for term in query_words[1:]:
        candidates = candidates.annotate(
            match_count=Count('id', filter=Q(name__icontains=term)) + F('match_count'),
        )
    # Order by relevance
    candidates = candidates.order_by('-exact_match','-match_count','name')
    
    return candidates
