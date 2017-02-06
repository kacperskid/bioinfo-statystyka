import pandas as pd
import scipy.stats
from collections import OrderedDict


class StatsExecutor:
    def __init__(self, filepath, sep=",", header=0):
        self.data = pd.read_csv(filepath, sep=sep, header=header)

        self.summary = self._summarize()
        self.headers_of_numeric_columns = list(self.summary)

        self.results = OrderedDict()
        self._prepare_results_storage()
        self._make_common_tests_set()

    def _summarize(self):
        return self.data.describe()

    def _prepare_results_storage(self):
        self.results["Shapiro"] = []
        self.results["Chisq"] = []
        self.results["Spearman"] = self.prepare_complex_multilayer_container()
        self.results["Anova"] = self.prepare_complex_multilayer_container()
        self.results["Ttest"] = self.prepare_complex_multilayer_container()
        self.results["Pearson"] = self.prepare_complex_multilayer_container()
        self.results["Kruskal"] = self.prepare_complex_multilayer_container()

    def prepare_complex_multilayer_container(self):
        container_for_each_header = {name: {} for name in self.headers_of_numeric_columns}
        return container_for_each_header

    def _make_common_tests_set(self):
        headers_copy = self.headers_of_numeric_columns[:]
        for name in self.headers_of_numeric_columns:
            self.results["Shapiro"].append(scipy.stats.shapiro(self.data[name]))
            self.results["Chisq"].append(scipy.stats.chisquare(self.data[name]))
            headers_copy.remove(name)
            for name2 in headers_copy:
                self.results["Spearman"][name][name2] = (scipy.stats.spearmanr(self.data[name], self.data[name2]))
                self.results["Anova"][name][name2] = scipy.stats.f_oneway(self.data[name], self.data[name2])
                self.results["Ttest"][name][name2] = scipy.stats.ttest_rel(self.data[name], self.data[name2])
                self.results["Pearson"][name][name2] = scipy.stats.pearsonr(self.data[name], self.data[name2])
                self.results["Kruskal"][name][name2] = scipy.stats.kruskal(self.data[name], self.data[name2])

    def print_results(self):
        self.print_summary()
        for test_name in self.results:
            self._print_section(test_name)
            if isinstance(self.results[test_name], dict):
                for header1 in self.results[test_name]:
                    for header2 in self.results[test_name][header1]:
                        print(header1, header2, "\n\t",
                              "test-statistics ", self.results[test_name][header1][header2][0],
                              "\n\t",
                              "p-value ", self.results[test_name][header1][header2][1],
                              "\n")
            else:
                for result in zip(self.headers_of_numeric_columns, self.results[test_name]):
                    print(
                        "{0} : \n\t p-value {1} \n\t test-statistics {2}".format(result[0], result[1][0], result[1][1]))
            print("\n" * 3)

    def print_summary(self):
        self._print_section("SUMMARY")
        print(self.summary)
        print("\n" * 3)

    @staticmethod
    def _print_section(section_name):
        print("-" * 50)
        print(section_name)
        print("-" * 50)


if __name__ == '__main__':
    tests = StatsExecutor("data.csv", sep=",", header=0)
    tests.print_results()