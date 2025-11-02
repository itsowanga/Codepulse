    #include <windows.h>
    #include <winuser.h>
    #include <iostream>
    #include <string>

    using namespace std;
    int main(void){

       // Manages the foreground process.
       HWND foreground = GetForegroundWindow();
       
       // Enters the loop if the foreground processes is active
        if(foreground != NULL){

            char processName[256];
            GetWindowText(foreground, processName, 256);
            string process = (string)processName;
            string filename = process.substr(0, process.find("-")-1);
            string language = filename.substr(filename.find("."), filename.size()-1);
            string editorName = process.substr(process.rfind("-")+2, process.size()-1);
            cout<<"File: "<<filename<<'\n'<< "Extension: "<<language<<'\n'<<"Editor: "<<editorName;
        }
        return 0;
    }


