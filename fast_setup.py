from cat.mad_hatter.decorators import hook

@hook  # Priorità predefinita = 1
def before_agent_starts(agent_input, cat):
    cat.send_notification(f"è entrato nel plugin")
    
    domanda = agent_input['input']
        
    # Dividi il problema in domande più piccole
    domanda = cat.llm(f"Dividi questa domanda in 3 domande più piccole: {domanda}. Dividi ogni domanda con un punto e virgola.")
    cat.send_notification(f"ha generato le domande")
    # Estrai le 3 domande
    domande = domanda.split(";")
    
    # Cerca una soluzione alle domande
    soluzioni = []
    for domanda in domande:
        risposta = cat.llm(f"Cerca 3 soluzioni alla domanda: {domanda.strip()}. Dividi le soluzioni con un punto e virgola. Utilizzando queste informazioni: {agent_input['episodic_memory']}, {agent_input['declarative_memory']}, {agent_input['tools_output']}")
        # Dividi le soluzioni
        soluzioni.append(risposta.split(";"))
    cat.send_notification(f"ha generato le soluzioni")
    
    # Chiedi all'LLM la soluzione migliore
    soluzioni_flat = [soluzione for lista in soluzioni for soluzione in lista]  # Appiattisci la lista di soluzioni
    soluzione_migliore = cat.llm(f"formula la risposta a questa domanda {domanda}, utilizza queste informazioni: {', '.join(soluzioni_flat)}?")
    
    cat.send_notification(f"ha generato la soluzione migliore")

    agent_input['input'] = soluzione_migliore
    
    #todo: la soluzione finale ha dei rpoblemi?
    cat.send_notification(f"la soluzione migliore e' stata generata")
    return agent_input


