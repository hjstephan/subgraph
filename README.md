# Subgraph Algorithmus

Ein effizienter Algorithmus zum Vergleichen zweier Graphen G und G' mittels Adjazenzmatrizen und Signatur-Arrays. Der Algorithmus bestimmt durch zyklische Rotation, ob ein Graph als Subgraph in einem anderen enthalten ist.

## 🎯 Problemstellung

Gegeben sind zwei Graphen G und G' mit jeweils n Knoten, repräsentiert durch Adjazenzmatrizen A und B. 

**Ziel**: Bestimme, ob Graph G in Graph G' enthalten ist, unter Berücksichtigung aller möglichen Knotenzuordnungen durch zyklische Rotation.

**Ergebnis**:
- Wenn B die Matrix A enthält (B ⊇ A): Verwerfe A, behalte B (G' hat mehr Informationen)
- Wenn A die Matrix B enthält (A ⊇ B): Behalte A, verwerfe B (G hat mehr Informationen)
- Wenn beide identisch sind: Beliebige behalten
- Wenn keiner den anderen enthält: Beide behalten

## 🔑 Kernidee

Der Algorithmus basiert auf zwei zentralen Konzepten:

### 1. Eindeutige Signaturen

Für jede Spalte der Adjazenzmatrix wird eine eindeutige Signatur berechnet:

```
Signatur = Σ(2^i für alle Zeilen i mit Wert 1) + Spaltenindex * 2^n
```

**Beispiel** (n=4):
```
Spalte 0: [1, 0, 1, 0] → 2^0 + 2^2 + 0*(2^4) = 1 + 4 + 0 = 5
Spalte 1: [1, 0, 1, 0] → 2^0 + 2^2 + 1*(2^4) = 1 + 4 + 16 = 21
```

**Warum eindeutig?**
- Die Zeilenkomponente (Σ 2^i) kodiert jede Binärkombination eindeutig
- Die Spaltengewichtung (col * 2^n) unterscheidet gleiche Muster an verschiedenen Positionen

### 2. Zyklische Rotation

Statt alle n! Permutationen zu prüfen, werden nur **n zyklische Rotationen** betrachtet:

```
Original:   [sig_0, sig_1, sig_2, sig_3]
Rotation 1: [sig_1, sig_2, sig_3, sig_0]
Rotation 2: [sig_2, sig_3, sig_0, sig_1]
Rotation 3: [sig_3, sig_0, sig_1, sig_2]
```

Dies erhält die sequentielle Ordnung und reduziert die Komplexität drastisch.

## ⏱️ Laufzeitkomplexität: O(n³)

### Detaillierte Analyse

Der Algorithmus arbeitet in drei Schritten:

**Schritt 1**: Signatur von G berechnen
```
- Iteriere über n × n Matrix-Einträge
- Komplexität: O(n²)
```

**Schritt 2**: Signatur von G' berechnen
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

Für beide Richtungen (A⊆B und B⊆A): **O(n³)**

### Warum nicht O(n!)?

**Wichtig**: Der Algorithmus verwendet **nur n Rotationen**, nicht n! Permutationen!

- **Alle Permutationen**: n! = 1·2·3·...·n (exponentiell)
  - Für n=10: 3.628.800 Möglichkeiten
- **Nur Rotationen**: n (linear in der Anzahl)
  - Für n=10: 10 Möglichkeiten

Die zyklische Rotation erhält die sequentielle Ordnung der Knoten und vermeidet die kombinatorische Explosion.

## 📦 Installation

### Voraussetzungen

```bash
python >= 3.8
numpy >= 1.21.0
```

### Aus dem Repository

```bash
# Repository klonen
git clone https://github.com/hjstephan/subgraph.git
cd subgraph

# Virtual Environment erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Dependencies installieren
pip install -r requirements.txt

# Package installieren (optional)
pip install -e .
```

### Requirements

```txt
numpy>=1.21.0
pytest>=7.0.0
pytest-cov>=3.0.0
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

### Coverage-Report generieren

```bash
pytest --cov=src --cov-report=html
```

Der HTML-Report wird in `doc/htmlcov/index.html` erstellt.

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

**Coverage**: Ziel ist 80%+ Code Coverage

## 📊 API-Referenz

### Klasse: `Subgraph`

#### `__init__(use_adjacency_list: bool = False)`

Initialisiert den Algorithmus.

**Parameter**:
- `use_adjacency_list`: Wenn True, wird Adjazenzliste für Vergleiche verwendet

#### `compare_graphs(A: np.ndarray, B: np.ndarray) -> Tuple[str, np.ndarray]`

Vergleicht zwei Graphen mittels Signatur-Arrays und zyklischer Rotation.

**Parameter**:
- `A`: Adjazenzmatrix von Graph G (n×n)
- `B`: Adjazenzmatrix von Graph G' (n×n)

**Returns**:
- `("keep_B", B)`: Wenn B ⊇ A (G' hat mehr Informationen)
- `("keep_A", A)`: Wenn A ⊇ B (G hat mehr Informationen)
- `("equal", A)`: Wenn beide identisch/isomorph sind
- `("keep_both", None)`: Wenn keiner den anderen enthält

**Komplexität**: O(n³)

#### `_compute_column_signature(matrix: np.ndarray) -> List[int]`

Berechnet eindeutige Signaturen für alle Spalten einer Matrix.

**Parameter**:
- `matrix`: Adjazenzmatrix (n×n)

**Returns**:
- Liste von eindeutigen Integer-Signaturen

**Komplexität**: O(n²)

#### `_find_signature_rotation_match(sig_A: List[int], sig_B: List[int]) -> bool`

Sucht nach zyklischer Rotation, bei der sig_A in sig_B enthalten ist.

**Parameter**:
- `sig_A`: Signaturen von Graph G
- `sig_B`: Signaturen von Graph G'

**Returns**:
- `True`: Wenn Match gefunden wurde
- `False`: Wenn kein Match existiert

**Komplexität**: O(n³) für n Rotationen

#### `_compare_signature_sequences(seq_A: List[int], seq_B: List[int]) -> bool`

Vergleicht zwei Signatur-Sequenzen elementweise mit Bit-Operationen.

**Parameter**:
- `seq_A`: Sequenz von Zeilenkomponenten aus A
- `seq_B`: Sequenz von Zeilenkomponenten aus B

**Returns**:
- `True`: Wenn für alle i gilt: (seq_A[i] & seq_B[i]) == seq_A[i]

**Komplexität**: O(n)

#### `analyze_complexity(n: int) -> dict`

Gibt detaillierte Laufzeitanalyse für n Knoten zurück.

**Parameter**:
- `n`: Anzahl der Knoten

**Returns**:
- Dictionary mit Komplexitätsanalyse für jeden Schritt

## 🎓 Theoretischer Hintergrund

### Polynomiale Hash-Funktion

Die Signatur-Berechnung nutzt eine polynomiale Hash-Funktion, die garantiert kollisionsfrei ist:

```
f(v, col) = Σ(2^i · v[i]) + col · 2^n
```

**Eigenschaften**:
- **Injektiv**: Jede Spalten-Konfiguration erhält eindeutige Signatur
- **Effizient**: O(n) Berechnung pro Spalte
- **Bit-kompatibel**: Ermöglicht schnelle Containment-Prüfung via AND-Operation

### Zyklische Rotation vs. Vollständige Permutation

**Problem**: Subgraph-Isomorphismus ist NP-vollständig

**Vereinfachung**: Beschränkung auf zyklische Rotationen
- Reduziert Suchraum von O(n!) auf O(n)
- Erhält strukturelle Eigenschaften (sequentielle Ordnung)

**Trade-off**: 
- ✅ Polynomielle Laufzeit O(n³)
- ⚠️ Findet nur Matches unter zyklischen Rotationen
- ⚠️ Vollständiges Subgraph-Isomorphismus erfordert O(n!)

### Bit-Operationen für Containment

Der Algorithmus nutzt effiziente Bit-Operationen:

```python
# Prüfe ob alle Kanten von A in B sind
(sig_A & sig_B) == sig_A
```

Dies ist äquivalent zu: "Alle Bits, die in A gesetzt sind, sind auch in B gesetzt"

## 🔧 Erweiterte Verwendung

### Mit Adjazenzlisten

Für sparse Graphen kann die Adjazenzlisten-Methode effizienter sein:

```python
algo = Subgraph(use_adjacency_list=True)

# Direkter Vergleich ohne Rotation (für einfache Fälle)
decision, kept = algo.compare_graphs_with_adj_list(G, G_prime)
```

**Komplexität**: O(n + m) für m Kanten (bei sparse Graphen)

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

## 🤝 Beitragen

Beiträge sind willkommen! Bitte beachten Sie:

1. Fork des Repositories
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Tests für neue Features hinzufügen
4. Sicherstellen, dass alle Tests bestehen (`pytest`)
5. Code committen (`git commit -m 'Add amazing feature'`)
6. Branch pushen (`git push origin feature/amazing-feature`)
7. Pull Request öffnen

## 👤 Autor

**Stephan Epp**
- Email: hjstephan86@gmail.com
- GitHub: [@hjstephan](https://github.com/hjstephan)

## 🔗 Verwandte Arbeiten

- **Subgraph Isomorphismus**: NP-vollständiges Problem der Graphentheorie
- **Graph Matching**: Verwandte Probleme in Computer Vision und Pattern Recognition
- **Polynomiale Hash-Funktionen**: Anwendungen in String-Matching und Datenstrukturen

## 📚 Weiterführende Literatur

- Ullmann, J. R. (1976). "An Algorithm for Subgraph Isomorphism"
- Cook, S. A. (1971). "The complexity of theorem-proving procedures"
- Cormen et al. (2009). "Introduction to Algorithms" (Graph Algorithms)

**Status**: Active Development | **Version**: 1.0.0 | **Python**: 3.8+