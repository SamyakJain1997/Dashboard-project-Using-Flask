from flask import Flask, render_template,flash, redirect, url_for, request, jsonify, make_response, Markup, session, redirect, url_for, Response, g
from flask_restful import Resource, Api
from flask import send_file
import pandas as pd
from sqlalchemy import create_engine
import time,io,os,json
from passlib.hash import sha256_crypt
from datetime import timedelta
from flask import Flask
from flask import render_template
import app_helper as ah
from werkzeug.utils import secure_filename
from application import application
from database_update_script import *

try:
    db_connection_str = 'mysql+pymysql://aisplcdb:Aisplcdb_987@157.245.99.230'
    db_connection = create_engine(db_connection_str)
    print("connection established")
except:
    print("Error")

UPLOAD_FOLDER = './static/upload'
app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def queryBuilder(database, tableName, word, columnName):
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if word == "noword" and columnName == "nocolumn":
        string = f'select * from {database}.{tableName}'
        paramDict = dict()
    else:
        if len(word) != 0:
            session[columnName] = word

        else:
            if (session.get(columnName)):
                session.pop(columnName, None)

        string = f'select * from {database}.{tableName} Where'
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        string = string + ' ' + "`"+key.strip()+"`" + " IS NULL"
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                    else:
                        string = string + ' ' + "`"+key.strip()+"`" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                else:
                    string = ""
        else:
            string = ""
    session['user'] = usersession
    return string, paramDict


def customQueryBuilderCentralDB(database, tableName, word, columnName, condition):
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if word == "noword" and columnName == "nocolumn":
        string = f'select * from aisplcdb.aispl_unique_customers'
        paramDict = dict()
    else:
        if len(word) != 0:
            session[columnName] = word

        else:
            if (session.get(columnName)):
                session.pop(columnName, None)

        string = f'select * from aisplcdb.aispl_unique_customers Where'
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        string = string + ' ' + "`"+key.strip()+"`" + " IS NULL"
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                    else:
                        string = string + ' ' + "`"+key.strip()+"`" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                else:
                    string = f'select * from aisplcdb.aispl_unique_customers'
        else:
            string = f'select * from aisplcdb.aispl_unique_customers'
    session['user'] = usersession
    return string, paramDict


def customQueryBuilderUniqueDB(database, tableName, word, columnName, condition,valuecheck):
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if word == "noword" and columnName == "nocolumn":
        string = f'SELECT * FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck});'
        paramDict = dict()
    else:
        if len(word) != 0:
            session[columnName] = word

        else:
            if (session.get(columnName)):
                session.pop(columnName, None)

        string = f'SELECT * FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck}) AND '
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        string = string + ' ' + "`"+key.strip()+"`" + " IS NULL"
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                    else:
                        string = string + ' ' + "`"+key.strip()+"`" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                else:
                    string = f'SELECT * FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck});'
        else:
            string = f'SELECT * FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck});'
    session['user'] = usersession
    return string, paramDict


def customQueryBuilderSourceDB(database, tableName, word, columnName, condition,valuecheck, tablecheck):
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if word == "noword" and columnName == "nocolumn":
        if tablecheck == "oneaispl_portal_customers":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE customer_tenant_id = "{valuecheck}";'
        elif tablecheck == "crm_customer":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE id = "{valuecheck}";'
        elif tablecheck == "tally_data_db":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
        elif tablecheck == "aispl_sales_db":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
        elif tablecheck == "aispl_ms_sales":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE end_customer_organization_id = "{valuecheck}";'
        elif tablecheck == "adobe_cdb":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
        paramDict = dict()
    else:
        if len(word) != 0:
            session[columnName] = word

        else:
            if (session.get(columnName)):
                session.pop(columnName, None)

        if tablecheck == "oneaispl_portal_customers":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE customer_tenant_id = "{valuecheck}" AND'
        elif tablecheck == "crm_customer":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE id = "{valuecheck}" AND'
        elif tablecheck == "tally_data_db":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}" AND'
        elif tablecheck == "aispl_sales_db":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}" AND'
        elif tablecheck == "aispl_ms_sales":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE end_customer_organization_id = "{valuecheck}" AND'
        elif tablecheck == "adobe_cdb":
            string = f'SELECT * FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}" AND'
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        string = string + ' ' + "`"+key.strip()+"`" + " IS NULL"
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                    else:
                        string = string + ' ' + "`"+key.strip()+"`" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND "
                        count += 1
                else:
                    string = ""
        else:
            string = ""
    session['user'] = usersession
    return string, paramDict



def customQueryBuilder(database, tableName, word, columnName, condition):
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    # if(word):
    if word == "noword" and columnName == "nocolumn":
        string = f"SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP '{condition}')"
        paramDict = dict()
    else:
        if len(word) != 0:
            session[columnName] = word

        else:
            if (session.get(columnName)):
                session.pop(columnName, None)

        string = f"SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP '{condition}') AND ("
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        string = string + key.strip()+" " + ")" + "IS NULL "
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND ( "
                        count += 1
                    else:
                        string = string + key.strip()+" " + ")" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND ( "
                        count += 1
                else:
                    string = ""
        else:
            string = ""
    session['user'] = usersession
    return string, paramDict

def customQueryBuilderAdobe(database, tableName, word, columnName, condition,year1,year2):
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    # if(word):
    if word == "noword" and columnName == "nocolumn":
        string = f"SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}')"
        paramDict = dict()
    else:
        if len(word) != 0:
            session[columnName] = word

        else:
            if (session.get(columnName)):
                session.pop(columnName, None)

        string = f"SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}') AND ("
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        string = string + key.strip()+" " + ")" + "IS NULL "
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND ( "
                        count += 1
                    else:
                        string = string + key.strip()+" " + ")" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            string = string + "AND ( "
                        count += 1
                else:
                    string = f"SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}')"
        else:
            string = f"SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}')"
    session['user'] = usersession
    return string, paramDict


def lazy(query, shape, param="none"):
    if param != "none":
        df1 = pd.read_sql(query, con=db_connection, params=param)
    else:
        df1 = pd.read_sql(query, con=db_connection)

    if (len(df1)):

        value = df1.to_html(header=False, index=False)  # time Eater
        value = value.replace('<table border="1" class="dataframe">', '')
        value = value.replace('</table>', '')
        value = value.replace('</tbody>', '')
        value = value.replace('<tbody>', '')

        for i in range(df1.shape[0]):
            value = value.replace(
                '<tr>', f'<tr id ="{i+shape}" onclick="myValue(this)"><td class="index">'+str(i+shape)+'</td>', 1)
    else:
        value = "<p class='noEntry'><p>"

    return value


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        olmsid = request.form['username'].lower()
        connection = db_connection.connect()
        user_details = connection.execute(
            "SELECT * FROM aisplcdb_ui.users WHERE user_id= %s", (olmsid)).fetchone()
        if (user_details):
            if (request.form['password'] == user_details[2]):
                # if sha256_crypt.verify(request.form['password'], df1[5]):
                # connection.execute("UPDATE aisplcdb_ui.users SET visit = %s WHERE olmid= %s", (str(int(df1[6])+ 1),olmsid))
                session['user'] = olmsid
                session.permanent = True
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', message="Incorrect Password")
        else:
            return render_template('login.html', message="Incorrect Username")
    return render_template('login.html',message="")


@app.route('/home')
def home():
    if g.user:
        return render_template('root.html')

    return redirect(url_for('index'))


# adobe api

@app.route("/adobecustcount", methods=['GET', 'POST'])
def adobecustcount():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_cust_count(resp_data)
    return _resp


@app.route("/adobetopstate", methods=['GET', 'POST'])
def adobetopstate():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_top_state(resp_data)
    return _resp


@app.route("/adobediffcust", methods=['GET', 'POST'])
def adobediffcust():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_diff_cust(resp_data)
    return _resp


@app.route("/adobedetailstable", methods=['GET', 'POST'])
def adobedetailstable():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_details_table(resp_data)
    return _resp


@app.route("/adobeexpiryyear", methods=['GET', 'POST'])
def adobeexpiryyear():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_expiry_year(resp_data)
    return _resp


@app.route("/adobeproductgroup", methods=['GET', 'POST'])
def adobeproductgroup():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_product_group(resp_data)
    return _resp


@app.route("/adobedistinctcust", methods=['GET', 'POST'])
def adobedistinctcust():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_distinct_cust(resp_data)
    return _resp


@app.route("/adobecitycount", methods=['GET', 'POST'])
def adobecitycount():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_city_count(resp_data)
    return _resp


@app.route("/adobecustdetailstable", methods=['GET', 'POST'])
def adobecustdetailstable():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.adobe_cust_details_table(resp_data)
    return _resp


# ms api

@app.route("/msdetailstable", methods=['GET', 'POST'])
def msdetailstable():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.ms_details_table(resp_data)
    return _resp


@app.route("/mssalescount", methods=['GET', 'POST'])
def mssalescount():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.ms_sales_count(resp_data)
    return _resp


@app.route("/mssalesgraph", methods=['GET', 'POST'])
def mssalesgraph():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.ms_sales_graph(resp_data)
    return _resp


@app.route("/mspurchasetype", methods=['GET', 'POST'])
def mspurchasetype():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.ms_purchase_type(resp_data)
    return _resp


@app.route("/msproductdist", methods=['GET', 'POST'])
def msproductdist():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.ms_product_dist(resp_data)
    return _resp


@app.route("/msyearwisecount", methods=['GET', 'POST'])
def msyearwisecount():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.ms_yearwise_count(resp_data)
    return _resp


# sales api

@app.route("/salessalescount", methods=['GET', 'POST'])
def salessalescount():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.sales_sales_count(resp_data)
    return _resp


@app.route("/salessalesgraph", methods=['GET', 'POST'])
def salessalesgraph():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.sales_sales_graph(resp_data)
    return _resp


@app.route("/salesordertype", methods=['GET', 'POST'])
def salesordertype():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.sales_order_type(resp_data)
    return _resp


@app.route("/salesproductdist", methods=['GET', 'POST'])
def salesproductdist():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.sales_product_dist(resp_data)
    return _resp


@app.route("/salestypecount", methods=['GET', 'POST'])
def salestypecount():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.sales_type_count(resp_data)
    return _resp


@app.route("/user_details", methods=['GET', 'POST'])
def user_details():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.user_details(resp_data)
    return _resp


# central DB API

@app.route("/central_db_count", methods=['GET', 'POST'])
def central_db_count():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.central_db_count(resp_data)
    return _resp


@app.route("/central_db_product_sales", methods=['GET', 'POST'])
def central_db_product_sales():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.central_db_product_sales(resp_data)
    return _resp


@app.route("/central_db_vendor_sales", methods=['GET', 'POST'])
def central_db_vendor_sales():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.central_db_vendor_sales(resp_data)
    return _resp


@app.route("/central_db_oem_sales", methods=['GET', 'POST'])
def central_db_oem_sales():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.central_db_oem_sales(resp_data)
    return _resp


@app.route("/central_db_gst_count", methods=['GET', 'POST'])
def central_db_gst_count():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.central_db_gst_count(resp_data)
    return _resp

@app.route("/unique_cust_count", methods=['GET', 'POST'])
def unique_cust_count():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.unique_cust_count(resp_data)
    return _resp
@app.route("/unique_cust_address", methods=['GET', 'POST'])
def unique_cust_address():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.unique_cust_address(resp_data)
    return _resp
@app.route("/unique_cust_city", methods=['GET', 'POST'])
def unique_cust_city():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.unique_cust_city(resp_data)
    return _resp
@app.route("/unique_cust_spoc", methods=['GET', 'POST'])
def unique_cust_spoc():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.unique_cust_spoc(resp_data)
    return _resp
@app.route("/unique_cust_email", methods=['GET', 'POST'])
def unique_cust_email():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.unique_cust_email(resp_data)
    return _resp
@app.route("/unique_cust_phone", methods=['GET', 'POST'])
def unique_cust_phone():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.unique_cust_phone(resp_data)
    return _resp

@app.route("/central_db__account_manager", methods=['GET', 'POST'])
def central_db__account_manager():
    if request.args:
        mainData = request.args.get("c")
    resp_data = mainData.split(",")
    _resp = ah.central_db__account_manager(resp_data)
    return _resp


# links
@app.route("/userdescription")
def doughnut():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('update.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))
@app.route("/userUpdateForm")
def userUpdateForm():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('userUpdate.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('dashboard.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))
@app.route('/adminPanel', methods=['GET', 'POST'])
def adminPanel():
    if g.user:
        sql_query = request.form.get("code_name")
        if sql_query == '':
            sql_query = "Please Type query"
        else:
            sql_query = sql_query
        sql_query = "Click on the Card Above to type Query"
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('adminPanel.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))

@app.route('/accountmanagercentraldb', methods=['GET', 'POST'])
def accountmanagercentraldb():
    if g.user:
        sql_query = request.form.get("code_name")
        if sql_query == '':
            sql_query = "Please Type query"
        else:
            sql_query = sql_query
        sql_query = "Click on the Card Above to type Query"
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('accountmanagercentraldb.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/uniqueCustDB', methods=['GET', 'POST'])
def uniqueCustDB():
    if g.user:
        return render_template('uniqueCustDB.html')
    return redirect(url_for('index'))


@app.route('/centralCustDB', methods=['GET', 'POST'])
def centralCustDB():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('centralCustDB.html', final_list3=final_list3)
    return redirect(url_for('index'))

@app.route('/sourceDB', methods=['GET', 'POST'])
def sourceDB():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('sourceDB.html', final_list3=final_list3)
    return redirect(url_for('index'))

@app.route('/unique_cust', methods=['GET', 'POST'])
def unique_cust():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('unique_cust.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))

@app.route('/adobeyearcompare', methods=['GET', 'POST'])
def adobeyearcompare():
    if g.user:
        # sql_query = request.form.get("code_name")
        year1 = request.form.get("year1")
        year2 = request.form.get("year2")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('adobeyearcompare.html', final_list3=final_list3,year1=year1,year2=year2)
    return redirect(url_for('index'))

@app.route('/adobeyearlist', methods=['GET', 'POST'])
def adobeyearlist():
    if g.user:
        if request.args:
            mainData = request.args.get("c")
            data = mainData.split(",")
            counter = int(data[4])
            year1 = data[6]
            year2 = data[7]
            data = mainData.split(",")
            database = data[0]
            table = data[1]
            column = data[2]
            word = data[3]
            condition = data[5]
            counter = int(data[4])
            query, params = customQueryBuilderAdobe(
            database, table, word, column, condition,year1,year2)
            if query:
                res = make_response(
                    jsonify(lazy(query+' limit '+str(counter)+',35;', counter, params)), 200)
            return res
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('adobeyearlist.html', final_list3=final_list3)
    return redirect(url_for('index'))

@app.route('/dashboardMs', methods=['GET', 'POST'])
def dashboardMs():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('dashboardMs.html', final_list3=final_list3)
    return redirect(url_for('index'))


@app.route('/dashboardsales', methods=['GET', 'POST'])
def dashboardsales():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('dashboardsales.html', final_list3=final_list3)
    return redirect(url_for('index'))


@app.route('/dashboardCentralDB', methods=['GET', 'POST'])
def dashboardCentralDB():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('dashboardCentralDB.html', final_list3=final_list3)
    return redirect(url_for('index'))


@app.route('/dashboard2', methods=['GET', 'POST'])
def dashboard2():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('dashboard_2.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/userUpdate', methods=['GET', 'POST'])
def userUpdate():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        if request.method == 'POST':
            if request.form['submit_button'] == 'Update User':
                user_id = request.form['username']
                name = request.form['name']
                department = request.form['department']
                email_id = request.form['email_id']
                password = request.form['password']
                user_type = request.form['user_type']
                contact_no = request.form['contact_no']
                connection = db_connection.connect()
                dfdf = connection.execute(
                    "SELECT * FROM aisplcdb_ui.users WHERE user_id= %s", (user_id)).fetchone()
                query = f"UPDATE aisplcdb_ui.users SET name = '{name}', password = '{password}', email_id = '{email_id}', contact_no = '{contact_no}', department = '{department}', user_type = '{user_type}' WHERE user_id = '{user_id}';"
                if (not dfdf):
                    return render_template('userUpdate.html', message="User Not Found", final_list3=final_list3)
                else:
                    connection.execute(query)
                    return render_template('update.html', message="User Updated", final_list3=final_list3)
            elif request.form['submit_button'] == 'Add User':
                user_id = request.form['username']
                name = request.form['name']
                department = request.form['department']
                email_id = request.form['email_id']
                password = request.form['password']
                user_type = request.form['user_type']
                contact_no = request.form['contact_no']
                connection = db_connection.connect()
                df1 = connection.execute(
                    "SELECT * FROM aisplcdb_ui.users WHERE user_id= %s", (user_id)).fetchone()
                if (not df1):
                    connection.execute("INSERT INTO aisplcdb_ui.users (user_id,name,password,email_id,contact_no,department,user_type) VALUES(%s,%s,%s,%s,%s,%s,%s);", (
                        user_id, name, password, email_id, contact_no, department, user_type))
                    return render_template('update.html', message="User Created", final_list3=final_list3)
                else:
                    return render_template('userUpdate.html', message="User Already Exists", final_list3=final_list3)
            elif request.form['submit_button'] == 'Delete User':
                user_id = request.form['username']
                connection = db_connection.connect()
                dfdf = connection.execute(
                    "SELECT * FROM aisplcdb_ui.users WHERE user_id= %s", (user_id)).fetchone()
                query = f'DELETE from aisplcdb_ui.users WHERE user_id = "{user_id}"'
                if (not dfdf):
                    return render_template('userUpdate.html', message="User Not Found", final_list3=final_list3)
                else:
                    connection.execute(query)
                    return render_template('update.html', message="User Deleted", final_list3=final_list3)
    return redirect(url_for('userUpdateForm'))
    # return render_template('update.html')


@app.route('/dashboard3', methods=['GET', 'POST'])
def dashboard3():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('dashboard_3.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/salesdbcusttable', methods=['GET', 'POST'])
def salesdbcusttable():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('salesdbcusttable.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/adobeclptable', methods=['GET', 'POST'])
def adobeclptable():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('adobe_clp_table.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/adobeflptable', methods=['GET', 'POST'])
def adobeflptable():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('adobe_flp_table.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/adobetlptable', methods=['GET', 'POST'])
def adobetlptable():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('adobe_tlp_table.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))


@app.route('/adobetviptable', methods=['GET', 'POST'])
def adobeviptable():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('adobe_vip_table.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))

@app.route('/centralDBTable', methods=['GET', 'POST'])
def centralDBTable():
    if g.user:
        sql_query = request.form.get("code_name")
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        return render_template('central_db_table.html', final_list3=final_list3, sql_query=sql_query)
    return redirect(url_for('index'))
@app.route('/fileupload', methods=['GET', 'POST'])
def fileupload():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        # return render_template('fileupload.html', final_list3=final_list3)
        return render_template('fileupload.html', final_list3=final_list3, data = ah.getfilenames(app.config['UPLOAD_FOLDER']))
    return redirect(url_for('index'))

# user links


@app.route('/database')
def database():
    usersession = session['user']
    session.clear()
    if request.args:
        databaseName = request.args.get("c")
    tableNames = pd.read_sql('show tables in '+databaseName, con=db_connection)
    tableNamesList = tableNames.to_json()
    res = make_response(tableNamesList, 200)
    session['user'] = usersession
    return res
@app.route('/custom_tableHeaders_adobe')
def custom_tableHeaders_adobe():
    usersession = session['user']
    session.clear()
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    condition = data[5]
    headers = pd.read_sql('SELECT * FROM aisplcdb_dev.aispl_adobe_distinct limit 0,1;', con=db_connection)
    headers1 = list(headers.columns)
    res = make_response(json.dumps(headers1), 200)
    session['user'] = usersession
    return res

@app.route('/custom_tableHeaders_source')
def custom_tableHeaders_source():
    usersession = session['user']
    session.clear()
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    condition = data[5]
    # valuecheck = data[6]
    tablecheck = data[7]
    if condition =="sourceDB":
        headers = pd.read_sql(f'SELECT * FROM aisplcdb.{tablecheck} limit 0,1;', con=db_connection)
    headers1 = list(headers.columns)
    res = make_response(json.dumps(headers1), 200)
    session['user'] = usersession
    return res


@app.route('/custom_tableHeaders')
def custom_tableHeaders():
    usersession = session['user']
    session.clear()
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    condition = data[5]
    # valuecheck = data[6]
    if condition == "Expiry":
        headers = pd.read_sql('select current_anniversary_date, program_type, product_name,deploy_to_email, end_user_id from ' +
                              database+'.'+table+' limit 0,1;', con=db_connection)
    elif condition =="AdobeYearCompare":
        headers = pd.read_sql('SELECT * FROM aisplcdb_dev.aispl_adobe_distinct limit 0,1;', con=db_connection)
    elif condition =="unique_central":
        headers = pd.read_sql('SELECT * FROM aisplcdb.aispl_central_database limit 0,1;', con=db_connection)
    elif condition =="CentralDB":
        headers = pd.read_sql('SELECT * FROM aisplcdb.aispl_unique_customers limit 0,1;', con=db_connection)
    else:
        headers = pd.read_sql(
            'select * from aisplcdb_dev.aispl_adobe_distinct limit 0,1;', con=db_connection)
    headers1 = list(headers.columns)
    res = make_response(json.dumps(headers1), 200)
    session['user'] = usersession
    return res


@app.route('/tableHeaders')
def tableHeaders():
    usersession = session['user']
    session.clear()
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    headers = pd.read_sql('select * from '+database+'.' +
                          table+' limit 0,1;', con=db_connection)
    headers1 = list(headers.columns)
    res = make_response(json.dumps(headers1), 200)
    session['user'] = usersession
    return res


@app.route("/custom_load")
def custom_load():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    print(data)
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    if condition == "Expiry":
        query = "SELECT current_anniversary_date, program_type, product_name,deploy_to_email, end_user_id from aisplcdb.adobe_cdb WHERE current_anniversary_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 15 DAY) ORDER BY current_anniversary_date "
        params = {}
    elif condition == "CentralDB":
        query, params = customQueryBuilderCentralDB(
            database, table, word, column, condition)
    else:
        query, params = customQueryBuilder(
            database, table, word, column, condition)
    if query:
        res = make_response(
            jsonify(lazy(query+' limit '+str(counter)+',35;', counter, params)), 200)
            
    else:
        res = make_response(jsonify(lazy(
            f"select * from {database}.{table} "+' limit '+str(counter)+',35;', counter)), 200)
    return res

@app.route("/custom_load_unique")
def custom_load_unique():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    valuecheck = str(data[6:])
    valuecheck = valuecheck.replace("[" , "")
    valuecheck = valuecheck.replace("]" , "")
    print("sssssssssssssssssssssss")
    print(len(valuecheck))
    print("sssssssssssssssssssssss")
    query,params = customQueryBuilderUniqueDB(database, table, word, column, condition,valuecheck)
    if query:
        res = make_response(
            jsonify(lazy(query, counter, params)), 200)
    return res

@app.route("/custom_load_source")
def custom_load_source():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    print(data)
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    valuecheck = data[6]
    tablecheck = data[7]
    query,params = customQueryBuilderSourceDB(database, table, word, column, condition,valuecheck,tablecheck)
    if query:
        res = make_response(
            jsonify(lazy(query, counter, params)), 200)
            
    else:
        res = make_response(jsonify(lazy(
            f"select * from {database}.{table} ", counter)), 200)
    return res


@app.route("/load")
def load():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    counter = int(data[4])
    query, params = queryBuilder(database, table, word, column)
    if query:
        res = make_response(
            jsonify(lazy(query+' limit '+str(counter)+',35;', counter, params)), 200)
    else:
        res = make_response(jsonify(lazy(
            f"select * from {database}.{table} "+' limit '+str(counter)+',35;', counter)), 200)
    return res

@app.route('/custom_downloadFile')
def custom_downloadFile():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    condition = data[5]
    if condition == "VIP":
        query = "SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP 'VIP')"
        params = {}
    elif condition == "TLP":
        query = "SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP 'TLP')"
        params = {}
    elif condition == "CLP":
        query = "SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP 'CLP')"
        params = {}
    elif condition == "FLP":
        query = "SELECT * FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP 'FLP')"
        params = {}
    elif condition == "Expiry":
        query = "SELECT current_anniversary_date, program_type, product_name,deploy_to_email, end_user_id from aisplcdb.adobe_cdb WHERE current_anniversary_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 15 DAY) ORDER BY current_anniversary_date "
        params = {}
    startTime = time.time()
    if (not query):
        query = f"select * from {database}.{table};"
    if params != "none":
        df1 = pd.read_sql(query, con=db_connection, params=params)
    else:
        df1 = pd.read_sql(query, con=db_connection)
    caldf = df1.to_csv(index=False, header=True)
    buf_str = io.StringIO(caldf)
    return send_file(io.BytesIO(buf_str.read().encode("utf-8")), mimetype="text/csv", download_name="data.csv")


@app.route('/downloadFile')
def downloadFile():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    query, params = queryBuilder(database, table, word, column)
    startTime = time.time()
    if (not query):
        query = f"select * from {database}.{table};"
    if params != "none":
        df1 = pd.read_sql(query, con=db_connection, params=params)
    else:
        df1 = pd.read_sql(query, con=db_connection)
    caldf = df1.to_csv(index=False, header=True)
    buf_str = io.StringIO(caldf)
    return send_file(io.BytesIO(buf_str.read().encode("utf-8")), mimetype="text/csv", download_name="data.csv")

@app.route('/custom_tableInfo_adobe')
def custom_tableInfo_adobe():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    year1 = data[6]
    year2 = data[7]
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if condition == "AdobeYearCompare":
        if word == "noword" and column == "nocolumn":
            query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}')"
            paramDict = dict()
        else:
            if len(word) != 0:
                session[column] = word

            else:
                if (session.get(column)):
                    session.pop(column, None)

            query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}') AND ("
            count = 0
            listOfKeys = session.keys()
            if (len(listOfKeys) > 0):
                for key, value in session.items():
                    if (value):
                        if value == "None":
                            query = query + key.strip()+" " + ")" + "IS NULL "
                            paramDict["word"+str(count)] = ""
                            if count != (len(listOfKeys) - 1):
                                query = query + "AND ( "
                            count += 1
                        else:
                            query = query + key.strip()+" " + ")" + " LIKE %(word"+str(count)+")s "
                            paramDict["word"+str(count)] = "%"+value+"%"
                            if count != (len(listOfKeys) - 1):
                                query = query + "AND ( "
                            count += 1
                    else:
                        query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}')"
            else:
                query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (subscription_end_year REGEXP '{year1}') AND (subscription_end_year REGEXP '{year2}')"
    if query:
        df3 = pd.read_sql(query, con=db_connection, params=paramDict)
        rows = df3.at[0, 'COUNT(*)']
    res = str(f"{rows}")
    session['user'] = usersession
    return res

@app.route('/custom_tableInfo_source')
def custom_tableInfo_source():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    valuecheck = data[6]
    tablecheck = data[7]
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if word == "noword" and column == "nocolumn":
        if tablecheck == "oneaispl_portal_customers":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE customer_tenant_id = "{valuecheck}";'
        elif tablecheck == "crm_customer":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE id = "{valuecheck}";'
        elif tablecheck == "tally_data_db":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
        elif tablecheck == "aispl_sales_db":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
        elif tablecheck == "aispl_ms_sales":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE end_customer_organization_id = "{valuecheck}";'
        elif tablecheck == "adobe_cdb":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
        paramDict = dict()
    else:
        if len(word) != 0:
            session[column] = word

        else:
            if (session.get(column)):
                session.pop(column, None)

        if tablecheck == "oneaispl_portal_customers":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE customer_tenant_id = "{valuecheck}" AND'
        elif tablecheck == "crm_customer":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE id = "{valuecheck}" AND'
        elif tablecheck == "tally_data_db":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}" AND'
        elif tablecheck == "aispl_sales_db":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}" AND'
        elif tablecheck == "aispl_ms_sales":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE end_customer_organization_id = "{valuecheck}" AND'
        elif tablecheck == "adobe_cdb":
            query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}" AND'
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        query = query + key.strip()+" " + ")" + "IS NULL "
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            query = query + "AND ( "
                        count += 1
                    else:
                        query = query + key.strip()+" " + ")" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            query = query + "AND ( "
                        count += 1
                else:
                    if tablecheck == "oneaispl_portal_customers":
                        query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE customer_tenant_id = "{valuecheck}";'
                    elif tablecheck == "crm_customer":
                        query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE id = "{valuecheck}";'
                    elif tablecheck == "tally_data_db":
                        query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
                    elif tablecheck == "aispl_sales_db":
                        query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
                    elif tablecheck == "aispl_ms_sales":
                        query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE end_customer_organization_id = "{valuecheck}";'
                    elif tablecheck == "adobe_cdb":
                        query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
        else:
            if tablecheck == "oneaispl_portal_customers":
                query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE customer_tenant_id = "{valuecheck}";'
            elif tablecheck == "crm_customer":
                query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE id = "{valuecheck}";'
            elif tablecheck == "tally_data_db":
                query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
            elif tablecheck == "aispl_sales_db":
                query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
            elif tablecheck == "aispl_ms_sales":
                query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE end_customer_organization_id = "{valuecheck}";'
            elif tablecheck == "adobe_cdb":
                query = f'SELECT COUNT(*) FROM aisplcdb.{tablecheck} WHERE aispl_id = "{valuecheck}";'
    if query:
        df3 = pd.read_sql(query, con=db_connection, params=paramDict)
        rows = df3.at[0, 'COUNT(*)']
    res = str(f"{rows}")
    session['user'] = usersession
    return res

@app.route('/custom_tableInfo_unique')
def custom_tableInfo_unique():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    valuecheck = str(data[6:])
    valuecheck = valuecheck.replace("[" , "")
    valuecheck = valuecheck.replace("]" , "")
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if condition == "unique_central":
        if word == "noword" and column == "nocolumn":
            query = f'SELECT COUNT(*) FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck})'
            paramDict = dict()
        else:
            if len(word) != 0:
                session[column] = word

            else:
                if (session.get(column)):
                    session.pop(column, None)

            query = f'SELECT COUNT(*) FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck}) AND ('
            count = 0
            listOfKeys = session.keys()
            if (len(listOfKeys) > 0):
                for key, value in session.items():
                    if (value):
                        if value == "None":
                            query = query + key.strip()+" " + ")" + "IS NULL "
                            paramDict["word"+str(count)] = ""
                            if count != (len(listOfKeys) - 1):
                                query = query + "AND ( "
                            count += 1
                        else:
                            query = query + key.strip()+" " + ")" + " LIKE %(word"+str(count)+")s "
                            paramDict["word"+str(count)] = "%"+value+"%"
                            if count != (len(listOfKeys) - 1):
                                query = query + "AND ( "
                            count += 1
                    else:
                        query = f'SELECT COUNT(*) FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck})'
            else:
                query = f'SELECT COUNT(*) FROM aisplcdb.aispl_central_database WHERE ref_id in ({valuecheck})'
    if query:
        df3 = pd.read_sql(query, con=db_connection, params=paramDict)
        rows = df3.at[0, 'COUNT(*)']
    res = str(f"{rows}")
    session['user'] = usersession
    return res


@app.route('/custom_tableInfo')
def custom_tableInfo():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if condition == "Expiry":
        query = f"SELECT COUNT(*) from aisplcdb.adobe_cdb WHERE current_anniversary_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 15 DAY)"
        paramDict = dict()
    elif condition == "CentralDB":
        if word == "noword" and column == "nocolumn":
            query = f'select COUNT(*) from aisplcdb.aispl_unique_customers'
            paramDict = dict()
        else:
            if len(word) != 0:
                session[column] = word

            else:
                if (session.get(column)):
                    session.pop(column, None)

            query = f'select COUNT(*) from aisplcdb.aispl_unique_customers Where'
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        query = query + ' ' + "`"+key.strip()+"`" + " IS NULL"
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            query = query + "AND "
                        count += 1
                    else:
                        query = query + ' ' + "`"+key.strip()+"`" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            query = query + "AND "
                        count += 1
                else:
                    query = f'select COUNT(*) from aisplcdb.aispl_unique_customers'
        else:
            query = f'select COUNT(*) from aisplcdb.aispl_unique_customers'
    else:
        if word == "noword" and column == "nocolumn":
            query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP '{condition}')"
            paramDict = dict()
        else:
            if len(word) != 0:
                session[column] = word

            else:
                if (session.get(column)):
                    session.pop(column, None)

            query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP '{condition}') AND ("
            count = 0
            listOfKeys = session.keys()
            if (len(listOfKeys) > 0):
                for key, value in session.items():
                    if (value):
                        if value == "None":
                            query = query + key.strip()+" " + ")" + "IS NULL "
                            paramDict["word"+str(count)] = ""
                            if count != (len(listOfKeys) - 1):
                                query = query + "AND ( "
                            count += 1
                        else:
                            query = query + key.strip()+" " + ")" + " LIKE %(word"+str(count)+")s "
                            paramDict["word"+str(count)] = "%"+value+"%"
                            if count != (len(listOfKeys) - 1):
                                query = query + "AND ( "
                            count += 1
                    else:
                        query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP '{condition}')"
            else:
                query = f"SELECT COUNT(*) FROM aisplcdb_dev.aispl_adobe_distinct WHERE (program_type REGEXP '{condition}')"
    if query:
        df3 = pd.read_sql(query, con=db_connection, params=paramDict)
        rows = df3.at[0, 'COUNT(*)']
    res = str(f"{rows}")
    session['user'] = usersession
    return res


@app.route('/tableInfo')
def tableInfo():
    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    table = data[1]
    column = data[2]
    word = data[3]
    condition = data[5]
    counter = int(data[4])
    usersession = session['user']
    session.pop('user', None)
    paramDict = dict()
    if word == "noword" and column == "nocolumn":
        query = f'select COUNT(*) from {database}.{table}'
        paramDict = dict()
    else:
        if len(word) != 0:
            session[column] = word

        else:
            if (session.get(column)):
                session.pop(column, None)

        query = f'select COUNT(*) from {database}.{table} Where'
        count = 0
        listOfKeys = session.keys()
        if (len(listOfKeys) > 0):
            for key, value in session.items():
                if (value):
                    if value == "None":
                        query = query + ' ' + "`"+key.strip()+"`" + " IS NULL"
                        paramDict["word"+str(count)] = ""
                        if count != (len(listOfKeys) - 1):
                            query = query + "AND "
                        count += 1
                    else:
                        query = query + ' ' + "`"+key.strip()+"`" + " LIKE %(word"+str(count)+")s "
                        paramDict["word"+str(count)] = "%"+value+"%"
                        if count != (len(listOfKeys) - 1):
                            query = query + "AND "
                        count += 1
                else:
                    query = f'select COUNT(*) from {database}.{table}'
        else:
            query = f'select COUNT(*) from {database}.{table}'
    if query:
        df3 = pd.read_sql(query, con=db_connection, params=paramDict)
        rows = df3.at[0, 'COUNT(*)']
    res = str(f"{rows}")
    session['user'] = usersession
    return res


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/adduser', methods=['GET', 'POST'])
def register():
    if g.user:
        user_type = f"SELECT user_type FROM aisplcdb_ui.users WHERE user_id ='{g.user}';"
        df3 = pd.read_sql(user_type, con=db_connection)
        json_data3 = json.dumps(json.loads(df3.to_json(orient="records")))
        final_list3 = json_data3
        if request.method == 'POST':
            if request.form['submit_button'] == 'Add User':
                user_id = request.form['username']
                name = request.form['name']
                department = request.form['department']
                email_id = request.form['email_id']
                password = request.form['password']
                user_type = request.form['user_type']
                contact_no = request.form['contact_no']
                connection = db_connection.connect()
                df1 = connection.execute(
                    "SELECT * FROM aisplcdb_ui.users WHERE user_id= %s", (user_id)).fetchone()
                if (not df1):
                    connection.execute("INSERT INTO aisplcdb_ui.users (user_id,name,password,email_id,contact_no,department,user_type) VALUES(%s,%s,%s,%s,%s,%s,%s);", (
                        user_id, name, password, email_id, contact_no, department, user_type))
                    return render_template('update.html', message="User Created", final_list3=final_list3)
                else:
                    return render_template('userUpdate.html', message="User Already Exists", final_list3=final_list3)
            elif request.form['submit_button'] == 'Delete User':
                user_id = request.form['username']
                connection = db_connection.connect()
                dfdf = connection.execute(
                    "SELECT * FROM aisplcdb_ui.users WHERE user_id= %s", (user_id)).fetchone()
                query = f'DELETE from aisplcdb_ui.users WHERE user_id = "{user_id}"'
                if (not dfdf):
                    return render_template('userUpdate.html', message="User Not Found", final_list3=final_list3)
                else:
                    connection.execute(query)
                    return render_template('update.html', message="User Deleted", final_list3=final_list3)
    return redirect(url_for('userUpdateForm'))
    # return render_template('update.html')



ALLOWED_EXTENSIONS = set(['xlsx', 'csv'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadfile', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return render_template('fileupload.html', data = ah.getfilenames(app.config['UPLOAD_FOLDER']))
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return render_template('fileupload.html', data = ah.getfilenames(app.config['UPLOAD_FOLDER']))
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded', "success")
			return render_template('fileupload.html', data = ah.getfilenames(app.config['UPLOAD_FOLDER']))
		else:
			flash('Allowed file types are xlsx/csv only!')
			return render_template('fileupload.html', data = ah.getfilenames(app.config['UPLOAD_FOLDER']))


# @app.route('/',methods=['POST'])

@app.route('/dataupdatetodb',methods=['POST'])
def dataupdatetodb():

    if request.args:
        mainData = request.args.get("c")
    data = mainData.split(",")
    database = data[0]
    filename = data[1]
    tablename = data[2]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if tablename=="adobe_cdb":
        resp_ = update_adobe_data_to_sql(file_path,database,tablename)
    if b"successfully" in resp_:
        flash("Data Updated sucessfully successfully.")
    else:
        flash(f"Error occured !! {resp_}")

    return redirect('/adminPanel')

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('index'))


class fetch(Resource):
    def get(self, database, table):
        df = pd.read_sql(
            f"select * from {database}.{table}", con=db_connection)
        return df.to_json(orient='split')


api.add_resource(fetch, '/fetch/<database>/<table>')

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True,
            host='0.0.0.0', port=8080, threaded=True)