from flask import Flask, render_template, redirect, url_for, request
import database
import scripts
import index


app = Flask(__name__)


@app.route('/', methods = ['GET','POST'])
def indexpage():
    '''Returns the landing page of the search engine web application'''
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect(url_for('results',query = request.form['query']))

@app.route('/results',methods = ['POST'])
def querypage():
    '''This function handles the query by the user, and displays the results'''
    # Get the query string from the HTML form.
    query = request.form['query_str'] 

    message = None # We will update this with a meaningful error message if one arises
    # Make the connection with the database
    scripts.database.make_connection('cs121project3','localhost',port = 27017)
    
    search_results = [] # We will update this with the results of querying the DB

    ## TEST SNIPPET TO EXAMINE TEMPLATE RENDERING ##
    # search_results = [{
    #     'url' : 'https://google.com',
    #     'title' : 'Hey there!',
    #     'pretty_url' : 'google.com/litsphaghet'
    # }]
    
    try:
        search_results = index.handle_query(query.lower())
    except KeyError: #Our backend service raises a KeyError if the given search term is a stopword or does not appear in the corpus
        message = "No search results found! Given search term is a stopword"
    return render_template('results.html', query_str = query, results = search_results, error_message = message)
    
if __name__ == "__main__":
    app.run(debug=True) #Set debug to False in production env