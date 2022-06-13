![Deploy to Azure](https://aka.ms/deploytoazurebutton)

# azure-functions-libpostal
An Azure Function project which utilizes [libpostal](https://github.com/openvenues/libpostal), a C library for parsing and normalizing street addresses. This can be useful for matching address strings with a database, and it can be used with Azure Cognitive Search to split an address over multiple index fields.

Due to C binding required for Libpostal, we need to [create an Azure Function on Linux using a custom container](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python). This will require a Premium plan or Dedicated (App Service) plan.


## Example
**Input**: Evert van de Beekstraat 354, 1118 CZ Schiphol, Nederland

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
