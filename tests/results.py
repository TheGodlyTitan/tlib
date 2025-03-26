from unittest import (
    TestCase,
    TextTestResult
)


class TestResult(TextTestResult):
    
    separator1 = '=' * 60
    separator2 = '-' * 60
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.packages = set()
        
    def startTestRun(self):
        # Handles Main Header
        self.stream.write('\n')
        self.stream.write('[tlib]: Running Tests\n')
    
    def getPackage(self, test: TestCase) -> str:
        return test.__module__.split('.')[0]
        
    def getName(self, test: TestCase) -> str:
        return f'{test.__class__.__name__}.{test._testMethodName}'
        
    def startTest(self, test: TestCase):
        # Per Test: Every line post-startTestRun
        super(TextTestResult, self).startTest(test)
        
        # Handle Package Header
        pkg = self.getPackage(test)
        if pkg not in self.packages:
            self.stream.write(f"{self.separator2}\n")
            print(f'Testing Package: "{pkg}"')
            self.packages.add(pkg)
            
        name = self.getName(test)
        space = 56- len(name)
        dots = '.' * max(0, space)
        self.stream.write(name)
        self.stream.write(f' {dots} ')
        self.stream.flush()

    def addSuccess(self, test: TestCase):
        super(TextTestResult, self).addSuccess(test)
        self.stream.writeln("✅")
        
    def addError(self, test: TestCase, err: Exception):
        super(TextTestResult, self).addError(test, err)
        self.stream.writeln("⚠️")

    def addFailure(self, test: TestCase, err: Exception):
        super(TextTestResult, self).addFailure(test, err)
        self.stream.writeln("❌")
            
    def addSkip(self, test: TestCase, reason: str):
        super(TextTestResult, self).addSkip(test, reason)
        self.stream.writeln("⏭️")
            
    def addExpectedFailure(self, test: TestCase, err: Exception):
        super(TextTestResult, self).addExpectedFailure(test, err)
        self.stream.writeln("🐞")
    
    def addUnexpectedSuccess(self, test: TestCase):
        super(TextTestResult, self).addUnexpectedSuccess(test)
        self.stream.writeln("🎉")
        
    def printErrors(self):
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getName(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err) 
