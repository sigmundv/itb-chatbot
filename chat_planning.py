import chat_acquired_knowledge
import chat_knowledge

# we load in the chatterbot corpus to use with the conversational queries
conversation_corpus = chat_knowledge.load_conversation_corpus()


def plan(db, query, query_type):
    # we search for previous satisfactory answers to the same query and return it if found

    previous_satisfactory_answer = chat_acquired_knowledge.get_previous_results(db, query, 1)
    if len(previous_satisfactory_answer) > 0:
        return previous_satisfactory_answer[0][0]

    # if no satisfactory answers were returned, from the lookup above, look for unsatisfactory answers,
    # which will be filtered out before we return the answer from the search below

    previous_unsatisfactory_answer = chat_acquired_knowledge.get_previous_results(db, query, 0)
    answers = [answer[0] for answer in previous_unsatisfactory_answer]

    if "question" in query_type:
        return chat_knowledge.get_question_knowledge(query_type["question"], answers)

    elif "conversation" in query_type:
        return chat_knowledge.get_conversation_knowledge(query_type["conversation"], conversation_corpus, answers)
