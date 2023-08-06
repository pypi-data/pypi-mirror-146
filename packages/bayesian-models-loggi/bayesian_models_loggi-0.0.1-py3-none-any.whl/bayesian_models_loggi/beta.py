import numpy as np
import plotly.figure_factory as ff

class BetaBayes:
    
    def __init__(self, alpha_priori, beta_priori, success_count, failure_count):
        self.alpha_priori = alpha_priori
        self.beta_priori = beta_priori
        self.success_count = success_count
        self.failure_count = failure_count
        self.sample = None
        self.sample_size = None
        self.all_scenarios = {}

    def generate_posteriori_sample(self, sample_size = 1000, return_data = False, name = 0):
        alpha_posteriori = self.alpha_priori + self.success_count
        beta_posteriori = self.beta_priori + self.failure_count
        
        if (self.sample_size is not None) and self.sample_size != sample_size:
            self.all_scenarios = {}
        
        self.sample_size = sample_size
        
        self.name = name
        self.sample = np.random.beta(a = alpha_posteriori, b = beta_posteriori, size = sample_size)
        self.all_scenarios[name] = self.sample
        
        
        if return_data:
            return self.sample
    
    def plot(self):
        if self.sample is not None:
            fig = ff.create_distplot([self.sample], [self.name], show_hist=False, show_rug=False)
            fig.show()
        else:
            raise Exception("You need to run the method `generate_posteriori_sample` first.")
            
    def generate_new_scenario(self, alpha_priori, beta_priori, success_count, failure_count, 
                              return_data = False, name = None):
        if self.sample is not None:
            alpha_posteriori = alpha_priori + success_count
            beta_posteriori = beta_priori + failure_count
            
            if name is None:
                scenario_name = len(self.all_scenarios.keys())
            else:
                scenario_name = name
            
            sample = np.random.beta(a = alpha_posteriori, b = beta_posteriori, size = self.sample_size)
            
            self.all_scenarios[scenario_name] = sample

            if return_data:
                return sample
        else:
            raise Exception("You need to run the method `generate_posteriori_sample` first.")
            
    def plot_scenarios(self, names = None):
        if (names is None) or (names == "all") or (names == list(self.all_scenarios.keys())):
            fig = ff.create_distplot(list(self.all_scenarios.values()),
                                     list(self.all_scenarios.keys()), 
                                     show_hist=False, show_rug=False)
            fig.show()
        elif type(names) == list:
            names_diff = set(names).intersection(set(self.all_scenarios.keys()))
            series = [self.all_scenarios[serie_name] for serie_name in names_diff]
            
            fig = ff.create_distplot(names_diff,
                                     series, 
                                     show_hist=False, show_rug=False)
            fig.show()
        else:
            raise Exception("You need to define the `names` param as a listo or as 'all'.")
            
    def prob_lower_than_constant(self, value, scenario_name = None):
        if scenario_name is None:
            scenario_name = self.name
            
        scenario_is_lower_count = (self.all_scenarios[scenario_name] < value).sum()
        scenario_is_lower_prob = 100 * scenario_is_lower_count/self.sample_size
        
        
        print("The probability that scenario {0} is lower than {1} is {2:.2f}%.".\
                 format(scenario_name, value, scenario_is_lower_prob))
            
        return scenario_is_lower_prob
    
    def prob_between_scenarios(self, scenario_name_1, scenario_name_2):
        all_scenarios_names = self.get_all_scenarios_names()
        
        if scenario_name_1 not in all_scenarios_names:
            raise Exception("The scenario name {0} is not defined.These are the available scenarios: {1}."\
                            .format(scenario_name_1, ", ".join(all_scenarios_names)))
        elif scenario_name_2 not in all_scenarios_names:
            raise Exception("The scenario name {0} is not defined.These are the available scenarios: {1}."\
                            .format(scenario_name_2,  ", ".join(all_scenarios_names)))
        else:
            scenario_1_is_lower_count = (self.all_scenarios[scenario_name_1]
                                         < self.all_scenarios[scenario_name_2]).sum()
            scenario_1_is_lower_prob = 100 * scenario_1_is_lower_count/self.sample_size
            
            print("The probability that scenario {0} is lower than scenario {1} is {2:.2f}%.".\
                 format(scenario_name_1, scenario_name_2, scenario_1_is_lower_prob))
            
            return scenario_1_is_lower_prob
    
    def get_all_scenarios_names(self):
        return list(self.all_scenarios.keys())

    def get_all_scenarios_data(self):
        return self.all_scenarios
    
    def remove_scenarios(self, removal):
        if removal == "all":
            self.all_scenarios = {}
        elif (type(removal) == str) or (type(removal) == int):
            del self.all_scenarios[removal]
        elif type(removal) == list:
            for name in removal:
                del self.all_scenarios[name]