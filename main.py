import parse
import json
import os

jsonfile = {}
ipList = set()
domainList = set()


def extractIPsFromJSON(json):
    for entry in json['log']['entries']:
        if(entry['serverIPAddress'] != ""):
            ipList.add(entry['serverIPAddress'])


def extractDomainNamesFromJSON(json):
    for entry in json['log']['entries']:
        domainList.add(entry['request']['url'].split("/")[2])


def parseRecordedNetworkFromWebsite(arg):
    if(arg == None):
        print("no arg provided")
    else:
        jsonfile = json.loads(open(arg, encoding="utf8").read())
        extractIPsFromJSON(jsonfile)
        extractDomainNamesFromJSON(jsonfile)
        print("file parsed")


def parseCommand(command):
    if(command.find(" ") != -1):
        return parse.parse("{command} {args}", command).named
    else:
        return {"command": command, "args": None}


def addRoutes(ips, gateway, interfaceNumber):
    for ip in ips:
        os.system(
            "route -p add {} mask 255.255.255.255 {} metric 1 if {}"
            .format(ip, gateway, interfaceNumber)
        )


def addRoutesCommand(args):
    if(jsonfile == {}):
        print("Parse a record file first")
    elif(args == None):
        print("No args provided")
    else:
        args = args.split(" ")
        addRoutes(ipList, args[0], args[1])


def deleteRoutes(args):
    if(jsonfile == {}):
        print("Parse a record file first")
    else:
        for ip in ipList:
            os.system(
                "route delete {}".format(ip)
            )


def getDomains(args):
    if(jsonfile == {}):
        print("Parse a record file first")
    else:
        domainStringList = ""
        for domain in domainList:
            domainStringList += domain + ",\n"
        print(domainStringList)


def help(args):
    print("""
    Commands:
        parse filename
        addRoutes gateway interfaceNumber
        deleteRoutes
        getDomains
        quit
        help
        ?
    """)


def main():
    switcher = {
        "parse": parseRecordedNetworkFromWebsite,
        "addRoutes": addRoutesCommand,
        "deleteRoutes": deleteRoutes,
        "getDomains": getDomains,
        "help": help,
        "?": help
    }
    commandText = ""
    quit = False

    while(not quit):
        commandText = input()
        if(commandText == "quit"):
            quit = True
        else:
            command = parseCommand(commandText)
            switchFunction = switcher.get(command.get("command"))
            if(switchFunction == None):
                help
            else:
                switchFunction(command.get("args"))

if __name__ == "__main__":
    main()