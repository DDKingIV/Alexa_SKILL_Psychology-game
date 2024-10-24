import lambda_function

#Lista per salvare le info sul paziente tra una visita e l'altra
savepatient = []




def calculate_status_modifiers(topic):
    lambda_function.currentvisit.topicbonusmalus = 0
    lambda_function.currentvisit.stressbonusmalus = 0
    lambda_function.currentvisit.trustbonusmalus = 0
    if curr_patient.state == "AN":
        currentvisit.topicbonusmalus = curr_patient.stress - curr_patient.trust
        currentvisit.stressbonusmalus = round(((curr_patient.stress - curr_patient.trust) / 10) - (p1.aggr / 3))
        currentvisit.trustbonusmalus = round(((curr_patient.stress - curr_patient.trust) / 10) + (p1.aggr / 3))
    if curr_patient.state == "NV":
        currentvisit.topicbonusmalus = round((curr_patient.stress / 2) - curr_patient.trust)
        currentvisit.stressbonusmalus = round(((curr_patient.stress - curr_patient.trust) / 10) - (p1.dire / 3))
        currentvisit.trustbonusmalus = round(((curr_patient.stress - curr_patient.trust) / 10) + (p1.dire / 3))
    if curr_patient.state == "TR":
        currentvisit.topicbonusmalus = round(curr_patient.stress - (curr_patient.trust / 2))
        currentvisit.stressbonusmalus = round(((curr_patient.trust + curr_patient.stress) / 10) - (p1.posi / 3))
        currentvisit.trustbonusmalus = round(((curr_patient.trust + curr_patient.stress) / 10) + (p1.posi / 3))
    if curr_patient.state == "AP":
        currentvisit.topicbonusmalus = (curr_patient.trust - curr_patient.stress)
        currentvisit.stressbonusmalus = round(((curr_patient.trust - curr_patient.stress) / 10) - (p1.grat / 3))
        currentvisit.trustbonusmalus = round(((curr_patient.trust - curr_patient.stress) / 10) + (p1.grat / 3))
    if curr_patient.state == "":
        currentvisit.topicbonusmalus = 0
        currentvisit.stressbonusmalus = 0
        currentvisit.trustbonusmalus = 0

def claculate_stresstrust_changes(self):
    if currentvisit.md == "ag":
        currentvisit.cs = 0
        currentvisit.ct = 0
        currentvisit.cs += (1 + (p1.aggr / 2) + random.randint(0, 1)) + currentvisit.stressbonusmalus
        currentvisit.ct -= (1 + (p1.aggr / 2) + random.randint(0, 1)) + currentvisit.trustbonusmalus
        currentvisit.choise = random.choice(aggre)
    elif currentvisit.md == "lo":
        currentvisit.cs = 0
        currentvisit.ct = 0
        currentvisit.cs -= (1 + (p1.grat / 2) + random.randint(0, 1)) + currentvisit.stressbonusmalus
        currentvisit.ct -= (1 + (p1.grat / 2) + random.randint(0, 1)) + currentvisit.trustbonusmalus
        currentvisit.choise = random.choice(logic)
    elif currentvisit.md == "dr":
        currentvisit.cs = 0
        currentvisit.ct = 0
        currentvisit.cs += (1 + (p1.dire / 2) + random.randint(0, 1)) + currentvisit.stressbonusmalus
        currentvisit.ct += (1 + (p1.dire / 2) + random.randint(0, 1)) + currentvisit.trustbonusmalus
        currentvisit.choise = random.choice(direc)
    elif currentvisit.md == "po":
        currentvisit.cs = 0
        currentvisit.ct = 0
        currentvisit.cs -= (1 + (p1.posi / 2) + random.randint(0, 1)) + currentvisit.stressbonusmalus
        currentvisit.ct += (1 + (p1.posi / 2) + random.randint(0, 1)) + currentvisit.trustbonusmalus
        currentvisit.choise = random.choice(posit)

def topicchange(self):
    if curr_patient.firstvisit:
        curr_patient.firstvisit = False
        curr_visit.agegendermod(self)
        self.nextquest()
    elif currentvisit.tpold != currentvisit.tp:
        currentvisit.currentmessage = "You respond: Ok, but now I would like to talk about something else"
        currentvisit.tpold = currentvisit.tp
        curr_visit.agegendermod(self)
        self.nextquest()
        self.updatetext()
    else:
        currentvisit.tpold = currentvisit.tp
        curr_visit.agegendermod(self)
        self.nextquest()
        

# funzione per aggiungere modifiers per età e sesso del paziente
def agegendermod(self):
    currentvisit.agmod = 0
    page = curr_patient.age
    if curr_patient.gender == "Male" and 0 < int(page) < 25:
        if currentvisit.md == "ag":
            currentvisit.agmod -= 3
        elif currentvisit.md == "dr":
            currentvisit.agmod -= 2
        elif currentvisit.md == "po":
            currentvisit.agmod += 0
        elif currentvisit.md == "lo":
            currentvisit.agmod += 1
    elif curr_patient.gender == "Male" and 25 < int(page) < 65:
        if currentvisit.md == "ag":
            currentvisit.agmod -= 1
        elif currentvisit.md == "dr":
            currentvisit.agmod += 3
        elif currentvisit.md == "po":
            currentvisit.agmod -= 1
        elif currentvisit.md == "lo":
            currentvisit.agmod -= 3
    elif curr_patient.gender == "Male" and 65 < int(page) < 100:
        if currentvisit.md == "ag":
            currentvisit.agmod += 3
        elif currentvisit.md == "dr":
            currentvisit.agmod += 3
        elif currentvisit.md == "po":
            currentvisit.agmod -= 3
        elif currentvisit.md == "lo":
            currentvisit.agmod += 2
    elif curr_patient.gender == "Female" and 0 < int(page) < 25:
        if currentvisit.md == "ag":
            currentvisit.agmod += 3
        elif currentvisit.md == "dr":
            currentvisit.agmod += 0
        elif currentvisit.md == "po":
            currentvisit.agmod -= 3
        elif currentvisit.md == "lo":
            currentvisit.agmod -= 1
    elif curr_patient.gender == "Female" and 25 < int(page) < 65:
        if currentvisit.md == "ag":
            currentvisit.agmod += 2
        elif currentvisit.md == "dr":
            currentvisit.agmod += 2
        elif currentvisit.md == "po":
            currentvisit.agmod -= 2
        elif currentvisit.md == "lo":
            currentvisit.agmod -= 3
    elif curr_patient.gender == "Female" and 65 < int(page) < 100:
        if currentvisit.md == "ag":
            currentvisit.agmod += 3
        elif currentvisit.md == "dr":
            currentvisit.agmod -= 1
        elif currentvisit.md == "po":
            currentvisit.agmod -= 3
        elif currentvisit.md == "lo":
            currentvisit.agmod += 3

            

def nextquest(self):
    currentvisit.tpbonusmalus = 0
    currentvisit.currentmessage = currentvisit.savedoctorreply
    if currentvisit.tp == "fm":
        currentvisit.tpbonusmalus = (currentvisit.ct + currentvisit.cs + currentvisit.agmod)#questa formula è da rivedere, questa determina quanto sale o scende il topic, quindi cambiala, magari anche in base al topic
        curr_patient.family += (currentvisit.tpbonusmalus+currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        curr_reactions.define_reaction()
        self.updatetext()
        return currentvisit.tpbonusmalus
    elif currentvisit.tp == "wr":
        currentvisit.tpbonusmalus = (currentvisit.cs + currentvisit.ct + currentvisit.agmod)
        curr_patient.work += (currentvisit.tpbonusmalus+currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        curr_reactions.define_reaction()
        self.updatetext()
        return currentvisit.tpbonusmalus
    elif currentvisit.tp == "fr":
        currentvisit.tpbonusmalus = (currentvisit.cs + currentvisit.ct + currentvisit.agmod)
        curr_patient.friendship += (currentvisit.tpbonusmalus+currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        curr_reactions.define_reaction()
        self.updatetext()
        return currentvisit.tpbonusmalus
    elif currentvisit.tp == "lv":
        currentvisit.tpbonusmalus = (currentvisit.cs + currentvisit.ct + currentvisit.agmod)
        curr_patient.love += (currentvisit.tpbonusmalus+currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        curr_reactions.define_reaction()
        self.updatetext()
        return currentvisit.tpbonusmalus

###############STAGE 3###############################
###Funzione per controllare lo stato del paziente
def updatestatus(self):
    if curr_patient.stress > 10 and curr_patient.trust > 10:
        curr_patient.state = "AN"  # an angry
        currentvisit.currentmessage = (
            "##WARNING## The patient is mad at you now!\nCareful, if you don't calm him down, you might worsen his problems")
        self.updatetext()
    elif curr_patient.stress > 10 and curr_patient.trust < 0:
        curr_patient.state = "NV"  # nv nevrosis
        currentvisit.currentmessage = (
            "##WARNING## The patient is experiencing a nevrotic episode!\nCareful, the patient's ractions are now unpredictable, calm him down before you damage him")
        self.updatetext()
    elif curr_patient.stress < 0 and curr_patient.trust > 10:
        curr_patient.state = "TR"  # tr love transfer
        currentvisit.currentmessage = (
            "##WARNING## The patient is experiencing TRANSFER towards you!\nCareful, missunderstandings may lead to your patient not trusting you anynmore. Re-gain control of the visit")
        self.updatetext()
    elif curr_patient.stress < 0 and curr_patient.trust < 0:
        curr_patient.state = "AP"  # ap apathetic
        currentvisit.currentmessage = (
            "##WARNING## The patient is becoming apathetic!\nCareful, If you don't engage the patient again, you may never be able to help him")
        self.updatetext()
    else:
        curr_patient.state = ""
        self.checktopicstatus()

##############STAGE 4#########################
# fa finire la visita se i topic si sballano
def checktopicstatus(self):
    topicsforendsession = {curr_patient.family: "family", curr_patient.work: "job", curr_patient.love: "love and partners",
                           curr_patient.selfvalue: "selfvalue", curr_patient.study: "study",
                           curr_patient.friendship: "friends"}
    if curr_patient.family < -25 or curr_patient.work < -25 or curr_patient.study < -25 or curr_patient.friendship < -25 or curr_patient.selfvalue < -25 or curr_patient.love < -25:
        currentvisit.currentmessage = (
                    "###Good news doctor! You have untangled the issued of the patient on the topic of " + topicsforendsession.get(
                min(topicsforendsession)))
        self.updatetext()
        self.change_screen() #change_screen diventa la funzione che porta alla schermata di riepilogo visita // FINE VISITA
    elif curr_patient.family > 25 or curr_patient.work > 25 or curr_patient.study > 25 or curr_patient.friendship > 25 or curr_patient.selfvalue > 25 or curr_patient.love > 25:
        currentvisit.currentmessage = (
                    "###Bad news doctor! you have disappointed  the patient on the topic of " + topicsforendsession.get(
                max(topicsforendsession)) + ", and he won't be your patient anymore")
        self.updatetext()
        self.change_screen()  #change_screen diventa la funzione che porta alla schermata di riepilogo visita // FINE VISITA
    else:
        currentvisit.stage += 1
        self.tppatientresponse()


def themesadder(self):
    currentvisit.theme = ""
    # Aggiungi fine gioco anche sugli altri temi
    if currentvisit.tp == "fm" and curr_patient.family < -10: #and curr_patient.trust > 5: #remember to tweak the values
        currentvisit.theme = "I think now I can tell you. Well...I think my problems with family are becouse of my father"
        endvisit.reason = currentvisit.theme
        currentvisit.motivation = "You have helped this patient open up about his problems, congratulations doc\n This is your last visit with " + curr_patient.name
        self.endsession()#devo inserire questa funzione che termina la visita
    else:
        currentvisit.theme = ""
        self.describe_emotional_status()        

    def tppatientresponse(self):
        curr_patient.tpresponse = ""
        if currentvisit.tp == "fm":
            if -10 < curr_patient.family <= -5 or curr_patient.family <= -10:
                curr_patient.tpresponse = random.choice(vlowfamily) # + gentrauma() "Questa funzione andrà ad aggiungere o un "" oppure una frase in caso viene generato un pezzo per il trauma
                self.themesadder()
            elif -5 < curr_patient.family <= 0:
                curr_patient.tpresponse = random.choice(lowfamily)
                if curr_patient.trauma == "fm":                                 #questo parte
                    pass                                                        #aggiunge
                elif curr_patient.trauma == "lv":                               #le frasi che ti fanno capire
                    curr_patient.tpresponse += random.choice(lovetraumapos)     #dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                self.themesadder()
            elif 0 < curr_patient.family <= 5:
                curr_patient.tpresponse = random.choice(highfamily)
                if curr_patient.trauma == "fm":                                 #questo parte
                    pass                                                        #aggiunge
                elif curr_patient.trauma == "lv":                               #le frasi che ti fanno capire
                    curr_patient.tpresponse += random.choice(lovetraumaneg)     #dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                self.themesadder()
            elif 5 < curr_patient.family <= 10 or curr_patient.family >= 10:
                curr_patient.tpresponse = random.choice(vhighfamily)
                self.themesadder()
            else:
                self.themesadder()
        elif currentvisit.tp == "lv":
                if -10 < curr_patient.love <= -5 or curr_patient.love <= -10:
                    curr_patient.tpresponse = random.choice(vlowlove)
                    self.themesadder()
                elif -5 < curr_patient.love <= 0:
                    curr_patient.tpresponse = random.choice(lowlove)
                    if curr_patient.trauma == "lv":                             # questo parte
                        pass                                                    # aggiunge
                    elif curr_patient.trauma == "fm":                           # le frasi che ti fanno capire
                        curr_patient.tpresponse += random.choice(familytraumapos)      # dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                    self.themesadder()
                elif 0 < curr_patient.love <= 5:
                    curr_patient.tpresponse = random.choice(highlove)
                    if curr_patient.trauma == "lv":  # questo parte
                        pass  # aggiunge
                    elif curr_patient.trauma == "fm":  # le frasi che ti fanno capire
                        curr_patient.tpresponse += random.choice(
                            familytraumaneg)  # dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                    self.themesadder()
                elif 5 < curr_patient.love <= 10 or curr_patient.love >= 10:
                    curr_patient.tpresponse = random.choice(vhighlove)
                    self.themesadder()
                else:
                    self.themesadder()
        elif currentvisit.tp == "fr":
                if -10 < curr_patient.friendship <= -5 or curr_patient.friendship <= -10:
                    curr_patient.tpresponse = random.choice(vlowrelations)
                    self.themesadder()
                elif -5 < curr_patient.friendship <= 0:
                    curr_patient.tpresponse = random.choice(lorelations)
                    if curr_patient.trauma == "lv":                             # questo parte
                        pass                                                    # aggiunge
                    elif curr_patient.trauma == "fm":                           # le frasi che ti fanno capire
                        curr_patient.tpresponse += random.choice(familytraumapos)      # dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                    self.themesadder()
                elif 0 < curr_patient.friendship <= 5:
                    curr_patient.tpresponse = random.choice(highrelations)
                    if curr_patient.trauma == "lv":  # questo parte
                        pass  # aggiunge
                    elif curr_patient.trauma == "fm":  # le frasi che ti fanno capire
                        curr_patient.tpresponse += random.choice(
                            familytraumaneg)  # dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                    self.themesadder()
                elif 5 < curr_patient.friendship <= 10 or curr_patient.friendship >= 10:
                    curr_patient.tpresponse = random.choice(vhighrelations)
                    self.themesadder()
                else:
                    self.themesadder()
        elif currentvisit.tp == "wr":
                if -10 < curr_patient.work <= -5 or curr_patient.work <= -10:
                    curr_patient.tpresponse = random.choice(vlowsuccess)
                    self.themesadder()
                elif -5 < curr_patient.work <= 0:
                    curr_patient.tpresponse = random.choice(losuccess)
                    if curr_patient.trauma == "lv":                             # questo parte
                        pass                                                    # aggiunge
                    elif curr_patient.trauma == "fm":                           # le frasi che ti fanno capire
                        curr_patient.tpresponse += random.choice(familytraumapos)      # dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                    self.themesadder()
                elif 0 < curr_patient.work <= 5:
                    curr_patient.tpresponse = random.choice(highsuccess)
                    if curr_patient.trauma == "lv":  # questo parte
                        pass  # aggiunge
                    elif curr_patient.trauma == "fm":  # le frasi che ti fanno capire
                        curr_patient.tpresponse += random.choice(
                            familytraumaneg)  # dove sta il trauma(devo aggiungere gli ELIF anche per gli altri possibili traumi e poi inserirlo in ogni topic)
                    self.themesadder()
                elif 5 < curr_patient.work <= 10 or curr_patient.work >= 10:
                    curr_patient.tpresponse = random.choice(vhighsuccess)
                    self.themesadder()
                else:
                    self.themesadder()
                    



def describe_emotional_status(self):
    currentvisit.additional_status_message = ""
    if -5 < curr_patient.stress < 5:
        currentvisit.stress_stage = 1
    elif 5< curr_patient.stress < 10:
        currentvisit.stress_stage = 2
    elif  10 < curr_patient.stress < 15:
        currentvisit.stress_stage = 3
    if -5 < curr_patient.trust < 5:
        currentvisit.trust_stage = 1
    elif 5< curr_patient.trust < 10:
        currentvisit.trust_stage = 2
    elif  10 < curr_patient.trust < 15:
        currentvisit.trust_stage = 3
    self.generate_emotion_description()

def generate_emotion_description(self):
    global emotional_status_dictionary
    if currentvisit.stress_stage != currentvisit.old_stress_stage and currentvisit.trust_stage != currentvisit.old_trust_stage:
        currentvisit.additional_status_message = emotional_status_dictionary[1][currentvisit.stress_stage] + "and" + emotional_status_dictionary[2][currentvisit.trust_stage]
    elif currentvisit.stress_stage != currentvisit.old_stress_stage:
        currentvisit.additional_status_message = emotional_status_dictionary[1][currentvisit.stress_stage]
    elif currentvisit.trust_stage != currentvisit.old_trust_stage:
        currentvisit.additional_status_message = emotional_status_dictionary[2][currentvisit.trust_stage]
    else:
        currentvisit.additional_status_message = ""
    currentvisit.calculate_old_stresstrust_stage()
    self.patientreply()


# Funzione per la risposta del paziente, questa cura solo la parte relativa a come stress e trust sono cambiati in base alla risposta del paziente
def patientreply(self):
    if currentvisit.theme == "":
        if currentvisit.cs > 4 and currentvisit.ct < -4:
            currentvisit.currentmessage = (random.choice(highstress) + ", " + random.choice(lowtrust) + ", " + curr_patient.tpresponse) + currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
        elif currentvisit.cs < -4 and currentvisit.ct > 4:
            currentvisit.currentmessage = (random.choice(lowstress) + ", " + random.choice(hightrust) + ", " + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
        elif currentvisit.cs > 4 and currentvisit.ct > 4:
            currentvisit.currentmessage = (random.choice(highstress) + ", but, " + random.choice(hightrust) + ", " + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
        elif currentvisit.cs < -4 and currentvisit.ct < -4:
            currentvisit.currentmessage = (random.choice(lowstress) + ", but, " + random.choice(lowtrust) + ", " + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
        elif currentvisit.cs > 4:
            currentvisit.currentmessage = (
                        random.choice(highstress) + ", " + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
        elif currentvisit.cs < -4:
            currentvisit.currentmessage = (
                        random.choice(lowstress) + ", " + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
        elif currentvisit.ct > 4:
            currentvisit.currentmessage = (
                    random.choice(hightrust) + ", " + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            self.updatetext()
        elif currentvisit.ct < -4:
            currentvisit.currentmessage = (
                    random.choice(lowtrust) + ", " + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
        else:
            currentvisit.currentmessage = (random.choice(norm_reply) + "," + curr_patient.tpresponse)+ currentvisit.additional_status_message
            currentvisit.visittime += 1
            curr_reactions.assignreactions()
            self.updatetext()
    else:
        # in questo branch ci finisci se hai concluso la visita salvando il paziente
        currentvisit.currentmessage = (currentvisit.theme)
        self.updatetext()
        # insert function to end visit

""""""