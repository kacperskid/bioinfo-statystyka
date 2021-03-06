# -*- coding: cp1250 -*-
from kpstat_tests import *
import pandas as pd
import scipy.stats
from collections import OrderedDict


class StatsExecutor:
    """Perform many tests on one data at once.

    Inputs are path of file, separator and header (0-no header, 1-header present).
    To print out summary, type analysis_name.print_results().
    To write html or txt summary, type type analysis_name.write_txt() or analysis_name.write_tho()
    """
    def __init__(self, filepath, sep=",", header=0):
        """Initializes file, generates data structure and finally automatically runs tests"""
        self.data = pd.read_csv(filepath, sep=sep, header=header) #wczytanie danych z pomoc� pandas
        self.summary = self._summarize() #statystyki opisowe dodane do obiektu
        self.headers_of_numeric_columns = list(self.summary)  #daje naglowki z kolumn podsumowania ktore automatycznie oblicza je tylko dla kolumn numerycznych
        
        self.results = OrderedDict() #tworzy liste wynikowa
        self._prepare_results_storage() #dodaje do listy wynikowej listy i slowniki z testami
        self._make_common_tests_set() #uruchamia wszystkie testy, mozna zahashowac 

    def _summarize(self):
        """Performs basic descriptive statistics using pandas"""
        return self.data.describe()# korzysta z wbudowanej metody dla obiektu csv od pandas dla statystyk opisowych

    def _prepare_results_storage(self):
        """Prepares containers for results"""
        self.results["Shapiro"] = []
        self.results["Chisq"] = []
        self.results["Spearman"] = self.prepare_complex_multilayer_container()
        self.results["Anova"] = self.prepare_complex_multilayer_container()
        self.results["Ttest"] = self.prepare_complex_multilayer_container()
        self.results["Pearson"] = self.prepare_complex_multilayer_container()
        self.results["Kruskal"] = self.prepare_complex_multilayer_container()

    def prepare_complex_multilayer_container(self):
        """Prepares container for tests that compare  different columns, requires """
        container_for_each_header = {name: {} for name in self.headers_of_numeric_columns}
        return container_for_each_header

    def _make_common_tests_set(self):
        """Automaticaly creates common tests for data, data, headers and summary need to be initialized """
        headers_copy = self.headers_of_numeric_columns[:] #kopije nag��wki na potrzeby metody
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
        """Main method for printing analysis results in console. Obviously requires launching analysis first"""
        self.print_summary() 
        for test_name in self.results:
            self._print_section(test_name)
            if isinstance(self.results[test_name], dict): #sprawdzenie czy wyniki sa slownikiem, jak nie to znak ze jest to slownik i trzeba uzyc innej prezentacji danych
                for header1 in self.results[test_name]:
                    for header2 in self.results[test_name][header1]:
                        print(header1, header2, "\n \t",
                              "test-statistics ", self.results[test_name][header1][header2][0],
                              "\n \t",
                              "p-value ", self.results[test_name][header1][header2][1],
                              "\n")
            else:
                for result in zip(self.headers_of_numeric_columns, self.results[test_name]): #iteracja po zzipowanej krotce naglowkow i wynikow
                    print(
                        "{0} : \n \t p-value {1} \n \t test-statistics {2}".format(result[0], result[1][0], result[1][1]))
            print("\n" * 3)

    def print_summary(self):
        """Prints out summary table"""
        self._print_section("SUMMARY")
        print(self.summary)
        print("\n" * 3)

    def write_txt(self,name="result.txt"):
        """Writes summary to text file, input is filename"""
        self.report_file=open(name,"w")
        self.write_summary()
        for test_name in self.results:
            self._write_section(test_name)
            if isinstance(self.results[test_name], dict):
                for header1 in self.results[test_name]:
                    for header2 in self.results[test_name][header1]:
                        
                        self.report_file.write("\n")
                        self.report_file.write(header1 + "-"+ header2)
                        self.report_file.write("\n \t test-statistics: ")
                        self.report_file.write(str(self.results[test_name][header1][header2][0]))
                        self.report_file.write("\n \t p value: ")
                        self.report_file.write(str(self.results[test_name][header1][header2][1]))
                        self.report_file.write("\n")

            else:
                for result in zip(self.headers_of_numeric_columns, self.results[test_name]):
                    self.report_file.write(str(
                        "\n {0} : \n \t test-statistics {1} \n \t p value {2}".format(result[0], result[1][0], result[1][1])))
            self.report_file.write("\n" * 3)
        self.report_file.close()
        
    def write_summary(self):
        """Writes summary for write_txt method"""
        self.report_file.write("SUMMARY\n")
        self.report_file.write(str(self.summary))
        self.report_file.write("\n" * 3)        

    @staticmethod
    def _print_section(section_name):
        """Prints current name of section and lots of stars for neat look"""
        print("-" * 50)
        print(section_name)
        print("-" * 50)

    def _write_section(self,section_name):
        """Writes to file name of current section"""
        self.report_file.write("-" * 50)
        self.report_file.write(section_name)
        self.report_file.write("-" * 50+"\n")

    def write_html(self,name="result.html"):
        """Main method for creating html formatted results"""
        self.report_file_html=open(name,"w")
        self.write_summary_html()
        for test_name in self.results:
            self._write_section_html(test_name)
            if isinstance(self.results[test_name], dict):
                for header1 in self.results[test_name]:
                    for header2 in self.results[test_name][header1]:
                        self.report_file_html.write("<p>\n")
                        self.report_file_html.write("\n")
                        self.report_file_html.write(header1 + "-"+ header2)
                        self.report_file_html.write("</br>\n \t test-statistics: ")
                        self.report_file_html.write(str(self.results[test_name][header1][header2][0]))
                        self.report_file_html.write("</br>\n \t p value:")
                        self.report_file_html.write(str(self.results[test_name][header1][header2][1]))
                        self.report_file_html.write("</br>\n")
                        self.report_file_html.write("</p>\n")

            else:
                for result in zip(self.headers_of_numeric_columns, self.results[test_name]):
                    self.report_file_html.write(str(
                        "\n<p>\n {0} : </br> \n \t test-statistics {1} </br>\n \t p value {2}</br>\n</p>".format(result[0], result[1][0], result[1][1])))
            self.report_file_html.write("\n</div>\n")
        self.report_file_html.write("\n</div>\n</body>\n</html>")
        self.report_file_html.close()
            
    def write_summary_html(self):
        """Generates html header and formatted summary table"""
        self.report_file_html.write(str("<html>\n<head>\n<link rel=\"stylesheet\" href=\"styles.css\">\t\n<title>Analysis results</title>\n</head>\n<body>\n<div class=\"main_container\">\n<div id=\"summary_table\">\n"))
        self.report_file_html.write("<h2>SUMMARY</h2>\n</br>\n")
        self.report_file_html.write(self.summary.to_html())
        self.report_file_html.write("\n</div>\n")   
        
    def _write_section_html(self,section_name):
        """Generate secion name"""
        self.report_file_html.write("<div class=\"test\"><h2>")
        self.report_file_html.write(section_name)
        self.report_file_html.write("</h2>\n")




if __name__ == '__main__':
    """This part of program launches only when the file is directly executed"""
    tests = StatsExecutor("data.csv", sep=",", header=0)
    #tests.print_results()
    #tests.write_txt()
    tests.write_html()
    instance_test(tests)
    close_test(tests.report_file_html)
    file_test("./result.html")
