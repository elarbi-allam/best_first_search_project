import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import numpy as np

class GraphVisualizer:
    """
    Classe pour visualiser le graphe et les résultats de l'algorithme BFS.
    """
    def __init__(self, graph):
        """
        Initialise le visualiseur avec un graphe.
        
        Args:
            graph: Instance de la classe Graph à visualiser
        """
        self.graph = graph
        self.fig = None
        self.ax = None
        self.pos = None
        
    def draw_graph(self, title="Graphe"):
        """
        Dessine le graphe avec les nœuds et les arêtes.
        
        Args:
            title: Titre du graphique
        """
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        graph_nx = self.graph.graph
        
        # Utiliser spring_layout pour positionner les nœuds automatiquement
        self.pos = nx.spring_layout(graph_nx, seed=42)
        
        # Dessiner les arêtes avec leur poids
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph_nx.edges(data=True)}
        nx.draw_networkx_edge_labels(graph_nx, self.pos, edge_labels=edge_labels)
        
        # Dessiner les arêtes
        nx.draw_networkx_edges(graph_nx, self.pos, arrows=True, arrowsize=20)
        
        # Dessiner les nœuds avec leur label et valeur heuristique
        node_labels = {node: f"{node}\nh={graph_nx.nodes[node]['heuristic']}" 
                       for node in graph_nx.nodes()}
        
        # Couleurs spéciales pour les nœuds de départ et d'arrivée
        node_colors = ['green' if node == self.graph.start_node else 
                      'red' if node == self.graph.goal_node else 
                      'skyblue' for node in graph_nx.nodes()]
        
        nx.draw_networkx_nodes(graph_nx, self.pos, node_color=node_colors, 
                              node_size=700)
        nx.draw_networkx_labels(graph_nx, self.pos, labels=node_labels)
        
        # Ajouter un titre et nettoyer l'affichage
        plt.title(title, fontsize=16)
        plt.axis('off')
        
        return self.fig, self.ax
    
    def visualize_path(self, path, title="Chemin trouvé par Best-First Search"):
        """
        Visualise le chemin trouvé par l'algorithme.
        
        Args:
            path: Liste des nœuds formant le chemin solution
            title: Titre du graphique
        """
        if path is None:
            print("Aucun chemin trouvé.")
            return
        
        fig, ax = self.draw_graph(title)
        
        # Créer une liste des arêtes du chemin pour les mettre en évidence
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        
        # Dessiner les arêtes du chemin en rouge et plus épaisses
        nx.draw_networkx_edges(self.graph.graph, self.pos, 
                              edgelist=path_edges, 
                              edge_color='red', 
                              width=3)
        
        # Mettre en évidence les nœuds du chemin
        path_nodes = path[1:-1]  # Exclure départ et arrivée qui ont déjà des couleurs spéciales
        if path_nodes:
            nx.draw_networkx_nodes(self.graph.graph, self.pos, 
                                  nodelist=path_nodes, 
                                  node_color='yellow', 
                                  node_size=700)
        
        return fig, ax
    
    def animate_search(self, steps, path, interval=1000, save_animation=False, filename='search_animation.mp4'):
        """
        Crée une animation de l'algorithme de recherche.
        
        Args:
            steps: Liste des états à chaque étape de l'algorithme
            path: Chemin final trouvé
            interval: Intervalle entre les images en millisecondes
            save_animation: Si True, sauvegarde l'animation dans un fichier
            filename: Nom du fichier pour sauvegarder l'animation
            
        Returns:
            Animation
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def init():
            ax.clear()
            graph_nx = self.graph.graph
            
            # Dessiner les arêtes
            nx.draw_networkx_edges(graph_nx, self.pos, arrows=True, arrowsize=20, ax=ax)
            
            # Dessiner les nœuds avec leur label et valeur heuristique
            node_labels = {node: f"{node}\nh={graph_nx.nodes[node]['heuristic']}" 
                           for node in graph_nx.nodes()}
            
            # Couleurs spéciales pour les nœuds de départ et d'arrivée
            node_colors = ['green' if node == self.graph.start_node else 
                          'red' if node == self.graph.goal_node else 
                          'skyblue' for node in graph_nx.nodes()]
            
            nx.draw_networkx_nodes(graph_nx, self.pos, node_color=node_colors, 
                                  node_size=700, ax=ax)
            nx.draw_networkx_labels(graph_nx, self.pos, labels=node_labels, ax=ax)
            
            # Dessiner les poids des arêtes
            edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph_nx.edges(data=True)}
            nx.draw_networkx_edge_labels(graph_nx, self.pos, edge_labels=edge_labels, ax=ax)
            
            ax.set_title("Exécution de Best-First Search", fontsize=16)
            ax.axis('off')
            return []
        
        def update(frame_num):
            ax.clear()
            step = steps[frame_num] if frame_num < len(steps) else steps[-1]
            
            graph_nx = self.graph.graph
            
            # Dessiner toutes les arêtes normales
            nx.draw_networkx_edges(graph_nx, self.pos, arrows=True, arrowsize=20, ax=ax)
            
            # Dessiner les poids des arêtes
            edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph_nx.edges(data=True)}
            nx.draw_networkx_edge_labels(graph_nx, self.pos, edge_labels=edge_labels, ax=ax)
            
            # Préparer les couleurs des nœuds selon leur état
            node_colors = []
            for node in graph_nx.nodes():
                if node == self.graph.start_node:
                    node_colors.append('green')
                elif node == self.graph.goal_node:
                    node_colors.append('red')
                elif node == step['current']:
                    node_colors.append('orange')  # Nœud actuel
                elif node in step['visited']:
                    node_colors.append('gray')    # Nœuds visités
                else:
                    node_colors.append('skyblue') # Nœuds non visités
            
            # Dessiner tous les nœuds
            nx.draw_networkx_nodes(graph_nx, self.pos, node_color=node_colors, 
                                  node_size=700, ax=ax)
            
            # Dessiner les labels des nœuds
            node_labels = {node: f"{node}\nh={graph_nx.nodes[node]['heuristic']}" 
                           for node in graph_nx.nodes()}
            nx.draw_networkx_labels(graph_nx, self.pos, labels=node_labels, ax=ax)
            
            # Dessiner le chemin trouvé jusqu'à présent
            path_so_far = step['path_so_far']
            if len(path_so_far) > 1:
                path_edges = [(path_so_far[i], path_so_far[i+1]) for i in range(len(path_so_far)-1)]
                nx.draw_networkx_edges(graph_nx, self.pos, edgelist=path_edges, 
                                      edge_color='red', width=3, ax=ax)
            
            # Ajouter des informations sur l'état actuel
            info_text = f"Étape {frame_num+1}/{len(steps)}\n"
            info_text += f"Nœud actuel: {step['current']}\n"
            info_text += f"Nœuds visités: {', '.join(step['visited'])}\n"
            
            # Ajouter un titre
            if step['current'] == self.graph.goal_node:
                ax.set_title("Objectif atteint!", fontsize=16)
            else:
                ax.set_title(f"Exploration du nœud {step['current']}", fontsize=16)
            
            ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=10,
                   bbox=dict(facecolor='white', alpha=0.8))
            
            ax.axis('off')
            return []
        
        # Créer l'animation
        ani = animation.FuncAnimation(fig, update, frames=len(steps), 
                                     init_func=init, blit=True, interval=interval)
        
        # Sauvegarder l'animation si demandé
        if save_animation:
            # S'assurer que ffmpeg est installé pour MP4
            writer = animation.FFMpegWriter(fps=1)
            ani.save(filename, writer=writer)
        
        plt.close()  # Fermer la figure mais pas l'animation
        return ani
    
    def show(self):
        """Affiche la visualisation."""
        plt.tight_layout()
        plt.show()
    
    def save_figure(self, filename):
        """
        Sauvegarde la figure actuelle dans un fichier.
        
        Args:
            filename: Nom du fichier pour sauvegarder la figure
        """
        plt.savefig(filename, bbox_inches='tight')