Assignment Scheduling Program – Beginner-Friendly README

This README explains what the program does, how it works step by step, and what each important part of the code means assuming you are a beginner-level Python programmer.



1. What problem does this program solve?

Imagine:

You have multiple assignments to complete
Some assignments depend on others (you must finish some first)
You are working in a group of students
Each student can ask an AI tool only a limited number of prompts per day

The program answers this question:

> Is it possible to complete all assignments within `m` days, and how many different valid schedules exist?

A schedule decides:

Which day an assignment is done
Which student does that assignment



2. Meaning of the input parameters

(a) Number of students

N = 3


There are 3 students in the group
Students are numbered as: `0, 1, 2`



(b) Prompt limit per student per day

K = 5


Each student can use at most 5 prompts per day
Prompts **cannot be shared** between students



(c) Assignment information


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


Each assignment has:

cost → number of prompts required
deps → list of assignments that must be completed *before* this one

Example:


6: {"cost": 5, "deps": [5, 1]}

Means:

Assignment 6 needs 5 prompts
Assignment 1 and 5 must be completed first



3. Important Python imports


from itertools import product
from collections import defaultdict


`itertools.product`

Generates all possible combinations
Used to try every possible way of assigning:

  Days to assignments
  Students to assignments

`defaultdict`

A dictionary that **automatically starts with 0**
Useful for counting prompt usage


4. Assignment list

python
assignment_ids = list(assignments.keys())


Extracts assignment numbers
Example: `[1, 2, 3, 4, 5, 6, 7, 8]`



5. Dependency checking function


def dependencies_satisfied(a, day, assignment_day):


This function checks:

Are all prerequisite assignments completed before this day?

Inside the function


for dep in assignments[a]["deps"]:


Go through every dependency of assignment `a`


if assignment_day[dep] >= day:
    return False


If a dependency is done on the same day or later, it is invalid

python
return True


All dependencies were completed earlier



6. Main logic: counting schedules


def count_schedules(m):


`m` = total number of days allowed
This function returns how many valid schedules exist



Step 1: Assign days to assignments

for day_assignment in product(range(1, m + 1), repeat=len(assignment_ids)):


Tries every possible way to assign a day (1 to m) to each assignment

Example for `m = 2`:


(1,1,1,1,1,1,1,1)
(1,1,1,1,1,1,1,2)



Step 2: Check dependencies

python
if not dependencies_satisfied(...):
    continue


If dependencies are violated → discard this schedule immediately



Step 3: Assign students


for student_assignment in product(range(N), repeat=len(assignment_ids)):


Tries every way to assign students to assignments



### Step 4: Track prompt usage

python
usage[day][student] += assignments[a]["cost"]


Counts how many prompts each student uses per day



Step 5: Capacity check


if all(usage[d][s] <= K for d in usage for s in usage[d]):


Ensures no student exceeds K prompts on any day

If valid → count this schedule


7. What the program outputs

Example output:


m = 5 → 18,468 schedules
m = 6 → 244,944 schedules


Meaning:

For 5 days, there are **18,468 valid ways** to schedule all assignments
For fewer than 5 days → **no valid schedule exists**



8. Important beginner notes 

This program uses **brute-force** (tries everything)
It is slow for large inputs
It is perfect for learning and correctness, not performance



9. What you should understand after reading this

By studying this program, you learn:

How constraints affect scheduling
How nested loops explore combinations
How real-world problems map to code
Why brute-force works (and when it doesn’t)


This script is designed to solve a scheduling problem where a group of students needs to complete several assignments over a set number of days. The core challenge is that some assignments depend on others being finished first, and students have a limited daily capacity for how much work they can do. 
Core Configuration and Data Setup

The code begins by importing the sys module and defining the solve_assignments function. At the top, two variables, N and K, are set to 3 and 5, representing three available students and a "budget" of five prompts per student per day. The tasks dictionary acts as the project roadmap. Each entry includes the number of prompts (effort) required to finish it and a deps list, which specifies which other assignments must be completed before that specific task can be started. For example, Assignment 4 can’t start until Assignments 7 and 2 are finished. 

Managing the Timeline
After asking the user how many days they want to simulate, the script initializes a completed set to track finished work and a schedule dictionary to store the results. It then enters a for loop that iterates through each day. At the start of every day, the code resets the student_prompts list, giving each of the three students a fresh bank of 5 prompts. It also creates a daily_tasks list to record what gets done during that specific 24-hour window. 

Logic for Selecting Tasks
The logic inside the daily loop is where the "brain" of the script lives. First, it identifies "available" tasks by checking the tasks dictionary to see which ones aren't finished yet and have all their dependencies met. To be efficient, it sorts these available tasks based on how many other tasks are waiting on them (their "out-degree"). This ensures that "bottleneck" assignments—the ones that unlock the most future work—are prioritized. 

Assigning Work to Students
Once the prioritized list of available tasks is ready, the script tries to fit them into the students' schedules. It iterates through the tasks and, for each one, looks for the first student who has enough prompts left in their daily budget to handle the work. If a student is found, their budget is docked, the task is marked as completed, and the assignment is logged. If no student has enough remaining prompts for a specific task, that task is skipped and must wait until the next day.
 
Final Reporting
After the days have run their course, the script prints out a summary. It loops through the schedule dictionary to show exactly which student did which assignment on each day. Finally, it performs a check to see if the completed set matches the full list of tasks. If some are missing, it warns the user which assignments were left unfinished; otherwise, it prints a success message confirming that the schedule was completed successfully.

