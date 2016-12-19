Feature: Login


##################### Sunny Case ###############################


  Scenario: Successful log in
      Given I have the following login details:
      |      email  | password |
      | shannoncates@gmail.com |  pass3  |
      When I click login button
      Then I get a '200' response
      And a message "success" is returned



#################### Rainy Case #############################

  Scenario: Empty email field
        Given I have the following login details:
              |email      |password  |
              |               | pass2    |
        When I click login button
        Then I get a '200' response
        And a message "Invalid email or password" is returned


  Scenario: Empty password field
        Given I have the following login details:
              |  email      |password  |
              | shannoncates@gmail.com |          |
        When I click login button
        Then I get a '200' response
        And a message "Invalid email or password" is returned