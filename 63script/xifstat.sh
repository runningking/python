#!/bin/bash
 
eth_in_old=$(ifconfig eth1|grep "RX bytes"|sed 's/RX bytes://'|awk '{print $1}')
eth_out_old=$(ifconfig eth1|grep "RX bytes"|sed 's/.*TX bytes://'|awk '{print $1}')
sleep 1
 
eth_in_new=$(ifconfig eth1|grep "RX bytes"|sed 's/RX bytes://'|awk '{print $1}')
eth_out_new=$(ifconfig eth1|grep "RX bytes"|sed 's/.*TX bytes://'|awk '{print $1}')
eth_in=$(echo "scale=2;($eth_in_new - $eth_in_old)/1000.0" | bc)
eth_out=$(echo "scale=2;($eth_out_new - $eth_out_old)/1000" | bc)
echo "IN: $eth_in KB" "|" "OUT:$eth_out KB"
