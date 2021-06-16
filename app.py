from agent import *
import random


def display_results(agents):
    for ag in agents:
        print(sum(ag.score))


def pair_agents(agents, verbose=False):
    random_agents = list(agents)
    random.shuffle(random_agents)

    pairings = list(zip(random_agents[:len(random_agents)//2],
                        random_agents[len(random_agents)//2:]
                        ))
    if verbose:
        for p in pairings:
            print("Pair : " + str(p[0]) + "|" + str(p[1]))
    return pairings


if __name__ == "__main__":
    verbose = False
    agents = []

    agents.append(ReciprocalAgent(0, "ReciprocalAgent"))
    agents.append(ReciprocalAgent(1, "ReciprocalAgent"))
    agents.append(ReciprocalAgent(2, "ReciprocalAgent"))

    agents.append(CollaborativeAgent(3, "CollaborativeAgent"))
    agents.append(CollaborativeAgent(4, "CollaborativeAgent"))
    agents.append(CollaborativeAgent(5, "CollaborativeAgent"))
    agents.append(CollaborativeAgent(9, "CollaborativeAgent"))

    agents.append(TraitorAgent(6, "TraitorAgent"))
    agents.append(TraitorAgent(7, "TraitorAgent"))
    agents.append(TraitorAgent(8, "TraitorAgent"))

    nb_rounds = 10000  # random.range(100)

    if verbose:
        print("nb of rounds", nb_rounds)
    for r in range(nb_rounds):
        pairings = pair_agents(agents, verbose)

        for pair in pairings:
            # Evaluate stretegie
            pair[0].initiate_interraction(pair[1])
            pair[0].decide()
            pair[1].initiate_interraction(pair[0])
            pair[1].decide()

            # resolve match
            """ Table format :
            (our answer, other agent's answer) : our score increment
            cooperate : True (T), betray : False (F)
            (T,T) :   1
            (T,F) :   20
            (F,T) :   0
            (F,F) :   5 """
            a = pair[0].cooperate
            b = pair[1].cooperate

            if a and b:
                pair[0].update_score(1)
                pair[1].update_score(1)
            if not a and not b:
                pair[0].update_score(5)
                pair[1].update_score(5)
            if not a and b:
                pair[0].update_score(0)
                pair[1].update_score(20)
            if a and not b:
                pair[0].update_score(20)
                pair[1].update_score(0)

            if verbose:
                print("({ad},{bd}): ({a},{b})".format(
                    ad=pair[0].description + "_" + str(pair[0].id), bd=pair[1].description + "_" + str(pair[1].id), a=a, b=b))
                print("update is a:{a}, b:{b}".format(
                    a=pair[0].score[-1], b=pair[1].score[-1]))
            # Update memories
            pair[0].update_memory(b)
            pair[1].update_memory(a)

    # display_results(agents)
    result = [sum(i.score) / nb_rounds for i in agents]
    print(result)
