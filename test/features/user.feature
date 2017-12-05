
Feature: Register

Scenario: User Registration Sunny Case
Given the user fills the form with these details:
| name     |  email                       | password |
| mariel  | foodie@gmail.com | password  |
When I submit the registration form
Then I should get a '200' response
And it will return these details:
| message | status |
| success | 200    |


Scenario: Sign up rainy email already exists
Given the user fills the registration form with these details:
| name     |  email                       | password
| mariel  | foodie.com | password
When I submit the registration form
Then I should get a '200' response
And it will return these details:
| message                    | status | 
|    email already exists    |    error   | 

Scenario: Sign up rainy no email
Given the user fills the form with these details:
| name     |  email                       | password |
| mariel  |  | password  | |
When I submit the signup form
Then I should get a '200' response
And it will return these details:
| message | status | 
|    email cannot be blank    |    error   |

Scenario: Sign up rainy invalid email
Given the user fills the form with these details:
| name     |  email                       | password |
| mariel  | foodie.com | password  |
When I submit the registration form
Then I should get a '200' response
And it will return these details:
| message | status | 
|    invalid email     |    error   | 

Scenario: Log in sunny
Given signs in as:
|email           |  password|
|foodie@gmail.com|  password|
When User signs in
Then I should get a '200' response
And it will return these details:
| message          | status | 
|    signed in     |    success  | 

Scenario: Log in rainy wrong password
Given signs in as:
|email           |  password|
|foodie@gmail.com|  wrongpass|
When User signs in
Then I should get a '200' response
And it will return these details:
| message          | status | 
|    email or password is incorrect     |    success  | 

Scenario: Log in rainy email does not exist
Given signs in as:
|email           |  password|
|foodie@gmail.com|  password|
When User signs in
Then I should get a '200' response
And it will return these details:
| message          | status | 
|    email or password is incorrect     |    success  | 

Scenario: Log in rainy no passed argument
Given signs in as:
|email           |  password|
|              |            |
When User signs in
Then I should get a '200' response
And it will return these details:
| message          | status | 
|    email or password is incorrect     |    success  | 

Scenario: Log out sunny
Given User is logged in as:
| email                    |  password|
| foodie@gmail.com |  fhm|
When User logs out
Then I should get a '200' response
And it will return these details:
|status|message|
|success    |signed out|

Scenario: Log out rainy 
Given User is not logged in as:
| email                    |  password|
| foodie@gmail.com |  fhm|
When User logs out
Then I should get a '200' response

