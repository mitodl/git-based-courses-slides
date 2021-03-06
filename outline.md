# Git based Courses

- Intro
  - Who Peter and Carson Are
  - Show overall process
  - What we will talk about
    - Course Production Workflow
    - Technical Implementation
- Course Production Workflow
    - XML Course Development
        - ...
  - Studio Course Publication
        - ...
- Technical Implementation
    - Course Import via Git
      - Management command
      - Sysadmin dashboard
  - Course Export via Git
	  - Management command
	  - Studio Export
		- Feature flag
		- Advanced settings
		- Export to Git view
  - Automation
	  - gitreload hook handler
	  - XML course development
		- Import initially
		- Add hook to repo
	  - Publishing to Students
		- Studio course
		  - Use button
		- XML Course
		  - Merge to `live`/`release`
	  - Content Store Optimization
		- Use shared storage (nfs, gluster, drbd, etc)
		- Set git no import flag
		- From minutes to seconds
- Conclusion
	- Why we think it works
	- Why is it better/worse than existing publish model
	- Future Work
	  - Course import API to remove dependency of gitreload on platform
	  - "Create a Course" Web request
		- Automatic repo creation, initial import, and trigger setup
	- Questions
  
