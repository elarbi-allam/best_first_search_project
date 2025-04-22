import json
import networkx as nx

class Graph:
    """
    Classe représentant un graphe pour l'algorithme Best-First Search.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.start_node = None
        self.goal_node = None
        
    def add_node(self, node_id, heuristic=0):
        """
        Ajoute un nœud au graphe avec sa valeur heuristique.
        
        Args:
            node_id: Identifiant unique du nœud
            heuristic: Valeur heuristique du nœud (estimation du coût pour atteindre le but)
        """
        self.graph.add_node(node_id, heuristic=heuristic)
    
    def add_edge(self, from_node, to_node, weight=1):
        """
        Ajoute une arête orientée entre deux nœuds avec un poids.
        
        Args:
            from_node: Nœud de départ
            to_node: Nœud d'arrivée
            weight: Poids/coût de l'arête
        """
        self.graph.add_edge(from_node, to_node, weight=weight)
    
    def set_start_node(self, node_id):
        """Définit le nœud de départ de la recherche."""
        if node_id in self.graph.nodes:
            self.start_node = node_id
        else:
            raise ValueError(f"Le nœud {node_id} n'existe pas dans le graphe")
    
    def set_goal_node(self, node_id):
        """Définit le nœud objectif de la recherche."""
        if node_id in self.graph.nodes:
            self.goal_node = node_id
        else:
            raise ValueError(f"Le nœud {node_id} n'existe pas dans le graphe")
    
    def get_heuristic(self, node_id):
        """Récupère la valeur heuristique d'un nœud."""
        return self.graph.nodes[node_id]['heuristic']
    
    def get_neighbors(self, node_id):
        """Récupère tous les voisins d'un nœud."""
        return list(self.graph.successors(node_id))
    
    def get_edge_weight(self, from_node_id, to_node_id):
        """Récupère le poids d'une arête entre deux nœuds."""
        return self.graph[from_node_id][to_node_id]['weight']
    
    def save_to_file(self, filename):
        """
        Sauvegarde le graphe dans un fichier JSON.
        
        Args:
            filename: Chemin du fichier pour sauvegarder le graphe
        """
        graph_data = {
            'nodes': [
                {
                    'id': node,
                    'heuristic': self.graph.nodes[node]['heuristic']
                } 
                for node in self.graph.nodes
            ],
            'edges': [
                {
                    'from': edge[0],
                    'to': edge[1],
                    'weight': self.graph.edges[edge]['weight']
                }
                for edge in self.graph.edges
            ],
            'start_node': self.start_node,
            'goal_node': self.goal_node
        }
        
        with open(filename, 'w') as file:
            json.dump(graph_data, file, indent=4)
    
    @classmethod
    def load_from_file(cls, filename):
        """
        Charge un graphe depuis un fichier JSON.
        
        Args:
            filename: Chemin du fichier à charger
            
        Returns:
            Graph: Une instance de graphe chargée depuis le fichier
        """
        with open(filename, 'r') as file:
            graph_data = json.load(file)
        
        graph = cls()
        
        # Ajouter les nœuds
        for node_data in graph_data['nodes']:
            graph.add_node(node_data['id'], node_data['heuristic'])
        
        # Ajouter les arêtes
        for edge_data in graph_data['edges']:
            graph.add_edge(edge_data['from'], edge_data['to'], edge_data['weight'])
        
        # Définir les nœuds de départ et d'arrivée
        if graph_data.get('start_node'):
            graph.set_start_node(graph_data['start_node'])
        
        if graph_data.get('goal_node'):
            graph.set_goal_node(graph_data['goal_node'])
        
        return graph
    
    def create_example_graph_1(self):
        """Crée un exemple de graphe simple pour tester l'algorithme."""
        # Nœuds avec heuristiques (estimations de distance à l'objectif)
        self.add_node('A', 7)
        self.add_node('B', 6)
        self.add_node('C', 4)
        self.add_node('D', 5)
        self.add_node('E', 2)
        self.add_node('F', 1)
        self.add_node('G', 0)  # Objectif
        
        # Arêtes avec poids (coût réel entre les nœuds)
        self.add_edge('A', 'B', 3)
        self.add_edge('A', 'C', 2)
        self.add_edge('B', 'D', 2)
        self.add_edge('C', 'D', 1)
        self.add_edge('C', 'E', 3)
        self.add_edge('D', 'E', 4)
        self.add_edge('D', 'F', 5)
        self.add_edge('E', 'G', 2)
        self.add_edge('F', 'G', 1)
        
        # Définir le nœud de départ et d'arrivée
        self.set_start_node('A')
        self.set_goal_node('G')
        
    def create_example_graph_2(self):
        """Crée un exemple de graphe plus complexe."""
        # Nœuds avec heuristiques
        self.add_node('S', 10)  # Départ
        self.add_node('A', 8)
        self.add_node('B', 7)
        self.add_node('C', 6)
        self.add_node('D', 4)
        self.add_node('E', 3)
        self.add_node('F', 2)
        self.add_node('G', 0)  # Objectif
        self.add_node('H', 5)
        self.add_node('I', 4)
        
        # Arêtes avec poids
        self.add_edge('S', 'A', 2)
        self.add_edge('S', 'B', 3)
        self.add_edge('A', 'C', 3)
        self.add_edge('B', 'D', 5)
        self.add_edge('C', 'E', 5)
        self.add_edge('C', 'H', 8)
        self.add_edge('D', 'F', 2)
        self.add_edge('E', 'G', 4)
        self.add_edge('F', 'G', 3)
        self.add_edge('H', 'I', 2)
        self.add_edge('I', 'G', 3)
        
        # Définir le nœud de départ et d'arrivée
        self.set_start_node('S')
        self.set_goal_node('G')