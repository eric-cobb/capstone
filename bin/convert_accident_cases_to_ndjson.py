import json
import sys, os

def main(arg):
    file = arg
    with open(file, "r") as read_file:
        data = json.load(read_file)

    result = [json.dumps(record) for record in data]

    # Output NDJSON file to write to
    file_basename = os.path.basename(file).split('.')[0]
    df = open(os.path.dirname(os.path.abspath(__file__)) + '/../data/output/' + file_basename + '.ndjson', "w")
    for rec in data:
        data_string = {}
        data_string['mkey'] = rec['cm_mkey']
        data_string['closed'] = rec['cm_closed']
        data_string['completionStatus'] = rec['cm_completionStatus']
        data_string['hasSafetyRec'] = rec['cm_hasSafetyRec']
        data_string['highestInjury'] = rec['cm_highestInjury']
        data_string['isStudy'] = rec['cm_isStudy']
        data_string['mode'] = rec['cm_mode']
        data_string['ntsbNum'] = rec['cm_ntsbNum']
        data_string['originalPublishedDate'] = rec['cm_originalPublishedDate']
        if 'cm_recentReportPublishDate' in rec:
            data_string['recentReportPublishDate'] = rec['cm_recentReportPublishDate']
        else:
            data_string['recentReportPublishDate'] = None
        if 'cm_mostRecentReportType' in rec:
            data_string['mostRecentReportType'] = rec['cm_mostRecentReportType']
        else:
            data_string['mostRecentReportType'] = None
        if 'cm_probableCause' in rec:
            data_string['probableCause'] = rec['cm_probableCause']
        else:
            data_string['probableCause'] = None
        data_string['city'] = rec['cm_city']
        data_string['country'] = rec['cm_country']
        data_string['eventDate'] = rec['cm_eventDate']
        data_string['state'] = rec['cm_state']
        if 'cm_agency' in rec:
            data_string['agency'] = rec['cm_agency']
        else:
            data_string['agency'] = None
        if 'cm_boardLaunch' in rec:
            data_string['boardLaunch'] = rec['cm_boardLaunch']
        else:
            data_string['cm_boardLaunch'] = None
        if 'cm_boardMeetingDate' in rec:
            data_string['boardMeetingDate'] = rec['cm_boardMeetingDate']
        else:
            data_string['cm_boardMeetingDate'] = None
        if 'cm_docketDate' in rec:
            data_string['docketDate'] = rec['cm_docketDate']
        else: 
            data_string['cm_docketDate'] = None
        if 'eventType' in rec:
            data_string['eventType'] = rec['cm_eventType']
        else: 
            data_string['eventType'] = None
        if 'reportDate' in rec:
            data_string['reportDate'] = rec['cm_reportDate']
        else:
            data_string['reportDate'] = None
        if 'reportNum' in rec:
            data_string['reportNum'] = rec['cm_reportNum']
        else:
            data_string['reportNum'] = None
        if 'reportType' in rec:
            data_string['reportType'] = rec['cm_reportType']
        else:
            data_string['reportType'] = None

        # Iterate through the aircraft
        aircraftNum = 0
        for acft in rec['cm_vehicles']:
            if aircraftNum > 1:
                break 

            aircraft = 'aircraft' + str(aircraftNum + 1)

            aircraftCategory = aircraft + '.aircraftCategory'
            data_string[aircraftCategory] = rec['cm_vehicles'][aircraftNum]['aircraftCategory']

            amateurBuilt = aircraft + '.amateurBuilt'
            data_string[amateurBuilt] = rec['cm_vehicles'][aircraftNum]['amateurBuilt']

            try:
                make = aircraft + '.make'
                data_string[make] = rec['cm_vehicles'][aircraftNum]['make'].title()
            except AttributeError:
                data_string[make] = None

            try:
                model = aircraft + '.model'
                data_string[model] = rec['cm_vehicles'][aircraftNum]['model'].upper()
            except AttributeError:
                data_string[model] = None

            numberOfEngines = aircraft + '.numberOfEngines'
            data_string[numberOfEngines] = rec['cm_vehicles'][aircraftNum]['numberOfEngines']

            registrationNumber = aircraft + '.registrationNumber'
            data_string[registrationNumber] = rec['cm_vehicles'][aircraftNum]['registrationNumber']

            gaFlight = aircraft + '.gaFlight'
            data_string[gaFlight] = rec['cm_vehicles'][aircraftNum]['gaFlight']

            # Iterate through the events for this aircraft
            eventNum = 0
            try:
                for evt in rec['cm_vehicles'][aircraftNum]['cm_events']:
                    if eventNum > 3:
                        break
                    event = aircraft + '.event' + str(eventNum + 1)
                    cicttEventSOEGroup = event + '.eventSOEGroup'
                    data_string[cicttEventSOEGroup] = rec['cm_vehicles'][aircraftNum]['cm_events'][eventNum]['cicttEventSOEGroup']

                    cm_eventCode = event + '.eventCode'
                    data_string[cm_eventCode] = rec['cm_vehicles'][aircraftNum]['cm_events'][eventNum]['cm_eventCode']

                    cm_isDefiningEvent = event + '.isDefiningEvent'
                    data_string[cm_isDefiningEvent] = rec['cm_vehicles'][aircraftNum]['cm_events'][eventNum]['cm_isDefiningEvent']

                    eventNum += 1
            except KeyError:
                pass
            
            try:
                # Iterate through the findings for this aircraft
                findingNum = 0
                for fdg in rec['cm_vehicles'][aircraftNum]['cm_findings']:
                    if findingNum > 6:
                        break
                    finding = aircraft + '.finding' + str(findingNum + 1)
                    findingCode = finding + '.findingCode'
                    data_string[findingCode] = rec['cm_vehicles'][aircraftNum]['cm_findings'][findingNum]['cm_findingCode']

                    findingReportText = finding + '.findingReportText'
                    data_string[findingReportText] = rec['cm_vehicles'][aircraftNum]['cm_findings'][findingNum]['cm_findingReportText']

                    findingText = finding + '.findingText'
                    data_string[findingText] = rec['cm_vehicles'][aircraftNum]['cm_findings'][findingNum]['cm_findingText']

                    findingNum += 1
            except KeyError:
                pass

            airMedical = aircraft + '.airMedical'
            data_string[airMedical] = rec['cm_vehicles'][aircraftNum]['airMedical']

            airMedicalType = aircraft + '.airMedicalType'
            data_string[airMedicalType] = rec['cm_vehicles'][aircraftNum]['airMedicalType']

            flightOperationType = aircraft + '.flightOperationType'
            data_string[flightOperationType] = rec['cm_vehicles'][aircraftNum]['flightOperationType']

            flightScheduledType = aircraft + '.flightScheduledType'
            data_string[flightScheduledType] = rec['cm_vehicles'][aircraftNum]['flightScheduledType']

            flightServiceType = aircraft + '.flightServiceType'
            data_string[flightServiceType] = rec['cm_vehicles'][aircraftNum]['flightServiceType']

            flightTerminalType = aircraft + '.flightTerminalType'
            data_string[flightTerminalType] = rec['cm_vehicles'][aircraftNum]['flightTerminalType']

            operatorName = aircraft + '.operatorName'
            data_string[operatorName] = rec['cm_vehicles'][aircraftNum]['operatorName']

            registeredOwner = aircraft + '.registeredOwner'
            data_string[registeredOwner] = rec['cm_vehicles'][aircraftNum]['registeredOwner']

            regulationFlightConductedUnder = aircraft + '.regulationFlightConductedUnder'
            data_string[regulationFlightConductedUnder] = rec['cm_vehicles'][aircraftNum]['regulationFlightConductedUnder']

            revenueSightseeing = aircraft + '.revenueSightseeing'
            data_string[revenueSightseeing] = rec['cm_vehicles'][aircraftNum]['revenueSightseeing']

            secondPilotPresent = aircraft + '.secondPilotPresent'
            data_string[secondPilotPresent] = rec['cm_vehicles'][aircraftNum]['secondPilotPresent']

            aircraftNum += 1

        if 'airportId' in rec:
            data_string['airportId'] = rec['airportId']
        else:
            data_string['airportId'] = None
        if 'airportName' in rec:
            data_string['airportName'] = rec['airportName']
        else:
            data_string['airportName'] = None
        if 'reportType' in rec:
            data_string['reportType'] = rec['cm_reportType']
        else: 
            data_string['reportType'] = None
        if 'analysisNarrative' in rec:
            data_string['analysisNarrative'] = rec['analysisNarrative']
        else:
            data_string['analysisNarrative'] = None
        if 'factualNarrative' in rec:
            data_string['factualNarrative'] = rec['factualNarrative']
        else:
            data_string['factualNarrative'] = None
        if 'prelimNarrative' in rec:
            data_string['prelimNarrative'] = rec['prelimNarrative']
        else:
            data_string['prelimNarrative'] = None
        if 'fatalInjuryCount' in rec:
            data_string['fatalInjuryCount'] = rec['cm_fatalInjuryCount']
        else:
            data_string['datalInjuryCount'] = None
        if 'minorInjuryCount' in rec:
            data_string['minorInjuryCount'] = rec['cm_minorInjuryCount']
        else:
            data_string['minorInjuryCount'] = None
        if 'seriousInjuryCount' in rec:
            data_string['seriousInjuryCount'] = rec['cm_seriousInjuryCount']
        else:
            data_string['seriousInjuryCount'] = None
        if 'accidentSiteCondition' in rec:
            data_string['accidentSiteCondition'] = rec['accidentSiteCondition']
        else:
            data_string['accidentSiteCondition'] = None
        if 'cm_docketOriginalPublishDate' in rec:
            data_string['docketOriginalPublishDate'] = rec['cm_docketOriginalPublishDate']
        else:
            data_string['docketOriginalPublishDate'] = None
        
        df.write(json.dumps(data_string) + "\n")
    df.close()

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        main(filename)
    except IndexError:
        print("No filename given")