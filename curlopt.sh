#!/bin/bash
 # Bash Menu Script Example 
 PS3='Please enter your choice: ' options=("Run App 1" "Test App 2" "Get Post signed URL 3" "Check Resource 4" "Upload 5" "Download Resource 6" "Exit 7")
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
     "Upload 5") 
        echo "curl -T filename https://goatfish100.s3.amazonaws.com/signed_URL"
        break
        ;;
     "Download Resource 6") 
        echo "curl https://goatfish100.s3.amazonaws.com/signed_URL"
        break
        ;;        
     "Exit 7")
	echo 'bye'
        break
        ;;        
    esac
done
