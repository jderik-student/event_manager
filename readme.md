# Event Manager Company: Software QA Analyst/Developer Onboarding Assignment

## Links to Closed Issues
### Username Validation
1. [Update Valid Username Constraints](https://github.com/jderik-student/event_manager/issues/9)
2. [Nickname Uniqueness](https://github.com/jderik-student/event_manager/issues/11)
### Password Validation
1. [Password Length](https://github.com/jderik-student/event_manager/issues/13)
2. [Password Complexity](https://github.com/jderik-student/event_manager/issues/15)
### Profile Field Edge Cases
1. [Profile Field - Ensure profile picture URL is a valid image](https://github.com/jderik-student/event_manager/issues/17)
2. [Profile Field Edge Cases](https://github.com/jderik-student/event_manager/issues/19)
### Instructor Video Issue
1. [The Example Values in the FastAPI Doc have different nicknames](https://github.com/jderik-student/event_manager/issues/7)

## DockerHub Deployed Image
https://hub.docker.com/repository/docker/jderikito1/is601-homework10/general

## Reflection
The biggest technical challenges I faced when working on this assignment came when trying to get all the unit tests working after immediately forking the repo. The test files that gave me the most issues were test_user_api.py, test_email.py, and test_user_service.py. The problems that were causing the tests to fail were not just typos or incorrectly spelled fields, rather test_user_api was missing valid tokens for tests, and test_email and test_user_service were missing the information for the SMTP server. From these issues, I learned how important it is to thoroughly read the existing documentation on comments of code and how to leverage online resources to help debug these issues. As a result, I was successfully able to create the required access tokens and realized that I needed to develop a Mailtrap account for this repo. Outside of the lessons I learned through these tests I also learned a lot about APIs in general and how to create/ structure them. I was able to learn and understand the workflow of sending and translating a user request to an API endpoint into the code's schemas and then into the database. Lastly, from working on this assignment I learned how valuable it is to break up your work into smaller commits which allowed for much digestable testing and helped in finding issues faster than if I had much larger commits.
From a collaborative standpoint I learned a lot about professional software development as well. The whole process was very insightful and helpful in understanding how to work in a professional environment. The exercise of reporting issues and providing information, helped me to be mindful of being thorough in my explanations as another team member may be the one to work on the issue or if I worked on the issue, it would be important for others to understand what I'm doing and why. Also, the workflow of getting my code changes approved, through first the CI pipeline (the tests) and the CD pipeline (DockerHub) showed how robust and thorough these pipelines are to ensure that no bad code reaches production. Overall, through all the steps we had to follow to get our code changes to the main branch, I gained a lot of insight into what it means to work in a collaborative professional environment in software development. 
