#!/usr/bin/python3

# This is a veeeery basic frontend for a bot
# This file should be copied to the /cgi-bin/ folder and given executable permissions for www-data or whichever user runs http
# You also need to create an empty /tmp/chat.txt file and be given write permissions to www-data or whichever user runs http (777 is not sufficient)

import cgi, os, shutil, unicodedata, subprocess, sys, random # Some basic functions
import cgitb; cgitb.enable() # For troubleshooting cgi stuff
from time import sleep

# We get the form data
form = cgi.FieldStorage()

# For printing web events
def my_print(mystr):
   
   print('Content-Type: text/event-stream\n\n\n')
   print('Cache-Control: no-cache\n\n')
   print('data: {"msg":"' + mystr + '"}\n\n', flush='true')

# This function would call a bot
def my_bot(mystr):

   my_bot_response = "Here you call a function"

   return "Response to " + mystr + ": " + my_bot_response


# If there's information in the form
if form:
   
   if 'refresh' in form: # This page with the variable refresh is called by the javascript from the main page
         res = subprocess.run(['/usr/bin/tail', '-30', '/tmp/chat.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Spits out last 50 lines of a file or a message. Simple.
         my_print(res.stdout.decode().replace('\n','<br>'))

   elif 'text' in form: # This page with the variable text is called by the fetch command

      if form['text'].value[0] != '!': # Normal text
         f = open("/tmp/chat.txt", "r")
         lines1 = f.readlines() #for line in lines: print(line.strip())
         f.close()

         f = open("/tmp/chat.txt", "w")
         rawcookies = str(os.environ["HTTP_COOKIE"])
         mycookies = dict([[item.split("=")[0].strip(), item.split("=")[1].strip()] for item in rawcookies.split(";")])
         if "UserID" in mycookies.keys():
            myc = mycookies["UserID"]
         else:
            myc = "Anon"
         f.writelines(lines1 + [str(os.environ["REMOTE_ADDR"]) + "--" + myc + ": " + form["text"].value+'\n']) # Adds lines from file + client IP address + cookie + new text
         f.close()
         
      else: # Here would come the bot
         f = open("/tmp/chat.txt", "r")
         lines1 = f.readlines() #for line in lines: print(line.strip())
         f.close()

         # Here would call the bot passing a text and getting a response

         f = open("/tmp/chat.txt", "w")
         f.writelines(lines1 + [my_bot(form["text"].value) + '\n'])
         f.close()         
         
      
   else:
      print("something")

# If no information in the form, then print the plain webpage
else:

   randomID = random.randrange(1000, 2000, 1) # Generates a random userID from 1000 to 2000 each time the browser is refreshed
   
   print("Set-cookie:UserID=" + str(randomID) + ";") # Sneaks is cookies in the http response (we must follow W3C standards)
   print("Content-Type:text/html\n\n\n") # Indicates the response is html
   
   print ("""
   <!DOCTYPE html>
   <html>
   <head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   </head>
   <body>
   <title>Status de bajadas de videos</title>
   <center>
   <p><h3>Chat comunitario</h3><p>
   </center>

   <div id="my_status">...</div>

   <script>
   // It starts an event listener with an event source as a form with a dummy parameter
   // It waits for an event. When the event comes, it prints the message sent by the event (pin nunber)
   // It displays whatever is sees
   function oper(){
      if(typeof(EventSource) !== "undefined") {

          var source = new EventSource("/cgi-bin/community_chat.py?refresh=true" );
          document.getElementById("my_status").innerHTML = "Wainting for event..." + "<br>";

          source.addEventListener('message', function(e) {
            var data = JSON.parse(e.data);
            document.getElementById("my_status").innerHTML = data.msg + "<br>";            
          }, false);

          source.addEventListener('open', function(e) {
             document.getElementById("my_status").innerHTML += " ";
          }, false);

      } else {
        document.getElementById("my_status").innerHTML = "Sorry, your browser does not support server-sent events...";
      }
   };
   oper();
   </script>


<input type="text" id="link" name="link" style="width: 400px"></textarea>
<button  onclick="show_results();">Enviar</button>

<script>
   // This function is called whenever the user submits text
   function show_results() {
       var mytext = document.getElementById('link').value;
       fetch('http://educagratis.bo/cgi-bin/community_chat.py?text='+ mytext);
       document.getElementById('link').value = ""
   }
</script>
  
</body>
</html>
""")
