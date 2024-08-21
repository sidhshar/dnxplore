import time
from pprint import pprint


def _custom_step(step_name, state):
    print("--"*20)
    print(f"Executing {step_name}")
    time.sleep(0.5)
    state[step_name] = "Completed"

class TenStepProcess(object):
    def __init__(self):
        # Initialization if needed
        self.state = {}

    def step_1(self):
        print("As a user, I have selected Scantype: Web, Domain: testvulnweb.com")
        _custom_step("Step 1", self.state)
        # print("Executing Step 1")
        # time.sleep(0.5)
        # # Perform the step logic here
        # self.state['step_1'] = "Completed"
    
    def step_2(self):
        _custom_step("Step 2", self.state)
        # print("Executing Step 2")
        # time.sleep(0.5)
        # # Perform the step logic here
        # self.state['step_2'] = "Completed"
    
    def step_3(self):
        print("Executing Step 3")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_3'] = "Completed"

    def step_4(self):
        print("Executing Step 4")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_4'] = "Completed"
    
    def step_5(self):
        print("Executing Step 5")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_5'] = "Completed"
    
    def step_6(self):
        print("Executing Step 6")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_6'] = "Completed"
    
    def step_7(self):
        print("Executing Step 7")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_7'] = "Completed"

    def step_8(self):
        print("Executing Step 8")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_8'] = "Completed"
    
    def step_9(self):
        print("Executing Step 9")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_9'] = "Completed"
    
    def step_10(self):
        print("Executing Step 10")
        time.sleep(0.5)
        # Perform the step logic here
        self.state['step_10'] = "Completed"

    def orchestrator(self):
        print("Starting Orchestration of 10 Steps")
        
        self.step_1()
        self.step_2()
        self.step_3()
        self.step_4()
        self.step_5()
        self.step_6()
        self.step_7()
        self.step_8()
        self.step_9()
        self.step_10()
        
        print("All steps completed.")
        pprint(self.state, indent=4)
        # print("Process state:", self.state)

if __name__ == "__main__":
    process = TenStepProcess()
    process.orchestrator()

