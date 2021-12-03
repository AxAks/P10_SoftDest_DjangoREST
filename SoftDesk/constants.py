"""
Constants used throughout the project
"""

#  mettre des chiffres dans les roles, ce serait plus propre ?
PROJECT_TYPES = [('Back-End', 'Back-End'), ('Front-End', 'Front-End'), ('iOS', 'iOS'), ('Android', 'Android')]
CONTRIBUTOR_ROLES = [('Creator', 'Creator'), ('Manager', 'Manager'), ('Author', 'Author')]
ISSUE_TAGS = [('Bug', 'Bug'), ('Feature', 'Feature'), ('Task', 'Task')]
ISSUE_PRIORITIES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
ISSUE_STATUSES = [('Todo', 'Todo'), ('Handled', 'Handled'), ('Closed',  'Closed')]

PROJECT_ADMIN = ['Manager', 'Creator']


UNSUCCESSFUL_LOGIN_MSG = 'Unsuccessful connection attempt'