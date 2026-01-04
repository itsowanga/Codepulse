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
    #include <vector>

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

    // Callback to store query results
    static vector<vector<string>> queryResults;
    static int queryCallback(void *data, int argc, char **argv, char **azColName) {
        vector<string> row;
        for(int i = 0; i < argc; i++) {
            row.push_back(argv[i] ? argv[i] : "NULL");
        }
        queryResults.push_back(row);
        return 0;
    }

    // Query total duration for a specific language today
    float getTotalDurationForLanguage(sqlite3* db, const string& language, const string& date) {
        string query = "SELECT SUM(duration_sec) FROM sessions WHERE language='" + language + 
                       "' AND date(timestamp)='" + date + "';";
        
        queryResults.clear();
        char *errMessage = 0;
        
        if(sqlite3_exec(db, query.c_str(), queryCallback, 0, &errMessage) != SQLITE_OK) {
            cerr << "Query error: " << errMessage << endl;
            sqlite3_free(errMessage);
            return 0.0;
        }
        
        if(queryResults.size() > 0 && queryResults[0].size() > 0) {
            return stof(queryResults[0][0]);
        }
        return 0.0;
    }

    // Query top projects by language/file for a specific date
    void getTopProjects(sqlite3* db, const string& date) {
        string query = "SELECT file, language, SUM(duration_sec) as total FROM sessions " \
                       "WHERE date(timestamp)='" + date + "' GROUP BY file, language ORDER BY total DESC;";
        
        queryResults.clear();
        char *errMessage = 0;
        
        if(sqlite3_exec(db, query.c_str(), queryCallback, 0, &errMessage) != SQLITE_OK) {
            cerr << "Query error: " << errMessage << endl;
            sqlite3_free(errMessage);
            return;
        }
        
        cout << "\n=== Top Projects ===" << endl;
        for(const auto& row : queryResults) {
            if(row.size() >= 3) {
                cout << row[0] << " (" << row[1] << "): " << stof(row[2]) << "s" << endl;
            }
        }
    }

    // Calculate focus streaks (consecutive 60s blocks)
    int calculateFocusStreaks(sqlite3* db, const string& date) {
        string query = "SELECT COUNT(*) FROM sessions WHERE date(timestamp)='" + date + "';";
        
        queryResults.clear();
        char *errMessage = 0;
        
        if(sqlite3_exec(db, query.c_str(), queryCallback, 0, &errMessage) != SQLITE_OK) {
            cerr << "Query error: " << errMessage << endl;
            sqlite3_free(errMessage);
            return 0;
        }
        
        if(queryResults.size() > 0 && queryResults[0].size() > 0) {
            return stoi(queryResults[0][0]);
        }
        return 0;
    }

    // Display daily stats
    void displayDailyStats(sqlite3* db, const string& date) {
        cout << "\n=== Productivity Stats for " << date << " ===" << endl;
        
        float cppDuration = getTotalDurationForLanguage(db, "C++", date);
        cout << "\nHow much C++ today? " << cppDuration << " seconds (" << (cppDuration / 60.0) << " minutes)" << endl;
        
        getTopProjects(db, date);
        
        int focusStreaks = calculateFocusStreaks(db, date);
        cout << "\nFocus Streaks: " << focusStreaks << " blocks of 60 seconds" << endl;
    }
    int main(int argc, char* argv[]){

        // Handle stats command
        if(argc > 1 && string(argv[1]) == "stats") {
            sqlite3* data;
            int file = sqlite3_open("activity.db", &data);
            
            if(file != SQLITE_OK){
                cout << "File did not open." << endl;
                return 1;
            }
            
            // Get today's date or use provided date
            time_t now = time(0);
            tm* ltm = localtime(&now);
            char dateBuffer[11];
            strftime(dateBuffer, sizeof(dateBuffer), "%Y-%m-%d", ltm);
            string date = (argc > 2) ? argv[2] : dateBuffer;
            
            displayDailyStats(data, date);
            sqlite3_close(data);
            return 0;
        }

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


