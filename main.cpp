    #include <windows.h>
    #include <winuser.h>
    #include <iostream>
   

    using namespace std;
    int main(void){

       // Manages the foreground process.
       HWND foreground = GetForegroundWindow();
       
       // Enters the loop if the foreground processes is active
        if(foreground != NULL){

            char processName[256];
            GetWindowText(foreground, processName, 256);
            cout<<processName;
        }
        return 0;
    }


