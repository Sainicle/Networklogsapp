from flask import Flask, Response, Request, render_template, request, redirect, session, url_for
import psycopg2
import dns.resolver
import dns
import subprocess
import socket
import subprocess
import requests
import pyotp



app = Flask(__name__) #setup


try:
    connection = psycopg2.connect(
            host = "34.92.135.43",
            port = 5432,
            user = "nakigbgf",
            password = "iBF9myDKqwdoOKv9XyKxBF5wECR7ZfSs",
            dbname = "nakigbgf"
        ) 
    print ("Connected to the Database ")

except psycopg2.Error as e:
    print("Unable to connect to the Database", f"Error: {e}")

#Ticket number value
ticket_number = 100000 



@app.route("/") #routes
def base():

    return render_template('base.html')


# result page of flask
@app.route('/result', methods =['POST'])
def result():
        # taking input from user
        user_input = request.form["user_input"]

        # Ticket number generater
        global ticket_number
        ticket_number += 1

        # Nslookup using python 
        Nslookup = subprocess.run(["nslookup", user_input], capture_output=True, text=True).stdout
        print(Nslookup)
            


        # ipconfig using python    
        ipconfig =  subprocess.run(["ipconfig"],capture_output=True, text=True).stdout
        print( "ipconfig details :-", ipconfig)


        # ping using python
        ping = subprocess.run(["ping", user_input], capture_output=True, text=True).stdout
        print(ping)

        # Traceroute using python 
        tracert = subprocess.run(["tracert", user_input], capture_output= True, text= True).stdout
        print(tracert)

        # what is my public ipv4 address 
        def Address():
            response = requests.get("https://api.ipify.org")
            if response.ok:
                return response.text
            else:
                return "Error getting IP Address"
        print("Myipv4 Address is:", Address())

        # For scanning port using socket library
        def scan(user_input, port):
            try:
                s = socket.create_connection((user_input, port), timeout=5)
                return f"Port {port} is open on {user_input}"
            except:
                return f"Port {port} is closed on {user_input}"
        
        ports = [80, 443]
        
        port_scan = [scan(user_input, port) for port in ports]
        portresult= "\n".join(port_scan)
        print(portresult)


        # postgresql connection 
        connection = psycopg2.connect(
            host = "34.92.135.43",
            port = 5432,
            user = "nakigbgf",
            password = "iBF9myDKqwdoOKv9XyKxBF5wECR7ZfSs",
            dbname = "nakigbgf"
        ) 
        # print("sucessfully connnected database")



        # postgresql inserting data intotable table
        cursor = connection.cursor()
        cursor.execute("INSERT INTO networklogs (TTnum, url, ipconfig, tracert, ping, nslookup, what_is_my_ip, port_scan ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (ticket_number, user_input, ipconfig, tracert, ping, Nslookup, Address(), portresult))
        connection.commit()
        cursor.close()
        connection.close()

        
        #
        # return result page displaying userdefined input
        return render_template("result.html",input = user_input, ticket_number=ticket_number)
    



#######################

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
