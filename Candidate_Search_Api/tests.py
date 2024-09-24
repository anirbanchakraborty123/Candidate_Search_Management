from django.test import TestCase
from .models import Candidate
from .views import search_candidates

class CandidateSearchTest(TestCase):
    def setUp(self):
        # Created some sample candidates
        Candidate.objects.create(name="Ajay Kumar Yadav")
        Candidate.objects.create(name="Kumar Sharma Yadav")
        Candidate.objects.create(name="Ajay Kumar Sharma")
        Candidate.objects.create(name="Ajay Singh kumar")
        Candidate.objects.create(name="Vijay Yadav")

    def test_search_exact_match(self):
        query = "Ajay Kumar Yadav"
        results = search_candidates(query)
        self.assertEqual([candidate.name for candidate in results], [
            "Ajay Kumar Yadav"
        ])

    def test_search_partial_match(self):
        query = "Ajay Kumar Yadav"
        results = search_candidates(query)
        self.assertEqual([candidate.name for candidate in results], [
            "Ajay Kumar Yadav", 
            "Ajay Kumar Sharma", 
            "Kumar Sharma Yadav", 
            "Ajay Singh Kumar", 
            "Vijay Yadav"
        ])

    def test_search_single_word(self):
        query = "Ajay"
        results = search_candidates(query)
        self.assertEqual([candidate.name for candidate in results], [
            "Ajay Kumar Yadav", 
            "Ajay Kumar Sharma", 
            "Ajay Singh Kumar"
        ])
