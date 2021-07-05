from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random #for payout determination


#attention checks: pricewheel seconds? introduction seconds? Courage Award with examples seconds? quiz zu oft falsch (FA items)? initial decision time? PEQ_1v attention check einbauen? beide attention checks failed? auf 2-3 PEQ seiten gleiche Antwort
#auf anweisungen verweisen

class welcome(Page):
    def vars_for_template(self): #execute when page is loaded
        self.player.get_time("start_total")
    # def before_next_page(self):
    #     print(self.player.start_total)
    #     self.player.get_time(self.player.start_total) #get start time

class prizewheel(Page):
    form_model = "player"
    form_fields = ["prizewheel"]

    # def before_next_page(self):
    #     print(self.player.start_instructions)
    #     self.player.get_time(self.player.start_instructions) #get start time

#class fail(Page): #DEACTIVATED for testing
#    def is_displayed(self):
#        return (self.player.prizewheel!=3 or
#        (self.player.timespent_lottery is not None and self.player.timespent_lottery < 0) or #30 secs
#        (self.player.timespent_instructions is not None and self.player.timespent_instructions < 0) or #60 secs
#        (self.player.timespent_failureaward is not None and self.player.timespent_failureaward < 0) or #50 secs
#        (self.player.quiz_totalwronganswers is not None and self.player.quiz_totalwronganswers >= 15) or # ANPASSEN NACH UNTEN FÜR STRENGER
#        (self.player.timespent_initialdecision is not None and self.player.timespent_initialdecision < 0) or #40 secs
#        (self.player.timespent_projectupdate is not None and self.player.timespent_projectupdate < 0) #80 secs
#        )

#Hier die # löschen um es zu aktivieren!

class fail(Page): #or conditions for mturk
    def is_displayed(self):
        return (
            (self.player.timespent_projectupdate is not None and self.player.timespent_projectupdate < 80) or #80 secs
            (self.player.timespent_initialdecision is not None and self.player.timespent_initialdecision < 40 and self.player.timespent_projectupdate is None) or #40 secs
            (self.player.quiz_totalwronganswers is not None and self.player.quiz_totalwronganswers >= 15 and self.player.timespent_initialdecision is None) or # ANPASSEN NACH UNTEN FÜR STRENGER
            (self.player.timespent_failureaward is not None and self.player.timespent_failureaward < 45 and self.player.timer_quiz is None) or #45 secs
            (self.player.timespent_instructions is not None and self.player.timespent_instructions < 60 and self.player.timespent_failureaward is None) or #60 secs
            (self.player.timespent_lottery is not None and self.player.timespent_lottery < 25 and self.player.timespent_instructions is None) or #25 secs. last condition needed otherwise lottery error message will always be displayed 
            self.player.prizewheel!=3
           ) 

    def vars_for_template(self):
        self.player.total_fails += 1

        #failed_at only shows last page that was failed
        if self.player.timespent_projectupdate is not None and self.player.timespent_projectupdate < 80:
            self.player.failed_at = f"ProjectUpdate {self.player.timespent_projectupdate}"
        elif self.player.timespent_initialdecision is not None and self.player.timespent_initialdecision < 40:
            self.player.failed_at = f"Initialinfos {self.player.timespent_initialdecision}"
        elif self.player.quiz_totalwronganswers is not None and self.player.quiz_totalwronganswers >= 15:
            self.player.failed_at = f"Quiz {self.player.quiz_totalwronganswers}"
        elif self.subsession.framing != "C0" and self.player.timespent_failureaward is not None and self.player.timespent_failureaward < 45: #conditions are evaluated one after another. if first one is false already, second one doesnt matter. here second one is none for control group
            self.player.failed_at = f"FAdescription {self.player.timespent_failureaward}"
        elif self.player.timespent_instructions is not None and self.player.timespent_instructions < 60:
            self.player.failed_at = f"Instructions {self.player.timespent_instructions}"
        elif self.player.timespent_lottery is not None and self.player.timespent_lottery < 25:
            self.player.failed_at = f"Lottery {self.player.timespent_lottery}"
        elif self.player.prizewheel != 3:
            self.player.failed_at = f"Pricewheel {self.player.prizewheel}"


class fail_peq(Page): #both attention checks <= 3. Participants can still continue if they want to risk a rejection. check in data for these people
    def is_displayed(self):
            return (self.player.pqAC1 <= 4 and self.player.pqAC2 <= 4)

    def vars_for_template(self):
        self.player.attention_failed = f"Attention checks failed with {self.player.pqAC1} and {self.player.pqAC2}"
        # self.player.total_fails += 1

# class fail_peq(Page): #both attention checks <= 2 AND several peqs answered exactly the same. 
#     def is_displayed(self):
#         if self.subsession.framing in {"A1", "A2", "A3"}:
#             return (self.player.pqAC1 <= 3 and self.player.pqAC2 <= 3 and
#             (self.player.pq23 == self.player.pq26 == self.player.pq24 == self.player.pq27) #bunch of peqs answered identically (non-control groups)
#             )
#         elif self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0":
#             return (self.player.pqAC1 <= 3 and self.player.pqAC2 <= 3 and
#             (self.player.pq12m == self.player.pq13 == self.player.pq14m == self.player.pq15m == self.player.pq17) #mop control
#             )
#         elif self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0":
#             return (self.player.pqAC1 <= 3 and self.player.pqAC2 <= 3 and
#             (self.player.pq12v == self.player.pq13 == self.player.pq14v == self.player.pq15v == self.player.pq17) #vacuum control
#             )
    # def before_next_page(self):
    #     self.player.attention_failed = f"Both attention checks failed with {self.player.pqAC1} and {self.player.pqAC2}"

class overview(Page):
    pass

class lottery1(Page):
    def vars_for_template(self): #execute when page is loaded
        self.player.get_time("start_lottery")

class lottery2(Page):
    form_model = "player"
    form_fields = ["lottery_choice"]

    def vars_for_template(self): #to create risk lottery bootstrap table
        list1 = Constants.lottery_gamble_successrate
        list2 = Constants.lottery_gamble_failurerate
        list3 = [f"id_lottery_choice_{i}" for i in range(1,17)] #1 to 16, 16th in case someone always wants to gamble (17 is exclusive)
        data = list(zip(list1,list2,list3))
        # print(data, len(data)) #[(85, 15, 'id_lottery_choice_1'), (80, 20, 'id_lottery_choice_2'), ..., (15, 85, 'id_lottery_choice_15')] 15
        return {"data": data} # {% for a,b,c in data %} -> {{ a }} .. .. -> displays 85% .. 15% ..  form.lottery_choice.0

    def before_next_page(self):
        self.participant.vars["global_lottery_choice"] = self.player.lottery_choice #if payout is needed in another app
        # print("global_lottery_choice" + str(self.participant.vars["global_lottery_choice"]))
        self.player.get_time("end_lottery")

class after_lottery(Page):
    def before_next_page(self):
        self.player.get_time("start_instructions") #get start time

class Experiment_instructions_A1(Page):
    form_model = "player"
    form_fields = ["timer_instructions"]
    def is_displayed(self):
        return self.subsession.framing == "A1" 

    def before_next_page(self):
        self.player.get_time("end_instructions")
        self.player.get_time("start_failureaward")

class Experiment_instructions_A2(Page):
    form_model = "player"
    form_fields = ["timer_instructions"]
    def is_displayed(self):
        return self.subsession.framing == "A2" 
    def before_next_page(self):
        self.player.get_time("end_instructions")
        self.player.get_time("start_failureaward")

class Experiment_instructions_A3(Page):
    form_model = "player"
    form_fields = ["timer_instructions"]
    def is_displayed(self):
        return self.subsession.framing == "A3" 
    def before_next_page(self):
        self.player.get_time("end_instructions")
        self.player.get_time("start_failureaward")

class Experiment_instructions_Control(Page):
    form_model = "player"
    form_fields = ["timer_instructions"]
    def is_displayed(self):
        return self.subsession.framing == "C0" 
    def before_next_page(self):
        self.player.get_time("end_instructions")

class FailureAward_A1(Page):
    def is_displayed(self):
        return self.subsession.framing == "A1"
    def before_next_page(self):
        self.player.get_time("end_failureaward") #get start time

class FailureAward_A2(Page):
    def is_displayed(self):
        return self.subsession.framing == "A2"
    def before_next_page(self):
        self.player.get_time("end_failureaward") #get start time

class FailureAward_A3(Page):
    def is_displayed(self):
        return self.subsession.framing == "A3"
    def before_next_page(self):
        self.player.get_time("end_failureaward") #get start time

#class FailureAward_2_A1(Page):
#    def is_displayed(self):
#        return self.subsession.framing == "A1"

#class FailureAward_2_A2(Page):
 #   def is_displayed(self):
  #      return self.subsession.framing == "A2"

#class FailureAward_2_A3(Page):
 #   def is_displayed(self):
  #      return self.subsession.framing == "A3"

class Quiz_FA_1(Page):
    form_model = "player"
    form_fields = ["first_task", "feedback", "when_FA_A1", "definition", "delay", "what_FA", "example", "variable", "compensation_FA", "dollars", "timer_quiz"]

    
    def first_task_error_message(self, value):
        #print('value is', value) #value equals selected radiobutton value of question 1 after submission
        if value != 3:
            self.player.first_task_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def feedback_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.feedback_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    #def manipulation_A1_error_message(self, value):
        # print('value is', value)
        #if value != 2:
         #   self.player.manipulation_A1_answers += ", " + str(value)
          #  self.player.quiz_totalwronganswers += 1
           # return 'Your answer is not correct. Please read the experimental instructions again.'
    def when_FA_A1_error_message(self, value):
        # print('value is', value)
        if value != 3:
            self.player.when_FA_A1_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def example_error_message(self, value):
        # print('value is', value, type(value))
        if not (value[0:3] == "6,0" or value == "6" or value[0:3] == "6.0"):
            self.player.example_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def variable_error_message(self, value):
        # print('value is', value)
        if not (value == "52000" or value == "52000,00" or value == "52000,0" or value == "52.000"):
            self.player.variable_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def dollars_error_message(self, value):
        # print('value is', value)
        if not (value[0:4] == "2,00" or value == "2,0" or value == "2" or value == "2.00" or value == "2.0"):
            self.player.dollars_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def definition_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.definition_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def delay_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.delay_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def what_FA_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.what_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
   
    def compensation_FA_error_message(self, value):
        # print('value is', value)
        if value != "['1', '2', '3', '4']":
            self.player.compensation_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'

    def is_displayed(self):
        return self.subsession.framing == "A1" 

class Quiz_FA_2(Page):
    form_model = "player"
    form_fields = ["first_task", "feedback", "when_FA_A2", "definition", "delay", "what_FA", "example", "variable", "compensation_FA", "dollars", "timer_quiz"]
    
    def first_task_error_message(self, value):
        #print('value is', value) #value equals selected radiobutton value of question 1 after submission
        if value != 3:
            self.player.first_task_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def feedback_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.feedback_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    #def manipulation_A2_error_message(self, value):
        # print('value is', value)
        #if value != 2:
          #  self.player.manipulation_A2_answers += ", " + str(value)
          #  self.player.quiz_totalwronganswers += 1
           # return 'Your answer is not correct. Please read the experimental instructions again.'
    def when_FA_A2_error_message(self, value):
        # print('value is', value)
        if value != 3:
            self.player.when_FA_A2_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def example_error_message(self, value):
        # print('value is', value, type(value))
        if not (value[0:3] == "6,0" or value == "6" or value[0:3] == "6.0"):
            self.player.example_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def variable_error_message(self, value):
        # print('value is', value)
        if not (value == "52000" or value == "52000,00" or value == "52000,0" or value == "52.000"):
            self.player.variable_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def dollars_error_message(self, value):
        # print('value is', value)
        if not (value[0:4] == "2,00" or value == "2,0" or value == "2" or value == "2.00" or value == "2.0"):
            self.player.dollars_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def definition_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.definition_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def delay_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.delay_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def what_FA_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.what_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'   
    def compensation_FA_error_message(self, value):
        # print('value is', value)
        if value != "['1', '2', '3', '4']":
            self.player.compensation_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'

    def is_displayed(self):
        return self.subsession.framing == "A2" 

class Quiz_FA_3(Page):
    form_model = "player"
    form_fields = ["first_task", "feedback", "when_FA", "definition", "delay", "what_FA", "example", "variable", "compensation_FA", "dollars", "timer_quiz"]
    
    def first_task_error_message(self, value):
        #print('value is', value) #value equals selected radiobutton value of question 1 after submission
        if value != 3:
            self.player.first_task_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def feedback_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.feedback_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    #def manipulation_A3_error_message(self, value):
        # print('value is', value)
       # if value != 2:
         #   self.player.manipulation_A3_answers += ", " + str(value)
          #  self.player.quiz_totalwronganswers += 1
          #  return 'Your answer is not correct. Please read the experimental instructions again.'
    def when_FA_error_message(self, value):
        # print('value is', value)
        if value != 3:
            self.player.when_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def example_error_message(self, value):
        # print('value is', value, type(value))
        if not (value[0:3] == "6,0" or value == "6" or value[0:3] == "6.0" or value == "6.0m"):
            self.player.example_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def variable_error_message(self, value):
        # print('value is', value)
        if not (value == "52000" or value == "52000,00" or value == "52000,0" or value == "52.000"):
            self.player.variable_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def dollars_error_message(self, value):
        # print('value is', value)
        if not (value[0:4] == "2,00" or value == "2" or value == "2,0" or value == "2.00" or value == "2.0" or value == "$2.0" or value == "$2.00"):
            self.player.dollars_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def definition_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.definition_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def delay_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.delay_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def what_FA_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.what_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def compensation_FA_error_message(self, value):
        # print('value is', value)
        if value != "['1', '2', '3', '4']":
            self.player.compensation_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    
    def is_displayed(self):
        return self.subsession.framing == "A3" 

class Quiz_Control(Page):
    form_model = "player"
    form_fields = ["first_task", "feedback", "example", "variable_c", "compensation_Co", "dollars", "timer_quiz"]
    
    def first_task_error_message(self, value):
        #print('value is', value) #value equals selected radiobutton value of question 1 after submission
        if value != 3:
            self.player.first_task_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def feedback_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.feedback_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def example_error_message(self, value):
        # print('value is', value, type(value))
        if not (value[0:3] == "6,0" or value == "6" or value[0:3] == "6.0"):
            self.player.example_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def variable_c_error_message(self, value):
        # print('value is', value)
        if not (value == "50000" or value == "50000,00" or value == "50000,0" or value == "50.000"):
            self.player.variable_c_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def dollars_error_message(self, value):
        # print('value is', value)
        if not (value[0:4] == "2,00" or value == "2" or value == "2,0" or value == "2.00" or value == "2.0"):
            self.player.dollars_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    def compensation_Co_error_message(self, value):
        # print('value is', value)
        if value != "['1', '2', '3']":
            self.player.compensation_FA_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Your answer is not correct. Please read the experimental instructions again.'
    
    def is_displayed(self):
        return self.subsession.framing == "C0" 


class Quiz_completed(Page):
    def before_next_page(self):
        self.player.get_time("start_mainpart")
        self.player.get_time("start_initialdecision")

class Project_2_A1(Page):
    def is_displayed(self):
        return self.subsession.framing == "A1" 
    def before_next_page(self):
        self.player.get_time("end_initialdecision")

class Project_2_A2(Page):
    def is_displayed(self):
        return self.subsession.framing == "A2" 
    def before_next_page(self):
        self.player.get_time("end_initialdecision")

class Project_2_A3(Page):
    def is_displayed(self):
        return self.subsession.framing == "A3" 
    def before_next_page(self):
        self.player.get_time("end_initialdecision")

class Project_2_Control(Page):
    def is_displayed(self):
        return self.subsession.framing == "C0" 
    def before_next_page(self):
        self.player.get_time("end_initialdecision")

class FA_1(Page):
    def is_displayed(self):
        return self.subsession.framing == "A1" 

class FA_2(Page):
    def is_displayed(self):
        return self.subsession.framing == "A2" 

class FA_3(Page):
    def is_displayed(self):
        return self.subsession.framing == "A3" 

class FA_Control(Page):
    def is_displayed(self):
        return self.subsession.framing == "C0" 

class Decision_1_A1(Page):
    form_model = "player"
    form_fields = ["initial_choices", 'timer_initialdecision']

    def before_next_page(self):
        #print(self.player.initial_choices.split(",")[-1]) # final initial decision. initial_choices records all button clicks on the two investment options
        self.player.initial_decision = self.player.initial_choices.split(",")[-1]
        self.participant.vars['initial_decision'] = "Smart " + self.player.initial_decision #global variable for the 2nd app
        # print("self.participant.vars['initial_decision']:",self.participant.vars['initial_decision'])
    
    def is_displayed(self):
        return self.subsession.framing == "A1" 

class Decision_1_A2(Page):
    form_model = "player"
    form_fields = ["initial_choices", 'timer_initialdecision']

    def before_next_page(self):
        #print(self.player.initial_choices.split(",")[-1]) # final initial decision. initial_choices records all button clicks on the two investment options
        self.player.initial_decision = self.player.initial_choices.split(",")[-1]
        self.participant.vars['initial_decision'] = "Smart " + self.player.initial_decision #global variable for the 2nd app
        # print("self.participant.vars['initial_decision']:",self.participant.vars['initial_decision'])
    
    def is_displayed(self):
        return self.subsession.framing == "A2" 

class Decision_1_A3(Page):
    form_model = "player"
    form_fields = ["initial_choices", 'timer_initialdecision']

    def before_next_page(self):
        #print(self.player.initial_choices.split(",")[-1]) # final initial decision. initial_choices records all button clicks on the two investment options
        self.player.initial_decision = self.player.initial_choices.split(",")[-1]
        self.participant.vars['initial_decision'] = "Smart " + self.player.initial_decision #global variable for the 2nd app
        # print("self.participant.vars['initial_decision']:",self.participant.vars['initial_decision'])
    
    def is_displayed(self):
        return self.subsession.framing == "A3" 
    
class Decision_1_Control(Page):
    form_model = "player"
    form_fields = ["initial_choices", 'timer_initialdecision']

    def before_next_page(self):
        #print(self.player.initial_choices.split(",")[-1]) # final initial decision. initial_choices records all button clicks on the two investment options
        self.player.initial_decision = self.player.initial_choices.split(",")[-1]
        self.participant.vars['initial_decision'] = "Smart " + self.player.initial_decision #global variable for the 2nd app
        # print("self.participant.vars['initial_decision']:",self.participant.vars['initial_decision'])
    
    def is_displayed(self):
        return self.subsession.framing == "C0" 

class PEQ_1m(Page):
    form_model = "player"
    form_fields = ["pqneu1", "pq7neu", "pq6mneu", "pq6_one_neu_m", "pq6_two_neu", "pq6_three_neu", "pq10", "pq10_eleven_m"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and (self.subsession.framing in {"A1", "A2", "A3"})

class PEQ_1v(Page):
    form_model = "player"
    form_fields = ["pqneu1", "pq7neu", "pq6vneu", "pq6_one_neu_v", "pq6_two_neu", "pq6_three_neu", "pq10", "pq10_eleven_v"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and (self.subsession.framing in {"A1", "A2", "A3"})

class PEQ_1m_control(Page):
    form_model = "player"
    form_fields = ["pqneu1", "pq7neu", "pq6mneu", "pq6_one_neu_m", "pq6_two_neu", "pq6_three_neu", "pq10_eleven_m"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0" 

class PEQ_1v_control(Page):
    form_model = "player"
    form_fields = ["pqneu1", "pq7neu", "pq6vneu", "pq6_one_neu_v", "pq6_two_neu", "pq6_three_neu", "pq10_eleven_v"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0" 

class OneYear_later(Page):
    def before_next_page(self):
        self.player.get_time("start_projectupdate")

class Project_update_FA_decision_A1_m(Page):
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subrecommendation", "calc_opened"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
        self.player.get_time("end_projectupdate")

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "A1"   

class Project_update_FA_decision_A1_v(Page):
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subrecommendation", "calc_opened"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
        self.player.get_time("end_projectupdate")

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "A1"

class Project_update_FA_decision_A2_m(Page):
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subrecommendation", "calc_opened"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
        self.player.get_time("end_projectupdate")

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "A2" 
    
class Project_update_FA_decision_A2_v(Page):
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subrecommendation", "calc_opened"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
        self.player.get_time("end_projectupdate")

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "A2"

class Project_update_FA_decision_A3_m(Page):
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subrecommendation", "calc_opened"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
        self.player.get_time("end_projectupdate")

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "A3" 

class Project_update_FA_decision_A3_v(Page):
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subrecommendation", "calc_opened"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
        self.player.get_time("end_projectupdate")

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "A3"

class Project_update_Control_decision(Page):
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subrecommendation", "calc_opened"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
        self.player.get_time("end_projectupdate")
    
    def is_displayed(self):
        return self.subsession.framing == "C0" 

        

class Decision_2YesNo(Page):
    form_model = "player"
    form_fields = ["sub1_choices", 'timer_subchoice'] #neues timer model erstellen

    def vars_for_template(self):
        sub_decision1adjusted = 100 - self.player.sub_decision
        return dict(sub_decision1adjusted=sub_decision1adjusted)
    def before_next_page(self):
        #print(self.player.sub1_choices.split(",")[-1]) # final sub1 decision. sub1_choices records all button clicks on the two investment options
        self.player.sub1_decision = self.player.sub1_choices.split(",")[-1]
        self.participant.vars['sub1_decision'] = "Smart " + self.player.sub1_decision #global variable for the 2nd app
        # print("self.participant.vars['sub1_decision']:",self.participant.vars['sub1_decision'])
        if self.player.sub1_decision == "terminate" and self.player.sub_decision > 50:
            self.player.sub1_consistency = "inconsistent"
        else:
            self.player.sub1_consistency = "consistent"


#class PEQ_2_FA(Page):
 #   form_model = "player"
  #  form_fields = ["pq5"]
   # def is_displayed(self):
    #    return self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3"
    
    #def is_displayed(self):
        #return self.player.VARIABLE==CONTINUED

class Twoyears_later(Page):
    def is_displayed(self):
        return self.player.sub1_decision != "terminate"

class Project_update_FA_2_decision_A1_m(Page):
    form_model = "player"
    form_fields = ['sub_decision2', "slider_inputs2", "timer_subrecommendation2"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision2'] = self.player.sub_decision2 #set global so can be used in the next app

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.player.sub1_decision != "terminate" and self.subsession.framing == "A1"

class Project_update_FA_2_decision_A1_v(Page):
    form_model = "player"
    form_fields = ['sub_decision2', "slider_inputs2", "timer_subrecommendation2"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision2'] = self.player.sub_decision2 #set global so can be used in the next app

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.player.sub1_decision != "terminate" and self.subsession.framing == "A1"

class Project_update_FA_2_decision_A2_m(Page):
    form_model = "player"
    form_fields = ['sub_decision2', "slider_inputs2", "timer_subrecommendation2"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
    
    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.player.sub1_decision != "terminate" and self.subsession.framing == "A2"

class Project_update_FA_2_decision_A2_v(Page):
    form_model = "player"
    form_fields = ['sub_decision2', "slider_inputs2", "timer_subrecommendation2"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision2'] = self.player.sub_decision2 #set global so can be used in the next app

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.player.sub1_decision != "terminate" and self.subsession.framing == "A2"

class Project_update_FA_2_decision_A3_m(Page):
    form_model = "player"
    form_fields = ['sub_decision2', "slider_inputs2", "timer_subrecommendation2"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
    
    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.player.sub1_decision != "terminate" and self.subsession.framing == "A3"

class Project_update_FA_2_decision_A3_v(Page):
    form_model = "player"
    form_fields = ['sub_decision2', "slider_inputs2", "timer_subrecommendation2"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision2'] = self.player.sub_decision2 #set global so can be used in the next app

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.player.sub1_decision != "terminate" and self.subsession.framing == "A3"

class Project_update_Control_2_decision(Page):
    form_model = "player"
    form_fields = ['sub_decision2', "slider_inputs2", "timer_subrecommendation2"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app
    
    def is_displayed(self):
        return self.player.sub1_decision != "terminate" and self.subsession.framing == "C0"


class Decision_3YesNo(Page):
    def is_displayed(self):
        return self.player.sub1_decision != "terminate"

    form_model = "player"
    form_fields = ["sub2_choices", 'timer_sub2choice'] #neues timer model erstellen

    def vars_for_template(self):
        sub_decision2adjusted = 100 - self.player.sub_decision2
        return dict(sub_decision2adjusted=sub_decision2adjusted)
    def before_next_page(self):
        #print(self.player.sub1_choices.split(",")[-1]) # final sub1 decision. sub1_choices records all button clicks on the two investment options
        self.player.sub2_decision = self.player.sub2_choices.split(",")[-1]
        self.participant.vars['sub2_decision'] = "Smart " + self.player.sub2_decision #global variable for the 2nd app
        # print("self.participant.vars['sub1_decision']:",self.participant.vars['sub1_decision'])
        if self.player.sub2_decision == "terminate" and self.player.sub_decision2 > 50:
            self.player.sub2_consistency = "inconsistent"
        else:
            self.player.sub2_consistency = "consistent"

        

class PEQ_Intro(Page):
    def vars_for_template(self):
       self.player.get_time("end_mainpart")
    #determine subsequent decision bonus payments
    def before_next_page(self):
        #project payout
        if self.player.sub1_decision == "terminate":
            if self.subsession.framing != "C0" and self.player.initial_decision == "Mop Robot": #with FA: if not control AND  mop
                self.player.payoff += c(Constants.alternative1_boni) #safe payment from alternative
                self.player.variable_payout = c(Constants.alternative1_boni)
                #print(f"Current player bonus payoff if terminate after first update for FA treatments: {self.participant.payoff}")
                self.player.payoff += c(Constants.failure_award) #plus FA
                self.player.fa_payout = c(Constants.failure_award)
                #print(f"Current player bonus payoff if terminate after first update plus FA: {self.participant.payoff}")
            elif self.subsession.framing == "C0" or self.player.initial_decision == "Vacuum Robot": #control OR vac chosen
                self.player.payoff += c(Constants.alternative1_boni_control) #safe payment from alternative
                self.player.variable_payout = c(Constants.alternative1_boni)
                self.player.fa_payout = 0
                #print(f"Current player bonus payoff if terminate after first update for control: {self.participant.payoff}")
        elif self.player.sub2_decision == "terminate":
            if self.subsession.framing != "C0" and self.player.initial_decision == "Mop Robot": #with FA
                population_fa = [0, 1] # 0: fa failed ; 1: fa succeeded
                weights_fa = [0.5, 0.50] # 50% to receive the fa
                self.player.failure_award_draft = random.choices(population_fa, weights_fa)[0] # returns a list with one entry (0 or 1)
                self.player.payoff += c(Constants.alternative2_boni) #safe payment from alternative
                self.player.variable_payout = c(Constants.alternative2_boni)
                #print(f"Current player bonus payoff if terminate after second update for FA treatments: {self.participant.payoff}")
                if self.player.failure_award_draft == 1:
                    self.player.payoff += c(Constants.failure_award) #plus FA
                    self.player.fa_payout = c(Constants.failure_award)
                    # print(f"Current player bonus payoff if terminate after second update plus FA draft successful: {self.participant.payoff}")
            elif self.subsession.framing == "C0" or self.player.initial_decision == "Vacuum Robot": #control
                self.player.payoff += c(Constants.alternative2_boni_control) #safe payment from alternative
                self.player.variable_payout = c(Constants.alternative2_boni_control)
                #print(f"Current player bonus payoff if terminate after second update for control: {self.participant.payoff}")
        elif self.player.sub2_decision == "continue":
            population = [0, 1] # 0: project failed ; 1: project succeeded
            weights = [0.80, 0.20] # project fails with 80% probability and succeeds with 20%
            self.player.project_success_outcome = random.choices(population, weights)[0] # returns a list with one entry (0 or 1)

            if self.player.project_success_outcome == 1: # project succeeded
                self.player.payoff += c(Constants.success_boni)
                self.player.variable_payout = c(Constants.success_boni)
                #print(f"Current player bonus payoff if continuation and best case: {self.participant.payoff}")
            elif self.player.project_success_outcome == 0: # project failed
                self.player.payoff += c(Constants.failure_boni)
                self.player.variable_payout = c(Constants.failure_boni)
                #print(f"Current player bonus payoff if continuation and worst case: {self.participant.payoff}")

        # Lottery payout
        self.player.lottery_draft = random.randint(1,15) # generate random number between 1 and 15 before session is generated
        self.player.lottery_outcome = random.randint(0,100) # generate random number between 0 and 100 before session is generated

        if self.player.lottery_choice > self.player.lottery_draft: # player chooses 14 and < 14 drafted then lotteryparticipation
            if self.player.lottery_outcome <= Constants.lottery_gamble_successrate[self.player.lottery_draft - 1]: #lottery participation succeeded
                self.player.payoff += c(Constants.lottery_success)
                self.player.lottery_payout = c(Constants.lottery_success)
            else:
                self.player.payoff += c(Constants.lottery_failure) #failed
                self.player.lottery_payout = c(Constants.lottery_failure)
        else:
            self.player.payoff += c(Constants.lottery_safe) #safe payment
            self.player.lottery_payout = c(Constants.lottery_safe)
        
        # print(f"Current player bonus payoff after lottery: {self.participant.payoff}")
        self.player.total_payout = self.participant.payoff_plus_participation_fee()

        self.player.get_time("start_peq")

class PEQ_FA_m1(Page):
    form_model = "player"
    form_fields = ["pq1", "pq4", "pq11", "pq11_one_neu", "pq11_two_neu", "pq11_three_neu", "pq11_four_neu"]
    
    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_m2(Page):
    form_model = "player"
    form_fields = ["pq18", "pq19", "pq20", "pq20_one_neu", "pqAC1"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_m3(Page):
    form_model = "player"
    form_fields = ["pq12m", "pq13", "pq14m", "pq15m", "pq16neu"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_m4(Page):
    form_model = "player"
    form_fields = ["pq23", "pq26", "pq26_one_neu", "pq24", "pq27"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_m5(Page):
    form_model = "player"
    form_fields = ["pq35", "pqAC2", "pq36"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_m6(Page):
    form_model = "player"
    form_fields = ["pq28", "pq29", "pq29_one_neu", "pq30", "pq37", "pq31", "pq31a"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_v1(Page):
    form_model = "player"
    form_fields = ["pq1", "pq4", "pq11", "pq11_one_neu", "pq11_two_neu", "pq11_three_neu", "pq11_four_neu"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_v2(Page):
    form_model = "player"
    form_fields = ["pq18", "pq19", "pq20","pq20_one_neu", "pqAC1"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_v3(Page):
    form_model = "player"
    form_fields = ["pq12v", "pq13", "pq14v", "pq15v", "pq16neu"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_v4(Page):
    form_model = "player"
    form_fields = ["pq23", "pq26", "pq26_one_neu", "pq24", "pq27"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_v5(Page):
    form_model = "player"
    form_fields = ["pq35", "pqAC2", "pq36"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_FA_v6(Page):
    form_model = "player"
    form_fields = ["pq28", "pq29", "pq29_one_neu", "pq30", "pq37", "pq31", "pq31a"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and (self.subsession.framing == "A1" or self.subsession.framing == "A2" or self.subsession.framing == "A3")

class PEQ_Control_m1(Page):
    form_model = "player"
    form_fields = ["pq1", "pq4", "pq11", "pq11_one_neu", "pq11_two_neu", "pq11_three_neu", "pq11_four_neu"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0"

class PEQ_Control_m2(Page):
    form_model = "player"
    form_fields = ["pq18", "pq19", "pq20","pq20_one_neu",  "pqAC1"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0"

class PEQ_Control_m3(Page):
    form_model = "player"
    form_fields = ["pq12m", "pq13", "pq14m", "pq15m", "pq16neu"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0"

class PEQ_Control_m4(Page):
    form_model = "player"
    form_fields = ["pq23", "pq26", "pq26_one_neu", "pq27"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0"

class PEQ_Control_m5(Page):
    form_model = "player"
    form_fields = ["pq35", "pqAC2", "pq36"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0"

class PEQ_Control_m6(Page):
    form_model = "player"
    form_fields = ["pq29", "pq31", "pq31a"]

    def is_displayed(self):
        return self.player.initial_decision == "Mop Robot" and self.subsession.framing == "C0"

class PEQ_Control_v1(Page):
    form_model = "player"
    form_fields = ["pq1", "pq4", "pq11", "pq11_one_neu", "pq11_two_neu", "pq11_three_neu", "pq11_four_neu"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0"

class PEQ_Control_v2(Page):
    form_model = "player"
    form_fields = ["pq18", "pq19", "pq20", "pq20_one_neu",  "pqAC1"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0"

class PEQ_Control_v3(Page):
    form_model = "player"
    form_fields = ["pq12v", "pq13", "pq14v", "pq15v", "pq16neu"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0"

class PEQ_Control_v4(Page):
    form_model = "player"
    form_fields = ["pq23", "pq26", "pq26_one_neu", "pq27"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0"

class PEQ_Control_v5(Page):
    form_model = "player"
    form_fields = ["pq35", "pqAC2", "pq36"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0"

class PEQ_Control_v6(Page):
    form_model = "player"
    form_fields = ["pq29", "pq31", "pq31a"]

    def is_displayed(self):
        return self.player.initial_decision == "Vacuum Robot" and self.subsession.framing == "C0"

class demographics(Page):
    form_model = "player"
    form_fields = ["gender", "age", "language", "country", "degree", "workexperience", "businessexperience", "industry"]

    def before_next_page(self):
        self.player.get_time("end_peq")
        self.player.get_time("end_total")
    #  self.player.time_spent(self.player.start_total, self.player.end_total, self.player.timespent_total)

class Compensation_FA(Page):
    def vars_for_template(self):
        return dict(scsrate = Constants.lottery_gamble_successrate[self.player.lottery_draft - 1]) #successrate for drafted lotterys

class End(Page):
    pass

#test sequence ohne fail/timer
#page_sequence = [welcome, prizewheel, overview, lottery1, lottery2, after_lottery, Experiment_instructions_A1, Experiment_instructions_A2, Experiment_instructions_A3, Experiment_instructions_Control, FailureAward_A1, FailureAward_A2, FailureAward_A3, Quiz_FA_1, Quiz_FA_2, Quiz_FA_3, Quiz_Control, Quiz_completed, Project_2_A1, Project_2_A2, Project_2_A3, Project_2_Control, FA_1, FA_2, FA_3, FA_Control, Decision_1_A1, Decision_1_A2, Decision_1_A3, Decision_1_Control, PEQ_1m, PEQ_1v, PEQ_1m_control, PEQ_1v_control, OneYear_later, Project_update_FA_decision_A1_m, Project_update_FA_decision_A2_m, Project_update_FA_decision_A3_m, Project_update_FA_decision_A1_v, Project_update_FA_decision_A2_v, Project_update_FA_decision_A3_v,Project_update_Control_decision, Decision_2YesNo, Twoyears_later, Project_update_FA_2_decision_A1_m,Project_update_FA_2_decision_A1_v, Project_update_FA_2_decision_A2_m, Project_update_FA_2_decision_A2_v, Project_update_FA_2_decision_A3_m, Project_update_FA_2_decision_A3_v, Project_update_Control_2_decision, Decision_3YesNo, PEQ_Intro, PEQ_FA_m1, PEQ_FA_m2, PEQ_FA_m3, PEQ_FA_m4, PEQ_FA_m5, PEQ_FA_m6, PEQ_FA_v1, PEQ_FA_v2, PEQ_FA_v3, PEQ_FA_v4, PEQ_FA_v5, PEQ_FA_v6, PEQ_Control_m1, PEQ_Control_m2, PEQ_Control_m3, PEQ_Control_m4, PEQ_Control_m5, PEQ_Control_m6, PEQ_Control_v1, PEQ_Control_v2, PEQ_Control_v3, PEQ_Control_v4, PEQ_Control_v5, PEQ_Control_v6, fail_peq, demographics, Compensation_FA, End]

#complete page seq
page_sequence = [welcome, prizewheel, fail, overview, lottery1, lottery2, fail, after_lottery, Experiment_instructions_A1, Experiment_instructions_A2, Experiment_instructions_A3, Experiment_instructions_Control, fail, FailureAward_A1, FailureAward_A2, FailureAward_A3, fail, Quiz_FA_1, Quiz_FA_2, Quiz_FA_3, Quiz_Control, fail, Quiz_completed, Project_2_A1, Project_2_A2, Project_2_A3, Project_2_Control, fail, FA_1, FA_2, FA_3, FA_Control, Decision_1_A1, Decision_1_A2, Decision_1_A3, Decision_1_Control, PEQ_1m, PEQ_1v, PEQ_1m_control, PEQ_1v_control, OneYear_later, Project_update_FA_decision_A1_m, Project_update_FA_decision_A2_m, Project_update_FA_decision_A3_m, Project_update_FA_decision_A1_v, Project_update_FA_decision_A2_v, Project_update_FA_decision_A3_v,Project_update_Control_decision, fail, Decision_2YesNo, Twoyears_later, Project_update_FA_2_decision_A1_m,Project_update_FA_2_decision_A1_v, Project_update_FA_2_decision_A2_m, Project_update_FA_2_decision_A2_v, Project_update_FA_2_decision_A3_m, Project_update_FA_2_decision_A3_v, Project_update_Control_2_decision, Decision_3YesNo, PEQ_Intro, PEQ_FA_m1, PEQ_FA_m2, PEQ_FA_m3, PEQ_FA_m4, PEQ_FA_m5, PEQ_FA_m6, PEQ_FA_v1, PEQ_FA_v2, PEQ_FA_v3, PEQ_FA_v4, PEQ_FA_v5, PEQ_FA_v6, PEQ_Control_m1, PEQ_Control_m2, PEQ_Control_m3, PEQ_Control_m4, PEQ_Control_m5, PEQ_Control_m6, PEQ_Control_v1, PEQ_Control_v2, PEQ_Control_v3, PEQ_Control_v4, PEQ_Control_v5, PEQ_Control_v6, fail_peq, demographics, Compensation_FA, End]

#compensation check
#page_sequence = [lottery1, lottery2, Decision_1_A1, Project_update_FA_decision_A1_v, Project_update_FA_decision_A1_m, Decision_2YesNo, Project_update_FA_2_decision_A1_v, Project_update_FA_2_decision_A1_m, Decision_3YesNo, PEQ_Intro, Compensation_FA]


#bei page sequence darauf achten, dass PEQ_2_FA nach project_Update_FA_decision_A1 bis A3 (nicht Control) kommt!

# page_sequence_A1 = [welcome, prizewheel, fail, overview, lottery1, lottery2, after_lottery, Experiment_instructions_A1, Quiz_FA_1, Quiz_completed, Project_2_A2, FA_1, Decision_1_A1, PEQ_1m, PEQ_1v, OneYear_later, Project_update_FA_decision_A1, PEQ_2_FA, Decision_2YesNo, Twoyears_later, Project_update_FA_2_decision_A1, Decision_3YesNo, PEQ_Intro, PEQ_FA_m1, PEQ_FA_m2, PEQ_FA_m3, PEQ_FA_m4, PEQ_FA_m5, PEQ_FA_m6, PEQ_FA_v1, PEQ_FA_v2, PEQ_FA_v3, PEQ_FA_v4, PEQ_FA_v5, PEQ_FA_v6, demographics, Compensation_FA, End]

# page_sequence_A2 = [welcome, prizewheel, fail, overview, lottery1, lottery2, after_lottery, Experiment_instructions_A2, Quiz_FA_2, Quiz_completed, Project_2_A3, FA_2, Decision_1_A2, PEQ_1m, PEQ_1v, OneYear_later, Project_update_FA_decision_A2, PEQ_2_FA, Decision_2YesNo, Twoyears_later, Project_update_FA_2_decision_A2, Decision_3YesNo, PEQ_Intro, PEQ_FA_m1, PEQ_FA_m2, PEQ_FA_m3, PEQ_FA_m4, PEQ_FA_m5, PEQ_FA_m6, PEQ_FA_v1, PEQ_FA_v2, PEQ_FA_v3, PEQ_FA_v4, PEQ_FA_v5, PEQ_FA_v6, demographics, Compensation_FA, End]

# page_sequence_A3 = [welcome, prizewheel, fail, overview, lottery1, lottery2, after_lottery, Experiment_instructions_A3, Quiz_FA_2, Quiz_completed, Project_2_Control, FA_3, Decision_1_A3, PEQ_1m, PEQ_1v, OneYear_later, Project_update_FA_decision_A3, PEQ_2_FA, Decision_2YesNo, Twoyears_later, Project_update_FA_2_decision_A2, Decision_3YesNo, PEQ_Intro, PEQ_FA_m1, PEQ_FA_m2, PEQ_FA_m3, PEQ_FA_m4, PEQ_FA_m5, PEQ_FA_m6, PEQ_FA_v1, PEQ_FA_v2, PEQ_FA_v3, PEQ_FA_v4, PEQ_FA_v5, PEQ_FA_v6, demographics, Compensation_FA, End]

# page_sequence_Control = [welcome, prizewheel, fail, overview, lottery1, lottery2, after_lottery, Experiment_instructions_Control, Quiz_Control, Quiz_completed, Project_2, Decision_1_Control, PEQ_1m, PEQ_1v, OneYear_later, Project_update_Control_decision, Decision_2YesNo, Twoyears_later, Project_update_Control_2_decision, Decision_3YesNo, PEQ_Intro, PEQ_Control_m1, PEQ_Control_m2, PEQ_Control_m3, PEQ_Control_m4, PEQ_Control_m5, PEQ_Control_m6, PEQ_Control_v1, PEQ_Control_v2, PEQ_Control_v3, PEQ_Control_v4, PEQ_Control_v5, PEQ_Control_v6, demographics, Compensation_Control, End]



# page_sequence ALL = [welcome, prizewheel, fail, overview, lottery1, lottery2, after_lottery, Experiment_instructions_A1, Experiment_instructions_A2, Experiment_instructions_A3, Experiment_instructions_Control, Quiz_FA_1, Quiz_FA_2, Quiz_FA_3, Quiz_Control, Quiz_completed, Project_2, FA_1, FA_2, FA_3, Decision_1_A1, Decision_1_A2, Decision_1_A3, Decision_1_Control, PEQ_1m, PEQ_1v, OneYear_later, Project_update_FA_decision_A1, Project_update_FA_decision_A2, Project_update_FA_decision_A3, Project_update_Control_decision, PEQ_2_FA, Decision_2YesNo, Twoyears_later, Project_update_FA_2_decision_A1, Project_update_FA_2_decision_A2, Project_update_FA_2_decision_A3, Project_update_Control_2_decision, Decision_3YesNo, PEQ_Intro, PEQ_FA_m1, PEQ_FA_m2, PEQ_FA_m3, PEQ_FA_m4, PEQ_FA_m5, PEQ_FA_m6, PEQ_FA_v1, PEQ_FA_v2, PEQ_FA_v3, PEQ_FA_v4, PEQ_FA_v5, PEQ_FA_v6, PEQ_Control_m1, PEQ_Control_m2, PEQ_Control_m3, PEQ_Control_m4, PEQ_Control_m5, PEQ_Control_m6, PEQ_Control_v1, PEQ_Control_v2, PEQ_Control_v3, PEQ_Control_v4, PEQ_Control_v5, PEQ_Control_v6, demographics, Compensation_FA, End]

