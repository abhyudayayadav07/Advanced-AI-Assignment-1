from itertools import product
from collections import defaultdict


N = 3          
K = 5          
m = 5          

assignments = {
    1: {"cost": 2, "deps": []},
    2: {"cost": 4, "deps": [1]},
    3: {"cost": 2, "deps": [4]},
    4: {"cost": 3, "deps": [7, 2]},
    5: {"cost": 5, "deps": [2]},
    6: {"cost": 5, "deps": [5, 1]},
    7: {"cost": 4, "deps": []},
    8: {"cost": 1, "deps": [6, 4]},
}

assignment_ids = list(assignments.keys())



def dependencies_satisfied(a, day, assignment_day):
    for dep in assignments[a]["deps"]:
        if assignment_day[dep] >= day:
            return False
    return True



def generate_all_schedules():
    valid_schedules = []

    
    for day_assignment in product(range(1, m + 1), repeat=len(assignment_ids)):
        assignment_day = dict(zip(assignment_ids, day_assignment))

        
        if not all(
            dependencies_satisfied(a, assignment_day[a], assignment_day)
            for a in assignment_ids
        ):
            continue

        
        for student_assignment in product(range(1, N + 1), repeat=len(assignment_ids)):
            usage = defaultdict(lambda: defaultdict(int))

            for idx, a in enumerate(assignment_ids):
                d = assignment_day[a]
                s = student_assignment[idx]
                usage[d][s] += assignments[a]["cost"]

            
            if all(usage[d][s] <= K for d in usage for s in usage[d]):
                schedule = {
                    a: (assignment_day[a], student_assignment[idx])
                    for idx, a in enumerate(assignment_ids)
                }
                valid_schedules.append(schedule)

    return valid_schedules



if __name__ == "__main__":
    schedules = generate_all_schedules()

    print(f"Total valid schedules: {len(schedules)}\n")

    for i, sched in enumerate(schedules, 1):
        print(f"Schedule {i}:")
        for a in sorted(sched):
            day, student = sched[a]
            print(f"  Assignment {a}: Day {day}, Student {student}")
        print()

