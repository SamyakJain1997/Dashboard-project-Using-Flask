import pandas as pd
from sqlalchemy import create_engine
import json
import os

try:
    db_connection_str = 'mysql+pymysql://aisplcdb:Aisplcdb_987@157.245.99.230'
    db_connection = create_engine(db_connection_str)
    print("connection established")
except:
    print("Error")

def get_data(query_list):
    resp_list = []
    print(query_list)
    for query_data in query_list:
        d = {}
        df = pd.read_sql(query_data[1], con=db_connection )
        df_dict = df.to_dict(orient="records")
        for k in df_dict[0].keys():
            d[k] = tuple(d[k] for d in df_dict) 
        resp_list.append({query_data[0]:d})
    return resp_list



def user_details(resp_data):
    query = [("full_name","SELECT user_id,name, password,contact_no, email_id,department,user_type from aisplcdb_ui.users;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "check_data" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("full_name")
        user_id= data.get("user_id")
        name= data.get("name")
        contact_no= data.get("contact_no")
        password= data.get("password")
        email_id= data.get("email_id")
        department= data.get("department")
        usertype= data.get("user_type")
        resp = {"user_id":user_id,"name":name,"password":password,"email_id":email_id,"contact_no":contact_no,"department":department,"usertype":usertype}
    else :
        resp = {"resp":"code not found"}
    return resp



# adobe count

def adobe_cust_count(resp_data):
    query = [("total_cust","SELECT COUNT(aispl_id) FROM aisplcdb.adobe_cdb;"),
    ("vip_count","SELECT COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb WHERE program_type = 'VIP';"),
    ("flp_count","SELECT COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb WHERE program_type = 'FLP';"),
    ("tlp_count","SELECT COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb WHERE program_type = 'TLP';"),
    ("clp_count","SELECT COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb WHERE program_type = 'CLP';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "total_cust":
        data = data_dict.get("total_cust")
        legend = 'total_cust'
        labels = 'Total Customer Entry'
        values = data.get("COUNT(aispl_id)")
        resp = {"values":values,"labels":labels,"legend":legend}
    elif resp_data[0] == "vip_count" :
        data_dict = (get_data(query)[1])
        data= data_dict.get("vip_count")
        values = data.get("COUNT(DISTINCT aispl_id)")
        resp = {"values":values}
    elif resp_data[0] == "flp_count" :
        data_dict = (get_data(query)[2])
        data= data_dict.get("flp_count")
        values = data.get("COUNT(DISTINCT aispl_id)")
        resp = {"values":values}
    elif resp_data[0] == "tlp_count" :
        data_dict = (get_data(query)[3])
        data= data_dict.get("tlp_count")
        values = data.get("COUNT(DISTINCT aispl_id)")
        resp = {"values":values}
    elif resp_data[0] == "clp_count" :
        data_dict = (get_data(query)[4])
        data= data_dict.get("clp_count")
        values = data.get("COUNT(DISTINCT aispl_id)")
        resp = {"values":values}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_top_state(resp_data):
    query = [("deploy_to_state","SELECT deploy_to_state, COUNT(deploy_to_state) FROM aisplcdb.adobe_cdb GROUP BY deploy_to_state ORDER BY COUNT(deploy_to_state) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "deploy_to_state":
        data = data_dict.get("deploy_to_state")
        legend = 'deploy_to_state'
        labels = data.get("deploy_to_state")
        values = data.get("COUNT(deploy_to_state)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_diff_cust(resp_data):
    query = [("lisence_expiry","SELECT COUNT(current_anniversary_date) from aisplcdb.adobe_cdb WHERE current_anniversary_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 15 DAY);"),
    ("total_cust_dist","SELECT (SELECT COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb)-(SELECT COUNT(current_anniversary_date) from aisplcdb.adobe_cdb WHERE current_anniversary_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 15 DAY));"),
    ("total_lisence","SELECT COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "program_type" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data_dict2 = (get_data(query)[2])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        data2= data_dict2.get("total_lisence")
        labels= 'lisense expiry'
        values= data.get("COUNT(current_anniversary_date)"),data1.get("(SELECT COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb)-(SELECT COUNT(current_anniversary_date) from aisplcdb.adobe_cdb WHERE current_anniversary_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 15 DAY))"),data2.get("COUNT(DISTINCT aispl_id)")
        resp = {"values":values,"labels":labels}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_details_table(resp_data):
    query = [("current_anniversary_date","SELECT current_anniversary_date, program_type, product_name,deploy_to_email, end_user_id from aisplcdb.adobe_cdb WHERE current_anniversary_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 15 DAY) ORDER BY current_anniversary_date;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "current_anniversary_date" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("current_anniversary_date")
        date = data.get("current_anniversary_date")
        legend = data.get("product_name")
        labels = data.get("deploy_to_email")
        program= data.get("program_type")
        values = data.get("end_user_id")
        resp = {"values":values,"labels":labels,"legend":legend, "date":date, "program":program}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_expiry_year(resp_data):
    query = [("anniversary_date","SELECT COUNT(DISTINCT current_anniversary_date), YEAR(current_anniversary_date) FROM aisplcdb.adobe_cdb WHERE current_anniversary_date IS NOT NULL GROUP BY YEAR(current_anniversary_date) ORDER BY YEAR(current_anniversary_date) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "anniversary_date" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("anniversary_date")
        legend = 'current_anniversary_date'
        labels = data.get("YEAR(current_anniversary_date)")
        values = data.get("COUNT(DISTINCT current_anniversary_date)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_product_group(resp_data):
    query = [("product_name","SELECT product_name,COUNT(*) FROM aisplcdb.adobe_cdb GROUP BY product_name;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "product_name" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("product_name")
        legend = 'product_name'
        labels = data.get("product_name")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_distinct_cust(resp_data):
    query = [("program_type","SELECT program_type,COUNT(DISTINCT aispl_id) FROM aisplcdb.adobe_cdb GROUP BY program_type ORDER BY COUNT(DISTINCT aispl_id) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "program_type" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("program_type")
        legend = 'program_type'
        labels = data.get("program_type")
        values = data.get("COUNT(DISTINCT aispl_id)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_city_count(resp_data):
    query = [("deploy_to_city","SELECT deploy_to_city, COUNT(*) FROM aisplcdb.adobe_cdb GROUP BY deploy_to_city ORDER BY COUNT(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "deploy_to_city":
        data_dict = (get_data(query)[0])
        data = data_dict.get("deploy_to_city")
        legend = 'deploy_to_city'
        labels = data.get("deploy_to_city")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def adobe_cust_details_table(resp_data):
    query = [("vip_table","SELECT DISTINCT aispl_id, end_user_id,end_user_name,membership_number from aisplcdb.adobe_cdb WHERE program_type = 'VIP';"),
    ("flp_table","SELECT DISTINCT aispl_id, end_user_id,end_user_name,membership_number from aisplcdb.adobe_cdb WHERE program_type = 'FLP';"),
    ("tlp_table","SELECT DISTINCT aispl_id, end_user_id,end_user_name,membership_number from aisplcdb.adobe_cdb WHERE program_type = 'TLP';"),
    ("clp_table","SELECT DISTINCT aispl_id, end_user_id,end_user_name,membership_number from aisplcdb.adobe_cdb WHERE program_type = 'FLP';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "vip_table" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("vip_table")
        date = data.get("aispl_id")
        legend = data.get("end_user_id")
        labels = data.get("end_user_name")
        values = data.get("membership_number")
        resp = {"values":values,"labels":labels,"legend":legend, "date":date}
    elif resp_data[0] == "flp_table" :
        data_dict = (get_data(query)[1])
        data= data_dict.get("flp_table")
        date = data.get("aispl_id")
        legend = data.get("end_user_id")
        labels = data.get("end_user_name")
        values = data.get("membership_number")
        resp = {"values":values,"labels":labels,"legend":legend, "date":date}
    elif resp_data[0] == "tlp_table" :
        data_dict = (get_data(query)[2])
        data= data_dict.get("tlp_table")
        date = data.get("aispl_id")
        legend = data.get("end_user_id")
        labels = data.get("end_user_name")
        values = data.get("membership_number")
        resp = {"values":values,"labels":labels,"legend":legend, "date":date}
    elif resp_data[0] == "clp_table" :
        data_dict = (get_data(query)[3])
        data= data_dict.get("clp_table")
        date = data.get("aispl_id")
        legend = data.get("end_user_id")
        labels = data.get("end_user_name")
        values = data.get("membership_number")
        resp = {"values":values,"labels":labels,"legend":legend, "date":date}
    else :
        resp = {"resp":"code not found"}
    return resp


# Ms Details

def ms_sales_count(resp_data):
    query = [("total_ms_cust","SELECT COUNT(*) FROM aisplcdb.aispl_ms_sales;"),
    ("end_customer_organization_id","SELECT COUNT(DISTINCT end_customer_organization_id) FROM aisplcdb.aispl_ms_sales;"),
    ("from_reseller_top_parent_id","SELECT COUNT(DISTINCT from_reseller_top_parent_id) FROM aisplcdb.aispl_ms_sales;"),
    ("mpn_id","SELECT COUNT(DISTINCT mpn_id) FROM aisplcdb.aispl_ms_sales;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "total_ms_cust":
        data = data_dict.get("total_ms_cust")
        legend = 'total_ms_cust'
        labels = ''
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    elif resp_data[0] == "end_customer_organization_id" :
        data_dict = (get_data(query)[1])
        data= data_dict.get("end_customer_organization_id")
        values = data.get("COUNT(DISTINCT end_customer_organization_id)")
        resp = {"values":values}
    elif resp_data[0] == "from_reseller_top_parent_id" :
        data_dict = (get_data(query)[2])
        data= data_dict.get("from_reseller_top_parent_id")
        values = data.get("COUNT(DISTINCT from_reseller_top_parent_id)")
        resp = {"values":values}
    elif resp_data[0] == "mpn_id" :
        data_dict = (get_data(query)[3])
        data= data_dict.get("mpn_id")
        values = data.get("COUNT(DISTINCT mpn_id)")
        resp = {"values":values}
    else:
        resp = {"resp":"code not found"}
    return resp
def ms_sales_graph(resp_data):
    query = [("sales_date","SELECT COUNT(*), MONTH(sales_date)FROM aisplcdb.aispl_ms_sales WHERE sales_date IS NOT NULL GROUP BY MONTH(sales_date) ORDER BY MONTH(sales_date) ASC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "sales_date" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("sales_date")
        legend = 'sales_date'
        labels = data.get("MONTH(sales_date)")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def ms_purchase_type(resp_data):
    query = [("purchase_type","SELECT purchase_type,COUNT(*) FROM aisplcdb.aispl_ms_sales GROUP BY purchase_type;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "purchase_type" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("purchase_type")
        legend = 'purchase_type'
        labels = data.get("purchase_type")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def ms_product_dist(resp_data):
    query = [("reported_subsegment","SELECT COUNT(*), credited_region FROM aisplcdb.aispl_ms_sales GROUP BY credited_region;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "reported_subsegment" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("reported_subsegment")
        legend = 'reported_subsegment'
        labels = data.get("credited_region")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def ms_yearwise_count(resp_data):
    query = [("sales_date","SELECT COUNT(*), YEAR(sales_date) FROM aisplcdb.aispl_ms_sales GROUP BY YEAR(sales_date);")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "sales_date" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("sales_date")
        legend = 'sales_date'
        labels = data.get("YEAR(sales_date)")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp


# sales Details

def sales_sales_count(resp_data):
    query = [("total_sales_cust","SELECT COUNT(*) FROM aisplcdb.aispl_sales_db;"),
    ("end_customer_organization_id","SELECT COUNT(DISTINCT am) FROM aisplcdb.aispl_sales_db;"),
    ("from_reseller_top_parent_id","SELECT COUNT(DISTINCT oem) FROM aisplcdb.aispl_sales_db;"),
    ("mpn_id","SELECT COUNT(DISTINCT ordertype) FROM aisplcdb.aispl_sales_db;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "total_sales_cust":
        data = data_dict.get("total_sales_cust")
        legend = 'total_sales_cust'
        labels = ''
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    elif resp_data[0] == "end_customer_organization_id" :
        data_dict = (get_data(query)[1])
        data= data_dict.get("end_customer_organization_id")
        values = data.get("COUNT(DISTINCT am)")
        resp = {"values":values}
    elif resp_data[0] == "from_reseller_top_parent_id" :
        data_dict = (get_data(query)[2])
        data= data_dict.get("from_reseller_top_parent_id")
        values = data.get("COUNT(DISTINCT oem)")
        resp = {"values":values}
    elif resp_data[0] == "mpn_id" :
        data_dict = (get_data(query)[3])
        data= data_dict.get("mpn_id")
        values = data.get("COUNT(DISTINCT ordertype)")
        resp = {"values":values}
    else:
        resp = {"resp":"code not found"}
    return resp
def sales_sales_graph(resp_data):
    query = [("sales_date","SELECT COUNT(*), am FROM aisplcdb.aispl_sales_db WHERE am IS NOT NULL GROUP BY am ORDER BY COUNT(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "sales_date" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("sales_date")
        legend = 'sales_date'
        labels = data.get("am")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def sales_order_type(resp_data):
    query = [("purchase_type","SELECT ordertype , COUNT(*) FROM aisplcdb.aispl_sales_db GROUP BY ordertype;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "purchase_type" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("purchase_type")
        legend = 'purchase_type'
        labels = data.get("ordertype")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}

    else :
        resp = {"resp":"code not found"}
    return resp
def sales_product_dist(resp_data):
    query = [("reported_subsegment","SELECT COUNT(*), oem FROM aisplcdb.aispl_sales_db WHERE oem IS NOT NULL GROUP BY oem ORDER BY count(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "reported_subsegment" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("reported_subsegment")
        legend = 'reported_subsegment'
        labels = data.get("oem")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def sales_type_count(resp_data):
    query = [("sales_date","SELECT COUNT(*), vendor FROM aisplcdb.aispl_sales_db WHERE vendor IS NOT NULL GROUP BY vendor ORDER BY count(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "sales_date" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("sales_date")
        legend = 'sales_date'
        labels = data.get("vendor")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
    
# central DB

def central_db_count(resp_data):
    query = [("total_customer_name","SELECT count(aispl_cust_id) from aisplcdb.aispl_unique_customers WHERE ref_id IS NOT NULL;"),
    ("total_customer_city","SELECT count(DISTINCT customer_city) from aisplcdb.aispl_central_database WHERE customer_city IS NOT NULL;"),
    ("total_product_name","SELECT count(DISTINCT product_name) from aisplcdb.aispl_central_database WHERE product_name IS NOT NULL;"),
    ("total_data_entry","SELECT count(*) from aisplcdb.aispl_central_database;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "total_customer_name":
        data = data_dict.get("total_customer_name")
        legend = 'total_customer_name'
        labels = ''
        values = data.get("count(aispl_cust_id)")
        resp = {"values":values,"labels":labels,"legend":legend}
    elif resp_data[0] == "total_customer_city" :
        data_dict = (get_data(query)[1])
        data= data_dict.get("total_customer_city")
        values = data.get("count(DISTINCT customer_city)")
        resp = {"values":values}
    elif resp_data[0] == "total_product_name" :
        data_dict = (get_data(query)[2])
        data= data_dict.get("total_product_name")
        values = data.get("count(DISTINCT product_name)")
        resp = {"values":values}
    elif resp_data[0] == "total_data_entry" :
        data_dict = (get_data(query)[3])
        data= data_dict.get("total_data_entry")
        values = data.get("count(*)")
        resp = {"values":values}
    else:
        resp = {"resp":"code not found"}
    return resp
def central_db_product_sales(resp_data):
    query = [("product_sales","SELECT COUNT(*), product_name FROM aisplcdb.aispl_central_database WHERE product_name IS NOT NULL GROUP BY product_name ORDER BY COUNT(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "product_sales" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("product_sales")
        legend = 'product_sales'
        labels = data.get("product_name")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp
def central_db_vendor_sales(resp_data):
    query = [("vendor_sales","SELECT COUNT(*), vendor FROM aisplcdb.aispl_central_database WHERE vendor !='None' GROUP BY vendor ORDER BY COUNT(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "vendor_sales" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("vendor_sales")
        legend = 'purchase_type'
        labels = data.get("vendor")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}

    else :
        resp = {"resp":"code not found"}
    return resp
def central_db_oem_sales(resp_data):
    query = [("oem_sales","SELECT COUNT(*), oem FROM aisplcdb.aispl_central_database WHERE oem IS NOT NULL GROUP BY oem ORDER BY COUNT(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "oem_sales" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("oem_sales")
        legend = 'oem_sales'
        labels = data.get("oem")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp

def central_db__account_manager(resp_data):
    query = [("account_manager","SELECT COUNT(*), account_manager FROM aisplcdb.aispl_central_database WHERE account_manager IS NOT NULL GROUP BY account_manager ORDER BY COUNT(*) DESC;")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "account_manager" :
        data_dict = (get_data(query)[0])
        data= data_dict.get("account_manager")
        legend = 'account_manager'
        labels = data.get("account_manager")
        values = data.get("COUNT(*)")
        resp = {"values":values,"labels":labels,"legend":legend}
    else :
        resp = {"resp":"code not found"}
    return resp

def central_db_gst_count(resp_data):
    query = [("lisence_expiry","SELECT count(gstin) from aisplcdb.aispl_unique_customers  WHERE gstin != 'None';"),
    ("total_cust_dist","SELECT count(gstin) from aisplcdb.aispl_unique_customers  WHERE gstin = 'None';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "gstin_count" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        labels= ['GST NUMBER', 'NO GST NUMBER']
        values= data.get("count(gstin)"),data1.get("count(gstin)")
        resp = {"values":values,"labels":labels}
    else :
        resp = {"resp":"code not found"}
    return resp


# UNIQUE CUST COUNT
def unique_cust_count(resp_data):
    query = [("lisence_expiry","SELECT COUNT(customer_name) from aisplcdb.aispl_unique_customers WHERE customer_name = 'None';"),
    ("total_cust_dist","SELECT COUNT(customer_name) from aisplcdb.aispl_unique_customers WHERE customer_name != 'None';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "address_count" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        labels= ['customer name', 'NO customer name']
        values= data.get("COUNT(customer_name)"),data1.get("COUNT(customer_name)")
        resp = {"values":values,"labels":labels}
    else:
        resp = {"resp":"code not found"}
    return resp

def unique_cust_address(resp_data):
    query = [("lisence_expiry","SELECT COUNT(customer_address) from aisplcdb.aispl_unique_customers WHERE customer_address = 'None';"),
    ("total_cust_dist","SELECT COUNT(customer_address) from aisplcdb.aispl_unique_customers WHERE customer_address != 'None';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "address_count" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        labels= ['Cust address', 'NO Cust address']
        values= data.get("COUNT(customer_address)"),data1.get("COUNT(customer_address)")
        resp = {"values":values,"labels":labels}
    else :
        resp = {"resp":"code not found"}
    return resp

def unique_cust_city(resp_data):
    query = [("lisence_expiry","SELECT COUNT(customer_city) from aisplcdb.aispl_unique_customers WHERE customer_city = 'None';"),
    ("total_cust_dist","SELECT COUNT(customer_city) from aisplcdb.aispl_unique_customers WHERE customer_city != 'None';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "address_count" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        labels= ['customer_city', ' NO customer_city']
        values= data.get("COUNT(customer_city)"),data1.get("COUNT(customer_city)")
        resp = {"values":values,"labels":labels}
    else :
        resp = {"resp":"code not found"}
    return resp
def unique_cust_spoc(resp_data):
    query = [("lisence_expiry","SELECT COUNT(customer_spoc) from aisplcdb.aispl_unique_customers WHERE customer_spoc = 'None';"),
    ("total_cust_dist","SELECT COUNT(customer_spoc) from aisplcdb.aispl_unique_customers WHERE customer_spoc != 'None';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "address_count" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        labels= ['customer_spoc', 'No customer_spoc']
        values= data.get("COUNT(customer_spoc)"),data1.get("COUNT(customer_spoc)")
        resp = {"values":values,"labels":labels}
    else :
        resp = {"resp":"code not found"}
    return resp
def unique_cust_email(resp_data):
    query = [("lisence_expiry","SELECT COUNT(customer_email) from aisplcdb.aispl_unique_customers WHERE customer_email = 'None';"),
    ("total_cust_dist","SELECT COUNT(customer_email) from aisplcdb.aispl_unique_customers WHERE customer_email != 'None';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "address_count" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        labels= ['customer_email', 'No customer_email']
        values= data.get("COUNT(customer_email)"),data1.get("COUNT(customer_email)")
        resp = {"values":values,"labels":labels}
    else :
        resp = {"resp":"code not found"}
    return resp
def unique_cust_phone(resp_data):
    query = [("lisence_expiry","SELECT COUNT(customer_phone) from aisplcdb.aispl_unique_customers WHERE customer_phone = 'None';"),
    ("total_cust_dist","SELECT COUNT(customer_phone) from aisplcdb.aispl_unique_customers WHERE customer_phone != 'None';")]
    data_dict = (get_data(query)[0])
    if resp_data[0] == "address_count" :
        data_dict = (get_data(query)[0])
        data_dict1 = (get_data(query)[1])
        data= data_dict.get("lisence_expiry")
        data1= data_dict1.get("total_cust_dist")
        labels= ['customer_phone', 'No customer_phone']
        values= data.get("COUNT(customer_phone)"),data1.get("COUNT(customer_phone)")
        resp = {"values":values,"labels":labels}
    else :
        resp = {"resp":"code not found"}
    return resp

def getfilenames(path):
    dir_list = os.listdir(path)
    # print(dir_list)
    # resp = json.dumps(json.loads(dir_list.to_json(orient="records")))
    # resp = json.dumps(dir_list)
    # print("TOTAL FILES TO BE PROCESSED",len(dir_list))
    # print(len(dir_list))
    # resp = dir_list[1]
    return dir_list
    
 
def deletefile(path, filename):
    if os.path.exists(path+"/"+filename):
        os.remove(path+"/"+filename) # one file at a time
        return("success")
    else:
        return ("not found")

