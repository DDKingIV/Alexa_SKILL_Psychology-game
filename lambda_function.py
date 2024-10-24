import random
import logging
import os
import boto3

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

#import from the file containing all content 
import names

SKILL_NAME = 'become a psychologist'
ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)
sb = CustomSkillBuilder(persistence_adapter=dynamodb_adapter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


#####################################################################################################################################################################################################
##################################################################################LOGICA DEL GIOCO###################################################################################################
#####################################################################################################################################################################################################


# classe paziente
class patient:
    def __init__(self, name, gender, age, stress, state, trust, family, work, love, friendship, tpresponse):
        self.name = name
        self.gender = gender
        self.age = age
        self.stress = stress
        self.state = state
        self.trust = trust
        self.family = family
        self.work = work
        self.love = love
        self.friendship = friendship
        self.tpresponse = tpresponse


# classe per la visita in corso
class curr_visit():
    def __init__(self, stage, tp, md, cs, ct, tpold, currentmessage, agmod, choise, firstvisit, topicbonusmalus,
                 stressbonusmalus, trustbonusmalus, theme, motivation, changetopic, doc_reply, ending, last_interaction):
        self.stage = stage
        self.tp = tp
        self.md = md
        self.cs = cs
        self.ct = ct
        self.tpold = tpold
        self.currentmessage = currentmessage
        self.agmod = agmod
        self.choise = choise
        self.firstvisit = firstvisit
        self.topicbonusmalus = topicbonusmalus
        self.stressbonusmalus = stressbonusmalus
        self.trustbonusmalus = trustbonusmalus
        self.theme = theme
        self.motivation = motivation
        self.changetopic = changetopic
        self.doc_reply = doc_reply
        self.ending = ending
        self.last_interaction = last_interaction


# generatore pazienti
def genpatient():
    genders = ["Male","Female"]
    gender = random.choice(genders)
    if gender == "Male":
        nameslist = names.boys
    else:
        nameslist = names.girls
    name = random.choice(nameslist)
    age = random.randint(20, 70)
    stress = random.randint(-9, 9)
    state = ""
    trust = random.randint(-9, 9)
    family = random.randint(-9, 9)
    work = random.randint(-9, 9)
    love = random.randint(-9, 9)
    friendship = random.randint(-9, 9)
    tpresponse = ""
    return patient(name, gender, age, stress, state, trust, family, work, love, friendship, tpresponse)


###########################################################################################################
####################VARIABILI SETTATE 1 TIME ALL'INIZIO DI OGNI NUOVA VISITA###############################
###########################################################################################################
currentvisit = curr_visit(0, "fm", "ag", 0, 0, "", "", 0, "", True, 0, 0, 0, "", "", "", "", "","")
curr_patient = patient("", 0, 0, "", 0, 0, 0, 0, 0, 0, "")


###########################################################################################################
#########################################LOGICA DI GIOCO###################################################
###########################################################################################################

def startvisit():
    global last_interaction
    curr_topic = {curr_patient.family: "my family", curr_patient.work: "my job", curr_patient.love: "my partner",
                  curr_patient.friendship: "my friends"}
    topic = curr_topic.get(max(curr_topic))
    topicvalue = max(curr_patient.family, curr_patient.work, curr_patient.love, curr_patient.friendship)
    #set the old topic for the change of topic
    set_old_topic = {curr_patient.family: "fm", curr_patient.work: "wr", curr_patient.love: "lv",
                  curr_patient.friendship: "fr"}
    currentvisit.tpold = set_old_topic.get(max(set_old_topic))
    if (curr_patient.stress + curr_patient.trust) / 2 > 8 and topicvalue > 7:
        initialtopic = (disappointedhigh+random.choice(an) + ", " + topic + ". "+emotion_close)
        currentvisit.firstvisit = "false"
    elif (curr_patient.stress + curr_patient.trust) / 2 > 8 and topicvalue < 3:
        initialtopic = (disappointedlow+random.choice(ap) + ", " + topic+ ". "+emotion_close)
        currentvisit.firstvisit = "false"
    elif (curr_patient.stress + curr_patient.trust) / 2 < 3 and topicvalue > 7:
        initialtopic = (excitedlow+random.choice(nv) + ", " + topic+ ". "+emotion_close)
        currentvisit.firstvisit = "false"
    elif (curr_patient.stress + curr_patient.trust) / 2 < 3 and topicvalue < 3:
        initialtopic = (excitedhigh+random.choice(tr) + ", " + topic+ ". "+emotion_close)
        currentvisit.firstvisit = "false"
    else:
        initialtopic = (random.choice(norm) + ", " + topic+ ". ")
        currentvisit.firstvisit = "false"
    return initialtopic

def stress_piece():
    if curr_patient.stress >= 10:
        S_description = random.choice(highstressdesc)
    elif -10 <= curr_patient.stress < 10:
        S_description = random.choice(avgstressdesc)
    else:
        S_description = random.choice(lowstressdesc)
    return S_description

def trust_piece():
    if curr_patient.trust >= 10:
        T_description = random.choice(lowtrustdesc)
    elif -10 <= curr_patient.trust < 10:
        T_description = random.choice(avgtrustdesc)
    else:
        T_description = random.choice(hightrustsdesc)
    return T_description

def congiunzione():
    if curr_patient.stress > 5 and curr_patient.trust > 5:
        conjun = random.choice(congiunzioni)
    elif curr_patient.stress < -5 and curr_patient.trust < -5:
        conjun = random.choice(vsprep)
    else:
        conjun = random.choice(congiunzioni)
    return conjun

def calc_additional_stress_level():
    if -15<= curr_patient.stress < -10 or curr_patient.stress < -15:
        return -3
    elif -10 <= curr_patient.stress <-1:
        return -2
    elif -1 <= curr_patient.stress < 0:
        return -1
    elif 0 <= curr_patient.stress < 1:
        return 1
    elif 1 <= curr_patient.stress < 10:
        return 2
    elif 10 <= curr_patient.stress <=15 or curr_patient.stress> 15:
        return 3

def calc_additional_trust_level():
    if -15<= curr_patient.trust < -10 or curr_patient.trust < -15:
        return -3
    elif -10 <= curr_patient.trust <-1:
        return -2
    elif -1 <= curr_patient.trust < 0:
        return -1
    elif 0 <= curr_patient.trust < 1:
        return 1
    elif 1 <= curr_patient.trust < 10:
        return 2
    elif 10 <= curr_patient.trust <=15 or curr_patient.trust > 15:
        return 3

def calc_accellerator_distance():
    distance = abs(curr_patient.stress - curr_patient.trust)
    if 0 <= distance < 5:
        return 2
    elif 5 <= distance < 15:
        return 3
    elif 15 <= distance < 25:
        return 4
    elif distance >= 25:
        return 5

def opening():
    global curr_patient
    curr_patient = genpatient()
    openingphrase = (
            "Ok, here is your new patient. " + "\nName " + curr_patient.name + ", It's a " + curr_patient.gender + ", " + str(curr_patient.age) + " years old, " + stress_piece() + congiunzione() +" "+ trust_piece() + ". The patients greets you and says: " + startvisit())
    currentvisit.last_interaction = openingphrase
    return openingphrase


def START_calculate_stresstrust_changes(approach):
    currentvisit.currentmessage = ""  # reset the phrase at beginning of each round
    additional_stress  = calc_additional_stress_level()
    additional_trust = calc_additional_trust_level()
    accellerator_distance = calc_accellerator_distance()
    currentvisit.cs = 0
    currentvisit.ct = 0
    if approach == "ag":
        currentvisit.cs += (accellerator_distance + additional_stress + random.randint(1,3)+currentvisit.stage)
        currentvisit.ct -= (accellerator_distance + additional_trust + random.randint(1,3)+currentvisit.stage)
        currentvisit.choise = random.choice(aggre)
    elif approach == "lo":
        currentvisit.cs -= (accellerator_distance + additional_stress + random.randint(1,3)+currentvisit.stage)
        currentvisit.ct -= (accellerator_distance + additional_trust + random.randint(1,3)+currentvisit.stage)
        currentvisit.choise = random.choice(logic)
    elif approach == "dr":
        currentvisit.cs += (accellerator_distance + additional_stress + random.randint(1,3)+currentvisit.stage)
        currentvisit.ct += (accellerator_distance + additional_trust + random.randint(1,3)+currentvisit.stage)
        currentvisit.choise = random.choice(direc)
    elif approach == "po":
        currentvisit.cs -= (accellerator_distance + additional_stress + random.randint(1,3)+currentvisit.stage)
        currentvisit.ct += (accellerator_distance + additional_trust + random.randint(1,3)+currentvisit.stage)
        currentvisit.choise = random.choice(posit)
    topicchange()


def topicchange():
    currentvisit.changetopic = ""
    if currentvisit.firstvisit:
        currentvisit.firstvisit = False
    elif currentvisit.tpold != currentvisit.tp:
        currentvisit.changetopic = "Ok, but now I would like to talk about something else"
        currentvisit.tpold = currentvisit.tp
    else:
        currentvisit.tpold = currentvisit.tp
    agegendermod()


# funzione per aggiungere modifiers per età e sesso del paziente
def agegendermod():
    currentvisit.agmod = 0
    page = curr_patient.age
    if curr_patient.gender == "Male" and 0 <= page <= 25:
        if currentvisit.md == "ag":
            currentvisit.agmod = -3
        elif currentvisit.md == "dr":
            currentvisit.agmod = -2
        elif currentvisit.md == "po":
            currentvisit.agmod = 0
        elif currentvisit.md == "lo":
            currentvisit.agmod = 1
    elif curr_patient.gender == "Male" and 25 < page <= 65:
        if currentvisit.md == "ag":
            currentvisit.agmod = -1
        elif currentvisit.md == "dr":
            currentvisit.agmod = 3
        elif currentvisit.md == "po":
            currentvisit.agmod = -1
        elif currentvisit.md == "lo":
            currentvisit.agmod = -3
    elif curr_patient.gender == "Male" and 65 < page <= 100:
        if currentvisit.md == "ag":
            currentvisit.agmod = 3
        elif currentvisit.md == "dr":
            currentvisit.agmod = 3
        elif currentvisit.md == "po":
            currentvisit.agmod = -3
        elif currentvisit.md == "lo":
            currentvisit.agmod = 2
    elif curr_patient.gender == "Female" and 0 <= page <= 25:
        if currentvisit.md == "ag":
            currentvisit.agmod = 3
        elif currentvisit.md == "dr":
            currentvisit.agmod = 0
        elif currentvisit.md == "po":
            currentvisit.agmod = -3
        elif currentvisit.md == "lo":
            currentvisit.agmod = -1
    elif curr_patient.gender == "Female" and 25 < page <= 65:
        if currentvisit.md == "ag":
            currentvisit.agmod = 2
        elif currentvisit.md == "dr":
            currentvisit.agmod = 2
        elif currentvisit.md == "po":
            currentvisit.agmod = -2
        elif currentvisit.md == "lo":
            currentvisit.agmod = -3
    elif curr_patient.gender == "Female" and 65 < page<= 100:
        if currentvisit.md == "ag":
            currentvisit.agmod = 3
        elif currentvisit.md == "dr":
            currentvisit.agmod = -1
        elif currentvisit.md == "po":
            currentvisit.agmod = -3
        elif currentvisit.md == "lo":
            currentvisit.agmod = 3
    #add stage level to increase visit velocity based on how many times you talked to patient
    if currentvisit.agmod <= 0:
        currentvisit.agmod -= currentvisit.stage
    else:
        currentvisit.agmod += currentvisit.stage
    new_values_StressTrustTopic()


def new_values_StressTrustTopic():
    currentvisit.doc_reply = ""
    currentvisit.tpbonusmalus = 0
    if currentvisit.tp == "fm":
        currentvisit.tpbonusmalus = (currentvisit.ct + currentvisit.cs + currentvisit.agmod)  
        curr_patient.family += (currentvisit.tpbonusmalus + currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        currentvisit.doc_reply = (currentvisit.choise + ", " + random.choice(famy))
    elif currentvisit.tp == "wr":
        currentvisit.tpbonusmalus = (currentvisit.cs + currentvisit.ct + currentvisit.agmod)
        curr_patient.work += (currentvisit.tpbonusmalus + currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        currentvisit.doc_reply = (currentvisit.choise + ", " + random.choice(worki))
    elif currentvisit.tp == "fr":
        currentvisit.tpbonusmalus = (currentvisit.cs + currentvisit.ct + currentvisit.agmod)
        curr_patient.friendship += (currentvisit.tpbonusmalus + currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        currentvisit.doc_reply = (currentvisit.choise + ", " + random.choice(friends))
    elif currentvisit.tp == "lv":
        currentvisit.tpbonusmalus = (currentvisit.cs + currentvisit.ct + currentvisit.agmod)
        curr_patient.love += (currentvisit.tpbonusmalus + currentvisit.topicbonusmalus)
        curr_patient.stress += currentvisit.cs
        curr_patient.trust += currentvisit.ct
        currentvisit.doc_reply = (currentvisit.choise + ", " + random.choice(loves))
    checktopicstatus()


# fa finire la visita se i topic si sballano
def checktopicstatus():
    currentvisit.motivation = ""
    topicsforendsession = {curr_patient.family: "family", curr_patient.work: "job",
                           curr_patient.love: "love and partners",
                           curr_patient.friendship: "friends"}
    if curr_patient.family < -18 or curr_patient.work < -18 or curr_patient.friendship < -18 or curr_patient.love < -18:
        currentvisit.motivation = excitedhigh + random.choice(endingquotes[currentvisit.tp][1]) + emotion_close
        currentvisit.ending = "po"
    elif curr_patient.family > 18 or curr_patient.work > 18 or curr_patient.friendship > 18 or curr_patient.love > 18:
        currentvisit.motivation = disappointedhigh + random.choice(endingquotes[currentvisit.tp][2]) + emotion_close
        currentvisit.ending = "ng"
    else:
        currentvisit.motivation = ""
        currentvisit.ending = ""
    themesadder()


def themesadder():
    currentvisit.theme = ""
    if currentvisit.motivation != "":
        currentvisit.theme = "" + currentvisit.motivation
    else:
        # FIDUCIA ALTA ma topics non molto alti, semplicemente il paziente dice di sentirsi meglio
        # STRESS ALTO ma topics non molto male, semplicemente il paziente si scoccia di te
        if curr_patient.stress >= 15:
            currentvisit.theme = disappointedhigh + random.choice(toostress) + emotion_close +"; " + currentvisit.motivation + ". You have stressed the patient out. "
            currentvisit.ending = "ng"
        elif curr_patient.trust <= -15:
            currentvisit.theme = disappointedhigh + random.choice(notrust)+ emotion_close +"; " + currentvisit.motivation + ". You have lost your patient's trust. "
            currentvisit.ending = "ng"
        elif curr_patient.trust >= 15:
            currentvisit.theme = excitedhigh + random.choice(muchtrust) + emotion_close +"; " + currentvisit.motivation + ". The patient is more confident now, but won't be aware of the traumas causing the problems. "
            currentvisit.ending = "ng"
        elif curr_patient.stress <= -15:
            currentvisit.theme = excitedhigh + random.choice(nostress)+ emotion_close + "; " +currentvisit.motivation + ". The patient is calm now, but you didn't bring out the trauma causing the problems. "
            currentvisit.ending = "ng"
        else:
            currentvisit.theme = "" + currentvisit.motivation
    tppatientresponse()


def tppatientresponse():
    curr_patient.tpresponse = ""
    if currentvisit.tp == "fm":
        if -10 < curr_patient.family <= -5 or curr_patient.family <= -10:
            curr_patient.tpresponse = excitedhigh+random.choice(vlowfamily)+emotion_close
        elif -5 < curr_patient.family <= 0:
            curr_patient.tpresponse = excitedmedium+random.choice(lowfamily)+emotion_close
        elif 0 < curr_patient.family <= 5:
            curr_patient.tpresponse = disappointedmedium+random.choice(highfamily)+emotion_close
        elif 5 < curr_patient.family <= 10 or curr_patient.family >= 10:
            curr_patient.tpresponse = disappointedhigh+random.choice(vhighfamily)+emotion_close
    elif currentvisit.tp == "lv":
        if -10 < curr_patient.love <= -5 or curr_patient.love <= -10:
            curr_patient.tpresponse = excitedhigh+random.choice(vlowlove)+emotion_close
        elif -5 < curr_patient.love <= 0:
            curr_patient.tpresponse = excitedmedium+random.choice(lowlove)+emotion_close
        elif 0 < curr_patient.love <= 5:
            curr_patient.tpresponse = disappointedmedium+random.choice(highlove)+emotion_close
        elif 5 < curr_patient.love <= 10 or curr_patient.love >= 10:
            curr_patient.tpresponse = disappointedhigh+random.choice(vhighlove)+emotion_close
    elif currentvisit.tp == "fr":
        if -10 < curr_patient.friendship <= -5 or curr_patient.friendship <= -10:
            curr_patient.tpresponse = excitedhigh+random.choice(vlowrelations)+emotion_close
        elif -5 < curr_patient.friendship <= 0:
            curr_patient.tpresponse = excitedmedium+random.choice(lorelations)+emotion_close
        elif 0 < curr_patient.friendship <= 5:
            curr_patient.tpresponse = disappointedmedium+random.choice(highrelations)+emotion_close
        elif 5 < curr_patient.friendship <= 10 or curr_patient.friendship >= 10:
            curr_patient.tpresponse = disappointedhigh+ random.choice(vhighrelations)+emotion_close
    elif currentvisit.tp == "wr":
        if -10 < curr_patient.work <= -5 or curr_patient.work <= -10:
            curr_patient.tpresponse = excitedhigh+ random.choice(vlowsuccess)+emotion_close
        elif -5 < curr_patient.work <= 0:
            curr_patient.tpresponse = excitedmedium+random.choice(losuccess)+emotion_close
        elif 0 < curr_patient.work <= 5:
            curr_patient.tpresponse = disappointedmedium+random.choice(highsuccess)+emotion_close
        elif 5 < curr_patient.work <= 10 or curr_patient.work >= 10:
            curr_patient.tpresponse = disappointedhigh+random.choice(vhighsuccess)+emotion_close
    patientreply()


# Funzione per la risposta del paziente, questa cura solo la parte relativa a come stress e trust sono cambiati in base alla risposta del paziente
#consider adding a variable that sends the trust/stress description out only if the level is changed compared to last time
def patientreply():
    if -15 < curr_patient.stress < -5 or curr_patient.stress <= -15:
        stress_description = excitedmedium + random.choice(lowstress) + emotion_close
        slevel = 1
    elif -5 <= curr_patient.stress <= 5:
        stress_description = disappointedlow + random.choice(avgstress) + emotion_close
        slevel = 2
    elif 5 < curr_patient.stress < 15 or curr_patient.stress >= 15:
        stress_description = disappointedhigh + random.choice(highstress) + emotion_close
        slevel = 3
    if -15 < curr_patient.trust < -5 or curr_patient.trust <= -15:
        trust_description = disappointedlow + random.choice(lowtrust) + emotion_close
        tlevel = 1
    elif -5 <= curr_patient.trust < 5:
        trust_description = excitedlow + random.choice(avgtrust) + emotion_close
        tlevel = 2
    elif 5 <= curr_patient.trust < 15 or curr_patient.trust >= 15:
        trust_description = excitedhigh + random.choice(hightrust) + emotion_close
        tlevel = 3
    create_final_repy(stress_description,trust_description,slevel,tlevel)
    
def create_final_repy(stress_description,trust_description,slev,tlev):
    if slev == 1 and tlev == 1:
        final_reply = random.choice(thedocreplyes)+ " " + currentvisit.changetopic + ", " + currentvisit.doc_reply + ". "+ random.choice(thepatientsays)+ " " + stress_description + random.choice(vsprep) +" " + trust_description + ", " + curr_patient.tpresponse
        currentvisit.currentmessage = final_reply
    elif slev == 3 and tlev == 3:
        final_reply = random.choice(thedocreplyes)+ " " + currentvisit.changetopic + ", " + currentvisit.doc_reply + ". "+ random.choice(thepatientsays)+ " " + stress_description + random.choice(vsprep) +" " + trust_description + ", " + curr_patient.tpresponse
        currentvisit.currentmessage = final_reply
    elif slev == 1 and tlev == 2:
        final_reply = random.choice(thedocreplyes)+ " " + currentvisit.changetopic + ", " + currentvisit.doc_reply + ". "+ random.choice(thepatientsays)+ " " + stress_description + random.choice(congiunzioni) +" " + trust_description + ", " + curr_patient.tpresponse
        currentvisit.currentmessage = final_reply
    elif slev == 2 and tlev == 1:
        final_reply = random.choice(thedocreplyes)+ " " + currentvisit.changetopic + ", " + currentvisit.doc_reply + ". "+ random.choice(thepatientsays)+ " " + stress_description + random.choice(congiunzioni) +" " + trust_description + ", " + curr_patient.tpresponse
        currentvisit.currentmessage = final_reply
    elif slev == 3 and tlev == 2:
        final_reply = random.choice(thedocreplyes)+ " " + currentvisit.changetopic + ", " + currentvisit.doc_reply + ". "+ random.choice(thepatientsays)+ " " + stress_description + random.choice(vsprep) +" " + trust_description + ", " + curr_patient.tpresponse
        currentvisit.currentmessage = final_reply
    elif slev == 2 and tlev == 3:
        final_reply = random.choice(thedocreplyes)+ " " + currentvisit.changetopic + ", " + currentvisit.doc_reply + ". "+ random.choice(thepatientsays)+ " " + stress_description + random.choice(vsprep) +" " + trust_description + ", " + curr_patient.tpresponse
        currentvisit.currentmessage = final_reply
    else:
        final_reply = random.choice(thedocreplyes)+ " " + currentvisit.changetopic + ", " + currentvisit.doc_reply + ". "+ random.choice(thepatientsays)+ " " + stress_description + ", " + trust_description + ", " + curr_patient.tpresponse
        currentvisit.currentmessage = final_reply
    currentvisit.last_interaction = final_reply


#####################################################################################################################################################################################################
##################################################################################LOGICA DI ALEXA###################################################################################################
#####################################################################################################################################################################################################


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch.

            Get the persistence attributes, to figure out the game state.
            """
    
    # type: (HandlerInput) -> Response
    attr = handler_input.attributes_manager.persistent_attributes
    
    if not attr:
        attr['cured_patients'] = 0
        attr['saved_patients'] = 0
        attr['lost_patients'] = 0
        attr['game_state'] = 'ENDED'
        attr['currently_visiting'] = "firsttime"
        

    attr['game_state'] = 'ENDED'  # DEVI RESETTARE LO STATO AD OGNI LANCIO DEL GIOCO SENNO' SBALLI GLI STATES
    handler_input.attributes_manager.session_attributes = attr
    handler_input.attributes_manager.save_persistent_attributes()

    if attr['currently_visiting'] == "firsttime":
        speech_text = opening_message
        reprompt = "Say yes to start a session or no to quit."
        attr['currently_visiting'] = "notfirsttime"
    elif attr['currently_visiting'] == "patientinprogress":
        # load persistent attributed of the patient from dynamodb
        curr_patient.name = attr['patient_save_slot'][0]
        curr_patient.gender = attr['patient_save_slot'][1]
        curr_patient.age = attr['patient_save_slot'][2]
        curr_patient.stress = attr['patient_save_slot'][3]
        curr_patient.state = attr['patient_save_slot'][4]
        curr_patient.trust = attr['patient_save_slot'][5]
        curr_patient.family = attr['patient_save_slot'][6]
        curr_patient.work = attr['patient_save_slot'][7]
        curr_patient.love = attr['patient_save_slot'][8]
        curr_patient.friendship = attr['patient_save_slot'][9]
        curr_patient.tpresponse = attr['patient_save_slot'][10]
        currentvisit.tpold = attr['patient_save_slot'][11]
        #a new attribute was added later after go live, I need this code to create the new attribute for returning players
        if len(attr['patient_save_slot'])<13:
            attr['patient_save_slot'] += "n"
        else:
            currentvisit.last_interaction = attr['patient_save_slot'][12]

        speech_text = "you were visiting a patient named {}, Would you like to continue your visit?".format(
            curr_patient.name)
        reprompt = "Say yes to continue the visit or no to close the game"
    else:
        #a new attribute was added later after go live, I need this code to create the new attribute for returning players
        if len(attr['patient_save_slot'])<13:
            attr['patient_save_slot'] += "n"
        speech_text = "Welcome back to your office doctor. You have visited {} patients. Saved {} patiens and lost {} patiens. Would you like to visit another patient?".format(attr['cured_patients'],attr['saved_patients'],attr['lost_patients'])
        reprompt = "Say yes to continue the visit or no to close the game"

    handler_input.attributes_manager.session_attributes = attr
    handler_input.attributes_manager.save_persistent_attributes()

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    
    #Quick check to have the correct reprompt based on if the player is visiting or not
    if ("game_state" in session_attr and
            session_attr["game_state"] == "STARTED"):
        For_repromt = "Choose a topic between family, friends, work or love and an approach between aggressive, logic, direct or positive. For example you can say: family aggressive or work logic. You can also say repeat to listen to the last interaction with your patient."
    else:
        For_repromt = "Say yes to begin a new visit or no to end the game"
        
    speech_text = (help_message + ". "+  For_repromt)
    reprompt = For_repromt

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda input:
    is_intent_name("AMAZON.CancelIntent")(input) or
    is_intent_name("AMAZON.StopIntent")(input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye doctor! Don't stay away for long, your patients need you! To come back, just say Alexa open become a psychologist "

    handler_input.response_builder.speak(
        speech_text).set_should_end_session(True)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    logger.info(
        "Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
    return handler_input.response_builder.response


def currently_playing(handler_input):
    """Function that acts as can handle for game state."""
    # type: (HandlerInput) -> bool
    is_currently_playing = False
    session_attr = handler_input.attributes_manager.session_attributes

    if ("game_state" in session_attr
            and session_attr['game_state'] == "STARTED"):
        is_currently_playing = True

    return is_currently_playing


@sb.request_handler(can_handle_func=lambda input:
not currently_playing(input) and
is_intent_name("AMAZON.YesIntent")(input))
def yes_handler(handler_input):
    """Handler for Yes Intent, only if the player said yes for
            a new game.
            """
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    session_attr['game_state'] = "STARTED"
    
    if currentvisit.tpold == "fm":
        topic_for_phrase = "family"
    elif currentvisit.tpold == "fr":
        topic_for_phrase = "friends"
    elif currentvisit.tpold == "lv":
        topic_for_phrase = "love"
    else:
        topic_for_phrase = "work"
    
    if session_attr['currently_visiting'] == "patientinprogress":
        speech_text = "ok last time you were talking about {}, choose topic and approach".format(topic_for_phrase)
        reprompt = "Choose topic and approach for your reply, or say 'repeat' to hear again the last interaction."
    else:
        speech_text = opening()
        currentvisit.stage = 0
        reprompt = "Choose topic and approach for your reply or say 'repeat' to hear again"

    session_attr['patient_save_slot'] = [curr_patient.name, curr_patient.gender, curr_patient.age, curr_patient.stress,
                                         curr_patient.state, curr_patient.trust,
                                         curr_patient.family, curr_patient.work, curr_patient.love,
                                         curr_patient.friendship, curr_patient.tpresponse, currentvisit.tp, currentvisit.last_interaction]
    session_attr['currently_visiting'] = "patientinprogress"

    handler_input.attributes_manager.persistent_attributes = session_attr
    handler_input.attributes_manager.save_persistent_attributes()

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
not currently_playing(input) and
is_intent_name("AMAZON.NoIntent")(input))
def no_handler(handler_input):
    """Handler for No Intent, only if the player said no for
            a new game.
            """
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    session_attr['game_state'] = "ENDED"

    handler_input.attributes_manager.persistent_attributes = session_attr
    handler_input.attributes_manager.save_persistent_attributes()

    speech_text = "Goodbye doctor! Don't stay away for long, your patients need you! To come back, just say Alexa open become a psychologist "

    handler_input.response_builder.speak(speech_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
currently_playing(input) and
is_intent_name("topic_approach")(input))
def number_guess_handler(handler_input):
    # Handler for processing approach and topic choosen by player.
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    # Getting the slots ID from the intent
    topic_intent = handler_input.request_envelope.request.intent.slots[
        "topic"].resolutions.resolutions_per_authority[0].values[0].value.id

    approach_intent = handler_input.request_envelope.request.intent.slots[
        "approach"].resolutions.resolutions_per_authority[0].values[0].value.id

    currentvisit.md = approach_intent
    currentvisit.tp = topic_intent
    START_calculate_stresstrust_changes(approach_intent)

    if currentvisit.theme == "":  # quando la visita non è ancora conclusa quindi non c'è un tema
        speech_text = currentvisit.currentmessage
        reprompt = "Choose the topic and approach for your reply to the patient or say 'repeat' to listen again"
        #this next parameter determines how fast the visit will be
        currentvisit.stage += 1
        session_attr['currently_visiting'] = "patientinprogress"
        session_attr['patient_save_slot'] = [curr_patient.name, curr_patient.gender, curr_patient.age,
                                             curr_patient.stress,
                                             curr_patient.state, curr_patient.trust,
                                             curr_patient.family, curr_patient.work, curr_patient.love,
                                             curr_patient.friendship, curr_patient.tpresponse, currentvisit.tp, currentvisit.last_interaction]
    else:
        speech_text = "The patient stops you and tells you: "+currentvisit.theme + ". Ok so the patient has left your office, would you like to visit a new patient?"
        reprompt = "Want to try a new patient?"
        ######set attributes#####
        session_attr['game_state'] = "ENDED"
        session_attr['currently_visiting'] = "notfirsttime"
        session_attr['cured_patients'] += 1
        session_attr['patient_save_slot'] = ["", "", 0, 0, "", 0, 0, 0, 0, 0, "","",""]
        #assign correct score
        if currentvisit.ending == "po":
            session_attr['saved_patients'] += 1
        elif currentvisit.ending == "ng":
            session_attr['lost_patients'] += 1
        else:
            pass


    handler_input.attributes_manager.persistent_attributes = session_attr
    handler_input.attributes_manager.save_persistent_attributes()

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
is_intent_name("AMAZON.FallbackIntent")(input) or
is_intent_name("AMAZON.YesIntent")(input) or
is_intent_name("AMAZON.NoIntent")(input))
def fallback_handler(handler_input):
    # AMAZON.FallbackIntent is only available in en-US locale.
    # This handler will not be triggered except in that locale,
    # so it is safe to deploy on any locale.

    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes

    if ("game_state" in session_attr and
            session_attr["game_state"] == "STARTED"):
        speech_text = (
            "Choose a topic between family, friends, work and love and an approach between logic, direct, aggressive and positive. For example you can say: family aggressive.")
        reprompt = "Choose approach and topic!"
    else:
        speech_text = (help_message)
        reprompt = "Say yes to start the visit or no to quit."
        
    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.RepeatIntent"))
def help_intent_handler(handler_input):
    """Handler for repeat Intent."""
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    
    repeat = session_attr['patient_save_slot'][12]
    
    #Quick check to have the correct reprompt based on if the player is visiting or not
    if ("game_state" in session_attr and
            session_attr["game_state"] == "STARTED"):
        speech_text = "You last interaction was: " + repeat + ". ok, now choose topic and approach for your reply!"
        For_repromt = "Choose a topic between family, friends, work or love and an approach between aggressive, logic, direct or positive. For example you can say: family aggressive."
    else:
        speech_text = "you are not currently visiting a patient, say yes to begin a new visit or no to end the game"
        For_repromt = "Say yes to begin a new visit or no to end the game"
        
    reprompt = For_repromt

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=lambda input: True)
def unhandled_intent_handler(handler_input):
    """Handler for all other unhandled requests."""
    # type: (HandlerInput) -> Response
    speech = "Say yes to continue or no to end the game!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
            respond with custom message.
            """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)
    speech = "Sorry, I can't understand that. Please say again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Response logger."""
    # type: (HandlerInput, Response) -> None
    logger.info("Response: {}".format(response))


lambda_handler = sb.lambda_handler()


#############################################CONTENT FOR THE PHRASE GENERATION#####################################################################
####liste delle frasi iniziali per introdurre la visita:
norm = names.norm
an = names.an
nv = names.nv
tr = names.tr
ap = names.ap
# liste per le risposte del dottore
aggre = names.aggre
logic = names.logic
posit = names.posit
direc = names.direc

famy = names.famy
worki = names.worki
friends = names.friends
loves = names.loves

# liste per lo status dei topic del paziente

vlowfamily = names.vlowfamily
lowfamily = names.lowfamily
highfamily = names.highfamily
vhighfamily = names.vhighfamily

vlowlove = names.vlowlove
lowlove = names.lowlove
highlove = names.highlove
vhighlove = names.vhighlove

vlowsuccess = names.vlowsuccess
losuccess = names.losuccess
highsuccess = names.highsuccess
vhighsuccess = names.vhighsuccess

vlowrelations = names.vlowrelations
lorelations = names.lorelations
highrelations = names.highrelations
vhighrelations = names.vhighrelations

# risposte del paziente(questa parte ti informa su come è andata la tua risposta corrente
highstress = names.highstress
lowstress = names.lowstress
hightrust = names.hightrust
lowtrust = names.lowtrust
avgtrust = names.avgtrust
avgstress = names.avgstress


# DIZIONARIO per le frasi di conclusione quando sballano i topic
endingquotes = names.endingquotes

#frasi per conclusione GIOCO
toostress = names.toostress
notrust = names.notrust
muchtrust = names.muchtrust
nostress = names.nostress

#tags per le emozioni
excitedlow = "<amazon:emotion name='excited' intensity='low'>"
excitedmedium= "<amazon:emotion name='excited' intensity='medium'>"
excitedhigh= "<amazon:emotion name='excited' intensity='high'>"

disappointedlow= "<amazon:emotion name='disappointed' intensity='low'>"
disappointedmedium="<amazon:emotion name='disappointed' intensity='medium'>"
disappointedhigh="<amazon:emotion name='disappointed' intensity='high'>"

emotion_close = "</amazon:emotion>"

#descriptions for opening
highstressdesc = names.highstressdesc
avgstressdesc = names.avgstressdesc
lowstressdesc = names.lowstressdesc

hightrustsdesc = names.hightrustsdesc
avgtrustdesc = names.avgtrustdesc
lowtrustdesc = names.lowtrustdesc

#intermezzi
thedocreplyes = names.thedocreplyes
thepatientsays = names.thepatientsays
vsprep = names.vsprep
congiunzioni = names.congiunzioni

#Standard messages
opening_message = names.opening_message
help_message = names.help_message

#########################################################################################################################################