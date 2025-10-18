# VSCode integration

![logo](img/vscode_logo.svg) 

Installation (extensions, settings) can be found [here](./tools_st_clt.md). 

## Open a project

To open a project, simply open the appropriate **folder**: `File -> Open Folder`.

You should open the **FOLDER**, not only the `main.c` file!!

![](img/vscodeOpenProject.png)

You can see that there is a `.vscode` folder (hidden on Linux/Mac) that contains the full configuration:
 * possibly `c_cpp_properties.json` give some information about the configuration of the C/C++ parts. The intelliSense mode for auto-completion needs it. It defines a configuration named `STM32 ARM`
 * `launch.json` get some information on how to use st-link when debugging.
 * possibly `settings.json` just tells that CMake will use a cross compiler.

## Compilation

The *build* button is on the status bar in the bottom of the window.

![](img/vscodeBuildProject.png)

A *compiler kit* should be selected. The first time, no *kit* is selected. One click on the `No kit selected` text leads to a menu:

![](img/vscodeSelectKit.png)

You have to choose the `arm-none-eabi` kit. If the cross compiler does not appear, it means that the compiler is not well installed. Have a look to the path (environment variable for your OS).

as soon as the kit is selected, a click on the build button causes the compilation. If everything goes well, the message `Build finished with exit code 0` is printed:

![](img/vscodeBuildOk.png)

## Debug session

For a debug session, just type **`F5`**, and choose the `debugger` view.

![](img/vscodeDebugProject.png)

You can use the classic buttons:
![](img/vscodeDebugButtons.png)
 * play/stop: run and pause the application on the real target
 * step onto: step one line. If it is a function, execute it.
 * step into: step one line. If it is a function, just go inside the function.
 * step out: get out of the function
 * restart: reset the application
 * **close**: close **correctly** the debugger (so that next debug session will start more easily…)

 You can use all the debugger windows:
 * variables
 * watch
 * call stack (nested function calls)
 * breakpoints (remove, disable, …)
 * Cortex peripherals => register access.

![](img/vscodeDebugRunning.png)