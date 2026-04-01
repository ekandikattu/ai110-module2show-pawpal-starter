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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
