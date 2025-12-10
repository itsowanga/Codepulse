    #include <windows.h>
    #include <winuser.h>
    #include <iostream>
    #include <stdio.h>
    #include <string>
    #include <sstream>
    #include <thread>
    #include <chrono>
    #include <ctime>
    #include <csignal>

   extern "C" {
    #include "sqlite3.h"
}

    using namespace std;

    // Global database pointer for signal handling
    static sqlite3* globalDb = nullptr;

    // Signal handler to ensure database is flushed and closed on exit/crash
    void signalHandler(int signum) {
        cerr << "\nSignal " << signum << " received. Flushing and closing database..." << endl;
        if (globalDb != nullptr) {
            sqlite3_close(globalDb);
        }
        exit(signum);
    }

    static int callback(void *NotUsed, int argc, char **argv, char **azColName) {
        int i;
        for(i = 0; i<argc; i++) {
            printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
        }
        printf("\n");
        return 0;
}
    int main(void){

        HWND foreground = GetForegroundWindow();
        char *errMessage = 0;
        sqlite3* data;
        char *sqlCreateTable;
        string insertTable;
        ostringstream sql;
        int file = 0;
        clock_t duration;
        float finalduration;
        time_t timestamp;
        
        // Register signal handlers for clean shutdown
        signal(SIGINT, signalHandler);
        signal(SIGTERM, signalHandler);

        //Attempt to open file and error handling when unable to open
        file = sqlite3_open("activity.db", &data);
        
        // Store database pointer globally for signal handler access
        globalDb = data;
    
        if(file != SQLITE_OK){
            cout<<"File did not open."<<endl;
            return 1;
        }

       else{
        // Create a sql table for logging
        sqlCreateTable = "CREATE TABLE sessions("\
        "timestamp TEXT,"\
        "file TEXT,"\
        "language TEXT,"\
        "duration_sec FLOAT);";

        // Execution of the sql statement
        if(sqlite3_exec(data, sqlCreateTable, callback, 0, &errMessage) != SQLITE_OK) {
            cerr << "SQL error: " << errMessage << endl;
            sqlite3_free(errMessage);
        }
        clock_t before = clock();
        while(foreground != NULL){
            // Store the foreground process information
            wchar_t processName[256];
            GetWindowText(foreground, processName, 256);
            
            // Convert wide char to regular string
            char buffer[256];
            wcstombs(buffer, processName, sizeof(buffer));
            string process = buffer;
            // Slice the string to find filename + language using the file extension.
            string filename = process.substr(0, process.find("-")-1);
            string language = filename.substr(filename.find("."), filename.size()-1);
            duration = clock() - before;
            finalduration = (float)duration / CLOCKS_PER_SEC;
            sql << "INSERT INTO sessions(timestamp, file, language, duration_sec) "
            << "VALUES (" << time(&timestamp) << ", '" << filename << "', '" << language << "', " << finalduration << ");";

            insertTable = sql.str();
            
            // Execute the INSERT statement
            errMessage = 0;
            if(sqlite3_exec(data, insertTable.c_str(), callback, 0, &errMessage) != SQLITE_OK) {
                cerr << "SQL insert error: " << errMessage << endl;
                sqlite3_free(errMessage);
            }
            
            sql.str("");
            sql.clear();
            this_thread::sleep_for(chrono::seconds(60));

        
    }
        sqlite3_close(data);
        return 0;
    }


