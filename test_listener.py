from robot.api import TestSuite

suite = TestSuite()
test = suite.tests.create('Image Debugger Test')    
test.body.create_keyword('Image Debugger')
result = suite.run(report=None,log=None, listener='ImageDebugger')
pass