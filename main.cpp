    #include <windows.h>
    #include <winuser.h>
    #include <iostream>
    #include <stdio.h>
    #include <string>
    #include <sql.h>
    using namespace std;
    int main(void){

       // Manages the foreground process.
       HWND foreground = GetForegroundWindow();
       
       // Enters the loop if the foreground processes is active
        if(foreground != NULL){
            // Store the foreground process information
            char processName[256];
            GetWindowText(foreground, processName, 256);
            string process = (string)processName;
            // Slice the string to find filename + language using the file extension.
            string filename = process.substr(0, process.find("-")-1);
            string language = filename.substr(filename.find("."), filename.size()-1);
            cout<<"File: "<<filename<<'\n'<< "Extension: "<<language;
        }
        return 0;
    }


