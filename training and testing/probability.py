import psycopg2, csv
from db import postgres
path = r"C:/Users/Ugochukwu/Desktop/GIS classes/Directed research/tables and results_trimmed_data"


class BayesPrediction:
    def __init__(self, host='localhost', database='postgres', schema='francis', user= 'postgres', passwd='doesql'):
        self.db = postgres(database=database, schema=schema)
        self.db.connect()
        self.country_list = []
        self.class_list = [29, 88, 206, 8, 64, 71, 85, 187, 23, 153]
        self.prior_go = []
        self.prior_nogo = []
        self.prior_set = []
        self.rows_training = 0
        self.rows_test =0
        self.list_likelyhood_go = []
        self.list_likelyhood_nogo = []
        self.likelyhood_set =[]
        self.feature_template = []
        self.test_truth = [] #stores the truth of test data by each class
        self.feature_template_transpose = []
        self.combo_likelyhood_go = []
        self.combo_likelyhood_nogo = []
        self.list_pp_go = []
        self.list_pp_nogo = []
        self.pp_set = []
        self.list_prediction = []
        self.list_accruacy = []
    def count_unique_country(self):
        """
        this function count how many countries are there in the database,
        and store all the country codes in self.country_list
        :return:
        """
        sql_str_uniq_cty = r"with temp as (select unnest(uniq_arr_country) as m from francis.usa_training)" \
                  r"select array_agg(m) t from temp"
        country_list = self.db.select(sql_str_uniq_cty)
        country_list = list(set(country_list[0]))
        self.country_list = country_list

    def count_rows(self):
        """
        this function counts how many rows are there in training table and test table
        :return:
        """
        str_sql_training = r"select count(*) from francis.usa_training"
        rows = self.db.select(str_sql_training)
        self.rows_training = rows[0]
        str_sql_test = r"select count(*) from francis.usa_test"
        rows = self.db.select(str_sql_test)
        self.rows_test = rows[0]

    def calc_prior_prob(self):
        """
        this function calcuates prior probability of going and not going
        :return:
        """
        for item in self.class_list:
            str_sql_go = r"select count (uniq_arr_country) " \
                      r"from francis.usa_training " \
                      r"where uniq_arr_country @> ARRAY[{0}]".format(item)
            str_sql_nogo = r"select count (uniq_arr_country) " \
                           r"from francis.usa_training " \
                           r"where not (uniq_arr_country @> ARRAY[{0}])".format(item)

            rows_go = self.db.select(str_sql_go)[0]
            rows_nogo = self.db.select(str_sql_nogo)[0]
            self.prior_go.append(rows_go/(self.rows_training*1.0))
            self.prior_nogo.append(rows_nogo/(self.rows_training*1.0))
            self.prior_set.append([self.prior_go,self.prior_nogo])


    def calc_likelyhood(self):
        """
        this function calcualtes the likelyhood of each feature in going group and not-going group.
        the results are stored in self.likelyhood_set, for example:
        [[likelyhood_go, likelyhood_nogo],[class2], [class3], [class4].....]
        :return:
        """
        for group in self.class_list:
            if len(self.list_likelyhood_go) > 0: del self.list_likelyhood_go[:]
            if len(self.list_likelyhood_nogo) > 0: del self.list_likelyhood_nogo[:]
            for feature in self.country_list:
                if feature != group:
                    str_sql_go = "select count (uniq_arr_country) " \
                              "from francis.usa_training " \
                              "where uniq_arr_country @> ARRAY[{0}] " \
                              "and uniq_arr_country @> ARRAY[{1}]".format(feature, group)

                    str_sql_nogo = r"select count (uniq_arr_country) " \
                                   r"from francis.usa_training " \
                                   r"where uniq_arr_country @> ARRAY[{0}] " \
                                   r"and not uniq_arr_country @> ARRAY[{1}]".format(feature,group)

                    a_go = self.db.select(str_sql_go)[0]
                    a_nogo = self.db.select(str_sql_nogo)[0]
                    str_sql_c_go = r"select sum(array_length(uniq_arr_country,1)) " \
                                   r"from francis.usa_training " \
                                   r"where uniq_arr_country @> ARRAY[{0}]".format(group)
                    str_sql_c_nogo = r"select sum(array_length(uniq_arr_country,1)) " \
                                     r"from francis.usa_training " \
                                     r"where NOT uniq_arr_country @> ARRAY[{0}]".format(group)
                    c_go = self.db.select(str_sql_c_go)[0]
                    c_nogo = self.db.select(str_sql_c_nogo)[0]
                    likelyhood_go = (a_go+1)/(c_go*1.0+(len(self.country_list)))
                    likelyhood_nogo = (a_nogo+1)/(c_nogo*1.0+(len(self.country_list)))
                else:
                    likelyhood_go = 0
                    likelyhood_nogo = 0
                self.list_likelyhood_go.append(likelyhood_go)
                self.list_likelyhood_nogo.append(likelyhood_nogo)
            self.likelyhood_set.append([self.list_likelyhood_go,self.list_likelyhood_nogo])


    def calc_feature_template(self):
        """
        calcuate the template
        :return:
        """
        for feature in self.country_list:
            sql_str_temp = r"select case when uniq_arr_country@>array[{0}] then 1 " \
                      r"else 0 END from francis.usa_test".format(feature)
            rows = self.db.select(sql_str_temp)
            self.feature_template.append(rows)



    def calc_truth_test(self):
        """
        calculate the truth of test data for 10 classes
        :return:
        """
        for group in self.class_list:
            str_sql_truth = r"select CASE when uniq_arr_country@>array[{0}] then 1 " \
                      r"else 0 END from francis.usa_test".format(group)
            rows = self.db.select(str_sql_truth)
            self.test_truth.append(rows)
        # #loop to print it out
        #
        # with open(path + '/truth_test.csv', 'a') as result:
        #     writter = csv.writer(result, delimiter='\t')
        #     for item in self.test_truth:
        #         writter.writerow(item)

    def calc_pp(self):
        for i in range(0,self.rows_test):
            self.feature_template_transpose.append([row[i] for row in self.feature_template])
        for index, group in enumerate(self.class_list):
            likelyhood_go = self.likelyhood_set[index][0]
            likelyhood_nogo = self.likelyhood_set[index][1]
            if len(self.list_pp_go) > 0: del self.list_pp_go[:]
            if len(self.list_pp_nogo) > 0: del self.list_pp_nogo[:]
            for row in self.feature_template_transpose:
                self.combo_likelyhood_go = [a*b for a, b in zip(likelyhood_go, row)]
                self.combo_likelyhood_nogo = [a*b for a, b in zip(likelyhood_nogo,row)]
                self.combo_likelyhood_go = [a for a in self.combo_likelyhood_go if a != 0]
                self.combo_likelyhood_nogo = [a for a in self.combo_likelyhood_nogo if a != 0]
                combo_likelyhood_go = reduce(lambda x,y: x*y, self.combo_likelyhood_go)
                combo_likelyhood_nogo = reduce(lambda x,y: x*y, self.combo_likelyhood_nogo)
                pp_go = self.prior_go[index]*combo_likelyhood_go
                self.list_pp_go.append(pp_go)
                pp_nogo = self.prior_nogo[index]*combo_likelyhood_nogo
                self.list_pp_nogo.append(pp_nogo)
            self.pp_set.append([self.list_pp_go,self.list_pp_nogo])
        # with open(path + '/template_set_ugo.csv', 'a') as result:
        #     writter = csv.writer(result, delimiter='\t')
        #     for item in self.feature_template_transpose:
        #         writter.writerow(item)


    def calc_prediction(self):
        for group in self.pp_set:
            go_minus_nogo = [a-b for a, b in zip(group[0],group[1])]
            prediction = list(map(lambda x: 1 if x>0 else 0, go_minus_nogo))
            self.list_prediction.append(prediction)


    def calc_accuracy(self):
        for index, group in enumerate(self.list_prediction):
            predict = group
            truth = self.test_truth[index]
            same = list(filter(lambda x: x==0, [a-b for a, b in zip(predict,truth)]))
            length_same = len(same)
            accuracy = length_same/(self.rows_test*1.0)
            self.list_accruacy.append(accuracy)





    def sequence(self):
        """
        the running sequence
        :return:
        """
        self.count_unique_country()
        self.count_rows()
        self.calc_prior_prob()
        self.calc_likelyhood()
        self.calc_feature_template()
        self.calc_truth_test()
        self.calc_pp()
        self.calc_prediction()
        self.calc_accuracy()
        print self.list_accruacy
        #print self.likelyhood_set




if __name__ == '__main__':
    obj = BayesPrediction()
    obj.sequence()