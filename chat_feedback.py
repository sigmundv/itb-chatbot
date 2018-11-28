import re
import textwrap

textwrapper = textwrap.TextWrapper(width=80)

# we build a regex pattern to get rid of words/spaces/numbers inside square brackets and other Wikimedia markup
pattern_to_clean = re.compile(r"\[\w*\s*\d+\]|\(listen\)|\[update\]")


def present_result(result):
    # this uses Python's textwrap module to make the output a bit more readable
    # by restricting the with to 80 points

    output = pattern_to_clean.sub('', result)
    wrapped_output = '\n'.join(textwrapper.wrap(output))
    print(wrapped_output)


def get_feedback():
    return input("\n\nAre you satisfied with the provided answer? Yes or no:\n\n").lower()
