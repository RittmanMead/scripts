#!/usr/bin/python

""" Security mapping audit for OBIEE 12c. This code will generate a permissions report for all
catalog objects, for the server upon which it is run. It takes the domain home as an argument in
order to generate the report. This code will create data frames out of the two csv files generated
by the security_audit.py code and then show you those rows which only exist on the lower environment,
or whichever environment you'd like to validate against.
1. Run code once on lower environment application server.
2. Run code once again on target migration environment.
3. Move file 'C:\security_mappings.csv or /tmp/security_mappings.csv from target
   migration server to lower environment server and rename it 'security_mappings_02',
   placing it in the same directory as your other security_mappings.csv file.
4. Run security_compare.py and go to 'localhost:5000/sec_audit' to view test results."""


# Imports - please ensure these are installed on all servers
import sys
import socket
import pandas as pd
import webbrowser
import threading
from flask import *
app = Flask(__name__)

# Arguments for security_mappings files
sec_mapping_01 = sys.argv[1]
sec_mapping_02 = sys.argv[2]

# Set dataframe config options
pd.set_option('display.max_colwidth', -1)


# Functions for flask app
@app.route('/sec_audit')
def show_audit():
    df_low = csv_to_dataframe(sec_mapping_01)
    df_high = csv_to_dataframe(sec_mapping_02)
    merged_df = df_low.merge(df_high, how='left', indicator=True)
    filtered_df = merged_df[merged_df['_merge'] == 'left_only']
    data = filtered_df[['Owner', 'Name', 'Path', 'ACL']]
    return render_template('audit_results.html', data=data.to_html(index=False))


# Generate data frames
def csv_to_dataframe(data):
    df = pd.DataFrame(pd.read_csv(data))
    return df


if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    webbrowser.open('http://' + host + ':5000/sec_audit', new=2)
    flask_thread = threading.Thread(target=app.run(host=host))
    flask_thread.start()
