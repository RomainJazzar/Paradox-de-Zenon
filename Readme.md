# Les Paradoxes de Zénon d'Élée
## Simulations Informatiques et Analyse Algorithmique

> *"La nature nous a donné une langue et deux oreilles afin que nous écoutions le double de ce que nous disons."* - Zénon d'Élée

## 📖 Contexte du Projet

Ce projet explore computationnellement les trois paradoxes célèbres du philosophe présocratique **Zénon d'Élée** (VIe siècle av. J.-C.). Ces paradoxes, conçus pour défendre la philosophie de Parménide sur l'impossibilité du mouvement et de la multiplicité, soulèvent des questions fondamentales sur la nature de l'espace, du temps et du mouvement.

### Les Paradoxes Étudiés

1. **Achille et la Tortue** - Le héros ne peut jamais rattraper la tortue qui a une longueur d'avance
2. **La Dichotomie** - Une pierre ne peut jamais atteindre un arbre car elle doit parcourir une infinité d'étapes
3. **La Flèche en Vol** - Une flèche est immobile à chaque instant, donc le mouvement est impossible

## 🎯 Problématique

**Question centrale :** Comment la simulation informatique peut-elle nous aider à comprendre et résoudre ces paradoxes millénaires qui questionnent notre intuition du mouvement ?

**Enjeux algorithmiques :**
- Représentation numérique de l'infini
- Convergence des séries mathématiques
- Limites de la précision computationnelle
- Discrétisation du temps continu

## 🚀 Solutions Implémentées

### 1. Achille et la Tortue (`achille_tortue.py`)

**Approche algorithmique :**
```python
while position_achille < position_tortue:
    position_achille += vitesse_achille * dt
    position_tortue += vitesse_tortue * dt
```

**Résolution mathématique :**
- Équation : `10t = 100 + 1t` → `t = 100/9 ≈ 11.11s`
- **Conclusion :** Achille rattrape la tortue ! Le paradoxe vient de l'analyse infinie d'étapes finies.

### 2. Dichotomie (`dichotomie.py`)

**Approche algorithmique :**
```python
while distance_restante > seuil_precision:
    position_pierre += distance_restante / 2
    distance_restante = position_arbre - position_pierre
```

**Résolution par série géométrique :**
- Série : `4 + 2 + 1 + 0.5 + 0.25 + ...`
- Somme : `S = 4/(1-0.5) = 8 mètres`
- **Conclusion :** La pierre atteint l'arbre ! La série infinie converge vers une valeur finie.

### 3. Flèche en Vol (`fleche_vol.py`)

**Approche algorithmique :**
```python
for dt in [1.0, 0.1, 0.01, 0.001, 0.0001]:
    vitesse_instantanee = deplacement / dt
```

**Résolution par calcul différentiel :**
- Vitesse instantanée : `v = dx/dt = lim(Δt→0) Δx/Δt`
- **Conclusion :** Le concept de dérivée résout le paradoxe ! La vitesse instantanée existe même si la position est fixe à un instant donné.

### 4. Visualisations Pygame

Interface graphique interactive permettant de :
- Visualiser en temps réel les simulations
-