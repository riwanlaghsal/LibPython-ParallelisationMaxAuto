from collections import deque
import threading
import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ─────────────────────────────────────────
# Partie Riwan — fonction globale
# ─────────────────────────────────────────

def interfere(t1, t2):
    """Retourne True si deux tâches interfèrent (conflit lecture/écriture)."""
    r1 = set(t1.reads)
    w1 = set(t1.writes)
    r2 = set(t2.reads)
    w2 = set(t2.writes)  # bug corrigé : était t2.reads

    cond_1 = bool(r1 & w2)
    cond_2 = bool(r2 & w1)
    cond_3 = bool(w1 & w2)

    return cond_1 or cond_2 or cond_3


# ─────────────────────────────────────────
# Classe Task
# ─────────────────────────────────────────

class Task:
    def __init__(self):
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None


# ─────────────────────────────────────────
# Classe TaskSystem
# ─────────────────────────────────────────

class TaskSystem:

    # ── Partie Ilyes — init + validation ──────────────────────────────────────

    def __init__(self, tasks, precedence):
        self._validate(tasks, precedence)
        self.tasks = tasks
        self.precedence = precedence
        self._task_map = {t.name: t for t in tasks}  # accès rapide par nom

    def _validate(self, tasks, precedence):
        seen = set()
        for t in tasks:
            if t.name in seen:
                raise ValueError(f"Erreur : tâche en double : {t.name}")
            seen.add(t.name)

        for name in precedence:
            if name not in seen:
                raise ValueError(f"Erreur : tâche inconnue dans le dictionnaire : {name}")

        for deps in precedence.values():
            for dep in deps:
                if dep not in seen:
                    raise ValueError(f"Erreur : dépendance inconnue : {dep}")

        visiting = set()
        visited = set()

        def dfs(node):
            visiting.add(node)
            for dep in precedence.get(node, []):
                if dep in visiting:
                    raise ValueError(f"Erreur : cycle détecté impliquant : {dep}")
                if dep not in visited:
                    dfs(dep)
            visiting.remove(node)
            visited.add(node)

        for name in seen:
            if name not in visited:
                dfs(name)

    # ── Partie Ilyes — exécution séquentielle ─────────────────────────────────

    def runSeq(self):
        """Exécute les tâches dans l'ordre topologique (séquentiel)."""
        in_degree = {t.name: 0 for t in self.tasks}
        dependents = {t.name: [] for t in self.tasks}

        for name, deps in self.precedence.items():
            in_degree[name] = len(deps)
            for dep in deps:
                dependents[dep].append(name)

        queue = deque([t for t in self.tasks if in_degree[t.name] == 0])

        while queue:
            task = queue.popleft()
            task.run()
            for dependent_name in dependents[task.name]:
                in_degree[dependent_name] -= 1
                if in_degree[dependent_name] == 0:
                    queue.append(self._task_map[dependent_name])

    # ── Partie Riwan — dépendances maximales ──────────────────────────────────

    def _get_tous_les_ancetres(self, nomTache):
        """Retourne tous les ancêtres (directs et indirects) d'une tâche."""
        tous_les_ancetres = set()

        def fouiller_parents(tache_courante):
            for parent in self.precedence.get(tache_courante, []):
                if parent not in tous_les_ancetres:
                    tous_les_ancetres.add(parent)
                    fouiller_parents(parent)

        fouiller_parents(nomTache)
        return list(tous_les_ancetres)

    def getDependencies(self, nomTache):
        """Retourne les ancêtres qui interfèrent réellement avec la tâche."""
        if nomTache not in self._task_map:
            raise ValueError(f"Erreur : la tâche '{nomTache}' n'existe pas dans le système.")

        tache_cible = self._task_map[nomTache]
        ancetres = self._get_tous_les_ancetres(nomTache)

        return [
            nom for nom in ancetres
            if interfere(self._task_map[nom], tache_cible)
        ]

    # ── Partie Riwan — exécution parallèle ───────────────────────────────────

    def run(self):
        """Exécute les tâches en parallèle en respectant les dépendances réelles (getDependencies)."""
        taches_restantes = set(self._task_map.keys())
        taches_terminees = set()

        while taches_restantes:
            taches_pretes = []

            for nom_tache in taches_restantes:
                dependances = self.getDependencies(nomTache=nom_tache)
                if all(dep in taches_terminees for dep in dependances):
                    taches_pretes.append(nom_tache)

            if not taches_pretes:
                raise RuntimeError("Erreur : Interblocage détecté. Exécution impossible.")

            threads = []
            for nom_tache in taches_pretes:
                tache_obj = self._task_map[nom_tache]
                t = threading.Thread(target=tache_obj.run)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            for nom_tache in taches_pretes:
                taches_terminees.add(nom_tache)
                taches_restantes.remove(nom_tache)

    # ── Partie Yassine — affichage graphe ─────────────────────────────────────

    def draw(self):
        """Affiche graphiquement le graphe du systeme de parallelisme maximal."""

        # Calcul des dependances reelles pour chaque tache
        deps_map = {t: self.getDependencies(t) for t in self._task_map}

        # Calcul des niveaux (couches) par BFS
        niveaux = {}
        queue = deque()
        for t in self._task_map:
            if not deps_map[t]:
                niveaux[t] = 0
                queue.append(t)

        while queue:
            tache = queue.popleft()
            for autre in self._task_map:
                if tache in deps_map[autre]:
                    nouveau_niveau = niveaux[tache] + 1
                    if autre not in niveaux or niveaux[autre] < nouveau_niveau:
                        niveaux[autre] = nouveau_niveau
                        queue.append(autre)

        # Calcul des positions (x, y) de chaque noeud
        par_niveau = {}
        for t, niv in niveaux.items():
            par_niveau.setdefault(niv, []).append(t)

        positions = {}
        for niv, taches in par_niveau.items():
            for i, t in enumerate(taches):
                x = i - (len(taches) - 1) / 2
                y = -niv
                positions[t] = (x, y)

        # Dessin
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title("Graphe de parallelisme maximal", fontsize=14, fontweight='bold')
        ax.axis('off')

        rayon = 0.2

        # Fleches
        for tache, deps in deps_map.items():
            for dep in deps:
                x1, y1 = positions[dep]
                x2, y2 = positions[tache]
                ax.annotate(
                    "", xy=(x2, y2 + rayon), xytext=(x1, y1 - rayon),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5)
                )

        # Noeuds
        for tache, (x, y) in positions.items():
            cercle = plt.Circle((x, y), rayon, color='lightblue', ec='black', lw=1.5, zorder=3)
            ax.add_patch(cercle)
            ax.text(x, y, tache, ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)

        ax.autoscale()
        plt.tight_layout()
        plt.show()

    # ── Partie Yassine — test de déterminisme ─────────────────────────────────

    def detTestRnd(self, dic_globals):
        """Vérifie si le résultat est identique entre exécution séquentielle et parallèle."""
        print("=== TEST DE DÉTERMINISME ALÉATOIRE ===")
        all_reads = set()
        for t in self.tasks:
            all_reads.update(t.reads)

        test_values = {var: random.randint(1, 100) for var in all_reads}

        for var, val in test_values.items():
            dic_globals[var] = val
        self.runSeq()
        res_seq = {t.name: {v: dic_globals.get(v) for v in t.writes} for t in self.tasks}

        for var, val in test_values.items():
            dic_globals[var] = val
        self.run()
        res_par = {t.name: {v: dic_globals.get(v) for v in t.writes} for t in self.tasks}

        if res_seq == res_par:
            print("SUCCES : Les résultats sont identiques.")
        else:
            print("ECHEC : Différence détectée entre séquentiel et parallèle !")

    # ── Partie Yassine — benchmark ────────────────────────────────────────────

    def parCost(self):
        """Compare le temps d'exécution moyen entre séquentiel et parallèle."""
        print("=== ANALYSE DES PERFORMANCES (Coût) ===")
        nb_essais = 5

        start_seq = time.time()
        for _ in range(nb_essais):
            self.runSeq()
        avg_seq = (time.time() - start_seq) / nb_essais

        start_par = time.time()
        for _ in range(nb_essais):
            self.run()
        avg_par = (time.time() - start_par) / nb_essais

        print(f"Moyenne Séquentielle : {avg_seq:.5f}s")
        print(f"Moyenne Parallèle   : {avg_par:.5f}s")

        if avg_par < avg_seq:
            gain = ((avg_seq - avg_par) / avg_seq) * 100
            print(f"Gain de performance : {gain:.1f}%")
        else:
            print("Le mode parallèle n'est pas plus rapide sur ce petit exemple.")
