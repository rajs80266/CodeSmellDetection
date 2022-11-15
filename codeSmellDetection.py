from copy import copy

initialCodeSmellsStatistic = {
    "DeadCodesAfterReturn" : 0,
    "MultipleReturnStatementsInFunction" : 0,
    "LongStatements" : 0,
    "MultipleSameFunctionNames" : 0,
    "LongClassOrMethod": 0,
    "LongLoopBlocks": 0,
    "LongConditionalBlocks": 0,
    "LongParameterList": 0
}
functionNames = None
codeSmellsStatistic = None

def describeCodeSmell(description, start, end, codeSmell):
    print(description, end = " ")
    if (start == end):
        print("at line", start + 1)
    else:
        print("from line", start + 1, "to line", end + 1)
    codeSmellsStatistic[codeSmell] += 1

def getLeadingSpaces(line):
    return len(line) - len(line.lstrip())

def getFunctionName(line):
    functionName = line.split()[1]
    if ('(' in functionName):
        functionName = functionName[:functionName.index('(')]
    return functionName

def hasReturnStatement(line):
    return "return" in line.split()

def checkDeadcodeAfterReturn(code, i):
    numberOfLines = len(code)
    leadingSpaces = getLeadingSpaces(code[i])
    j = i + 1
    while (j < numberOfLines and leadingSpaces == getLeadingSpaces(code[j])):
        j += 1
    if (i+1 != j):
        describeCodeSmell('Dead Code found after Return Statement', i + 1, j - 1, 'DeadCodesAfterReturn')

def checkFunctionHavingMultipleReturn(code, i):
    numberOfLines = len(code)
    leadingSpaces = getLeadingSpaces(code[i])
    j = i
    returnCounts = []
    while (j < numberOfLines and (leadingSpaces <= getLeadingSpaces(code[j])) or code[j].lstrip() == ""):
        if (hasReturnStatement(code[j])): returnCounts.append(j + 1)
        j += 1
    if (len(returnCounts) > 1):
        describeCodeSmell('Multiple return statements found at lines ' + str(returnCounts) + ' of function', i - 1, j - 1, 'MultipleReturnStatementsInFunction')

def checkLongStatements(code, i):
    if (len(code[i].lstrip().split()) > 20):
        describeCodeSmell('Long statement found', i, i, 'LongStatements')

def checkSameFunctionNames(functionNames, numberOfLines):
    functionNames = sorted(functionNames, key=lambda d: d['functionName'])
    i = 0
    j = 1
    while (j < len(functionNames)):
        if (functionNames[i]['functionName'] != functionNames[j]['functionName']):
            if (i + 1 < j):
                lineNumbers = [func['lineNumber'] for func in functionNames[i : j]]
                describeCodeSmell('Multiple functions with same name: ' + functionNames[i]['functionName'] + ' found at lines '+ str(lineNumbers), 0, numberOfLines - 1, 'MultipleSameFunctionNames')
            i = j
        j += 1
    if (i + 1 < j):
        print(i, j)

def checkLongBlocks(code, i, blockType):
    numberOfLines = len(code)
    leadingSpaces = getLeadingSpaces(code[i])
    j = i
    while (j < numberOfLines and (leadingSpaces <= getLeadingSpaces(code[j])) or code[j].lstrip() == ""):
        j += 1
    if (blockType == "CLASS" and (j - i) > 60):
        describeCodeSmell('Long Class found', i, j - 1, 'LongClassOrMethod')
    if (blockType == "METHOD" and (j - i) > 40):
        describeCodeSmell('Long Method found', i, j - 1, 'LongClassOrMethod')
    if (blockType == "LOOP" and (j - i) > 20):
        describeCodeSmell('Long Loop Blocks found', i, j - 1, 'LongLoopBlocks')
    if (blockType == "CONDITIONAL" and (j - i) > 10):
        describeCodeSmell('Long Conditional Blocks found', i, j - 1, 'LongConditionalBlocks')

def checkLongParameterList(code, i):
    if (len(code[i].split(',')) > 4):
        describeCodeSmell('Long parameter list found', i, i, 'LongParameterList')

def checkBlocks(code, i):
    ifConditions = ["if(", "if "]
    otherConditions = ["else(", "else ", "elif(", "elif ", "case "]
    if (code[i].lstrip()[0 : 4] == "def "):
        functionNames.append({
            'functionName': getFunctionName(code[i]),
            'lineNumber': i + 1,
        })
        checkFunctionHavingMultipleReturn(code, i + 1)
        checkLongParameterList(code, i)
        blockType = "METHOD"
    elif (code[i].lstrip()[0 : 6] == "class "):
        blockType = "CLASS"
    elif (code[i].lstrip()[0 : 3] in ifConditions or code[i].lstrip()[0 : 3] in otherConditions):
        blockType = "CONDITIONAL"
    else:
        blockType = "LOOPS"
    checkLongBlocks(code, i + 1, blockType)

def findCodeSmells(fileName):
    file1 = open(fileName, 'r')
    code = file1.readlines()
    numberOfLines = len(code)
    i = 0
    while (i < numberOfLines):
        if (hasReturnStatement(code[i])):
            checkDeadcodeAfterReturn(code, i)
        if (len(code[i]) > 1 and code[i][-2] == ':'):
            checkBlocks(code, i)
        checkLongStatements(code, i)
        i += 1
    checkSameFunctionNames(functionNames, numberOfLines)

codeSmellsStatistic = copy(initialCodeSmellsStatistic)
functionNames = []
findCodeSmells('file1.py')
print(codeSmellsStatistic)

codeSmellsStatistic = copy(initialCodeSmellsStatistic)
functionNames = []
findCodeSmells('codeSmellDetection.py')
print(codeSmellsStatistic)