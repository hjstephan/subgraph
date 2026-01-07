# Subgraph Algorithmus

Ein effizienter Algorithmus zum Vergleichen zweier Graphen $G$ und $G'$ mittels Adjazenzmatrizen und Signatur-Arrays. Der Algorithmus bestimmt durch zyklische Rotation, ob ein Graph als Subgraph in einem anderen enthalten ist.

## 🎯 Problemstellung

Gegeben sind zwei Graphen $G$ und $G'$ mit jeweils $n$ Knoten, repräsentiert durch Adjazenzmatrizen $A$ und $B$. 

**Ziel**: Bestimme, ob Graph $G$ in Graph $G'$ enthalten ist, unter Berücksichtigung aller möglichen Knotenzuordnungen durch zyklische Rotation.

**Ergebnis**:
- Wenn $B$ die Matrix $A$ enthält ($B \supseteq A$): Verwerfe $A$, behalte $B$ ($G'$ hat mehr Informationen)
- Wenn $A$ die Matrix $B$ enthält ($A \supseteq B$): Behalte $A$, verwerfe $B$ ($G$ hat mehr Informationen)
- Wenn beide identisch sind: Beliebige behalten
- Wenn keiner den anderen enthält: Beide behalten

## 🔑 Kernidee

Der Algorithmus basiert auf zwei zentralen Konzepten:

### 1. Eindeutige Signaturen

Für jede Spalte der Adjazenzmatrix wird eine eindeutige Signatur berechnet:

```
Signatur = Σ(2^i) für alle Zeilen i mit Wert 1 + Spaltenindex * 2^n
```

**Beispiel** ($n=4$):
```
Spalte 0: [1, 0, 1, 0] → 2^0 + 2^2 + 0*(2^4) = 1 + 4 + 0 = 5
Spalte 1: [1, 0, 1, 0] → 2^0 + 2^2 + 1*(2^4) = 1 + 4 + 16 = 21
```

**Warum eindeutig?**
- Die Zeilenkomponente $\sum 2^i$ kodiert jede Binärkombination eindeutig
- Die Spaltengewichtung $\text{col} \cdot 2^n$ unterscheidet gleiche Muster an verschiedenen Positionen

### 2. Zyklische Rotation

Statt alle $n!$ Permutationen zu prüfen, werden nur **$n$ zyklische Rotationen** betrachtet:

```
Original:   [sig_0, sig_1, sig_2, sig_3]
Rotation 1: [sig_1, sig_2, sig_3, sig_0]
Rotation 2: [sig_2, sig_3, sig_0, sig_1]
Rotation 3: [sig_3, sig_0, sig_1, sig_2]
```

Dies erhält die sequentielle Ordnung und reduziert die Komplexität drastisch.

## ⏱️ Laufzeitkomplexität: $O(n^3)$

### Detaillierte Analyse

Der Algorithmus arbeitet in drei Schritten:

**Schritt 1**: Signatur von $G$ berechnen
```
- Iteriere über n × n Matrix-Einträge
- Komplexität: O(n²)
```

**Schritt 2**: Signatur von $G'$ berechnen
```
- Iteriere über n × n Matrix-Einträge
- Komplexität: O(n²)
```

**Schritt 3**: Alle zyklischen Rotationen prüfen
```
- Für jede der n Rotationen:
  - Signatur neu berechnen: O(n²)
  - Sequenzen vergleichen: O(n²)
- Komplexität: O(n * (n² + n²)) = O(n³)
```

Für beide Richtungen ($A \subseteq B$ und $B \subseteq A$): **$O(n^3)$**

**Wichtig**: Der Algorithmus verwendet **nur $n$ Rotationen**, nicht $n!$ Permutationen!

Die Rotation der Spalten entspricht dem Drehen des Graphen. Dabei bleibt die Struktur des Graphen, gegeben durch die Verbundenheit der Knoten und Kanten, immer erhalten. Deshalb sind nur $n$ Rotation zu betrachten und nicht $n!$ viele Permutationen. Der Graph wird so lange gedreht, bis eine Subgraph-Beziehung existiert oder das Drehen vollständig durchgeführt wurde, ohne dass eine Subgraph-Beziehung existiert. Zur Überprüfung der Subgraph-Beziehung werden die Elemente der Signatur-Arrays in $O(n^2)$ Laufzeit verglichen. 

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/hjstephan/subgraph.git
cd subgraph

# Virtual Environment erstellen
python -m venv venv
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# Package installieren (optional)
pip install -e .
```

## 💻 Verwendung

### Grundlegendes Beispiel

```python
import numpy as np
from subgraph import Subgraph

# Algorithmus initialisieren
algo = Subgraph()

# Graph G definieren
G = np.array([
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
])

# Graph G' definieren (mit zusätzlicher Kante)
G_prime = np.array([
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
])

# Graphen vergleichen
decision, kept_matrix = algo.compare_graphs(G, G_prime)

print(f"Entscheidung: {decision}")
# Output: "keep_B" (G' hat mehr Informationen)
```

### Signaturen berechnen

```python
# Signaturen einzeln berechnen
signatures_G = algo._compute_column_signature(G)
print(f"Signaturen von G: {signatures_G}")
# Output: [1, 18, 36, 48]

signatures_G_prime = algo._compute_column_signature(G_prime)
print(f"Signaturen von G': {signatures_G_prime}")
# Output: [5, 18, 36, 48]
```

### Rotation-Match prüfen

```python
# Prüfe ob G in G' enthalten ist (mit Rotationen)
is_contained = algo._find_signature_rotation_match(
    signatures_G, 
    signatures_G_prime
)
print(f"G in G' enthalten: {is_contained}")
# Output: True
```

## 🧪 Tests

Das Projekt verwendet pytest mit umfassender Test-Suite und Code-Coverage.

### Alle Tests ausführen

```bash
pytest
```

### Mit ausführlichem Output

```bash
pytest -v
```

### Spezifische Tests

```bash
# Nur Signatur-Tests
pytest tests/test_subgraph.py::TestSubgraph::test_compute_column_signature_complex -v

# Nur Integration-Tests
pytest tests/test_integration.py -v
```

### Test-Struktur

```
tests/
├── test_subgraph.py          # Haupttests (37 Tests)
├── test_integration.py       # Integrationstests
└── test_performace.py        # Performance-Tests
```

## 🔧 Erweiterte Verwendung

### Mit Adjazenzlisten

Für sparse Graphen kann die Adjazenzlisten-Methode effizienter sein:

```python
algo = Subgraph(use_adjacency_list=True)

# Direkter Vergleich ohne Rotation (für einfache Fälle)
decision, kept = algo.compare_graphs_with_adj_list(G, G_prime)
```

**Komplexität**: $O(n + m)$ für $m$ Kanten (bei sparse Graphen)

### Verschiedene Graphgrößen

Der Algorithmus unterstützt Graphen unterschiedlicher Größe:

```python
# G: 3×3, G': 5×5
G_small = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, 0]
])

G_large = np.array([
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]
])

decision, kept = algo.compare_graphs(G_small, G_large)
# Prüft ob G_small als Subgraph in G_large enthalten ist
```
