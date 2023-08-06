import os
from httplib2 import Http


def get_service(service_name='sheets', version='v4'):
    """
    Setup the Sheets API. Construct a Resource for interacting with an API.

    :return: A Resource object with methods for interacting with the service.
    """
    # Scope of access for the resource object being built
    from oauth2client import file, client, tools
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/spreadsheets.readonly',
              'https://www.googleapis.com/auth/drive.file']
    current_dir = os.path.dirname(__file__)
    token = os.path.join(current_dir, 'resources/', 'token.json')
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        secrets = os.path.join(current_dir, 'resources/', 'spreadsheet_secrets.json')
        flow = client.flow_from_clientsecrets(secrets, scopes)
        creds = tools.run_flow(flow, store)
    from googleapiclient.discovery import build
    service = build(service_name, version, http=creds.authorize(Http()))
    return service


def get_rows(id, worksheet, cols):
    """
    Get all the rows from the sheet of the Google spreadsheet

    :param str id: ID of the spreadsheet
    :param int cols: Number of columns(starting from column 'A') that are to be included in the returned result
    :return: a list of lists representing the rows that were read
    """
    rows = []
    from googleapiclient.errors import HttpError
    try:
        last_column = chr(ord('A') + cols - 1)
        range = worksheet + '!A2:' + last_column
        result = get_service().spreadsheets().values().get(spreadsheetId=id, range=range).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            for row in values:
                try:
                    rows.append(row[:cols])
                except:
                    pass
    except HttpError as e:
        if e.resp.get('status') and int(e.resp.get('status')) == 404:
            print('The Sheet with ID {} could not be found.'.format(id))
    return rows


def write_rows(id, rows, worksheet):
    """
    Explicitly overrides the rows of a google sheet.
    The rows are overriden left-to-right. i.e. Row 'A' till the length of each row passed to this function.

    :param str id: ID of the spreadsheet
    :param list(list) rows: rows to be written to the spreadsheet in Google sheets
    :param Tag worksheet: Type of tag that will decide which worksheet will be written to in the spreadsheet
    """
    if rows and len(rows) > 0:
        size = len(rows[0])
        last_column = chr(ord('A') + size - 1)
        # Determine the range of cells which have to be written to
        range = worksheet + '!A2:' + last_column
        body = {
            'values': rows
        }
        result = get_service().spreadsheets().values().update(
            spreadsheetId=id, range=range,
            valueInputOption='USER_ENTERED', body=body).execute()
        print('{0} rows written to.'.format(result.get('updatedRows')))
        print('{0} cells written to.'.format(result.get('updatedCells')))


def clear_rows(id, worksheet, cols):
    """
    Explicitly overrides the rows of a google sheet.
    The rows are overriden left-to-right. i.e. Row 'A' till the length of each row passed to this function.

    :param str id: ID of the spreadsheet
    :param IssueType worksheet: tag for which the rows have to be cleared.
                          This will decide the worksheet which will be cleared in the spreadsheet
    :param int cols: Number of columns starting from column 'A' which have to be cleared
    """
    last_column = chr(ord('A') + cols - 1)
    # Determine the range of cells which have to be cleared
    range = worksheet + '!A2:' + last_column
    get_service().spreadsheets().values().clear(spreadsheetId=id, range=range).execute()


def append_rows(id, worksheet, rows):
    """
    Append rows to an existing worksheet in a Google spreadsheet.

    :param str id: ID of the spreadsheet
    :param Tag worksheet: tag for which the rows have to be cleared.
                    This will decide the worksheet which will be cleared in the spreadsheet
    :param list(list) rows: rows to be written to the spreadsheet in google sheets
    """
    if rows:
        # How the input data should be inserted.
        if get_rows(id, worksheet, 2):
            insert_data_option = 'INSERT_ROWS'
        else:
            insert_data_option = 'OVERWRITE'
        size = len(rows[0])
        last_column = chr(ord('A') + size - 1)
        # Determine the range of cells which have to be appended to
        range = worksheet + '!A:' + last_column
        # How the input data should be interpreted.
        value_input_option = 'RAW'
        body = {
            'values': [[str(item) for item in row if row] for row in rows]
        }
        result = get_service().spreadsheets().values().append(spreadsheetId=id, range=range,
                                                              valueInputOption=value_input_option,
                                                              insertDataOption=insert_data_option,
                                                              body=body).execute()
        print('{0} rows appended.'.format(result.get('updates').get('updatedRows')))
        print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))


def create_spreadsheet(title, sheet_names):
    """
    Creates a spreadsheet in Google sheets

    :param title: Title to be set on the sheet
    :param sheet_names: Names of the worksheets within the google sheet
    :raises AssertionError in case the creation of the sheet did not go through
    :return: tuple(spreadsheet ID, spreadsheet URL)
    """
    spreadsheet_body = {
        "properties": {
            "title": title
        },
        "sheets": [{"properties": {"title": name}} for name in sheet_names]
    }

    request = get_service().spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    assert type(response) == dict and response['spreadsheetId'] and response['properties']['title'] == title
    return response


def update_title(spreadsheet_id, title):
    """
    Updates the spreadsheet title

    :param spreadsheet_id: ID of the google sheet which has to be modified
    :param title: Title to be set on the spreadsheet
    :raises AssertionError in case the update did not go through successfully
    """
    batch_update_spreadsheet_request_body = {
        # A list of updates to apply to the spreadsheet.
        # Requests will be applied in the order they are specified.
        # If any request is not valid, no requests will be applied.
        'requests': [
            {
                "updateSpreadsheetProperties": {
                    "properties": {
                        "title": title
                    },
                    "fields": "title"
                }
            }
        ],
        "includeSpreadsheetInResponse": True
    }

    request = get_service().spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                       body=batch_update_spreadsheet_request_body)
    response = request.execute()
    # Asserting whether the title was changed or not
    assert type(response) == dict and response['updatedSpreadsheet']['properties']['title'] == title


def give_domain_permissions(spreadsheet_id, domain_name, role):
    """
    Updates the spreadsheet to give a given domain permissions

    :param spreadsheet_id: ID of the google sheet which has to be modified
    :param domain_name: Name of the domain that must be given permission to the file
    :param role: Role for which permission is to be given.
                    Can be :
                    # - organizer
                    # - fileOrganizer
                    # - writer
                    # - reader
    :raises AssertionError in case the update did not go through successfully
    """
    # To give write access, role : writer
    permission_request_body = {
        "domain": domain_name,
        "type": "domain",
        "role": role,
    }

    request = get_service('drive', 'v3').permissions().create(fileId=spreadsheet_id,
                                                              body=permission_request_body)
    response = request.execute()
    # Asserting whether the permission was created or not
    assert type(response) == dict and response['type'] == "domain" and response['role'] == 'writer'


def add_header(spreadsheet_id, sheet_id, headers):
    """
    Updates the spreadsheet title

    :param spreadsheet_id: ID of the google sheet which has to be modified
    :param headers: list of strings which represent the headers for the file
    :raises AssertionError in case the update did not go through successfully
    """
    batch_update_spreadsheet_request_body = {
        # A list of updates to apply to the spreadsheet.
        # Requests will be applied in the order they are specified.
        # If any request is not valid, no requests will be applied.
        'requests': [
            {
                "updateCells": {
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredValue": {
                                        "stringValue": header
                                    },
                                    "userEnteredFormat": {
                                        # Specify yellow background color
                                        "backgroundColor": {
                                            "red": 1,
                                            "green": 1,
                                            "blue": 0,
                                            "alpha": 1
                                        },
                                        # Specify Bold font of size 12
                                        "textFormat": {
                                            "fontSize": 12,
                                            "bold": True,
                                        },
                                        # Wrap the headers
                                        "wrapStrategy": "WRAP"
                                    }
                                } for header in headers]
                        }
                    ],
                    "fields": "*",
                    # Specifying the first row
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(headers)
                    }
                }
            }
        ],
        "includeSpreadsheetInResponse": True
    }

    request = get_service().spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                       body=batch_update_spreadsheet_request_body)
    request.execute()
