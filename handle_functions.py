import pandas as pd
import math

def table_sort(filename):
    df = pd.read_excel(f"./data/{filename}.xlsx")
    # print(df)

    # Tried to chang nan to None, to no avail
    df = df.where(pd.notnull(df), None)
    # print(df)

    first_col = list(df.columns)[0]
    # print(list(df.columns)[0])

    df = df.sort_values(first_col)
    # print(df)

    df.to_excel(f"./data/{filename}.xlsx", index=False)
    return df.reset_index(drop=True)

# table_sort('testdsave')

def header_val(df):
    headers = list(df.columns)
    # print(headers)
    return headers

def row_values(filename):
    df = pd.read_excel(f"./data/{filename}.xlsx")
    rows = df.values
    # print(rows)
    return rows

# row_values('testdelisite')

testlist = {'DRIVER_NO': ['20'],  'IC_NO': [''], 'LORRY_NO': [''], 'COMISSION': [''], 'BASIC': [''], 'ROAD_TAX': [''], 'INSPECTION': ['']}
testlist2 = {}
def add(add_list, filename):
    df = pd.read_excel(f"./data/{filename}.xlsx")

    # Convert val to string then uppercase, back into dict
    add_list = { key: [str(val[0]).upper()] for key, val in add_list.items()}
    # print("New: ", add_list)

    to_add_df = pd.DataFrame(add_list)
    add_first_col = list(to_add_df.columns)[0]
    to_add_val = str(to_add_df[add_first_col].values[0]).upper()

    print(to_add_df)
    print("Added: ", to_add_val)

    first_col = list(df.columns)[0]
    # print(first_col)
    ori_col = df[first_col]

    frames = [df, to_add_df]

    # Check if first_col: DRIVER_NO/DELISITE etc unique
    if df[ori_col == to_add_val].empty:
        print(f"Unique entry, adding new {first_col}: {to_add_val}...")
        data = pd.concat(frames)
        data.to_excel(f"./data/{filename}.xlsx", index=False)
        print("Data saved")
        table_sort(filename)
        flag = True
    else:
        print(f"Duplicated entry, {first_col}: {to_add_val} already exists")
        data = df
        flag = False

    print("Data&Flag: ", [data, flag])
    return [data, flag]

# add(testlist2, 'testdsave')
# header_val(table_sort("testdriver"))

testa = {'entry': ["1", "3", "4"]}
def delete_entry(del_list, filename):
    df = pd.read_excel(f"./data/{filename}.xlsx")

    if del_list != {}:
        # Delete tables based on index, which starts from 0
        new_list = [int(i) - 1 for i in del_list['entry']]
        # print(new_list)

        data = df.drop(new_list)
        # print(data)
        data.to_excel(f"./data/{filename}.xlsx", index=False)
        flag = True
    else:
        data = df
        flag = False

    return [data, flag]

def get_entry(get_list, filename):
    df = pd.read_excel(f"./data/{filename}.xlsx")

    if get_list != {}:
        index_list = [int(get_list['radio_entry'][0]) - 1]
        # print(index_list)

        # Replace nan with empty str
        specific_row = df.iloc[index_list[0]]
        specific_row = specific_row.where(pd.notnull(specific_row), '')
        # print("Row: ", specific_row)

        # Row to dict
        row_dict = specific_row.to_dict()
        # print(row_dict)
        return [row_dict, index_list[0]]
    else:
        return [{}, -1]

# get_entry({'radio_entry': ['2']}, 'DRIVER')

# editedit = {'DRIVER_NO': 'A00', 'NAME': "ENGSUNAI E'PRISE  QKA5183", 'IC_NO': '690728135989', 'LORRY_NO': 'QKA5183', 'COMISSION': nan, 'BASIC': nan, 'ROAD_TAX': nan, 'INSPECTION': nan}
def edit(edit_list, filename, row_index):
    df = pd.read_excel(f"./data/{filename}.xlsx")

    new_list = { key: str(val[0]).upper() for key, val in edit_list.items() }

    print("new edit list: ", new_list)

    to_edit_df = pd.DataFrame([new_list])
    edit_first_col = list(to_edit_df.columns)[0]
    # print(to_edit_df)

    first_col = list(df.columns)[0]
    # print(first_col)

    ori_list_1 = df.loc[row_index].to_dict()
    print("ori1 row: ", ori_list_1)
    ori_list = { key: [str(val).upper().replace('NAN','')] for key, val in ori_list_1.items() }
    print("ori row: ", ori_list)

    print("before: ", df.at[row_index, first_col])
    print("editdf", to_edit_df.at[0, edit_first_col])

    # Check if first_col: DRIVER_NO/DELISITE etc is same
    if df.at[row_index, first_col] == to_edit_df.at[0, edit_first_col]:
        # Replace ori row with edit row
        print("same first col")
        df.loc[row_index] = new_list
        print("after replace: ", df.loc[row_index])
        df.to_excel(f"./data/{filename}.xlsx", index=False)
        print("Data saved")
        table_sort(filename)
        flag = 3
        return [df, flag]

    else:
        print("diff first col")

        # Delete ori_col, use add for validation, add ori_col back again
        data = df.drop(row_index)
        # print("DEleted:", data)
        data.to_excel(f"./data/{filename}.xlsx", index=False)

        # Check whole table first_col for dupe
        data = add(edit_list, filename)
        # print("Done add: ", data[0])
        new_dupe_flag = data[1]
        # print("New edit flag: ", new_dupe_flag)

        # 6 means editted, 7 means edit val dupe
        if new_dupe_flag:
            return_flag = 6
        else:
            return_flag = 7

        # if New value dupe, means deleted ori_val need to be added back
        if return_flag == 7:
            data = add(ori_list, filename)
            # print("Add ori: ", data[0])
            ori_dupe_flag = data[1]
            # print("Ori flag: ", ori_dupe_flag)

        sorted_df = table_sort(filename)
        print(sorted_df)

        return[sorted_df, return_flag]


# edit(editedit, 'DRIVER')

