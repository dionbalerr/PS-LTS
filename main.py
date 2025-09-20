from flask import Flask, render_template, request
import webview
import pandas as pd
import threading
from datetime import datetime
import handle_functions as table

app = Flask(__name__)


@app.context_processor
def inject_current_year():
    return {"year": datetime.now().year}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/maintenance")
def maint_menu():
    maint_menu_flag = True
    return render_template("home.html", maint_menu_flag=maint_menu_flag)


@app.route("/maintenance/<string:flag_check>")
def details_menu(flag_check):
    maint_menu_flag = True
    return render_template("home.html",
                           maint_menu_flag=maint_menu_flag,
                           flag_check=flag_check)


@app.route("/maintenance/<string:flag_check>/<int:num>")
def details_listing(num, flag_check):
    print(f"{num} clicked")
    print(f"{flag_check} clicked")

    filename = flag_check

    headers = table.header_val(table.table_sort(filename))
    # print(headers)
    rows = table.row_values(filename)

    # 1 for default table, 2 for del, 3 for edit
    if num == 1:
        return render_template("table.html",
                               headers=headers,
                               rows=rows,
                               flag_check=flag_check)
    elif num == 2:
        return render_template("del_table.html",
                               headers=headers,
                               rows=rows,
                               flag_check=flag_check)
    elif num == 3:
        return render_template("edit_table.html",
                               headers=headers,
                               rows=rows,
                               flag_check=flag_check)


@app.route("/maintenance/<string:flag_check>/data", methods=['POST'])
def handle_data(flag_check):
    data = dict(request.form.lists())
    print(data)

    if flag_check == 'DRIVER':
        driver_no = request.form.get('DRIVER_NO').upper()
        # print(driver_no)
    elif flag_check == 'DELISITE':
        site_no = request.form.get('SITE_NO').upper()
        # print(site_no)
    elif flag_check == 'SUPPLIER':
        supp_no = request.form.get('SUPPLIER_NO').upper()
        # print(supp_no)
    elif flag_check == 'CLIENT':
        client_no = request.form.get('CLIENT_NO').upper()
        # print(client_no)

    filename = flag_check

    new_table = table.add(data, filename)
    new_table_df = pd.DataFrame(new_table[0])

    print(new_table)
    print(new_table_df)
    print("Flag is: ", new_table[1])

    rows = new_table_df.values
    headers = table.header_val(table.table_sort(filename))
    # print(rows, headers)

    # 1 means NEW, 2 means DUPE
    if new_table[1]:
        modal_flag = 1
    else:
        modal_flag = 2
    # print(modal_flag)

    if flag_check == 'DRIVER':
        return render_template("table.html",
                               headers=headers,
                               rows=rows,
                               driver_no=driver_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)
    elif flag_check == 'DELISITE':
        return render_template("table.html",
                               headers=headers,
                               rows=rows,
                               site_no=site_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)
    elif flag_check == 'SUPPLIER':
        return render_template("table.html",
                               headers=headers,
                               rows=rows,
                               supp_no=supp_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)
    elif flag_check == 'CLIENT':
        return render_template("table.html",
                               headers=headers,
                               rows=rows,
                               client_no=client_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)


@app.route("/maintenance/<string:flag_check>/delete", methods=['POST'])
def delete_data(flag_check):
    data = dict(request.form.lists())
    # print(data)

    if data != {}:
        no_entry = len(data['entry'])
    else:
        no_entry = ""
    # print("Length:", no_entry)

    filename = flag_check

    new_table = table.delete_entry(data, filename)
    new_table_df = pd.DataFrame(new_table[0])
    # print(new_table_df)

    rows = new_table_df.values
    headers = table.header_val(table.table_sort(filename))

    # 3 means success, 4 means failed(no entry selected
    if new_table[1]:
        modal_flag = 3
    else:
        modal_flag = 4
    print(modal_flag)

    return render_template("table.html",
                               headers=headers,
                               rows=rows,
                               flag_check=flag_check,
                               modal_flag=modal_flag,
                               no_entry=no_entry)


@app.route("/maintenance/<string:flag_check>/get", methods=['POST'])
def get_data(flag_check):
    # Gets index of row, searches in get_entry
    data = dict(request.form.lists())
    # print(data)

    filename = flag_check
    row_value = table.get_entry(data, filename)

    current_row = row_value[0]
    print(current_row)

    row_index = row_value[1]
    print("index: ", row_index)

    headers = table.header_val(table.table_sort(filename))
    # print(headers)
    rows = table.row_values(filename)

    modal_flag = 5
    return render_template("edit_table.html",
                               headers=headers,
                               rows=rows,
                               flag_check=flag_check,
                               modal_flag=modal_flag,
                               current_row=current_row,
                               row_index=row_index)


@app.route("/maintenance/<string:flag_check>/edit/<int:row_index>", methods=['POST'])
def edit_data(flag_check, row_index):
    data = dict(request.form.lists())

    if flag_check == 'DRIVER':
        driver_no = request.form.get('DRIVER_NO').upper()
        # print(driver_no)
    elif flag_check == 'DELISITE':
        site_no = request.form.get('SITE_NO').upper()
        # print(site_no)
    elif flag_check == 'SUPPLIER':
        supp_no = request.form.get('SUPPLIER_NO').upper()
        # print(supp_no)
    elif flag_check == 'CLIENT':
        client_no = request.form.get('CLIENT_NO').upper()
        # print(client_no)

    filename = flag_check

    new_table = table.edit(data, filename, row_index)
    print(new_table)

    new_table_df = pd.DataFrame(new_table[0])
    print(new_table_df)
    print("Flag is: ", new_table[1])

    rows = new_table_df.values
    headers = table.header_val(table.table_sort(filename))
    # print(rows, headers)

    # 6 means EDITED, 7 means EDIT_ DUPE
    if new_table[1] == 6:
        modal_flag = 6
    elif new_table[1] == 7:
        modal_flag = 7

    print("mflag: ", modal_flag)

    if flag_check == 'DRIVER':
        return render_template("edit_table.html",
                               headers=headers,
                               rows=rows,
                               driver_no=driver_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)
    elif flag_check == 'DELISITE':
        return render_template("edit_table.html",
                               headers=headers,
                               rows=rows,
                               site_no=site_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)
    elif flag_check == 'SUPPLIER':
        return render_template("edit_table.html",
                               headers=headers,
                               rows=rows,
                               supp_no=supp_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)
    elif flag_check == 'CLIENT':
        return render_template("edit_table.html",
                               headers=headers,
                               rows=rows,
                               client_no=client_no,
                               flag_check=flag_check,
                               modal_flag=modal_flag)


def start_server():
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    new_thread = threading.Thread(target=start_server)
    new_thread.daemon = True
    new_thread.start()

    webview.create_window("PS LTS", "http://127.0.0.1:5000")
    webview.start()
