#!/usr/bin/env python3
"""
Version graphique avec Pygame du paradoxe de la Flèche en Vol
Simulation interactive avec analyse des instants
"""

import pygame
import sys
import math
import random

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 1400
HAUTEUR = 900
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
GRIS = (128, 128, 128)
GRIS_CLAIR = (200, 200, 200)
JAUNE = (255, 255, 0)
ORANGE = (255, 165, 0)
VIOLET = (128, 0, 128)
CYAN = (0, 255, 255)
ROSE = (255, 192, 203)

class FlecheVolSimulation:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("🏹 Paradoxe de la Flèche en Vol - Zénon d'Élée")
        self.horloge = pygame.time.Clock()
        
        # Polices
        self.font_petit = pygame.font.Font(None, 18)
        self.font = pygame.font.Font(None, 24)
        self.font_titre = pygame.font.Font(None, 36)
        self.font_grand = pygame.font.Font(None, 48)
        
        # Paramètres de simulation
        self.reset_simulation()
        
        # Interface
        self.simulation_active = False
        self.vitesse_simulation = 1.0
        self.mode_analyse = "continu"  # "continu", "instants", "derivee", "quantique"
        self.delta_t_actuel = 0.1
        self.deltas_disponibles = [1.0, 0.5, 0.1, 0.05, 0.01, 0.001]
        self.index_delta = 2
        
        # Effets visuels
        self.particules_fleche = []
        self.trail_fleche = []
        self.instant_fige = False
        self.temps_gel = 0.0
        
        # Analyse quantique
        self.positions_quantiques = []
        self.incertitude_active = False
        
    def reset_simulation(self):
        """Remet à zéro la simulation"""
        self.position_fleche = 0.0
        self.position_cible = 800.0  # 800 pixels = 80m
        self.vitesse_fleche = 120.0  # 120 pixels/seconde = 12 m/s
        self.temps = 0.0
        self.historique_positions = []
        self.historique_temps = []
        self.historique_vitesses = []
        self.vol_termine = False
        self.particules_fleche = []
        self.trail_fleche = []
        self.instant_analyse = 0
        self.positions_quantiques = []
        
    def ajouter_particule_fleche(self):
        """Ajoute des particules de trainée pour la flèche"""
        if len(self.particules_fleche) < 50:
            particule = {
                'x': 100 + self.position_fleche + random.uniform(-5, 5),
                'y': HAUTEUR//2 + random.uniform(-3, 3),
                'vx': random.uniform(-20, -10),
                'vy': random.uniform(-10, 10),
                'vie': 1.0,
                'taille': random.uniform(1, 3)
            }
            self.particules_fleche.append(particule)
    
    def mettre_a_jour_particules(self, dt):
        """Met à jour les particules d'effet"""
        for particule in self.particules_fleche[:]:
            particule['x'] += particule['vx'] * dt
            particule['y'] += particule['vy'] * dt
            particule['vie'] -= dt * 2
            particule['taille'] *= 0.99
            if particule['vie'] <= 0:
                self.particules_fleche.remove(particule)
    
    def dessiner_particules(self):
        """Dessine les particules d'effet"""
        for particule in self.particules_fleche:
            alpha = int(particule['vie'] * 255)
            couleur = ORANGE
            rayon = max(1, int(particule['taille']))
            pygame.draw.circle(self.ecran, couleur, 
                             (int(particule['x']), int(particule['y'])), rayon)
    
    def dessiner_scene(self):
        """Dessine la scène de tir (arc, flèche, cible)"""
        y_vol = HAUTEUR // 2
        
        # Ligne de vol
        pygame.draw.line(self.ecran, GRIS_CLAIR, (100, y_vol), (900, y_vol), 2)
        
        # Arc (position de départ)
        arc_x = 80
        pygame.draw.arc(self.ecran, NOIR, (arc_x - 15, y_vol - 30, 30, 60), 
                       math.pi * 0.2, math.pi * 1.8, 3)
        # Corde d'arc
        pygame.draw.line(self.ecran, NOIR, (arc_x - 10, y_vol - 25), (arc_x - 10, y_vol + 25), 2)
        
        # Cible (cercles concentriques)
        cible_x = 100 + self.position_cible
        for i, (rayon, couleur) in enumerate([(30, ROUGE), (20, BLANC), (10, ROUGE)]):
            pygame.draw.circle(self.ecran, couleur, (int(cible_x), y_vol), rayon)
            pygame.draw.circle(self.ecran, NOIR, (int(cible_x), y_vol), rayon, 2)
        
        # Centre de la cible
        pygame.draw.circle(self.ecran, NOIR, (int(cible_x), y_vol), 3)
        
        # Marqueurs de distance
        for i in range(0, 900, 100):
            x = 100 + i
            pygame.draw.line(self.ecran, GRIS, (x, y_vol - 5), (x, y_vol + 5), 1)
            distance_m = i // 10  # 1m = 10 pixels
            texte = self.font_petit.render(f"{distance_m}m", True, GRIS)
            self.ecran.blit(texte, (x - 8, y_vol + 10))
    
    def dessiner_fleche(self):
        """Dessine la flèche avec détails"""
        if self.position_fleche >= self.position_cible:
            return
        
        y_vol = HAUTEUR // 2
        x_fleche = 100 + self.position_fleche
        
        # Corps de la flèche
        longueur_fleche = 20
        pygame.draw.line(self.ecran, NOIR, 
                        (x_fleche - longueur_fleche, y_vol), 
                        (x_fleche, y_vol), 4)
        
        # Pointe de la flèche
        pygame.draw.polygon(self.ecran, ROUGE, [
            (x_fleche, y_vol),
            (x_fleche - 8, y_vol - 4),
            (x_fleche - 8, y_vol + 4)
        ])
        
        # Plumes
        pygame.draw.polygon(self.ecran, VERT, [
            (x_fleche - longueur_fleche, y_vol),
            (x_fleche - longueur_fleche - 6, y_vol - 3),
            (x_fleche - longueur_fleche - 6, y_vol + 3)
        ])
        
        # Trail de mouvement
        if len(self.trail_fleche) > 1:
            points = [(100 + pos, y_vol) for pos in self.trail_fleche[-10:]]
            if len(points) > 1:
                pygame.draw.lines(self.ecran, CYAN, False, points, 2)
        
        # Vitesse instantanée (vecteur)
        if self.mode_analyse == "derivee":
            vitesse_scale = self.vitesse_fleche / 4
            pygame.draw.arrow(self.ecran, BLEU, 
                            (x_fleche, y_vol - 15), 
                            (x_fleche + vitesse_scale, y_vol - 15), 2)
            texte_v = self.font_petit.render(f"v = {self.vitesse_fleche:.1f} px/s", True, BLEU)
            self.ecran.blit(texte_v, (x_fleche - 30, y_vol - 35))
    
    def dessiner_analyse_instants(self):
        """Dessine l'analyse par instants discrets"""
        if self.mode_analyse != "instants":
            return
        
        y_start = 600
        
        # Titre
        titre = self.font_titre.render(f"Analyse par Instants (Δt = {self.delta_t_actuel}s)", True, VIOLET)
        self.ecran.blit(titre, (50, y_start))
        
        # Grille temporelle
        pygame.draw.rect(self.ecran, BLANC, (50, y_start + 40, 800, 200))
        pygame.draw.rect(self.ecran, NOIR, (50, y_start + 40, 800, 200), 2)
        
        # Instants discrets
        nb_instants = min(10, int(3.0 / self.delta_t_actuel))
        for i in range(nb_instants):
            temps_instant = i * self.delta_t_actuel
            x_instant = 50 + (temps_instant / 3.0) * 800
            
            # Ligne verticale pour l'instant
            pygame.draw.line(self.ecran, GRIS, 
                           (x_instant, y_start + 40), 
                           (x_instant, y_start + 240), 1)
            
            # Position de la flèche à cet instant
            pos_instant = self.vitesse_fleche * temps_instant
            y_position = y_start + 50 + (pos_instant / self.position_cible) * 180
            
            # Point de position
            couleur = ROUGE if abs(temps_instant - self.temps) < self.delta_t_actuel/2 else GRIS
            pygame.draw.circle(self.ecran, couleur, (int(x_instant), int(y_position)), 4)
            
            # Étiquette temps
            texte_t = self.font_petit.render(f"{temps_instant:.3f}s", True, couleur)
            self.ecran.blit(texte_t, (x_instant - 20, y_start + 245))
        
        # Légendes
        texte_pos = self.font_petit.render("Position", True, NOIR)
        self.ecran.blit(texte_pos, (10, y_start + 140))
        texte_temps = self.font_petit.render("Temps →", True, NOIR)
        self.ecran.blit(texte_temps, (450, y_start + 250))
        
        # Analyse de l'instant actuel
        instant_actuel = int(self.temps / self.delta_t_actuel)
        infos_instant = [
            f"Instant actuel: {instant_actuel}",
            f"Position exacte: {self.position_fleche:.2f} px",
            f"À cet instant: POSITION FIXE",
            f"Durée de l'instant: {self.delta_t_actuel}s",
            f"Argument de Zénon: Pas de mouvement dans l'instant"
        ]
        
        for i, info in enumerate(infos_instant):
            couleur = VIOLET if i == 4 else NOIR
            texte = self.font.render(info, True, couleur)
            self.ecran.blit(texte, (900, y_start + 50 + i * 25))
    
    def dessiner_analyse_derivee(self):
        """Dessine l'analyse par dérivées"""
        if self.mode_analyse != "derivee":
            return
        
        y_start = 600
        
        # Titre
        titre = self.font_titre.render("Analyse par Calcul Différentiel", True, BLEU)
        self.ecran.blit(titre, (50, y_start))
        
        # Fonction position
        infos_derivee = [
            "📍 Position: x(t) = v₀ × t",
            f"📍 x({self.temps:.3f}) = {self.vitesse_fleche} × {self.temps:.3f} = {self.position_fleche:.2f} px",
            "",
            "📈 Vitesse: v(t) = dx/dt = v₀",
            f"📈 v({self.temps:.3f}) = {self.vitesse_fleche:.1f} px/s (CONSTANTE)",
            "",
            "⚡ Accélération: a(t) = dv/dt = 0",
            "",
            "💡 RÉSOLUTION: À l'instant t, position FIXE mais vitesse ≠ 0 !",
            "💡 Le mouvement = variation de position, pas position elle-même"
        ]
        
        for i, info in enumerate(infos_derivee):
            if info:
                couleur = BLEU if "💡" in info else NOIR
                texte = self.font.render(info, True, couleur)
                self.ecran.blit(texte, (50, y_start + 40 + i * 25))
        
        # Graphique de la fonction position
        graph_x, graph_y = 700, y_start + 50
        graph_w, graph_h = 300, 150
        
        pygame.draw.rect(self.ecran, BLANC, (graph_x, graph_y, graph_w, graph_h))
        pygame.draw.rect(self.ecran, NOIR, (graph_x, graph_y, graph_w, graph_h), 2)
        
        # Courbe position(temps)
        points = []
        for i in range(graph_w):
            t = (i / graph_w) * 10  # 10 secondes max
            x = self.vitesse_fleche * t
            y_point = graph_y + graph_h - (x / 1200) * graph_h  # Normalisation
            points.append((graph_x + i, y_point))
        
        if len(points) > 1:
            pygame.draw.lines(self.ecran, BLEU, False, points, 2)
        
        # Point actuel
        t_actuel = min(self.temps, 10)
        x_point = graph_x + (t_actuel / 10) * graph_w
        y_point = graph_y + graph_h - (self.position_fleche / 1200) * graph_h
        pygame.draw.circle(self.ecran, ROUGE, (int(x_point), int(y_point)), 5)
        
        # Tangente (dérivée)
        if t_actuel > 0:
            slope = self.vitesse_fleche / 10 * graph_w / graph_h
            x1, x2 = max(graph_x, x_point - 50), min(graph_x + graph_w, x_point + 50)
            y1 = y_point - slope * (x_point - x1)
            y2 = y_point + slope * (x2 - x_point)
            pygame.draw.line(self.ecran, ROUGE, (x1, y1), (x2, y2), 2)
    
    def dessiner_analyse_quantique(self):
        """Dessine l'analyse quantique (superposition)"""
        if self.mode_analyse != "quantique":
            return
        
        y_vol = HAUTEUR // 2
        
        # Positions multiples de la flèche
        if self.incertitude_active:
            for i in range(5):
                pos_quantum = self.position_fleche + random.gauss(0, 20)  # Incertitude ±20px
                x_quantum = 100 + pos_quantum
                
                if 100 <= x_quantum <= 900:
                    # Flèche fantôme
                    alpha = 100
                    pygame.draw.line(self.ecran, (*CYAN, alpha), 
                                   (x_quantum - 15, y_vol), (x_quantum, y_vol), 2)
                    pygame.draw.circle(self.ecran, (*CYAN, alpha), 
                                     (int(x_quantum), y_vol), 3)
        
        # Titre et explications
        y_start = 600
        titre = self.font_titre.render("Analyse Quantique - Superposition", True, CYAN)
        self.ecran.blit(titre, (50, y_start))
        
        infos_quantum = [
            "🌌 Dans l'interprétation quantique:",
            "• La flèche existe simultanément en plusieurs positions",
            "• L'observation 'force' une position spécifique", 
            "• Le mouvement devient probabiliste",
            "• Résolution: Le paradoxe disparaît dans l'incertitude",
            "",
            f"Position moyenne: {self.position_fleche:.1f} px",
            f"Incertitude: ±20 px (principe d'Heisenberg)",
            "Appuyez sur U pour activer/désactiver l'incertitude"
        ]
        
        for i, info in enumerate(infos_quantum):
            if info:
                couleur = CYAN if "🌌" in info or "•" in info else NOIR
                texte = self.font.render(info, True, couleur)
                self.ecran.blit(texte, (50, y_start + 40 + i * 25))
    
    def dessiner_info_principale(self):
        """Dessine les informations principales"""
        # Titre
        titre = self.font_grand.render("🏹 Paradoxe de la Flèche en Vol", True, NOIR)
        self.ecran.blit(titre, (50, 10))
        
        # Informations de base
        y_info = 60
        infos_base = [
            f"⏱️  Temps: {self.temps:.3f}s",
            f"🏹 Position flèche: {self.position_fleche:.1f}px ({self.position_fleche/10:.1f}m)",
            f"🎯 Distance à la cible: {max(0, self.position_cible - self.position_fleche):.1f}px",
            f"⚡ Vitesse: {self.vitesse_fleche:.1f} px/s ({self.vitesse_fleche/10:.1f} m/s)",
            f"🎮 Mode d'analyse: {self.mode_analyse.title()}"
        ]
        
        if self.mode_analyse == "instants":
            infos_base.append(f"📊 Δt actuel: {self.delta_t_actuel}s")
        
        for i, info in enumerate(infos_base):
            texte = self.font.render(info, True, NOIR)
            self.ecran.blit(texte, (50, y_info + i * 25))
        
        # État du vol
        if self.position_fleche >= self.position_cible and not self.vol_termine:
            impact = self.font_titre.render("🎯 Impact ! La flèche a atteint la cible !", True, ROUGE)
            self.ecran.blit(impact, (50, y_info + len(infos_base) * 25 + 20))
            self.vol_termine = True
        
        # Paradoxe de Zénon
        y_paradoxe = 200
        paradoxe_titre = self.font_titre.render("🤔 Paradoxe de Zénon", True, VIOLET)
        self.ecran.blit(paradoxe_titre, (50, y_paradoxe))
        
        explication_zenon = [
            "À chaque instant, la flèche occupe une position précise.",
            "Si l'instant est infiniment court, aucun mouvement n'est possible.",
            "Donc à chaque instant, la flèche est au repos.",
            "Comment le mouvement peut-il exister ?",
            "",
            "🔬 Différentes résolutions selon le mode d'analyse..."
        ]
        
        for i, ligne in enumerate(explication_zenon):
            couleur = VIOLET if ligne.startswith("🔬") else NOIR
            texte = self.font.render(ligne, True, couleur)
            self.ecran.blit(texte, (50, y_paradoxe + 40 + i * 22))
        
        # Contrôles
        y_controles = HAUTEUR - 120
        controles_titre = self.font_titre.render("🎮 Contrôles", True, BLEU)
        self.ecran.blit(controles_titre, (50, y_controles - 30))
        
        controles = [
            "ESPACE: ▶️ Start/Pause    R: 🔄 Reset    M: 📊 Mode analyse",
            "↑/↓: ⚡ Vitesse simulation    +/-: 📏 Δt (mode instants)",
            "U: 🌌 Incertitude quantique    F: ❄️ Figer instant    Q: ❌ Quitter"
        ]
        
        for i, controle in enumerate(controles):
            texte = self.font_petit.render(controle, True, GRIS)
            self.ecran.blit(texte, (50, y_controles + i * 20))
    
    def mettre_a_jour_simulation(self):
        """Met à jour la simulation"""
        if not self.simulation_active or self.instant_fige:
            return
        
        dt = 1/60 * self.vitesse_simulation
        
        if self.position_fleche < self.position_cible:
            # Mise à jour position
            self.position_fleche += self.vitesse_fleche * dt
            self.temps += dt
            
            # Historique
            if len(self.historique_temps) == 0 or self.temps - self.historique_temps[-1] >= 0.05:
                self.historique_positions.append(self.position_fleche)
                self.historique_temps.append(self.temps)
                self.historique_vitesses.append(self.vitesse_fleche)
                self.trail_fleche.append(self.position_fleche)
                
                # Limiter la longueur du trail
                if len(self.trail_fleche) > 20:
                    self.trail_fleche.pop(0)
            
            # Effets visuels
            if random.random() < 0.3:  # 30% de chance
                self.ajouter_particule_fleche()
        
        # Mise à jour des particules
        self.mettre_a_jour_particules(dt)
        
        # Gestion du gel temporel
        if self.instant_fige:
            self.temps_gel += dt
            if self.temps_gel > 2.0:  # 2 secondes de gel
                self.instant_fige = False
                self.temps_gel = 0.0
    
    def gerer_evenements(self):
        """Gère les événements utilisateur"""
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_SPACE:
                    self.simulation_active = not self.simulation_active
                
                elif evenement.key == pygame.K_r:
                    self.reset_simulation()
                    self.simulation_active = False
                
                elif evenement.key == pygame.K_m:
                    modes = ["continu", "instants", "derivee", "quantique"]
                    current_index = modes.index(self.mode_analyse)
                    self.mode_analyse = modes[(current_index + 1) % len(modes)]
                
                elif evenement.key == pygame.K_UP:
                    self.vitesse_simulation = min(3.0, self.vitesse_simulation + 0.2)
                
                elif evenement.key == pygame.K_DOWN:
                    self.vitesse_simulation = max(0.1, self.vitesse_simulation - 0.2)
                
                elif evenement.key == pygame.K_PLUS or evenement.key == pygame.K_EQUALS:
                    if self.index_delta > 0:
                        self.index_delta -= 1
                        self.delta_t_actuel = self.deltas_disponibles[self.index_delta]
                
                elif evenement.key == pygame.K_MINUS:
                    if self.index_delta < len(self.deltas_disponibles) - 1:
                        self.index_delta += 1
                        self.delta_t_actuel = self.deltas_disponibles[self.index_delta]
                
                elif evenement.key == pygame.K_u:
                    self.incertitude_active = not self.incertitude_active
                
                elif evenement.key == pygame.K_f:
                    self.instant_fige = not self.instant_fige
                    if self.instant_fige:
                        self.temps_gel = 0.0
                
                elif evenement.key == pygame.K_q:
                    return False
        
        return True
    
    def executer(self):
        """Boucle principale"""
        en_cours = True
        
        while en_cours:
            en_cours = self.gerer_evenements()
            
            # Mise à jour
            self.mettre_a_jour_simulation()
            
            # Rendu
            self.ecran.fill(BLANC)
            
            # Dessiner tous les éléments
            self.dessiner_scene()
            self.dessiner_particules()
            self.dessiner_fleche()
            self.dessiner_info_principale()
            
            # Analyses spécifiques selon le mode
            if self.mode_analyse == "instants":
                self.dessiner_analyse_instants()
            elif self.mode_analyse == "derivee":
                self.dessiner_analyse_derivee()
            elif self.mode_analyse == "quantique":
                self.dessiner_analyse_quantique()
            
            # Effet de gel temporel
            if self.instant_fige:
                overlay = pygame.Surface((LARGEUR, HAUTEUR))
                overlay.set_alpha(100)
                overlay.fill(BLEU)
                self.ecran.blit(overlay, (0, 0))
                
                texte_gel = self.font_titre.render("❄️ INSTANT FIGÉ", True, BLANC)
                self.ecran.blit(texte_gel, (LARGEUR//2 - 100, HAUTEUR//2))
            
            pygame.display.flip()
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulation = FlecheVolSimulation()
    simulation.executer()