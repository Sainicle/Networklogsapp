from flask import Flask, Response, Request, render_template, request, redirect, session
# import sqlite3
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
            password = "7cITWg4h8J3wUFqEYYhEtLcp4GUHqjkS",
            dbname = "nakigbgf"
        ) 
    print ("Connected to the Database ")

except psycopg2.Error as e:
    print("Unable to connect to the Database", f"Error: {e}")

#Ticket number value
ticket_number = 100001 

@app.route("/", methods = ['GET','POST']) #routes
def base():
    if request.method == 'POST':
        print("hello")
        
    
    return render_template('base.html')
#
#unique key generator
# @app.route("/generate_key")
# def generate_key():
#     otp = generate_random_otp()
#     session['otp'] = otp
#     return redirect("/")

# def generate_random_otp():
#     secret_key = pyotp.random_base32()
#     totp = pyotp.TOTP(secret_key)
#     otp = totp.now()
#     return otp 

# @app.route("/validate_otp", methods= ["POST"])
# def validate_otp():
#     entered_otp = request.form["otp"]
#     if 'otp' in session and session['otp'] == entered_otp:
#         return redirect("/")
#     else:
#         return "Invalid OTP. Please try again or generate new OTP"

# result page of flask
@app.route('/result', methods =['POST'])
def getvalue():
        # taking input from user
        name = request.form["name"]
        print (name) 

        # Ticket number generater
        global ticket_number
        ticket_number += 1
    
        # Nslookup using python 
        Nslookup = subprocess.run(["nslookup", name], capture_output=True, text=True).stdout
        print(Nslookup)
            


        # ipconfig using python    
        ipconfig =  subprocess.run(["ipconfig"],capture_output=True, text=True).stdout
        print( "ipconfig details :-", ipconfig)


        # ping using python
        ping = subprocess.run(["ping", name], capture_output=True, text=True).stdout
        print(ping)

        # Traceroute using python 
        tracert = subprocess.run(["tracert", name], capture_output= True, text= True).stdout
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
        def scan(name, port):
            try:
                s = socket.create_connection((name, port), timeout=5)
                return f"Port {port} is open on {name}"
            except:
                return f"Port {port} is closed on {name}"
        
        ports = [80, 443]
        
        port_scan = [scan(name, port) for port in ports]
        portresult= "\n".join(port_scan)
        print(portresult)


        # postgresql connection 
        connection = psycopg2.connect(
            host = "34.92.135.43",
            port = 5432,
            user = "nakigbgf",
            password = "7cITWg4h8J3wUFqEYYhEtLcp4GUHqjkS",
            dbname = "nakigbgf"
        ) 
        print("sucessfully connnected database")



        # postgresql inserting data intotable table
        cursor = connection.cursor()
        cursor.execute("INSERT INTO networklogs (TTnum, url, ipconfig, tracert, ping, nslookup, what_is_my_ip, port_scan ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (ticket_number, name, ipconfig, tracert, ping, Nslookup, Address(), portresult))
        connection.commit()
        cursor.close()
        connection.close()

        
        # sqlite connection
        # connection = sqlite3.connect('Network_data.db')
        # cursor=connection.cursor()
        # print("sucessfully connnected database")

        # inserting user defined query into database
        # cursor.execute("INSERT INTO network (TTnum, url, ipconfig, tracert, ping, nslookup, what_is_my_ip, port_scan ) VALUES (?,?,?,?,?,?,?,?)", (ticket_number, name, ipconfig, tracert, ping, Nslookup, Address(), portresult))
        # connection.commit()
        # connection.close()

        # return result page displaying userdefined input
        return render_template("result.html", n=name, ticket_number=ticket_number)     
    



#######################

if __name__ == "__main__":
    app.run(debug=True)