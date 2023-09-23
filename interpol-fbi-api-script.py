import requests
import json
import pandas as pd
import pycountry
from datetime import datetime, date
from sqlalchemy import create_engine
import cx_Oracle   # pip install cx_Oracle

# Replace with your Oracle database connection details
USERNAME = "RM95511"
PASSWORD = "210696"
HOST = "oracle.fiap.com.br"
PORT = "1521"
SID = "ORCL"
TARGET_TABLE = 'FBI_INTERPOL_WANTED_CRIMINALS'

# Install Oracle Client https://www.oracle.com/database/technologies/instant-client/downloads.html
# Copy the address where the instant client was unzipped
lib_dir = r"C:\Users\cgodevs\Downloads\archived\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11"

# ------------------------------ UTILITIES --------------------------------
def remove_keys_from_dict(the_dict: dict, keys: list):
    for key in keys:
        if key in the_dict:
            del the_dict[key]

def format_date(date_str):
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return str(date_str)  # Return the original value as string if it's not a valid date    

def list_to_string(the_list):
    try:
        joined_string = '; '.join(the_list)
        return joined_string
    except:
        return the_list         

def walk_json_path(json_obj, *args):
    inner_value = json_obj
    for arg in args:
        try:
            current_value = inner_value.get(arg, '')
            if current_value == {}:
                break
            inner_value = inner_value.get(arg, '')
        except:
            return ''
    return inner_value           

def add_html_paragraph_tags(string):
    strings_with_tags = '<p>' + string + '</p>'
    return strings_with_tags

def get_country_name(country_id):  # 2 letters country code
    try:
        country_obj = pycountry.countries.get(alpha_2=country_id)
        if country_obj != None: 
            return country_obj.name
        return country_id
    except:
        print('An error happened! country_id is: ' + str(country_id))
        return country_id     

def transform_float_feet_height_to_cm_string(h):
    try:
        feet = int(h / 10)
        inches = int(h % 10)

        feet_cm = feet * 30.48
        inches_cm = inches * 2.54
        
        meters = float(feet_cm + inches_cm) / 100
        
        meters_str = f"{meters:.2f}"
        return meters_str
    except:
        return h   

def get_age_from_date_of_birth(date_string):
    date_format = "%B %d, %Y"
    try:
        date_then = datetime.strptime(date_string, date_format).date()
        current_date = date.today()
        age_in_years = str(int((current_date - date_then).days / 365.25)) + ' years old'  # Account for leap years
        return age_in_years
    except:
        return ''           

def SQL_CREATE_STATEMENT_FROM_DATAFRAME(source_df, target_table_name):
    only_text_data_type_df = source_df.astype(str)
    sql_text = pd.io.sql.get_schema(only_text_data_type_df, target_table_name)   
    oracle_clean_statement = sql_text.replace('\"', '').replace('TEXT', 'CLOB')
    return oracle_clean_statement

def SQL_INSERT_STATEMENT_FROM_DATAFRAME(source_df, target_table_name):
    sql_texts = []
    for index, row in source_df.iterrows():
        columns_str = ', '.join(source_df.columns)
        values_list = [str(value).replace("'", "''") if value is not None else 'NULL' for value in row.values]
        values_str = ', '.join([f"'{value}'" if value != 'NULL' else 'NULL' for value in values_list])
        insert_statement = f"INSERT INTO {target_table_name} ({columns_str}) VALUES ({values_str})"
        sql_texts.append(insert_statement)
    return sql_texts        
        
# --------------------------- CALL FBI API --------------------------------

# Create an empty DataFrame
fbi_wanted_df = pd.DataFrame()

page = 1
while True:
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
    data = json.loads(response.content)

    if data['total'] == 0 or data['items'] == []:
        print('No more data available')
        break

    response_items = data['items']

    # Ensure all keys are present in every dictionary
    all_keys = set().union(*(item.keys() for item in response_items))
    for item in response_items:
        for k in all_keys:
            item.setdefault(k, None)

    # Create a DataFrame
    df = pd.DataFrame(response_items, columns=all_keys)

    # Concatenate the DataFrame to the existing DataFrame
    fbi_wanted_df = pd.concat([fbi_wanted_df, df], axis=0, sort=True, ignore_index=True)
    page += 1
    if page == 199:     # Loop safety check
        print('Something\'s wrong, page iteration is at 199')
        break           

# --------------------------- CALL INTERPOL API --------------------------------

page = 1
resultPerPage = 160
#notices_iterated = 0

interpol_wanted_df = pd.DataFrame()
while True:
    response = requests.get('https://ws-public.interpol.int/notices/v1/red', params={'page': page, 'resultPerPage': resultPerPage})
    try:
        interpol_data = json.loads(response.content)
    except:
        break
    page += 1

    # Get all red notices
    red_notices = interpol_data['_embedded']['notices']

    # Get each red notice inner content
    for notice in red_notices:
        try:
            more_details_url = notice['_links']['self']['href']
            more_details_json = json.loads(requests.get(more_details_url, timeout=20).content) 

            # Handle images
            thumbnail_url = walk_json_path(notice, '_links', 'thumbnail', 'href') 
            images_url = walk_json_path(notice, '_links', 'images', 'href')
            try:
                larger_image_url = json.loads(requests.get(images_url).content)['_embedded']['images'][0]['_links']['self']['href']
                images_dict = {'thumb': thumbnail_url, 'large': larger_image_url}  # Set dict to match FBI response keys 
            except:
                images_dict = {}

            # Remove useless keys
            keys_to_remove_from_dict = ['_links', 'thumbnail', '_embedded']
            remove_keys_from_dict(notice, keys_to_remove_from_dict)
            remove_keys_from_dict(more_details_json, keys_to_remove_from_dict)

            full_notices_dict = {**notice, **more_details_json}  # Unpacking dicts into one
            full_notices_dict['images'] = str(images_dict)

            df =  pd.DataFrame([full_notices_dict])

            # Explode JSON columns
            arrest_warrants = pd.concat([pd.json_normalize(record) for record in df['arrest_warrants']], ignore_index=True)
            df = pd.concat([df.drop(columns='arrest_warrants'), arrest_warrants], axis=1)

            interpol_wanted_df = pd.concat([interpol_wanted_df, df], axis=0, sort=True, ignore_index=True)     
        except Exception as e:
            print('An exception happened. Skipping notice: ') 
            print(notice)
            print(e)
            continue

    if page == 99:   # Loop safety check
        print('Something\'s wrong, page index is 99 in code')
        break          


# -------------------- Transforming and uniting data from both sources ------------------------
interpol_wanted_df['wanted_origin'] = 'INTERPOL'
fbi_wanted_df['wanted_origin'] = 'FBI'    

fbi_wanted_df.rename(
    columns={
        'scars_and_marks':'distinguishing_marks',
        'caution':'charges',
        'eyes':'eyes_color',
        'hair':'hair_color'
    }, 
    inplace=True
)

interpol_wanted_df.rename(
    columns={
        'date_of_birth':'dates_of_birth_used',
        'charge': 'charges',
        'sex_id': 'sex',
        'country_of_birth_id': 'nationality',
        'eyes_colors_id':'eyes_color',
        'hairs_id':'hair_color',
        'languages_spoken_ids': 'languages'
    }, 
    inplace=True
)

interpol_wanted_df['dates_of_birth_used'] = pd.to_datetime(interpol_wanted_df['dates_of_birth_used'])
interpol_wanted_df['dates_of_birth_used'] = interpol_wanted_df['dates_of_birth_used'].apply(format_date)
interpol_wanted_df['age_range'] = interpol_wanted_df['dates_of_birth_used'].apply(get_age_from_date_of_birth)
fbi_wanted_df['dates_of_birth_used'] = fbi_wanted_df['dates_of_birth_used'].apply(list_to_string)

interpol_wanted_df['charges'] = interpol_wanted_df['charges'].apply(add_html_paragraph_tags)

fbi_wanted_df['aliases'] = fbi_wanted_df['aliases'].apply(list_to_string)
interpol_wanted_df['aliases'] = (interpol_wanted_df['forename'] + ' ' + interpol_wanted_df['name']).str.title()
interpol_wanted_df['forename'] = interpol_wanted_df['forename'].str.title()
interpol_wanted_df['name'] = interpol_wanted_df['name'].str.title()

sex_mapping = {'M': 'Male', 'F': 'Female'}
interpol_wanted_df['sex'] = interpol_wanted_df['sex'].map(sex_mapping)

interpol_wanted_df['eyes_color'] = interpol_wanted_df['eyes_color'].apply(list_to_string)
interpol_wanted_df['hair_color'] = interpol_wanted_df['hair_color'].apply(list_to_string)

fbi_wanted_df['height_max'] = fbi_wanted_df['height_max'].apply(transform_float_feet_height_to_cm_string)
fbi_wanted_df['height_min'] = fbi_wanted_df['height_min'].apply(transform_float_feet_height_to_cm_string)
fbi_wanted_df['height'] = fbi_wanted_df['height_min'] + ';' + fbi_wanted_df['height_max']

interpol_wanted_df['languages'] = interpol_wanted_df['languages'].apply(list_to_string)
fbi_wanted_df['languages'] = fbi_wanted_df['languages'].apply(list_to_string)

interpol_wanted_df['nationality'] = interpol_wanted_df['nationality'].apply(get_country_name)
interpol_wanted_df['issuing_country_id'] = interpol_wanted_df['issuing_country_id'].apply(get_country_name)
fbi_wanted_df['issuing_country_id'] = 'United States of America'

interpol_wanted_df['wanted_origin_id'] = interpol_wanted_df['entity_id']
fbi_wanted_df['wanted_origin_id'] = fbi_wanted_df['uid']

fbi_wanted_df['field_offices'] = fbi_wanted_df['field_offices'].apply(list_to_string)
fbi_wanted_df['occupations'] = fbi_wanted_df['occupations'].apply(list_to_string)
fbi_wanted_df['possible_countries'] = fbi_wanted_df['possible_countries'].apply(list_to_string)
fbi_wanted_df['possible_states'] = fbi_wanted_df['possible_states'].apply(list_to_string)
fbi_wanted_df['subjects'] = fbi_wanted_df['subjects'].apply(list_to_string)
interpol_wanted_df['images'] = interpol_wanted_df['images'].apply(lambda item: [item])

interpol_wanted_df.drop('entity_id', axis=1, inplace=True)
interpol_wanted_df.drop('charge_translation', axis=1, inplace=True)
interpol_wanted_df.drop('nationalities', axis=1, inplace=True)
fbi_wanted_df.drop('path', axis=1, inplace=True)
fbi_wanted_df.drop('legat_names', axis=1, inplace=True)
fbi_wanted_df.drop('locations', axis=1, inplace=True)
fbi_wanted_df.drop('files', axis=1, inplace=True)
fbi_wanted_df.drop('coordinates', axis=1, inplace=True)
fbi_wanted_df.drop('uid', axis=1, inplace=True)
fbi_wanted_df.drop('@id', axis=1, inplace=True)
fbi_wanted_df.drop('additional_information', axis=1, inplace=True)
fbi_wanted_df.drop('description', axis=1, inplace=True)
fbi_wanted_df.drop('reward_max', axis=1, inplace=True)
fbi_wanted_df.drop('reward_min', axis=1, inplace=True)

merged_df = pd.concat([interpol_wanted_df, fbi_wanted_df], axis=0, ignore_index=True)
merged_df['weight'].replace(0, None, inplace=True)

# -------------------------------------- SAVE TO ORACLE DATABASE --------------------------------------
try:
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except:  # may have been initialized already
    pass

dsn = cx_Oracle.makedsn(HOST, PORT, sid=SID)
connection = cx_Oracle.connect(user=USERNAME, password=PASSWORD, dsn=dsn)
cursor = connection.cursor()

try:  # Check if table exists
    pd.read_sql(f'SELECT * FROM {TARGET_TABLE}', connection)
except:
    try:
        cursor.execute(SQL_CREATE_STATEMENT_FROM_DATAFRAME(merged_df, TARGET_TABLE))
        print('Table created')
    except Exception as e:
        print('Table not created')
        print(e)

# Write the DataFrame to Oracle database 
insert_statements = SQL_INSERT_STATEMENT_FROM_DATAFRAME(merged_df, TARGET_TABLE)
for statement in insert_statements:
    try:
        cursor.execute(statement)
    except Exception as e:
        print(e)

connection.commit()  # Commit the changes
cursor.close()  # Close the cursor
