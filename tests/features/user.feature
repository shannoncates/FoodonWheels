Feature: Sign Up


Scenario: Adding User (Sunny)
Given I have the following user details:
|     email     | first_name | middle_initial | last_name | password | contact_number | address  |
| aya@gmail.com |     Aya    |        T       |   Flores  |  wertyu  |   09123456789  | address4 |
When the user clicks the submit button
Then it should have a '200' response
