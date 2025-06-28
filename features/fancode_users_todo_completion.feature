Feature: FanCode City Users Todo Completion Validation
  As a QA Engineer
  I want to validate that all users of FanCode city have more than half of their todos completed
  So that I can ensure business requirements are met

  Background:
    Given the JSONPlaceholder API is accessible
    And the FanCode city coordinates are defined as latitude between -40 and 5 and longitude between 5 and 100

  @smoke @fancode
  Scenario: All FanCode city users should have more than 50% todo completion rate
    Given I have access to the user and todo data from the API
    When I identify all users belonging to FanCode city
    And I calculate the todo completion percentage for each FanCode user
    Then all FanCode city users should have more than 50% of their todos completed

  @regression @fancode
  Scenario: Validate FanCode city user identification
    Given I have access to the user data from the API
    When I filter users by FanCode city coordinates
    Then I should get users with latitude between -40 and 5
    And I should get users with longitude between 5 and 100
    And the identified users should be a subset of all users

  @api @fancode
  Scenario: Validate todo completion calculation accuracy
    Given I have a user with known todos
    When I calculate their todo completion percentage
    Then the calculation should be mathematically correct
    And the percentage should be between 0 and 100

  @business_logic @fancode
  Scenario Outline: FanCode user todo completion validation with different completion rates
    Given a FanCode city user has <total_todos> todos
    And <completed_todos> of them are completed
    When I calculate the completion percentage
    Then the completion percentage should be <expected_percentage>
    And the user should <result> the FanCode completion criteria

    Examples:
      | total_todos | completed_todos | expected_percentage | result |
      | 10          | 6              | 60.0               | pass   |
      | 10          | 5              | 50.0               | fail   |
      | 20          | 11             | 55.0               | pass   |
      | 8           | 4              | 50.0               | fail   |
      | 15          | 8              | 53.33              | pass   |

  @edge_cases @fancode
  Scenario: Handle users with no todos
    Given a FanCode city user has no todos
    When I calculate their todo completion percentage
    Then the completion percentage should be 0
    And the user should fail the FanCode completion criteria

  @boundary @fancode
  Scenario Outline: Validate FanCode city boundary conditions
    Given a user has coordinates latitude <lat> and longitude <lng>
    When I check if the user belongs to FanCode city
    Then the user should be <result> as a FanCode city user

    Examples:
      | lat  | lng | result     |
      | -40  | 5   | identified |
      | -40  | 100 | identified |
      | 5    | 5   | identified |
      | 5    | 100 | identified |
      | 0    | 50  | identified |
      | -40.1| 50  | not identified |
      | 5.1  | 50  | not identified |
      | 0    | 4.9 | not identified |
      | 0    | 100.1| not identified |

  @error_handling @fancode
  Scenario: Handle API connectivity issues gracefully
    Given the API is temporarily unavailable
    When I attempt to fetch user and todo data
    Then the system should handle the error gracefully
    And provide meaningful error messages

  @performance @fancode
  Scenario: Validate performance requirements
    Given I need to validate all FanCode users
    When I run the complete validation process
    Then the validation should complete within 10 seconds
    And the API calls should complete within 5 seconds each
