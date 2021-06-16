import random


class Agent:
    """
    Notes
    ----------
    There is a really big assumption in this simulation. Agents have no idea when the game will end. Therefore, they can not modify their strategy based on the number games left to play.
    The score increment is calculated based on a combination of our answer and the answer of the other agent.
    Table format :
        (our answer, other agent's answer) : our score increment
        cooperate : True (T), betray : False (F)
        (T,T) :   1
        (T,F) :   20
        (F,T) :   0
        (F,F) :   5
    """

    def __init__(self, identifier, description="unamed agent"):
        """
        Parameters
        ----------
        id :    int
                Our identifier
        description :  String
                Short description
        agent_id:   int
                    Id of the agent that is currently interracting with us
        cooperate : boolean
                    out current answer (True : cooperate, False: betray)
        memory :    dictionary
                    past interractions with the other agents. (dictionnary whose key is the agent id)
        score : array of int
                our score increment, updated after each round
        """
        self.id = identifier
        self.description = description
        self.agent_id = None
        self.cooperate = True
        self.memory = {}
        self.score = []

    def __str__(self):
        return 'ID='+str(self.id)+'; '+self.description

    def decide(self):
        """
        logic for  decision
        The only known information at that time is the Agent with whom we interract
        and our memory of our past interractions with them
        """
        ###########################################################################
        # Add you logic here
        # for example :
        # - always cooperate
        # - always betray
        # - randomly choose
        # - betray if other agent has betrayed you in the past
        # - cooperate by default, but betray if the agent betrayed you last time.
        self.cooperate = True
        ###########################################################################

    def initiate_interraction(self, agent_id):
        self.agent_id = agent_id

    def update_memory(self, agent_decision):
        """
        update our memory with the last interraction we have had with a specific agent.
        store both our answer and theirs, stored as a list, in an array : (their answer, our answer)
        """
        last_memory = (agent_decision, self.cooperate)
        if self.agent_id in self.memory:
            self.memory[self.agent_id].append(last_memory)
        else:
            self.memory[self.agent_id] = [last_memory]

    def update_score(self, delta):
        """
        Parameters
        ----------
        delta : int
            our last round score increase
        """
        self.score.append(delta)


class CollaborativeAgent(Agent):
    def decide(self):
        self.cooperate = True


class ReciprocalAgent(Agent):
    def decide(self):
        self.cooperate = True
        if self.agent_id in self.memory:
            self.cooperate = self.memory[self.agent_id][-1]


class TraitorAgent(Agent):
    def decide(self):
        self.cooperate = False
        if self.agent_id in self.memory:
            if False in self.memory[self.agent_id]:
                self.cooperate = False


class UnforgivingAgent(Agent):
    def decide(self):
        self.cooperate = True
        if self.agent_id in self.memory:
            if False in self.memory[self.agent_id]:
                self.cooperate = False


class ChaoticAgent(Agent):
    def decide(self):
        self.cooperate = random.choice((True, False))
