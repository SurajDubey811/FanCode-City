Feature: Data Model Validation
  As a developer
  I want to ensure data models work correctly
  So that I can reliably handle user and todo data

  @model @smoke
  Scenario: Create User model from API data
    Given I have user data from the JSONPlaceholder API
    When I create a User object from the API data
    Then the User object should have all required fields
    And the coordinates should be properly extracted from the address

  @model @smoke
  Scenario: Create Todo model from API data
    Given I have todo data from the JSONPlaceholder API
    When I create a Todo object from the API data
    Then the Todo object should have all required fields
    And the completion status should be a boolean value

  @model @edge_cases
  Scenario Outline: User model with various coordinate values
    Given I have user data with latitude <lat> and longitude <lng>
    When I create a User object from this data
    Then the User object should have latitude <lat>
    And the User object should have longitude <lng>

    Examples:
      | lat   | lng    |
      | -40.0 | 5.0    |
      | 5.0   | 100.0  |
      | 0.0   | 50.0   |
      | -20.5 | 75.25  |

  @model @validation
  Scenario: User model string representation
    Given I have a User object with name "John Doe"
    When I convert the User to string
    Then the string should contain the user's name
    And the string should be human-readable

  @model @validation
  Scenario: Todo model string representation
    Given I have a Todo object with title "Sample Todo"
    When I convert the Todo to string
    Then the string should contain the todo's title
    And the string should indicate completion status
