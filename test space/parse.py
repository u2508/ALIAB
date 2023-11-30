import wikitextparser as wtp

try:
    # Your code that may raise DisambiguationError
    result = wtp.parse("Your input here")
    print(result)
except wtp.exceptions.DisambiguationError as e:
    # Display all options
    print("DisambiguationError: Multiple options found.")
    print("Options:")
    for option in e.options:
        print(f"- {option}")
