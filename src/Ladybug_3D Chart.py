# This component creates a 3D chart of hourly or daily data.
# By Chris Mackey and Mostapha Sadeghipour Roudsari
# Chris@MackeyArchitecture.com and Sadeghipour@gmail.com
# Ladybug started by Mostapha Sadeghipour Roudsari is licensed
# under a Creative Commons Attribution-ShareAlike 3.0 Unported License.

"""
Use this component to make a 3D chart in the Rhino scene of any climate data or hourly simulation data.
-
Provided by Ladybug 0.0.58
    
    Args:
        _inputData: A list of input data to plot.
        _xScale_: The scale of the X axis of the graph. The default will plot the X axis with a length of 365 Rhino model units (for 365 days of the year). Connect a list of values for multiple graphs.
        _yScale_: The scale of the Y axis of the graph. The default will plot the Y axis with a length of 24 Rhino model units (for 24 hours of the day). Connect a list of values for multiple graphs.
        _zScale_: The scale of the Z axis of the graph. The default will plot the Z axis with a number of Rhino model units corresponding to the input data values.  Set to 0 to see graphCurves appear on top of the mesh.  Connect a list of values for multiple graphs.
        _yCount_: The number of segments on your y-axis.  The default is set to 24 for 24 hours of the day. This variable is particularly useful for input data that is not for each hour of the year.
        legendPar_: Optional legend parameters from the Ladybug Legend Parameters component.
        _basePoint_: An optional point with which to locate the 3D chart in the Rhino Model.  The default is set to the Rhino origin at (0,0,0).
        condStatement_ : An optional conditional statement, which will remove data from the chart that does not fit the conditions. The input must be a valid python conditional statement (e.g. a > 25).
        bakeIt_ : If set to True, the chart will be Baked into the Rhino scene as a colored mesh.
    Returns:
        readMe!: ...
        graphMesh: A 3D plot of the input data as a colored mesh.  Multiple meshes will be output for several input data streams or graph scales.
        graphCurves: A list of curves and test surfaces representing the time periods corresponding to the input data.  Note that if the time period of the input data is not clear, no curves will be generated here.
        legend: A legend of the chart. Connect this output to a grasshopper "Geo" component in order to preview the legend in the Rhino scene.
        legendBasePts: The legend base point, which can be used to move the legend in relation to the chart with the grasshopper "move" component.
        titleText: String values representing the title and time labels of the chart.  Hook this up to a Ladybug "TextTag3D" component in order to get text that bakes into Rhino as text.
        titleBasePts: Points for placement of the title and time labels of the chart.  Hook this up to a Ladybug "TextTag3D" component in order to get text that bakes into Rhino as text.
        conditionalHOY: The input data for the hours of the year that pass the conditional statement.
"""

ghenv.Component.Name = "Ladybug_3D Chart"
ghenv.Component.NickName = '3DChart'
ghenv.Component.Message = 'VER 0.0.58\nNOV_01_2014'
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "2 | VisualizeWeatherData"
#compatibleLBVersion = VER 0.0.58\nAUG_20_2014
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import scriptcontext as sc
import Rhino as rc
import System
from math import pi as PI

from clr import AddReference
AddReference('Grasshopper')
import Grasshopper.Kernel as gh
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
import math


def checkConditionalStatement(annualHourlyData, conditionalStatement):
        lb_preparation = sc.sticky["ladybug_Preparation"]()
        indexList, listInfo = lb_preparation.separateList(annualHourlyData, lb_preparation.strToBeFound)
        
        letters = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
        # remove 'and' and 'or' from conditional statements
        csCleaned = conditionalStatement.Replace('and', '')
        csCleaned = csCleaned.Replace('or', '')
        
        # find the number of the lists that have assigned conditional statements
        listNum = []
        for count, let in enumerate(letters):
            if csCleaned.find(let)!= -1: listNum.append(count)
        
        # check if all the conditions are actually applicable
        for num in listNum:
            if num>len(listInfo) - 1:
                warning = 'A conditional statement is assigned for list number ' + `num + 1` + '  which is not existed!\n' + \
                          'Please remove the letter "' + letters[num] + '" from the statements to solve this problem!\n' + \
                          'Number of lists are ' + `len(listInfo)` + '. Please fix this issue and try again.'
                          
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
                return -1, -1
        
        selList = []
        [selList.append([]) for i in range(len(listInfo))]
        startHour = listInfo[0][5]
        endHour = listInfo[0][6]
        
        for i in range(len(listInfo)):
            selList[i] = annualHourlyData[indexList[i]+7:indexList[i+1]]
            if listInfo[i][5]!= startHour or  listInfo[i][6]!=endHour :
                warning = 'Length of all the lists should be the same to apply conditional statemnets.' + \
                          ' Please fix this issue and try again!\nList number '+ `i+1` + ' is the one that causes the issue.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
                return -1, -1
        
        # replace the right list in the conditional statement
        statement = conditionalStatement.split(' ')
        finalStatement = 'pattern = '
        titleStatement = '...                         ...                         ...\n' +\
                         'Conditional Selection Applied:\n'
        
        for statemntPart in statement:
            statementCopy = str.Copy(statemntPart) # a copy to make a meaningful string
            
            if statemntPart!='and' and statemntPart!='or':
                for num in listNum:
                    toBeReplacedWith = 'selList[this][HOY]'.replace('this', `num`)
                    titleToBeReplacedWith = listInfo[num][2]
                    
                    statemntPart = statemntPart.replace(letters[num], toBeReplacedWith, 20000)
                    statementCopy = statementCopy.replace(letters[num], titleToBeReplacedWith, 20000)
                    if statementCopy.find(letters[num])!=-1: break
                    
                titleStatement = titleStatement + ' ' + statementCopy
            else:
                
                titleStatement = titleStatement + '\n' + statementCopy
            finalStatement = finalStatement + ' ' + statemntPart
        print titleStatement
        
        # check for the pattern
        patternList = []
       
        for HOY in range(8760):
            try:
                exec(finalStatement)
                patternList.append(pattern)
            except:
                pass
                
        return titleStatement, patternList

def makeChart(values, xSize, xScale, yScale, zScale, patternList, basePoint, colors, yCount):
    #If there is no yCount, define it as 24
    if yCount == []:
        if len(values) == 24:
            yCount = 1
        else:
            yCount = xSize
    else:
        yCount = yCount[0]
    
    # make a monocolor mesh without webbing between the primary faces.
    ySize = int(len(values)/xSize)
    meshFacePts = []
    
    for i in range(len(values)):
        xMove = - xScale * (i % xSize)
        yMove = yScale * int(i / xSize)
        zMove = zScale * values[i]
        movingVec = rc.Geometry.Vector3f(xMove,yMove,zMove)
        newPoint = rc.Geometry.Point3d.Add(basePoint, movingVec)
        
        facePt1 = newPoint
        facePt2 = rc.Geometry.Point3d(newPoint.X + xScale, newPoint.Y, newPoint.Z)
        facePt3 = rc.Geometry.Point3d(newPoint.X + xScale, newPoint.Y + yScale, newPoint.Z)
        facePt4 = rc.Geometry.Point3d(newPoint.X, newPoint.Y + yScale, newPoint.Z)
        
        meshFacePts.append([facePt1, facePt2, facePt3, facePt4])
    
    joinedMesh = rc.Geometry.Mesh()
    
    for list in  meshFacePts:
        mesh = rc.Geometry.Mesh()
        
        for point in list:
            mesh.Vertices.Add(point)
        
        mesh.Faces.AddFace(0, 1, 2, 3)
        joinedMesh.Append(mesh)
    
    #Create the first webbing in between the primary mesh faces.
    for listCount, list in enumerate(meshFacePts):
        if listCount < len(meshFacePts)-yCount:
            mesh = rc.Geometry.Mesh()
            mesh.Vertices.Add(list[2])
            mesh.Vertices.Add(meshFacePts[listCount+yCount][1])
            mesh.Vertices.Add(meshFacePts[listCount+yCount][0])
            mesh.Vertices.Add(list[3])
            
            mesh.Faces.AddFace(0, 1, 2, 3)
            joinedMesh.Append(mesh)
    
    #Create the second webbing in between the primary mesh faces.
    for listCount, list in enumerate(meshFacePts):
        if listCount/yCount != int(listCount/yCount):
            mesh = rc.Geometry.Mesh()
            mesh.Vertices.Add(list[2])
            mesh.Vertices.Add(list[1])
            mesh.Vertices.Add(meshFacePts[listCount-1][0])
            mesh.Vertices.Add(meshFacePts[listCount-1][3])
            
            mesh.Faces.AddFace(0, 1, 2, 3)
            joinedMesh.Append(mesh)
    
    # color the mesh faces.
    joinedMesh.VertexColors.CreateMonotoneMesh(System.Drawing.Color.Gray)
    
    for srfNum in range (joinedMesh.Faces.Count):
        if srfNum < len(values):
            joinedMesh.VertexColors[4 * srfNum + 0] = colors[srfNum]
            joinedMesh.VertexColors[4 * srfNum + 1] = colors[srfNum]
            joinedMesh.VertexColors[4 * srfNum + 3] = colors[srfNum]
            joinedMesh.VertexColors[4 * srfNum + 2] = colors[srfNum]
        elif srfNum >= len(values) and srfNum < len(values)*2 - yCount:
            joinedMesh.VertexColors[4 * srfNum + 0] = colors[srfNum-len(values)]
            joinedMesh.VertexColors[4 * srfNum + 1] = colors[srfNum-len(values)+yCount]
            joinedMesh.VertexColors[4 * srfNum + 3] = colors[srfNum-len(values)]
            joinedMesh.VertexColors[4 * srfNum + 2] = colors[srfNum-len(values)+yCount]
        elif srfNum >= len(values)*2 - yCount:
            extraVal = int((srfNum - len(values)*2 - yCount)/(yCount-1))
            if yCount == 2: extraVal = extraVal+2
            joinedMesh.VertexColors[4 * srfNum + 0] = colors[srfNum-2*len(values)+(yCount+3)+extraVal]
            joinedMesh.VertexColors[4 * srfNum + 1] = colors[srfNum-2*len(values)+(yCount+3)+extraVal]
            joinedMesh.VertexColors[4 * srfNum + 3] = colors[srfNum-2*len(values)+(yCount+3)+extraVal-1]
            joinedMesh.VertexColors[4 * srfNum + 2] = colors[srfNum-2*len(values)+(yCount+3)+extraVal-1]
        else: pass
    
    #Make a copy of the mesh for purposes of placing the legend correctly.
    originalMesh = rc.Geometry.Mesh.Duplicate(joinedMesh)
    
    # Cull mesh faces that do not meet the conditional statement.
    if condStatement_:
        cullFaceIndices = []
        for count, boolean in enumerate(patternList):
            if boolean == False:
                cullFaceIndices.append(count)
                if count < len(values)-yCount:
                    cullFaceIndices.append(count+len(values))
                    cullFaceIndices.append(count+len(values)-yCount)
                extraVal = int((count - (yCount+1))/yCount)-1
                cullFaceIndices.append(count+(2*len(values))-(yCount+3)-extraVal)
                cullFaceIndices.append(count+(2*len(values))-(yCount+3)-extraVal+1)
            else: pass
        
        joinedMesh.Faces.DeleteFaces(cullFaceIndices)
    else: pass
    
    # Rotate the mesh to be correctly oriented towards the Rhino X and Y axes.
    joinedMesh.Rotate(-math.pi/2, rc.Geometry.Vector3d.ZAxis, basePoint)
    originalMesh.Rotate(-math.pi/2, rc.Geometry.Vector3d.ZAxis, basePoint)
    
    return joinedMesh, originalMesh

def createChartCrvs(values, analysisStart, analysisEnd, xSize, xScale, yScale, zScale, basePoint, yHeight, lb_preparation, legendFont, legendFontSize, lb_visualization):
    ySize = int(len(values)/xSize)
    # Get a value to set the chart curves with.
    orderedVal = values[:]
    orderedVal.sort()
    zMax = orderedVal[0]*zScale + sc.doc.ModelAbsoluteTolerance*5
    
    # Decompose the analysis period
    startMonth = analysisStart[0]
    startDay = analysisStart[1]
    startHour = analysisStart[2]
    endMonth = analysisEnd[0]
    endDay = analysisEnd[1]
    endHour = analysisEnd[2]
    
    # Make a list of days in ech month of the analysis period.
    monthsList = []
    for month in range(startMonth, endMonth+1, 1):
        monthsList.append(month)
    
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    textStrings = []
    daysList = []
    for count, month in enumerate(monthsList):
        textStrings.append(monthNames[month-1])
        if count == 0 and startMonth == endMonth:
            daysList.append(daysPerMonth[month-1] + 1 - startDay + (endDay - daysPerMonth[month-1]))
        elif count == 0:
            daysList.append(daysPerMonth[month-1] + 1 - startDay)
        elif count == len(monthsList) - 1 and endDay != daysPerMonth[month-1]:
            daysList.append(endDay)
        else:
            daysList.append(daysPerMonth[month-1])
    
    # Make the chart curves for each month and get base points for the text
    if legendFontSize == None: legendFontSize = xScale*.75
    monthCurves = []
    textBasePts = []
    curveVertices = []
    i = 0
    for monthDays in daysList:
        Point1 = rc.Geometry.Point3d(basePoint.X+i, basePoint.Y-xScale, zMax)
        Point2 = rc.Geometry.Point3d(basePoint.X+i+(monthDays*yScale), basePoint.Y-xScale, zMax)
        Point3 = rc.Geometry.Point3d(basePoint.X+i+(monthDays*yScale), basePoint.Y+yHeight-xScale-((24-xSize)*xScale), zMax)
        Point4 = rc.Geometry.Point3d(basePoint.X+i, basePoint.Y+yHeight-xScale-((24-xSize)*xScale), zMax)
        curveVertices.append([Point1, Point2, Point3, Point4])
        i+=(monthDays*yScale)
    
    for count, list in enumerate(curveVertices):
        monthCurves.append(rc.Geometry.PolylineCurve([list[0], list[1], list[2], list[3], list[0]]))
        textBasePts.append(rc.Geometry.Point3d(list[0].X+(daysList[count]*yScale*.5) - legendFontSize*2, list[0].Y-legendFontSize*1.5, list[0].Z))
    
    #Make the text surfaces for each month.
    textSrfs = []
    for count, monthText in enumerate(textStrings):
        textSrf = lb_visualization.text2srf([monthText], [textBasePts[count]], legendFont, legendFontSize)
        textSrfs.extend(textSrf[0])
    
    #Generate curves for each of the major hours.
    hoursList = []
    hoursList.append(startHour-1)
    for hour in range(startHour, endHour+1, 1):
        hoursList.append(hour)
    
    hourTextPts = []
    hourLines = []
    i = -xScale
    for hour in hoursList:
        startPt = rc.Geometry.Point3d(basePoint.X, basePoint.Y+i, zMax)
        endPt = rc.Geometry.Point3d(basePoint.X+(ySize*yScale), basePoint.Y+i, zMax)
        hourLines.append(rc.Geometry.LineCurve(startPt, endPt))
        hourTextPts.append(rc.Geometry.Point3d(basePoint.X - legendFontSize*6, basePoint.Y+i, zMax))
        i+=(xScale)
    
    hoursPerPeriod = [0, 6, 12, 18, 24]
    hourNames = ["12 AM", "6 AM", "12 PM", "6 PM", "12 AM"]
    
    for hourCount, hour in enumerate(hoursList):
        for count, period in enumerate(hoursPerPeriod):
            if hour == period:
                textStrings.append(hourNames[count])
                monthCurves.append(hourLines[hourCount])
                textBasePts.append(hourTextPts[hourCount])
                srfs = lb_visualization.text2srf([hourNames[count]], [hourTextPts[hourCount]], legendFont, legendFontSize)[0]
                for srf in srfs:
                    textSrfs.append(srf)
    
    return monthCurves, textBasePts, textStrings, textSrfs


def main(inputData, basePoint, xScale, yScale, zScale, yCount, legendPar, condStatement, bakeIt):
    # import the classes
    if sc.sticky.has_key('ladybug_release'):
        try:
            if not sc.sticky['ladybug_release'].isCompatible(ghenv.Component): return -1
        except:
            warning = "You need a newer version of Ladybug to use this compoent." + \
            "Use updateLadybug component to update userObjects.\n" + \
            "If you have already updated userObjects drag Ladybug_Ladybug component " + \
            "into canvas and try again."
            w = gh.GH_RuntimeMessageLevel.Warning
            ghenv.Component.AddRuntimeMessage(w, warning)
            return -1
        lb_preparation = sc.sticky["ladybug_Preparation"]()
        lb_visualization = sc.sticky["ladybug_ResultVisualization"]()
        
        conversionFac = lb_preparation.checkUnits()
        # copy the custom code here
        if len(inputData)== 0: return -1
        
        if len(inputData)!= 0 and inputData[0]!=None and str(inputData[0]) != "Connect input data here":
            
            # check conditional statement for the whole year
            titleStatement = -1
            if condStatement:
                print 'Checking conditional statements...'
                # send all data and statement to a function and return back
                # True, False Pattern and condition statement
                titleStatement, patternList = checkConditionalStatement(inputData, condStatement)
            if titleStatement == -1:
                patternList = [False] * 8760
                titleStatement = False
            
            hoursOfYear = []
            for hoy, pattern in enumerate(patternList):
                if pattern: hoursOfYear.append(hoy + 1)
            
            # separate the data
            indexList, listInfo = lb_preparation.separateList(inputData, lb_preparation.strToBeFound)
        
            #separate total, diffuse and direct radiations
            separatedLists = []
            for i in range(len(indexList)-1):
                selList = []
                [selList.append(float(x)) for x in inputData[indexList[i]+7:indexList[i+1]]]
                separatedLists.append(selList)
            
            
            res = [[],[], [], [], [], [], []]
            # legendBasePoints = []
            for i, results in enumerate(separatedLists):
                
                if 'Month' in listInfo[i][4]:
                    # scale for the monthly data
                    xExtraFactor = 10
                else:
                    xExtraFactor = 1
                
                    
                try:
                    # assuming there is a scale for this chart
                    xSCC = 10 * float(xScale[i]) * xExtraFactor /conversionFac
                except:
                    try:
                        # try the first item
                        xSCC = 10 * float(xScale[0]) * xExtraFactor /conversionFac
                    except:
                        xSCC = 10 * xExtraFactor/conversionFac
                
                # make sure the scale is not 0
                if xSCC == 0: xSCC = 10 * xExtraFactor/conversionFac
                
                # this is because I rotate the geometry 90 degrees!
                ySC = abs(xSCC)
                
                try:
                    ySCC = 10 * float(yScale[i])/conversionFac
                except:
                    try:
                        ySCC = 10 * float(yScale[0])/conversionFac
                    except:
                        ySCC = 10/conversionFac
                
                if ySCC==0: ySCC = 10/conversionFac
                
                xSC = abs(ySCC)
                
                # read running period
                stMonth, stDay, stHour, endMonth, endDay, endHour = lb_visualization.readRunPeriod((listInfo[i][5], listInfo[i][6]), False)
                
                try:
                    xC = float(yCount[i])
                except:
                    try:
                        xC = float(yCount[0])
                    except:
                        if 'Daily' in listInfo[i][4]: xC = 7
                        elif listInfo[i][4] == 'Monthly' or listInfo[i][4] == 'Monthly-> averaged': xC = 1
                        else: xC = abs(endHour - stHour) + 1
                        
                if xC == 0: xC = abs(endHour - stHour) + 1
                xC = int(xC)
                
                dataType = listInfo[i][2]
                
                if ('Rad' in dataType): extraFactor = 100
                elif ('Hum' in dataType): extraFactor = 5
                elif ('Illuminance' in dataType): extraFactor = 5000
                elif ('Wind Direction' in dataType): extraFactor = 30
                else: extraFactor = 1
                #if xExtraFactor !=1: extraFactor = extraFactor/3
                
                try:
                    zSC = 10 * float(zScale[i])/(conversionFac*extraFactor)
                except:
                    try:
                        zSC = 10 * float(zScale[0])/(conversionFac*extraFactor)
                    except:
                        zSC = 10/(conversionFac*extraFactor)
                
                
                print 'zScale is set to ' +  ("%.2f" % (1/extraFactor)) + ' for ' + dataType
                    
                zSC = abs(zSC)
                
                # read legend parameters
                lowB, highB, numSeg, customColors, legendBasePoint, legendScale, legendFont, legendFontSize = lb_preparation.readLegendParameters(legendPar, False)
                
                # Get the graph colors
                colors = lb_visualization.gradientColor(results, lowB, highB, customColors)
                
                # draw the graph mesh
                coloredChart, originalMesh = makeChart(results, xC, xSC, ySC, zSC, patternList, rc.Geometry.Point3d.Origin, colors, yCount)
                
                #Create the chart curves.
                if yCount == []: yHeight = 24*xSC
                else: yHeight = yCount[i]*xSC
                
                if yHeight == 24*xSC:
                    if len(results) == 8760 or listInfo[i][4] == "Hourly":
                        chartCrvs, textBasePts, textStrings, textSrfs = createChartCrvs(results, listInfo[i][5], listInfo[i][6], xC, xSC, ySC, zSC, rc.Geometry.Point3d.Origin, yHeight, lb_preparation, legendFont, legendFontSize, lb_visualization)
                    else:
                        chartCrvs = []
                        textBasePts = []
                        textStrings = []
                        textSrfs = []
                else:
                    chartCrvs = []
                    textBasePts = []
                    textStrings = []
                    textSrfs = []
                
                #Add the results of the createChartCrvs() function to their respective lists.
                finalChartCrvs = []
                for item in chartCrvs:
                    finalChartCrvs.append(item)
                for item in textSrfs:
                    finalChartCrvs.append(item)
                
                # Group eveything together to use it for the bounding box.
                allGeo = []
                for item in finalChartCrvs:
                    allGeo.append(item)
                allGeo.append(originalMesh)
                
                #Calculate a bounding box around everything that will help place the legend ad title.
                lb_visualization.calculateBB(allGeo, True)
                
                try: movingDist = -1.5 * lb_visualization.BoundingBoxPar[2] # moving distance for sky domes
                except: movingDist = 0
                
                movingVector = rc.Geometry.Vector3d(0, i * movingDist,0)
                coloredChart.Translate(movingVector)
                titleTextCurve, titleStr, titlebasePt = lb_visualization.createTitle([listInfo[i]],lb_visualization.BoundingBoxPar, legendScale, None, False, legendFont, legendFontSize)
                
                legendTitle = listInfo[i][3]
                placeName = listInfo[i][1]
                dataType = listInfo[i][2]
                
                #Group all title stuff together.
                titleText = []
                titleBasePoints = []
                titleBasePoints.append(titlebasePt)
                for item in textBasePts:
                    titleBasePoints.append(item)
                titleText.append(titleStr)
                for item in textStrings:
                    titleText.append(item)
                
                # create legend geometries
                legendSrfs, legendText, legendTextCrv, textPt, textSize = lb_visualization.createLegend(results
                    , lowB, highB, numSeg, legendTitle, lb_visualization.BoundingBoxPar, legendBasePoint, legendScale, legendFont, legendFontSize)
                
                textPt.append(titlebasePt)
                
                ptCount  = 0
                for pt in textPt:
                    ptLocation = rc.Geometry.Point(pt)
                    ptLocation.Translate(movingVector) # move it to the right place
                    textPt[ptCount] = rc.Geometry.Point3d(ptLocation.Location)
                    ptCount += 1
                
                transMtx = rc.Geometry.Transform.Translation(movingVector)
                for crv in legendTextCrv:
                    for c in crv: c.Translate(movingVector)
                for crv in titleTextCurve:
                    for c in crv: c.Translate(movingVector)
                for geo in finalChartCrvs:
                    geo.Translate(movingVector)
                for point in titleBasePoints:
                    point.Transform(transMtx)
                
                # generate legend colors
                legendColors = lb_visualization.gradientColor(legendText[:-1], lowB, highB, customColors)
                
                # color legend surfaces
                legendSrfs = lb_visualization.colorMesh(legendColors, legendSrfs)
                try: legendSrfs.Translate(movingVector) # move it to the right place
                except:
                    msg = "0 hour meets the conditional statemnet."
                    print msg
                    w = gh.GH_RuntimeMessageLevel.Warning
                    ghenv.Component.AddRuntimeMessage(w, msg)
                    return -1
                
                if legendBasePoint == None:
                    nlegendBasePoint = lb_visualization.BoundingBoxPar[0]
                    movedLegendBasePoint = rc.Geometry.Point3d.Add(nlegendBasePoint, movingVector);
                else:
                    movedLegendBasePoint = rc.Geometry.Point3d.Add(legendBasePoint, movingVector);
                
                fullLegTxt = lb_preparation.flattenList(legendTextCrv + titleTextCurve)
                
                # If the user has specified a base point, move all geometry to align with that base point.
                if basePoint:
                    translation = rc.Geometry.Transform.Translation(basePoint.X, basePoint.Y, basePoint.Z)
                    transVec = rc.Geometry.Vector3d(basePoint.X, basePoint.Y, basePoint.Z)
                    coloredChart.Transform(translation)
                    movedLegendBasePoint.Transform(translation)
                    legendSrfs.Transform(translation)
                    for item in fullLegTxt:
                        item.Transform(translation)
                    for item in finalChartCrvs:
                        item.Transform(translation)
                    for point in titleBasePoints:
                        point.Transform(translation)
                else: pass
                
                if bakeIt:
                    studyLayerName = '3D_CHARTS'
                    legendText.append(titleStr)
                    # check the study type
                    try:
                        newLayerIndex, l = lb_visualization.setupLayers(dataType, 'LADYBUG', placeName, studyLayerName, False, False, 0, 0)
                    except:
                        placeName = 'alternateLayerName'
                        newLayerIndex, l = lb_visualization.setupLayers(dataType, 'LADYBUG', placeName, studyLayerName, False, False, 0, 0)
                    lb_visualization.bakeObjects(newLayerIndex, coloredChart, legendSrfs, legendText, textPt, textSize, legendFont)
                
                res[0].append(coloredChart)
                res[1].append([legendSrfs, fullLegTxt])
                res[2].append(movedLegendBasePoint)
                res[3].append(titleText)
                res[4].append(titleBasePoints)
                res[5].append(hoursOfYear)
                res[6].append(finalChartCrvs)
            return res
        elif str(inputData[0]) == "Connect input data here":
            print 'Connect inputData!'
            return -1
        else:
            warning = 'Please ensure that the connected inputData is valid!'
            print warning
            w = gh.GH_RuntimeMessageLevel.Warning
            ghenv.Component.AddRuntimeMessage(w, warning)
            return -1
    else:
        print "You should first let the Ladybug fly..."
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, "You should first let the Ladybug fly...")
        return -1
    
    conversionFac = lb_preparation.checkUnits()



result = main(_inputData, _basePoint_, _xScale_, _yScale_, _zScale_, _yCount_, legendPar_, condStatement_, bakeIt_)
if result!= -1:
    graphMesh = DataTree[System.Object]()
    legend = DataTree[System.Object]()
    graphCurves = DataTree[System.Object]()
    legendBasePts = DataTree[System.Object]()
    conditionalPts = DataTree[System.Object]()
    titleText = DataTree[System.Object]()
    titleBasePts = DataTree[System.Object]()
    conditionalHOY = DataTree[System.Object]()
    
    for i, leg in enumerate(result[1]):
        p = GH_Path(i)
        graphMesh.Add(result[0][i], p)
        legend.Add(leg[0], p)
        legend.AddRange(leg[1], p)
        legendBasePts.Add(result[2][i], p)
        titleText.AddRange(result[3][i], p)
        titleBasePts.AddRange(result[4][i], p)
        conditionalHOY.AddRange(result[5][i], p)
        graphCurves.AddRange(result[6][i], p)
    ghenv.Component.Params.Output[4].Hidden = True
    ghenv.Component.Params.Output[5].Hidden = True
    ghenv.Component.Params.Output[6].Hidden = True
    ghenv.Component.Params.Output[7].Hidden = True