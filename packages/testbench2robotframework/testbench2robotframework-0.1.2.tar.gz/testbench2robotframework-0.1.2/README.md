## Creating robot files
To generate the robot files itb2robot needs two parameters.
A JSON configuration file and a directory or ZIP file containing the TestBench JSON report files.
If no configuration file is passed, itb2robot searches the current working directory for a file named "config.json".

```
tb2robot -c config.json path/to/json/files.zip
```

## Configuration of output
To configure the output of the converter a json configuration file is used. This file contains the following settings:

### rfLibraryRoots
A list of the different root subdivisions of the TestBench in which robot libraries are defined. Libraries that are not part of one of these subdivisions will not be imported into the robot file. The only exception to this are forced imports, which are always included in the robot files.

```json
"rfLibraryRoots": ["RobotLibraries", "RF"]
```

![rfLibraryRootsTestBench](./res/rfLibraryRootsTestBench.PNG)


### rfResourceRoots
Like the libraries, the root subdivisions of the resource files must also be specified. This can be done in rfResourceRoots.

```json
"rfResourceRoots": ["RF-Resources"]
```

### fullyQualified
Boolean variable that defines whether the library name is prepended to a keyword call.
```json
"fullyQualified": true
```

### resourceDirectory
Path to the directory which contains the used resource files.
The path can be absolute or relative. In case of a relative path, a "{root}" is prepended. This parameter is necessary to specify a relative path to the resource directory when importing the resources in the setting section of a robot file.

```json
"resourceDirectory": "{root}/Resources",
```

```robotframework
*** Settings ***
Resource    ../Resources/myKeywords.resource
```

### generationDirectory
Path to the directory where the robot files will be generated.
The path can be absolute or relative. As with the resource directory, a "{root}" can be prepended to indicate that this is a relative path

```json
"generationDirectory": "{root}/Generated"
```

### logSuiteNumbering
Boolean variable that defines whether the prefix of a directory that determines the execution order is shown in the logs.

```json
"logSuiteNumbering": true
```

### clearGenerationDirectory
Boolean variable that defines whether the specified generation directory and all files contained in it should be deleted before new robot files will be created.

```json
"clearGenerationDirectory": true,
```

### logCompoundInteractions
To generate not only the atomic interactions in the robot files, the parameter logCompoundInteractions can be set to true.
This way, compound interactions are displayed as comments in the robot code. Furthermore, the atomic interactions that make up these compound interactions are indented to indicate which parent interaction they belong to.

```json
"logCompoundInteractions": true,
```

### subdivisionsMapping
A dictionary that defines which library or resource should be imported in the robot file, if a keyword from the library/resource is used. The keys of the dictionaries are the names of the libraries or resources and the values represent the import statements.

```json
"subdivisionsMapping": {
  "libraries": {
    "SeleniumLibrary": "SeleniumLibrary    timeout=10    implicit_wait=1    run_on_failure=Capture Page Screenshot",
    "Schneewitchen": "MyLibrary"
  },
  "resources": {
    "MyKeywords": "MyKeywords.resource"
  }
}
```
### forcedImport
Specifies which libraries must be imported into each generated robot file regardless of whether a keyword from this library is used.

```json
"forcedImport": {
  "libraries": []
}
```

### loggingConfiguration
Option to set itb2robots log level.
Valid options are:
- "CRITICAL"
- "FATAL"
- "ERROR"
- "WARNING"
- "WARN"
- "INFO"
- "DEBUG"
- "NOTSET"

If no option is specified, the log level will be set to "INFO".

```json
"loggingConfiguration": {
  "console": {
    "logLevel": "info"
  }
}
```