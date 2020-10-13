#!/bin/bash
 # Bash Menu Script Example 
 PS3='Please enter your choice: ' options=("Inbound 1" "Outbound 2" "Inbound bad 3" "Outbound bad 4" "Exit 5")
  select opt in "${options[@]}" 
    do case $opt in
     "Inbound 1") 
        curl -d @test/cdr_inbound.json -H "Content-Type: application/json" -X POST http://localhost:8001/data
        break 
        ;; 
     "Outbound 2") 
        curl -d @test/cdr_outbound.json -H "Content-Type: application/json" -X POST http://localhost:8001/data
        break
        ;;
     "Inbound bad 3") 
        curl -d @test/cdr_inbound_missing_compact.json -H "Content-Type: application/json" -X POST http://localhost:8001/data
        break
        ;;
     "Outbound bad 4") 
        curl -d @test/cdr_outbound_missing.json -H "Content-Type: application/json" -X POST http://localhost:8001/data
        break
        ;;        
     "Exit 5")
	echo 'bye'
        break
        ;;        
    esac
done
