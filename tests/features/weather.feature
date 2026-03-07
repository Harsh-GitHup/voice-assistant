Feature: Weather query handling
  Scenario: User asks for weather in a valid city
    Given the assistant is listening
    When the user says "What is the weather in Paris"
    Then the assistant should respond with "The weather is"

  Scenario: Check weather via voice
    Given the assistant is active
    And the user says "What is the weather in New York"
    Then the assistant should fetch data from OpenWeather
    And speak the temperature to the user

  Scenario: User asks weather for a city
    Given the assistant is listening
    When the user says "what is the weather in London"
    Then the assistant should respond with "the weather is clear sky in London"
    And the assistant should fetch data from OpenWeather
    And speak the temperature to the user