#!/bin/bash

org=$1 # sandbox alias
verMin=$2 # which version of the flow does the check start with
verMaxDelta=$3 # how many versions of the flow will not be deleted counting from the active one

# get the active version of the Active flow
echo "Request for Active flow versions"
mapfile resultActive < <(sfdx force:data:soql:query --query "Select DefinitionId, VersionNumber From Flow Where Status =  'Active' AND VersionNumber > $verMin" --targetusername $org --usetoolingapi)

<< RESULT
these first two lines are excluded:
DEFINITIONID VERSIONNUMBER
────────────────── ─────────────
RESULT
let "a=${#resultActive[@]}-2"

# get the active version of Obsolete and Draft flow
echo "Request for Inactive flow versions"
mapfile resultInactive < <(sfdx force:data:soql:query --query "Select ID, DefinitionId, VersionNumber From Flow Where (Status =  'Obsolete' OR Status = 'Draft') AND VersionNumber > $verMin " --targetusername $org --usetoolingapi)
let "b=${#resultInactive[@]}-2"
declare -a flowsArr
echo "I'm starting to process the lists"
for row in "${resultInactive[@]:2:$b}";do
    IFS=' ' read -ra flowInactiv <<< "$row" # we get a string divided into an array - Inactiv flow    
    let "verInactiveFlow = ${flowInactiv[2]}" # the version of the inactive flow to check
    for value in "${resultActive[@]:2:$a}";do
        IFS=' ' read -ra flowActiv <<< "$value" # we get a string divided into an array - Activ flow
        let "verActiveFlowAndDelta = ${flowActiv[1]} - $verMaxDelta" # the version of the active flow with a delta for checking
                
        if [[ "${flowActiv[0]}" = "${flowInactiv[1]}" ]]
        then
            if (( $verInactiveFlow < $verActiveFlowAndDelta ))
            then
                echo "added for deletion ID " ${flowInactiv[0]}           
                flowsArr+=( ${flowInactiv[0]} ) #add "Select ID" form Inactive flow  
            fi          
        fi     
    done    
done

# Delete flows
echo "deletion starts "
echo ${#flowsArr[@]} " flows are removed"
con=0
for flowDelete in "${flowsArr[@]}";do
    con=$((con + 1))
    sfdx force:data:record:delete --sobjecttype Flow --sobjectid $flowDelete --targetusername $org --usetoolingapi 
    echo "there are " $((${#flowsArr[@]}-$con)) " flows left"
done
