# Define a name with whitespace characters
name = "\t  \n  John Doe  \n\t"

# Print name with whitespace
print("Original name with whitespace:")
print(repr(name))  # Using repr() to show whitespace characters clearly

# Using lstrip() - removes leading (left) whitespace
print("\nUsing lstrip():")
print(repr(name.lstrip()))

# Using rstrip() - removes trailing (right) whitespace
print("\nUsing rstrip():")
print(repr(name.rstrip()))

# Using strip() - removes both leading and trailing whitespace
print("\nUsing strip():")
print(repr(name.strip()))
