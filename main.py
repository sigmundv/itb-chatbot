from chatbot import chat_parser, chat_planning, chat_feedback, chat_acquired_knowledge, chat_knowledge
import pathlib

db_file = "chatbot.db"

# we use an SQLite database to store user feedback regarding the usefulness of an answer
# if the database does not exist, we create it together with a table to store the feedback
if not pathlib.Path(db_file).exists():
    dbm = chat_acquired_knowledge.DatabaseManager(db_file)
    dbm.create('''CREATE TABLE queries (
                    query text, answer text, satisfied integer,
                    unique (query, answer))''')

# we run he program in an infinite loop so the user will be prompted again after each input
while True:

    print("\nWelcome, please enter a query (or q to quit):\n")

    query = input().lower().replace('?', '')  # remove the question mark if there is any as it's not needed for search

    # if the user inputs 'q' we stop the program
    if query == 'q':
        break

    query_type = chat_parser.parse(query)

    # we run the planning and presenting step in an infinite loop so we can restart the planning step
    # when the user gives negative feedback
    while True:
        query_result = chat_planning.plan(db_file, query, query_type)
        chat_feedback.present_result(query_result)

        # we get the user feedback, and in case of 'yes' we store the answer for later retrieval,
        # break out of the inner loop, and continue to the next query
        feedback = chat_feedback.get_feedback()
        if "yes" in feedback:
            chat_acquired_knowledge.store_satisfactory_result(db_file, query=query, answer=query_result)
            break

        # in case of 'no' we store the also store the answer, but mark it as unsatisfactory
        # and restart the planning step
        else:
            chat_acquired_knowledge.store_unsatisfactory_result(db_file, query=query, answer=query_result)
            continue
