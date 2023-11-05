import requests
import pandas as pd
import xml.etree.ElementTree as ET
# “Thank you to arXiv for use of its open access interoperability.”

def search_by_define(search_query : str, search_by : str, category_taxonomy : str = ""):
    """
    defined the exact search query as user wanted 

    reference : https://info.arxiv.org/help/api/user-manual.html#query_details

    Args:
    search_by (str): search by prefix
    category (str): default will be empty as not searched by category / fields

    category can be found at https://arxiv.org/category_taxonomy

    Return:
    str : final crafted and customized search string
    """
    # search by title 
    if ((search_by == "title") & (len(category_taxonomy) == 0)):
        search_query = "ti:" + search_query 

    # search by abstract
    if ((search_by == "abstract") & (len(category_taxonomy) == 0)):
        search_query = "abs:" + search_query

    # search by category / fields 
    if (search_by == "category"):
        search_query = "cat:" + category_taxonomy

    # search by combinations of "title" + "category"
    if ((search_by == "title") & (len(category_taxonomy) != 0)):
        search_query = "ti:" + search_query + "+AND+cat:" + category_taxonomy

    # search by combinations of "abstract" + "category"
    if ((search_by == "abstract") & (len(category_taxonomy) != 0)):
        search_query = "abs:" + search_query + "+AND+cat:" + category_taxonomy

    return search_query

def arxiv_search(search_query : str = "", id_list : str = "", start : int = 0, max_results : int = 10, sortBy : str = "submittedDate", sortOrder : str = "descending", search_by : str = "title", category_taxonomy : str = "") -> str:
    """
    perform arxiv search based on specific query, id
    set default start to be 0 as returned by first 10 results
    set default max_results to be 10

    Args:
    search_query (str): articles that match search_query
    search_by (str): three options offered "title" and "abstract" and "category"
    category_taxonomy (str): default will be empty as not searched by category / fields
    id_list (str): articles that are in id_list
    start (int): the index of the first returned result
    max_results (int): number of results returned by the query
    sortBy (str): sortBy can be "relevance", "lastUpdatedDate", "submittedDate"
    sortOrder (str): sortOrder can be either "ascending" or "descending"

    Return:
    str : contaning XML format of search results
    """
    try:
        # define customized search
        search_query = search_by_define(search_query = search_query, search_by = search_by, category_taxonomy = category_taxonomy)
        #print(search_query)
        # case 1 : only search for query 
        if (len(id_list) == 0):
            if (start == -1):
                arxiv_api = "http://export.arxiv.org/api/query?search_query={search_query}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}".format(search_query = search_query, max_results = max_results, sortBy = sortBy, sortOrder = sortOrder)
            else:
                arxiv_api = "http://export.arxiv.org/api/query?search_query={search_query}&start={start}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}".format(search_query = search_query, start = start, max_results = max_results, sortBy = sortBy, sortOrder = sortOrder)
        
        # case 2 : only search for articles in id list
        elif (len(search_query) == 0):
            if (start == -1):
                arxiv_api = arxiv_api = "http://export.arxiv.org/api/query?id_list={id_list}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}".format(id_list = id_list, max_results = max_results, sortBy = sortBy, sortOrder = sortOrder)
            else:
                arxiv_api = arxiv_api = "http://export.arxiv.org/api/query?id_list={id_list}&start={start}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}".format(id_list = id_list, start = start, max_results = max_results, sortBy = sortBy, sortOrder = sortOrder)
        
        # case 3 : search for both cases aka case1&case2
        elif (len(search_query) & len(id_list)):
            if (start == -1):
                arxiv_api = arxiv_api = "http://export.arxiv.org/api/query?search_query={search_query}&id_list={id_list}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}".format(search_query = search_query, id_list = id_list, max_results = max_results, sortBy = sortBy, sortOrder = sortOrder)
            else:
                arxiv_api = arxiv_api = "http://export.arxiv.org/api/query?search_query={search_query}&id_list={id_list}&start={start}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}".format(search_query = search_query, id_list = id_list, start = start, max_results = max_results, sortBy = sortBy, sortOrder = sortOrder)

        # print(arxiv_api)
        response = requests.get(url = arxiv_api)
        # print(arxiv_api)

        # check status code
        if (response.status_code == 200):
            # get string of XML data
            xml_search_data = response.text

            return xml_search_data

        else:
            return "We could not reach to arXiv API data this time. Try this later on."

    except Exception as e:

        raise e

def parse_xml_data(xml_data : str) -> dict:
    """
    parse XML data into human readable data including paper titles, data published, etc

    Args:
    xml_data (str): a string XML data

    Return:
    dict : contaning all paper results information including date published, paper tile, paper summary, download link
    """    
    # parse the XML data
    base = ET.fromstring(xml_data)

    # arXiv XML followed with atom structures
    namespaces = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

    # initialize dictionary to store each result
    paper_results = {}
    paper_ref = 1

    # each entry for each result paper
    for entry in base.findall('atom:entry', namespaces = namespaces):
        entry_published = entry.find('atom:published', namespaces=namespaces).text
        #entry_id = entry.find('atom:id', namespaces=namespaces).text
        entry_title = entry.find('atom:title', namespaces=namespaces).text
        entry_summary = entry.find('atom:summary', namespaces=namespaces).text
        entry_summary = entry_summary.replace("\n", " ")

        # find paper pdf link
        pdf_link_element = entry.find("atom:link[@title='pdf']", namespaces=namespaces)
        if pdf_link_element is not None:
            pdf_link = pdf_link_element.attrib['href']

        # find fields related
        field = [category.attrib['term'] for category in entry.findall('atom:category', namespaces=namespaces)]
        
        # make field strings
        field_str = ""
        for f in range(len(field)):
            if (f != len(field)-1):
                field_str = field_str + field[f] + " | "
            else:
                field_str = field_str + field[f]
        #print(field_str)

        # store each data
        tmp_data = {"date published" : entry_published, "paper tile" : entry_title, "category fields" : field_str,"paper summary" : entry_summary, "download link" : pdf_link}

        # name as paper_1, paper_2 ...
        paper_results["paper_" + str(paper_ref)] = tmp_data

        paper_ref = paper_ref + 1

    return paper_results

def make_clickable(val):
    """
    make DataFrame link clickable

    cited from : https://stackoverflow.com/questions/56615331/pandas-hyper-link-to-one-of-the-columns-in-dataframe
    """
    # make target column become clickable
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)

def view_dataframe(data : dict) -> pd.DataFrame:
    """
    view search results as DataFrame format

    Args:
    data (str): paper search results

    Return:
    pd.DataFrame : all data presented as DataFrame
    """    
    try:
        # initialize all DataFrame here ...
        all_data_df = pd.DataFrame()

        # all data loop
        for k,v in data.items():
            # get each paper data
            tmp_store = data[k]

            # each element from paper data
            date_published = data[k]["date published"]
            paper_tile = data[k]["paper tile"]
            paper_fields = data[k]["category fields"]
            paper_summary = data[k]["paper summary"]
            paper_download_link = data[k]["download link"]

            # form temp DataFrame for each paper data
            temp_df = pd.DataFrame([[date_published, paper_tile, paper_fields, paper_summary, paper_download_link]], columns=["date_published", "paper_tile", "paper_fields", "paper_summary", "paper_download_link"])
            # add to the all_data 
            all_data_df = pd.concat([all_data_df, temp_df], ignore_index=True)

            # display whole messages
            pd.set_option('display.max_colwidth', None) 

        # make link clickable in the DataFrame
        # all_data_df.style.format({'paper_download_link': make_clickable})

        return all_data_df

    except Exception as e:
        raise e







































    