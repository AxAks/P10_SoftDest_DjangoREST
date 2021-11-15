"""
draft



Unauthenticaded:
Signup -> AllowAny
Create -> AllowAny


Create Project ->  isAuthenticated
Get Projects -> IsAuthenticated, only own projects
Get Specific project -> IsAuthenticated,  ?only own projects?IsContributor
Update Project -> IsAuthenticated, IsProjectCreator or IsProjectManager













Projects permissions:IsAuthenticated + IsContributor (IsCreator or IsManager or IsAuthor)
- CR:IsAuthenticated + IsProjectContributor UD:IsProjectCreator or IsProjectManager

Contributors permissions: IsAuthenticated + IsCreator or IsManager
- CR:IsAuthenticated + IsProjectContributor UD:IsProjectCreator or IsProjectManager
(views : Creator= unique, Manager=unique par project)

Issues permissions: IsAuthenticated +
- CR:IsAuthenticated + IsProjectContributor  UD:IsIssueAuthor

Comments permissions: IsAuthenticated +
- CR:IsAuthenticated + IsProjectContributor  UD:IsCommentAuthor

"""


