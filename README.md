I attempt to understand what is going on here

https://www.quora.com/q/quorahaqathon/Quora-Haqathon-Sorted-Set

> Each `<...>` represents a four byte unsigned integer in [network byte order](http://www.tutorialspoint.com/unix_sockets/network_byte_orders.htm)* sent or received on the socket. All client -> server and server -> client commands are prefixed with the number of fields in the command.



Command to run for './sample'

```bash
python echo_server.py
```

```bash
echo hello | socat -t 2 ./socket -
```



Command to run for './haqathon'

```bash
python server.py
```

```bash
python client.py < sample.in > sample.out
diff sample.out sample.ref
rm socket
```



