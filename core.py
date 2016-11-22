import sys
import statistics
import math
'''TODO
2. PERCENTILE
'''

class Dataframe:
    df = [] #entire csv file
    columns = []    #names of the coloumns in csv
    num_of_rows = 0
    data = []   #actuall content in the csv

    def read_csv(self,file_name,first_row_header=True):
        #open file
        self.csv_file = open(file_name,"r").read()

        #split csv by lines
        csv = self.csv_file.split('\n')
        for sect in csv:
            #split and append element into list
            sect = sect.split(",")
            self.df.append(sect)

        #
        if first_row_header == True:
            self.columns = self.df[0]

        #clean data
        self.data_prep()

    def write_csv(self,name):
        #open csv
        self.csv_file = open(name,"w")

        #make str to write into csv
        str_to_write = ""
        #make str to right by looping through df
        for line in self.df:
            for char in line:
                str_to_write += char + ","
            str_to_write += "\n"

        #write to csv
        self.csv_file.write(str_to_write)

    #clean data
    def data_prep(self):
        self.num_of_rows = len(self.df) - 1
        self.data = self.df[1:-1]

    #show dataframe
    def display(self):
        #string to display init
        str_to_display = ""
        #make str by looping through dataframe
        for line in self.df:
            for char in line:
                str_to_display += "\t"+ str(char)
            str_to_display += "\n"

        #show data frame
        print(str_to_display)

    def data_by_row(self, row_num):
        #data to return is nth row in dataframe
        data_to_return = self.df[row_num]

        #return row
        return data_to_return

    def data_by_column(self, column_name):
        #init array to return
        data_to_return = []

        #find column number
        #init var to loop with
        self.index = 0
        for self.col in self.columns:
            # if column is found, break
            if column_name == self.col:
                break
            #if not, add and loop
            self.index += 1

        #for row each row
        for row in self.df:
            #if row is column, just keep looping
            if row == self.columns:
                continue

            #if row is blank, because its last, break
            if row == ['']:
                break

            #append data to returning array
            data_to_return.append(row[self.index])

        #return data ignoring columns
        return data_to_return[:] #ICHANGED THIS AYBE PROBLEM HELP PLSPLSPLS

    def fill_blanks(self,filler="NULL"):
        #init row counter
        self.row_count = 0
        for self.row in self.df:
            #init row counter
            self.char_count = 0

            #if df is at end, ignore rest
            if self.row == ['']:
                continue

            #loop through elements in row
            for self.char in self.row:
                #if the element is blank
                if len(self.char) == 0:
                    #set blank to user's filler
                    self.df[self.row_count][self.char_count] = filler

                #add to char counter
                self.char_count += 1

            #add to row counter
            self.row_count += 1

        #clean dataframe
        self.data_prep()

    def find_replace(self, find, replace):
        #init row cunter
        self.row_count = 0

        # start looping through
        for self.row in self.df:
            #init element count
            self.char_count = 0

            #if row is blank, ignore
            if self.row == ['']:
                continue

            #loop through element in character
            for self.char in self.row:
                if self.char == find:
                    self.df[self.row_count][self.char_count] = replace

                #up char count
                self.char_count += 1
            #up row count
            self.row_count += 1

        #clean df
        self.data_prep()

    def find_replace_conditional(self, conditions, find, replace):
        #replace column names with index in column list
        #new and used dict for looping
        self.perf_conditions = {}
        #for iters in dict
        for self.key in conditions:
            #find id for col name
            col_id = self.query_column_names(self.key)
            #add id and value to dict to be used
            self.perf_conditions[col_id] = conditions[self.key]

        #init row counter
        self.row_count = 0

        # start looping through
        for self.row in self.df:
            #init element count
            self.char_count = 0

            #if row is blank, ignore
            if self.row == ['']:
                continue
            #loop through element in character
            for self.char in self.row:
                #if char is found in element
                if self.char == find:
                    self.conds_met = True
                    #for equality conditions to be mean
                    for self.key in self.perf_conditions:
                        #if condition is not met
                        if self.row[self.key] != self.perf_conditions[self.key]:
                            #don't bother continuing to search
                            #mark as conditions not met
                            self.conds_met = False
                            break

                    #if conditions are still meant
                    if self.conds_met == True:
                        #replace value with replacer
                        self.df[self.row_count][self.char_count] = replace

                #up char count
                self.char_count += 1
            #up row count
            self.row_count += 1

        #clean df
        self.data_prep()

    def query_column_names(self,query_name):
        col_num = 0
        found = False
        for col in self.columns:
            if col == query_name:
                found = True
                return col_num
            col_num += 1
        if found == False:
            sys.exit()
            print("No Column Name As Such")

    def rename_column(self, dict_col_name_change):
        #define column indexer
        col_index = 0
        #for old columns in columns in df
        for column in self.columns:
            #loo[ though col in users requested columns
            for old_column in dict_col_name_change:
                #if too col are the same
                if old_column == column:
                    #set that column to the uesrs requested column name
                    self.columns[col_index] = dict_col_name_change[old_column]

    def mean(self, exclude=[]):
        #gets data by column **

        data_avgs = {}
        for column in self.columns:


            #get the data in the column
            col_data = self.data_by_column(column)
            #make data floats
            try:
                #convert data to floats; exclude ones user doesn't want
                data_to_mean = [ float(position) for position in col_data if col_data.index(position) not in exclude ]
                #average the data
                data_mean = statistics.mean(data_to_mean)
                #add avg to list of avg
                data_avgs[column] = data_mean

            except TypeError:
                data_avgs[column] = "Data String, Skipped On Averaging Data"

            except ValueError:
                data_avgs[column] = "Data String, Skipped On Averaging Data"

        #give dict with avg by column_name
        return data_avgs

    def median(self, exclude=[]):
        #gets data by column **

        data_meds = {}
        for column in self.columns:
            #get the data in the column
            col_data = self.data_by_column(column)

            #make data floats
            try:
                #convert data to floats; exclude ones user doesn't want
                data_to_median = [ float(position) for position in col_data if col_data.index(position) not in exclude ]
                #median the data
                data_median = statistics.median(data_to_median)
                #add median to list of median
                data_meds[column] = data_median

            except TypeError:
                data_meds[column] = "Data String, Skipped On Medianing Data"

            except ValueError:
                data_meds[column] = "Data String, Skipped On Medianing Data"

        #give dict with avg by column_name
        return data_meds

    def range(self, exclude=[]):
        #gets data by column **

        data_range = {}
        for column in self.columns:
            #get the data in the column
            col_data = self.data_by_column(column)

            #make data floats
            try:
                #convert data to floats; exclude ones user doesn't want
                data_to_range = [ float(position) for position in col_data if col_data.index(position) not in exclude ]
                #range the data
                data_output_range = max(data_to_range) - min(data_to_range)
                #add avg to list of avg
                data_range[column] = data_output_range

            except TypeError:
                data_range[column] = "Data String, Skipped On Ranging Data"

            except ValueError:
                data_range[column] = "Data String, Skipped On Rangin Data"

        #give dict with avg by column_name
        return data_range

    def mode(self, exclude=[]):
        # gets data by column **

        data_mode = {}
        for column in self.columns:
            # get the data in the column
            col_data = self.data_by_column(column)

            # make data floats
            try:
                #convert data to floats; exclude ones user doesn't want
                data_to_mode = [ float(position) for position in col_data if col_data.index(position) not in exclude ]
                # average the data
                data_out_mode = statistics.mode(data_to_mode)
                # add avg to list of avg
                data_mode[column] = data_out_mode

            except TypeError:
                data_mode[column] = "Data String, Skipped On Moding Data"

            except statistics.StatisticsError:
                data_mode[column] = "No Mode"

            except ValueError:
                data_mode[column] = "Data String, Skipped On Moding Data"


        # give dict with mode by column_name
        return data_mode

    def std_dev(self, exclude=[]):
        # gets data by column **

        data_std_dev = {}
        for column in self.columns:
            # get the data in the column
            col_data = self.data_by_column(column)

            # make data floats
            try:
                #convert data to floats; exclude ones user doesn't want
                data_to_std_dev = [ float(position) for position in col_data if col_data.index(position) not in exclude ]
                # find master avg of data
                datas_avg = statistics.mean(data_to_std_dev)

                deviations = []
                #conduct deviating calculating
                for element in data_to_std_dev:
                    calc_deviation = (element - datas_avg) ** 2
                    deviations.append(calc_deviation)

                #find standard deviation true value
                cols_std_dev = math.sqrt(statistics.mean(deviations))

                # add std_dev to list of avg
                data_std_dev[column] = cols_std_dev

            except TypeError:
                data_std_dev[column] = "Data String, Skipped On Standard Deviation -ing Data"

            except ValueError:
                data_std_dev[column] = "Data String, Skipped On Standard Deviation -ing Data"



        # give dict with std_dev by column_name
        return data_std_dev

    def pct_change(self, exclude=[], base="FIRST"):
        # gets data by column **

        data_pct_change = {}
        for column in self.columns:
            # get the data in the column
            col_data = self.data_by_column(column)
            col_pct_changes = []

            # make data floats
            try:
                #convert data to floats; exclude ones user doesn't want
                data_to_pct_change = [ float(position) for position in col_data if col_data.index(position) not in exclude ]
                #get base value
                obsv_base = data_to_pct_change[0] if base == "FIRST" else max(data_to_pct_change) if base == "MAX" else min(data_to_pct_change)

                #compute pct_change over the vals
                for element in data_to_pct_change:
                    try:
                        ele_pct_change = (element - obsv_base) / obsv_base

                    except ZeroDivisionError:
                        ele_pct_change = "Div:0:Error"
                    col_pct_changes.append(ele_pct_change)

                data_pct_change[column] = col_pct_changes



            except TypeError:
                data_pct_change[column] = "Data String, Skipped On Standard Deviation -ing Data"

            except ValueError:
                data_pct_change[column] = "Data String, Skipped On Standard Deviation -ing Data"



        # give dict with std_dev by column_name
        return data_pct_change

    def sum(self, exclude=[]):
        #gets data by column **

        data_sum = {}
        for column in self.columns:
            #get the data in the column
            col_data = self.data_by_column(column)

            #make data floats
            try:#convert data to floats; exclude ones user doesn't want
                data_to_sum = [ float(position) for position in col_data if col_data.index(position) not in exclude ]
                #sum the data
                data_output_sum = sum(data_to_sum)
                #add avg to list of avg
                data_sum[column] = data_output_sum

            except TypeError:
                data_sum[column] = "Data String, Skipped On Ranging Data"

            except ValueError:
                data_sum[column] = "Data String, Skipped On Rangin Data"

        #give dict with avg by column_name
        return data_sum

    def rolling_avg(self, push, exclude=[]):
        # gets data by column **

        data_rolled_avg = {}
        for column in self.columns:
            # get the data in the column
            col_data = self.data_by_column(column)

            # make data floats
            try:
                # convert data to floats; exclude ones user doesn't want
                data_ = [float(position) for position in col_data if
                                        col_data.index(position) not in exclude]
                # find master avg of data
                datas_avg = statistics.mean(data_[:push])
                data_to_comp = data_[push:]

                deviations = ["DevFrom" for _ in range(push)]
                #conduct deviating calculating
                for element in data_to_comp:
                    calc_deviation = (element - datas_avg) / datas_avg
                    deviations.append(calc_deviation)


                # add std_dev to list of avg
                data_rolled_avg[column] = deviations

            except ZeroDivisionError:
                data_rolled_avg[column] = "Div:0:Error"

            except ValueError:
                data_rolled_avg[column] = "Data String, Skipped On Rolling Average -ing Data"
                
        return data_rolled_avg

    def export_numpy_array(self, np, exclude=[], split=None):
        # gets data by column **

        np_data = {}
        for column in self.columns:
            # get the data in the column
            col_data = self.data_by_column(column)

            # make data floats
            try:
                # convert data to floats; exclude ones user doesn't want
                np_to_array = [float(position) for position in col_data if
                         col_data.index(position) not in exclude]

                #if their is a split, split it
                if split:
                    first_array = np_to_array[:split+1]
                    sec_array = np_to_array[split+1:]

                    np_data[column] = [np.array(first_array).astype(np.float), np.array(sec_array).astype(np.float)]

                else:
                    np_data[column] = np.array(first_array).astype(np.float)


            except ZeroDivisionError:
                np_data[column] = "Div:0:Error"

            except ValueError:
                np_data[column] = "Data String, Skipped On Rolling Average -ing Data"

        return np_data

