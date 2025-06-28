Feature: API Client Functionality
  As a developer
  I want to ensure the API client works correctly
  So that I can reliably fetch data from JSONPlaceholder API

  Background:
    Given the JSONPlaceholder API is available at "http://jsonplaceholder.typicode.com"

  @api @smoke
  Scenario: Fetch all users from API
    Given I have an API client instance
    When I fetch all users from the API
    Then I should receive a list of users
    And the list should contain exactly 10 users
    And each user should have required fields for FanCode validation

  @api @smoke
  Scenario: Fetch all todos from API
    Given I have an API client instance
    When I fetch all todos from the API
    Then I should receive a list of todos
    And the list should contain exactly 200 todos
    And each todo should have required fields for completion calculation

  @api @regression
  Scenario: Fetch todos for specific user
    Given I have an API client instance
    And I know a valid user ID
    When I fetch todos for that specific user
    Then I should receive only todos belonging to that user
    And all returned todos should have the correct user ID

  @api @error_handling
  Scenario: Handle invalid user ID gracefully
    Given I have an API client instance
    When I fetch todos for a non-existent user ID
    Then I should receive an empty list
    And no errors should be thrown

  @api @performance
  Scenario: API response time validation
    Given I have an API client instance
    When I measure the response time for fetching users
    Then the response time should be less than 5 seconds
    When I measure the response time for fetching todos
    Then the response time should be less than 5 seconds
