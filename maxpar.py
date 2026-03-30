import threading

def interfere(t1, t2):

    r1 = set(t1.reads)
    w1 = set(t1.writes)

    r2 = set(t2.reads)
    w2 = set(t2.writes)

    cond_1 = bool(r1 & w2)
    cond_2 = bool(r2 & w1)
    cond_3 = bool(w1 & w2)

    return cond_1 or cond_2 or cond_3

def _get_tous_les_ancetres(self, nomTache):
    tous_les_ancetres = set()

    def fouiller_parents(tache_courante):
        parents_direct = self.precedence.get(tache_courante, [])

        for parent in parents_direct:
            if parent not in tous_les_ancetres:
                tous_les_ancetres.add(parent)
                fouiller_parents(parent)

    fouiller_parents(nomTache)

    return list(tous_les_ancetres)

def getDependencies(self, nomTache):
    if nomTache not in self.tasks:
        raise ValueError(f"Erreur : la tâche '{nomTache}' n'existe pas dans le système.")

    dependances_maximales = []
    tache_cible = self.tasks[nomTache]

    ancetres = self._get_tous_les_ancetres(nomTache)

    for nom_ancetre in ancetres:
        tache_ancetre = self.tasks[nom_ancetre]
        if interfere(tache_ancetre, tache_cible):
            dependances_maximales.append(nom_ancetre)

    return dependances_maximales

def run(self):
        taches_restantes = set(self.tasks.keys())

        taches_terminees = set()

        while taches_restantes:
            taches_pretes = []

            for nom_tache in taches_restantes:
                dependances = self.getDependencies(nomTache=nom_tache)
                if all(dep in taches_terminees for dep in dependances):
                    taches_pretes.append(nom_tache)

            if not taches_pretes:
                raise RuntimeError("Erreur : Interblocage (cycle) détecté. Exécution impossible.")

            threads = []
            for nom_tache in taches_pretes:
                tache_obj = self.tasks[nom_tache]
                t = threading.Thread(target=tache_obj.run)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            for nom_tache in taches_pretes:
                taches_terminees.add(nom_tache)
                taches_restantes.remove(nom_tache)
from collections import deque


class Task:
    def __init__(self):
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None


class TaskSystem:
    def __init__(self, tasks, precedence):
        self._validate(tasks, precedence)
        self.tasks = tasks
        self.precedence = precedence

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

    def runSeq(self):
        task_map = {t.name: t for t in self.tasks}
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
                    queue.append(task_map[dependent_name])
