# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Class Pet: (structure for all pets, including their attributes, and methods to access them)
- Methods:
    - getBreed
    - getWeight
    - getStatus
    - setBreed
    - setWeight
    - setStatus
    - showPetInfo

- Attributes:
    - breed
    - weight
    - health_status

Class Owner: (add/remove pets from users, get/set their info and preferences)
- Methods: 
    - Add Pet
    - Remove Pet
    - showPets
    - showOwnerInfo
    - getPreferences
    - setPreferences
- Attributes: 
    - pets
    - gender
    - age
    - preferences

Class Task: (add/remove/change/show tasks)
- Methods: 
    - add task
    - remove task
    - changeTask
    - showTasks

- Attributes: 
    - tasks -> (duration, priority)
    
Class Scheduler: (create/show schedules)
- Methods: 
    - makeSchedule
    - showSchedule
- Attributes: 
    - schedules

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
1. added a pet_id attribute to identify pets by id rather than name (duplicate names can mess up the logic)
2. reduced redundancy by changing explicit get/set methods in the two dataclasses, which have direct attribute access already. They now also perform validation of the values.
3. allowed tasks as input to Scheduler.makeSchedule and the Owner class, so ensured tasks inputted via Owner only.
4. Changed Owner methods to use ordered lists and map lookup to show and update/get values.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
- the scheduler considered time, priority, and preferences. I decided that priority should be first, since it directly identified what was most important, followed by time, then preferences to maximize tasks completed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
- the scheduler checks for exact timestamps when checking for scheduling conflicts rather than overlapping durations. This is reasonable since we want lightweight conflict checking, which can be easily done via comparison of the timestamp values. Having to add complex time-interval math too early complicates the task, which we don't want to do in this scenario.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
1. I used Copilot to brainstorm design choices, implement decision making i've made, debug issues with code changes, implement pytest test cases to very the code logic was implemented correctly, and other things.
2. The concise prompts with the correct context were the most helpful to get exactly what I wanted out of the agent in one-shot. Also, changing to ask mode and asking clarifying, pointed questions helped me understand exactly the roadblock I was not getting from looking at the code myself.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
1. I did not accept that the Task class had properly sorted the tasks since i did not see that logic in the agent output. I evaluated this by asking for a pytest test case to verify the sorting logic, and explain any problem and fix the agent had to make to get the test case to pass. In this way, it added the correct sorting logic and explained the mistake I had noticed.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
1. I tested pet creation/deletion, task creation/deletion, task sorting, schedule creation, and how all of the tasks and schedules changed ordering depending on filtering by time, priority, or preferences.
2. These tests are important to ensure the code logic in the app works as intended. Safeguarding against bugs ensures a smooth experience for the user and also makes maintenance and future development safer and easier for both people who are new and old to the codebase.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
1. I am confident the scheduler works correctly, but I know that I still would like to confirm more edge cases at a future time to make sure its safe for a large user base. 
2. I would test how adding the same task and description, along with the same priority affects the scheduling. Having two tasks be virtually identical would be interesting to see how it will parse them if they don't overlap in duration. Which one will be first? I also want to see what happens if I add a large amount of pets to a user and see how their schedule changes depending on different preferences.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satisfied with the UML diagram creation and thought process that went into it.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
1. I would improve the conflict resolution logic to better respond to duration conflicts, since I think users will have that problem a lot (especially the busier ones).

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
It's important to understand how the app is supposed to function, and make sure that the AI understands your vision and the features you want to implement. The key is explaining everything clearly and concisely to develop a solid plan and design that will make a great app!
