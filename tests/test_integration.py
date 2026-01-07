"""
Test Suite für Subgraph Subgraph Algorithmus
Umfassende Tests mit maximaler Code Coverage
"""

import pytest
import numpy as np
from subgraph import Subgraph, create_example_graphs

class TestIntegration:
    """Integrationstests für komplette Workflows"""
    
    def test_full_workflow_matrix_method(self):
        """Test: Kompletter Workflow mit Matrixmethode"""
        algo = Subgraph()
        A, B = create_example_graphs()
        
        # Berechne Signaturen
        sig_A = algo._compute_column_signature(A)
        sig_B = algo._compute_column_signature(B)
        
        # Vergleiche
        decision, kept = algo.compare_graphs(A, B)
        
        assert len(sig_A) == A.shape[1]
        assert len(sig_B) == B.shape[1]
        assert decision == "keep_B"
        assert kept is not None
    
    def test_full_workflow_adjacency_list_method(self):
        """Test: Kompletter Workflow mit Adjazenzliste"""
        algo = Subgraph()
        A, B = create_example_graphs()
        
        # Konvertiere zu Adjazenzlisten
        adj_A = algo.adjacency_matrix_to_list(A)
        adj_B = algo.adjacency_matrix_to_list(B)
        
        # Vergleiche
        decision, kept = algo.compare_graphs_with_adj_list(A, B)
        
        assert len(adj_A) == A.shape[0]
        assert len(adj_B) == B.shape[0]
        assert decision == "keep_B"
    
    def test_both_methods_give_same_result(self):
        """Test: Beide Methoden liefern gleiches Ergebnis"""
        algo = Subgraph()
        A, B = create_example_graphs()
        
        decision1, kept1 = algo.compare_graphs(A, B)
        decision2, kept2 = algo.compare_graphs_with_adj_list(A, B)
        
        assert decision1 == decision2
        if kept1 is not None and kept2 is not None:
            assert np.array_equal(kept1, kept2)