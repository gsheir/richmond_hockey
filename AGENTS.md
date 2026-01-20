# **General instructions**

Where available, use thinking mode or verbalise your thought process before returning your response.

Make full use of markdown formatting in your reponse, including suitable headers. Do not create any additional markdown files to report progress or as a summary, display these in the chat window instead.

Always use British English, including in your responses, any code created (including file names, module names, function names etc.) and any documentation created. Use the Oxford style for any technical writing, including the use of the Oxford comma and using the en-dash with spaces around it: “ – “.

## **If asked to propose a solution**

Respond to the following question types as indicated:

- "Describe the steps ...": Do not make any code changes. Do not return code snippets. Just describe the steps in detail so that they can be implemented by an AI agent or a human. Do not include estimates. Structure this preferably in stages that can be implemented separately.

If you are unclear on the requirements, clarify those before proposing solutions.

## **If code changes are required**

Read the full codebase before making any proposals or changes.

Always ask for user confirmation before making changes unless explicitly told to make changes.

If using logging, be concise rather than verbose. Do not use excessive formatting with dividers; newlines are sufficient.

Add only neccesary comments. Do not use excessive formatting with dividers; newlines are sufficient.

Provide a summary in the chat window after making the changes. If the changes are more than a few lines, comprehensively describe all changes in your summary.

# **Repo-specific instructions**

## **Python**

This project uses `uv` for dependency management. Use `uv add` to add any dependencies. Use `uv run` to run any Python.

### **Code structure**

Always add imports to the top of the file, not halfway through.

### **Formatting**

This project uses Ruff for formatting. After making Python changes, use `uv run ruff format; uv run ruff check` to format, and address any errors before finishing.

### **Testing**

This project uses `pytest`. Tests should be very concise, preferably of the form

```python
def test_a_function():
    input_data = ...
    expected = ...
    result = a_function(input_data)

    assert result == expected

```

Don't use mocks unless absolutely neccesary. Use fixtures only for test setup, not for input data.

Related tests for a single function should be grouped under a test class.
