from django.test import TestCase
from .models import Candidate
from .views import search_candidates

class CandidateSearchTests(TestCase):

    def setUp(self):
        # Create candidate records
        Candidate.objects.create(name="Ajay Kumar Yadav")
        Candidate.objects.create(name="Rajesh Yadav")
        Candidate.objects.create(name="Kumar Sharma Yadav")
        Candidate.objects.create(name="Ajay Singh")
        Candidate.objects.create(name="Ajay Kumar Sharma")

    def test_search_exact_and_partial_matches(self):
        query = "Ajay Kumar Yadav"
        results = search_candidates(query)
        result_names = [candidate.name for candidate in results]
        expected_results = [
                            "Ajay Kumar Yadav",   # Exact match
                            "Ajay Kumar Sharma",  # Partial match (Ajay, Kumar)
                            "Kumar Sharma Yadav", # Partial match (Kumar, Yadav)
                            "Ajay Singh",         # Partial match (Ajay)
                            "Rajesh Yadav"        # Partial match (Yadav)
                            ]
        self.assertEqual(result_names, expected_results)
