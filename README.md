# Documentation

## Structures de données principales

### Classe `Node`

Représente une personne dans le graphe.

**Attributs** :
- `id` (int) : Identifiant unique de la personne
- `name` (str) : Prénom de la personne
- `surname` (str) : Nom de famille de la personne
- `avatar` (str) : Chemin ou URL vers l'avatar/photo de la personne
- `birthday` (str) : Date de naissance de la personne
- `sex` (bool) : Genre de la personne (probablement True pour masculin, False pour féminin)
- `relationships` (List[Union['Vertex', int]]) : Liste des relations (arêtes) que cette personne entretient avec d'autres personnes

### Classe `Vertex`

Représente une relation/arête entre deux personnes dans le graphe.

**Attributs** :
- `id` (str) : Identifiant unique de la relation
- `rank` (int) : Niveau ou degré de la relation (important pour la contrainte mentionnée)
- `parent` (Union[Node, int]) : Personne considérée comme "parent" dans cette relation, ou son ID
- `child` (Union[Node, int]) : Personne considérée comme "enfant" dans cette relation, ou son ID

**Contrainte importante** : Le nombre maximum de parents de rang k pour un nœud est limité à 2^k.

### Classe `Graph`

Représente l'ensemble du graphe de relations.

**Attributs** :
- `nodes` (List[Node]) : Liste de toutes les personnes dans le graphe
- `vertices` (List[Vertex]) : Liste de toutes les relations dans le graphe

## Gestion des opérations - Cas d'utilisation

### Classe `UseCases`

Cette classe implémente les fonctionnalités de base pour manipuler le graphe.

**Méthodes** :
- `create_node(node: Node)` : Ajoute une nouvelle personne au graphe
- `update_node(id: int, name: str, surname: str...)` : Met à jour les informations d'une personne existante
- `delete_node(id: int)` : Supprime une personne du graphe et toutes ses relations
- `create_vertex(rank: int, parent: Node, child: Node)` : Crée une nouvelle relation entre deux personnes avec un rang spécifique
- `delete_vertex(id: int)` : Supprime une relation spécifique
- `updateVertex(id: int, rank: int, parent: int = None, child: int = None)` : Met à jour les informations d'une relation existante
- `loadFromJson(json: object)` : Charge un graphe à partir d'un objet JSON
- `load_from_csv(nodes_path: Path, vertices_path: Path)` : Charge un graphe à partir de fichiers CSV (un pour les personnes, un pour les relations)

## Algorithmes d'analyse et de traitement

### Classe abstraite `Solver`

Représente un résolveur abstrait pour exécuter des algorithmes sur le graphe.

**Méthodes** :
- `solve()` (abstraite) : Méthode à implémenter par les sous-classes pour exécuter l'algorithme spécifique

### Sous-classes de `Solver`

Différents algorithmes applicables au graphe, chacun avec son utilité particulière :

#### `DijkstraSolver` et `BellmanFordSolver`
Ces deux solveurs permettent de trouver le chemin le plus court entre deux nœuds spécifiques.

**Attributs** :
- `startNode` : Nœud de départ
- `endNode` : Nœud d'arrivée

**Cas d'utilisation** : Trouver la relation la plus proche entre deux personnes dans l'arbre généalogique ou le réseau social.

#### `PrimSolver` et `KruskalSolver`
Ces solveurs permettent de trouver l'arbre couvrant de poids minimum dans le graphe.

**Attributs** :
- `initialGraph` : Le graphe sur lequel appliquer l'algorithme

**Cas d'utilisation** : Identifier les relations essentielles dans un réseau complexe de personnes, potentiellement pour simplifier la visualisation ou l'analyse.

#### `DepthFirstSearchSolver`
Implémente un parcours en profondeur du graphe.

**Attributs** :
- `initialGraph` : Le graphe à parcourir

**Cas d'utilisation** : Explorer systématiquement les branches familiales ou les relations, idéal pour rechercher des ancêtres spécifiques ou tracer des lignées complètes.

#### `BreadthFirstSearchSolver`
Implémente un parcours en largeur du graphe.

**Attributs** :
- `initialGraph` : Le graphe à parcourir

**Cas d'utilisation** : Explorer les relations par niveau de proximité, parfait pour identifier les personnes à un degré de séparation spécifique d'une personne donnée.

