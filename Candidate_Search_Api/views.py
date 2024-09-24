from django.db.models import Q, Case, When
from .models import Candidate

def search_candidates(query: str):
    """ 
        Search candidates by their name based on a given query and
        returns a list of candidates sorted by relevancy 
    """
    
    # Split the query into words for matching
    query_words = query.split()
    
    # Build the Q objects for exact matches and partial matches
    exact_match = Q(name__iexact=query)
    partial_match = Q()
    
    # Create partial match conditions
    for word in query_words:
        partial_match |= Q(name__icontains=word)

    # Fetch all candidates that match the conditions
    candidates = Candidate.objects.filter(partial_match)

    # Separate exact matches and partial matches
    exact_candidates = candidates.filter(exact_match)
    partial_candidates = candidates.exclude(exact_match)

    # Sort partial candidates by the number of matching words
    sorted_partial_candidates = sorted(
        partial_candidates,
        key=lambda c: sum(word.lower() in c.name.lower() for word in query_words),
        reverse=True
    )
    queryset_like = Candidate.objects.filter(id__in=[x.id for x in sorted_partial_candidates])

    preserved_order = Case(*[When(id=item.id, then=pos) for pos, item in enumerate(sorted_partial_candidates)])
    
    ordered_queryset = queryset_like.order_by(preserved_order)

    # Combine exact matches with sorted partial matches
    return exact_candidates | ordered_queryset