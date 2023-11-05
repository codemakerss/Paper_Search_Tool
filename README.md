# Paper_Search_Tool
This project aims to help researchers to easily find the paper they wanted without going to the main journal or other paper research websites.

## Demo 

#### - Light Mode

![light](https://github.com/codemakerss/Paper_Search_Tool/blob/main/img/light_mode.jpg)

#### - Dark Mode

![dark](https://github.com/codemakerss/Paper_Search_Tool/blob/main/img/dark_mode.jpg)

## How to use

- Set up a virtual environment before proceed to following steps:

  ```bash
  python3 -m venv venv # set up virtual environment
  ```

  ```bash
  source venv/bin/activate # activate virtual environment
  ```
  
- Safe Mode (Recommend)

  1. git clone to your own directory 

  ```bash
  git clone https://github.com/codemakerss/Paper_Search_Tool.git
  ```

  2. find and go to the directory called `src`
  ```bash
  cd ./Paper_Search_Tool/src
  ```
  
  3. install all dependencies from `requirements.txt`
  ```bash
  pip install -r requirements.py 
  ```
  
  4. run the app
  ```bash
  python3 Paper_Search.py 
  ```
  
- Applicaton (Beta - MacOS only)

  1. git clone to your own directory 

  ```bash
  git clone https://github.com/codemakerss/Paper_Search_Tool.git
  ```
  
  2. find and go to the directory called `dist`
  ```bash
  cd ./Paper_Search_Tool/src/dist
  ```

  3. open the `PaperSearchApp.app` application
  ```bash
  open -a PaperSearchApp.app
  ```
  
## Features (only support arXiv this moment)

|  Parameters  | Data Type |                            Usage                             |
| :----------: | :-------: | :----------------------------------------------------------: |
| Search query |  string   | words user want to search for<br />note : if you want to search for two words and above, please use this format: `quant+finance` or `web3+blockchain` |
|  Search by   |  string   |      user can search by `title`, `abstract`, `category`      |
|   Taxonomy   |  string   | more taxonomy information can be found at : https://arxiv.org/category_taxonomy |
|   Id list    |  string   |              comma-delimited list of arXiv id's              |
| Max results  |    int    |  maximum number chucks of the results to download at a time  |

Note: If user select `category` for `Search by`, then user also must select one value from `Taxonomy`

## Functions

|   Functions    |                           Perform                            |
| :------------: | :----------------------------------------------------------: |
|      Copy      | right click the result cell in the middle to see the pop-up menu for user to copy content |
| Download Paper | right click the result cell in the middle to see the pop-up menu for user to download paper |

## Other

For more information, please visit [ArXiv Official Page](https://arxiv.org) and their [API Documents](https://info.arxiv.org/help/api/index.html).

## License

[MIT](https://choosealicense.com/licenses/mit/)



