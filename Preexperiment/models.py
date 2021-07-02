from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import datetime
from django import forms #for multiplechoice questions

author = 'RS'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'beispiel'
    players_per_group = None
    num_rounds = 1

    lottery_payout = ["$0.75", "$1.50", "$0.00"] # used in the html table template
    lottery_gamble_successrate = [(85 - i) for i in range(0,75, 5)] #[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
    lottery_gamble_failurerate = [(15 + i) for i in range(0,75, 5)]

     #lottery payment
    lottery_success = 1.50
    lottery_failure = 0.00
    lottery_safe = 0.75

    alternative1_boni = 2.90 #first subsequent decision (termination)
    alternative1_boni_control = 3.00
    success_boni = 3.50 #second subsequent decision (continuation, twice)
    failure_boni = 1.50
    alternative2_boni = 2.40 #second subsequent decision (continuation then termination)
    alternative2_boni_control = 2.45
    failure_award = 0.10 #50% for termination at 2nd subsequent decision (see pages.py)

class Subsession(BaseSubsession):
    framing = models.StringField() # A1/A2/A3/C0

    def creating_session(self): #automatically executed when session is generated
        if self.session.config["name"] == "A1": #see dict in settings.py
            self.framing = "A1"
        elif self.session.config["name"] == "A2":
            self.framing = "A2"
        elif self.session.config["name"] == "A3":
            self.framing = "A3"
        elif self.session.config["name"] == "C0":
            self.framing = "C0"
        else:
            print("treatment not found")

class Group(BaseGroup):
    pass

def quiz(q, choiceslist):
    return models.IntegerField(verbose_name = q,choices=choiceslist,widget=widgets.RadioSelect) #choiceslist = [[1, "abc"], [2, "def"], ...]

def create_peq(labelinput):
    return models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label=labelinput)

def create_mc(mc,choiceslist): #same as quiz function
    return models.IntegerField(verbose_name = mc,choices=choiceslist,widget=widgets.RadioSelect)

class Player(BasePlayer):
    # total_fails = models.IntegerField(initial=0)
    failed_at = models.StringField() #to track at which page participant failed
    attention_failed = models.StringField()
    lottery_choice = models.PositiveIntegerField(choices=[[i, f"Scenario {i}"] for i in range(1,17)], widget=widgets.RadioSelect) #Lottery page; 17 is exclusive

    #mop vs vacuum
    initial_choices = models.StringField() # records all button clicks on the two initial options of a participant
    initial_decision = models.StringField() # final initial decision

    #first sub decision 0 100 slider
    sub_decision = models.IntegerField(label="", min=0, max=100, widget=widgets.Slider(attrs={'step': '1'}, show_value=True)) # from 0 (termination) to 100 (continuation)
    slider_inputs = models.StringField() #store all slider inputs after mouse-release
    #first sub decision conti/termi decision
    sub1_choices = models.StringField() # records all button clicks on the first sub decision of a participant
    sub1_decision = models.StringField() # final sub1 decision
    sub1_consistency = models.StringField()

    #second sub decision 0 100 slider
    sub_decision2 = models.IntegerField(label="", min=0, max=100, widget=widgets.Slider(attrs={'step': '1'}, show_value=True)) # from 0 (termination) to 100 (continuation)
    slider_inputs2 = models.StringField() #store all slider inputs after mouse-release
    #second sub decision conti/termi decision
    sub2_choices = models.StringField()
    sub2_decision = models.StringField()
    sub2_consistency = models.StringField()

    quiz_totalwronganswers = models.IntegerField(initial=0) #increases, as long as atleast one answers is incorrect when page is submitted

    #timespent
    timespent_mainpart = models.IntegerField() #get total time spent
    timespent_lottery = models.IntegerField()
    timespent_failureaward = models.IntegerField()
    timespent_peq = models.IntegerField()
    timespent_instructions = models.IntegerField()
    timespent_total = models.IntegerField()
    timespent_initialdecision = models.IntegerField()
    timespent_projectupdate = models.IntegerField()

    def get_time(self, start_or_end): #specify pages.py, eg: before_next_page(self): self.player.get_time("end_mainpart")
        if start_or_end == "start_mainpart":
            self.start_mainpart = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_mainpart":
            self.end_mainpart = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            difference = datetime.datetime.strptime(self.end_mainpart, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_mainpart, "%d/%m/%Y %H:%M:%S")
            self.timespent_mainpart = int(difference.total_seconds())
            # self.timespent_mainpart = f"{float(duration):.0f}" #in minutes; for seconds: f"{duration:.0f}sec; {float(duration / 60):.2f}min"
        elif start_or_end == "start_peq":
            self.start_peq = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_peq":
            self.end_peq = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            difference = datetime.datetime.strptime(self.end_peq, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_peq, "%d/%m/%Y %H:%M:%S")
            self.timespent_peq = int(difference.total_seconds()) 
        elif start_or_end == "start_lottery":
            self.start_lottery = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_lottery":
            self.end_lottery = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            difference = datetime.datetime.strptime(self.end_lottery, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_lottery, "%d/%m/%Y %H:%M:%S")
            self.timespent_lottery = int(difference.total_seconds())
        elif start_or_end == "start_failureaward":
            self.start_failureaward = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_failureaward":
            self.end_failureaward = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            difference = datetime.datetime.strptime(self.end_failureaward, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_failureaward, "%d/%m/%Y %H:%M:%S")
            self.timespent_failureaward = int(difference.total_seconds())
        elif start_or_end == "start_instructions":
            self.start_instructions = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_instructions":
            self.end_instructions = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            difference = datetime.datetime.strptime(self.end_instructions, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_instructions, "%d/%m/%Y %H:%M:%S")
            self.timespent_instructions = int(difference.total_seconds())
        elif start_or_end == "start_initialdecision":
            self.start_initialdecision = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_initialdecision":
            self.end_initialdecision = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            difference = datetime.datetime.strptime(self.end_initialdecision, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_initialdecision, "%d/%m/%Y %H:%M:%S")
            self.timespent_initialdecision = int(difference.total_seconds())
        elif start_or_end == "start_projectupdate":
            self.start_projectupdate = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_projectupdate":
            self.end_projectupdate = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            difference = datetime.datetime.strptime(self.end_projectupdate, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_projectupdate, "%d/%m/%Y %H:%M:%S")
            self.timespent_projectupdate = int(difference.total_seconds())
        elif start_or_end == "start_total":
            self.start_total = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elif start_or_end == "end_total":
            self.end_total = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            difference = datetime.datetime.strptime(self.end_total, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.start_total, "%d/%m/%Y %H:%M:%S")
            self.timespent_total = int(difference.total_seconds())


    # def get_time2(self, start_end_variable): #e.g. self.player.get_time("start_total")
    #     print(f"model before {self.end_total}")
    #     start_end_variable = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #     self.endtotal_total = start_end_variable
    #     print(f"model after {self.end_total}")

    # def time_spent2(self, starttime, endtime, timespent_variable): #e.g. self.player.time_spent(self, start_mainpart, end_mainpart, timespent_mainpart)
    #     difference = datetime.datetime.strptime(endtime, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(starttime, "%d/%m/%Y %H:%M:%S")
    #     duration = difference.total_seconds()
    #     self.timespent_variable = f"{float(duration / 60):.2f}" #in minutes f"{duration:.0f}sec; {float(duration / 60):.2f}min"

    #timers
    start_mainpart = models.StringField() 
    end_mainpart = models.StringField() 
    start_lottery = models.StringField() #drop criteria
    end_lottery = models.StringField() 
    start_failureaward = models.StringField() #drop criteria
    end_failureaward = models.StringField() 
    start_peq = models.StringField()
    end_peq = models.StringField()
    start_instructions = models.StringField()
    end_instructions = models.StringField()
    start_initialdecision = models.StringField()
    end_initialdecision = models.StringField()
    start_projectupdate = models.StringField()
    end_projectupdate = models.StringField()
    start_total = models.StringField() #get time of participant when welcome page is loaded
    end_total = models.StringField() #get time of participant when last page is loaded

    timer_instructions = models.StringField()
    timer_quiz = models.StringField() # has to be a stringfield, since multiple attempts are possible which have to be stored in an array. intfields cant easily store arrays
    timer_initialdecision = models.StringField()
    timer_subrecommendation = models.StringField()
    timer_subchoice = models.StringField()
    timer_subrecommendation2 = models.StringField()
    timer_sub2choice = models.StringField()

    #quiz error tracker
    first_task_answers = models.StringField(initial="FirstTry") #records all incorrect answers after FirstTry in an array (--> stringfield). stays FirstTry, if first answers chosen is the correct one
    feedback_answers = models.StringField(initial="FirstTry")
    manipulation_A1_answers = models.StringField(initial="FirstTry")
    manipulation_A2_answers = models.StringField(initial="FirstTry")
    manipulation_A3_answers = models.StringField(initial="FirstTry")
    when_FA_A1_answers = models.StringField(initial="FirstTry")
    when_FA_A2_answers = models.StringField(initial="FirstTry")
    definition_answers = models.StringField(initial="FirstTry")
    delay_answers = models.StringField(initial="FirstTry")
    what_FA_answers = models.StringField(initial="FirstTry")
    compensation_FA_answers = models.StringField(initial="FirstTry")
    compensation_Co_answers = models.StringField(initial="FirstTry")
    example_answers = models.StringField(initial="FirstTry")
    variable_answers = models.StringField(initial="FirstTry")
    dollars_answers = models.StringField(initial="FirstTry")
    variable_c_answers = models.StringField(initial="FirstTry")

    calc_opened = models.IntegerField(initial=0) #set to 1 if calc was opened on the first initial decision page
    # ip_address = models.StringField()
    # browser = models.StringField()

    #quiz
    first_task=create_mc("My first task as a leading manager of the projects department is to...", [[1,"... develop a new product idea."],[2,"... select two innovation projects."], [3,"... select one of two potential innovation projects."]])

    feedback=create_mc("Please select the right answer:", [[1,"My decisions will be reviewed and I might receive written feedback later on."],[2,"My decisions will not be reviewed by anyone."], [3,"My decisions do not influence my compensation."]])

    manipulation_A1=create_mc("The board is convinced that Courage Awards help CleverClean to gain a competitive advantage by granting them to managers who have the courage to...", [[2,"... take value adding risks by trying something new and are not afraid to fail big."],[1,"... motivate themselves and others to strive for high effort even when a project seems to fail."], [3,"... do their outmost to avoid as many mistakes as possible during their daily working routine."]])

    manipulation_A2=create_mc("The board is convinced that Courage Awards help CleverClean to gain a competitive advantage by granting them to managers who have the courage to...", [[2,"... 'pull the plug' of a failing project before more resources are wasted and are not afraid to admit their failures."],[1,"... motivate themselves and others to strive for high effort even when a project seems to fail."], [3,"... do their outmost to avoid as many mistakes as possible during their daily working routine."]]) 

    manipulation_A3=create_mc("The board is convinced that Courage Awards help CleverClean to gain a competitive advantage by granting them to managers who have the courage to...", [[2,"... take value adding risks by trying something new and are not afraid to fail big. Additionally, managers should also have the courage to ”pull the plug” of a failing project before more resources are wasted and are not afraid to admit their failures."],[1,"... motivate themselves and others to strive for high effort even when a project seems to fail."], [3,"... do their outmost to avoid as many mistakes as possible during their daily working routine."]]) 

    when_FA=create_mc("When do I receive a Courage Award?", [[1,"I will always receive a Courage Award with 100% certainty by the end of the experiment."],[2,"In case I keep investing in a failing project which ends up generating high returns."], [3,"In case I take value adding risks but my project ends up failing and I deliberately decide for project discontinuation."]])

    when_FA_A1=create_mc("When do I, as a leading project manager, receive a Courage Award?", [[1,"I receive a Courage Award when a riskless and innovative project ends up failing and I continue it."],[2,"I receive a Courage Award when I start a risky project that turns out to be profitable and I terminate it."], [3,"I receive a Courage Award when I start a risky and innovative project that ends up failing and I terminate it."]])

    when_FA_A2=create_mc("When do I, as a leading project manager, receive a Courage Award?", [[1,"I receive a Courage Award when I continue a failing project that was riskless but appeared innovative."],[2,"I receive a Courage Award when I terminate a profitable project that was risky but appeared highly innovative."], [3,"I receive a Courage Award when I terminate a failing project that was risky but appeared highly innovative."]])

    definition=create_mc("How does CleverClean define a failing project?", [[1,"A project is defined as failing in case the management board itself announces that the project is failing."],[2,"A project is defined as failing if investing any additional dollar in this project creates lower expected returns than investing in alternative projects."], [3,"A project is defined as failing when it generates more expected value than initially predicted and more than the expected value of an alternative project."]])

    delay=create_mc("The possibility to receive a Courage Award...", [[1,"... decreases in case of delayed project discontinuation."],[2,"... increases in case of delayed project discontinuation."], [3,"... is independent of the timing of my discontinuation decision."]])

    what_FA=create_mc("What do I receive as a Courage Award...", [[1,"... 0.2 million Lira."],[2,"... 1% of the total 0.2 million Lira Courage Award budget."], [3,"... 1% of the project's outcome."]])

    # multiplechoice field: choices has to be an iterable and every of its elements has to contain exactly 2 elements.
    compensation_FA = models.StringField(widget=forms.widgets.CheckboxSelectMultiple(choices=[["1","Fixed payment"],["2","Lottery payout"], ["3","Variable compensation from the main task"], ["4","Potential Courage Award"]]), label="What are the components of your total compensation? (please select all applicable boxes)")

    compensation_Co = models.StringField(widget=forms.widgets.CheckboxSelectMultiple(choices=[["1","Fixed payment"],["2","Lottery payout"], ["3","Variable compensation from the main task"], ["4","A monetary bonus"]]), label="What are the components of your total compensation? (please select all applicable boxes)")

    example = models.StringField(label="In the following example, what is the project account balance after project completion (in million Lira)?")

    variable = models.StringField(label="How much is your variable compensation in Lira if the project account balance is 5m Lira and you qualify to receive a Courage Award with a budget of 0.2m Lira?")

    variable_c = models.StringField(label="How much is your variable compensation in Lira if the project account balance is 5m Lira after the completion of the project?")

    dollars = models.StringField(label="How many Dollars equal 40,000 Lira?")


#PEQs


    pq1=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="After I selected my project, I mainly focused on:")

    pq2=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="It was important for CleverClean that I: ")

    pq3=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="In my opinion project continuation is associated with failure.")

    pq4=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="According to CleverClean, continuing the project meant to invest more money in a failing project.")

    pq5=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="The Courage Award influenced my recommendation to the management board as follows: I was more tending to... ")

    pq6mneu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize your selected project? It displays a ...")

    pq6vneu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize your selected project? It displays a ...")

    pq6_one_neu_m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize your selected project? It displays a ...")

    pq6_one_neu_v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize your selected project? It displays a ...")

    pq6_two_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize your selected project? It displays a ...")

    pq6_three_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="What is the likelihood of your chosen project to succeed?")

    pq7neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="In your opinion, how risky is it to choose the project Smart Mop Robot?")

    pqneu1=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="Which project is - in your opinion - the riskier one?")

    pq7m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I feel that choosing the Smart Mop Robot project is…")

    pq7v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I feel that choosing the Smart Vacuum Robot project is…")

    pq8v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I am convinced that my chosen project Smart Vacuum Robot will be successful.")

    pq8m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I am convinced that my chosen project Smart Mop Robot will be successful.")

    pq9m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I believe there are very little risks in continuing to invest in the Smart Mop Robot.")

    pq9v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I believe there are very little risks in continuing to invest in the Smart Vacuum Robot.")

    pq10=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="The Courage Award motivated me to take risks.")

    pq10_eleven_m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I strongly preferred choosing Smart Mop Robot over Smart Vacuum Robot.") #see Fehrenbacher 2020 paper (description of the dependent variable)

    pq10_eleven_v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I strongly preferred choosing Smart Vacuum Robot over Smart Mop Robot.")

    pq11=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="In my role as a manager at CleverClean I had concerns about taking risks.")

    pq11_one_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize the decision to continue the project?")

    pq11_two_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize the decision to continue the project?")

    pq11_three_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="How would you characterize the decision to continue the project?")

    pq11_four_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="What is the likelihood of your project to succeed?")

    pq12m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I consider it as a failure to have originally invested in the project Smart Mop Robot.")

    pq12v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I consider it as a failure to have originally invested in the project Smart Vacuum Robot.")

    pq13=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I had already invested so much that it seemed silly…")

    pq14m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I feel responsible for the outcome of my Smart Mop Robot project.")

    pq14v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I feel responsible for the outcome of my Smart Vacuum Robot project.")

    pq15m=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="It was important to me to complete the Smart Mop Robot project.")

    pq15v=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="It was important to me to complete the Smart Vacuum Robot project.")

    pq16=create_mc("I calculated the expected value in order to make my decisions.", [[1,"Yes"],[2,"No"]])

    pq16neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="The expected value of the project's outcome was important for making my decisions.")

    pq17=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="When I took my decisions I mainly focused on the positive aspects of my project.")

    pq18=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I am afraid to receive negative feedback from the experimental administrator.")

    pq19=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I have doubts about taking responsibility for future CelverClean projects.")

    pq20=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I feel that at CleverClean, failures are tolerated and not punished.")

    pq20_one_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I feel that at CleverClean, mistakes are perceived as an opportunity to improve oneself.")

    pq21=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="It is safe to take risks at CleverClean") 

    pq22=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="Due to the Courage Award I was not afraid to terminate my project and thereby admit my failure.") 

    pq23=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="To what extent do you feel the need to justify your initial project decision?") 

    pq24=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="For me, receiving a Courage Award is something one should be ashamed of.")

    pq25=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I thought that it would look good if I...")

    pq26=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="In your opinion, what is the likelihood that terminating the project results in negative personal consequences (e.g. decreased promotion probability):")

    pq26_one_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I thought that it would make a good impression if I ...")

    pq27=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I was afraid that important persons (e.g. superiors) could receive a bad impression of me in case I terminate the project.")

    pq28=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="The monetary compensation of $0.10 (2000 Lira) from the Courage Award was important to me.")

    pq29=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="It was important to me to achieve the highest possible compensation.")

    pq29_one_neu=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="It was important to me to receive the Courage Award.")

    pq30=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="Due to the Courage Award I put more focus on discovering potential project flaws.") #wording changed 15th march

    pq31=create_mc("I have already heard about the topic of „biases“ and its role in decision-making.", [[1,"Yes"],[2,"No"]])

    pq31a=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I am very familiar with the topic „biases“.")

    pq32=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I diversified the amount of risk I took between the initial project decision and the decisions regarding the further development of the project (e.g. when I took high risks in the beginning I played it save later on).")

    pq33=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="Once I start something I want to finish it.")

    pq34=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I generally assume that errors are not always avoidable.")

    pq35=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I have no problems with openly admitting my mistakes.")

    pq36=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I often worry about what others think about me.")

    pqAC1=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I have used the Internet at least once in my life.") #attention check, reversed 15th march

    pqAC2=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="I currently pay attention to the questions I am being asked in the survey.")

    pq37=create_mc("I have already heard about Courage Awards (also known as Failure Awards) and their role in decision-making.", [[1,"Yes"],[2,"No"]])

    #Demographics 
    gender = models.StringField(choices=["Male", "Female", "Diverse"],widget=widgets.RadioSelectHorizontal, label="Please indicate your gender.")
    degree = models.StringField(choices=["High-school", "College", "Bachelor degree", "Master degree", "MBA", "PhD", "Others"], label="What is the highest degree you have already achieved?")
    age = models.IntegerField(choices=[i for i in range(14,99)], label="Please indicate your age.")
    language = models.StringField(label="What is your native language?")
    country = models.StringField(choices=["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "The Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Republic of the", "Congo, Democratic Republic of the", "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor (Timor-Leste)", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "The Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein" , "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia, Federated States of", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates","United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City (Holy See)", "Venezuela","Vietnam", "Yemen", "Zambia", "Zimbabwe"], label="In which country do you live? ")
    workexperience = models.StringField(choices=["< 1 year", "1-2 years", "3-5 years", "6-10 years", "> 10 years"], label="How many years of work experience do you have?")
    industry = models.StringField(choices=["Accountant", "Advertising/Commercial/Public Relations", "Agriculture", "Airlines", "Automotive", "Banking, Finance, Insurance & Real Estate", "Business Services/Business Management", "Clothing Manufacturing", "Computer Software", "Doctors & Other Health Professionals", "Education", "Food Stores", "Government Employees", "Health", "IT", "Lawyers / Law Firms", "Manufacturing", "Pharmaceuticals / Health Products", "Restaurants & Drinking Establishments", "Retired", "Sports/Professional", "Student", "TV / Movies / Music", "Unemployed", "Others"], label="In which industry do you work? ")
    businessexperience=create_mc("Do you have any working experience or educational knowledge in business related fields (e.g., project management, market development, business studies, ...)?", [[1,"Yes"],[2,"No"]])
    mturk = models.StringField(choices=["0", "1-3", "4-10", "> 10"], label="In how many experimental studies have you participated so far?")


    prizewheel=create_mc("What is the expected value of this prize wheel?", [[1,"$0.00"],[2,"$0.25"], [3,"$1.25"], [4,"$1.50"], [5,"$2.00"], [6,"$5.75"], [7,"$6.00"], [8,"$8.00"], [9,"$10.00"]])

    #payout stuff
    lottery_draft = models.PositiveIntegerField() #to determine drafted scenario
    lottery_outcome = models.PositiveIntegerField() #to determine outcome in case of lottery participation
    project_success_outcome = models.PositiveIntegerField() #0:worst case; 1: best case
    failure_award_draft = models.PositiveIntegerField() #50% chance to receive FA
    variable_payout = models.CurrencyField()
    fa_payout = models.CurrencyField()
    lottery_payout = models.CurrencyField()
    total_payout = models.CurrencyField() #store player total payout