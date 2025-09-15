#!/usr/bin/env python3
"""
Version graphique avec Pygame du paradoxe de la Dichotomie
Simulation interactive de la pierre qui doit atteindre l'arbre
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
MARRON = (139, 69, 19)
VERT_FONCE = (0, 100, 0)

class DichotomieSimulation:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("🌳 Paradoxe de la Dichotomie - Zénon d'Élée")
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
        self.mode_affichage = "normal"  # "normal", "zenon", "mathematique", "energie"
        self.afficher_etapes = True
        self.afficher_serie = True
        self.animation_automatique = True
        
        # Effets visuels
        self.particules_pierre = []
        self.trail_pierre = []
        self.etapes_zenon = []
        
    def reset_simulation(self):
        """Remet à zéro la simulation"""
        self.position_zeno = 100.0  # Position de Zénon
        self.position_pierre = 100.0  # Position de la pierre (commence avec Zénon)
        self.position_arbre = 900.0   # Position de l'arbre (800 pixels = 8 mètres)
        self.distance_totale = self.position_arbre - self.position_zeno
        
        self.etape_actuelle = 0
        self.distance_a_parcourir = 0.0
        self.temps = 0.0
        self.historique_positions = []
        self.historique_distances = []
        self.historique_temps = []
        self.lancement_termine = False
        
        # Animation
        self.particules_pierre = []
        self.trail_pierre = []
        self.etapes_zenon = []
        self.temps_etape = 0.0
        self.duree_etape = 2.0  # 2 secondes par étape
        
        # Calculs mathématiques
        self.serie_termes = []
        self.somme_partielle = 0.0
        
    def ajouter_particule_pierre(self, x, y):
        """Ajoute des particules d'effet pour la pierre"""
        for i in range(8):
            particule = {
                'x': x + random.uniform(-8, 8),
                'y': y + random.uniform(-8, 8),
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(-30, 30),
                'vie': 1.0,
                'taille': random.uniform(2, 5),
                'couleur': random.choice([GRIS, GRIS_CLAIR, NOIR])
            }
            self.particules_pierre.append(particule)
    
    def mettre_a_jour_particules(self, dt):
        """Met à jour les particules d'effet"""
        for particule in self.particules_pierre[:]:
            particule['x'] += particule['vx'] * dt
            particule['y'] += particule['vy'] * dt
            particule['vy'] += 100 * dt  # Gravité
            particule['vie'] -= dt * 1.5
            particule['taille'] *= 0.98
            if particule['vie'] <= 0:
                self.particules_pierre.remove(particule)
    
    def dessiner_particules(self):
        """Dessine les particules d'effet"""
        for particule in self.particules_pierre:
            alpha = int(particule['vie'] * 255)
            couleur = particule['couleur']
            rayon = max(1, int(particule['taille']))
            pygame.draw.circle(self.ecran, couleur, 
                             (int(particule['x']), int(particule['y'])), rayon)
    
    def dessiner_scene(self):
        """Dessine la scène avec Zénon, l'arbre et l'environnement"""
        y_sol = HAUTEUR // 2 + 100
        
        # Sol/herbe
        pygame.draw.rect(self.ecran, VERT, (0, y_sol, LARGEUR, HAUTEUR - y_sol))
        
        # Ligne de lancement
        pygame.draw.line(self.ecran, GRIS_CLAIR, 
                        (self.position_zeno, y_sol), 
                        (self.position_arbre, y_sol), 2)
        
        # Zénon (philosophe avec toge)
        x_zeno = self.position_zeno
        # Corps (rectangle beige/blanc)
        pygame.draw.rect(self.ecran, BLANC, (x_zeno - 15, y_sol - 50, 30, 50))
        # Tête
        pygame.draw.circle(self.ecran, (255, 220, 177), (int(x_zeno), y_sol - 65), 12)
        # Bras tenant la pierre (si pas encore lancée)
        if self.etape_actuelle == 0:
            pygame.draw.line(self.ecran, (255, 220, 177), 
                           (x_zeno + 10, y_sol - 40), (x_zeno + 25, y_sol - 30), 3)
        
        # Texte "Zénon"
        texte_zeno = self.font.render("Zénon d'Élée", True, NOIR)
        self.ecran.blit(texte_zeno, (x_zeno - 40, y_sol - 90))
        
        # Arbre (tronc + feuillage)
        x_arbre = self.position_arbre
        # Tronc
        pygame.draw.rect(self.ecran, MARRON, (x_arbre - 15, y_sol - 80, 30, 80))
        # Feuillage (plusieurs cercles verts)
        for i, (offset_x, offset_y, rayon) in enumerate([
            (-10, -70, 25), (10, -75, 20), (0, -90, 30)
        ]):
            pygame.draw.circle(self.ecran, VERT_FONCE, 
                             (int(x_arbre + offset_x), y_sol + offset_y), rayon)
        
        # Texte "Arbre"
        texte_arbre = self.font.render("Arbre", True, VERT_FONCE)
        self.ecran.blit(texte_arbre, (x_arbre - 20, y_sol - 120))
        
        # Marqueurs de distance
        distance_totale_m = self.distance_totale / 100  # Conversion pixels -> mètres
        for i in range(int(distance_totale_m) + 1):
            x_marqueur = self.position_zeno + (i * 100)  # Tous les mètres
            if x_marqueur <= self.position_arbre:
                pygame.draw.line(self.ecran, GRIS, 
                               (x_marqueur, y_sol - 5), (x_marqueur, y_sol + 5), 1)
                texte_dist = self.font_petit.render(f"{i}m", True, GRIS)
                self.ecran.blit(texte_dist, (x_marqueur - 8, y_sol + 10))
    
    def dessiner_pierre(self):
        """Dessine la pierre avec trail de mouvement"""
        if self.lancement_termine:
            return
        
        y_sol = HAUTEUR // 2 + 100
        x_pierre = self.position_pierre
        y_pierre = y_sol - 20  # Hauteur de lancement
        
        # Trail de la pierre
        if len(self.trail_pierre) > 1:
            points = [(pos, y_pierre) for pos in self.trail_pierre[-15:]]
            if len(points) > 1:
                for i in range(len(points) - 1):
                    alpha = int((i / len(points)) * 255)
                    pygame.draw.line(self.ecran, ORANGE, points[i], points[i + 1], 3)
        
        # Pierre (cercle gris)
        pygame.draw.circle(self.ecran, GRIS, (int(x_pierre), int(y_pierre)), 6)
        pygame.draw.circle(self.ecran, NOIR, (int(x_pierre), int(y_pierre)), 6, 2)
        
        # Ombre de la pierre
        pygame.draw.ellipse(self.ecran, (0, 0, 0, 100), 
                          (x_pierre - 8, y_sol - 5, 16, 8))
        
        # Vitesse et direction (flèche)
        if self.animation_automatique and self.simulation_active:
            fleche_fin_x = x_pierre + 30
            pygame.draw.line(self.ecran, ROUGE, 
                           (x_pierre + 8, y_pierre), (fleche_fin_x, y_pierre), 3)
            pygame.draw.polygon(self.ecran, ROUGE, [
                (fleche_fin_x, y_pierre),
                (fleche_fin_x - 8, y_pierre - 4),
                (fleche_fin_x - 8, y_pierre + 4)
            ])
    
    def dessiner_etapes_zenon(self):
        """Dessine la visualisation des étapes de Zénon"""
        if not self.afficher_etapes:
            return
        
        y_start = 600
        
        # Zone des étapes
        pygame.draw.rect(self.ecran, BLANC, (50, y_start, LARGEUR - 100, 250))
        pygame.draw.rect(self.ecran, NOIR, (50, y_start, LARGEUR - 100, 250), 2)
        
        # Titre
        titre = self.font_titre.render("Étapes de la Dichotomie de Zénon", True, VIOLET)
        self.ecran.blit(titre, (60, y_start + 10))
        
        # Ligne représentant la distance totale
        ligne_y = y_start + 60
        ligne_start = 100
        ligne_longueur = 1000
        
        pygame.draw.line(self.ecran, NOIR, 
                        (ligne_start, ligne_y), 
                        (ligne_start + ligne_longueur, ligne_y), 3)
        
        # Position de Zénon et de l'arbre
        pygame.draw.circle(self.ecran, BLEU, (ligne_start, ligne_y), 8)
        pygame.draw.circle(self.ecran, VERT_FONCE, (ligne_start + ligne_longueur, ligne_y), 8)
        
        # Étiquettes
        texte_zeno = self.font_petit.render("Zénon", True, BLEU)
        self.ecran.blit(texte_zeno, (ligne_start - 20, ligne_y - 25))
        texte_arbre = self.font_petit.render("Arbre", True, VERT_FONCE)
        self.ecran.blit(texte_arbre, (ligne_start + ligne_longueur - 20, ligne_y - 25))
        
        # Visualisation des étapes
        position_actuelle = 0
        couleurs = [ROUGE, ORANGE, JAUNE, VERT, BLEU, VIOLET]
        
        for i in range(min(6, self.etape_actuelle + 1)):
            # Distance de cette étape
            distance_etape = ligne_longueur / (2 ** (i + 1))
            
            # Position de fin de cette étape
            fin_etape = position_actuelle + distance_etape
            
            # Dessiner la section
            couleur = couleurs[i % len(couleurs)]
            pygame.draw.line(self.ecran, couleur,
                           (ligne_start + position_actuelle, ligne_y - 10),
                           (ligne_start + fin_etape, ligne_y - 10), 8)
            
            # Étiquette de l'étape
            texte_etape = self.font_petit.render(f"Étape {i+1}", True, couleur)
            texte_dist = self.font_petit.render(f"{8/(2**(i+1)):.3f}m", True, couleur)
            self.ecran.blit(texte_etape, (ligne_start + position_actuelle + 5, ligne_y + 15))
            self.ecran.blit(texte_dist, (ligne_start + position_actuelle + 5, ligne_y + 35))
            
            position_actuelle = fin_etape
        
        # Position actuelle de la pierre
        if self.etape_actuelle > 0:
            pos_pierre_relative = (self.position_pierre - self.position_zeno) / self.distance_totale
            x_pierre_ligne = ligne_start + pos_pierre_relative * ligne_longueur
            pygame.draw.circle(self.ecran, ROUGE, (int(x_pierre_ligne), ligne_y), 6)
    
    def dessiner_serie_mathematique(self):
        """Dessine l'analyse de la série mathématique"""
        if not self.afficher_serie:
            return
        
        y_start = 100
        x_start = 900
        
        # Cadre pour la série
        pygame.draw.rect(self.ecran, BLANC, (x_start, y_start, 450, 400))
        pygame.draw.rect(self.ecran, NOIR, (x_start, y_start, 450, 400), 2)
        
        # Titre
        titre = self.font_titre.render("Série Géométrique", True, BLEU)
        self.ecran.blit(titre, (x_start + 10, y_start + 10))
        
        # Formule générale
        formule = self.font.render("S = 4 + 2 + 1 + 0.5 + 0.25 + ...", True, NOIR)
        self.ecran.blit(formule, (x_start + 10, y_start + 50))
        
        formule2 = self.font.render("S = 4/(1-0.5) = 8 mètres", True, BLEU)
        self.ecran.blit(formule2, (x_start + 10, y_start + 75))
        
        # Tableau des termes
        y_tableau = y_start + 110
        headers = ["Étape", "Distance", "Somme", "Reste"]
        col_width = 100
        
        # En-têtes
        for i, header in enumerate(headers):
            texte = self.font_petit.render(header, True, NOIR)
            self.ecran.blit(texte, (x_start + 10 + i * col_width, y_tableau))
        
        # Ligne de séparation
        pygame.draw.line(self.ecran, NOIR, 
                        (x_start + 10, y_tableau + 20), 
                        (x_start + 430, y_tableau + 20), 1)
        
        # Données des étapes
        distance_initiale = 4.0  # Première moitié = 4m
        somme = 0.0
        
        for i in range(min(8, self.etape_actuelle + 2)):
            y_ligne = y_tableau + 30 + i * 20
            
            terme = distance_initiale / (2 ** i)
            somme += terme
            reste = 8.0 - somme
            
            # Couleur selon l'étape actuelle
            couleur = ROUGE if i == self.etape_actuelle else NOIR
            
            # Données de la ligne
            donnees = [
                f"{i+1}",
                f"{terme:.3f}m",
                f"{somme:.3f}m", 
                f"{reste:.3f}m"
            ]
            
            for j, donnee in enumerate(donnees):
                texte = self.font_petit.render(donnee, True, couleur)
                self.ecran.blit(texte, (x_start + 15 + j * col_width, y_ligne))
        
        # Convergence
        if self.etape_actuelle > 3:
            convergence = self.font.render("→ Converge vers 8m", True, VERT)
            self.ecran.blit(convergence, (x_start + 10, y_start + 350))
            
            conclusion = self.font.render("La pierre atteint l'arbre !", True, VERT)
            self.ecran.blit(conclusion, (x_start + 10, y_start + 370))
    
    def dessiner_info_principale(self):
        """Dessine les informations principales"""
        # Titre
        titre = self.font_grand.render("🌳 Paradoxe de la Dichotomie", True, NOIR)
        self.ecran.blit(titre, (50, 10))
        
        # Informations de base
        y_info = 60
        distance_restante = self.position_arbre - self.position_pierre
        distance_parcourue = self.position_pierre - self.position_zeno
        
        infos_base = [
            f"📍 Position pierre: {distance_parcourue:.1f}px ({distance_parcourue/100:.3f}m)",
            f"🎯 Distance à l'arbre: {distance_restante:.1f}px ({distance_restante/100:.3f}m)",
            f"📊 Étape actuelle: {self.etape_actuelle}",
            f"⏱️  Temps: {self.temps:.1f}s",
            f"🎮 Mode: {self.mode_affichage.title()}"
        ]
        
        for i, info in enumerate(infos_base):
            texte = self.font.render(info, True, NOIR)
            self.ecran.blit(texte, (50, y_info + i * 25))
        
        # Paradoxe de Zénon
        y_paradoxe = 200
        paradoxe_titre = self.font_titre.render("🤔 Le Paradoxe", True, VIOLET)
        self.ecran.blit(paradoxe_titre, (50, y_paradoxe))
        
        explication = [
            "Pour atteindre l'arbre, la pierre doit d'abord",
            "parcourir la moitié de la distance (4m).",
            "Puis la moitié du reste (2m), puis encore",
            "la moitié (1m), et ainsi de suite...",
            "",
            "Zénon conclut : Une infinité d'étapes →",
            "la pierre ne peut jamais atteindre l'arbre !",
            "",
            "🔬 Mais la série 4+2+1+0.5+... = 8m"
        ]
        
        for i, ligne in enumerate(explication):
            couleur = VERT if ligne.startswith("🔬") else NOIR
            texte = self.font.render(ligne, True, couleur)
            self.ecran.blit(texte, (50, y_paradoxe + 40 + i * 22))
        
        # État du lancement
        if distance_restante < 5:  # Très proche
            impact = self.font_titre.render("🎯 La pierre a atteint l'arbre !", True, VERT)
            self.ecran.blit(impact, (50, y_paradoxe + 280))
            if not self.lancement_termine:
                self.lancement_termine = True
                # Explosion de particules
                for _ in range(20):
                    self.ajouter_particule_pierre(self.position_arbre, HAUTEUR//2 + 80)
        
        # Contrôles
        y_controles = 50
        x_controles = 900
        
        controles_titre = self.font_titre.render("🎮 Contrôles", True, BLEU)
        self.ecran.blit(controles_titre, (x_controles, y_controles - 30))
        
        controles = [
            "ESPACE: ▶️ Start/Pause",
            "R: 🔄 Reset",
            "M: 📊 Mode affichage", 
            "E: 📈 Étapes on/off",
            "S: 🧮 Série on/off",
            "A: 🤖 Animation auto",
            "↑/↓: ⚡ Vitesse",
            "Q: ❌ Quitter"
        ]
        
        for i, controle in enumerate(controles):
            texte = self.font_petit.render(controle, True, GRIS)
            self.ecran.blit(texte, (x_controles, y_controles + i * 18))
    
    def mettre_a_jour_simulation(self):
        """Met à jour la simulation"""
        if not self.simulation_active:
            return
        
        dt = 1/60 * self.vitesse_simulation
        self.temps += dt
        
        if not self.lancement_termine and self.animation_automatique:
            self.temps_etape += dt
            
            # Nouvelle étape toutes les 2 secondes
            if self.temps_etape >= self.duree_etape:
                self.etape_suivante()
                self.temps_etape = 0.0
        
        # Mise à jour des particules
        self.mettre_a_jour_particules(dt)
        
        # Historique
        if len(self.historique_temps) == 0 or self.temps - self.historique_temps[-1] >= 0.1:
            self.historique_positions.append(self.position_pierre)
            self.historique_distances.append(self.position_arbre - self.position_pierre)
            self.historique_temps.append(self.temps)
    
    def etape_suivante(self):
        """Passe à l'étape suivante de la dichotomie"""
        if self.lancement_termine:
            return
        
        distance_restante = self.position_arbre - self.position_pierre
        
        if distance_restante > 1:  # Seuil minimal
            # Parcourir la moitié de la distance restante
            moitie_distance = distance_restante / 2
            self.position_pierre += moitie_distance
            
            # Ajouter au trail
            self.trail_pierre.append(self.position_pierre)
            if len(self.trail_pierre) > 20:
                self.trail_pierre.pop(0)
            
            # Particules d'effet
            self.ajouter_particule_pierre(self.position_pierre, HAUTEUR//2 + 80)
            
            self.etape_actuelle += 1
        else:
            self.lancement_termine = True
    
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
                    modes = ["normal", "zenon", "mathematique", "energie"]
                    try:
                        current_index = modes.index(self.mode_affichage)
                        self.mode_affichage = modes[(current_index + 1) % len(modes)]
                    except ValueError:
                        self.mode_affichage = "normal"
                
                elif evenement.key == pygame.K_e:
                    self.afficher_etapes = not self.afficher_etapes
                
                elif evenement.key == pygame.K_s:
                    self.afficher_serie = not self.afficher_serie
                
                elif evenement.key == pygame.K_a:
                    self.animation_automatique = not self.animation_automatique
                
                elif evenement.key == pygame.K_UP:
                    self.vitesse_simulation = min(3.0, self.vitesse_simulation + 0.2)
                
                elif evenement.key == pygame.K_DOWN:
                    self.vitesse_simulation = max(0.1, self.vitesse_simulation - 0.2)
                
                elif evenement.key == pygame.K_RETURN:
                    # Étape manuelle
                    if not self.animation_automatique:
                        self.etape_suivante()
                
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
            self.ecran.fill((135, 206, 235))  # Bleu ciel
            
            # Dessiner tous les éléments
            self.dessiner_scene()
            self.dessiner_pierre()
            self.dessiner_particules()
            self.dessiner_info_principale()
            
            if self.afficher_etapes:
                self.dessiner_etapes_zenon()
            
            if self.afficher_serie:
                self.dessiner_serie_mathematique()
            
            pygame.display.flip()
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulation = DichotomieSimulation()
    simulation.executer()