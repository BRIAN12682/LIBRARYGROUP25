# LIBRARY SYSTEMS Group25
Library Systems web based application 

## Getting started
Creating a web based library syastem that allows users to request for the books and allows the librarian to add the books.
the librarian can be allowed to add various information about

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/group-251/library-systems-group25.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/group-251/library-systems-group25/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

Brainstorming . 
 The Group brainstormed by coming together to put ideas on paper and thereafter created a low fidelity 
paper prototype to formalize the initial design concept. Firstly, the user’s functional requirements were 
defined; e.g. requesting for a book. 
We initially made a mistake of counting the authentication part as a user story but we were corrected by 
the Lecturer. Then the website has been designed in a sharp and engaging format to appeal to our 
target audience but with a very clear navigational framework to make the website as user friendly and 
seamless to use as possible and appealing. 

PROJECT INFORMATION
e a web-based application that a enables student to request for books from a library catalog. The 
library should contain a set of books showing the title, publication date, subject area, author etc. The 
Librarian should have an interface to post the books and the student should be able to search for a book 
and request for it. A book once requested needs to have a return date that is automatically tracked. A 
book is unavailable if it has been given out, and only becomes available when returned. Before the 
return date (1 day) the borrower should get a notification to return the book. Moreover, a book 
returned 3 days after the return date attracts a penalty of 5,000 UGX. If return after ten days the penalty 
is 15,000 UGX. The system should display a report that shows the books that need to be returned, when 
they should be returned and the penalty