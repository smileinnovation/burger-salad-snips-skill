#!/usr/bin/env python3
import uuid
import os
import sys
from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider
from AWSIoTPythonSDK.core.protocol.connection.cores import ProgressiveBackOffCore
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryInvalidRequestException

GROUP_CA_PATH = "./certs/groupCA/"

# General message notification callback
def customOnMessage(message):
    print('Received message on topic %s: %s\n' % (message.topic, message.payload))

class GGConnect:
    def __init__(self, host, rootCA, certPath, privateKeyPath, thingName, maxRetries=10):
        self.host = host
        self.rootCA = rootCA
        self.certPath = certPath
        self.privateKeyPath = privateKeyPath
        self.thingName = thingName
        self.clientId = thingName
        self.maxRetries = maxRetries
        self.disscovered = False
        self.groupCA = None
        self.coreInfo = None
        self.connected = False
        
        # Progressive back off core
        self.backOffCore = ProgressiveBackOffCore()
        # Discover GGCs
        self.discoveryInfoProvider = DiscoveryInfoProvider()
        self.discoveryInfoProvider.configureEndpoint(self.host)
        self.discoveryInfoProvider.configureCredentials(self.rootCA, self.certPath, self.privateKeyPath)
        self.discoveryInfoProvider.configureTimeout(10)  # 10 sec

    def connectToGG(self):
        retryCount = self.maxRetries
        print("Discovering greengrass core")
        while retryCount != 0:
            try:
                discoveryInfo = self.discoveryInfoProvider.discover(self.thingName)
                caList = discoveryInfo.getAllCas()
                coreList = discoveryInfo.getAllCores()
            
                # We only pick the first ca and core info
                groupId, ca = caList[0]
                coreInfo = coreList[0]
                self.groupCA = GROUP_CA_PATH + groupId + "_CA_" + str(uuid.uuid4()) + ".crt"
                if not os.path.exists(GROUP_CA_PATH):
                    os.makedirs(GROUP_CA_PATH)
                groupCAFile = open(self.groupCA, "w")
                groupCAFile.write(ca)
                groupCAFile.close()
                self.discovered = True
                break
            except DiscoveryInvalidRequestException as e:
                print("Invalid discovery request detected!")
                print("Type: %s" % str(type(e)))
                print("Error message: %s" % e.message)
                print("Stopping...")
                break
            except BaseException as e:
                print("Error in discovery!")
                print("Type: %s" % str(type(e)))
                print("Error message: %s" % e.message)
                retryCount -= 1
                print("\n%d/%d retries left\n" % (retryCount, self.maxRetries))
                print("Backing off...\n")
                self.backOffCore.backOff()

        if not self.discovered:
            print("Discovery failed after %d retries. Exiting...\n" % (self.maxRetries))
            sys.exit(-1)
        print("Done")
            
        # Iterate through all connection options for the core and use the first successful one
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId)
        self.myAWSIoTMQTTClient.configureCredentials(self.groupCA, self.privateKeyPath, self.certPath)
        self.myAWSIoTMQTTClient.onMessage = customOnMessage
        print("Connecting to the Core")
        for connectivityInfo in coreInfo.connectivityInfoList:
            currentHost = connectivityInfo.host
            currentPort = connectivityInfo.port
            self.myAWSIoTMQTTClient.configureEndpoint(currentHost, currentPort)
            try:
                self.myAWSIoTMQTTClient.connect()
                connected = True
                break
            except:
                print("Error occured while connecting: {}\n{}".format(sys.exc_info()[0],sys.exc_info()[1]))
                print("Retrying ...")
                self.backOffCore.backOff()
                
        if not connected:
            print("Cannot connect to core %s. Exiting..." % coreInfo.coreThingArn)
            sys.exit(-2)
        print("Done")
        return self.myAWSIoTMQTTClient
