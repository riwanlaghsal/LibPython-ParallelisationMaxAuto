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
