#!/bin/bash
# automatic launch of scripts from the directory

org=$1 # sandbox alias
echo "start"

# getting a list of scripts from the current directory
scipts=`ls *.apex`
echo "list of scripts:"
for eachscript in $scipts
do
   echo $eachscript
done

echo "==run=="
for eachscript in $scipts
do
   echo "===== $eachscript is running"
   sfdx force:apex:execute -u $org -f $eachscript > "debug_${eachscript}".txt # running the script and logging
   echo "debug_${eachscript}.txt has been created"
   echo "checking for the condition"
   #  checking for the success of the script execution
   if grep "Executed successfully." debug_${eachscript}.txt; then 
      echo -e "\033[32m $eachscript was executed successfully${NC} \033[0m " 
   else
      echo  -e "\033[31m !!! $eachscript FAILD !!!!${NC} \033[0m " 
      cat debug_${eachscript}.txt
   fi
done
   echo "===== completed ====="


