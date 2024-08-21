

class SSAPI(object):
    pass

class SSRegistry(object):
    pass

class QueueManager(object):
    pass

class ScanAdminTracker(object):
    pass

class TBABE(object):
    pass

class ServiceReport(object):
    pass

class ServiceScoutSuite(object):
    pass

class MockWorkflow(object):
    def run(self):
        print("Executing MockWorkflow")

if __name__ == "__main__":
    MockWorkflow().run()


