# Psychrometric Chart
# By Chris Mackey
# Chris@MackeyArchitecture.com
# Ladybug started by Mostapha Sadeghipour Roudsari is licensed
# under a Creative Commons Attribution-ShareAlike 3.0 Unported License.

"""
Use this component to draw a psychrometric chart in the Rhino scene and evaluate a set of temperatures and humidity ratios in terms of indoor comfort.  Connected data can include either outdoor temperature and humidty ratios from imported EPW weather data, indoor temperature and humidity ratios from an energy simulation, or indivdual numerical inputs of temperature and humidity.  The input data will be plotted alongside polygons on the chart representing comfort as well as polygons representing the efects of passive building strategies on comfort.
_
The specific human energy balance model used by the psychrometric chart is the Predicted Mean Vote (PMV) model developed by P.O. Fanger. PMV is a seven-point scale from cold (-3) to hot (+3) that is used in comfort surveys.  Each interger value of the scale indicates the following: -3:Cold, -2:Cool, -1:Slightly Cool, 0:Neutral, +1:Slightly Warm, +2:Warm, +3:Hot.  The range of comfort is generally accepted as a PMV between -1 and +1 and this is what defines the range of the comfort polygon on the psychrometric chart.
Accordingly, this component will also output the PMV of the occupant for the input conditions as well as an estimated percentage of people dissatisfied (PPD) in the given conditions.
_
The comfort models that make this component possible were translated to python from a series of validated javascript comfort models developed at the Berkely Center for the Built Environment (CBE).
Specific documentation on the comfort models can be found here: https://code.google.com/p/cbe-comfort-tool/wiki/ComfortModels
_
Special thanks goes to the authors of the online CBE Thermal Comfort Tool who first made the javascript models in order to power the tool:
Hoyt Tyler, Schiavon Stefano, Piccioli Alberto, Moon Dustin, and Steinfeld Kyle, 2013, CBE Thermal Comfort Tool. 
Center for the Built Environment, University of California Berkeley, http://cbe.berkeley.edu/comforttool/
_
The information for the polygons representing passive strategies comes from the climate consultant psychrometric chart.  Further information on how these polygons are calculated can be found here:
http://apps1.eere.energy.gov/buildings/tools_directory/software.cfm/ID=123/pagename=alpha_list
-
Provided by Ladybug 0.0.58
    
    Args:
        _dryBulbTemperature: A number representing the dry bulb temperature of the air in degrees Celcius.  This input can also accept a list of temperatures representing conditions at different times or the direct output of dryBulbTemperature from the Import EPW component.  Indoor temperatures from Honeybee energy simulations are also possible inputs.
        _relativeHumidity: A number between 0 and 100 representing the relative humidity of the air in percentage.  This input can also accept a list of relative humidity values representing conditions at different times or the direct output of relativeHumidity from of the Import EPW component.
        barometricPressure_: A number representing the barometric pressure in Pascals.  If no value is connected here, the default pressure will be 101325 Pa, which is air pressure at sea level.  It is recommended that you connect the barometric pressure from the Import epw component here as the air pressure at sea level can cause some misleading results for cities at higher elevations.
        -------------------------: ...
        meanRadTemperature_: A number representing the mean radiant temperature of the surrounding surfaces in degrees Celcius.  If no value is plugged in here, this component will assume that the mean radiant temperature is equal to 23 C.  This input can also accept a list of temperatures and this will produce several comfort polygons (one for each mean radiant temperature).
        windSpeed_: A number representing the wind speed of the air in meters per second.  If no value is plugged in here, this component will assume a very low wind speed of 0.05 m/s, characteristic of most indoor conditions.  This input can also accept a list of wind speeds representing conditions and this will produce several comfort polygons (one for each wind speed).
        metabolicRate_: A number representing the metabolic rate of the human subject in met.  This input can also accept text inputs for different activities.  Acceptable text inputs include Sleeping, Reclining, Sitting, Typing, Standing, Driving, Cooking, House Cleaning, Walking, Walking 2mph, Walking 3mph, Walking 4mph, Running 9mph, Lifting 10lbs, Lifting 100lbs, Shoveling, Dancing, and Basketball.  If no value is input here, the component will assume a metabolic rate of 1 met, which is the metabolic rate of a seated human being.  This input can also accept lists of metabolic rates and will produce multiple comfort polygons accordingly.
        clothingLevel_: A number representing the clothing level of the human subject in clo.  If no value is input here, the component will assume a clothing level of 1 clo, which is roughly the insulation provided by a 3-piece suit. A person dressed in shorts and a T-shirt has a clothing level of roughly 0.5 clo and a person in a thick winter jacket can have a clothing level as high as 2 to 4 clo.  This input can also accept lists of clothing levels and will produce multiple comfort polygons accordingly.
        -------------------------: ...
        mergeComfPolygons_:  Set to "True" if you have connected multiple values for any of the four comfort variables in the section above and you wish to merge all of the computed comfort polygons into one.
        comfortPar_: Optional comfort parameters from the "Ladybug_PMV Comfort Parameters" component.  Use this to adjust maximum and minimum acceptable humidity ratios.  These comfortPar can also change whether comfort is defined by eighty or ninety percent of people comfortable.
        passiveStrategy_: An optional text input of passive strategies to be laid over the psychrometric chart as polygons.  It is recommended that you use the "Ladybug_Passive Strategy List" to select which polygons you would like to display.  Otherwise, acceptable text inputs include "Evaporative Cooling", "Thermal Mass + Night Vent", "Occupant Use of Fans", "Internal Heat Gain", and "Dessicant Dehumidification".
        strategyPar_: Optional passive strategy parameters from the "Ladybug_Passive Strategy Parameters" component.  Use this to adjust the maximum comfortable wind speed, the building balance temperature, and the temperature limits for thermal mass and night flushing.
        -------------------------: ...
        analysisPeriod_: An optional analysis period from the Ladybug_Analysis Period component.  If no Analysis period is given and epw data from the ImportEPW component has been connected, the analysis will be run for the enitre year.
        annualHourlyData_: An optional list of hourly data from the Import epw component, which will be used to create hourPointColors that correspond to the hours of the data (e.g. windSpeed).  You can connect up several different annualHourly data here.
        conditionalStatement_: This input allows users to remove data that does not fit specific conditions or criteria from the psychrometric chart. The conditional statement input here should be a valid condition statement in Python, such as "a>25" or "b<80" (without quotation marks).
                              The current version of this component accepts "and" and "or" operators. To visualize the hourly data, only lowercase English letters should be used as variables, and each letter alphabetically corresponds to each of the lists (in their respective order): "a" always represents dryBulbtemperature, "b" always represents the relativeHumidity, "c" always represents the 1st list plugged into annualHourlyData_, "d" represents the 2nd list, etc.
                              For example, if you want to plot the data for the time period when temperature is between 18C and 23C, and humidity is less than 80%, the conditional statement should be written as 18<a<23 and b<80 (without quotation marks).
        basePoint_: An optional base point that will be used to place the Psychrometric Chart in the Rhino scene.  If no base point is provided, the base point will be the Rhino model origin.
        scale_: An optional number to change the scale of the spychrometric chart in the Rhino scene.  By default, this value is set to 1.
        legendPar_: Optional legend parameters from the Ladybug Legend Parameters component.
        _runIt: Set to "True" to run the component and generate a psychrometric chart!
    Returns:
        readMe!: ...
        -------------------------: ...
        totalComfortPercent: The percent of the input data that are  inside all comfort and passive strategy polygons.
        totalComfortOrNot: A list of 0's and 1's indicating, for each hour of the input data, if the hour is inside a comfort or strategy polygon (1) or not(0).
        strategyNames:  A list of names for the comfort polygons and strategeis that corresponds to the numbers in the following outputs.
        strategyPercentOfTime: The percent of the input data that are in each of the comfort or passive strategy polygons.  Each number here corresponds to the names in the "strategyNames" output above.
        strategyOrNot: A list of 0's and 1's indicating, for each hour of the input temperature and humidity ratio, if the hour is inside a given comfort or passive strategy polygon (1) or not(0).  If there are multiple comfort polyogns or passive strategies connected to the passiveStrategy_ input, this output will be a grafted list for each polygon.  Each list here corresponds to the names in the "strategyNames" output above.
        -------------------------: ...
        chartCurvesAndTxt: The chart curves and text labels of the psychrometric chart.
        psychChartMesh: A colored mesh showing the number of input hours happen in each part of the psychrometric chart.
        legend: A colored legend showing the number of hours that correspond to each color.
        legendBasePt: The legend base point, which can be used to move the legend in relation to the chart with the grasshopper "move" component.
        comfortPolygons: A brep representing the range of comfort for the input radiant temperature, wind speed, metabolic rate and clothing level.  IF multiple values have been hooked up for any of these inputs, multiple polygons will be output here.
        strategyPolygons: A brep representing the area of the chart made comfortable by the passive strategies.  If multiple strategies have been hooked up to the passiveStrategy_ input, multiple polygons will be output here.
        -------------------------: ...
        chartHourPoints: Points representing each of the hours of input temperature and humidity ratio.  By default, this ouput is hidden and, to see it, you should connect it to a Grasshopper preview component.
        hourPointColors: Colors that correspond to the chartHourPoints above and can be hooked up to the "Swatch" input of a Grasshopper Preview component that has the hour points above connected as geometry.  By default, points are colored red if they lie inside comfort or strategy polygons and are colored blue if they do not meet such comfort criteria.  In the event that you have hooked up annualHourlyData_ this output will be a grafted list of colors.  The first list corresponds to the comfort conditions while the second list colors points based on the annualHourlyData.
        hourPointLegend: A legend that corresponds to the hour point colors above.  In the event that annualHourlyData_ is connected, this output will be a grafted list of legends that each correspond to the grafted lists of colors.
"""
ghenv.Component.Name = "Ladybug_Psychrometric Chart"
ghenv.Component.NickName = 'PsychChart'
ghenv.Component.Message = 'VER 0.0.58\nOCT_23_2014'
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "2 | VisualizeWeatherData"
#compatibleLBVersion = VER 0.0.58\nAUG_20_2014
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import Grasshopper.Kernel as gh
import math
import scriptcontext as sc
import Rhino as rc
import rhinoscriptsyntax as rs
import System
from System import Object
from clr import AddReference
AddReference('Grasshopper')
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path



def checkTheInputs():
    #Define a value that will indicate whether someone has hooked up epw data.
    epwData = False
    epwStr = []
    
    #Check lenth of the _dryBulbTemperature list and evaluate the contents.
    checkData1 = False
    airTemp = []
    airMultVal = False
    if len(_dryBulbTemperature) != 0:
        try:
            if "Temperature" in _dryBulbTemperature[2]:
                airTemp = _dryBulbTemperature[7:]
                checkData1 = True
                epwData = True
                epwStr = _dryBulbTemperature[0:7]
        except: pass
        if checkData1 == False:
            for item in _dryBulbTemperature:
                try:
                    airTemp.append(float(item))
                    checkData1 = True
                except: checkData1 = False
        if len(airTemp) > 1: airMultVal = True
        if checkData1 == False:
            warning = '_dryBulbTemperature input does not contain valid temperature values in degrees Celcius.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        print 'Connect a temperature in degrees celcius for _dryBulbTemperature'
    
    #Check lenth of the _relativeHumidity list and evaluate the contents.
    checkData2 = False
    relHumid = []
    humidMultVal = False
    nonValue = True
    if len(_relativeHumidity) != 0:
        try:
            if "Humidity" in _relativeHumidity[2]:
                relHumid = _relativeHumidity[7:]
                checkData2 = True
                epwData = True
                epwStr = _relativeHumidity[0:7]
        except: pass
        if checkData2 == False:
            for item in _relativeHumidity:
                try:
                    if 0 <= float(item) <= 100:
                        relHumid.append(float(item))
                        checkData2 = True
                    else: nonValue = False
                except:checkData2 = False
        if nonValue == False: checkData2 = False
        if len(relHumid) > 1: humidMultVal = True
        if checkData2 == False:
            warning = '_relativeHumidity input does not contain valid value.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        print 'Connect a value for _relativeHumidity.'
    
    #Check lenth of the _relativeHumidity list and evaluate the contents.
    checkData3 = False
    barPress = []
    pressMultVal = False
    nonValue = True
    if len(barometricPressure_) != 0:
        try:
            if "Barometric Pressure" in barometricPressure_[2]:
                barPress = barometricPressure_[7:]
                checkData3 = True
                epwData = True
                epwStr = barometricPressure_[0:7]
        except: pass
        if checkData3 == False:
            for item in barometricPressure_:
                try:
                    if 0 <= float(item) <= 100:
                        barPress.append(float(item))
                        checkData3 = True
                    else: nonValue = False
                except:checkData3 = False
        if nonValue == False: checkData3 = False
        if len(barPress) > 1: pressMultVal = True
        if checkData3 == False:
            warning = 'barometricPressure_ input does not contain valid value.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        checkData3 = True
        barPress = [101325]
        print 'No value connected for barPress_.  It will be assumed that the barometric pressure is that at sea level: 101325 Pa.'
    
    
    #Check to make sure that the temperature, barometric pressure and humidity ratio lists are the same length.
    checkData4 = False
    if checkData1 == True and checkData2 == True and checkData3 == True:
        if airMultVal == True or humidMultVal == True or pressMultVal == True:
            listLenCheck = []
            if airMultVal == True: listLenCheck.append(len(airTemp))
            if humidMultVal == True: listLenCheck.append(len(relHumid))
            if pressMultVal == True: listLenCheck.append(len(barPress))
            
            if all(x == listLenCheck[0] for x in listLenCheck) == True:
                checkData4 = True
                calcLength = listLenCheck[0]
                
                def duplicateData(data, calcLength):
                    dupData = []
                    for count in range(calcLength):
                        dupData.append(data[0])
                    return dupData
                
                if airMultVal == False: airTemp = duplicateData(airTemp, calcLength)
                if humidMultVal == False: relHumid = duplicateData(relHumid, calcLength)
                if pressMultVal == False: barPress = duplicateData(barPress, calcLength)
            else:
                calcLength = None
                warning = 'If you have put in lists with multiple values for temperature or humidity, the lengths of these lists must match between temperature and humidity or you have a single value for a given parameter to be applied to all values in the list.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        else:
            checkData4 = True
            calcLength = 1
    else:
        calcLength = 0
    
    
    #Make sure that the lengths of the 4 other comfort parameters match and assign default values if nothing is connected.
    #Check lenth of the meanRadTemperature_ list and evaluate the contents.
    checkData5 = False
    radTemp = []
    radMultVal = False
    if len(meanRadTemperature_) != 0:
        for item in meanRadTemperature_:
            try:
                radTemp.append(float(item))
                checkData5 = True
            except: checkData5 = False
        if len(radTemp) > 1: radMultVal = True
        if checkData5 == False:
            warning = 'meanRadTemperature_ input does not contain valid temperature values in degrees Celcius.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        checkData5 = True
        radTemp = [23]
        print 'No value connected for meanRadTemperature_.  It will be assumed that the radiant temperature is equal to 23 degrees Celcius.'
    
    #Check lenth of the windSpeed_ list and evaluate the contents.
    checkData6 = False
    windSpeed = []
    windMultVal = False
    nonPositive = True
    if len(windSpeed_) != 0:
        for item in windSpeed_:
            try:
                if float(item) >= 0:
                    windSpeed.append(float(item))
                    checkData6 = True
                else: nonPositive = False
            except: checkData6 = False
        if nonPositive == False: checkData6 = False
        if len(windSpeed) > 1: windMultVal = True
        if checkData6 == False:
            warning = 'windSpeed_ input does not contain valid wind speed in meters per second.  Note that wind speed must be positive.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        checkData6 = True
        windSpeed = [0.05]
        print 'No value connected for windSpeed_.  It will be assumed that the wind speed is a low 0.05 m/s.'
    
    #Check lenth of the metabolicRate_ list and evaluate the contents.
    checkData7 = False
    metRate = []
    metMultVal = False
    nonVal = True
    if len(metabolicRate_) != 0:
        for item in metabolicRate_:
            try:
                if 0.5 <= float(item) <= 10:
                    metRate.append(float(item))
                    checkData7 = True
                else: nonVal = False
            except: checkData7 = False
        if checkData7 == False:
            try:
                if str(metabolicRate_[0]) == "Sleeping": metRate.append(0.7)
                elif str(metabolicRate_[0]) == "Reclining": metRate.append(0.8)
                elif str(metabolicRate_[0]) == "Sitting": metRate.append(1.0)
                elif str(metabolicRate_[0]) == "Typing": metRate.append(1.1)
                elif str(metabolicRate_[0]) == "Standing": metRate.append(1.2)
                elif str(metabolicRate_[0]) == "Driving": metRate.append(1.5)
                elif str(metabolicRate_[0]) == "Cooking": metRate.append(1.8)
                elif str(metabolicRate_[0]) == "House Cleaning": metRate.append(2.7)
                elif str(metabolicRate_[0]) == "Walking": metRate.append(1.7)
                elif str(metabolicRate_[0]) == "Walking 2mph": metRate.append(2.0)
                elif str(metabolicRate_[0]) == "Walking 3mph": metRate.append(2.6)
                elif str(metabolicRate_[0]) == "Walking 4mph": metRate.append(3.8)
                elif str(metabolicRate_[0]) == "Running 9mph": metRate.append(9.5)
                elif str(metabolicRate_[0]) == "Lifting 10lbs": metRate.append(2.1)
                elif str(metabolicRate_[0]) == "Lifting 100lbs": metRate.append(4.0)
                elif str(metabolicRate_[0]) == "Shoveling": metRate.append(4.4)
                elif str(metabolicRate_[0]) == "Dancing": metRate.append(3.4)
                elif str(metabolicRate_[0]) == "Basketball": metRate.append(6.3)
                else: pass
            except: pass
        if len(metRate) > 0: checkData7 = True
        if nonVal == False: checkData7 = False
        if len(metRate) > 1: metMultVal = True
        if checkData7 == False:
            warning = 'metabolicRate_ input does not contain valid value. Note that metabolicRate_ must be a value between 0.5 and 10. Any thing outside of that is frankly not human.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        checkData7 = True
        metRate = [1]
        print 'No value connected for metabolicRate_.  It will be assumed that the metabolic rate is that of a seated person at 1 met.'
    
    #Check lenth of the clothingLevel_ list and evaluate the contents.
    checkData8 = False
    cloLevel = []
    cloMultVal = False
    noVal = True
    if len(clothingLevel_) != 0:
        for item in clothingLevel_:
            try:
                if 0 <= float(item) <= 5:
                    cloLevel.append(float(item))
                    checkData8 = True
                else: noVal = False
            except: checkData8 = False
        if noVal == False: checkData8 = False
        if len(cloLevel) > 1: cloMultVal = True
        if checkData8 == False:
            warning = 'clothingLevel_ input does not contain valid value. Note that clothingLevel_ must be a value between 0 and 5. Any thing outside of that is frankly not human.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        checkData8 = True
        cloLevel = [1]
        print 'No value connected for clothingLevel_.  It will be assumed that the clothing level is that of a person wearing a 3-piece suit at 1 clo.'
    
    #Finally, for those lists of length greater than 1, check to make sure that they are all the same length.
    checkData9 = False
    if checkData5 == True and checkData6 == True and checkData7 == True and checkData8 == True:
        if radMultVal == True or windMultVal == True or metMultVal == True or cloMultVal == True:
            listLenCheck = []
            if radMultVal == True: listLenCheck.append(len(radTemp))
            if windMultVal == True: listLenCheck.append(len(windSpeed))
            if metMultVal == True: listLenCheck.append(len(metRate))
            if cloMultVal == True: listLenCheck.append(len(cloLevel))
            
            if all(x == listLenCheck[0] for x in listLenCheck) == True:
                checkData9 = True
                calcLength2 = listLenCheck[0]
                
                def duplicateData(data, calcLength2):
                    dupData = []
                    for count in range(calcLength2):
                        dupData.append(data[0])
                    return dupData
                
                if radMultVal == False: radTemp = duplicateData(radTemp, calcLength2)
                if windMultVal == False: windSpeed = duplicateData(windSpeed, calcLength2)
                if metMultVal == False: metRate = duplicateData(metRate, calcLength2)
                if cloMultVal == False: cloLevel = duplicateData(cloLevel, calcLength2)
                exWork = duplicateData([0], calcLength2)
            else:
                calcLength = None
                warning = 'If you have put in lists with multiple values for meanRadTemperature, windSpeed, clothingLevel, or metabolicRate, the lengths of these lists must match across the parameters or you have a single value for a given parameter to be applied to all values in the list.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        else:
            checkData9 = True
            calcLength2 = 1
            exWork = [0]
    else:
        calcLength2 = 0
        exWork = []
    
    # Check the humidity ratio upper and lower bounds and assign defaults if none are connected.
    checkData10 = True
    if comfortPar_ != []:
        try:
            eightyPercentComfortable = bool(comfortPar_[0])
            humidRatioUp = float(comfortPar_[1])
            humidRatioLow = float(comfortPar_[2])
        except:
            eightyPercentComfortable = False
            humidRatioUp = 0.030
            humidRatioLow = 0.0
            checkData10 = False
            warning = 'The comfortPar_ are not valid comfort parameters from the Ladybug_Comfort Parameters component.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        eightyPercentComfortable = False
        humidRatioUp = 0.030
        humidRatioLow = 0.0
    
    #Check the annualhourly data and conditional statement
    checkData11 = True
    annualHourlyData = _dryBulbTemperature + _relativeHumidity + annualHourlyData_
    if epwData == True and len(_dryBulbTemperature + _relativeHumidity) > 17533 and conditionalStatement_:
        titleStatement, patternList = checkConditionalStatement(annualHourlyData, conditionalStatement_)
        if titleStatement == -1 or patternList == -1:
            checkData11 = False
    else:
        titleStatement = None
        patternList = []
    
    #Check the passive strategy inputs to be sure that they are correct.
    checkData12 = True
    if len(passiveStrategy_) > 0:
        for item in passiveStrategy_:
            if item == "Evaporative Cooling" or item == "Thermal Mass + Night Vent"  or item == "Occupant Use of Fans" or item == "Internal Heat Gain" or item == "Humidification Only" or item == "Dehumidification Only" or item == "Dessicant Dehumidification": pass
            else: checkData12 = False
    if checkData12 == False:
        warning = 'Input for passiveStrategy_ is not valid.'
        print warning
        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    
    #Check to be sure that epw data has been connected and the calculation length is 8760 if the user has connected an analysis period.
    checkData13 = True
    if analysisPeriod_ != []:
        if epwData == True and calcLength == 8760: pass
        else:
            checkData13 = False
            warning = 'Analysis periods can only be used with EPW or EnergyPlus simulation data that is hourly for the full year.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    
    #Average all of the barometric pressures together (this is the pressure that will be used to construct the chart).
    if len(barPress) > 1: avgBarPress = (sum(barPress)/len(barPress))
    elif len(barPress) ==1: avgBarPress = barPress[0]
    else: avgBarPress = None
    
    #If all of the checkDatas have been good to go, let's give a final go ahead.
    if checkData1 == True and checkData2 == True and checkData3 == True and checkData4 == True and checkData5 == True and checkData6 == True and checkData7 == True and checkData8 == True and checkData9 == True and checkData10 == True and checkData11 == True and checkData12 == True and checkData13 == True:
        checkData = True
    else:
        checkData = False
    
    
    #Let's return everything we need.
    return checkData, epwData, epwStr, calcLength, airTemp, relHumid, barPress, avgBarPress, radTemp, windSpeed, metRate, cloLevel, exWork, humidRatioUp, humidRatioLow, calcLength2, eightyPercentComfortable, titleStatement, patternList



def checkConditionalStatement(annualHourlyData, conditionalStatement):
        lb_preparation = sc.sticky["ladybug_Preparation"]()
        indexList, listInfo = lb_preparation.separateList(annualHourlyData, lb_preparation.strToBeFound)
        
        letters = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
        # remove 'and' and 'or' from conditional statements
        csCleaned = conditionalStatement.replace('and', '',20000)
        csCleaned = csCleaned.replace('or', '',20000)
        
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
        
        selList = [[]] * len(listInfo)
        for i in range(len(listInfo)):
            selList[i] = annualHourlyData[indexList[i]+7:indexList[i+1]]
            if listInfo[i][4]!='Hourly' or listInfo[i][5]!=(1,1,1) or  listInfo[i][6]!=(12,31,24) or len(selList[i])!=8760:
                warning = 'At least one of the input data lists is not a valis ladybug hourly data! Please fix this issue and try again!\n List number = '+ `i+1`
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
                return -1, -1
        
        # replace the right list in the conditional statement
        statement = conditionalStatement.split(' ')
        finalStatement = 'pattern = '
        titleStatement = '...                         ...                         ...\n' +\
                         'Conditional Selection Applied:\n'
        
        for statemntPart in statement:
            statementCopy = str.Copy(statemntPart)
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
        try:
            for HOY in range(8760):
                exec(finalStatement)
                patternList.append(pattern)
        except Exception,e:
            warning = 'There is an error in the conditional statement:\n' + `e`
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
            return -1, -1
        
        return titleStatement, patternList


def drawPsychChart(avgBarPress, lb_comfortModels, legendFont, legendFontSize, scaleFactor, epwData, epwStr, lb_visualization):
    #Generate a list of temperatures that will be used to make the relative humidity curves.
    tempNum = range(-20, 55, 5)
    relHumidNum = range(10, 110, 10)
    
    #Set up a list of lists to hold the humidity ratio values and make a list of the barometric pressure.
    humidRatio = []
    barPressList = []
    for item in tempNum:
        barPressList.append(avgBarPress)
    
    #Get humidity ratio values for each of the temperatures at the different relative humidity levels.
    for relHumid in relHumidNum:
        relHumidList = []
        for item in tempNum:
            relHumidList.append(relHumid)
        HR, EN, vapPress, satPress = lb_comfortModels.calcHumidRatio(tempNum, relHumidList, barPressList)
        
        humidRatio.append(HR)
    
    #Put a scale factor on the humidty ratio to make it on the same scale as the temperature.
    for listCount, list in enumerate(humidRatio):
        for count, num in enumerate(list):
            humidRatio[listCount][count] = num*scaleFactor
    
    #Use the humidity ratio and the dry bulb temperature to create coordinates for the lines.
    humidLinePts = []
    for list in humidRatio:
        linePts = []
        for count, item in enumerate(list):
            linePts.append(rc.Geometry.Point3d(tempNum[count], item, 0))
        humidLinePts.append(linePts)
    
    #Make the chart relative humidity lines.
    humidCurves = []
    humidCurves.append(rc.Geometry.LineCurve(rc.Geometry.Point3d(tempNum[0], 0, 0), rc.Geometry.Point3d(tempNum[-1], 0, 0)))
    for pointList in humidLinePts:
        humidCurves.append(rc.Geometry.Curve.CreateInterpolatedCurve(pointList, 3))
    
    #If the humidity ratio goes larger than 0.030, chop off the humidity line there.
    maxLine = rc.Geometry.LineCurve(rc.Geometry.Point3d(tempNum[0], 0.03 * scaleFactor, 0), rc.Geometry.Point3d(tempNum[-1], 0.03 * scaleFactor, 0))
    maxBrep = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(maxLine, rc.Geometry.Vector3d.ZAxis))
    maxhumidCurves = []
    for curve in humidCurves:
        splitCrv = curve.Split(maxBrep, sc.doc.ModelAbsoluteTolerance)
        if len(splitCrv) != 0:
            maxhumidCurves.append(splitCrv[0])
        else:
            maxhumidCurves.append(curve)
    
    #Make the isothermal lines.
    tempCurves = []
    tempLabelBasePts = []
    tempText = []
    for count, temp in enumerate(tempNum):
        tempCurves.append(rc.Geometry.LineCurve(rc.Geometry.Point3d(temp, 0, 0), rc.Geometry.Point3d(temp, humidRatio[-1][count], 0)))
        tempLabelBasePts.append(rc.Geometry.Point3d(temp-0.75, -1, 0))
        tempText.append(str(temp))
    
    #Split the isothermal lines.
    maxTempCurves = []
    for curve in tempCurves:
        splitCrv = curve.Split(maxBrep, sc.doc.ModelAbsoluteTolerance)
        if len(splitCrv) != 0:
            maxTempCurves.append(splitCrv[0])
        else:
            maxTempCurves.append(curve)
    
    #Make the lines of constant humidity ratio.
    satBrep = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(humidCurves[-1], rc.Geometry.Vector3d.ZAxis))
    hrLines = []
    ratioList = []
    ratioText = []
    ratioBasePt = []
    ratioStart = (0.03*scaleFactor)/6
    for index in range(6):
        ratioList.append(ratioStart)
        ratioStart += (0.03*scaleFactor)/6
    for ratio in ratioList:
        hrLines.append(rc.Geometry.LineCurve(rc.Geometry.Point3d(tempNum[0], ratio, 0), rc.Geometry.Point3d(tempNum[-1], ratio, 0)))
        ratioText.append(str(ratio/scaleFactor))
        ratioBasePt.append(rc.Geometry.Point3d(tempNum[-1]+.5, ratio-.375, 0))
    maxHrLines = []
    for curve in hrLines:
        splitCrv = curve.Split(satBrep, sc.doc.ModelAbsoluteTolerance)
        if len(splitCrv) != 0:
            maxHrLines.append(splitCrv[-1])
        else:
            maxHrLines.append(curve)
    
    # Bring all of the curves into one list.
    chartCurves = []
    for curve in maxhumidCurves:
        chartCurves.append(curve)
    for curve in maxTempCurves:
        chartCurves.append(curve)
    for curve in maxHrLines:
        chartCurves.append(curve)
    
    #Set a default text height if the user has not provided one.
    if legendFontSize == None:
        legendFontSize = 0.6
    
    # Make the temperature text for the chart.
    tempLabels = []
    for count, text in enumerate(tempText):
        tempLabels.extend(lb_visualization.text2srf([text], [tempLabelBasePts[count]], legendFont, legendFontSize)[0])
    
    # Make the humidity ratio text for the chart.
    ratioLabels = []
    for count, text in enumerate(ratioText):
        ratioLabels.extend(lb_visualization.text2srf([text], [ratioBasePt[count]], legendFont, legendFontSize)[0])
    
    # Make the relative humidity text for the chart.
    relHumidBasePts = []
    relHumidTxt = []
    relHumidLabels = []
    for curve in maxhumidCurves[1:]:
        curvePt = curve.PointAtNormalizedLength(0.98)
        relHumidBasePts.append(rc.Geometry.Point3d(curvePt.X-1.75, curvePt.Y, 0))
    for humid in relHumidNum:
        relHumidTxt.append(str(humid)+"%")
    for count, text in enumerate(relHumidTxt[:-1]):
        relHumidLabels.extend(lb_visualization.text2srf([text], [relHumidBasePts[count]], legendFont, legendFontSize*.75)[0])
    
    #Make axis labels for the chart.
    xAxisLabels = []
    xAxisTxt = ["Dry Bulb Temperature"]
    xAxisPt = [rc.Geometry.Point3d(-20.5, -2.5, 0)]
    xAxisLabels.extend(lb_visualization.text2srf(xAxisTxt, xAxisPt, legendFont, legendFontSize*1.25)[0])
    
    yAxisLabels = []
    yAxisTxt = ["Humidity Ratio"]
    yAxisPt = [rc.Geometry.Point3d(55, 0.0245*scaleFactor, 0)]
    yAxisLabels.extend(lb_visualization.text2srf(yAxisTxt, yAxisPt, legendFont, legendFontSize*1.25)[0])
    rotateTransf = rc.Geometry.Transform.Rotation(1.57079633, rc.Geometry.Point3d(55, 0.0245*scaleFactor, 0))
    for geo in yAxisLabels:
        geo.Transform(rotateTransf)
    
    #Make the chart title.
    def getDateStr(start, end):
        stMonth, stDay, stHour, endMonth, endDay, endHour = lb_visualization.readRunPeriod((start, end), False)
        period = `stDay`+ ' ' + lb_visualization.monthList[stMonth-1] + ' ' + `stHour` + ':00' + \
                 " - " + `endDay`+ ' ' + lb_visualization.monthList[endMonth-1] + ' ' + `endHour` + ':00'
        return period
    
    titleLabels = []
    if epwData == True:
        titleTxt = ["Psychrometric Chart", epwStr[1]]
        if analysisPeriod_ == []:
            titleTxt.append(getDateStr(epwStr[5], epwStr[6]))
        else:
            titleTxt.append(getDateStr(analysisPeriod_[0], analysisPeriod_[1]))
    else: titleTxt = ["Psychrometric Chart", "Unlown Location", "Unknown Time Period"]
    titlePt = [rc.Geometry.Point3d(-19, 0.0295*scaleFactor, 0), rc.Geometry.Point3d(-19, (0.0295*scaleFactor)-(legendFontSize*2.5), 0),  rc.Geometry.Point3d(-19, (0.0295*scaleFactor)-(legendFontSize*5), 0)]
    for count, text in enumerate(titleTxt):
        titleLabels.extend(lb_visualization.text2srf([text], [titlePt[count]], legendFont, legendFontSize*1.5)[0])
    
    #Bring all text and curves together in one list.
    chartCrvAndText = []
    for item in chartCurves:
        chartCrvAndText.append(item)
    for item in tempLabels:
        chartCrvAndText.append(item)
    for item in ratioLabels:
        chartCrvAndText.append(item)
    for item in relHumidLabels:
        chartCrvAndText.append(item)
    for item in xAxisLabels:
        chartCrvAndText.append(item)
    for item in yAxisLabels:
        chartCrvAndText.append(item)
    for item in titleLabels:
        chartCrvAndText.append(item)
    
    
    return chartCrvAndText, humidCurves


def colorMesh(airTemp, relHumid, barPress, lb_preparation, lb_comfortModels, lb_visualization, scaleFactor, lowB, highB, customColors):
    # Make the full chart mesh
    
    #Generate a list of temperatures that will be used to make the mesh.
    tempNumMesh = range(-20, 51, 1)
    relHumidNumMesh = range(0, 105, 5)
    
    #Get humidity ratio values for each of the temperatures at the different relative humidity levels.
    humidRatioMesh = []
    for relHum in relHumidNumMesh:
        relHumidListMesh = []
        for item in tempNumMesh:
            relHumidListMesh.append(relHum)
        pressList = []
        for item in tempNumMesh:
            pressList.append(avgBarPress)
        HR, EN, vapPress, satPress = lb_comfortModels.calcHumidRatio(tempNumMesh, relHumidListMesh, pressList)
        for count, num in enumerate(HR):
            HR[count] = num*scaleFactor
        humidRatioMesh.append(HR)
    
    #Make the mesh faces.
    chartMesh = rc.Geometry.Mesh()
    meshFacePts = []
    
    for listCount, list in enumerate(humidRatioMesh[:-1]):
        for tempCount, temp in enumerate(tempNumMesh[:-1]):
            facePt1 = rc.Geometry.Point3d(temp, list[tempCount], 0)
            facePt2 = rc.Geometry.Point3d(temp, humidRatioMesh[listCount+1][tempCount], 0)
            facePt3 = rc.Geometry.Point3d(tempNumMesh[tempCount+1], humidRatioMesh[listCount+1][tempCount+1], 0)
            facePt4 = rc.Geometry.Point3d(tempNumMesh[tempCount+1], list[tempCount+1], 0)
            
            meshFacePts.append([facePt1, facePt2, facePt3, facePt4])
    
    for list in  meshFacePts:
        mesh = rc.Geometry.Mesh()
        for point in list:
            mesh.Vertices.Add(point)
        
        mesh.Faces.AddFace(0, 1, 2, 3)
        chartMesh.Append(mesh)
    uncoloredMesh = chartMesh
    
    #Calculate the humidity ratio for each of the hours of the year and use this to make points for the chart.
    HR, EN, vapPress, satPress = lb_comfortModels.calcHumidRatio(airTemp, relHumid, barPress)
    hourPts = []
    for count, ratio in enumerate(HR):
        hourPts.append(rc.Geometry.Point3d(airTemp[count], ratio*scaleFactor, 0))
    
    #Make a list to hold values for all of the mesh faces.
    meshFrequency = []
    for count, value in enumerate(range(0, 100, 5)):
        meshFrequency.append([])
        for face in range(-20, 50, 1):
            meshFrequency[count].append([])
    
    #Bin the input humidity and temperatures into categories that correspond to the mesh faces.
    def getTempIndex(hour):
        if airTemp[hour] > -20 and airTemp[hour] < 50:
            index  = int(round(airTemp[hour] +19.5))
        else: index = -1
        return index
    
    for hour, humid in enumerate(relHumid):
        tempIndex = getTempIndex(hour)
        if tempIndex != -1:
            if humid < 5: meshFrequency[0][tempIndex].append(1)
            elif humid < 10: meshFrequency[1][tempIndex].append(1)
            elif humid < 15:meshFrequency[2][tempIndex].append(1)
            elif humid < 20:meshFrequency[3][tempIndex].append(1)
            elif humid < 25:meshFrequency[4][tempIndex].append(1)
            elif humid < 30:meshFrequency[5][tempIndex].append(1)
            elif humid < 35:meshFrequency[6][tempIndex].append(1)
            elif humid < 40:meshFrequency[7][tempIndex].append(1)
            elif humid < 45:meshFrequency[8][tempIndex].append(1)
            elif humid < 50:meshFrequency[9][tempIndex].append(1)
            elif humid < 55:meshFrequency[10][tempIndex].append(1)
            elif humid < 60:meshFrequency[11][tempIndex].append(1)
            elif humid < 65:meshFrequency[12][tempIndex].append(1)
            elif humid < 70:meshFrequency[13][tempIndex].append(1)
            elif humid < 75:meshFrequency[14][tempIndex].append(1)
            elif humid < 80:meshFrequency[15][tempIndex].append(1)
            elif humid < 85:meshFrequency[16][tempIndex].append(1)
            elif humid < 90:meshFrequency[17][tempIndex].append(1)
            elif humid < 95:meshFrequency[18][tempIndex].append(1)
            else: meshFrequency[19][tempIndex].append(1)
    
    #Sum all of the lists together to get the frequency.
    finalMeshFrequency = []
    for humidlist in meshFrequency:
        for templist in humidlist:
            finalMeshFrequency.append(sum(templist))
    
    #Get a list of colors
    colors = lb_visualization.gradientColor(finalMeshFrequency, lowB, highB, customColors)
    
    # color the mesh faces.
    uncoloredMesh.VertexColors.CreateMonotoneMesh(System.Drawing.Color.Gray)
    
    for srfNum in range (uncoloredMesh.Faces.Count):
        uncoloredMesh.VertexColors[4 * srfNum + 0] = colors[srfNum]
        uncoloredMesh.VertexColors[4 * srfNum + 1] = colors[srfNum]
        uncoloredMesh.VertexColors[4 * srfNum + 3] = colors[srfNum]
        uncoloredMesh.VertexColors[4 * srfNum + 2] = colors[srfNum]
    
    # Remove the mesh faces that do not have any hour associated with them.
    cullFaceIndices = []
    for count, freq in enumerate(finalMeshFrequency):
        if freq == 0:
            cullFaceIndices.append(count)
    uncoloredMesh.Faces.DeleteFaces(cullFaceIndices)
    
    #Return everything that's useful.
    return hourPts, uncoloredMesh, finalMeshFrequency


def unionAllCurves(Curves):
    res = []
    
    for curveCount in range(0, len(Curves), 2):
        try:
            sc.doc = rc.RhinoDoc.ActiveDoc #change target document
            
            rs.EnableRedraw(False)
            
            guid1 = sc.doc.Objects.AddCurve(Curves[curveCount])
            guid2 = sc.doc.Objects.AddCurve(Curves[curveCount + 1])
            all = rs.CurveBooleanUnion([guid1, guid2])
            rs.DeleteObjects(guid1)
            rs.DeleteObjects(guid2)
            if all:
                a = [rs.coercegeometry(a) for a in all]
                for g in a: g.EnsurePrivateCopy() #must ensure copy if we delete from doc
            
            rs.DeleteObjects(all)
            
            sc.doc = ghdoc #put back document
            rs.EnableRedraw()
            
            if a == None:
                a = [Curves[curveCount], Curves[curveCount + 1]]
        except:
            rs.DeleteObjects(guid1)
            sc.doc = ghdoc #put back document
            rs.EnableRedraw()
            a = [Curves[curveCount]]
        
        if a:
            res.extend(a)
    return res


def calcComfAndStrategyPolygons(radTemp, windSpeed, metRate, cloLevel, exWork, humidRatioUp, humidRatioLow, passiveStrategy, relHumidLines, calcLengthComf, lb_comfortModels, chartBoundary, scaleFactor, eightyPercentComfort):
    #Take just the top middle and bottom lines for making the comofrt range in order to speed up the calculation.
    relHumidLines = [relHumidLines[0], relHumidLines[5], relHumidLines[10]]
    
    #Make a comfort polyline for each of the variables in the comfCalcLength.
    #First get the points that represent the lower and upper bound of comfort at each relative humidty line.
    comfPolyLinePts = []
    for index in range(calcLengthComf):
        upTemperPts = []
        downTemperPts = []
        for count, humidity in enumerate(range(0,150,50)):
            upTemper, downTemper = lb_comfortModels.calcComfRange(radTemp[index]+2, radTemp[index]-2, radTemp[index], windSpeed[index], humidity, metRate[index], cloLevel[index], exWork[index], eightyPercentComfort)
            
            if upTemper < 50:
                if upTemper > -20:
                    upIntersect = rc.Geometry.Intersect.Intersection.CurvePlane(relHumidLines[count], rc.Geometry.Plane(rc.Geometry.Point3d(upTemper, 0,0), rc.Geometry.Vector3d.XAxis), sc.doc.ModelAbsoluteTolerance)[0].PointA
                else: upIntersect = relHumidLines[count].PointAtStart
            else: upIntersect = relHumidLines[count].PointAtEnd
            upTemperPts.append(upIntersect)
            
            if downTemper < 50:
                if downTemper > -20:
                    downIntersect = rc.Geometry.Intersect.Intersection.CurvePlane(relHumidLines[count], rc.Geometry.Plane(rc.Geometry.Point3d(downTemper, 0,0), rc.Geometry.Vector3d.XAxis), sc.doc.ModelAbsoluteTolerance)[0].PointA
                else: downIntersect = relHumidLines[count].PointAtStart
            else: upIntersect = relHumidLines[count].PointAtEnd
            downTemperPts.append(downIntersect)
        comfPolyLinePts.append([upTemperPts, downTemperPts])
    
    #Use the collected points to define a boundary curve around the comfort zone.
    chartBoundaryBrep = rc.Geometry.Surface.CreateExtrusion(chartBoundary, rc.Geometry.Vector3d.ZAxis)
    comfortCurves = []
    comfortCrvSegments = []
    for futurePoly in comfPolyLinePts:
        upperBoundary = rc.Geometry.Curve.CreateInterpolatedCurve(futurePoly[0], 3)
        lowerBoundary = rc.Geometry.Curve.CreateInterpolatedCurve(futurePoly[1], 3)
        try:
            upperBoundary = upperBoundary.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)[0]
            lowerBoundary = upperBoundary.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)[0]
        except: pass
        upperBrep = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(upperBoundary, rc.Geometry.Vector3d.ZAxis))
        lowerBrep = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(lowerBoundary, rc.Geometry.Vector3d.ZAxis))
        splitCurve = chartBoundary.Split(upperBrep, sc.doc.ModelAbsoluteTolerance)[0]
        try:
            bottomCurve = splitCurve.Split(lowerBrep, sc.doc.ModelAbsoluteTolerance)[0]
            topCurve = splitCurve.Split(lowerBrep, sc.doc.ModelAbsoluteTolerance)[2]
            joinedCurves = rc.Geometry.Curve.JoinCurves([upperBoundary, topCurve, lowerBoundary, bottomCurve])[0]
            comfortCrvSegments.append([upperBoundary, lowerBoundary, topCurve, bottomCurve])
            comfortCurves.append(joinedCurves)
        except:
            warning = 'Comfort polygon has fallen completely off of the psych chart.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    if comfortCurves != []:
        #If the user has speified a max or a min humidity ratio, use that to trim the comfort boundary.
        if humidRatioUp != 0.03:
            splittingLineUp = rc.Geometry.LineCurve(rc.Geometry.Point3d(-30, humidRatioUp*scaleFactor, 0), rc.Geometry.Point3d(60, humidRatioUp*scaleFactor, 0))
            splittingBrepUp = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(splittingLineUp, rc.Geometry.Vector3d.ZAxis))
            for count, curve in enumerate(comfortCurves):
                try:
                    splitCurves = curve.Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)
                    if len(splitCurves) > 1:
                        joinedComfBound = rc.Geometry.Curve.JoinCurves([splitCurves[0], rc.Geometry.LineCurve(splitCurves[0].PointAtStart, splitCurves[0].PointAtEnd)])[0]
                        comfortCurves[count] = joinedComfBound
                    else: pass
                except: pass
        
        if humidRatioLow != 0:
            splittingLineLow = rc.Geometry.LineCurve(rc.Geometry.Point3d(-30, humidRatioLow*scaleFactor, 0), rc.Geometry.Point3d(60, humidRatioLow*scaleFactor, 0))
            splittingBrepLow = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(splittingLineLow, rc.Geometry.Vector3d.ZAxis))
            for count, curve in enumerate(comfortCurves):
                try:
                    splitCurves = curve.Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)
                    if len(splitCurves) > 1:
                        joinedComfBound = rc.Geometry.Curve.JoinCurves([splitCurves[1], rc.Geometry.LineCurve(splitCurves[1].PointAtStart, splitCurves[1].PointAtEnd)])[0]
                        comfortCurves[count] = joinedComfBound
                    else: pass
                except: pass
        
        #If the user has multiple comfort polygons and has selected to merge them, them merge them.
        mergedCurvesFinal = comfortCurves
        if len(comfortCurves) > 1 and mergeComfPolygons_ == True:
            listLength = len(comfortCurves)
            count  = 0
            while len(mergedCurvesFinal) > 1 and count < int(listLength/2) + 1:
                mergedCurvesFinal = unionAllCurves(mergedCurvesFinal)
                count += 1
            
            if mergedCurvesFinal == None:
                mergedCurvesFinal = comfortCurves
                print "Attempt to merge comfort curves failed.  Component will return multiple comfort boundaries."
        
        #Add the comfort polygons to the strategy list.
        strategyListTest = []
        if len(mergedCurvesFinal) == 1:
            strategyListTest.append("Comfort")
        else:
            for count, curve in enumerate(mergedCurvesFinal):
                strategyListTest.append("Comfort " + str(count))
        
        #Organize data to be used to construct the strategy curves
        windSpeed.sort()
        windSpeed[0] = windSpeed[-1]
        cloLevel.sort()
        cloLevel[0] = cloLevel[0]
        upBoundXList = []
        upBoundCrv = []
        lowBoundXList = []
        lowBoundCrv = []
        for crvList in comfortCrvSegments:
            upBoundXList.append(crvList[0].PointAtStart.X)
            upBoundCrv.append(crvList[0])
            lowBoundXList.append(crvList[1].PointAtEnd.X)
            lowBoundCrv.append(crvList[1])
        upBoundXList, upBoundCrv = zip(*sorted(zip(upBoundXList, upBoundCrv)))
        comfortCrvSegments[0][0] = upBoundCrv[-1]
        lowBoundXList, lowBoundCrv = zip(*sorted(zip(lowBoundXList, lowBoundCrv)))
        comfortCrvSegments[0][1] = lowBoundCrv[0]
        
        #Define a function to offset curves and return things that will stand out on the psychrometric chart.
        def outlineCurve(curve):
            try:
                offsetCrv = curve.Offset(rc.Geometry.Plane.WorldXY, 0.15, sc.doc.ModelAbsoluteTolerance, rc.Geometry.CurveOffsetCornerStyle.Sharp)[0]
                finalBrep = (rc.Geometry.Brep.CreatePlanarBreps([curve, offsetCrv])[0])
                if finalBrep.Edges.Count < 3:
                    finalBrep = curve
            except:
                finalBrep = curve
                warning = "Creating an outline of one of the comfort or strategy curves failed.  Component will return a solid brep."
                print warning
                w = gh.GH_RuntimeMessageLevel.Warning
                ghenv.Component.AddRuntimeMessage(w, warning)
            return finalBrep
        
        #Define a function that will extract the points from a polycurve line
        def getCurvePoints(curve):
            exploCurve = rc.Geometry.PolyCurve.DuplicateSegments(curve)
            individPts = []
            for line in exploCurve:
                individPts.append(line.PointAtStart)
            return individPts
        
        #Turn the comfort curve into a brep that will show up well on the chart.
        finalComfortBreps = []
        for curve in mergedCurvesFinal:
            finalComfortBreps.append(outlineCurve(curve))
        
        #Evaluate each of the connected strategies and draw polygons for them on the chart.
        passiveStrategyCurves = []
        passiveStrategyBreps = []
        
        if len(passiveStrategy) != 0:
            #If the user has connected strategy parameters, read them out.
            if strategyPar_ != []:
                if len(strategyPar_) == 4:
                    tempAboveComf = strategyPar_[0]
                    tempBelowComf = strategyPar_[1]
                    maxWindSpeed = strategyPar_[2]
                    bldgBalPt = strategyPar_[3]
                else:
                    warning = 'The strategyPar_ list does not contain valid data.  StrategyPar_ must come from the "Ladybug_Passive Strategy Parameters" component.'
                    print warning
                    w = gh.GH_RuntimeMessageLevel.Warning
                    ghenv.Component.AddRuntimeMessage(w, warning)
                    tempAboveComf = 16.7
                    tempBelowComf = 2.8
                    maxWindSpeed = 1.5
                    bldgBalPt = 12.8
            else:
                tempAboveComf = 16.7
                tempBelowComf = 2.8
                maxWindSpeed = 1.5
                bldgBalPt = 12.8
            
            for comfCount, comfortCurve in enumerate([mergedCurvesFinal[0]]):
                
                #If the user has hooked up evaporative cooling, add an evaporative cooling curve to the chart.
                if "Evaporative Cooling" in passiveStrategy:
                    comfPolygonPts = getCurvePoints(comfortCurve)
                    ptXYSum = []
                    for point in comfPolygonPts:
                        ptXYSum.append(point.X + point.Y)
                    ptXYSum, comfPolygonPts = zip(*sorted(zip(ptXYSum, comfPolygonPts)))
                    startPt = comfPolygonPts[-1]
                    #Calculate the enthalpy at the start point.
                    enthalpy = (startPt.X * (1.01 + 0.00189*((startPt.Y/scaleFactor)*1000))) + 2.5*((startPt.Y/scaleFactor)*1000)
                    #If the temperature at the edge of the chart is 50C, use that to find another point of the line.
                    newHR = (((enthalpy - 50.5) / 2.5945)/1000)* scaleFactor
                    endPt = rc.Geometry.Point3d(50, newHR, 0)
                    evapCoolLine = rc.Geometry.LineCurve(startPt, endPt)
                    #If there is a minimum humidity ratio, use the comfort upper curve. otherwise, use the comfort bottom curve.
                    if humidRatioLow == 0 and humidRatioUp*scaleFactor >= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                        boundaryLine = comfortCrvSegments[comfCount][0]
                        joinedEvapBound = rc.Geometry.Curve.JoinCurves([evapCoolLine, boundaryLine])[0]
                    elif humidRatioLow == 0:
                        boundaryLine = comfortCrvSegments[comfCount][0]
                        boundaryLine = boundaryLine.Split(rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(evapCoolLine, rc.Geometry.Vector3d.ZAxis)), sc.doc.ModelAbsoluteTolerance)[0]
                        joinedEvapBound = rc.Geometry.Curve.JoinCurves([evapCoolLine, boundaryLine])[0]
                    elif humidRatioUp*scaleFactor >= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                        boundaryLine = comfortCrvSegments[comfCount][1]
                        boundaryLine = boundaryLine.Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[0]
                        transVector = rc.Geometry.Vector3d.Subtract(rc.Geometry.Vector3d(boundaryLine.PointAtEnd.X, boundaryLine.PointAtEnd.Y,boundaryLine.PointAtEnd.Z), rc.Geometry.Vector3d(evapCoolLine.PointAtStart.X, evapCoolLine.PointAtStart.Y,evapCoolLine.PointAtStart.Z))
                        evapLine2 = evapCoolLine.DuplicateCurve()
                        evapLine2.Translate(transVector)
                        evapLine2 = evapLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)[0]
                        comfLine2 = comfortCrvSegments[comfCount][0].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        comfLine1 = rc.Geometry.LineCurve(comfLine2.PointAtStart, boundaryLine.PointAtEnd)
                        joinedEvapBound = rc.Geometry.Curve.JoinCurves([evapCoolLine, evapLine2, comfLine1, comfLine2])[0]
                    else:
                        boundaryLine = comfortCrvSegments[comfCount][1]
                        boundaryLine = boundaryLine.Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[0]
                        transVector = rc.Geometry.Vector3d.Subtract(rc.Geometry.Vector3d(boundaryLine.PointAtEnd.X, boundaryLine.PointAtEnd.Y,boundaryLine.PointAtEnd.Z), rc.Geometry.Vector3d(evapCoolLine.PointAtStart.X, evapCoolLine.PointAtStart.Y,evapCoolLine.PointAtStart.Z))
                        evapLine2 = evapCoolLine.DuplicateCurve()
                        evapLine2.Translate(transVector)
                        evapLine2 = evapLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)[0]
                        comfLine2 = comfortCrvSegments[comfCount][0].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        comfLine2 = comfLine2.Split(rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(evapCoolLine, rc.Geometry.Vector3d.ZAxis)), sc.doc.ModelAbsoluteTolerance)[0]
                        comfLine1 = rc.Geometry.LineCurve(comfLine2.PointAtStart, boundaryLine.PointAtEnd)
                        joinedEvapBound = rc.Geometry.Curve.JoinCurves([evapCoolLine, evapLine2, comfLine1, comfLine2])[0]
                    joinedEvapBrep = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(joinedEvapBound, rc.Geometry.Vector3d.ZAxis))
                    chartBoundSegments = chartBoundary.Split(joinedEvapBrep, sc.doc.ModelAbsoluteTolerance)
                    if len(chartBoundSegments) == 3:
                        segment = chartBoundSegments[2]
                    else: segment = chartBoundSegments[1]
                    joinedEvapCoolBound = rc.Geometry.Curve.JoinCurves([joinedEvapBound, segment])[0]
                    passiveStrategyCurves.append(joinedEvapCoolBound)
                    passiveStrategyBreps.append(outlineCurve(joinedEvapCoolBound))
                    strategyListTest.append("Evaporative Cooling")
                
                #If the user has hooked up thermal mass and night flushing, add an thernal mass curve to the chart.
                if "Thermal Mass + Night Vent" in passiveStrategy:
                    #If there is a minimum humidity ratio, use the comfort upper curve. Otherwise, use the comfort bottom curve.
                    ChartBoundCheck = 0
                    if humidRatioLow == 0.0 and humidRatioUp*scaleFactor >= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                        strategyLine = rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Point3d(comfortCrvSegments[comfCount][0].PointAtEnd.X+tempAboveComf, comfortCrvSegments[comfCount][0].PointAtEnd.Y, 0))
                        boundaryLine = comfortCrvSegments[comfCount][0]
                        transformMass = rc.Geometry.Transform.Translation(tempAboveComf, 0, 0)
                        boundaryLine2 = boundaryLine.DuplicateCurve()
                        boundaryLine2.Transform(transformMass)
                        splitCrv = boundaryLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)
                        if len(splitCrv) == 2:
                            boundaryLine2 = splitCrv[1]
                            ChartBoundCheck = 2
                        else: ChartBoundCheck = 1
                        joinedMassBound = rc.Geometry.Curve.JoinCurves([strategyLine, boundaryLine, boundaryLine2])[0]
                    elif humidRatioLow == 0.0:
                        cornerPt = rc.Geometry.Intersect.Intersection.CurveCurve(splittingLineUp, comfortCrvSegments[comfCount][0], sc.doc.ModelAbsoluteTolerance, sc.doc.ModelAbsoluteTolerance)[0].PointA
                        strategyLine = rc.Geometry.LineCurve(cornerPt, rc.Geometry.Point3d(cornerPt.X+tempAboveComf, humidRatioUp*scaleFactor, 0))
                        boundaryLine = comfortCrvSegments[comfCount][0].Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0]
                        transformMass = rc.Geometry.Transform.Translation(tempAboveComf, 0, 0)
                        boundaryLine2 = boundaryLine.DuplicateCurve()
                        boundaryLine2.Transform(transformMass)
                        splitCrv = boundaryLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)
                        if len(splitCrv) == 2:
                            boundaryLine2 = splitCrv[1]
                            ChartBoundCheck = 2
                        else: ChartBoundCheck = 1
                        joinedMassBound = rc.Geometry.Curve.JoinCurves([strategyLine, boundaryLine, boundaryLine2])[0]
                    elif humidRatioUp*scaleFactor >= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                        strategyLine1 = rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Point3d(comfortCrvSegments[comfCount][0].PointAtEnd.X+tempAboveComf, comfortCrvSegments[comfCount][0].PointAtEnd.Y, 0))
                        cornerPt = rc.Geometry.Intersect.Intersection.CurveCurve(splittingLineLow, comfortCrvSegments[comfCount][0], sc.doc.ModelAbsoluteTolerance, sc.doc.ModelAbsoluteTolerance)[0].PointA
                        strategyLine2 = rc.Geometry.LineCurve(cornerPt, rc.Geometry.Point3d(cornerPt.X+tempAboveComf, humidRatioLow*scaleFactor, 0))
                        splitCrv1 = strategyLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)
                        if len(splitCrv1) == 2:
                            strategyLine2 = splitCrv1[0]
                        boundaryLine = comfortCrvSegments[comfCount][0]
                        boundaryLine = boundaryLine.Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[-1]
                        transformMass = rc.Geometry.Transform.Translation(tempAboveComf, 0, 0)
                        boundaryLine2 = boundaryLine.DuplicateCurve()
                        boundaryLine2.Transform(transformMass)
                        splitCrv = boundaryLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)
                        if len(splitCrv) == 2:
                            boundaryLine2 = splitCrv[1]
                            ChartBoundCheck = 0
                        else: ChartBoundCheck = 3
                        joinedMassBound = rc.Geometry.Curve.JoinCurves([strategyLine1, boundaryLine, strategyLine2, boundaryLine2])[0]
                    else:
                        cornerPt1 = rc.Geometry.Intersect.Intersection.CurveCurve(splittingLineUp, comfortCrvSegments[comfCount][0], sc.doc.ModelAbsoluteTolerance, sc.doc.ModelAbsoluteTolerance)[0].PointA
                        cornerPt2 = rc.Geometry.Intersect.Intersection.CurveCurve(splittingLineLow, comfortCrvSegments[comfCount][0], sc.doc.ModelAbsoluteTolerance, sc.doc.ModelAbsoluteTolerance)[0].PointA
                        strategyLine1 = rc.Geometry.LineCurve(cornerPt1, rc.Geometry.Point3d(cornerPt1.X+tempAboveComf, humidRatioUp*scaleFactor, 0))
                        strategyLine2 = rc.Geometry.LineCurve(cornerPt2, rc.Geometry.Point3d(cornerPt2.X+tempAboveComf, humidRatioLow*scaleFactor, 0))
                        splitCrv1 = strategyLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)
                        if len(splitCrv1) == 2:
                            strategyLine2 = splitCrv1[0]
                        boundaryLine = comfortCrvSegments[comfCount][0]
                        boundaryLine = boundaryLine.Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[-1]
                        boundaryLine = boundaryLine.Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0]
                        transformMass = rc.Geometry.Transform.Translation(tempAboveComf, 0, 0)
                        boundaryLine2 = boundaryLine.DuplicateCurve()
                        boundaryLine2.Transform(transformMass)
                        splitCrv = boundaryLine2.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)
                        if len(splitCrv) == 2:
                            boundaryLine2 = splitCrv[1]
                            ChartBoundCheck = 0
                        else: ChartBoundCheck = 3
                        joinedMassBound = rc.Geometry.Curve.JoinCurves([strategyLine1, boundaryLine, strategyLine2, boundaryLine2])[0]
                    
                    joinedMassBrep = rc.Geometry.Brep.CreateFromSurface(rc.Geometry.Surface.CreateExtrusion(joinedMassBound, rc.Geometry.Vector3d.ZAxis))
                    chartBoundSegments = chartBoundary.Split(joinedMassBrep, sc.doc.ModelAbsoluteTolerance)
                    if ChartBoundCheck == 1:
                        segment = chartBoundSegments[0]
                    elif ChartBoundCheck == 2:
                        try: segment = chartBoundSegments[2]
                        except: segment = chartBoundSegments[1]
                    elif ChartBoundCheck == 0: segment = chartBoundSegments[1]
                    if len(chartBoundSegments) != 0: joinedMassCoolBound = rc.Geometry.Curve.JoinCurves([joinedMassBound, segment])[0]
                    else: joinedMassCoolBound = joinedMassBound
                    passiveStrategyCurves.append(joinedMassCoolBound)
                    passiveStrategyBreps.append(outlineCurve(joinedMassCoolBound))
                    strategyListTest.append("Thermal Mass + Night Vent")
                    #passiveStrategyBreps.append(joinedMassCoolBound)
                
                #If the user has hooked up natural ventilation, add a natural ventilation curve to the chart.
                if "Occupant Use of Fans" in passiveStrategy and windSpeed[comfCount] < maxWindSpeed:
                    #Calculate the upper boundary of Natural ventilation.
                    upTemperPts = []
                    for count, humidity in enumerate(range(0,150,50)):
                        upTemper, downTemper = lb_comfortModels.calcComfRange(radTemp[comfCount]+2, radTemp[comfCount]-2, radTemp[comfCount], maxWindSpeed, humidity, metRate[comfCount], cloLevel[comfCount], exWork[comfCount], eightyPercentComfort)
                        
                        if upTemper < 50:
                            if upTemper > -20:
                                upIntersect = rc.Geometry.Intersect.Intersection.CurvePlane(relHumidLines[count], rc.Geometry.Plane(rc.Geometry.Point3d(upTemper, 0,0), rc.Geometry.Vector3d.XAxis), sc.doc.ModelAbsoluteTolerance)[0].PointA
                            else: upIntersect = relHumidLines[count].PointAtStart
                        else: upIntersect = relHumidLines[count].PointAtEnd
                        upTemperPts.append(upIntersect)
                    natVentBoundary = rc.Geometry.Curve.CreateInterpolatedCurve(upTemperPts, 3)
                    try: natVentBoundary = upperBoundary.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)[0]
                    except: pass
                    
                    if humidRatioLow == 0 and humidRatioUp*scaleFactor >= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                        strategyLine1 = rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Intersect.Intersection.CurveCurve(natVentBoundary, rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Point3d(50, comfortCrvSegments[comfCount][0].PointAtEnd.Y, 0)), sc.doc.ModelAbsoluteTolerance, sc.doc.ModelAbsoluteTolerance)[0].PointA)
                        strategyLine2 = rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtStart, natVentBoundary.PointAtStart)
                        boundaryLine = comfortCrvSegments[comfCount][0]
                        natVentLine = natVentBoundary.Split(rc.Geometry.Surface.CreateExtrusion(rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Point3d(50, comfortCrvSegments[comfCount][0].PointAtEnd.Y, 0)), rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0]
                    elif humidRatioLow == 0:
                        strategyLine1 = rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0].PointAtEnd, natVentBoundary.Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0].PointAtEnd)
                        strategyLine2 = rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtStart, natVentBoundary.PointAtStart)
                        boundaryLine = comfortCrvSegments[comfCount][0].Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0]
                        natVentLine = natVentBoundary.Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0]
                    elif humidRatioUp*scaleFactor >= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                        strategyLine1 = rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Intersect.Intersection.CurveCurve(natVentBoundary, rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Point3d(50, comfortCrvSegments[comfCount][0].PointAtEnd.Y, 0)), sc.doc.ModelAbsoluteTolerance, sc.doc.ModelAbsoluteTolerance)[0].PointA)
                        natVentLine = natVentBoundary.Split(rc.Geometry.Surface.CreateExtrusion(rc.Geometry.LineCurve(comfortCrvSegments[comfCount][0].PointAtEnd, rc.Geometry.Point3d(50, comfortCrvSegments[comfCount][0].PointAtEnd.Y, 0)), rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        boundaryLine = comfortCrvSegments[comfCount][0].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        strategyLine2 = rc.Geometry.LineCurve(boundaryLine.PointAtStart, natVentLine.PointAtStart)
                    else:
                        natVentLine = natVentBoundary.Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        boundaryLine = comfortCrvSegments[comfCount][0].Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        strategyLine1 = rc.Geometry.LineCurve(boundaryLine.PointAtStart, natVentLine.PointAtStart)
                        strategyLine2 = rc.Geometry.LineCurve(boundaryLine.PointAtEnd, natVentLine.PointAtEnd)
                    joinedNatVentBound = rc.Geometry.Curve.JoinCurves([strategyLine1, boundaryLine, strategyLine2, natVentLine])[0]
                    passiveStrategyCurves.append(joinedNatVentBound)
                    passiveStrategyBreps.append(outlineCurve(joinedNatVentBound))
                    strategyListTest.append("Occupant Use of Fans")
                
                #If the user has hooked up internal gain, add an internal gain curve to the chart.
                if "Internal Heat Gain" in passiveStrategy:
                    heatBoundary = rc.Geometry.LineCurve(rc.Geometry.Point3d(bldgBalPt, 0, 0), rc.Geometry.Point3d(bldgBalPt, scaleFactor*0.03, 0))
                    heatBoundary = heatBoundary.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)[0]
                    
                    if humidRatioLow == 0:
                        boundaryLine = comfortCrvSegments[comfCount][1]
                        strategyLine1 = chartBoundary.Split(rc.Geometry.Surface.CreateExtrusion(boundaryLine, rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0].Split(rc.Geometry.Surface.CreateExtrusion(heatBoundary, rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0]
                        strategyLine2 = chartBoundary.Split(rc.Geometry.Surface.CreateExtrusion(boundaryLine, rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0].Split(rc.Geometry.Surface.CreateExtrusion(heatBoundary, rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[2]
                        joinedHeatBound = rc.Geometry.Curve.JoinCurves([strategyLine1, boundaryLine, strategyLine2, heatBoundary])[0]
                    else:
                        boundaryLine = comfortCrvSegments[comfCount][1].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        heatBoundaryNew = heatBoundary.Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[1]
                        strategyLine1 = chartBoundary.Split(rc.Geometry.Surface.CreateExtrusion(comfortCrvSegments[comfCount][1], rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0].Split(rc.Geometry.Surface.CreateExtrusion(heatBoundary, rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[2]
                        strategyLine2 = rc.Geometry.LineCurve(boundaryLine.PointAtStart, heatBoundaryNew.PointAtStart)
                        joinedHeatBound = rc.Geometry.Curve.JoinCurves([strategyLine1, boundaryLine, strategyLine2, heatBoundaryNew])[0]
                    
                    passiveStrategyCurves.append(joinedHeatBound)
                    passiveStrategyBreps.append(outlineCurve(joinedHeatBound))
                    strategyListTest.append("Internal Heat Gain")
                
                #If the user has hooked up humidification only, add a humidification only curve to the chart.
                if "Humidification Only" in passiveStrategy and humidRatioLow != 0:
                    boundary1 = comfortCrvSegments[comfCount][1].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[0]
                    boundary2 = comfortCrvSegments[comfCount][0].Split(splittingBrepLow, sc.doc.ModelAbsoluteTolerance)[0]
                    boundary3 = rc.Geometry.LineCurve(boundary1.PointAtStart, boundary2.PointAtStart)
                    boundary4 = rc.Geometry.LineCurve(boundary1.PointAtEnd, boundary2.PointAtEnd)
                    
                    joinedHumidBound = rc.Geometry.Curve.JoinCurves([boundary1, boundary2, boundary3, boundary4])[0]
                    
                    passiveStrategyCurves.append(joinedHumidBound)
                    passiveStrategyBreps.append(outlineCurve(joinedHumidBound))
                    strategyListTest.append("Humidification Only")
                
                #If the user has hooked up dehumidification only, add a dehumidification only curve to the chart.
                if "Dessicant Dehumidification" in passiveStrategy and humidRatioUp*scaleFactor <= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                    comfPolygonPts = getCurvePoints(comfortCurve)
                    ptXYSum = []
                    for point in comfPolygonPts:
                        ptXYSum.append(point.X + point.Y)
                    ptXYSum, comfPolygonPts = zip(*sorted(zip(ptXYSum, comfPolygonPts)))
                    startPt = comfPolygonPts[-1]
                    #Calculate the enthalpy at the start point.
                    enthalpy = (startPt.X * (1.01 + 0.00189*((startPt.Y/scaleFactor)*1000))) + 2.5*((startPt.Y/scaleFactor)*1000)
                    #If the temperature at the edge of the chart is 50C, use that to find another point of the line.
                    newHR = (((enthalpy + 20.2) / 2.4622)/1000)* scaleFactor
                    endPt = rc.Geometry.Point3d(-20, newHR, 0)
                    dessicantLine = rc.Geometry.LineCurve(startPt, endPt)
                    boundary1 = dessicantLine.Split(chartBoundaryBrep, sc.doc.ModelAbsoluteTolerance)[0]
                    try:
                        boundary2 = comfortCrvSegments[comfCount][1].Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[1]
                        boundary3 = rc.Geometry.LineCurve(boundary1.PointAtStart, boundary2.PointAtStart)
                        boundary4 = rc.Geometry.LineCurve(boundary1.PointAtEnd, boundary2.PointAtEnd)
                        joinedHumidBound = rc.Geometry.Curve.JoinCurves([boundary1, boundary2, boundary3, boundary4])[0]
                        
                    except:
                        boundary2 = chartBoundary.Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0].Split(rc.Geometry.Surface.CreateExtrusion(boundary1, rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0]
                        boundary3 = rc.Geometry.LineCurve(boundary1.PointAtStart, boundary2.PointAtStart)
                        joinedHumidBound = rc.Geometry.Curve.JoinCurves([boundary1, boundary2, boundary3])[0]
                    
                    passiveStrategyCurves.append(joinedHumidBound)
                    passiveStrategyBreps.append(outlineCurve(joinedHumidBound))
                    strategyListTest.append("Dessicant Dehumidification")
                
                #If the user has hooked up dessicant dehumidification, add a dessicant dehumidification curve to the chart.
                if "Dehumidification Only" in passiveStrategy and humidRatioUp*scaleFactor <= comfortCrvSegments[comfCount][0].PointAtEnd.Y:
                    boundary1 = comfortCrvSegments[comfCount][0].Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[1]
                    try:
                        boundary2 = comfortCrvSegments[comfCount][1].Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[1]
                        boundary3 = rc.Geometry.LineCurve(boundary1.PointAtStart, boundary2.PointAtStart)
                        boundary4 = rc.Geometry.LineCurve(boundary1.PointAtEnd, boundary2.PointAtEnd)
                        joinedHumidBound = rc.Geometry.Curve.JoinCurves([boundary1, boundary2, boundary3, boundary4])[0]
                        
                    except:
                        boundary2 = chartBoundary.Split(splittingBrepUp, sc.doc.ModelAbsoluteTolerance)[0].Split(rc.Geometry.Surface.CreateExtrusion(boundary1, rc.Geometry.Vector3d.ZAxis), sc.doc.ModelAbsoluteTolerance)[0]
                        boundary3 = rc.Geometry.LineCurve(boundary1.PointAtStart, boundary2.PointAtStart)
                        joinedHumidBound = rc.Geometry.Curve.JoinCurves([boundary1, boundary2, boundary3])[0]
                    
                    passiveStrategyCurves.append(joinedHumidBound)
                    passiveStrategyBreps.append(outlineCurve(joinedHumidBound))
                    strategyListTest.append("Dehumidification Only")
        else:
            tempBelowComf = 2.8
        
        maxComfortPolyTemp = comfortCrvSegments[0][0].PointAt(0.5).X
        
        #Try to boolean all of the strategy and comfort curves together so that we can get a sense of comfort over the whole graph.
        allCurves = []
        for crv in mergedCurvesFinal:
            allCurves.append(crv)
        for crv in passiveStrategyCurves:
            allCurves.append(crv)
        
        if len(allCurves) > 1:
            listLength = len(allCurves)
            count  = 0
            while len(allCurves) > 1 and count < int(listLength/2) + 1:
                allCurves = unionAllCurves(allCurves)
                count += 1
        
        
        #Move the strategy outlines up just a bit so that they can be seen over the mesh.
        transformMatrix = rc.Geometry.Transform.Translation(0,0,sc.doc.ModelAbsoluteTolerance*5)
        for brep in finalComfortBreps:
            brep.Transform(transformMatrix)
        for brep in passiveStrategyBreps:
            brep.Transform(transformMatrix)
        
        
        return mergedCurvesFinal, finalComfortBreps, passiveStrategyCurves, passiveStrategyBreps, strategyListTest, allCurves, tempBelowComf, maxComfortPolyTemp
    else:
        return [], [], [], [], [], [], 2.8, 0


def statisticallyAnalyzePolygons(hourPts, comfortPolyline, strategyPolylines, unionedCurves, epwData, epwStr, strategyTextNames, tempBelowComf, airTemp, maxComfortPolyTemp, patternList):
    #Define lists to be filled up with the data.
    strategyPercent = []
    strategyOrNot = []
    
    #For each of the comfort polygons, determine how many of the hour points are inside of them and make a comfotr or not list.
    for countComf, comfortPolygon in enumerate(comfortPolyline):
        comfBool = []
        for hourPt in hourPts:
            if str(comfortPolygon.Contains(hourPt, rc.Geometry.Plane.WorldXY, sc.doc.ModelAbsoluteTolerance)) == "Inside": comfBool.append(1)
            else:comfBool.append(0)
        if len(comfBool) != 0:
            comfPercent = (sum(comfBool)/len(comfBool))*100
        else:
            comfPercent =100
        strategyPercent.append(comfPercent)
        if epwData == True:
            if analysisPeriod_:
                comfBool.insert(0,analysisPeriod_[1])
                comfBool.insert(0,analysisPeriod_[0])
            else:
                comfBool.insert(0, epwStr[6])
                comfBool.insert(0, epwStr[5])
            comfBool.insert(0, epwStr[4])
            comfBool.insert(0, "Boolean Value")
            comfBool.insert(0, "Comfortable Hours in " + strategyTextNames[countComf] + " Polygon")
            comfBool.insert(0, epwStr[1])
            comfBool.insert(0, epwStr[0])
        strategyOrNot.append(comfBool)
    
    #For each of the strategy polygons, determine how many of the hour points are inside of them and make a comfort or not list.
    for countStrat, comfortPolygon in enumerate(strategyPolylines):
        comfBool = []
        if strategyTextNames[countComf + countStrat + 1] != "Thermal Mass + Night Vent" or epwData == False or patternList != []:
            for hourPt in hourPts:
                if str(comfortPolygon.Contains(hourPt, rc.Geometry.Plane.WorldXY, sc.doc.ModelAbsoluteTolerance)) == "Inside": comfBool.append(1)
                else:comfBool.append(0)
        else:
            for hourCt, hourPt in enumerate(hourPts):
                if str(comfortPolygon.Contains(hourPt, rc.Geometry.Plane.WorldXY, sc.doc.ModelAbsoluteTolerance)) == "Inside" and airTemp[hourCt-12] < maxComfortPolyTemp-tempBelowComf: comfBool.append(1)
                else:comfBool.append(0)
        comfPercent = (sum(comfBool)/len(comfBool))*100
        strategyPercent.append(comfPercent)
        if epwData == True:
            if analysisPeriod_:
                comfBool.insert(0,analysisPeriod_[1])
                comfBool.insert(0,analysisPeriod_[0])
            else:
                comfBool.insert(0, epwStr[6])
                comfBool.insert(0, epwStr[5])
            comfBool.insert(0, epwStr[4])
            comfBool.insert(0, "Boolean Value")
            comfBool.insert(0, "Comfortable Hours in " + strategyTextNames[countComf + countStrat + 1] + " Polygon")
            comfBool.insert(0, epwStr[1])
            comfBool.insert(0, epwStr[0])
        strategyOrNot.append(comfBool)
    
    #For the total comfort, determine how many of the hour points are inside of them and make a comfort or not list.
    temporaryPercent = []
    temporaryComfOrNot = []
    for polygon in unionedCurves:
        comfBool = []
        for hourPt in hourPts:
            if str(polygon.Contains(hourPt, rc.Geometry.Plane.WorldXY, sc.doc.ModelAbsoluteTolerance)) == "Inside": comfBool.append(1)
            else:comfBool.append(0)
        if len(comfBool) != 0:
            comfPercent = (sum(comfBool)/len(comfBool))*100
        else:
            comfPercent = 100
        temporaryPercent.append(comfPercent)
        temporaryComfOrNot.append(comfBool)
    
    #Build the final percent and comfort or not lists.
    finalTotalPercent = sum(temporaryPercent)
    finalComfOrNot = []
    for listCount, list in enumerate(temporaryComfOrNot):
        for count, item in enumerate(list):
            if listCount == 0:
                finalComfOrNot.append(item)
            else:
                finalComfOrNot[count] = finalComfOrNot[count] + item
    
    if epwData == True:
        if analysisPeriod_:
            finalComfOrNot.insert(0,analysisPeriod_[1])
            finalComfOrNot.insert(0,analysisPeriod_[0])
        else:
            finalComfOrNot.insert(0, epwStr[6])
            finalComfOrNot.insert(0, epwStr[5])
        finalComfOrNot.insert(0, epwStr[4])
        finalComfOrNot.insert(0, "Boolean Value")
        finalComfOrNot.insert(0, "Comfortable Hours in All Polygons")
        finalComfOrNot.insert(0, epwStr[1])
        finalComfOrNot.insert(0, epwStr[0])
    
    
    return finalTotalPercent, finalComfOrNot, strategyPercent, strategyOrNot


def getPointColors(totalComfOrNot, annualHourlyDataSplit, annualDataStr, numSeg, customColors, legendBasePoint, legendScale, legendFont, legendFontSize, lb_visualization):
    #Define the lists.
    pointColors = []
    colorLegends = []
    
    #Get the colors for comfort.
    if str(totalComfOrNot[0]) == "key:location/dataType/units/frequency/startsAt/endsAt":
        totalComfOrNot = totalComfOrNot[7:]
    pointColors.append(lb_visualization.gradientColor(totalComfOrNot, 0, 1, customColors))
    
    #Get the colors for annualHourly Data.
    for list in annualHourlyDataSplit:
        if len(list) != 0:
            pointColors.append(lb_visualization.gradientColor(list, "min", "max", customColors))
    
    #Generate a legend for comfort.
    legend = []
    legendSrfs, legendText, legendTextCrv, textPt, textSize = lb_visualization.createLegend(totalComfOrNot, 0, 1, 2, "Comfort", lb_visualization.BoundingBoxPar, legendBasePoint, legendScale, legendFont, legendFontSize)
    legendColors = lb_visualization.gradientColor(legendText[:-1], 0, 1, customColors)
    legendSrfs = lb_visualization.colorMesh(legendColors, legendSrfs)
    legend.append(legendSrfs)
    for list in legendTextCrv:
        for item in list:
            legend.append(item)
    colorLegends.append(legend)
    
    #Generate legends for annualHourly Data.
    for listCount, list in enumerate(annualHourlyDataSplit):
        if len(list) != 0:
            legend = []
            legendSrfs, legendText, legendTextCrv, textPt, textSize = lb_visualization.createLegend(list, "min", "max", numSeg, annualDataStr[listCount][3], lb_visualization.BoundingBoxPar, legendBasePoint, legendScale, legendFont, legendFontSize)
            legendColors = lb_visualization.gradientColor(legendText[:-1], "min", "max", customColors)
            legendSrfs = lb_visualization.colorMesh(legendColors, legendSrfs)
            legend.append(legendSrfs)
            for list in legendTextCrv:
                for item in list:
                    legend.append(item)
            colorLegends.append(legend)
    
    
    return pointColors, colorLegends


def main(epwData, epwStr, calcLength, airTemp, relHumid, barPress, avgBarPress, radTemp, windSpeed, metRate, cloLevel, exWork, humidRatioUp, humidRatioLow, calcLengthComf, eightyPercentComfortable, titleStatement, patternList):
    #Import the classes.
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
        lb_comfortModels = sc.sticky["ladybug_ComfortModels"]()
        lb_visualization = sc.sticky["ladybug_ResultVisualization"]()
        
        # Read the legend parameters.
        lowB, highB, numSeg, customColors, legendBasePoint, legendScale, legendFont, legendFontSize = lb_preparation.readLegendParameters(legendPar_, False)
        
        # Generate the chart curves.
        scaleFactor = 1500
        chartCurves, humidityLines = drawPsychChart(avgBarPress, lb_comfortModels, legendFont, legendFontSize, scaleFactor, epwData, epwStr, lb_visualization)
        
        #If there is annual hourly data, split it up.
        if annualHourlyData_ != []:
            def chunks(l, n):
                finalList = []
                for i in range(0, len(l), n):
                    finalList.append(l[i:i+n])
                return finalList
            annualHourlyDataSplit = chunks(annualHourlyData_, 8767)
        else: annualHourlyDataSplit = [[]]
        annualDataStr = []
        if annualHourlyDataSplit != [[]]:
            for list in annualHourlyDataSplit:
                annualDataStr.append(list[:7])
        
        # If an analysis period is selected, use that to select out the data.
        if analysisPeriod_ != [] and epwData == True and calcLength == 8760:
            airTemp = lb_preparation.selectHourlyData(_dryBulbTemperature, analysisPeriod_)[7:]
            relHumid = lb_preparation.selectHourlyData(_relativeHumidity, analysisPeriod_)[7:]
            if len(barPress) == 8760:
                barPress = lb_preparation.selectHourlyData(barPress, analysisPeriod_)[7:]
            else:
                barPress2 = []
                for num in range(len(airTemp)):
                    barPress2.append(barPress[0])
                barPress = barPress2
            if len(patternList) == 8760:
                HOYS, months, days = getHOYsBasedOnPeriod(analysisPeriod_, 1)
                newPatternList = []
                for hour in HOYS:
                    newPatternList.append(patternList[hour-1])
                patternList = newPatternList
            if annualHourlyDataSplit != [[]]:
                annualHourlyDataSplitNew = []
                for list in annualHourlyDataSplit:
                    annualHourlyDataSplitNew.append(lb_preparation.selectHourlyData(list, analysisPeriod_)[7:])
                annualHourlyDataSplit = annualHourlyDataSplitNew
        else:
            annualHourlyDataSplitNew = []
            for list in annualHourlyDataSplit:
                annualHourlyDataSplitNew.append(lb_preparation.selectHourlyData(list, analysisPeriod_)[7:])
            annualHourlyDataSplit = annualHourlyDataSplitNew
        
        #If a conditional statement is applied, use it to select out data.
        if patternList != []:
            newAirTemp = []
            newRelHumid = []
            newBarPress = []
            newAnnualHourlyDataSplit = []
            for list in annualHourlyDataSplit:
                newAnnualHourlyDataSplit.append([])
            for count, bool in enumerate(patternList):
                if bool == True:
                    newAirTemp.append(airTemp[count])
                    newRelHumid.append(relHumid[count])
                    newBarPress.append(barPress[count])
                    for listCount in range(len(annualHourlyDataSplit)):
                        newAnnualHourlyDataSplit[listCount].append(annualHourlyDataSplit[listCount][count])
            airTemp = newAirTemp
            relHumid = newRelHumid
            barPress = newBarPress
            annualHourlyDataSplit = newAnnualHourlyDataSplit
        
        #As long as the calculation length is more than 1, make a colored mesh and get chart points for the input data.
        legend = []
        if calcLength > 1:
            hourPts, coloredMesh, meshFaceValues = colorMesh(airTemp, relHumid, barPress, lb_preparation, lb_comfortModels, lb_visualization, scaleFactor, lowB, highB, customColors)
            legendTitle = "Hours"
            lb_visualization.calculateBB(chartCurves[62:70], True)
            legendSrfs, legendText, legendTextCrv, textPt, textSize = lb_visualization.createLegend(meshFaceValues, lowB, highB, numSeg, legendTitle, lb_visualization.BoundingBoxPar, legendBasePoint, legendScale, legendFont, legendFontSize)
            legendColors = lb_visualization.gradientColor(legendText[:-1], lowB, highB, customColors)
            legendSrfs = lb_visualization.colorMesh(legendColors, legendSrfs)
            legend.append(legendSrfs)
            for list in legendTextCrv:
                for item in list:
                    legend.append(item)
            if legendBasePoint == None:
                legendBasePoint = lb_visualization.BoundingBoxPar[0]
        else:
            hourPts = [rc.Geometry.Point3d(airTemp[0], lb_comfortModels.calcHumidRatio(airTemp, relHumid, barPress)[0][0]*scaleFactor, 0)]
            coloredMesh = None
            meshFaceValues = []
            legendBasePoint = None
        
        # Get a polycurve that represents the boundary of the chart.
        chartBoundary = rc.Geometry.Curve.JoinCurves([chartCurves[0], chartCurves[25], chartCurves[31], chartCurves[10], chartCurves[11]])[0]
        
        # Calculate the comfort and strategy polygons.
        comfortPolyline, comfortPolygon, strategyPolylines, strategyPolygons, strategyTextNames, unionedCurves, tempBelowComf, maxComfortPolyTemp = calcComfAndStrategyPolygons(radTemp, windSpeed, metRate, cloLevel, exWork, humidRatioUp, humidRatioLow, passiveStrategy_, humidityLines, calcLengthComf, lb_comfortModels, chartBoundary, scaleFactor, eightyPercentComfortable)
        
        #Calculate how many hours are in each comfort or strategy and comfort polygons.
        totalComfPercent, totalComfOrNot, strategyPercent, strategyOrNot = statisticallyAnalyzePolygons(hourPts, comfortPolyline, strategyPolylines, unionedCurves, epwData, epwStr, strategyTextNames, tempBelowComf, airTemp, maxComfortPolyTemp, patternList)
        
        #Generate colors for the points.
        if len(totalComfOrNot) > 1:
            pointColors, pointLegends = getPointColors(totalComfOrNot, annualHourlyDataSplit, annualDataStr, numSeg, customColors, legendBasePoint, legendScale, legendFont, legendFontSize, lb_visualization)
        else:
            pointColors = []
            pointLegends = []
        
        #If the user has selected to scale or move the geometry, scale it all and/or move it all.
        if basePoint_ != None:
            transformMtx = rc.Geometry.Transform.Translation(basePoint_.X, basePoint_.Y, basePoint_.Z)
            for geo in chartCurves: geo.Transform(transformMtx)
            coloredMesh.Transform(transformMtx)
            for geo in legend: geo.Transform(transformMtx)
            legendBasePoint.Transform(transformMtx)
            for geo in comfortPolygon: geo.Transform(transformMtx)
            for geo in strategyPolygons: geo.Transform(transformMtx)
            for geo in hourPts: geo.Transform(transformMtx)
            for list in pointLegends:
                for geo in list:
                    geo.Transform(transformMtx)
            basePoint = basePoint_
        else: basePoint = rc.Geometry.Point3d(0,0,0)
        
        if scale_ != None:
            transformMtx = rc.Geometry.Transform.Scale(basePoint, scale_)
            for geo in chartCurves: geo.Transform(transformMtx)
            coloredMesh.Transform(transformMtx)
            for geo in legend: geo.Transform(transformMtx)
            legendBasePoint.Transform(transformMtx)
            for geo in comfortPolygon: geo.Transform(transformMtx)
            for geo in strategyPolygons: geo.Transform(transformMtx)
            for geo in hourPts: geo.Transform(transformMtx)
        
        
        return totalComfPercent, totalComfOrNot, strategyTextNames, strategyPercent, strategyOrNot, chartCurves, coloredMesh, legend, legendBasePoint, comfortPolygon, strategyPolygons, hourPts, pointColors, pointLegends
    else:
        print "You should first let the Ladybug fly..."
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, "You should first let the Ladybug fly...")
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None




#Check the inputs.
checkData = False
if _runIt == True:
    checkData, epwData, epwStr, calcLength, airTemp, relHumid, barPress, \
    avgBarPress, radTemp, windSpeed, metRate, cloLevel, exWork, humidRatioUp, \
    humidRatioLow, calcLengthComf, eightyPercentComfortable, titleStatement, \
    patternList = checkTheInputs()

#If the inputs are good, run the function.
if checkData == True:
    
    results = main(epwData, epwStr, calcLength, airTemp, relHumid, barPress, \
                   avgBarPress, radTemp, windSpeed, metRate, cloLevel, exWork, \
                   humidRatioUp, humidRatioLow, calcLengthComf, \
                   eightyPercentComfortable, titleStatement, patternList)
                   
    if results != -1:
        totalComfortPercent, totalComfortOrNot, strategyNames, strategyPercentOfTime, \
        initStrategyOrNot, chartCurvesAndTxt, psychChartMesh, legend, legendBasePt, \
        comfortPolygons, strategyPolygons, chartHourPoints, pointColors, \
        pointLegends = results
    
        #Unpack the data tree of the strategyOrNot.
        strategyOrNot = DataTree[Object]()
        for listCount, list in enumerate(initStrategyOrNot):
            for item in list:
                strategyOrNot.Add(item, GH_Path(listCount))
        #Unpack the data tree of point colors and their legends.
        hourPointColors = DataTree[Object]()
        for listCount, list in enumerate(pointColors):
            for item in list:
                hourPointColors.Add(item, GH_Path(listCount))
        hourPointLegend = DataTree[Object]()
        for listCount, list in enumerate(pointLegends):
            for item in list:
                hourPointLegend.Add(item, GH_Path(listCount))



#Hide the points input.
ghenv.Component.Params.Output[11].Hidden = True
ghenv.Component.Params.Output[15].Hidden = True
ghenv.Component.Params.Output[17].Hidden = True