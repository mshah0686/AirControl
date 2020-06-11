//
//  AppDelegate.swift
//  Temp
//
//  Created by Malav Shah on 6/11/20.
//  Copyright © 2020 Malav Shah. All rights reserved.
//

import Cocoa

@NSApplicationMain
class AppDelegate: NSObject, NSApplicationDelegate {



    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Insert code here to initialize your application
    }

    func applicationWillTerminate(_ aNotification: Notification) {
        // Insert code here to tear down your application
    }
    
    @IBAction func talk(sender: NSButton) {
        print("hello world")
        let path = "/usr/bin/say"
        let arguments = ["hello world"]
        let task = Process.launchedProcess(launchPath: path, arguments: arguments)
        task.waitUntilExit()
    }


}

