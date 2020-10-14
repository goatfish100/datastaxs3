#!/bin/bash
 # Bash Menu Script Example 
 PS3='Please enter your choice: ' options=("Run App 1" "Test App 2" "Get Post signed URL 3" "Check Resource 4" "Download Resource 5" "Exit 6")
  select opt in "${options[@]}" 
    do case $opt in
     "Run App 1")
        echo "python3 mainapp.py"
        python3 mainapp.py
        break 
        ;;
        "Test App 2") 
        echo "python3 -m pytest"
        python3 -m pytest
        break 
        ;; 
     "Get Post signed URL 3") 
        echo "curl localhost:5000/s3post/YOUR_OBJ"
        break 
        ;; 
     "Check Resource 4") 
        echo "curl localhost:5000/s3check/morebeermofo"
        break
        ;;
     "Download Resource 5") 
        echo "curl localhost:5000/s3geturl/YOUR_RESOURCE_NAME"
        break
        ;;
     "Exit 6")
	echo 'bye'
        break
        ;;        
    esac
done
