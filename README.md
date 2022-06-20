[![Deploy to Azure](https://aka.ms/deploytoazurebutton)][deployment-url]
[![Deploy to Azure Gov](https://aka.ms/deploytoazuregovbutton)][deployment-url-gov]

[deployment-url]: https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FiMicknl%2Fazure-functions-libpostal%2Fmain%2Fdeploy%2Faz_function_deployment.json

[deployment-url-gov]: https://portal.azure.us/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FiMicknl%2Fazure-functions-libpostal%2Fmain%2Fdeploy%2Faz_function_deployment.json


# azure-functions-libpostal
An Azure Function project which utilizes [libpostal](https://github.com/openvenues/libpostal), a C library for parsing and normalizing street addresses. This can be useful for matching address strings with a database, and it can be used with Azure Cognitive Search to split an address over multiple index fields.

Due to C binding required for Libpostal, we need to [create an Azure Function on Linux using a custom container](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python). This will require a Premium plan or Dedicated (App Service) plan.

## How to deploy

You can easily deploy this Azure Function in your own Azure environment, by clicking the Deploy to Azure button.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)][deployment-url] [![Deploy to Azure Gov](https://aka.ms/deploytoazuregovbutton)][deployment-url-gov]

This will deploy an Azure Function app with a dedicated App Service plan (B3 sku) using the provided Docker container of this project. The project can easily be forked to make code changes and/or infrastructure changes.

## Endpoints
### /api/ParseAddress (GET/POST)
**Input**: 
```json
{
	"address": "Evert van de Beekstraat 354, 1118 CZ Schiphol, Nederland",
}
```

or

```https://[APP_NAME].azurewebsites.net/api/ParseAddress?address=Evert%20van%20de%20Beekstraat%20354,%201118%20CZ%20Schiphol,%20Nederland```


**Output**:
```json
{
	"road": "evert van de beekstraat",
	"house_number": "354",
	"postcode": "1118cz",
	"city": "schiphol",
	"country": "nederland"
}
```

### /api/ParseAddressCognitiveSearch (POST)

**Input**:
```json
{
    "values": [
      {
        "recordId": "a1",
        "data":
           {
             "address": 
                "Evert van de Beekstraat 354, 1118 CZ Schiphol, Nederland "
           }
      },
      {
        "recordId": "b5",
        "data":
           {
             "address": 
                "One Microsoft Way, Redmond, WA 98052, United States"
           }
      },
      {
        "recordId": "c3",
        "data":
           {
             "address": null
           }
      }
    ]
}
```

**Output**:
```json
{
    "values": [
        {
            "recordId": "a1",
            "data": {
                "road": "evert van de beekstraat",
                "house_number": "354",
                "postcode": "1118cz",
                "city": "schiphol",
                "country": "nederland"
            }
        },
        {
            "recordId": "b5",
            "data": {
                "house": "one",
                "road": "microsoft way",
                "city": "redmond",
                "state": "wa",
                "postcode": "98052",
                "country": "united states"
            }
        },
        {
            "recordId": "c3",
            "errors": [
                {
                    "message": "Could not complete operation for record."
                }
            ]
        }
    ]
}
```


## Use with Cognitive Search

```json
{
    "skills": [
      {
        "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
        "name": "ParseAddressSkill",
        "description": "This skill calls an Azure Function binding to libpostal for fast international address parsing/normalization.",
        "uri": "https://[YOUR-DEPLOYED-FUNCTION].azurewebsites.net/api/ParseAddressCognitiveSearch",
        "context": "/document",
        "inputs": [
          {
            "name": "address",
            "source": "/document/address"
          }
        ],
        "outputs": [
		  {
            "name": "house",
            "targetName": "house"
          },
          {
            "name": "road",
            "targetName": "road"
          },
		  {
            "name": "house_number",
            "targetName": "house_number"
          },
		  {
            "name": "postcode",
            "targetName": "postcode"
          },
		  {
            "name": "city",
            "targetName": "city"
          },
		  {
            "name": "state",
            "targetName": "state"
          },
		  {
            "name": "country",
            "targetName": "country"
          }               
        ]
      }
  ]
}
```

## Getting Started with Azure Function

#### Project Structure
The main project folder (<project_root>) can contain the following files:

* **local.settings.json** - Used to store app settings and connection strings when running locally. This file doesn't get published to Azure. To learn more, see [local.settings.file](https://aka.ms/azure-functions/python/local-settings).
* **requirements.txt** - Contains the list of Python packages the system installs when publishing to Azure.
* **host.json** - Contains global configuration options that affect all functions in a function app. This file does get published to Azure. Not all options are supported when running locally. To learn more, see [host.json](https://aka.ms/azure-functions/python/host.json).
* **.vscode/** - (Optional) Contains store VSCode configuration. To learn more, see [VSCode setting](https://aka.ms/azure-functions/python/vscode-getting-started).
* **.venv/** - (Optional) Contains a Python virtual environment used by local development.
* **Dockerfile** - (Optional) Used when publishing your project in a [custom container](https://aka.ms/azure-functions/python/custom-container).
* **tests/** - (Optional) Contains the test cases of your function app. For more information, see [Unit Testing](https://aka.ms/azure-functions/python/unit-testing).
* **.funcignore** - (Optional) Declares files that shouldn't get published to Azure. Usually, this file contains .vscode/ to ignore your editor setting, .venv/ to ignore local Python virtual environment, tests/ to ignore test cases, and local.settings.json to prevent local app settings being published.

Each function has its own code file and binding configuration file ([**function.json**](https://aka.ms/azure-functions/python/function.json)).


#### Developing your Python function using VS Code

This project includes a devcontainer that can be used on GitHub Codespaces or Visual Studio Code with Docker. During first build, it wil compile the Libpostal C module and download all training data.

If you have not already, please checkout our [quickstart](https://aka.ms/azure-functions/python/quickstart) to get you started with Azure Functions developments in Python. 

#### Publishing your function app to Azure 

```sh
docker build --tag imicknl/azurefunctionsimage:v1.0.0 .
docker run -p 8080:80 -it imicknl/azurefunctionsimage:v1.0.0
```

For more information on deployment options for Azure Functions, please visit this [guide](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python#publish-the-project-to-azure).
