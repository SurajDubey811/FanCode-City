Feature: Utility Functions
  As a developer
  I want to ensure utility functions work correctly
  So that I can rely on helper functions for validation logic

  @utils @smoke
  Scenario Outline: Email validation with various formats
    Given I have an email address "<email>"
    When I validate the email format
    Then the validation result should be <expected>

    Examples:
      | email                    | expected |
      | user@example.com         | true     |
      | test.email@domain.co.uk  | true     |
      | invalid.email            | false    |
      | @invalid.com             | false    |
      | user@                    | false    |
      | user@domain              | false    |

  @utils @fancode
  Scenario Outline: FanCode city coordinate validation
    Given I have coordinates latitude <lat> and longitude <lng>
    When I check if the coordinates are within FanCode city bounds
    Then the result should be <expected>

    Examples:
      | lat   | lng   | expected |
      | -40   | 5     | true     |
      | -40   | 100   | true     |
      | 5     | 5     | true     |
      | 5     | 100   | true     |
      | 0     | 50    | true     |
      | -40.1 | 50    | false    |
      | 5.1   | 50    | false    |
      | 0     | 4.9   | false    |
      | 0     | 100.1 | false    |

  @utils @calculation
  Scenario Outline: Todo completion percentage calculation
    Given I have a list of todos with <total> items
    And <completed> of them are marked as completed
    When I calculate the completion percentage
    When I check if the coordinates are within FanCode city bounds
    Then the result should be <expected_percentage>

    Examples:
      | total | completed | expected_percentage |
      | 10    | 0         | 0.0                |
      | 10    | 5         | 50.0               |
      | 10    | 6         | 60.0               |
      | 10    | 10        | 100.0              |
      | 0     | 0         | 0.0                |
      | 3     | 1         | 33.33              |

  @utils @edge_cases
  Scenario: Handle empty todo list
    Given I have an empty list of todos
    When I calculate the completion percentage
    When I check if the coordinates are within FanCode city bounds
    Then the result should be 0.0

  @utils @custom_bounds
  Scenario: FanCode city validation with custom bounds
    Given I define custom coordinate bounds with lat_min -30, lat_max 10, lng_min 0, lng_max 120
    And I have coordinates latitude 0 and longitude 50
    When I check if the coordinates are within the custom bounds
    Then the result should be true
