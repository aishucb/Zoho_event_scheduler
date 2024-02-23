from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
app = Flask(__name__)

def create_accesstoken():
    token_endpoint = "https://accounts.zoho.in/oauth/v2/token"

    token_params = {
        "refresh_token": "1000.47d85ac27064b6801c5134ac81e98587.1da31f9e2abe7082ff45096368b75da8",
        "grant_type": "refresh_token",
        "client_id": "1000.BQNB81JIEWQ777VETFRY0NOEN79MBS",
        "client_secret": "eaab72e5f57e58628e250ad5f1f0357ca43f7fb881",
        "redirect_uri": "https://www.google.co.in/"
    }

    response = requests.post(token_endpoint, data=token_params)
    if response.status_code == 200:
        access_token_data = response.json()
        access_token = access_token_data.get("access_token")
        if access_token:
            return access_token
        else:
            print("Access token not found in the API response.")
    else:
        print("Failed to generate the access token.")
        print(response.status_code, response.json())
    return None

def create_zoho_connect_event(access_token, scope_id, group_id ,title, start_year, start_month, start_date, start_hour, start_min, end_year, end_month, end_date, end_hour, end_min,interval):
    url = "https://connect.zoho.in/pulse/api/addEvent"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    params = {
        "scopeID": scope_id,
        "title": title,
        "startYear": start_year,
        "startMonth": start_month,
        "startDate": start_date,
        "startHour": start_hour,
        "startMin": start_min,
        "endYear": end_year,
        "endMonth": end_month,
        "endDate": end_date,
        "endHour": end_hour,
        "endMin": end_min,
        "intervalDay": interval,
        "partitionId":group_id
    }

    response = requests.post(url, headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def teamnames():
    access_token = create_accesstoken()

    # Replace 'your_scope_id' with the actual scope ID
    scope_id = '34903000000002003'
    url = f'https://connect.zoho.in/pulse/api/allGroups?scopeID={scope_id}'

    # Headers with authorization information
    headers = {
        'Authorization': f'Zoho-oauthtoken {access_token}',
        'Content-Type': 'application/json',
    }

    # Make a GET request to get all groups
    response = requests.get(url, headers=headers)

    # Dictionary to store group information
    group_dict = {}

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            # Parse the response JSON
            all_groups = response.json().get('allGroups', {}).get('groups', [])

            # Display or process information about all groups
            for group in all_groups:
                group_id = group.get('id')
                group_name = group.get('name')
                group_desc = group.get('desc', 'N/A')
                group_status = group.get('status')

                # Add group information to the dictionary
                group_dict[group_id] = {'name': group_name, 'description': group_desc, 'status': group_status}

                # Display or process information about admin users
                

        except Exception as e:
            print(f"Error parsing response: {e}")
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

    return group_dict

@app.route('/')
def index():
    groups = teamnames()
    return render_template('index.html', groups=groups)
    


@app.route('/create_event', methods=['POST'])
def create_event():
    try:
        access_token = create_accesstoken()
        title = request.form.get('event_title')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        repeat_option = request.form.get('repeat_option')
        group_id = request.form.get('selected_team')
        scope_id = "34903000000002003"

        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        start_hour = start_date.hour
        start_min = start_date.minute

        # Parse end date
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        end_hour = end_date.hour
        end_min = end_date.minute

        print(f"Access Token: {access_token}")
        print(f"Title: {title}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Group ID: {group_id}")
        print(f"Scope ID: {scope_id}")

        access_token = create_accesstoken()  # Ensure you need to recreate the token here
        create_zoho_connect_event(access_token, scope_id, group_id, title, start_year, start_month, start_day, start_hour, start_min, end_year, end_month, end_day, end_hour, end_min, repeat_option)

        group_id = 34903000000002004
        result = create_zoho_connect_event(access_token, scope_id, group_id, title, start_year, start_month, start_day, start_hour, start_min, end_year, end_month, end_day, end_hour, end_min, repeat_option)

        print(f"Result: {result}")
        return jsonify(result)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
