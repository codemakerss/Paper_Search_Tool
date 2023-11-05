import arxiv_researches as ar
import pandas as pd
def arxiv_search_without_constrains(search_query : str, num_results : int):
    """
    simple arXiv search with only query 

    Args:
    search_query : str
    num_results : int

    Returns:
    pd.DataFrame : all paper results
    """
    if (num_results):
        raw_data = ar.arxiv_search(search_query = search_query, search_by = "", category_taxonomy = "", id_list = "", start = -1, max_results = num_results)
    else:
        raw_data = ar.arxiv_search(search_query = search_query, search_by = "", category_taxonomy = "", id_list = "", start = -1, max_results = 10)
    
    result = ar.parse_xml_data(raw_data)
    final_data = ar.view_dataframe(result)

    return final_data

def arxiv_search_only_id_list(id_list : str):
    """
    simple arXiv search with only id list 

    Args:
    id_list : str
    num_results : int

    Returns:
    pd.DataFrame : all paper results
    """

    raw_data = ar.arxiv_search(search_query = "", search_by = "", category_taxonomy = "", id_list = id_list, start = -1, max_results = 1)
    
    result = ar.parse_xml_data(raw_data)
    final_data = ar.view_dataframe(result)


    return final_data

def arxiv_search_only_title(title : str, num_results : int):
    """
    simple arXiv search with only title

    Args:
    title : str
    num_results : int

    Returns:
    pd.DataFrame : all paper results
    """
    if num_results:
        raw_data = ar.arxiv_search(search_query = title, search_by = "title", category_taxonomy = "", id_list = "", start = -1, max_results = num_results)
    else:
        raw_data = ar.arxiv_search(search_query = title, search_by = "title", category_taxonomy = "", id_list = "", start = -1, max_results = 10)
    
    result = ar.parse_xml_data(raw_data)
    final_data = ar.view_dataframe(result)


    return final_data

def arxiv_search_only_abstract(abstract : str, num_results : int):
    """
    simple arXiv search with only abstract

    Args:
    abstract : str
    num_results : int

    Returns:
    pd.DataFrame : all paper results
    """
    if num_results:
        raw_data = ar.arxiv_search(search_query = abstract, search_by = "abstract", category_taxonomy = "", id_list = "", start = -1, max_results = num_results)
    else:
        raw_data = ar.arxiv_search(search_query = abstract, search_by = "abstract", category_taxonomy = "", id_list = "", start = -1, max_results = 10)
    
    result = ar.parse_xml_data(raw_data)
    final_data = ar.view_dataframe(result)


    return final_data

def arxiv_search_only_category(category_search : str, category_taxonomy : str, num_results : int):
    """
    simple arXiv search with only category

    Args:
    category_search : str
    category_taxonomy : int
    num_results : int

    Returns:
    pd.DataFrame : all paper results
    """
    if num_results:
        raw_data = ar.arxiv_search(search_query = category_search, search_by = "category", category_taxonomy = category_taxonomy, id_list = "", start = -1, max_results = num_results)
    else:
        raw_data = ar.arxiv_search(search_query = category_search, search_by = "category", category_taxonomy = category_taxonomy, id_list = "", start = -1, max_results = 10)
    
    result = ar.parse_xml_data(raw_data)
    final_data = ar.view_dataframe(result)   

    return final_data 

def arxiv_search_query_and_id_list():
    pass

def arxiv_search_title_and_category():
    pass
def arxiv_search_abstract_and_category():
    pass


# test_data = {'paper_1': {'date published': '2023-09-28T06:17:15Z', 'paper tile': 'Intergenerational Equity in Models of Climate Change Mitigation:\n  Stochastic Interest Rates introduce Adverse Effects, but (Non-linear) Funding\n  Costs can Improve Intergenerational Equity', 'category fields': 'q-fin.MF | econ.GN | q-fin.EC | 91-10 | I.6.3; J.4', 'paper summary': '  Assessing the costs of climate change is essential to finding efficient pathways for the transition to a net-zero emissions economy, which is necessary to stabilise global temperatures at any level. In evaluating the benefits and costs of climate change mitigation, the discount rate converting future damages and costs into net-present values influences the timing of mitigation.   Here, we amend the DICE model with a stochastic interest rate model to consider the uncertainty of discount rates in the future. Since abatement reduces future damages, changing interest rates renders abatement investments more or less beneficial. Stochastic interest rates will hence lead to a stochastic abatement strategy.   We introduce a simple stochastic abatement model and show that this can increase intergenerational inequality concerning cost and risk.   Analysing the sensitivities of the model calibration analytically and numerically exhibits that intergenerational inequality is a consequence of the DICE model calibration (and maybe that of IAMs in general).   We then show that introducing funding of abatement costs reduces the variation of future cash-flows, which occur at different times but are off-setting in their net-present value. This effect can be interpreted as improving intergenerational effort sharing, which might be neglected in classical optimisation. This mechanism is amplified, including dependence of the interest rate risk on the amount of debt to be financed, i.e. considering the limited capacity of funding sources. As an alternative policy optimisation method, we propose limiting the total cost of damages and abatement below a fixed level relative to GDP - this modification induces equality between generations compared to their respective economic welfare, inducing early and fast mitigation of climate change to keep the total cost of climate change below 3% of global GDP. ', 'download link': 'http://arxiv.org/pdf/2309.16186v2'}, 'paper_2': {'date published': '2023-09-19T23:50:45Z', 'paper tile': 'Bell Correlations as Selection Artefacts', 'category fields': 'quant-ph | physics.hist-ph', 'paper summary': '  We propose an explanation of the correlations characteristic of Bell experiments, showing how they may arise as a special sort of selection artefact. This explanation accounts for the phenomena that have been taken to imply nonlocality, without recourse to any direct spacelike causality or influence. If correct, the proposal offers a novel way to reconcile nonlocality with relativity. The present paper updates an earlier version of the proposal (arXiv:2101.05370v4 [quant-ph], arXiv:2212.06986 [quant-ph]) in two main respects: (i) in demonstrating its application in a real Bell experiment; and (ii) in avoiding the need for an explicit postulate of retrocausality. ', 'download link': 'http://arxiv.org/pdf/2309.10969v1'}, 'paper_3': {'date published': '2023-09-18T19:24:21Z', 'paper tile': 'Reasoning about the Unseen for Efficient Outdoor Object Navigation', 'category fields': 'cs.RO | cs.AI', 'paper summary': '  Robots should exist anywhere humans do: indoors, outdoors, and even unmapped environments. In contrast, the focus of recent advancements in Object Goal Navigation(OGN) has targeted navigating in indoor environments by leveraging spatial and semantic cues that do not generalize outdoors. While these contributions provide valuable insights into indoor scenarios, the broader spectrum of real-world robotic applications often extends to outdoor settings. As we transition to the vast and complex terrains of outdoor environments, new challenges emerge. Unlike the structured layouts found indoors, outdoor environments lack clear spatial delineations and are riddled with inherent semantic ambiguities. Despite this, humans navigate with ease because we can reason about the unseen. We introduce a new task OUTDOOR, a new mechanism for Large Language Models (LLMs) to accurately hallucinate possible futures, and a new computationally aware success metric for pushing research forward in this more complex domain. Additionally, we show impressive results on both a simulated drone and physical quadruped in outdoor environments. Our agent has no premapping and our formalism outperforms naive LLM-based approaches ', 'download link': 'http://arxiv.org/pdf/2309.10103v1'}, 'paper_4': {'date published': '2023-09-16T06:25:06Z', 'paper tile': 'Charged spherically symmetric black holes in scalar-tensor Gauss-Bonnet\n  gravity', 'category fields': 'gr-qc | hep-th', 'paper summary': '  We derive a novel class of four-dimensional black hole solutions in Gauss-Bonnet gravity coupled with a scalar field in presence of Maxwell electrodynamics. In order to derive such solutions, we assume the ansatz $ g_{tt}\\neq g_{rr}{}^{-1}$ for metric potentials. Due to the ansatz for the metric, the Reissner Nordstr\\"om gauge potential cannot be recovered because of the presence of higher-order terms ${\\cal O}\\left(\\frac{1}{r}\\right)$ which are not allowed to be vanishing. Moreover, the scalar field is not allowed to vanish. If it vanishes, a function of the solution results undefined. For this reason, the solution cannot be reduced to a Reissner Nordstr\\"om space-time in any limit. Furthermore, it is possible to show that the electric field is of higher-order in the monopole expansion: this fact explicitly comes from the contribution of the scalar field. Therefore, we can conclude that the Gauss-Bonnet scalar field acts as non-linear electrodynamics creating monopoles, quadrupoles, etc. in the metric potentials. We compute the invariants associated with the black holes and show that, when compared to Schwarzschild or Reissner-Nordstr\\"om space-times, they have a soft singularity. Also, it is possible to demonstrate that these black holes give rise to three horizons in AdS space-time and two horizons in dS space-time. Finally, thermodynamic quantities can be derived and we show that the solution can be stable or unstable depending on a critical value of the temperature. ', 'download link': 'http://arxiv.org/pdf/2309.08894v1'}, 'paper_5': {'date published': '2023-09-08T09:58:25Z', 'paper tile': 'Interband scattering- and nematicity-induced quantum oscillation\n  frequency in FeSe', 'category fields': 'cond-mat.str-el | cond-mat.dis-nn | cond-mat.supr-con', 'paper summary': '  Understanding the nematic phase observed in the iron-chalcogenide materials is crucial for describing their superconducting pairing. Experiments on FeSe$_{1-x}$S$_x$ showed that one of the slow Shubnikov--de Haas quantum oscillation frequencies disappears when tuning the material out of the nematic phase via chemical substitution or pressure, which has been interpreted as a Lifshitz transition [Coldea et al., npj Quant Mater 4, 2 (2019), Reiss et al., Nat. Phys. 16, 89-94 (2020)]. Here, we present a generic, alternative scenario for a nematicity-induced sharp quantum oscillation frequency which disappears in the tetragonal phase and is not connected to an underlying Fermi surface pocket. We show that different microscopic interband scattering mechanisms - for example, orbital-selective scattering - in conjunction with nematic order can give rise to this quantum oscillation frequency beyond the standard Onsager relation. We discuss implications for iron-chalcogenides and the interpretation of quantum oscillations in other correlated materials. ', 'download link': 'http://arxiv.org/pdf/2309.04237v1'}, 'paper_6': {'date published': '2023-09-06T17:18:55Z', 'paper tile': 'GPT-InvestAR: Enhancing Stock Investment Strategies through Annual\n  Report Analysis with Large Language Models', 'category fields': 'q-fin.ST | cs.CL | cs.LG', 'paper summary': '  Annual Reports of publicly listed companies contain vital information about their financial health which can help assess the potential impact on Stock price of the firm. These reports are comprehensive in nature, going up to, and sometimes exceeding, 100 pages. Analysing these reports is cumbersome even for a single firm, let alone the whole universe of firms that exist. Over the years, financial experts have become proficient in extracting valuable information from these documents relatively quickly. However, this requires years of practice and experience. This paper aims to simplify the process of assessing Annual Reports of all the firms by leveraging the capabilities of Large Language Models (LLMs). The insights generated by the LLM are compiled in a Quant styled dataset and augmented by historical stock price data. A Machine Learning model is then trained with LLM outputs as features. The walkforward test results show promising outperformance wrt S&P500 returns. This paper intends to provide a framework for future work in this direction. To facilitate this, the code has been released as open source. ', 'download link': 'http://arxiv.org/pdf/2309.03079v1'}, 'paper_7': {'date published': '2023-09-01T13:58:24Z', 'paper tile': 'On the flow of perfect energy tensors', 'category fields': 'gr-qc', 'paper summary': '  The necessary and sufficient conditions are obtained for a unit time-like vector field $u$ to be the unit velocity of a divergence-free perfect fluid energy tensor. This plainly kinematic description of a conservative perfect fluid requires considering eighteen classes defined by differential concomitants of $u$. For each of these classes, we get the additional constraints that label the flow of a conservative energy tensor, and we obtain the pairs of functions $\\{\\rho,p\\}$, energy density and pressure, which complete a solution to the conservation equations. ', 'download link': 'http://arxiv.org/pdf/2309.00463v2'}, 'paper_8': {'date published': '2023-08-22T11:10:58Z', 'paper tile': 'Transmission of optical communication signals through ring core fiber\n  using perfect vortex beams', 'category fields': 'physics.optics | quant-ph | physics.class-ph, quant-ph', 'paper summary': '  Orbital angular momentum can be used to implement high capacity data transmission systems that can be applied for classical and quantum communications. Here we experimentally study the generation and transmission properties of the so-called perfect vortex beams and the Laguerre-Gaussian beams in ring-core optical fibers. Our results show that when using a single preparation stage, the perfect vortex beams present less ring-radius variation that allows coupling of higher optical power into a ring core fiber. These results lead to lower power requirements to establish fiber-based communications links using orbital angular momentum and set the stage for future implementations of high-dimensional quantum communication over space division multiplexing fibers. ', 'download link': 'http://arxiv.org/pdf/2308.11354v2'}, 'paper_9': {'date published': '2023-08-19T03:01:45Z', 'paper tile': 'Inductive-bias Learning: Generating Code Models with Large Language\n  Model', 'category fields': 'cs.LG | cs.AI | cs.CL | cs.PL', 'paper summary': "  Large Language Models(LLMs) have been attracting attention due to a ability called in-context learning(ICL). ICL, without updating the parameters of a LLM, it is possible to achieve highly accurate inference based on rules ``in the context'' by merely inputting a training data into the prompt. Although ICL is a developing field with many unanswered questions, LLMs themselves serves as a inference model, seemingly realizing inference without explicitly indicate ``inductive bias''. On the other hand, a code generation is also a highlighted application of LLMs. The accuracy of code generation has dramatically improved, enabling even non-engineers to generate code to perform the desired tasks by crafting appropriate prompts. In this paper, we propose a novel ``learning'' method called an ``Inductive-Bias Learning (IBL)'', which combines the techniques of ICL and code generation. An idea of IBL is straightforward. Like ICL, IBL inputs a training data into the prompt and outputs a code with a necessary structure for inference (we referred to as ``Code Model'') from a ``contextual understanding''. Despite being a seemingly simple approach, IBL encompasses both a ``property of inference without explicit inductive bias'' inherent in ICL and a ``readability and explainability'' of the code generation. Surprisingly, generated Code Models have been found to achieve predictive accuracy comparable to, and in some cases surpassing, ICL and representative machine learning models. Our IBL code is open source: https://github.com/fuyu-quant/IBLM ", 'download link': 'http://arxiv.org/pdf/2308.09890v1'}, 'paper_10': {'date published': '2023-08-02T04:06:16Z', 'paper tile': 'QUANT: A Minimalist Interval Method for Time Series Classification', 'category fields': 'cs.LG', 'paper summary': "  We show that it is possible to achieve the same accuracy, on average, as the most accurate existing interval methods for time series classification on a standard set of benchmark datasets using a single type of feature (quantiles), fixed intervals, and an 'off the shelf' classifier. This distillation of interval-based approaches represents a fast and accurate method for time series classification, achieving state-of-the-art accuracy on the expanded set of 142 datasets in the UCR archive with a total compute time (training and inference) of less than 15 minutes using a single CPU core. ", 'download link': 'http://arxiv.org/pdf/2308.00928v1'}}
# result = ar.view_dataframe(test_data)
# # result = result.drop('paper_fields')
# result1 = result.to_dict(orient='list')
# result1.pop('paper_fields')
# print(result1)

# def test():
#     app = fe.App()
#     temp_query = app.get_serach_query_value()
#     if (temp_query != 0):
#         test1 = arxiv_search_without_constrains(temp_query)
#         print(test1)
#     app.mainloop()


# if __name__ == "__main__":
#     app = fe.App()
#     temp_query = app.get_serach_query_value()
#     if (temp_query != 0):
#         test1 = arxiv_search_without_constrains(temp_query)
#         print(test1)
    
    # print("test1: ", app.get_arxiv_search_by_optionmenu())
    # print("test2: ", app.get_arxiv_category_taxonomy_optionmenu())
    # print("test3: ", app.get_arxiv_id_list_textbox())
    # print("test4: ", app.get_arxiv_max_results())
    # print("test5: ", app.get_scholar_display_language())
    # print("test6: ", app.get_scholar_display_at_year())
    # print("test7: ", app.get_scholar_display_until_year())
    # print("test8: ", app.get_scholar_max_results())
    # app.mainloop()



