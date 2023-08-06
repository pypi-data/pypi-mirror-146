import json
import datetime
import requests, os

absolute_path = os.path.abspath("Lyftrondata")

def openjson(filename):
    with open(filename, "r") as opened_file:
        json_file = json.load(opened_file)
    return json_file


def clean_null(json_file):
    """ THIS METHOD CLEANS ALL THE NULL INSIDE DATA RESPONSE FILES
    Args: 
       json_file(dict/json): file contains all the parsed responses.
    Returns:
        tables[dict]: Null free responses
    """
    tables = dict()
    for table, table_respones in json_file.items():
        cleaned = dict()
        if isinstance(table_respones, list):
            table_respones = table_respones[0]
            
        for key, value in table_respones.items():
            if key.__contains__("1"):
                key = key[:-1]
                print(key)
            if value == None:
                value = "xyzabc"
            cleaned[key] = value
        tables[table] = cleaned
    return tables


def replace(schema_old, schema_new):
    """ THIS METHOD REPLACE ALL OLD SCHEMA WITH NEW_SCHEMA UPDATES
    Args:
        schema_old(dict/json): old schema file.
        schema_new(dict/json): new schema file.
    Returns:
        schema[dict]: returns old schema file with current changes in new schema.
    """
    for key, value in schema_new['Tables'].items():
        schema_old['Tables'][key] = value
    schema_old['Methods'] = schema_new['Methods']
    return schema_old


def __flatten(data, parent_key='', sep='_'):
    """THIS METHOD FLATTEN ALL THE NESTED RESPONSE
    Args:
        data[dict]: complete nested response.
        parent_key[string]: fixed parameter.
        sep[string]: add _ after every child key concat.
    Returns:
        dict[dict]: flatten dictonaray 
    """
    from collections import abc

    items = []
    for k, v in data.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, abc.MutableMapping):
            items.extend(__flatten(v, new_key, sep=sep).items())
        elif isinstance(v, abc.MutableSequence):
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)


def parse_json(json_file):

    parsedJson = dict()

    for key, value in json_file.items():
        parsedJson[key] = __flatten(value)
    return parsedJson


def writeJson(filename, json_file):
    with open(filename, "w") as opened_file:
        json.dump(json_file, opened_file)
    return True


def addConstraint(filename):
    """ THIS METHOD ADD ALL THE CONSTRAINTS IN SCHEMA BY USING ENDPOINTS AS A REFERENCE
        Note: ENDPOINT AND SCHEMA FILE MUST BE INSIDE SAME FOLDER 
    Args:
        filename(string): name of connector file
    return:
        schema_file(dict) : returns updated schema dictonaray with constraint inside
    """
    endpoint_file = openjson(f"{absolute_path}/{filename}/lib/Lyftrondata_{filename}_Connector_endpoints.json")
    schema_file = openjson(f'{absolute_path}/{filename}/schema/Lyftrondata_{filename}_Connector_schema.json')
    mismatched = list()
    print(f"Total Number of Endpoints :{len(endpoint_file['views'])+len(endpoint_file['endpoints'])+len(endpoint_file['nested_endpoints'])}")
    print(f"Total Number of Table in Schema :{len(schema_file['Tables'])}")

    for table, table_data in endpoint_file['views'].items():
        if table not in schema_file['Tables']:
            mismatched.append(table)
        else:
            for col in schema_file['Tables'][table]['columns']:
                if col['column'] == table_data['replace_to']:
                    col['constraint'] = f"FOREIGN KEY ({table_data['replace_to']}) REFERENCES {table_data['from_endpoint_name']}({table_data['replace_from']})"

            for col in schema_file['Tables'][table_data['from_endpoint_name']]['columns']:
                if col['column'] == table_data['replace_from']:
                    col['constraint'] = "PRIMARY KEY"
    print(mismatched)
    writeJson(f'{absolute_path}/{filename}/schema/Lyftrondata_{filename}_Connector_schema.json', schema_file)


def req(url):
    token = None
    header = {'Authorization': f'Bearer {token}'}
    req = requests.request("GET", url, headers=header)
    if not req:
        return {}
    else:
        return req.json()


def check_data_type(val):

    if type(val) is int:
        datatype = "int"
        return datatype

    elif type(True) == type(val) or type(False) == type(val):
        datatype = "boolean"
        return datatype

    elif val == "":
        return "varchar(255)"

    elif type(val) is str:
        try:
            datetime.datetime.strptime(val, "%Y-%m-%dT%H:%M:%S")
            datatype = "datetime"
            return datatype

        except:
            datatype = "varchar(255)"
            return datatype
    else:
        datatype = "varchar(255)"
        return datatype


def createSchemafromEndpoints(endpoint_json, endpointjson_keys=None):
    endpoints = {
    }
    for endpoint_Name, endpoint_url in endpoint_json.items():
        endpoints_data = req(endpoint_url)
        if type(endpoints_data) == dict:
            endpoints[endpoint_Name] = endpoints_data

        elif type(endpoints_data) == list:
            if not endpoints_data:
                endpoints[endpoint_Name] = {}
            else:
                endpoints[endpoint_Name] = endpoints_data[0]

    create_schema(endpoints, endpointjson_keys)


def create_schema(filename, endpoints, endpoints_keys=None):

    jsn = {
        "Tables": {}
    }

    schema_path = f"{absolute_path}/{filename}/schema/Lyftrondata_{filename}_Connector_schema.json"
    
    def table_info(file, table_name, columns):
        file['Tables'].update({
            table_name: {
                "datatype": "table",
                            "columns": columns
            }
        }
        )

    def column_info(keys, constraint, values, description):
        datatype = check_data_type(values)
        col_info = {
            "column": keys,
            "constraint": constraint,
            "datatype": datatype,
            "description": description
        }

        return col_info

    def addkey():
        for k, v in endpoints_keys.items():
            datatype = check_data_type(endpoints[k][v])
            key = {
                "column": v,
                "constraint": f"FOREIGN KEY ({v}) REFERENCES {k}({v})",
                "datatype": datatype,
                "description": ""
            }
        return key

    for endpointName, endpoint_json in endpoints.items():
        cols = []

        if endpoints_keys is not None:
            for i, j in endpoints_keys.items():
                if endpointName == i:
                    pass
                else:
                    cols.append(addkey())
        print("Creating schema of " + endpointName)

        if not endpoint_json:
            cols = []
            table_info(jsn, endpointName, cols)

        for endpoint_key, endpoint_value in endpoint_json.items():

            if type(endpoint_value) is list:
                col = []
                for i in endpoint_value:
                    if not i:
                        col = []
                    else:
                        for key, val in i.items():
                            col.append(column_info(key, "", val, ""))
                if endpoints_keys is not None:
                    col.append(addkey())
                table_info(jsn, endpoint_key, col)

            elif type(endpoint_value) is dict:
                col = []
                for key, val in endpoint_value.items():
                    col.append(column_info(key, "", val, ""))
                if endpoints_keys is not None:
                    col.append(addkey())
                table_info(jsn, endpoint_key, col)

            else:
                if endpoints_keys is not None:
                    for i, j in endpoints_keys.items():
                        if endpointName == i and j == endpoint_key:
                            cols.append(column_info(
                                endpoint_key, "PRIMARY KEY", endpoint_value, ""))
                        elif endpoint_key == j:
                            pass
                        else:
                            cols.append(column_info(
                                endpoint_key, "", endpoint_value, ""))
                else:
                    cols.append(column_info(
                        endpoint_key, "", endpoint_value, ""))
            table_info(jsn, endpointName, cols)

    with open(f"{absolute_path}/systemtables.json", "r") as systables:
        tables = json.load(systables)
        
    with open(f"{absolute_path}/methods.json", "r") as methods:
        methods = json.load(methods)
    
    if os.path.exists(schema_path):
        with open(schema_path) as old_schema_file:
            old_schema = json.load(old_schema_file)
            jsn['Tables'].update(old_schema['Tables'])
    
    with open(schema_path, "w") as f:
        jsn['Tables'].update(tables)
        jsn.update(methods)
        json.dump(jsn, f)