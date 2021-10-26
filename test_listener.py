from robot.api import TestSuite

suite = TestSuite()
suite.resource.imports.library('ImageHorizonLibrary', args=['reference_folder=C:/Users/exgil01/Documents/RobotFramework-DEV/robot-e2e/images'])
test = suite.tests.create('Image Debugger Test')    
test.body.create_keyword('Debug Image')
result = suite.run(report=None,log=None)
