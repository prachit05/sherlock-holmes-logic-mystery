import pprint

class Rule:
    """Represents a logical rule, e.g., {Premise1, Premise2} -> Conclusion."""
    def __init__(self, premises, conclusion):
        # A set of fact strings that must be true for the conclusion to be true.
        self.premises = set(premises)
        # The fact string that is concluded if all premises are met.
        self.conclusion = conclusion

    def __repr__(self):
        return f"{', '.join(self.premises)} -> {self.conclusion}"

class KnowledgeBase:
    """Stores and manages all the known facts."""
    def __init__(self, initial_facts=None):
        self.facts = set(initial_facts) if initial_facts else set()

    def add_fact(self, fact):
        """Adds a fact to the knowledge base."""
        self.facts.add(fact)

    def get_facts(self):
        """Returns all facts in the knowledge base."""
        return self.facts

    def __repr__(self):
        return f"KB({pprint.pformat(self.facts)})"

def forward_chaining(kb, rules):
    """
    Performs forward chaining to deduce all possible facts.

    This function repeatedly iterates through the rules, adding new conclusions
    to the knowledge base until no more deductions can be made.
    """
    new_facts_added = True
    deductions = [] # To track the new facts found in this run

    # Loop until a full pass over the rules produces no new facts
    while new_facts_added:
        new_facts_added = False
        for rule in rules:
            # Check if all premises of the rule are in the knowledge base
            # and the conclusion is not already there.
            if rule.premises.issubset(kb.get_facts()) and rule.conclusion not in kb.get_facts():
                kb.add_fact(rule.conclusion)
                deductions.append(f"Deduced: {rule.conclusion}")
                new_facts_added = True
    
    return deductions

# --- Main execution block to demonstrate the engine ---
if __name__ == "__main__":
    print("🕵️  Initializing Sherlock's Logic Engine...\n")

    # 1. Define the initial facts from the crime scene
    initial_facts = [
        "Victim(Lord_Harrington)",
        "Location(Workshop)",
        "LockedFromInside(Workshop_Door)",
        "NoVisibleWounds(Lord_Harrington)",
        "Present(Cogsworth_Automaton)"
    ]

    # 2. Define the rules of deduction Sherlock can use
    game_rules = [
        Rule({"LockedFromInside(Workshop_Door)", "NoVisibleWounds(Lord_Harrington)"}, "Suggests(ImpossibleCrime)"),
        Rule({"Suggests(ImpossibleCrime)"}, "Motive(InternalAffair)"),
        Rule({"Present(Cogsworth_Automaton)", "Location(Workshop)"}, "Witness(Cogsworth_Automaton)"),
        
        # This is a key rule the player will unlock later with a clue
        Rule({"Activated(Consciousness_Device)", "Victim(Lord_Harrington)"}, "IsAlive(Lord_Harrington)"),
        Rule({"NoVisibleWounds(Lord_Harrington)"}, "IsDead(Lord_Harrington)"), # This fact comes from observation
    ]

    # 3. Initialize the Knowledge Base
    kb = KnowledgeBase(initial_facts)
    print("--- Initial Facts ---")
    pprint.pprint(kb.get_facts())
    print("-" * 23)

    # 4. Run the engine to see what can be deduced initially
    print("\n🔎 Running initial deductions...")
    new_conclusions = forward_chaining(kb, game_rules)
    if new_conclusions:
        for conclusion in new_conclusions:
            print(conclusion)
    else:
        print("No new deductions could be made from initial facts.")

    print("\n--- Knowledge Base After Initial Deductions ---")
    pprint.pprint(kb.get_facts())
    print("-" * 45)

    # 5. Simulate the player finding a critical clue
    print("\n✨ Player finds a hidden, still-warm 'Consciousness Transfer Device'!")
    kb.add_fact("Activated(Consciousness_Device)")
    
    print("\n🔎 Running deductions with the new clue...")
    new_conclusions = forward_chaining(kb, game_rules)
    if new_conclusions:
        for conclusion in new_conclusions:
            print(conclusion)
    
    print("\n--- Final Knowledge Base ---")
    pprint.pprint(kb.get_facts())
    print("-" * 28)

    # Check for the story's core contradiction
    if "IsAlive(Lord_Harrington)" in kb.get_facts() and "IsDead(Lord_Harrington)" in kb.get_facts():
        print("\n💥 CONTRADICTION DETECTED! The case is solved.")
        print("Lord Harrington is both biologically dead and consciously alive.")