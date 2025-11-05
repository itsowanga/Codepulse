    #include <windows.h>
    #include <winuser.h>
    #include <iostream>
    #include <stdio.h>
    #include <string>
    #include <thread>
    #include <chrono>
    #include <ctime>

   extern "C" {
    #include "sqlite3.h"
}

    using namespace std;

    static int callback(void *NotUsed, int argc, char **argv, char **azColName) {
        int i;
        for(i = 0; i<argc; i++) {
            printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
        }
        printf("\n");
        return 0;
}
    int main(void){

       // Manages the foreground process.
        HWND foreground = GetForegroundWindow();
        char *errMessage = 0;
        sqlite3* data;
        char *sqlCreateTable;
        char* insertTable;
        int file = 0;
        clock_t duration;
        float finalduration;
        time_t timestamp;
        

        //Attempt to open file and error handling when unable to open
        file = sqlite3_open("activity.db", &data);
    
        if(file != SQLITE_OK){
            cout<<"File did not open."<<endl;
            return 1;
        }

       else{
        // Create a sql table for logging
        sqlCreateTable = "CREATE TABLE session("\
        "timestamp TEXT,"\
        "file TEXT,"\
        "language TEXT,"\
        "duration_sec FLOAT);";

        // Execution of the sql statement
        sqlite3_exec(data, sqlCreateTable, callback, 0, &errMessage);     
        clock_t before = clock();
        while(foreground != NULL){
            // Store the foreground process information
            char processName[256];
            GetWindowText(foreground, processName, 256);
            string process = (string)processName;
            // Slice the string to find filename + language using the file extension.
            string filename = process.substr(0, process.find("-")-1);
            string language = filename.substr(filename.find("."), filename.size()-1);
            duration = clock() - before;
            finalduration = (float)duration / CLOCKS_PER_SEC;
            insertTable = "INSERT INTO sessions(timestamp, file, language, duration_sec)"\
                          "VALUES ("+time(&timestamp)+','+filename+','+language+','+finalduration+");";
            this_thread::sleep_for(chrono::seconds(60));

        
    }
        return 0;
    }


